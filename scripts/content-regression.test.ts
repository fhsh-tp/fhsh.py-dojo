// @vitest-environment node
/**
 * Content-layer regression test.
 *
 * For each challenge that declares a `reference_solution` in its frontmatter,
 * verify that the reference solution, given the exact inputs a student would
 * receive, produces the same output the generator declares as correct. This is
 * the offline equivalent of the reference solution earning an Accepted verdict
 * against the production encrypted pool (the production judge compares student
 * output against the generator's expected output).
 *
 * Challenges lacking `reference_solution` are skipped and counted. The
 * coverage floor (at least one reference solution exists) always runs; only
 * the generator-comparison half skips when python3 or PyYAML is unavailable,
 * matching the `build:pools` preflight behavior. Random inputs come from the
 * WASM engine (same single source of truth as the build pipeline).
 */
import { describe, it, expect } from 'vitest'
import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { resolve, join } from 'node:path'

import { POOL_SIZE, readChallenge, generateInputs, runGenerator } from './generate-pools.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')
const SAMPLE_INPUTS = 20

/**
 * Deterministic, seed-independent-from-the-pool index sampler: FNV-1a on the
 * seed string feeds an LCG; picks `take` distinct indices in [0, size).
 * Deterministic so CI stays stable; decoupled from the pool seed so the
 * sample is not simply the pool's prefix.
 */
function sampleIndices(seedStr: string, size: number, take: number): number[] {
  let h = 0xcbf29ce484222325n
  for (const byte of Buffer.from(seedStr, 'utf-8')) {
    h ^= BigInt(byte)
    h = (h * 0x100000001b3n) & 0xffffffffffffffffn
  }
  let state = h
  const next = () => {
    state = (state * 6364136223846793005n + 1442695040888963407n) & 0xffffffffffffffffn
    return Number((state >> 33n) % BigInt(size))
  }
  const picked = new Set<number>()
  while (picked.size < Math.min(take, size)) picked.add(next())
  return [...picked].sort((a, b) => a - b)
}

function pythonAvailable(): boolean {
  try {
    execFileSync('python3', ['-c', 'import yaml'], { encoding: 'utf-8', timeout: 10_000 })
    return true
  } catch {
    return false
  }
}

const hasPython = pythonAvailable()
const files = existsSync(CHALLENGES_DIR)
  ? readdirSync(CHALLENGES_DIR)
      .filter((f) => f.endsWith('.md'))
      .sort()
  : []

describe('content-layer regression: reference_solution earns AC against generator', () => {
  // Coverage floor runs BEFORE (and independently of) the python3 skip guard:
  // even in an environment without python3, a suite that would validate ZERO
  // reference solutions must fail loudly, not skip into a green no-op. The
  // count comes from a frontmatter text scan so it needs no python3.
  it('coverage floor: at least one challenge declares reference_solution', () => {
    expect(files.length).toBeGreaterThan(0)
    const withRefCount = files.filter((f) =>
      /^reference_solution:/m.test(readFileSync(join(CHALLENGES_DIR, f), 'utf-8')),
    ).length
    console.log(
      `[content-regression] ${withRefCount}/${files.length} challenge(s) declare reference_solution`,
    )
    expect(
      withRefCount,
      'expected at least one challenge to declare reference_solution',
    ).toBeGreaterThan(0)
  })

  if (!hasPython) {
    it.skip('generator comparison skipped — python3 or PyYAML unavailable', () => {})
    return
  }

  const challenges = files.map((f) => readChallenge(join(CHALLENGES_DIR, f)))

  for (const c of challenges) {
    const run = c.reference_solution ? it : it.skip
    run(
      `${c.slug}: reference_solution matches generator on student-facing inputs`,
      async () => {
        // Generate the FULL production pool (same seed as build:pools, so
        // these are exactly the shipped inputs), then sample SAMPLE_INPUTS
        // entries across the whole range with an independent deterministic
        // index sequence. Plain prefix-taking would forever test only the
        // first 10% of every pool; unseeded sampling would make CI flaky.
        const fullPool = await generateInputs(
          { params: c.params, seed: c.slug, input_budget: c.input_budget },
          POOL_SIZE,
        )
        const indices = sampleIndices(`${c.slug}::regression-sample`, POOL_SIZE, SAMPLE_INPUTS)
        const rawInputs = indices.map((i) => fullPool[i]!)
        // Reproducibility breadcrumb for failures.
        console.log(`[content-regression] ${c.slug} sampled indices: ${indices.join(',')}`)
        // The generator yields {input, expected_output}: `input` is what the
        // student actually receives (identity for standard challenges, or the
        // factory-transformed input for JSON-factory challenges).
        const expected = runGenerator(c.generator, rawInputs)
        const studentInputs = expected.map((t) => t.input)
        const actual = runGenerator(c.reference_solution as string, studentInputs)

        expect(actual.length).toBe(expected.length)
        for (let i = 0; i < expected.length; i++) {
          expect(actual[i]!.expected_output.trimEnd()).toBe(expected[i]!.expected_output.trimEnd())
        }
      },
      60_000,
    )
  }
})
