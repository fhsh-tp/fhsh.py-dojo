import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { ref, nextTick } from 'vue'
import CodeEditor from '../components/editor/CodeEditor.vue'

// ── Hoist spies so they are available inside vi.mock factories ────────────────
const {
  closeBracketsSpy,
  autocompletionSpy,
  editorViewCtorSpy,
  dispatchSpy,
  themeSpy,
  settingsHolder,
} = vi.hoisted(() => ({
  closeBracketsSpy: vi.fn(() => ({ extension: 'closeBrackets' })),
  autocompletionSpy: vi.fn(() => ({ extension: 'autocompletion' })),
  editorViewCtorSpy: vi.fn(),
  dispatchSpy: vi.fn(),
  // Records every EditorView.theme(spec) call so tests can assert the font-size
  // theme is built from settings.value.fontSize (the real fontSizeThemeSpec is used).
  themeSpy: vi.fn(() => ({})),
  // Holds the reactive settings ref the mocked useEditorSettings hands back.
  settingsHolder: { ref: null as ReturnType<typeof ref> | null },
}))

// ── Stubs for CodeMirror modules (dynamically imported in onMounted) ─────────

vi.mock('@codemirror/autocomplete', () => ({
  closeBrackets: closeBracketsSpy,
  closeBracketsKeymap: [],
  autocompletion: autocompletionSpy,
  localCompletionSource: vi.fn(),
}))

vi.mock('@codemirror/view', () => {
  class EditorView {
    static updateListener = { of: vi.fn(() => ({})) }
    static theme = themeSpy
    requestMeasure = vi.fn()
    destroy = vi.fn()
    state = { doc: { toString: () => '' } }
    dispatch = dispatchSpy
    constructor() {
      editorViewCtorSpy()
    }
  }
  return {
    EditorView,
    keymap: { of: vi.fn(() => ({})) },
    lineNumbers: vi.fn(() => ({})),
    drawSelection: vi.fn(() => ({})),
    dropCursor: vi.fn(() => ({})),
    rectangularSelection: vi.fn(() => ({})),
  }
})

vi.mock('@codemirror/commands', () => ({
  defaultKeymap: [],
  history: vi.fn(() => ({})),
  historyKeymap: [],
  indentWithTab: {},
}))

vi.mock('@codemirror/lang-python', () => ({
  python: vi.fn(() => ({})),
  pythonLanguage: {
    data: {
      of: vi.fn(() => ({})),
    },
  },
}))

vi.mock('@codemirror/theme-one-dark', () => ({
  oneDark: {},
}))

vi.mock('@codemirror/state', () => {
  class Compartment {
    of(ext: unknown) {
      return ext
    }
    reconfigure(ext: unknown) {
      return { reconfigure: ext }
    }
  }
  return {
    EditorState: {
      create: vi.fn(() => ({})),
      tabSize: { of: vi.fn(() => ({})) },
    },
    Compartment,
    Prec: { highest: (ext: unknown) => ext },
  }
})

// vi.mock paths resolve relative to THIS test file → composables is one level up.
vi.mock('../composables/pythonCompletions', () => ({
  pythonStdlibCompletions: vi.fn(() => () => null),
}))

// Controllable editor settings — each test starts from defaults (both enabled).
// NOTE: vi.mock paths resolve relative to THIS test file, so the composables
// dir is one level up (../composables), not two.
vi.mock('../composables/useEditorSettings', () => ({
  useEditorSettings: () => settingsHolder.ref,
}))

vi.stubGlobal(
  'ResizeObserver',
  class {
    observe = vi.fn()
    disconnect = vi.fn()
  },
)

// Wait until the skeleton disappears — signals lazy imports resolved and editor built.
async function waitForEditor(wrapper: ReturnType<typeof mount>) {
  await vi.waitFor(
    () => {
      expect(wrapper.find('[class*="animate-pulse"]').exists()).toBe(false)
    },
    { timeout: 2000 },
  )
}

// ─────────────────────────────────────────────────────────────────────────────

describe('CodeEditor', () => {
  beforeEach(() => {
    closeBracketsSpy.mockClear()
    autocompletionSpy.mockClear()
    editorViewCtorSpy.mockClear()
    dispatchSpy.mockClear()
    themeSpy.mockClear()
    settingsHolder.ref = ref({ version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 })
  })

  it('shows skeleton while loading', () => {
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    expect(wrapper.find('[class*="animate-pulse"]').exists()).toBe(true)
  })

  it('calls closeBrackets during editor initialisation when enabled (Requirement: Bracket auto-closing)', async () => {
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(closeBracketsSpy).toHaveBeenCalled()
  })

  it('calls autocompletion during editor initialisation when enabled (Requirement: Automatic completion trigger)', async () => {
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(autocompletionSpy).toHaveBeenCalled()
  })

  it('does NOT wire autocompletion when the setting is disabled (Requirement: Automatic completion trigger)', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    }
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(autocompletionSpy).not.toHaveBeenCalled()
  })

  it('does NOT wire closeBrackets when the setting is disabled (Requirement: Bracket auto-closing)', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: false,
      fontSize: 14,
    }
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(closeBracketsSpy).not.toHaveBeenCalled()
  })

  it('reconfigures without rebuilding the editor when a setting toggles (Requirement: Live application without editor rebuild)', async () => {
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(editorViewCtorSpy).toHaveBeenCalledTimes(1)
    dispatchSpy.mockClear()

    // toggle autocomplete off
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    }
    await nextTick()
    await flushPromises()

    // no new EditorView was constructed; a reconfigure was dispatched instead
    expect(editorViewCtorSpy).toHaveBeenCalledTimes(1)
    expect(dispatchSpy).toHaveBeenCalled()
  })

  it('reconfigures without rebuilding the editor when the font size changes (Requirement: Adjustable editor font size)', async () => {
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    expect(editorViewCtorSpy).toHaveBeenCalledTimes(1)
    dispatchSpy.mockClear()

    // bump the font size
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 18,
    }
    await nextTick()
    await flushPromises()

    // no new EditorView was constructed; a reconfigure was dispatched instead
    expect(editorViewCtorSpy).toHaveBeenCalledTimes(1)
    expect(dispatchSpy).toHaveBeenCalled()
  })

  it('builds the font-size theme from settings.value.fontSize on init (Requirement: Adjustable editor font size)', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 22,
    }
    const wrapper = mount(CodeEditor, { props: { modelValue: '' } })
    await waitForEditor(wrapper)
    // The seeded font size flows through the real fontSizeThemeSpec into EditorView.theme.
    expect(themeSpy).toHaveBeenCalledWith({ '&': { fontSize: '22px' } })
  })
})
