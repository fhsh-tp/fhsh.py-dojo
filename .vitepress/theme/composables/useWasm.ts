/** Result returned by generate_challenge WASM function (new format). */
export interface GeneratedInputs {
  inputs: string[]
}

type WasmMod = {
  default: () => Promise<void>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  generate_challenge: (params_json: string, count: number) => any
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  generate_dev_inputs?: (spec_json: string) => any
}

// Module-level cache — shared across all composable instances
let wasmModule: WasmMod | null = null
let wasmInitPromise: Promise<void> | null = null

/** Dynamic import using template literal so Vite cannot statically resolve the path. */
const WASM_MOD_PATH = '/wasm/testcase_generator.js'
const _loadWasmMod: () => Promise<WasmMod> = () =>
  import(/* @vite-ignore */ `${WASM_MOD_PATH}`)

/**
 * Lazily loads the WASM module once and caches it.
 * Concurrent callers await the same init promise to avoid double-init.
 */
export function useWasm(loaderOverride?: () => Promise<WasmMod>) {
  const loader = loaderOverride ?? _loadWasmMod

  async function loadWasm(): Promise<void> {
    if (wasmModule) return
    if (!wasmInitPromise) {
      wasmInitPromise = (async () => {
        const mod = await loader()
        await mod.default()
        wasmModule = mod
      })()
    }
    await wasmInitPromise
  }

  /**
   * Generate random input strings from a JSON params specification.
   * @param params_json - JSON-serialised params object from frontmatter
   * @param count - number of testcase inputs to generate
   */
  async function generateChallenge(
    params_json: string,
    count: number,
  ): Promise<GeneratedInputs | null> {
    await loadWasm()
    if (!wasmModule) return null
    try {
      const result = wasmModule.generate_challenge(params_json, count)
      return typeof result === 'object' ? result : JSON.parse(result)
    } catch (e) {
      console.error('[useWasm] generate_challenge error:', e)
      return null
    }
  }

  /**
   * Generate one full testcase_plan round (dev mode for plan challenges).
   * @param spec_json - JSON-serialised `{ params, testcase_plan }` object
   */
  async function generateDevInputs(spec_json: string): Promise<GeneratedInputs | null> {
    await loadWasm()
    if (!wasmModule) return null
    if (typeof wasmModule.generate_dev_inputs !== 'function') {
      console.error('[useWasm] generate_dev_inputs missing — stale WASM artifact, run pnpm build:wasm')
      return null
    }
    try {
      const result = wasmModule.generate_dev_inputs(spec_json)
      return typeof result === 'object' ? result : JSON.parse(result)
    } catch (e) {
      console.error('[useWasm] generate_dev_inputs error:', e)
      return null
    }
  }

  return { loadWasm, generateChallenge, generateDevInputs }
}
