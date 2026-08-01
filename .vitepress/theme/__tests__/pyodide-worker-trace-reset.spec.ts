/**
 * Wiring guard for cross-run trace-state reset.
 *
 * The mechanism (a leaked tracer from an errored run poisons the next
 * execution) is proven by real-python tests in worker-utils-python.spec.ts.
 * This suite guards the WIRING: every worker handler must reset the
 * interpreter's trace state (resetTraceState) before clearing globals and
 * running the next wrapped code — for every single input, not just the
 * first. Drives the actual worker module with a mocked Pyodide runtime.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'

// Captured from the worker module at dispatch time — a static import would
// run the module's `self.onmessage = ...` before the `self` stub exists.
let traceResetSnippet: string | undefined

const calls: string[] = []
const mockRunPythonAsync = vi.fn(async (code: string) => {
  calls.push(code === traceResetSnippet ? '<reset>' : '<exec>')
})
const mockClear = vi.fn(() => {
  calls.push('<clear>')
})

vi.mock('/pyodide/pyodide.mjs', () => ({
  loadPyodide: vi.fn(async () => ({
    runPythonAsync: mockRunPythonAsync,
    globals: { clear: mockClear, get: vi.fn(() => '') },
  })),
}))

const postedMessages: unknown[] = []
vi.stubGlobal('self', {
  onmessage: null as ((e: { data: unknown }) => Promise<void>) | null,
  postMessage: (msg: unknown) => {
    postedMessages.push(msg)
  },
})

async function dispatch(data: unknown): Promise<void> {
  const mod = await import('../workers/pyodide.worker')
  traceResetSnippet = mod.TRACE_RESET_SNIPPET
  const handler = (self as unknown as { onmessage: (e: { data: unknown }) => Promise<void> })
    .onmessage
  await handler({ data })
}

/** Per-input handler sequence must be: reset → clear → exec. */
function expectResetBeforeEachExec(inputCount: number): void {
  expect(calls).toEqual(Array.from({ length: inputCount }, () => ['<reset>', '<clear>', '<exec>']).flat())
}

beforeEach(() => {
  calls.length = 0
  postedMessages.length = 0
})

describe('trace-state reset wiring', () => {
  it('run_only resets trace state before every testcase execution', async () => {
    await dispatch({ type: 'run_only', code: 'print(1)', inputs: ['a\n', 'b\n', 'c\n'] })
    expectResetBeforeEachExec(3)
  })

  it('run resets trace state before every testcase execution', async () => {
    await dispatch({
      type: 'run',
      code: 'print(1)',
      testcases: [
        { input: 'a\n', expected_output: '1\n' },
        { input: 'b\n', expected_output: '1\n' },
      ],
    })
    expectResetBeforeEachExec(2)
  })

  it('execute resets trace state before execution', async () => {
    await dispatch({ type: 'execute', code: 'print(1)', stdin: 'a\n' })
    expectResetBeforeEachExec(1)
  })

  it('generate resets trace state before every generator run', async () => {
    await dispatch({ type: 'generate', generatorCode: 'print(1)', inputs: ['a\n', 'b\n'] })
    expectResetBeforeEachExec(2)
  })
})
