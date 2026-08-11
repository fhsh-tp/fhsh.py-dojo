/**
 * Pyodide Web Worker
 *
 * Responsibilities:
 *  - Load Pyodide from CDN once, reuse across runs (task 4.1)
 *  - Handle RunRequest messages from the main thread (task 4.2)
 *  - Inject op-count TLE guard via sys.settrace (task 4.3)
 *  - Simulate stdin and capture stdout (task 4.4)
 *  - Execute testcases one by one, posting TestcaseResult per case (task 4.5)
 *  - Set a wall-clock setTimeout as secondary TLE guard (task 4.6)
 *  - Clear namespace between testcases (task 4.7)
 *  - Handle GenerateRequest: run generator code per input to produce expected_output
 */

import { buildWrappedCode, computeVerdict, buildTestcaseResultFields } from './worker-utils'
import type { VerdictDetail } from './worker-utils'
import { exceededDeadline } from './deadline'
export type { VerdictDetail }

// ── Message protocol types (task 4.2) ──────────────────────────────────────

export interface RunRequest {
  type: 'run'
  code: string
  testcases: Array<{ input: string; expected_output: string }>
  /** Maximum Python bytecode operations per testcase. Default: 10_000_000 */
  opLimit?: number
  /** Controls which fields are included in TestcaseResult. Default: 'hidden' */
  verdictDetail?: VerdictDetail
  /**
   * Shared buffer the main thread raises the interrupt signal in when a
   * testcase outruns its deadline. Absent when the environment cannot provide
   * one; judging then falls back to elapsed adjudication alone.
   */
  interruptBuffer?: SharedArrayBuffer
}

/**
 * Emitted immediately before user code for one testcase begins executing, so
 * the main thread can arm that testcase's deadline. The Worker blocks inside
 * synchronous Python right after posting this, which is exactly why the
 * countdown cannot live in the Worker itself.
 */
export interface TestcaseStart {
  type: 'testcase_start'
  index: number
  /**
   * Identifies this arming. An expiry whose generation no longer matches
   * belongs to a finished testcase and must stay silent.
   */
  generation: number
}

export interface TestcaseResult {
  type: 'testcase_result'
  index: number
  verdict: 'AC' | 'WA' | 'TLE' | 'RE'
  actual?: string
  expected?: string
  elapsed_ms: number
  /** Set for RE verdicts */
  error?: string
}

export interface RunComplete {
  type: 'run_complete'
  total: number
  passed: number
}

/** Request to run the generator script against a list of inputs. */
export interface GenerateRequest {
  type: 'generate'
  generatorCode: string
  inputs: string[]
}

export interface GenerateTestcase {
  input: string
  expected_output: string
  /** Set if the generator threw an error for this input */
  error?: string
}

export interface GenerateComplete {
  type: 'generate_complete'
  testcases: GenerateTestcase[]
}

/** Request to run code against multiple inputs in production mode (no comparison). */
export interface RunOnlyRequest {
  type: 'run_only'
  code: string
  inputs: string[]
  /** Maximum Python bytecode operations per testcase. Default: 10_000_000 */
  opLimit?: number
  /** See RunRequest.interruptBuffer. */
  interruptBuffer?: SharedArrayBuffer
}

/** Per-testcase result for run_only — no verdict fields (prod judges in WASM). */
export interface RunOnlyTestcaseResult {
  type: 'testcase_result'
  index: number
  stdout: string
  elapsed_ms: number
  /** Set for non-timeout failures only. */
  error?: string
  /**
   * Set (true) when the testcase was stopped by a limit rather than by a
   * defect in the code — the op-limit guard or the wall-clock deadline. The
   * WASM judge maps this flag straight to TLE.
   */
  timed_out?: boolean
}

/** Request to execute code with stdin, returning raw stdout (no verdict comparison). */
export interface ExecuteRequest {
  type: 'execute'
  code: string
  stdin: string
  /** Maximum Python bytecode operations. Default: 10_000_000 */
  opLimit?: number
  /** See RunRequest.interruptBuffer. */
  interruptBuffer?: SharedArrayBuffer
}

export interface ExecuteResult {
  type: 'execute_result'
  stdout: string
  elapsed_ms: number
  /** Set if execution failed (runtime error or TLE) */
  error?: string
}

