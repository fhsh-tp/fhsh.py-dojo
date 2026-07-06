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

export const EDITOR_SETTINGS_KEY = 'fhsh-py-dojo:editor-settings'
export const EDITOR_SETTINGS_SCHEMA_VERSION = 1

export interface EditorSettings {
  /** schema version, for forward-compatible migration of future fields. */
  version: number
  /** show the completion dropdown (and its "type hint" details) while typing. */
  autocomplete: boolean
  /** auto-insert the closing counterpart when typing ( [ {. */
  closeBrackets: boolean
}

export const DEFAULT_EDITOR_SETTINGS: EditorSettings = {
  version: EDITOR_SETTINGS_SCHEMA_VERSION,
  autocomplete: true,
  closeBrackets: true,
}

/**
 * Merge a stored (possibly partial, corrupt, or wrong-typed) value over the
 * defaults and coerce field types. Never throws — unknown input degrades to
 * defaults. This is the forward-compatible migration point: `version` is always
 * rewritten to the current schema version.
 */
export function normalizeEditorSettings(raw: unknown): EditorSettings {
  const obj = raw && typeof raw === 'object' ? (raw as Record<string, unknown>) : {}
  return {
    version: EDITOR_SETTINGS_SCHEMA_VERSION,
    autocomplete:
      typeof obj.autocomplete === 'boolean' ? obj.autocomplete : DEFAULT_EDITOR_SETTINGS.autocomplete,
    closeBrackets:
      typeof obj.closeBrackets === 'boolean' ? obj.closeBrackets : DEFAULT_EDITOR_SETTINGS.closeBrackets,
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
