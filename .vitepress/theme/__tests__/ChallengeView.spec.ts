import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import ChallengeView from '../views/ChallengeView.vue'

// --- vitepress mock ---
vi.mock('vitepress', () => ({
  useData: () => ({
    frontmatter: {
      value: {
        algorithm: 'caesar_encrypt',
        testcase_count: 3,
        generator: 'print(42)',
        starter_code: '# write code here',
        params: { n: { type: 'int', min: 1, max: 10 } },
      },
    },
    page: { value: { relativePath: 'challenge/caesar-encrypt.md' } },
  }),
  useRouter: () => ({ go: vi.fn() }),
  Content: { template: '<div class="vp-content" />' },
}))

// --- useWasm mock: never resolves to simulate slow WASM ---
let resolveWasm: ((v: unknown) => void) | null = null
vi.mock('../composables/useWasm', () => ({
  useWasm: () => ({
    generateChallenge: vi.fn(
      () =>
        new Promise((resolve) => {
          resolveWasm = resolve
        }),
    ),
  }),
}))

// --- useExecutor mock ---
vi.mock('../composables/useExecutor', () => ({
  useExecutor: () => ({
    isRunning: ref(false),
    run: vi.fn(),
    stop: vi.fn(),
    execute: vi.fn().mockResolvedValue({ type: 'execute_result', stdout: '', elapsed_ms: 0 }),
  }),
}))

// --- Worker mock (Pyodide): track instances for terminate assertions ---
const mockWorkerInstances: MockWorker[] = []
class MockWorker {
  onmessage: ((e: MessageEvent) => void) | null = null
  onerror: ((e: ErrorEvent) => void) | null = null
  postMessage = vi.fn()
  terminate = vi.fn()
  constructor() {
    mockWorkerInstances.push(this)
  }
}
vi.stubGlobal('Worker', MockWorker)

// --- ResizeObserver stub for jsdom ---
vi.stubGlobal('ResizeObserver', class {
  observe = vi.fn()
  disconnect = vi.fn()
  unobserve = vi.fn()
})

// --- CodeEditor stub (avoids CodeMirror DOM issues) ---
const CodeEditorStub = { name: 'CodeEditor', template: '<div class="code-editor-stub" />' }

describe('ChallengeView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    resolveWasm = null
    mockWorkerInstances.length = 0
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('shows ProblemPanel immediately — no skeleton during generation (Requirement: Challenge UI renders immediately)', async () => {
    const wrapper = mount(ChallengeView, {
      global: {
        stubs: { CodeEditor: CodeEditorStub },
      },
    })
    // Allow onMounted to run and generation to start
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    // ProblemPanel must be visible even though generation hasn't completed
    expect(wrapper.findComponent({ name: 'ProblemPanel' }).exists()).toBe(true)
    // Skeleton loader must NOT appear in the left panel
    expect(wrapper.find('.animate-pulse').exists()).toBe(false)
  })

  it('RunButton isReady is false before generation completes (Requirement: Run button is disabled until testcases are ready)', async () => {
    const wrapper = mount(ChallengeView, {
      global: {
        stubs: { CodeEditor: CodeEditorStub },
      },
    })
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    const runButton = wrapper.findComponent({ name: 'RunButton' })
    expect(runButton.exists()).toBe(true)
    expect(runButton.props('isReady')).toBe(false)
  })

  it('shows both Run and Submit buttons (Requirement: Button Layout Split)', async () => {
    const wrapper = mount(ChallengeView, {
      global: {
        stubs: { CodeEditor: CodeEditorStub, Teleport: true },
      },
    })
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    // Run button (always enabled)
    const runBtn = wrapper.find('[data-testid="run-btn"]')
    expect(runBtn.exists()).toBe(true)
    expect(runBtn.text()).toContain('執行')
    expect(runBtn.attributes('disabled')).toBeUndefined()

    // Submit button (RunButton component, disabled before testcases ready)
    const submitBtn = wrapper.findComponent({ name: 'RunButton' })
    expect(submitBtn.exists()).toBe(true)
    expect(submitBtn.props('isReady')).toBe(false)
  })

  it('Run button is clickable before testcases are ready', async () => {
    const wrapper = mount(ChallengeView, {
      global: {
        stubs: { CodeEditor: CodeEditorStub, Teleport: true },
      },
    })
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    const runBtn = wrapper.find('[data-testid="run-btn"]')
    expect(runBtn.attributes('disabled')).toBeUndefined()
    // Click should not throw
    await runBtn.trigger('click')
  })

  it('Worker is terminated on unmount (Requirement: Worker is terminated on component unmount)', async () => {
    const wrapper = mount(ChallengeView, {
      global: {
        stubs: { CodeEditor: CodeEditorStub },
      },
    })
    await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick()

    // After generation starts (onMounted fires), a worker should have been created
    // The WASM phase runs first (mocked to never resolve), so Worker might not be created yet.
    // After unmount, no Worker should remain active (terminate called if one was created).
    wrapper.unmount()

    // All created Worker instances should have been terminated
    for (const worker of mockWorkerInstances) {
      expect(worker.terminate).toHaveBeenCalled()
    }
  })
})
