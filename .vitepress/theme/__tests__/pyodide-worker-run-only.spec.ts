/**
 * Tests for the Pyodide Worker run_only message protocol:
 * RunOnlyRequest/RunOnlyResult type contracts, plus mock-driven behavior
 * tests for the structured timeout classification (timed_out flag).
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import type { RunOnlyRequest, RunOnlyTestcaseResult } from '../workers/pyodide.worker'

describe('RunOnlyRequest type', () => {
  it('accepts a valid run_only request shape', () => {
    const req: RunOnlyRequest = {
      type: 'run_only',
      code: 'print("hello")',
      inputs: ['world'],
    }
    expect(req.type).toBe('run_only')
    expect(req.code).toBe('print("hello")')
    expect(req.inputs).toEqual(['world'])
    expect(req.opLimit).toBeUndefined()
  })

  it('accepts multiple inputs', () => {
    const req: RunOnlyRequest = {
      type: 'run_only',
      code: 'for line in sys.stdin: print(line)',
      inputs: ['a', 'b', 'c'],
    }
    expect(req.inputs).toHaveLength(3)
    expect(req.inputs[0]).toBe('a')
  })

  it('accepts optional opLimit', () => {
    const req: RunOnlyRequest = {
      type: 'run_only',
      code: 'x = input()',
      inputs: ['42'],
      opLimit: 5_000_000,
    }
    expect(req.opLimit).toBe(5_000_000)
  })
})

describe('RunOnlyResult type', () => {
  it('accepts a successful testcase_result with required fields only', () => {
    const result: RunOnlyTestcaseResult = {
      type: 'testcase_result',
      index: 0,
      stdout: 'hello world\n',
      elapsed_ms: 12.5,
    }
    expect(result.type).toBe('testcase_result')
    expect(result.index).toBe(0)
    expect(result.stdout).toBe('hello world\n')
    expect(result.elapsed_ms).toBe(12.5)
    expect(result.error).toBeUndefined()
  })

  it('accepts a testcase_result with an error field', () => {
    const result: RunOnlyTestcaseResult = {
      type: 'testcase_result',
      index: 1,
      stdout: '',
      elapsed_ms: 3.2,
      error: 'NameError: name "foo" is not defined',
    }
    expect(result.error).toBe('NameError: name "foo" is not defined')
  })

  it('does NOT contain verdict, expected, or actual fields', () => {
    const result: RunOnlyTestcaseResult = {
      type: 'testcase_result',
      index: 0,
      stdout: '42\n',
      elapsed_ms: 8.0,
    }
    expect(result).not.toHaveProperty('verdict')
    expect(result).not.toHaveProperty('expected')
    expect(result).not.toHaveProperty('actual')
  })

  it('accepts a timed-out result carrying the structured flag and no error', () => {
    const result: RunOnlyTestcaseResult = {
      type: 'testcase_result',
      index: 2,
      stdout: '',
      elapsed_ms: 5000,
      timed_out: true,
    }
    expect(result.timed_out).toBe(true)
    expect(result.error).toBeUndefined()
    expect(result).not.toHaveProperty('verdict')
  })
})

// ── Mock-driven behavior: timeout classification happens in the Worker ─────

const DEFAULT_OP_LIMIT = 10_000_000
const execOutcomes: Array<'ok' | 'tle' | 'tle-bigint' | 'error' | 'fake-tle'> = []
let execIndex = 0
let traceResetSnippet: string | undefined
// Classification probes `_op_count` from globals — the mock exposes the
// count each outcome would leave behind in a real run. Pyodide hands back
// BigInt for Python ints above 2^53-1, so the mock covers both types.
let mockOpCount: number | bigint = 0

/** Trace reset still runs through the async entry point. */
const mockRunPythonAsync = vi.fn(async (code: string) => {
  if (code === traceResetSnippet) return
  throw new Error('wrapped user code must run through the synchronous entry point')
})

/**
 * Wrapped student code runs synchronously (design D3): an interrupt raised
 * during asynchronous execution escapes the handler's try/catch and kills the
 * Worker instead of producing a verdict.
 */
