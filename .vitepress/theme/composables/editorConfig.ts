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
