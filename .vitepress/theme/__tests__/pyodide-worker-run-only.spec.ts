/**
 * Tests for the Pyodide Worker run_only message protocol:
 * RunOnlyRequest/RunOnlyResult type contracts, plus mock-driven behavior
 * tests for the structured timeout classification (timed_out flag).
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import type { RunOnlyRequest } from '../workers/pyodide.worker'

interface RunOnlyTestcaseResult {
  type: 'testcase_result'
  index: number
  stdout: string
  error?: string
  elapsed_ms: number
  /** Set (true) only for op-limit timeouts, classified in the Worker. */
  timed_out?: boolean
}

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

const execOutcomes: Array<'ok' | 'tle' | 'error'> = []
let execIndex = 0
let traceResetSnippet: string | undefined

const mockRunPythonAsync = vi.fn(async (code: string) => {
  if (code === traceResetSnippet) return
  const outcome = execOutcomes[execIndex++] ?? 'ok'
  if (outcome === 'tle') {
    throw new Error('PythonError: TimeoutError: Operation limit exceeded (10000000 ops)')
  }
  if (outcome === 'error') {
    throw new Error("PythonError: NameError: name 'x' is not defined")
  }
})

vi.mock('/pyodide/pyodide.mjs', () => ({
  loadPyodide: vi.fn(async () => ({
    runPythonAsync: mockRunPythonAsync,
    globals: { clear: vi.fn(), get: vi.fn(() => 'out\n') },
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

  async function dispatchRunOnly(outcomes: Array<'ok' | 'tle' | 'error'>): Promise<void> {
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
