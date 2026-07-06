import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { Teleport } from 'vue'
import RunModal from '../components/editor/RunModal.vue'
import type { ExecuteResult } from '../workers/pyodide.worker'

// Mock useExecutor: capture the execute mock for test control
const executeMock = vi.fn<[string, string], Promise<ExecuteResult>>()
vi.mock('../composables/useExecutor', () => ({
  useExecutor: () => ({
    isRunning: { value: false },
    run: vi.fn(),
    stop: vi.fn(),
    execute: executeMock,
  }),
}))

// Helper to mount with Teleport disabled (renders inline)
function mountModal(props: { code: string; defaultStdin: string; isOpen: boolean }) {
  return mount(RunModal, {
    props,
    global: {
      stubs: { Teleport: true },
    },
  })
}

describe('RunModal', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    executeMock.mockResolvedValue({
      type: 'execute_result',
      stdout: 'hello\n',
      elapsed_ms: 10,
    })
  })

  it('renders modal with stdin textarea and execute button', () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: 'test input', isOpen: true })
    expect(wrapper.find('textarea').exists()).toBe(true)
    expect(wrapper.find('[data-testid="execute-btn"]').exists()).toBe(true)
  })

  // Run seam (Requirement: Run activity captured through a dedicated seam)
  it('emits a run event with stdin/stdout after executing', async () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: 'abc', isOpen: true })
    await wrapper.find('[data-testid="execute-btn"]').trigger('click')
    await flushPromises()
    const runEvents = wrapper.emitted('run')
    expect(runEvents).toBeTruthy()
    expect(runEvents?.[0]?.[0]).toMatchObject({ stdin: 'abc', stdout: 'hello\n' })
  })

  it('is hidden when isOpen is false', () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: '', isOpen: false })
    expect(wrapper.find('[data-testid="run-modal"]').exists()).toBe(false)
  })

  it('pre-fills stdin with defaultStdin prop (testcase[0].input)', () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: '3\nHELLO', isOpen: true })
    const textarea = wrapper.find('textarea')
    expect((textarea.element as HTMLTextAreaElement).value).toBe('3\nHELLO')
  })

  it('defaults stdin to empty string when defaultStdin is empty', () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: '', isOpen: true })
    const textarea = wrapper.find('textarea')
    expect((textarea.element as HTMLTextAreaElement).value).toBe('')
  })

  it('calls execute with code and stdin on Execute click', async () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: 'input data', isOpen: true })

    await wrapper.find('[data-testid="execute-btn"]').trigger('click')
    expect(executeMock).toHaveBeenCalledWith('print("hi")', 'input data')
  })

  it('displays stdout after execution', async () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: '', isOpen: true })

    await wrapper.find('[data-testid="execute-btn"]').trigger('click')
    // Wait for promise to resolve
    await flushPromises()

    expect(wrapper.find('[data-testid="output-area"]').text()).toContain('hello')
  })

  it('displays error after failed execution', async () => {
    executeMock.mockResolvedValueOnce({
      type: 'execute_result',
      stdout: '',
      elapsed_ms: 5,
      error: 'NameError: name "x" is not defined',
    })

    const wrapper = mountModal({ code: 'print(x)', defaultStdin: '', isOpen: true })

    await wrapper.find('[data-testid="execute-btn"]').trigger('click')
    await flushPromises()

    expect(wrapper.find('[data-testid="error-area"]').text()).toContain('NameError')
  })

  it('emits close when close button is clicked', async () => {
    const wrapper = mountModal({ code: 'print("hi")', defaultStdin: '', isOpen: true })

    await wrapper.find('[data-testid="close-btn"]').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('allows re-execute with modified stdin', async () => {
    const wrapper = mountModal({ code: 'print(input())', defaultStdin: 'first', isOpen: true })

    // First execute
    await wrapper.find('[data-testid="execute-btn"]').trigger('click')
    await flushPromises()

    // Modify stdin
    await wrapper.find('textarea').setValue('second')
    await wrapper.find('[data-testid="execute-btn"]').trigger('click')

    expect(executeMock).toHaveBeenCalledTimes(2)
    expect(executeMock).toHaveBeenLastCalledWith('print(input())', 'second')
  })
})
