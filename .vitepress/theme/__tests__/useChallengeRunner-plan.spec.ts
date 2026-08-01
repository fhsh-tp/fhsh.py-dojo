/**
 * Tests for useChallengeRunner testcase_plan support.
 * Dev strategy must route plan challenges through generate_dev_inputs;
 * prod strategy must request exactly the plan total from select_testcases.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

// ── WASM pool module mock (prod) ──────────────────────────────────────────
const mockLoadPool = vi.fn()
const mockSelectTestcases = vi.fn()
const mockJudge = vi.fn()
const mockGetExpected = vi.fn()

vi.mock('/wasm/testcase_generator.js', () => ({
  default: vi.fn().mockResolvedValue(undefined),
  load_pool: mockLoadPool,
  select_testcases: mockSelectTestcases,
  judge: mockJudge,
  get_expected: mockGetExpected,
}))

// ── fetch mock (prod) ─────────────────────────────────────────────────────
const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

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

// ── useWasm mock (dev) ────────────────────────────────────────────────────
const mockGenerateChallenge = vi.fn()
const mockGenerateDevInputs = vi.fn()
vi.mock('../composables/useWasm', () => ({
  useWasm: () => ({
    generateChallenge: mockGenerateChallenge,
    generateDevInputs: mockGenerateDevInputs,
  }),
}))

const PLAN = [
  { count: 2, override: { n: { max: 20 } } },
  { count: 1, override: { n: { min: 2500 } } },
  { literal: '1\n1\n-999\n' },
]
const PLAN_TOTAL = 4

function planConfig() {
  return {
    id: 'deque-find-min-max',
    algorithm: 'deque-scan',
    params: { n: { type: 'int', min: 1, max: 4000 } },
    generator: 'print(input())',
    // Deliberately wrong count: a plan must override it with the plan total.
    testcaseCount: 99,
    starterCode: '',
    verdictDetail: 'hidden' as const,
    testcasePlan: PLAN,
  }
}

describe('computePlanTotal', () => {
  it('sums band counts and counts each literal as one', async () => {
    const { computePlanTotal } = await import('../composables/useChallengeRunner')
    expect(computePlanTotal(PLAN)).toBe(PLAN_TOTAL)
  })
})

describe('dev strategy with testcase_plan', () => {
  let originalProd: boolean

  beforeEach(() => {
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = false
  })

  afterEach(() => {
    // @ts-expect-error - restoring read-only env
    import.meta.env.PROD = originalProd
    mockWorkerInstances.length = 0
    vi.clearAllMocks()
  })

  it('routes through generateDevInputs with the full plan spec, preserving order', async () => {
    const devInputs = ['5\n', '17\n', '3000\n', '1\n1\n-999\n']
    mockGenerateDevInputs.mockResolvedValue({ inputs: devInputs })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner(planConfig())
    const loading = runner.loadTestcases()

    // Generator worker phase: echo each input back as its expected output.
    await vi.waitFor(() => {
      expect(mockWorkerInstances.length).toBe(1)
    })
    mockWorkerInstances[0]!.onmessage!({
      data: {
        type: 'generate_complete',
        testcases: devInputs.map((input) => ({ input, expected_output: input })),
      },
    } as MessageEvent)
    await loading

    expect(mockGenerateDevInputs).toHaveBeenCalledWith(
      JSON.stringify({ params: planConfig().params, testcase_plan: PLAN }),
    )
    expect(mockGenerateChallenge).not.toHaveBeenCalled()
    expect(runner.inputs.value).toEqual(devInputs)
    expect(runner.isReady.value).toBe(true)
  })

  it('surfaces an engine rejection instead of silently degrading', async () => {
    mockGenerateDevInputs.mockResolvedValue(null)

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner(planConfig())
    await runner.loadTestcases()

    expect(runner.errorMessage.value).toContain('testcase_plan')
    expect(runner.isReady.value).toBe(false)
    expect(mockGenerateChallenge).not.toHaveBeenCalled()
  })

  it('keeps non-plan challenges on generateChallenge', async () => {
    mockGenerateChallenge.mockResolvedValue({ inputs: ['1\n'] })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const config = { ...planConfig(), testcasePlan: undefined, testcaseCount: 1 }
    const loading = runner_load(useChallengeRunner(config))

    await vi.waitFor(() => {
      expect(mockWorkerInstances.length).toBe(1)
    })
    mockWorkerInstances[0]!.onmessage!({
      data: {
        type: 'generate_complete',
        testcases: [{ input: '1\n', expected_output: '1\n' }],
      },
    } as MessageEvent)
    await loading

    expect(mockGenerateChallenge).toHaveBeenCalledWith(JSON.stringify(config.params), 1)
    expect(mockGenerateDevInputs).not.toHaveBeenCalled()
  })

  function runner_load(runner: { loadTestcases(): Promise<void> }) {
    return runner.loadTestcases()
  }
})

describe('prod strategy with testcase_plan', () => {
  let originalProd: boolean

  beforeEach(() => {
    setActivePinia(createPinia())
    originalProd = import.meta.env.PROD
    // @ts-expect-error - overriding read-only env for test
    import.meta.env.PROD = true

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

  it('requests exactly the plan total, ignoring testcaseCount', async () => {
    mockSelectTestcases.mockReturnValue({
      inputs: ['5\n', '17\n', '3000\n', '1\n1\n-999\n'],
      session_id: 's_plan',
      verdict_detail: 'hidden',
    })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner(planConfig())
    await runner.loadTestcases()

    expect(mockSelectTestcases).toHaveBeenCalledWith('deque-find-min-max', PLAN_TOTAL)
    expect(runner.isReady.value).toBe(true)
  })

  it('surfaces a WASM count-mismatch error to the user', async () => {
    mockSelectTestcases.mockImplementation(() => {
      throw new Error('Plan pool requires exactly 4 testcases per session, requested 99')
    })

    const { useChallengeRunner } = await import('../composables/useChallengeRunner')
    const runner = useChallengeRunner(planConfig())
    await runner.loadTestcases()

    expect(runner.errorMessage.value).toContain('exactly 4')
    expect(runner.isReady.value).toBe(false)
  })
})