type WorkerOutMessage = TestcaseResult | TestcaseStart | RunComplete | GenerateComplete | ExecuteResult

const PYODIDE_CDN = '/pyodide/'
const DEFAULT_OP_LIMIT = 10_000_000

/**
 * Shown in Run mode when execution is stopped by the deadline. Deliberately
 * free of any limit value — the op-limit guard's own message embeds the limit
 * and must not reach a student.
 */
export const TIMED_OUT_MESSAGE = 'Execution timed out'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let pyodide: any = null

/** Load Pyodide from CDN on first call, reuse thereafter (task 4.1) */
async function ensurePyodide(): Promise<void> {
  if (pyodide !== null) return

  // Dynamic import from CDN — @vite-ignore prevents Vite from bundling the URL
  const mod = await import(/* @vite-ignore */ `${PYODIDE_CDN}pyodide.mjs`)
  pyodide = await mod.loadPyodide({ indexURL: PYODIDE_CDN })
}

/**
 * Python snippet that clears interpreter trace state. Exported so the
 * wiring-guard test asserts against the same constant instead of a copy.
 */
export const TRACE_RESET_SNIPPET = 'import sys\nsys.settrace(None)'

/**
 * Did the just-failed run exceed its op limit? Probes the wrapper's
 * `_op_count` left in globals (the errored run's namespace is still intact
 * at catch time — cleanup happens before the NEXT run). The guard's
 * TimeoutError fires only when count exceeds the limit, so `count > limit`
 * identifies guard-raised timeouts without matching error-message text —
 * a student raising their own TimeoutError stays an ordinary RE (their
 * count is necessarily ≤ limit, or the guard would have fired first).
 */
function opLimitExceeded(opLimit: number): boolean {
  try {
    const count: unknown = pyodide.globals.get('_op_count')
    // Pyodide converts Python ints above 2^53-1 to BigInt — a count that
    // large is still "exceeded", and missing it would misclassify a
    // genuine guard timeout as RE (leaking the op-limit message).
    if (typeof count === 'bigint') return count > BigInt(opLimit)
    return typeof count === 'number' && count > opLimit
  } catch {
    return false
  }
}

/**
 * Clear any tracer left over from a previous run in this interpreter.
 *
 * The wrapper's own `sys.settrace(None)` teardown sits AFTER the user code,
 * so any ordinary exception (the normal RE path) skips it and the tracer
 * leaks into the shared interpreter. The next execution then dies in its
 * 'call' event — before its first line — with a NameError from the stale
 * tracer, falsely failing a correct testcase. Must run BEFORE
 * `globals.clear()`: while `_op_count` still exists the stale tracer stays
 * callable, so the reset normally executes cleanly. Edge case: if the
 * leftover count is already near its limit, the reset's own events make
 * the stale tracer raise — CPython then auto-clears tracing and the catch
 * absorbs the error, so both paths end with clean trace state.
 */
async function resetTraceState(): Promise<void> {
  try {
    await pyodide.runPythonAsync(TRACE_RESET_SNIPPET)
  } catch {
    // A stale tracer may throw mid-reset; CPython auto-clears tracing when
    // the tracer itself raises, so trace state is clean either way.
  }
}


/**
 * View over the main thread's interrupt buffer, once supplied. Pyodide polls
 * this inside its evaluation loop, which is what lets a blocked Worker be
 * stopped from outside without terminating it.
 */
let interruptView: Uint8Array | null = null

/** Monotonic per-testcase arming id, wrapped to the shared byte slot. */
let armGeneration = 0

/**
 * Hand the shared buffer to Pyodide. Absent buffer means the environment is
 * not cross-origin isolated; judging then rests on elapsed adjudication alone,
 * which is a weaker but still real gate.
 */
function registerInterruptBuffer(buffer: SharedArrayBuffer | undefined): void {
  if (buffer === undefined) return
  try {
    interruptView = new Uint8Array(buffer)
    pyodide.setInterruptBuffer(interruptView)
  } catch {
    // Older runtimes without setInterruptBuffer must not break judging.
    interruptView = null
  }
}

/**
 * Did this failure come from the deadline interrupt? Pyodide tags the thrown
 * error with the Python exception type, so this does not match on message
 * text — a student raising their own KeyboardInterrupt is indistinguishable
 * by text but produces the same verdict either way, since the elapsed check
 * is what ultimately decides.
 */
