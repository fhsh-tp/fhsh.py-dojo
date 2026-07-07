import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, DOMWrapper, type VueWrapper } from '@vue/test-utils'
import { ref } from 'vue'
import EditorSettingsPopover from '../components/editor/EditorSettingsPopover.vue'
import { FONT_SIZE_MIN, FONT_SIZE_MAX } from '../composables/editorConfig'

// Controllable, shared editor-settings ref. vi.mock paths resolve relative to
// THIS test file → composables is one level up (../composables).
const { settingsHolder } = vi.hoisted(() => ({
  settingsHolder: { ref: null as ReturnType<typeof ref> | null },
}))

vi.mock('../composables/useEditorSettings', () => ({
  useEditorSettings: () => settingsHolder.ref,
  DEFAULT_EDITOR_SETTINGS: { version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 },
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
const FS_DEC = '[data-testid="font-size-decrease"]'
const FS_INC = '[data-testid="font-size-increase"]'
const FS_VAL = '[data-testid="font-size-value"]'

// The panel is teleported to <body>, so it lives outside the wrapper's subtree.
const panelEl = () => document.querySelector(PANEL)
const dom = (sel: string) => new DOMWrapper(document.querySelector(sel) as Element)

beforeEach(() => {
  settingsHolder.ref = ref({ version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 })
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
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    }
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
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: false,
      closeBrackets: false,
      fontSize: 20,
    }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(RESET).trigger('click')
    expect(settingsHolder.ref!.value).toEqual({
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 14,
    })
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

describe('EditorSettingsPopover font-size stepper (Requirement: Adjustable editor font size)', () => {
  it('shows the current font size', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect((document.querySelector(FS_VAL) as HTMLElement).textContent).toContain('14px')
  })

  it('increase raises the shared font size by one step', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(FS_INC).trigger('click')
    expect((settingsHolder.ref!.value as { fontSize: number }).fontSize).toBe(15)
  })

  it('decrease lowers the shared font size by one step', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(FS_DEC).trigger('click')
    expect((settingsHolder.ref!.value as { fontSize: number }).fontSize).toBe(13)
  })

  it('disables the increase control at the maximum', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: FONT_SIZE_MAX,
    }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect((document.querySelector(FS_INC) as HTMLButtonElement).disabled).toBe(true)
    expect((document.querySelector(FS_DEC) as HTMLButtonElement).disabled).toBe(false)
  })

  it('disables the decrease control at the minimum', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: FONT_SIZE_MIN,
    }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    expect((document.querySelector(FS_DEC) as HTMLButtonElement).disabled).toBe(true)
    expect((document.querySelector(FS_INC) as HTMLButtonElement).disabled).toBe(false)
  })

  it('does not exceed the maximum when increasing at the bound', async () => {
    settingsHolder.ref!.value = {
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: FONT_SIZE_MAX,
    }
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    // The disabled button blocks clicks; the shared value stays clamped either way.
    await dom(FS_INC).trigger('click')
    expect((settingsHolder.ref!.value as { fontSize: number }).fontSize).toBe(FONT_SIZE_MAX)
  })

  // Regression (round-1 finding): the row must be a role="group" div, NOT a
  // for-less <label>. Under a <label>, a click on the non-interactive value text
  // is forwarded by the browser to the first labelable descendant (the − button),
  // silently shrinking and persisting the font size.
  it('does not change the font size when the row value text is clicked (Requirement: Adjustable editor font size)', async () => {
    const w = mountPopover()
    await w.find(GEAR).trigger('click')
    await flushPromises()
    await dom(FS_VAL).trigger('click')
    expect((settingsHolder.ref!.value as { fontSize: number }).fontSize).toBe(14)
  })
})
