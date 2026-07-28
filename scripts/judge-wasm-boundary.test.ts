// @vitest-environment node
/**
 * Real JS↔WASM boundary test for the judge path.
 *
 * The judge's Rust unit tests construct native structs and the frontend
 * tests mock the WASM module — neither crosses serde_wasm_bindgen, which
 * has its own rules (an explicit `timed_out: undefined` key is NOT
 * "absent"; it once rejected whole batches with "invalid type: unit
 * value"). This suite drives the actual wasm-pack artifact with the exact
 * object shapes the frontend can produce.
 *
 * Self-contained on purpose: it encrypts its OWN pool via the same
 * `encryptPool` + `getPoolKey` path the build uses, because the CI verify
 * job builds the WASM engine but intentionally does NOT run build:pools
 * (see .github/workflows/ci.yml) — docs/public/pools/ is absent there.
 * Requires only the WASM artifact (no skip guard — a gate that silently
 * skips is not a gate; CI builds the artifact before tests).
 */
import { readFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, it, expect } from 'vitest'

import { encryptPool } from './generate-pools.js'
import { getPoolKey } from './pool-key.js'

const ROOT = resolve(import.meta.dirname, '..')
const WASM_DIR = resolve(ROOT, 'docs/public/wasm')
const GLUE_PATH = resolve(WASM_DIR, 'testcase_generator.js')
const WASM_PATH = resolve(WASM_DIR, 'testcase_generator_bg.wasm')

type JudgeWasm = {
  default: (init: { module_or_path: Uint8Array }) => Promise<unknown>
  load_pool: (id: string, data: Uint8Array) => void
  select_testcases: (id: string, count: number) => { inputs: string[]; session_id: string }
  judge: (
    id: string,
    sessionId: string,
    results: unknown,
  ) => Array<{ verdict: string; error?: string; elapsed_ms: number }>
}

let wasm: JudgeWasm | null = null
async function loadJudgeWasm(): Promise<JudgeWasm> {
  if (wasm) return wasm
  const mod: JudgeWasm = await import(`${GLUE_PATH}`)
  await mod.default({ module_or_path: readFileSync(WASM_PATH) })
  wasm = mod
  return mod
}

/** Encrypt a throwaway pool with the SAME key path the build pipeline uses. */
function makePool(id: string, testcases: Array<{ input: string; expected_output: string }>) {
  const key = getPoolKey(ROOT)
  return new Uint8Array(encryptPool(key, id, 'hidden', testcases))
}

const TCS = [
  { input: '1\n', expected_output: 'alpha' },
  { input: '2\n', expected_output: 'beta' },
  { input: '3\n', expected_output: 'gamma' },
]

describe('judge wasm boundary: timed_out survives serde_wasm_bindgen', () => {
  it('WASM artifact is present (run pnpm build:wasm if this fails)', () => {
    expect(existsSync(GLUE_PATH)).toBe(true)
    expect(existsSync(WASM_PATH)).toBe(true)
  })

  it('explicit undefined keys do not break the batch; true → TLE without error; error → RE', async () => {
    const mod = await loadJudgeWasm()
    mod.load_pool('boundary-a', makePool('boundary-a', TCS))
    const sel = mod.select_testcases('boundary-a', 3)
    expect(sel.inputs).toHaveLength(3)

    // Exactly what the frontend collector may produce: non-TLE entries with
    // an explicit `error: undefined` key, plus one structured timeout.
    const results = [
      { stdout: 'definitely wrong output', error: undefined, elapsed_ms: 1.0 },
      { stdout: '', elapsed_ms: 4000.0, timed_out: true },
      { stdout: '', error: 'NameError: x', elapsed_ms: 1.0 },
    ]

    const verdicts = mod.judge('boundary-a', sel.session_id, results)
    expect(verdicts).toHaveLength(3)
    expect(verdicts[0]!.verdict).toBe('WA')
    expect(verdicts[1]!.verdict).toBe('TLE')
    expect(verdicts[1]!.error).toBeUndefined()
    expect(verdicts[2]!.verdict).toBe('RE')
    expect(verdicts[2]!.error).toContain('NameError')
  })

  it('a batch with explicit timed_out: undefined keys still judges (regression)', async () => {
    const mod = await loadJudgeWasm()
    mod.load_pool('boundary-b', makePool('boundary-b', TCS.slice(0, 2)))
    const sel = mod.select_testcases('boundary-b', 2)

    // The shape that once rejected the whole batch with
    // "invalid type: unit value, expected a boolean".
    const results = [
      { stdout: 'alpha', error: undefined, elapsed_ms: 1.0, timed_out: undefined },
      { stdout: 'nope', error: undefined, elapsed_ms: 1.0, timed_out: undefined },
    ]

    const verdicts = mod.judge('boundary-b', sel.session_id, results)
    expect(verdicts).toHaveLength(2)
    for (const v of verdicts) {
      expect(['AC', 'WA']).toContain(v.verdict)
    }
  })
})
