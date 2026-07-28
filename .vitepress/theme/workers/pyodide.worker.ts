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
}

/** Request to execute code with stdin, returning raw stdout (no verdict comparison). */
export interface ExecuteRequest {
  type: 'execute'
  code: string
  stdin: string
  /** Maximum Python bytecode operations. Default: 10_000_000 */
  opLimit?: number
}

export interface ExecuteResult {
  type: 'execute_result'
  stdout: string
  elapsed_ms: number
  /** Set if execution failed (runtime error or TLE) */
  error?: string
}

type WorkerOutMessage = TestcaseResult | RunComplete | GenerateComplete | ExecuteResult

const PYODIDE_CDN = '/pyodide/'
const DEFAULT_OP_LIMIT = 10_000_000
/** Wall-clock budget per testcase in milliseconds (task 4.6) */
const WALL_CLOCK_MS = 5_000

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
 * Clear any tracer left over from a previous run in this interpreter.
 *
 * The wrapper's own `sys.settrace(None)` teardown sits AFTER the user code,
 * so any ordinary exception (the normal RE path) skips it and the tracer
 * leaks into the shared interpreter. The next execution then dies in its
 * 'call' event — before its first line — with a NameError from the stale
 * tracer, falsely failing a correct testcase. Must run BEFORE
 * `globals.clear()`: while `_op_count` still exists the stale tracer stays
 * callable, so this line executes without relying on CPython's
 * clear-on-tracer-exception fallback (which the catch covers anyway).
 */
async function resetTraceState(): Promise<void> {
  try {
    await pyodide.runPythonAsync('import sys\nsys.settrace(None)')
  } catch {
    // A stale tracer may throw mid-reset; CPython auto-clears tracing when
    // the tracer itself raises, so trace state is clean either way.
  }
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

  const { code, testcases, opLimit = DEFAULT_OP_LIMIT, verdictDetail = 'hidden' } = event.data as RunRequest

  await ensurePyodide()

  let passed = 0

  for (let i = 0; i < testcases.length; i++) {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const { input, expected_output } = testcases[i]!
    const startTime = performance.now()

    // Wall-clock fallback (task 4.6): set a flag if JS event loop re-enters
    // after the timeout. For truly blocked Workers, the main-thread kill
    // in useExecutor provides the hard wall-clock guarantee.
    let wallClockTle = false
    const wallClock = setTimeout(() => {
      wallClockTle = true
    }, WALL_CLOCK_MS)

    // Namespace cleanup before each testcase (task 4.7)
    await resetTraceState()
    try {
      pyodide.globals.clear()
    } catch {
      // globals.clear() may not exist on all Pyodide versions; ignore
    }

    try {
      const wrapped = buildWrappedCode(code, input, opLimit)
      await pyodide.runPythonAsync(wrapped)

      clearTimeout(wallClock)

      if (wallClockTle) {
        self.postMessage({
          type: 'testcase_result',
          index: i,
          verdict: 'TLE',
          elapsed_ms: performance.now() - startTime,
          ...buildTestcaseResultFields('', expected_output, verdictDetail),
        } satisfies TestcaseResult)
        continue
      }

      // stdout capture result (task 4.4)
      const actual: string = pyodide.globals.get('_output') ?? ''
      const elapsed_ms = performance.now() - startTime
      const verdict = computeVerdict(actual, expected_output)

      if (verdict === 'AC') passed++

      self.postMessage({
        type: 'testcase_result',
        index: i,
        verdict,
        elapsed_ms,
        ...buildTestcaseResultFields(actual, expected_output, verdictDetail),
      } satisfies TestcaseResult)
    } catch (err: unknown) {
      clearTimeout(wallClock)
      const elapsed_ms = performance.now() - startTime
      const errMsg = String(err)
      const isTle = errMsg.includes('TimeoutError') || errMsg.includes('Operation limit')

      self.postMessage({
        type: 'testcase_result',
        index: i,
        verdict: isTle ? 'TLE' : 'RE',
        elapsed_ms,
        error: isTle ? undefined : errMsg,
        ...buildTestcaseResultFields('', expected_output, verdictDetail),
      } satisfies TestcaseResult)
    }
  }

  self.postMessage({
    type: 'run_complete',
    total: testcases.length,
    passed,
  } satisfies WorkerOutMessage)
}

// ── Run-only handler (production mode, no comparison) ─────────────────────

async function handleRunOnly(req: RunOnlyRequest): Promise<void> {
  const { code, inputs, opLimit = DEFAULT_OP_LIMIT } = req

  await ensurePyodide()

  for (let i = 0; i < inputs.length; i++) {
    const input = inputs[i]!
    const startTime = performance.now()

    await resetTraceState()
    try {
      pyodide.globals.clear()
    } catch {
      // ignore
    }

    try {
      const wrapped = buildWrappedCode(code, input, opLimit)
      await pyodide.runPythonAsync(wrapped)

      const stdout: string = pyodide.globals.get('_output') ?? ''

      self.postMessage({
        type: 'testcase_result',
        index: i,
        stdout,
        elapsed_ms: performance.now() - startTime,
      })
    } catch (err: unknown) {
      const errMsg = String(err)

      self.postMessage({
        type: 'testcase_result',
        index: i,
        stdout: '',
        elapsed_ms: performance.now() - startTime,
        error: errMsg,
      })
    }
  }

  self.postMessage({ type: 'run_complete' })
}

// ── Execute handler (pure execution, no verdict) ─────────────────────────

async function handleExecute(req: ExecuteRequest): Promise<void> {
  const { code, stdin, opLimit = DEFAULT_OP_LIMIT } = req

  await ensurePyodide()

  const startTime = performance.now()

  // Namespace cleanup
  await resetTraceState()
  try {
    pyodide.globals.clear()
  } catch {
    // ignore
  }

  try {
    const wrapped = buildWrappedCode(code, stdin, opLimit)
    await pyodide.runPythonAsync(wrapped)

    const stdout: string = pyodide.globals.get('_output') ?? ''

    self.postMessage({
      type: 'execute_result',
      stdout,
      elapsed_ms: performance.now() - startTime,
    } satisfies ExecuteResult)
  } catch (err: unknown) {
    const errMsg = String(err)

    self.postMessage({
      type: 'execute_result',
      stdout: '',
      elapsed_ms: performance.now() - startTime,
      error: errMsg,
    } satisfies ExecuteResult)
  }
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
