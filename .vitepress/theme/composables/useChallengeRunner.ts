/**
 * useChallengeRunner — unified orchestration layer for challenge lifecycle.
 *
 * Abstracts over two strategies:
 * - Dev: WASM inputs → Pyodide generator → JS comparison (existing flow)
 * - Prod: fetch encrypted pool → WASM decrypt/select → student code → WASM judge
 *
 * ChallengeView uses this composable instead of directly touching WASM, Workers, or generators.
 */
import { ref, type Ref } from 'vue'
import { createInterruptChannel, DeadlineWatchdog } from '../workers/deadline'
import { useChallengeStore } from '../stores/challenge'
import { useExecutorStore } from '../stores/executor'
import { useWasm, type GeneratedInputs } from '../composables/useWasm'
import type {
  GenerateRequest,
  GenerateComplete,
  TestcaseResult,
  RunRequest,
  RunComplete,
  VerdictDetail,
  TestcaseStart,
} from '../workers/pyodide.worker'

export type { VerdictDetail }

export interface ChallengeConfig {
  /**
   * Per-challenge unique slug — the markdown file basename with `.md` removed
   * (e.g. `multiplication-table`). Used as the sole pool fetch / WASM session
   * key. Required; there is intentionally no fallback to `algorithm` because
   * multiple challenges share `algorithm` values and falling back would
   * re-introduce the cross-challenge pool collision this type is designed to
   * prevent.
   */
  id: string
  /** Educational categorization (e.g. `nested-loop`). Metadata only — NOT used as a pool key. */
  algorithm: string
  params: Record<string, unknown>
  generator: string
  testcaseCount: number
  starterCode: string
  verdictDetail: VerdictDetail
  /**
   * Optional testcase partition plan from frontmatter (band/literal entries).
   * When present the effective per-session testcase count is the plan total
   * (band counts summed, one per literal) — `testcaseCount` is ignored — and
   * both strategies switch to plan-aware WASM entries.
   */
  testcasePlan?: unknown[]
}

/**
 * Plan total = Σ band counts + one per literal entry. Mirrors the engine's
 * rule; the engine independently validates (count must equal the pool's
 * plan_block_size in prod), so any drift here fails loudly instead of
 * silently degrading. Invalid entries yield NaN, which also fails loudly.
 */
export function computePlanTotal(plan: unknown[]): number {
  let total = 0
  for (const entry of plan) {
    const e = entry as Record<string, unknown>
    if (e !== null && typeof e === 'object' && 'literal' in e) {
      total += 1
    } else {
      total += typeof e?.count === 'number' ? (e.count as number) : NaN
    }
  }
  return total
}

/** Effective per-session testcase count: plan total when a plan is declared. */
function effectiveTestcaseCount(config: ChallengeConfig): number {
  return config.testcasePlan !== undefined
    ? computePlanTotal(config.testcasePlan)
    : config.testcaseCount
}

/** Return type exposed to ChallengeView */
export interface ChallengeRunner {
  loadTestcases(): Promise<void>
  submit(code: string): Promise<void>
  stop(): void
  inputs: Ref<string[]>
  isReady: Ref<boolean>
  isRunning: Ref<boolean>
  errorMessage: Ref<string>
  verdictDetail: Ref<VerdictDetail>
  cleanup(): void
}

const VALID_VERDICT_DETAILS = new Set<VerdictDetail>(['hidden', 'actual', 'full'])
const WALL_CLOCK_KILL_MS = 6_000

export function resolveVerdictDetail(raw: string | undefined): VerdictDetail {
  const v = raw ?? 'hidden'
  return VALID_VERDICT_DETAILS.has(v as VerdictDetail) ? (v as VerdictDetail) : 'hidden'
}

// ── WASM module types for pool/judge (loaded dynamically in prod) ──────────

type WasmPoolMod = {
  default: () => Promise<void>
  load_pool: (challenge_id: string, data: Uint8Array) => void
  select_testcases: (challenge_id: string, count: number) => { inputs: string[]; session_id: string; verdict_detail: string }
  judge: (challenge_id: string, session_id: string, results: unknown[]) => unknown[]
  get_expected: (challenge_id: string, session_id: string, index: number) => string | null
}

const WASM_MOD_PATH = '/wasm/testcase_generator.js'

let wasmPoolMod: WasmPoolMod | null = null
let wasmInitPromise: Promise<void> | null = null

async function ensureWasmPool(): Promise<WasmPoolMod> {
  if (wasmPoolMod) return wasmPoolMod
  if (!wasmInitPromise) {
    wasmInitPromise = (async () => {
      const mod = await import(/* @vite-ignore */ `${WASM_MOD_PATH}`) as WasmPoolMod
      await mod.default()
      wasmPoolMod = mod
    })()
  }
  await wasmInitPromise
  return wasmPoolMod!
}

