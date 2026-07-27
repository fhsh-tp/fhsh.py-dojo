/**
 * Node-side loader for the testcase-generator WASM module.
 *
 * The build pipeline generates pool inputs with the SAME Rust engine the
 * browser uses (single source of truth) — there is no Python replica of the
 * input-generation logic anymore. The web-target glue is imported via a
 * template-literal dynamic import (so typecheck and unit tests do not
 * require the artifact to exist on disk) and initialized from a byte
 * buffer (Node's fetch cannot load file:// URLs).
 *
 * Initialization is strictly lazy: importing this module never touches the
 * WASM artifact. Only the first call to `generatePoolInputs()` (or
 * `ensureWasmArtifact()`) does.
 */
import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const PROJECT_ROOT = resolve(import.meta.dirname, '..')
const WASM_DIR = resolve(PROJECT_ROOT, 'docs/public/wasm')
const GLUE_PATH = resolve(WASM_DIR, 'testcase_generator.js')
const WASM_PATH = resolve(WASM_DIR, 'testcase_generator_bg.wasm')

/** Pool spec envelope accepted by the WASM `generate_pool_inputs` entry. */
export interface PoolSpec {
  params: Record<string, unknown>
  seed?: string
  input_budget?: number
}

type WasmMod = {
  default: (init: { module_or_path: Uint8Array }) => Promise<unknown>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  generate_pool_inputs: (spec_json: string, count: number) => any
}

let wasmMod: WasmMod | null = null
let initPromise: Promise<WasmMod> | null = null

/**
 * Verify the WASM artifact exists, with an actionable error otherwise.
 * Used by the build script's preflight before any challenge is processed.
 */
export function ensureWasmArtifact(): void {
  if (!existsSync(GLUE_PATH) || !existsSync(WASM_PATH)) {
    throw new Error(
      `[wasm-input-generator] WASM artifact not found at ${WASM_DIR}.\n` +
        '  The build pipeline requires the WASM engine to be built first.\n' +
        '  Run: pnpm build:wasm',
    )
  }
}

async function loadWasm(): Promise<WasmMod> {
  if (wasmMod) return wasmMod
  if (!initPromise) {
    initPromise = (async () => {
      ensureWasmArtifact()
      // Template literal keeps this import dynamic: tsc/vitest resolve it at
      // runtime only, so environments without the artifact can still import
      // this module (and the build script's pure helpers) safely.
      const mod: WasmMod = await import(`${GLUE_PATH}`)
      // The template-literal import bypasses static typing, so verify the
      // contract BEFORE calling into the module: a stale or renamed glue
      // must fail here with a clear message, not with "not a function".
      if (typeof mod.default !== 'function' || typeof mod.generate_pool_inputs !== 'function') {
        throw new Error(
          '[wasm-input-generator] loaded WASM glue is missing expected exports ' +
            '(default init / generate_pool_inputs) — the artifact is stale. Run: pnpm build:wasm',
        )
      }
      await mod.default({ module_or_path: readFileSync(WASM_PATH) })
      wasmMod = mod
      return mod
    })()
  }
  return initPromise
}

/**
 * Generate `count` pool input strings for one challenge.
 *
 * Any engine-side error (parse validation, budget violation) is rethrown
 * with the message intact — callers abort the build; the WASM instance is
 * never reused after a trap.
 */
export async function generatePoolInputs(spec: PoolSpec, count: number): Promise<string[]> {
  const mod = await loadWasm()
  const result = mod.generate_pool_inputs(JSON.stringify(spec), count)
  // Trust boundary: the WASM return shape is untyped (dynamic import).
  // An undersized batch must never silently flow into pool encryption.
  if (!Array.isArray(result?.inputs) || result.inputs.length !== count) {
    throw new Error(
      `[wasm-input-generator] WASM returned ${result?.inputs?.length ?? 'no'} inputs, expected ${count}`,
    )
  }
  return result.inputs as string[]
}
