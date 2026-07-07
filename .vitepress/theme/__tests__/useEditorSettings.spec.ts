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
    expect(normalizeEditorSettings({})).toEqual({
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 14,
    })
  })

  it('fills the missing closeBrackets field from defaults', () => {
    expect(normalizeEditorSettings({ autocomplete: false })).toEqual({
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    })
  })

  it('coerces non-boolean fields to their defaults', () => {
    // strings/numbers are not booleans → fall back to defaults
    expect(normalizeEditorSettings({ autocomplete: 'yes', closeBrackets: 0 })).toEqual({
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 14,
    })
  })

  it('garbage input degrades to defaults without throwing', () => {
    expect(normalizeEditorSettings(null)).toEqual(DEFAULT_EDITOR_SETTINGS)
    expect(normalizeEditorSettings('nope')).toEqual(DEFAULT_EDITOR_SETTINGS)
    expect(normalizeEditorSettings(42)).toEqual(DEFAULT_EDITOR_SETTINGS)
  })

  // fontSize numeric normalization — rows taken from the spec Example table.
  it.each([
    [100, 24], // above max → clamped down
    [3, 10], // below min → clamped up
    [15.6, 16], // non-integer → rounded to nearest
    [9.4, 10], // rounds to 9 then clamps up to the min
    [23.6, 24], // rounds to 24, stays at the max
    [14, 14], // already valid → unchanged
    [10, 10], // lower bound
    [24, 24], // upper bound
  ])('clamps/rounds a numeric fontSize %p to %p', (input, expected) => {
    expect(normalizeEditorSettings({ fontSize: input }).fontSize).toBe(expected)
  })

  it.each([['big'], [null], [undefined], [NaN], [Infinity], [-Infinity], [{}], [[]]])(
    'falls back to the default fontSize when the stored value is %p',
    (bad) => {
      expect(normalizeEditorSettings({ fontSize: bad }).fontSize).toBe(14)
    },
  )

  // Schema v1 → v2 migration: fill fontSize from default, bump version,
  // preserve the student's existing boolean choices.
  it('upgrades a version-1 object without losing choices (Scenario: Version 1 object upgrades without losing choices)', () => {
    expect(normalizeEditorSettings({ version: 1, autocomplete: false })).toEqual({
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    })
  })
})

describe('useEditorSettings (Requirement: Persistent editor settings)', () => {
  it('returns defaults when localStorage is empty (Requirement: Default settings preserve current behavior)', () => {
    expect(useEditorSettings().value).toEqual({
      version: 2,
      autocomplete: true,
      closeBrackets: true,
      fontSize: 14,
    })
  })

  it('reads and merges a partial stored object', () => {
    localStorage.setItem(EDITOR_SETTINGS_KEY, JSON.stringify({ autocomplete: false }))
    expect(useEditorSettings().value).toEqual({
      version: 2,
      autocomplete: false,
      closeBrackets: true,
      fontSize: 14,
    })
  })

  it('clamps an out-of-range stored fontSize on read (Scenario: Out-of-range stored value is clamped on read)', () => {
    localStorage.setItem(EDITOR_SETTINGS_KEY, JSON.stringify({ fontSize: 100 }))
    expect(useEditorSettings().value.fontSize).toBe(24)
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

  it('persists a fontSize change across a fresh read', async () => {
    const s = useEditorSettings()
    s.value = { ...s.value, fontSize: 18 }
    await nextTick()
    await flushPromises()
    expect(JSON.parse(localStorage.getItem(EDITOR_SETTINGS_KEY) as string).fontSize).toBe(18)
    _resetEditorSettingsForTests()
    expect(useEditorSettings().value.fontSize).toBe(18)
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
