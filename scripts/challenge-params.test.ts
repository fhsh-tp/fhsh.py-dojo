// @vitest-environment node
/**
 * All-challenge params conformance gate.
 *
 * Every `docs/challenge/*.md` params declaration MUST be accepted by the
 * Rust/WASM engine parser and pass its input-size budget. This replaces the
 * retired generator-parity test as the guard against content-side drift:
 * a challenge declaring a type or field the engine does not support fails
 * HERE, naming the file — instead of silently shipping a degraded pool
 * (the `type: str` → literal "UNKNOWN_TYPE" incident on challenge id 22).
 *
 * Deliberately NO skip guards: a missing WASM artifact or an empty
 * challenge directory is a failure, not a skip — a gate that silently
 * skips is not a gate. The build pipeline (gen:keymaterial → build:wasm →
 * build:pools → test) guarantees the artifact exists in CI.
 */
import { mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { afterAll, describe, expect, it } from 'vitest'

import { buildPoolRequest, computePlanTotal, readChallenge } from './generate-pools.js'
import { ensureWasmArtifact, generatePoolInputs } from './wasm-input-generator.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')

/**
 * Run one challenge declaration through the engine exactly as the pool build
 * does: plan challenges request one full block (TS-computed plan total) with
 * the plan attached, non-plan challenges request a single sample. Returns
 * the generated inputs so callers can assert count consistency.
 */
async function smokeGenerate(filePath: string): Promise<string[]> {
  const challenge = readChallenge(filePath)
  const planTotal =
    challenge.testcase_plan !== undefined
      ? computePlanTotal(challenge.testcase_plan, filePath)
      : undefined
  // Spec comes from the SAME request builder the pool build uses; only the
  // count differs (one sample / one block — this is a smoke gate, not a
  // full pool build).
  const { spec } = buildPoolRequest(challenge, filePath)
  const inputs = await generatePoolInputs(spec, planTotal ?? 1)
  if (planTotal !== undefined) {
    // TS-side plan total and the engine's own computation must agree — a
    // full block came back, so the engine accepted count == planTotal as a
    // multiple of ITS total, which is only possible when the two match.
    expect(inputs).toHaveLength(planTotal)
  }
  return inputs
}

describe('challenge params conformance', () => {
  it('WASM artifact is present (run `pnpm build:wasm` if this fails)', () => {
    expect(() => ensureWasmArtifact()).not.toThrow()
  })

  const files = readdirSync(CHALLENGES_DIR).filter((f) => f.endsWith('.md'))

  it('at least one challenge file exists', () => {
    expect(files.length).toBeGreaterThan(0)
  })

  it.each(files)('%s: params parse and fit the input budget', async (file) => {
    // One generated sample (or one full plan block) proves the declaration
    // parses, passes budget enforcement, and actually renders. Seeded for
    // reproducible failures.
    const inputs = await smokeGenerate(join(CHALLENGES_DIR, file))
    expect(inputs.length).toBeGreaterThan(0)
    expect(typeof inputs[0]).toBe('string')
  })
})

describe('testcase_plan gate logic (fixtures — no plan challenge in repo yet)', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'plan-gate-'))
  afterAll(() => rmSync(tmp, { recursive: true, force: true }))

  function writeFixture(name: string, fm: string): string {
    const filePath = join(tmp, name)
    writeFileSync(
      filePath,
      `---
algorithm: deque-scan
${fm}
generator: |
  n = int(input())
  print(n)
---

body
`,
      'utf-8',
    )
    return filePath
  }

  it('a valid plan challenge generates exactly one block through the gate', async () => {
    const filePath = writeFixture(
      'plan-valid.md',
      `params:
  n:
    type: int
    min: 1
    max: 999
testcase_plan:
  - count: 2
    override:
      n:
        min: 100
        max: 100
  - literal: "7\\n"`,
    )
    const inputs = await smokeGenerate(filePath)
    expect(inputs).toEqual(['100', '100', '7\n'])
  })

  it('a plan/testcase_count coexistence is named and refused', () => {
    const filePath = writeFixture(
      'plan-coexist.md',
      `params:
  n:
    type: int
testcase_count: 5
testcase_plan:
  - count: 2`,
    )
    expect(() => readChallenge(filePath)).toThrow(/mutually exclusive/)
    expect(() => readChallenge(filePath)).toThrow(/plan-coexist\.md/)
  })

  it('an engine-invalid plan fails the gate with the entry index', async () => {
    const filePath = writeFixture(
      'plan-bad-override.md',
      `params:
  n:
    type: int
testcase_plan:
  - count: 2
    override:
      m:
        max: 5`,
    )
    await expect(smokeGenerate(filePath)).rejects.toThrow(/unknown key 'm'/)
  })
})
