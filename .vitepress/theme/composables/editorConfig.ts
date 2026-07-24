/**
 * Editor configuration shared between the live editor and its tests.
 *
 * `AUTO_CLOSE_BRACKETS` is the exact set of openers the editor auto-closes.
 * lang-python's default `closeBrackets` language data also includes the quote
 * characters (' " ''' """), but the editor-autocomplete spec requires
 * "Quotes are NOT auto-closed" — so we override the language data with just
 * these brackets (applied at highest precedence in CodeEditor.vue).
 */
export const AUTO_CLOSE_BRACKETS = ['(', '[', '{'] as const

/**
 * Bounds, default, and step (all px) for the editor `fontSize` setting.
 *
 * Single source of truth shared by three consumers so they can never drift:
 * `useEditorSettings.normalizeEditorSettings` clamps to [MIN, MAX], the
 * `EditorSettingsPopover` stepper increments by STEP and disables at the bounds,
 * and `CodeEditor.vue` seeds the initial font size. DEFAULT is 14 to match the
 * editor's pre-existing hard-coded appearance, so students who never change it
 * see no visual difference.
 */
export const FONT_SIZE_MIN = 10
export const FONT_SIZE_MAX = 24
export const FONT_SIZE_DEFAULT = 14
export const FONT_SIZE_STEP = 1

/**
 * The CodeMirror theme spec that applies a given editor font size.
 *
 * Kept as a plain object (no CodeMirror import) so it is trivially assertable in
 * tests and so this config module stays dependency-free; `CodeEditor.vue` wraps
 * it with the lazily-imported `EditorView.theme` inside the fontSize compartment.
 */
export function fontSizeThemeSpec(px: number): { '&': { fontSize: string } } {
  return { '&': { fontSize: `${px}px` } }
}
