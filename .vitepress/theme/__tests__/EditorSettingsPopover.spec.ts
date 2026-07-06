import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, DOMWrapper, type VueWrapper } from '@vue/test-utils'
import { ref } from 'vue'
import EditorSettingsPopover from '../components/editor/EditorSettingsPopover.vue'

// Controllable, shared editor-settings ref. vi.mock paths resolve relative to
// THIS test file → composables is one level up (../composables).
const { settingsHolder } = vi.hoisted(() => ({
  settingsHolder: { ref: null as ReturnType<typeof ref> | null },
}))

vi.mock('../composables/useEditorSettings', () => ({
  useEditorSettings: () => settingsHolder.ref,
  DEFAULT_EDITOR_SETTINGS: { version: 1, autocomplete: true, closeBrackets: true },
}))

let wrapper: VueWrapper | null = null

function mountPopover() {
  wrapper = mount(EditorSettingsPopover, { attachTo: document.body })
  return wrapper
}

const GEAR = '[data-testid="editor-settings-gear"]'
const PANEL = '[data-testid="editor-settings-panel"]'
const AC = '[data-testid="toggle-autocomplete"]'
const CB = '[data-testid="toggle-close-brackets"]'
const RESET = '[data-testid="editor-settings-reset"]'

// The panel is teleported to <body>, so it lives outside the wrapper's subtree.
const panelEl = () => document.querySelector(PANEL)
const dom = (sel: string) => new DOMWrapper(document.querySelector(sel) as Element)

beforeEach(() => {
  settingsHolder.ref = ref({ version: 1, autocomplete: true, closeBrackets: true })
})
afterEach(() => {
  wrapper?.unmount()
  wrapper = null
  // Safety: drop any teleported panel left in <body>.
  document.querySelectorAll(PANEL).forEach((el) => el.remove())
})

describe('EditorSettingsPopover (Requirement: Editor settings entry point)', () => {
  it('shows a gear button and no panel initially', () => {
    const w = mountPopover()
    expect(w.find(GEAR).exists()).toBe(true)
    expect(panelEl()).toBeNull()
  })

  it('opens the panel (teleported to body) with two toggles reflecting current settings', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect(panelEl()).not.toBeNull()
    expect((document.querySelector(AC) as HTMLInputElement).checked).toBe(true)
    expect((document.querySelector(CB) as HTMLInputElement).checked).toBe(true)
  })

  it('reflects a disabled setting as an unchecked toggle', async () => {
    settingsHolder.ref!.value = { version: 1, autocomplete: false, closeBrackets: true }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect((document.querySelector(AC) as HTMLInputElement).checked).toBe(false)
  })

  it('toggling a switch updates the shared settings', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(AC).setValue(false)
    expect((settingsHolder.ref!.value as { autocomplete: boolean }).autocomplete).toBe(false)
  })

  it('reset restores defaults', async () => {
    settingsHolder.ref!.value = { version: 1, autocomplete: false, closeBrackets: false }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(RESET).trigger('click')
    expect(settingsHolder.ref!.value).toEqual({ version: 1, autocomplete: true, closeBrackets: true })
  })

  it('closes on Escape', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect(panelEl()).not.toBeNull()
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await flushPromises()
    expect(panelEl()).toBeNull()
  })

  // Dismiss is bound to mousedown so that grabbing the bottom-panel drag handle
  // (also a mousedown) closes the popover before the drag shifts the gear.
  it('closes on an outside mousedown', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect(panelEl()).not.toBeNull()
    document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(panelEl()).toBeNull()
  })
})
