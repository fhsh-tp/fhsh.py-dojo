// @vitest-environment node
/**
 * Real JS↔WASM boundary test for the judge path.
 *
 * The judge's Rust unit tests construct native structs and the frontend
 * tests mock the WASM module — neither crosses serde_wasm_bindgen, which
 * has its own rules (an explicit `timed_out: undefined` key is NOT
 * "absent"; it once rejected whole batches with "invalid type: unit
 * value"). This suite drives the actual wasm-pack artifact with the exact
 * object shapes the frontend can produce, against a real encrypted pool.
 *
 * Requires the WASM artifact and pools (build pipeline guarantees both:
 * gen:keymaterial → build:wasm → build:pools → test). Deliberately no
 * skip guards — a gate that silently skips is not a gate.
 */
import { readFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, it, expect } from 'vitest'

const ROOT = resolve(import.meta.dirname, '..')
const WASM_DIR = resolve(ROOT, 'docs/public/wasm')
const GLUE_PATH = resolve(WASM_DIR, 'testcase_generator.js')
const WASM_PATH = resolve(WASM_DIR, 'testcase_generator_bg.wasm')
const POOL_PATH = resolve(ROOT, 'docs/public/pools/hello-world.bin')

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

describe('judge wasm boundary: timed_out survives serde_wasm_bindgen', () => {
  it('artifacts are present (run pnpm build:wasm / build:pools if this fails)', () => {
    expect(existsSync(GLUE_PATH)).toBe(true)
    expect(existsSync(WASM_PATH)).toBe(true)
    expect(existsSync(POOL_PATH)).toBe(true)
  })

  it('explicit undefined keys do not break the batch; true → TLE without error; error → RE', async () => {
    const mod: JudgeWasm = await import(`${GLUE_PATH}`)
    await mod.default({ module_or_path: readFileSync(WASM_PATH) })

    mod.load_pool('hello-world', readFileSync(POOL_PATH))
    const sel = mod.select_testcases('hello-world', 3)
    expect(sel.inputs).toHaveLength(3)

    // Exactly what the frontend collector may produce: non-TLE entries with
    // an explicit `error: undefined` key, plus one structured timeout.
    const results = [
      { stdout: 'definitely wrong output', error: undefined, elapsed_ms: 1.0 },
      { stdout: '', elapsed_ms: 4000.0, timed_out: true },
      { stdout: '', error: 'NameError: x', elapsed_ms: 1.0 },
    ]

    const verdicts = mod.judge('hello-world', sel.session_id, results)
    expect(verdicts).toHaveLength(3)
    expect(verdicts[0]!.verdict).toBe('WA')
    expect(verdicts[1]!.verdict).toBe('TLE')
    expect(verdicts[1]!.error).toBeUndefined()
    expect(verdicts[2]!.verdict).toBe('RE')
    expect(verdicts[2]!.error).toContain('NameError')
  })

  it('a batch with explicit timed_out: undefined keys still judges (regression)', async () => {
    const mod: JudgeWasm = await import(`${GLUE_PATH}`)
    await mod.default({ module_or_path: readFileSync(WASM_PATH) })

    mod.load_pool('hello-world', readFileSync(POOL_PATH))
    const sel = mod.select_testcases('hello-world', 2)

    // The shape that once rejected the whole batch with
    // "invalid type: unit value, expected a boolean".
    const results = [
      { stdout: 'x', error: undefined, elapsed_ms: 1.0, timed_out: undefined },
      { stdout: 'y', error: undefined, elapsed_ms: 1.0, timed_out: undefined },
    ]

    const verdicts = mod.judge('hello-world', sel.session_id, results)
    expect(verdicts).toHaveLength(2)
    for (const v of verdicts) {
      expect(['AC', 'WA']).toContain(v.verdict)
    }
  })
})
