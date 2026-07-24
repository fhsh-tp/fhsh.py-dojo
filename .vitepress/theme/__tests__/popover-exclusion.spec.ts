import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, type VueWrapper } from '@vue/test-utils'
import { defineComponent, h, ref } from 'vue'
import DownloadRecordButton from '../components/editor/DownloadRecordButton.vue'
import EditorSettingsPopover from '../components/editor/EditorSettingsPopover.vue'

/**
 * Integration test for mutual exclusion between the two REAL popover
 * components (Requirement: Mutual exclusion between anchored popovers;
 * editor-settings scenario "Another popover opening closes settings").
 *
 * useAnchoredPopover.spec.ts proves the registry mechanism with synthetic
 * hosts; this file proves the two production components actually share the
 * same module-level registry when mounted on one page, without referencing
 * each other.
 */

vi.mock('../persistence/db', () => ({ listSessions: vi.fn().mockResolvedValue([]) }))
vi.mock('../lib/download', () => ({ downloadTextFile: vi.fn() }))
const { settingsHolder } = vi.hoisted(() => ({
  settingsHolder: { ref: null as ReturnType<typeof ref> | null },
}))
vi.mock('../composables/useEditorSettings', () => ({
  useEditorSettings: () => settingsHolder.ref,
  DEFAULT_EDITOR_SETTINGS: { version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 },
}))

const GEAR = '[data-testid="editor-settings-gear"]'
const DL_BTN = '[data-testid="download-record-btn"]'
const SETTINGS_PANEL = '[data-testid="editor-settings-panel"]'
const DL_PANEL = '[data-testid="download-panel"]'

const Host = defineComponent({
  render() {
    return h('div', [
      h(DownloadRecordButton, { slug: 'arithmetic-sum', title: '等差數列求和' }),
      h(EditorSettingsPopover),
    ])
  },
})

let wrapper: VueWrapper | null = null

const settingsOpen = () => document.querySelector(SETTINGS_PANEL) !== null
const downloadOpen = () => {
  const el = document.querySelector(DL_PANEL) as HTMLElement | null
  return el !== null && el.style.display !== 'none'
}

beforeEach(() => {
  settingsHolder.ref = ref({ version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 })
  wrapper = mount(Host, { attachTo: document.body })
})
afterEach(() => {
  wrapper?.unmount()
  wrapper = null
  document.querySelectorAll(`${SETTINGS_PANEL}, ${DL_PANEL}`).forEach((el) => el.remove())
})

describe('popover mutual exclusion between the real components', () => {
  it('opening the download popover closes the settings popover', async () => {
    await wrapper!.find(GEAR).trigger('click')
    await flushPromises()
    expect(settingsOpen()).toBe(true)

    await wrapper!.find(DL_BTN).trigger('click')
    await flushPromises()
    expect(settingsOpen()).toBe(false)
    expect(downloadOpen()).toBe(true)
  })

  it('opening the settings popover closes the download popover', async () => {
    await wrapper!.find(DL_BTN).trigger('click')
    await flushPromises()
    expect(downloadOpen()).toBe(true)

    await wrapper!.find(GEAR).trigger('click')
    await flushPromises()
    expect(downloadOpen()).toBe(false)
    expect(settingsOpen()).toBe(true)
  })
})
