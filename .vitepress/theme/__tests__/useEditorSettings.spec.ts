import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { nextTick } from 'vue'
import { flushPromises } from '@vue/test-utils'
import {
  useEditorSettings,
  normalizeEditorSettings,
  DEFAULT_EDITOR_SETTINGS,
  EDITOR_SETTINGS_KEY,
  _resetEditorSettingsForTests,
} from '../composables/useEditorSettings'

beforeEach(() => {
  localStorage.clear()
  _resetEditorSettingsForTests()
})
afterEach(() => {
  localStorage.clear()
  _resetEditorSettingsForTests()
})

describe('normalizeEditorSettings (Requirement: Settings data contract with defaults merge and normalization)', () => {
  it('empty object yields defaults', () => {
    expect(normalizeEditorSettings({})).toEqual({ version: 1, autocomplete: true, closeBrackets: true })
  })

  it('fills the missing closeBrackets field from defaults', () => {
    expect(normalizeEditorSettings({ autocomplete: false })).toEqual({
      version: 1,
      autocomplete: false,
      closeBrackets: true,
    })
  })

  it('coerces non-boolean fields to their defaults', () => {
    // strings/numbers are not booleans → fall back to defaults
    expect(normalizeEditorSettings({ autocomplete: 'yes', closeBrackets: 0 })).toEqual({
      version: 1,
      autocomplete: true,
      closeBrackets: true,
    })
  })

  it('garbage input degrades to defaults without throwing', () => {
    expect(normalizeEditorSettings(null)).toEqual(DEFAULT_EDITOR_SETTINGS)
    expect(normalizeEditorSettings('nope')).toEqual(DEFAULT_EDITOR_SETTINGS)
    expect(normalizeEditorSettings(42)).toEqual(DEFAULT_EDITOR_SETTINGS)
  })
})

describe('useEditorSettings (Requirement: Persistent editor settings)', () => {
  it('returns defaults when localStorage is empty (Requirement: Default settings preserve current behavior)', () => {
    expect(useEditorSettings().value).toEqual({ version: 1, autocomplete: true, closeBrackets: true })
  })

  it('reads and merges a partial stored object', () => {
    localStorage.setItem(EDITOR_SETTINGS_KEY, JSON.stringify({ autocomplete: false }))
    expect(useEditorSettings().value).toEqual({ version: 1, autocomplete: false, closeBrackets: true })
  })

  it('degrades corrupt JSON to defaults', () => {
    localStorage.setItem(EDITOR_SETTINGS_KEY, 'this is not json')
    expect(useEditorSettings().value).toEqual(DEFAULT_EDITOR_SETTINGS)
  })

  it('persists a change across a fresh read (persistence round-trip)', async () => {
    const s = useEditorSettings()
    s.value = { ...s.value, autocomplete: false }
    await nextTick()
    await flushPromises()
    // written to localStorage
    expect(JSON.parse(localStorage.getItem(EDITOR_SETTINGS_KEY) as string).autocomplete).toBe(false)
    // a fresh singleton reads the persisted value back
    _resetEditorSettingsForTests()
    expect(useEditorSettings().value.autocomplete).toBe(false)
  })

  it('shares one reactive ref across calls (same-tab singleton)', () => {
    expect(useEditorSettings()).toBe(useEditorSettings())
  })
})

describe('useEditorSettings SSR safety (Requirement: SSR-safe settings access)', () => {
  it('returns defaults without touching localStorage when window is undefined', () => {
    const originalWindow = globalThis.window
    const getItem = vi.spyOn(Storage.prototype, 'getItem')
    try {
      // simulate SSR
      // @ts-expect-error deleting window to emulate a non-browser environment
      delete globalThis.window
      const s = useEditorSettings()
      expect(s.value).toEqual(DEFAULT_EDITOR_SETTINGS)
      expect(getItem).not.toHaveBeenCalled()
    } finally {
      globalThis.window = originalWindow
      getItem.mockRestore()
    }
  })
})
