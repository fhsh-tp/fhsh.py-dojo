/**
 * Integration tests for useChallengeRunner production path.
 * Verifies that verdictDetail comes from the pool (WASM select_testcases),
 * not from frontmatter config. Also tests stop/cancel/cleanup semantics.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { isRef, type Ref } from 'vue'

// ── WASM module mock ──────────────────────────────────────────────────────
const mockLoadPool = vi.fn()
const mockSelectTestcases = vi.fn()
const mockJudge = vi.fn()
const mockGetExpected = vi.fn()

const mockWasmMod = {
  default: vi.fn().mockResolvedValue(undefined),
  load_pool: mockLoadPool,
  select_testcases: mockSelectTestcases,
  judge: mockJudge,
  get_expected: mockGetExpected,
}

vi.mock('/wasm/testcase_generator.js', () => mockWasmMod)

// ── fetch mock ────────────────────────────────────────────────────────────
const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

// ── Worker mock ───────────────────────────────────────────────────────────
const mockWorkerInstances: Array<{ onmessage: ((e: MessageEvent) => void) | null; onerror: ((e: Event) => void) | null; postMessage: ReturnType<typeof vi.fn>; terminate: ReturnType<typeof vi.fn> }> = []
vi.stubGlobal('Worker', class {
  onmessage: ((e: MessageEvent) => void) | null = null
  onerror: ((e: Event) => void) | null = null
  postMessage = vi.fn()
  terminate = vi.fn()
  constructor() {
    mockWorkerInstances.push(this as typeof mockWorkerInstances[number])
  }
})

// ── useWasm mock (only used in dev, but imported at module level) ─────────
vi.mock('../composables/useWasm', () => ({
  useWasm: () => ({
    generateChallenge: vi.fn(),
  }),
}))

describe('useChallengeRunner prod path - slug-as-pool-key', () => {
  let originalProd: boolean

  beforeEach(() => {
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = true

    mockSelectTestcases.mockReturnValue({
      inputs: ['1\n'],
      session_id: 's_slug',
      verdict_detail: 'hidden',
    })

    mockFetch.mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(10)),
    })
  })

  afterEach(() => {
    // @ts-expect-error - restoring read-only env
    import.meta.env.PROD = originalProd
    mockWorkerInstances.length = 0
    vi.clearAllMocks()
  })

  it('fetches /pools/<id>.bin (slug), not /pools/<algorithm>.bin', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'multiplication-table',
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    expect(mockFetch).toHaveBeenCalledTimes(1)
    expect(mockFetch.mock.calls[0]![0]).toBe('/pools/multiplication-table.bin')
    expect(mockFetch.mock.calls[0]![0]).not.toBe('/pools/nested-loop.bin')
  })

  it('passes slug (not algorithm) to load_pool and select_testcases', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'multiplication-table',
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    expect(mockLoadPool).toHaveBeenCalledTimes(1)
    expect(mockLoadPool.mock.calls[0]![0]).toBe('multiplication-table')
    expect(mockSelectTestcases).toHaveBeenCalledTimes(1)
    expect(mockSelectTestcases.mock.calls[0]![0]).toBe('multiplication-table')
  })

  it('passes slug to judge() and the next select_testcases on submit', async () => {
    mockJudge.mockReturnValue([{ verdict: 'AC', elapsed_ms: 5 }])

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'multiplication-table',
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    const submitPromise = runner.submit('print(1)')
    await new Promise((r) => setTimeout(r, 0))

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!
    submitWorker.onmessage?.(new MessageEvent('message', {
      data: { type: 'testcase_result', index: 0, stdout: '1\n', elapsed_ms: 5 },
    }))
    submitWorker.onmessage?.(new MessageEvent('message', {
      data: { type: 'run_complete' },
    }))

    await submitPromise

    expect(mockJudge).toHaveBeenCalledTimes(1)
    expect(mockJudge.mock.calls[0]![0]).toBe('multiplication-table')
    // After judge consumes the session, runner re-selects for the next submit.
    expect(mockSelectTestcases).toHaveBeenCalledTimes(2)
    expect(mockSelectTestcases.mock.calls[1]![0]).toBe('multiplication-table')
  })

  it('passes the worker timed_out flag through to judge verbatim', async () => {
    mockJudge.mockReturnValue([{ verdict: 'TLE', elapsed_ms: 4000 }])

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'multiplication-table',
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    const submitPromise = runner.submit('while True: pass')
    await new Promise((r) => setTimeout(r, 0))

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!
    submitWorker.onmessage?.(new MessageEvent('message', {
      data: { type: 'testcase_result', index: 0, stdout: '', elapsed_ms: 4000, timed_out: true },
    }))
    submitWorker.onmessage?.(new MessageEvent('message', {
      data: { type: 'run_complete' },
    }))

    await submitPromise

    expect(mockJudge).toHaveBeenCalledTimes(1)
    const judgedResults = mockJudge.mock.calls[0]![2] as Array<Record<string, unknown>>
    expect(judgedResults).toHaveLength(1)
    expect(judgedResults[0]).toMatchObject({ stdout: '', timed_out: true })
  })

  it('surfaces an error when load_pool rejects an identity mismatch', async () => {
    // Simulate the WASM `load_pool` raising the identity-mismatch error that
    // it would produce if the encrypted payload's challenge_id (slug) does
    // NOT match the caller-supplied key (e.g. algorithm passed by mistake,
    // or a manually renamed pool file). The runner SHALL surface this as a
    // user-visible errorMessage rather than silently continuing.
    mockLoadPool.mockImplementationOnce(() => {
      throw new Error('challenge_id mismatch: expected "nested-loop" but pool contains "multiplication-table"')
    })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'nested-loop', // wrong key: caller used algorithm, pool was built with slug
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    expect(runner.errorMessage.value).toMatch(/池|pool/i)
    expect(mockSelectTestcases).not.toHaveBeenCalled()
  })

  it('does NOT retry the algorithm path when /pools/<id>.bin returns 404', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
    })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'multiplication-table',
      algorithm: 'nested-loop',
      params: {},
      generator: '',
      testcaseCount: 1,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    expect(mockFetch).toHaveBeenCalledTimes(1)
    expect(mockFetch.mock.calls[0]![0]).toBe('/pools/multiplication-table.bin')
    // The runner must surface an error and stop — NOT retry with algorithm.
    expect(runner.errorMessage.value).toMatch(/載入測資池|404/)
    expect(mockLoadPool).not.toHaveBeenCalled()
  })
})

describe('ChallengeConfig type contract', () => {
  it('rejects configs missing the required id field at type-check time', async () => {
    // Documents the spec scenario "Configuration without id fails at type-check".
    // The `@ts-expect-error` directive triggers iff the line below has a type
    // error — i.e. iff `id` is still required by ChallengeConfig. If someone
    // relaxes the type, this test will fail at vitest type-check (and at
    // `pnpm typecheck` when this file is reachable from the app tsconfig).
    if (false) {
      const { useChallengeRunner } = await import('../composables/useChallengeRunner')
      // @ts-expect-error — id is required on ChallengeConfig
      useChallengeRunner({
        algorithm: 'caesar_encrypt',
        params: {},
        generator: '',
        testcaseCount: 2,
        starterCode: '',
        verdictDetail: 'hidden',
      })
    }
    expect(true).toBe(true)
  })
})

describe('useChallengeRunner prod path - verdictDetail from pool', () => {
  let originalProd: boolean

  beforeEach(() => {
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = true

    mockSelectTestcases.mockReturnValue({
      inputs: ['1\n', '2\n'],
      session_id: 's_1',
      verdict_detail: 'actual',
    })

    mockFetch.mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(10)),
    })
  })

  afterEach(() => {
    // @ts-expect-error - restoring read-only env
    import.meta.env.PROD = originalProd
    mockWorkerInstances.length = 0
    vi.clearAllMocks()
  })

  it('verdictDetail is a reactive ref sourced from pool, not frontmatter', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden', // frontmatter says hidden
    })

    await runner.loadTestcases()

    // verdictDetail should be a reactive ref (not a static string)
    expect(isRef(runner.verdictDetail)).toBe(true)
    // Its value should come from the pool ('actual'), not frontmatter ('hidden')
    expect((runner.verdictDetail as Ref<string>).value).toBe('actual')
  })

  it('submit sends RunOnlyRequest to worker, not RunRequest', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    // Mock judge to return verdicts
    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
      { verdict: 'AC', elapsed_ms: 12 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    // Start submit — this creates a worker and posts a message
    const submitPromise = runner.submit('print(42)')

    // Wait a tick for the worker to be created
    await new Promise((r) => setTimeout(r, 0))

    // Find the worker that was created for submit (not for loadTestcases)
    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    // Verify the message sent to the worker is RunOnlyRequest, not RunRequest
    const postedMessage = submitWorker.postMessage.mock.calls[0]?.[0]
    expect(postedMessage).toBeDefined()
    expect(postedMessage.type).toBe('run_only')
    expect(postedMessage.code).toBe('print(42)')
    expect(postedMessage.inputs).toEqual(['1\n', '2\n'])
    // RunOnlyRequest must NOT contain these RunRequest fields
    expect(postedMessage).not.toHaveProperty('testcases')
    expect(postedMessage).not.toHaveProperty('verdictDetail')
    expect(postedMessage).not.toHaveProperty('expected_output')

    // Simulate worker completing to let submit finish
    if (submitWorker.onmessage) {
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'testcase_result', index: 0, stdout: '42\n', elapsed_ms: 10 },
      }))
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'testcase_result', index: 1, stdout: '42\n', elapsed_ms: 12 },
      }))
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'run_complete' },
      }))
    }

    await submitPromise
  })

  it('inputs passed to Worker postMessage are a plain Array copy, not the WASM-returned reference', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    // Capture the exact array object returned by select_testcases
    const wasmInputsRef = ['1\n', '2\n']
    mockSelectTestcases.mockReturnValue({
      inputs: wasmInputsRef,
      session_id: 's_1',
      verdict_detail: 'actual',
    })

    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
      { verdict: 'AC', elapsed_ms: 12 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    const submitPromise = runner.submit('print(42)')
    await new Promise((r) => setTimeout(r, 0))

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!
    const postedInputs = submitWorker.postMessage.mock.calls[0]?.[0]?.inputs

    // Must be a plain Array with correct values
    expect(Array.isArray(postedInputs)).toBe(true)
    expect(postedInputs).toEqual(['1\n', '2\n'])
    // Must NOT be the same object reference (should be a spread copy)
    expect(postedInputs).not.toBe(wasmInputsRef)

    // Let worker complete
    if (submitWorker.onmessage) {
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'testcase_result', index: 0, stdout: '42\n', elapsed_ms: 10 },
      }))
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'testcase_result', index: 1, stdout: '42\n', elapsed_ms: 12 },
      }))
      submitWorker.onmessage(new MessageEvent('message', {
        data: { type: 'run_complete' },
      }))
    }

    await submitPromise
  })
})

// ── Prod runner stop/cancel tests ──────────────────────────────────────────

describe('useChallengeRunner prod path - stop/cancel semantics', () => {
  let originalProd: boolean

  beforeEach(() => {
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = true

    mockSelectTestcases.mockReturnValue({
      inputs: ['1\n', '2\n'],
      session_id: 's_1',
      verdict_detail: 'actual',
    })

    mockFetch.mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(10)),
    })
  })

  afterEach(() => {
    // @ts-expect-error - restoring read-only env
    import.meta.env.PROD = originalProd
    mockWorkerInstances.length = 0
    vi.clearAllMocks()
    vi.useRealTimers()
  })

  // Task 2.1: stop() during in-flight submission settles Promise and sets isRunning false
  it('stop() during in-flight runStudentCode settles Promise and sets isRunning false', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
      { verdict: 'AC', elapsed_ms: 12 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    // Start submit — worker is created but never completes
    const submitPromise = runner.submit('print(42)')
    await new Promise((r) => setTimeout(r, 0))

    expect(runner.isRunning.value).toBe(true)

    // Call stop while submission is in-flight
    runner.stop()

    // The Promise should settle (not hang)
    const result = await Promise.race([
      submitPromise.then(() => 'settled'),
      new Promise((r) => setTimeout(() => r('timeout'), 500)),
    ])
    expect(result).toBe('settled')
    expect(runner.isRunning.value).toBe(false)
  })

  // Task 2.2: killTimer does not fire after stop
  it('killTimer does not fire after stop()', async () => {
    vi.useFakeTimers()
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    const submitPromise = runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    // Stop while in-flight
    runner.stop()

    // Advance time past the kill timeout — the killTimer callback should NOT fire
    // (worker.terminate should have been called only once by stop, not again by killTimer)
    const terminateCountAfterStop = submitWorker.terminate.mock.calls.length
    await vi.advanceTimersByTimeAsync(60_000)

    // killTimer would have called terminate again if not cleared
    expect(submitWorker.terminate.mock.calls.length).toBe(terminateCountAfterStop)

    await submitPromise
  })

  // Task 2.3: stop when no submission is in-flight is a no-op
  it('stop() when no submission is in-flight is a no-op', async () => {
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    // Should not throw
    expect(() => runner.stop()).not.toThrow()
    expect(runner.isRunning.value).toBe(false)
  })

  // Task 4.1: cleanup during prod submission cancels killTimer and settles Promise
  it('cleanup() during in-flight submission cancels killTimer and settles Promise', async () => {
    vi.useFakeTimers()
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    const submitPromise = runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    // Cleanup while in-flight
    runner.cleanup()

    // The Promise should settle
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

  // Task 4.3: no stale timer fires after cleanup (prod)
  it('no stale timer fires after cleanup()', async () => {
    vi.useFakeTimers()
    const { useChallengeRunner } = await import('../composables/useChallengeRunner')

    mockJudge.mockReturnValue([
      { verdict: 'AC', elapsed_ms: 10 },
    ])

    const runner = useChallengeRunner({
      id: 'caesar_encrypt',
      algorithm: 'caesar_encrypt',
      params: {},
      generator: '',
      testcaseCount: 2,
      starterCode: '',
      verdictDetail: 'hidden',
    })

    await runner.loadTestcases()

    runner.submit('print(42)')
    await vi.advanceTimersByTimeAsync(0)

    const submitWorker = mockWorkerInstances[mockWorkerInstances.length - 1]!

    runner.cleanup()

    const terminateCount = submitWorker.terminate.mock.calls.length

    // Advance well past any possible timer
    await vi.advanceTimersByTimeAsync(120_000)

    // terminate should not have been called again by stale timer
    expect(submitWorker.terminate.mock.calls.length).toBe(terminateCount)
  })
})