// ── Factory ────────────────────────────────────────────────────────────────

export function useChallengeRunner(config: ChallengeConfig): ChallengeRunner {
  const isProd = import.meta.env.PROD

  if (isProd) {
    return useProdRunner(config)
  } else {
    return useDevRunner(config)
  }
}

// ── Dev Strategy ───────────────────────────────────────────────────────────
// Preserves existing flow: WASM inputs → Pyodide generator → JS comparison

function useDevRunner(config: ChallengeConfig): ChallengeRunner {
  const challengeStore = useChallengeStore()
  const executorStore = useExecutorStore()
  const { generateChallenge, generateDevInputs } = useWasm()

  const inputs = ref<string[]>([])
  const isReady = ref(false)
  const isRunning = ref(false)
  const errorMessage = ref('')

  let localTestcases: Array<{ input: string; expected_output: string }> = []
  let activeWorker: Worker | null = null
  // Hoisted references for submission worker stop/cancel support
  let submitWorker: Worker | null = null
  let submitKillTimerId: ReturnType<typeof setTimeout> | null = null
  let submitInflightResolve: (() => void) | null = null

  async function loadTestcases() {
    if (!config.generator) {
      errorMessage.value = 'generator 程式碼未設定，請在 frontmatter 中加入 generator 欄位'
      return
    }

    // Plan challenges preview one full plan round (declaration order, values
    // random per load); non-plan challenges keep the historical entropy flow.
    const generated =
      config.testcasePlan !== undefined
        ? await generateDevInputs(
            JSON.stringify({ params: config.params, testcase_plan: config.testcasePlan }),
          )
        : await generateChallenge(JSON.stringify(config.params), config.testcaseCount)

    if (!generated) {
      errorMessage.value =
        config.testcasePlan !== undefined
          ? 'WASM 生成失敗，請確認 params 與 testcase_plan 格式正確'
          : 'WASM 生成失敗，請確認 params 格式正確'
      return
    }

    const testcases = await runGenerator(config.generator, generated.inputs)

    if (testcases === null) {
      errorMessage.value = 'Generator 執行失敗，請確認 generator 程式碼正確'
      return
    }

    localTestcases = testcases
    inputs.value = testcases.map((tc) => tc.input)

    const storeTestcases =
      config.verdictDetail === 'full'
        ? testcases
        : testcases.map((tc) => ({ input: tc.input }))
    challengeStore.setCurrentChallenge({ starter_code: config.starterCode, testcases: storeTestcases })
    isReady.value = true
  }

  function runGenerator(
    generatorCode: string,
    genInputs: string[],
  ): Promise<Array<{ input: string; expected_output: string }> | null> {
    return new Promise((resolve) => {
      const worker = new Worker(new URL('../workers/pyodide.worker.ts', import.meta.url), {
        type: 'module',
      })
      activeWorker = worker

      worker.onmessage = (event: MessageEvent<GenerateComplete>) => {
        if (event.data.type === 'generate_complete') {
          activeWorker = null
          worker.terminate()
          const testcases = event.data.testcases.map((tc) => {
            if (tc.error) {
              console.error('[generator] error for input:', tc.input, tc.error)
            }
            return { input: tc.input, expected_output: tc.expected_output }
          })
          resolve(testcases)
        }
      }

      worker.onerror = () => {
        activeWorker = null
        worker.terminate()
        resolve(null)
      }

      const req: GenerateRequest = { type: 'generate', generatorCode, inputs: genInputs }
      worker.postMessage(req)
    })
  }

  async function submit(code: string) {
    if (!localTestcases.length) return
    isRunning.value = true
    executorStore.setRunning(localTestcases.length)

    await new Promise<void>((resolve) => {
      const worker = new Worker(new URL('../workers/pyodide.worker.ts', import.meta.url), {
        type: 'module',
      })
      submitWorker = worker
      submitInflightResolve = resolve

      function settle() {
        submitWorker = null
        submitKillTimerId = null
        submitInflightResolve = null
      }

      const totalBudget = localTestcases.length * WALL_CLOCK_KILL_MS

      // Per-testcase deadline for the dev submit path. This is where dev-mode
      // submissions actually run — `useExecutor.run()` looks like the submit
      // path but has no callers, so wiring the watchdog there alone would have
      // left every dev submission with elapsed-only adjudication.
      const channel = createInterruptChannel()
      const watchdog = new DeadlineWatchdog(channel)

      submitKillTimerId = setTimeout(() => {
        watchdog.dispose()
        worker.terminate()
        executorStore.setDone(executorStore.totalTestcases, executorStore.passedCount)
        isRunning.value = false
        settle()
        resolve()
      }, totalBudget)

      worker.onmessage = (event: MessageEvent<TestcaseStart | TestcaseResult | RunComplete>) => {
        const msg = event.data
        if (msg.type === 'testcase_start') {
          watchdog.arm(msg.generation)
        } else if (msg.type === 'testcase_result') {
          watchdog.disarm()
          executorStore.addResult(msg)
        } else if (msg.type === 'run_complete') {
          if (submitKillTimerId !== null) clearTimeout(submitKillTimerId)
          watchdog.dispose()
          executorStore.setDone(msg.total, msg.passed)
          worker.terminate()
          isRunning.value = false
          settle()
          resolve()
        }
      }

      worker.onerror = () => {
        if (submitKillTimerId !== null) clearTimeout(submitKillTimerId)
        watchdog.dispose()
        executorStore.setDone(executorStore.totalTestcases, executorStore.passedCount)
        worker.terminate()
        isRunning.value = false
        settle()
        resolve()
      }

      const request: RunRequest = {
        type: 'run',
        code,
        testcases: localTestcases.map((tc) => ({
          input: tc.input,
          expected_output: tc.expected_output,
        })),
        verdictDetail: config.verdictDetail,
        ...(channel.buffer === null ? {} : { interruptBuffer: channel.buffer }),
      }
      worker.postMessage(request)
    })
  }

  function stop() {
    // Terminate generator-phase worker if active
    activeWorker?.terminate()
    activeWorker = null
    // Terminate submission worker and cancel killTimer if in-flight
    if (submitKillTimerId !== null) {
      clearTimeout(submitKillTimerId)
      submitKillTimerId = null
    }
    submitWorker?.terminate()
    submitWorker = null
    if (submitInflightResolve) {
      const r = submitInflightResolve
      submitInflightResolve = null
      r()
    }
    isRunning.value = false
  }

  function cleanup() {
    stop()
    // Null out all references to prevent stale callbacks after unmount
    activeWorker = null
    submitWorker = null
    submitKillTimerId = null
    submitInflightResolve = null
  }

  return { loadTestcases, submit, stop, inputs, isReady, isRunning, errorMessage, verdictDetail: ref(config.verdictDetail) as Ref<VerdictDetail>, cleanup }
}

