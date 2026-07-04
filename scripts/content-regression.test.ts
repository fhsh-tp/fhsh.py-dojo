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
 * Challenges lacking `reference_solution` are skipped and counted. If python3
 * or PyYAML is unavailable, the whole suite skips with a warning rather than
 * failing, matching the `build:pools` preflight behavior.
 */
import { describe, it, expect } from 'vitest'
import { execFileSync } from 'node:child_process'
import { existsSync, readdirSync } from 'node:fs'
import { resolve, join } from 'node:path'

import { readChallenge, generateInputs, runGenerator } from './generate-pools.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')
const SAMPLE_INPUTS = 20

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
  if (!hasPython) {
    it.skip('skipped — python3 or PyYAML unavailable', () => {})
    return
  }

  const challenges = files.map((f) => readChallenge(join(CHALLENGES_DIR, f)))
  const withRef = challenges.filter((c) => c.reference_solution)
  const withoutRef = challenges.filter((c) => !c.reference_solution)

  it('reports coverage', () => {
    console.log(
      `[content-regression] ${withRef.length} challenge(s) with reference_solution; ` +
        `${withoutRef.length} skipped for lacking it.`,
    )
    expect(challenges.length).toBeGreaterThan(0)
    // Coverage floor: the suite exists to compare reference solutions against
    // generators. If it validates ZERO of them (field dropped, all null), it is
    // silently vacuous — fail rather than report a green no-op.
    expect(
      withRef.length,
      'expected at least one challenge to declare reference_solution',
    ).toBeGreaterThan(0)
  })

  for (const c of challenges) {
    const run = c.reference_solution ? it : it.skip
    run(
      `${c.slug}: reference_solution matches generator on student-facing inputs`,
      () => {
        const rawInputs = generateInputs(c.params, SAMPLE_INPUTS)
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
