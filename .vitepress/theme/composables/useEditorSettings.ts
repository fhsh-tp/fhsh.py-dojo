/**
 * Global, persistent editor preferences.
 *
 * The single owner of the editor-settings contract: defaults merge, schema
 * version, type normalization, and SSR-safe access. State is a module-level
 * singleton backed by `useLocalStorage`, so `CodeEditor.vue` and
 * `EditorSettingsPopover.vue` read one shared reactive source (two independent
 * `useLocalStorage` calls in the same tab do NOT auto-sync, hence the singleton).
 *
 * SSR-safe by construction: when `window` is absent, an ephemeral defaults ref
 * is returned and never cached as the singleton, so a server-rendered ref can
 * never leak into the client. `localStorage` is only ever touched on the client.
 */
import { ref, type Ref } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import { FONT_SIZE_MIN, FONT_SIZE_MAX, FONT_SIZE_DEFAULT } from './editorConfig'

export const EDITOR_SETTINGS_KEY = 'fhsh-py-dojo:editor-settings'
// v1: autocomplete + closeBrackets. v2: adds fontSize (additive — v1 blobs
// upgrade cleanly by filling fontSize from its default on read).
export const EDITOR_SETTINGS_SCHEMA_VERSION = 2

export interface EditorSettings {
  /** schema version, for forward-compatible migration of future fields. */
  version: number
  /** show the completion dropdown (and its "type hint" details) while typing. */
  autocomplete: boolean
  /** auto-insert the closing counterpart when typing ( [ {. */
  closeBrackets: boolean
  /** editor font size in px, clamped to [FONT_SIZE_MIN, FONT_SIZE_MAX]. */
  fontSize: number
}

export const DEFAULT_EDITOR_SETTINGS: EditorSettings = {
  version: EDITOR_SETTINGS_SCHEMA_VERSION,
  autocomplete: true,
  closeBrackets: true,
  fontSize: FONT_SIZE_DEFAULT,
}

/**
 * Coerce an arbitrary stored value into a valid font size: reject anything that
 * is not a finite number (falls back to the default), then round to the nearest
 * integer and clamp into the [MIN, MAX] range. Rounding happens before clamping
 * so e.g. 9.4 → 9 → 10 and 23.6 → 24 → 24.
 */
function normalizeFontSize(raw: unknown): number {
  if (typeof raw !== 'number' || !Number.isFinite(raw)) return FONT_SIZE_DEFAULT
  return Math.min(FONT_SIZE_MAX, Math.max(FONT_SIZE_MIN, Math.round(raw)))
}

/**
 * Merge a stored (possibly partial, corrupt, or wrong-typed) value over the
 * defaults and coerce field types. Never throws — unknown input degrades to
 * defaults. This is the forward-compatible migration point: `version` is always
 * rewritten to the current schema version, and any field missing from an older
 * schema (e.g. a v1 blob with no `fontSize`) is filled from its default while
 * existing choices are preserved.
 */
export function normalizeEditorSettings(raw: unknown): EditorSettings {
  const obj = raw && typeof raw === 'object' ? (raw as Record<string, unknown>) : {}
  return {
    version: EDITOR_SETTINGS_SCHEMA_VERSION,
    autocomplete:
      typeof obj.autocomplete === 'boolean'
        ? obj.autocomplete
        : DEFAULT_EDITOR_SETTINGS.autocomplete,
    closeBrackets:
      typeof obj.closeBrackets === 'boolean'
        ? obj.closeBrackets
        : DEFAULT_EDITOR_SETTINGS.closeBrackets,
    fontSize: normalizeFontSize(obj.fontSize),
  }
}

let singleton: Ref<EditorSettings> | null = null

/**
 * Reactive, localStorage-persisted editor settings shared across the app.
 * Returns the same ref on every client-side call.
 */
export function useEditorSettings(): Ref<EditorSettings> {
  // SSR / no browser: ephemeral defaults, never cached — never touches storage.
  if (typeof window === 'undefined') {
    return ref<EditorSettings>({ ...DEFAULT_EDITOR_SETTINGS })
  }

  if (!singleton) {
    const stored = useLocalStorage<EditorSettings>(
      EDITOR_SETTINGS_KEY,
      { ...DEFAULT_EDITOR_SETTINGS },
      {
        // A corrupt or partial blob must degrade to a valid object, not throw.
        serializer: {
          read: (raw: string): EditorSettings => {
            try {
              return normalizeEditorSettings(JSON.parse(raw))
            } catch {
              return { ...DEFAULT_EDITOR_SETTINGS }
            }
          },
          write: (value: EditorSettings): string => JSON.stringify(value),
        },
      },
    )
    // Self-heal: rewrite the normalized full object so any pre-existing partial
    // storage converges to the current schema.
    stored.value = normalizeEditorSettings(stored.value)
    singleton = stored
  }
  return singleton
}

/** Test-only: drop the cached singleton so a fresh localStorage state can be used. */
export function _resetEditorSettingsForTests(): void {
  singleton = null
}