function wasInterrupted(err: unknown): boolean {
  return (err as { type?: string } | null | undefined)?.type === 'KeyboardInterrupt'
}

/** Announce the start of one testcase so the main thread arms its deadline. */
function armDeadline(index: number): void {
  armGeneration = (armGeneration + 1) & 0xff
  self.postMessage({ type: 'testcase_start', index, generation: armGeneration } satisfies TestcaseStart)
}

// ── Message handler ────────────────────────────────────────────────────────

self.onmessage = async (
  event: MessageEvent<RunRequest | RunOnlyRequest | ExecuteRequest | GenerateRequest | { type: 'preload' }>,
) => {
  const { type } = event.data

  // Preload message: warm up Pyodide in the background and stay idle.
  if (type === 'preload') {
    await ensurePyodide()
    return
  }

  if (type === 'generate') {
    await handleGenerate(event.data as GenerateRequest)
    return
  }

  if (type === 'execute') {
    await handleExecute(event.data as ExecuteRequest)
    return
  }

  if (type === 'run_only') {
    await handleRunOnly(event.data as RunOnlyRequest)
    return
  }

  if (type !== 'run') return

  const { code, testcases, opLimit = DEFAULT_OP_LIMIT, verdictDetail = 'hidden', interruptBuffer } = event.data as RunRequest

  await ensurePyodide()
  registerInterruptBuffer(interruptBuffer)

  let passed = 0

  for (let i = 0; i < testcases.length; i++) {
    const { input, expected_output } = testcases[i]!

    // Namespace cleanup before each testcase (task 4.7)
    await resetTraceState()
    try {
      pyodide.globals.clear()
    } catch {
      // globals.clear() may not exist on all Pyodide versions; ignore
    }

    // Arm strictly around user code. An interrupt landing while the runtime
    // does its own work was measured to leave that runtime unusable for every
    // subsequent testcase.
    armDeadline(i)
    const startTime = performance.now()

    let verdict: TestcaseResult['verdict']
    let actual = ''
    let errMsg: string | undefined

    try {
      pyodide.runPython(buildWrappedCode(code, input, opLimit))
      // stdout capture result (task 4.4)
      actual = pyodide.globals.get('_output') ?? ''
      verdict = computeVerdict(actual, expected_output)
    } catch (err: unknown) {
      // Probe the op counter instead of matching error text — a student
      // raising their own TimeoutError is an ordinary RE (dev and prod
      // classify identically). A deadline interrupt is never an RE.
      if (opLimitExceeded(opLimit) || wasInterrupted(err)) {
        verdict = 'TLE'
      } else {
        verdict = 'RE'
        errMsg = String(err)
      }
    }

    const elapsed_ms = performance.now() - startTime

    // Authoritative layer: however the code responded to the interrupt — or
    // if no interrupt channel existed at all — outrunning the budget is TLE.
    if (exceededDeadline(elapsed_ms)) {
      verdict = 'TLE'
      errMsg = undefined
    }

    if (verdict === 'AC') passed++

    self.postMessage({
      type: 'testcase_result',
      index: i,
      verdict,
      elapsed_ms,
      error: errMsg,
      ...buildTestcaseResultFields(verdict === 'TLE' || verdict === 'RE' ? '' : actual, expected_output, verdictDetail),
    } satisfies TestcaseResult)
  }

  self.postMessage({
    type: 'run_complete',
    total: testcases.length,
    passed,
  } satisfies WorkerOutMessage)
}

// ── Run-only handler (production mode, no comparison) ─────────────────────

