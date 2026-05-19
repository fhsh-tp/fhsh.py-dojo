/**
 * Tests for useChallengeRunner dev path - stop/cancel/cleanup semantics.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

// ── Worker mock ───────────────────────────────────────────────────────────
const mockWorkerInstances: Array<{
  onmessage: ((e: MessageEvent) => void) | null
  onerror: ((e: Event) => void) | null
  postMessage: ReturnType<typeof vi.fn>
  terminate: ReturnType<typeof vi.fn>
}> = []
vi.stubGlobal(
  'Worker',
  class {
    onmessage: ((e: MessageEvent) => void) | null = null
    onerror: ((e: Event) => void) | null = null
    postMessage = vi.fn()
    terminate = vi.fn()
    constructor() {
      mockWorkerInstances.push(this as (typeof mockWorkerInstances)[number])
    }
  },
)

// ── useWasm mock ─────────────────────────────────────────────────────────
const mockGenerateChallenge = vi.fn()
vi.mock('../composables/useWasm', () => ({
  useWasm: () => ({
    generateChallenge: mockGenerateChallenge,
  }),
}))

// ── WASM pool mock (not used in dev, but imported at module level) ───────
vi.mock('/wasm/testcase_generator.js', () => ({
  default: vi.fn().mockResolvedValue(undefined),
  load_pool: vi.fn(),
  select_testcases: vi.fn(),
  judge: vi.fn(),
  get_expected: vi.fn(),
}))

describe('useChallengeRunner dev path - stop/cancel semantics', () => {
  let originalProd: boolean

  beforeEach(() => {
    vi.useFakeTimers()
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = false

    // Mock WASM generateChallenge to return inputs
    mockGenerateChallenge.mockResolvedValue({
      inputs: ['1\n', '2\n'],
    })
  })

  afterEach(() => {
    // @ts-expect-error - restoring read-only env
    import.meta.env.PROD = originalProd
    mockWorkerInstances.length = 0
    vi.clearAllMocks()
    vi.useRealTimers()
  })

  /** Helper: create runner, load testcases (complete generator phase).
   *  Works with both real and fake timers. */
  async function createReadyRunner() {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner({
      id: 'test_algo',
      algorithm: 'test_algo',
      params: { shift: { type: 'int', min: 1, max: 25 } },
      generator: 'def generate(input): return input',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'full',
    })

    // Start loadTestcases — this creates a generator worker
    const loadPromise = runner.loadTestcases()
    // Flush microtasks — works with both real and fake timers
    await vi.advanceTimersByTimeAsync(0)

    // Complete the generator worker
    const generatorWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!
    if (generatorWorker.onmessage) {
      generatorWorker.onmessage(
        new MessageEvent('message', {
          data: {
            type: 'generate_complete',
            testcases: [
              { input: '1\n', expected_output: 'A' },
              { input: '2\n', expected_output: 'B' },
            ],
          },
        }),
      )
    }
    await loadPromise

    return runner
  }

  // Task 3.1: stop during dev submission settles Promise
  it('stop() during submission terminates worker, clears killTimer, sets isRunning false', async () => {
    const runner = await createReadyRunner()

    // Start submit — creates a submission worker
    const submitPromise = runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    expect(runner.isRunning.value).toBe(true)

    // Stop while submission in-flight
    runner.stop()

    // The submit Promise should settle
    const result = await Promise.race([
      submitPromise.then(() => 'settled'),
      vi.advanceTimersByTimeAsync(500).then(() => 'timeout'),
    ])
    expect(result).toBe('settled')
    expect(runner.isRunning.value).toBe(false)
  })

  // Task 3.2: stop during generator phase terminates activeWorker
  it('stop() during generator phase terminates activeWorker', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner({
      id: 'test_algo',
      algorithm: 'test_algo',
      params: { shift: { type: 'int', min: 1, max: 25 } },
      generator: 'def generate(input): return input',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'full',
    })

    // Start loadTestcases — generator worker is created but not completed
    runner.loadTestcases()
    await vi.advanceTimersByTimeAsync(0)

    const generatorWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    // Stop during generator phase
    runner.stop()

    expect(generatorWorker.terminate).toHaveBeenCalled()
    expect(runner.isRunning.value).toBe(false)
  })

  // Task 3.3: killTimer does not fire after dev stop
  it('killTimer does not fire after stop()', async () => {
    const runner = await createReadyRunner()

    const submitPromise = runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    runner.stop()

    const terminateCountAfterStop = submitWorker.terminate.mock.calls.length

    // Advance past killTimer timeout
    await vi.advanceTimersByTimeAsync(60_000)

    // terminate should not be called again by stale killTimer
    expect(submitWorker.terminate.mock.calls.length).toBe(terminateCountAfterStop)

    await submitPromise
  })

  // Task 4.2: cleanup during dev submission cancels killTimer and settles Promise
  it('cleanup() during dev submission cancels killTimer and settles Promise', async () => {
    const runner = await createReadyRunner()

    const submitPromise = runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    runner.cleanup()

    // Promise should settle
    const result = await Promise.race([
      submitPromise.then(() => 'settled'),
      vi.advanceTimersByTimeAsync(500).then(() => 'timeout'),
    ])
    expect(result).toBe('settled')

    // No stale timer should fire
    const terminateCountAfterCleanup = submitWorker.terminate.mock.calls.length
    await vi.advanceTimersByTimeAsync(60_000)
    expect(submitWorker.terminate.mock.calls.length).toBe(terminateCountAfterCleanup)

    await submitPromise
  })

  // Task 4.3 (dev part): no stale timer fires after cleanup
  it('no stale timer fires after cleanup()', async () => {
    const runner = await createReadyRunner()

    runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    runner.cleanup()

    const terminateCount = submitWorker.terminate.mock.calls.length

    await vi.advanceTimersByTimeAsync(120_000)

    expect(submitWorker.terminate.mock.calls.length).toBe(terminateCount)
  })
})
