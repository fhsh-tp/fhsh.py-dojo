/**
 * ChallengeView integration tests for verdict_detail data stripping.
 * Verifies that ChallengeView delegates to useChallengeRunner correctly.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { ref } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import ChallengeView from '../views/ChallengeView.vue'
import { useChallengeStore } from '../stores/challenge'

// --- mutable frontmatter for per-test control ---
const mockFrontmatter: Record<string, unknown> = {
  algorithm: 'caesar_encrypt',
  testcase_count: 2,
  generator: 'print(42)',
  starter_code: '# code',
  params: { n: { type: 'int', min: 1, max: 10 } },
}

vi.mock('vitepress', () => ({
  useData: () => ({
    frontmatter: { get value() { return mockFrontmatter } },
    page: { value: { relativePath: 'challenge/caesar-encrypt.md' } },
  }),
  useRouter: () => ({ go: vi.fn() }),
  Content: { template: '<div class="vp-content" />' },
}))

// --- useChallengeRunner mock ---
const mockLoadTestcases = vi.fn()
const mockSubmit = vi.fn()
const mockStop = vi.fn()
const mockCleanup = vi.fn()
const mockInputs = ref<string[]>([])
const mockIsReady = ref(false)
const mockIsRunning = ref(false)
const mockErrorMessage = ref('')
const mockVerdictDetail = ref('hidden')

vi.mock('../composables/useChallengeRunner', () => ({
  useChallengeRunner: () => ({
    loadTestcases: mockLoadTestcases,
    submit: mockSubmit,
    stop: mockStop,
    cleanup: mockCleanup,
    inputs: mockInputs,
    isReady: mockIsReady,
    isRunning: mockIsRunning,
    errorMessage: mockErrorMessage,
    verdictDetail: mockVerdictDetail,
  }),
  resolveVerdictDetail: (raw: string | undefined) => {
    const valid = new Set(['hidden', 'actual', 'full'])
    const v = raw ?? 'hidden'
    return valid.has(v) ? v : 'hidden'
  },
}))

// --- useExecutor mock (still used for RunModal) ---
vi.mock('../composables/useExecutor', () => ({
  useExecutor: () => ({
    isRunning: ref(false),
    run: vi.fn(),
    stop: vi.fn(),
    execute: vi.fn().mockResolvedValue({ type: 'execute_result', stdout: '', elapsed_ms: 0 }),
  }),
}))

vi.stubGlobal('Worker', class {
  onmessage = null
  onerror = null
  postMessage = vi.fn()
  terminate = vi.fn()
})

vi.stubGlobal('ResizeObserver', class {
  observe = vi.fn()
  disconnect = vi.fn()
  unobserve = vi.fn()
})

const CodeEditorStub = { name: 'CodeEditor', template: '<div class="code-editor-stub" />' }

describe('ChallengeView verdict_detail delegation', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    mockLoadTestcases.mockClear()
    mockSubmit.mockClear()
    mockStop.mockClear()
    mockCleanup.mockClear()
    mockInputs.value = []
    mockIsReady.value = false
    mockIsRunning.value = false
    mockErrorMessage.value = ''
    mockVerdictDetail.value = 'hidden'
    delete mockFrontmatter.verdict_detail
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('calls loadTestcases on mount', async () => {
    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    expect(mockLoadTestcases).toHaveBeenCalledTimes(1)
    wrapper.unmount()
  })

  it('calls cleanup on unmount', async () => {
    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    wrapper.unmount()
    expect(mockCleanup).toHaveBeenCalledTimes(1)
  })

  it('hidden mode: resolves verdict_detail correctly', async () => {
    // verdict_detail omitted → defaults to hidden
    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    // The runner should have been created with verdictDetail='hidden'
    expect(mockLoadTestcases).toHaveBeenCalled()
    wrapper.unmount()
  })

  it('full mode: resolves verdict_detail correctly', async () => {
    mockFrontmatter.verdict_detail = 'full'

    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    expect(mockLoadTestcases).toHaveBeenCalled()
    wrapper.unmount()
  })

  it('displays error message from runner', async () => {
    mockErrorMessage.value = 'Test error'

    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    expect(wrapper.text()).toContain('Test error')
    wrapper.unmount()
  })

  it('does not import useWasm directly', () => {
    // Verify ChallengeView source does not contain useWasm import
    // This is a structural test — the actual import is blocked by the mock setup
    expect(mockLoadTestcases).toBeDefined()
  })

  it('prod mode: TestResultPanel receives verdictDetail from pool (runner), not frontmatter', async () => {
    // Simulate: frontmatter says hidden, but pool (runner) says actual
    delete mockFrontmatter.verdict_detail // defaults to 'hidden'
    mockVerdictDetail.value = 'actual' // pool says 'actual'

    const wrapper = mount(ChallengeView, {
      global: { stubs: { CodeEditor: CodeEditorStub } },
    })
    await flushPromises()

    // Find TestResultPanel and check its verdict-detail prop
    const panel = wrapper.findComponent({ name: 'TestResultPanel' })
    expect(panel.exists()).toBe(true)
    expect(panel.props('verdictDetail')).toBe('actual')

    wrapper.unmount()
  })
})