// ── Prod Strategy ──────────────────────────────────────────────────────────
// Encrypted pool → WASM decrypt/select → student code → WASM judge

function useProdRunner(config: ChallengeConfig): ChallengeRunner {
  const challengeStore = useChallengeStore()
  const executorStore = useExecutorStore()

  const inputs = ref<string[]>([])
  const isReady = ref(false)
  const isRunning = ref(false)
  const errorMessage = ref('')
  const poolVerdictDetail = ref<VerdictDetail>('hidden')

  let sessionId = ''
  let runWorker: Worker | null = null
  // Hoisted references for stop/cancel support
  let prodKillTimerId: ReturnType<typeof setTimeout> | null = null
  let prodInflightResolve: ((value: Array<{ stdout: string; error?: string; elapsed_ms: number }> | null) => void) | null = null

  async function loadTestcases() {
    try {
      // Fetch encrypted pool by per-challenge slug (NOT by algorithm — multiple
      // challenges share `algorithm` values, which would alias their pools).
      const resp = await fetch(`/pools/${config.id}.bin`)
      if (!resp.ok) {
        errorMessage.value = `無法載入測資池 (${resp.status})`
        return
      }
      const data = new Uint8Array(await resp.arrayBuffer())

      // Load & decrypt via WASM
      const wasm = await ensureWasmPool()
      wasm.load_pool(config.id, data)

      // Select testcases — verdict_detail from pool is the source of truth
      const result = wasm.select_testcases(config.id, effectiveTestcaseCount(config))
      sessionId = result.session_id
      inputs.value = result.inputs
      poolVerdictDetail.value = resolveVerdictDetail(result.verdict_detail)

      // Update store (inputs only, no expected_output in prod)
      challengeStore.setCurrentChallenge({
        starter_code: config.starterCode,
        testcases: result.inputs.map((input) => ({ input })),
      })
      isReady.value = true
    } catch (err) {
      errorMessage.value = `測資池載入失敗: ${err instanceof Error ? err.message : err}`
    }
  }

  async function submit(code: string) {
    if (!inputs.value.length || !sessionId) return
    isRunning.value = true
    executorStore.setRunning(inputs.value.length)

    // Run student code in Pyodide Worker — only sends inputs, no expected_output
    const outputs = await runStudentCode(code, inputs.value)

    if (!outputs) {
      executorStore.setDone(inputs.value.length, 0)
      isRunning.value = false
      return
    }

    // Judge via WASM — keyed by slug, matching the slug used at load time.
    try {
      const wasm = await ensureWasmPool()
      const verdicts = wasm.judge(config.id, sessionId, outputs) as Array<{
        verdict: string
        actual?: string
        expected?: string
        elapsed_ms: number
        error?: string
      }>

      let passed = 0
      verdicts.forEach((v, i) => {
        if (v.verdict === 'AC') passed++
        executorStore.addResult({
          type: 'testcase_result',
          index: i,
          verdict: v.verdict as 'AC' | 'WA' | 'TLE' | 'RE',
          actual: v.actual,
          expected: v.expected,
          elapsed_ms: v.elapsed_ms,
          error: v.error,
        })
      })
      executorStore.setDone(verdicts.length, passed)

      // Session is consumed; need fresh select for next submit
      const result = wasm.select_testcases(config.id, effectiveTestcaseCount(config))
      sessionId = result.session_id
      inputs.value = result.inputs
      poolVerdictDetail.value = resolveVerdictDetail(result.verdict_detail)
    } catch (err) {
      errorMessage.value = `判定失敗: ${err instanceof Error ? err.message : err}`
      executorStore.setDone(inputs.value.length, 0)
    }

    isRunning.value = false
  }

  function runStudentCode(
    code: string,
    codeInputs: string[],
  ): Promise<Array<{
    stdout: string
    error?: string
    elapsed_ms: number
    timed_out?: boolean
  }> | null> {
    return new Promise((resolve) => {
      const worker = new Worker(new URL('../workers/pyodide.worker.ts', import.meta.url), {
        type: 'module',
      })
      runWorker = worker
      prodInflightResolve = resolve

      function settle() {
        runWorker = null
        prodKillTimerId = null
        prodInflightResolve = null
      }

      const results: Array<{
        stdout: string
        error?: string
        elapsed_ms: number
        timed_out?: boolean
      }> = []
      const totalBudget = codeInputs.length * WALL_CLOCK_KILL_MS

      // Per-testcase deadline: the Worker blocks inside synchronous Python, so
      // only this thread can stop a testcase that outruns its budget.
      const channel = createInterruptChannel()
      const watchdog = new DeadlineWatchdog(channel)

      prodKillTimerId = setTimeout(() => {
        watchdog.dispose()
        worker.terminate()
        settle()
        resolve(null)
      }, totalBudget)

      worker.onmessage = (event: MessageEvent) => {
        const msg = event.data
        if (msg.type === 'testcase_start') {
          watchdog.arm(msg.generation)
          return
        }
        if (msg.type === 'testcase_result') {
          watchdog.disarm()
          results.push({
            stdout: msg.stdout ?? '',
            error: msg.error,
            elapsed_ms: msg.elapsed_ms,
            // Attach ONLY when set: an explicit `timed_out: undefined` key
            // is not "absent" to serde-wasm-bindgen — it reaches
            // deserialize_bool and rejects the whole batch. (The Rust side
            // is also Option<bool> as a second layer of defense.)
            ...(msg.timed_out === true ? { timed_out: true } : {}),
          })
        } else if (msg.type === 'run_complete') {
          if (prodKillTimerId !== null) clearTimeout(prodKillTimerId)
          watchdog.dispose()
          worker.terminate()
          settle()
          resolve(results)
        }
      }

      worker.onerror = () => {
        if (prodKillTimerId !== null) clearTimeout(prodKillTimerId)
        watchdog.dispose()
        worker.terminate()
        settle()
        resolve(null)
      }

      worker.postMessage({
        type: 'run_only',
        code,
        inputs: [...codeInputs],
        ...(channel.buffer === null ? {} : { interruptBuffer: channel.buffer }),
      })
    })
  }

  function stop() {
    // Cancel killTimer if in-flight
    if (prodKillTimerId !== null) {
      clearTimeout(prodKillTimerId)
      prodKillTimerId = null
    }
    // Terminate worker
    runWorker?.terminate()
    runWorker = null
    // Settle in-flight Promise with null (aborted)
    if (prodInflightResolve) {
      const r = prodInflightResolve
      prodInflightResolve = null
      r(null)
    }
    isRunning.value = false
  }

  function cleanup() {
    stop()
    // Null out all references to prevent stale callbacks after unmount
    runWorker = null
    prodKillTimerId = null
    prodInflightResolve = null
  }

  return { loadTestcases, submit, stop, inputs, isReady, isRunning, errorMessage, verdictDetail: poolVerdictDetail, cleanup }
}