const mockRunPython = vi.fn((code: string) => {
  if (code === traceResetSnippet) return
  const outcome = execOutcomes[execIndex++] ?? 'ok'
  if (outcome === 'tle') {
    mockOpCount = DEFAULT_OP_LIMIT + 1
    throw new Error('PythonError: TimeoutError: Operation limit exceeded (10000000 ops)')
  }
  if (outcome === 'tle-bigint') {
    // e.g. a student set _op_count = 10**16 before the guard fired.
    mockOpCount = 10_000_000_000_000_001n
    throw new Error('PythonError: TimeoutError: Operation limit exceeded (10000000 ops)')
  }
  if (outcome === 'error') {
    mockOpCount = 42
    throw new Error("PythonError: NameError: name 'x' is not defined")
  }
  if (outcome === 'fake-tle') {
    // Student raised their own TimeoutError — count stays under the limit.
    mockOpCount = 42
    throw new Error('PythonError: TimeoutError: my own timeout')
  }
  mockOpCount = 42
  return undefined
})

vi.mock('/pyodide/pyodide.mjs', () => ({
  loadPyodide: vi.fn(async () => ({
    runPythonAsync: mockRunPythonAsync,
    runPython: mockRunPython,
    setInterruptBuffer: vi.fn(),
    globals: {
      clear: vi.fn(),
      get: vi.fn((key: string) => (key === '_op_count' ? mockOpCount : 'out\n')),
    },
  })),
}))

const postedMessages: Array<Record<string, unknown>> = []
vi.stubGlobal('self', {
  onmessage: null as ((e: { data: unknown }) => Promise<void>) | null,
  postMessage: (msg: Record<string, unknown>) => {
    postedMessages.push(msg)
  },
})

describe('run_only timeout classification (mock-driven)', () => {
  beforeEach(() => {
    postedMessages.length = 0
    execOutcomes.length = 0
    execIndex = 0
  })

  async function dispatchRunOnly(
    outcomes: Array<'ok' | 'tle' | 'tle-bigint' | 'error' | 'fake-tle'>,
  ): Promise<void> {
    execOutcomes.push(...outcomes)
    const mod = await import('../workers/pyodide.worker')
    traceResetSnippet = mod.TRACE_RESET_SNIPPET
    const handler = (self as unknown as { onmessage: (e: { data: unknown }) => Promise<void> })
      .onmessage
    await handler({
      data: { type: 'run_only', code: 'print(1)', inputs: outcomes.map((_, i) => `${i}\n`) },
    })
  }

  function testcaseResults(): Array<Record<string, unknown>> {
    return postedMessages.filter((m) => m.type === 'testcase_result')
  }

  it('op-limit timeout posts timed_out: true and no error field', async () => {
    await dispatchRunOnly(['tle'])
    const [r] = testcaseResults()
    expect(r).toMatchObject({ index: 0, stdout: '', timed_out: true })
    expect(r).not.toHaveProperty('error')
  })

  it('ordinary failure keeps the error shape without timed_out', async () => {
    await dispatchRunOnly(['error'])
    const [r] = testcaseResults()
    expect(r!.error).toContain('NameError')
    expect(r).not.toHaveProperty('timed_out')
  })

  it('a BigInt op count (beyond 2^53-1) still classifies as TLE', async () => {
    await dispatchRunOnly(['tle-bigint'])
    const [r] = testcaseResults()
    expect(r).toMatchObject({ timed_out: true })
    expect(r).not.toHaveProperty('error')
  })

  it('a student-raised TimeoutError stays RE — classification probes the op counter', async () => {
    await dispatchRunOnly(['fake-tle'])
    const [r] = testcaseResults()
    expect(r!.error).toContain('my own timeout')
    expect(r).not.toHaveProperty('timed_out')
  })

  it('mixed batch classifies per testcase independently', async () => {
    await dispatchRunOnly(['ok', 'tle', 'error'])
    const rs = testcaseResults()
    expect(rs).toHaveLength(3)
    expect(rs[0]).not.toHaveProperty('timed_out')
    expect(rs[0]).not.toHaveProperty('error')
    expect(rs[1]).toMatchObject({ timed_out: true })
    expect(rs[1]).not.toHaveProperty('error')
    expect(rs[2]!.error).toContain('NameError')
    expect(rs[2]).not.toHaveProperty('timed_out')
    expect(postedMessages.at(-1)).toMatchObject({ type: 'run_complete' })
  })
})
