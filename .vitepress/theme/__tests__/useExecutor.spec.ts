import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useExecutor } from '../composables/useExecutor'
import type { ExecuteResult } from '../workers/pyodide.worker'

// Mock Worker: class-based so `new Worker(...)` works correctly
let lastWorkerInstance: MockWorker
class MockWorker {
  onmessage: ((e: MessageEvent) => void) | null = null
  onerror: ((e: Event) => void) | null = null
  postMessage = vi.fn()
  terminate = vi.fn()
  constructor() {
    lastWorkerInstance = this
  }
}
vi.stubGlobal('Worker', MockWorker)

describe('useExecutor', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    vi.useFakeTimers()
  })

  it('exposes isRunning, run, stop, and execute', () => {
    const { isRunning, run, stop, execute } = useExecutor()
    expect(typeof isRunning.value).toBe('boolean')
    expect(typeof run).toBe('function')
    expect(typeof stop).toBe('function')
    expect(typeof execute).toBe('function')
  })

  it('isRunning starts as false', () => {
    const { isRunning } = useExecutor()
    expect(isRunning.value).toBe(false)
  })

  it('stop does not throw when not running', () => {
    const { stop } = useExecutor()
    expect(() => stop()).not.toThrow()
  })

  describe('execute()', () => {
    it('creates a Worker and sends an ExecuteRequest carrying the interrupt buffer', () => {
      const { execute } = useExecutor()
      execute('print("hi")', 'hello')

      expect(lastWorkerInstance.postMessage).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'execute',
          code: 'print("hi")',
          stdin: 'hello',
          // Without this the Worker cannot be interrupted at the deadline and
          // falls back to elapsed-only adjudication.
          interruptBuffer: expect.any(SharedArrayBuffer),
        }),
      )
    })

    it('resolves with ExecuteResult on success', async () => {
      const { execute } = useExecutor()
      const promise = execute('print("hi")', 'hello')

      // Simulate worker response
      const result: ExecuteResult = { type: 'execute_result', stdout: 'hi\n', elapsed_ms: 10 }
      lastWorkerInstance.onmessage!(new MessageEvent('message', { data: result }))

      const res = await promise
      expect(res.stdout).toBe('hi\n')
      expect(res.elapsed_ms).toBe(10)
      expect(res.error).toBeUndefined()
    })

    it('resolves with error on runtime error', async () => {
      const { execute } = useExecutor()
      const promise = execute('raise Exception("bad")', '')

      const result: ExecuteResult = { type: 'execute_result', stdout: '', elapsed_ms: 5, error: 'Exception: bad' }
      lastWorkerInstance.onmessage!(new MessageEvent('message', { data: result }))

      const res = await promise
      expect(res.error).toBe('Exception: bad')
    })

    it('terminates worker after receiving result', async () => {
      const { execute } = useExecutor()
      const promise = execute('pass', '')

      const result: ExecuteResult = { type: 'execute_result', stdout: '', elapsed_ms: 1 }
      lastWorkerInstance.onmessage!(new MessageEvent('message', { data: result }))

      await promise
      expect(lastWorkerInstance.terminate).toHaveBeenCalled()
    })

    it('resolves with timeout error after wall-clock kill', async () => {
      const { execute } = useExecutor()
      const promise = execute('while True: pass', '')

      // Advance past the 6s kill timer
      vi.advanceTimersByTime(6_000)

      const res = await promise
      expect(res.error).toContain('timed out')
      expect(lastWorkerInstance.terminate).toHaveBeenCalled()
    })
  })
})