async function handleRunOnly(req: RunOnlyRequest): Promise<void> {
  const { code, inputs, opLimit = DEFAULT_OP_LIMIT, interruptBuffer } = req

  await ensurePyodide()
  registerInterruptBuffer(interruptBuffer)

  for (let i = 0; i < inputs.length; i++) {
    const input = inputs[i]!

    await resetTraceState()
    try {
      pyodide.globals.clear()
    } catch {
      // ignore
    }

    armDeadline(i)
    const startTime = performance.now()

    let stdout = ''
    let timedOut = false
    let errMsg: string | undefined

    try {
      pyodide.runPython(buildWrappedCode(code, input, opLimit))
      stdout = pyodide.globals.get('_output') ?? ''
    } catch (err: unknown) {
      // Classify limit-stops HERE by probing the actual op counter and the
      // interrupt type — downstream the judge only reads the structured flag.
      // The op-limit message embeds the limit, so a stopped result carries no
      // error field at all.
      if (opLimitExceeded(opLimit) || wasInterrupted(err)) {
        timedOut = true
      } else {
        errMsg = String(err)
      }
    }

    const elapsed_ms = performance.now() - startTime

    // Authoritative layer, identical to the dev path: outrunning the budget
    // is a timeout no matter how the code responded to the interrupt.
    if (exceededDeadline(elapsed_ms)) {
      timedOut = true
      errMsg = undefined
      stdout = ''
    }

    self.postMessage({
      type: 'testcase_result',
      index: i,
      stdout: timedOut ? '' : stdout,
      elapsed_ms,
      ...(timedOut ? { timed_out: true } : errMsg !== undefined ? { error: errMsg } : {}),
    } satisfies RunOnlyTestcaseResult)
  }

  self.postMessage({ type: 'run_complete' })
}

// ── Execute handler (pure execution, no verdict) ─────────────────────────

async function handleExecute(req: ExecuteRequest): Promise<void> {
  const { code, stdin, opLimit = DEFAULT_OP_LIMIT, interruptBuffer } = req

  await ensurePyodide()
  registerInterruptBuffer(interruptBuffer)

  // Namespace cleanup
  await resetTraceState()
  try {
    pyodide.globals.clear()
  } catch {
    // ignore
  }

  armDeadline(0)
  const startTime = performance.now()

  let stdout = ''
  let errMsg: string | undefined

  try {
    pyodide.runPython(buildWrappedCode(code, stdin, opLimit))
    stdout = pyodide.globals.get('_output') ?? ''
  } catch (err: unknown) {
    errMsg = wasInterrupted(err) ? TIMED_OUT_MESSAGE : String(err)
  }

  const elapsed_ms = performance.now() - startTime

  // Same authoritative layer as the judged paths. Run mode has no verdict, so
  // the deadline surfaces as an error string the modal can display.
  if (exceededDeadline(elapsed_ms)) {
    errMsg = TIMED_OUT_MESSAGE
    stdout = ''
  }

  self.postMessage({
    type: 'execute_result',
    stdout: errMsg === undefined ? stdout : '',
    elapsed_ms,
    ...(errMsg === undefined ? {} : { error: errMsg }),
  } satisfies ExecuteResult)
}

// ── Generator handler ──────────────────────────────────────────────────────

async function handleGenerate(req: GenerateRequest): Promise<void> {
  await ensurePyodide()

  const { generatorCode, inputs } = req
  const testcases: GenerateTestcase[] = []

  for (const input of inputs) {
    // Clear namespace before each generator run
    await resetTraceState()
    try {
      pyodide.globals.clear()
    } catch {
      // ignore
    }

    try {
      // Generators are trusted authored code — exempt from the op-count
      // guard (opLimit: null) so heavy but legitimate generators are not
      // killed now that flat top-level code is actually counted.
      const wrapped = buildWrappedCode(generatorCode, input, null)
      await pyodide.runPythonAsync(wrapped)
      const rawOutput: string = (pyodide.globals.get('_output') ?? '').trimEnd()

      // Support factory format: generator outputs JSON {"input": "...", "expected_output": "..."}
      // This allows generators to transform WASM params into a different student input format
      // (e.g., decrypt challenges where student receives ciphertext instead of plaintext)
      let tcInput = input
      let tcOutput = rawOutput
      if (rawOutput.startsWith('{')) {
        try {
          const parsed = JSON.parse(rawOutput) as { input: string; expected_output: string }
          if (typeof parsed.input === 'string' && typeof parsed.expected_output === 'string') {
            tcInput = parsed.input
            tcOutput = parsed.expected_output
          }
        } catch {
          // Not valid JSON — treat as plain expected output
        }
      }

      testcases.push({ input: tcInput, expected_output: tcOutput })
    } catch (err: unknown) {
      testcases.push({ input, expected_output: '', error: String(err) })
    }
  }

  self.postMessage({
    type: 'generate_complete',
    testcases,
  } satisfies GenerateComplete)
}
