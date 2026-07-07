import { describe, it, expect } from 'vitest'
import { EditorState, Prec } from '@codemirror/state'
import { closeBrackets, insertBracket } from '@codemirror/autocomplete'
import { python, pythonLanguage } from '@codemirror/lang-python'
import { AUTO_CLOSE_BRACKETS } from '../composables/editorConfig'

// Uses the REAL CodeMirror stack (not the mocked CodeEditor unit test) to verify
// actual bracket-closing behaviour — the exact composition CodeEditor.vue builds
// in its `buildCloseBrackets(true)` branch.
function buildState(doc = '') {
  return EditorState.create({
    doc,
    extensions: [
      python(),
      closeBrackets(),
      Prec.highest(pythonLanguage.data.of({ closeBrackets: { brackets: [...AUTO_CLOSE_BRACKETS] } })),
    ],
  })
}

describe('editor bracket auto-closing (Requirement: Bracket auto-closing)', () => {
  it('auto-closes ( into ()', () => {
    const tr = insertBracket(buildState(), '(')
    expect(tr).not.toBeNull()
    expect(tr!.state.doc.toString()).toBe('()')
  })

  it('auto-closes [ into []', () => {
    const tr = insertBracket(buildState(), '[')
    expect(tr).not.toBeNull()
    expect(tr!.state.doc.toString()).toBe('[]')
  })

  it('auto-closes { into {}', () => {
    const tr = insertBracket(buildState(), '{')
    expect(tr).not.toBeNull()
    expect(tr!.state.doc.toString()).toBe('{}')
  })

  it('does NOT auto-close a double quote (Scenario: Quotes are NOT auto-closed)', () => {
    // insertBracket returns null when the char is not a configured bracket,
    // so the editor inserts a bare " with no matching closer.
    expect(insertBracket(buildState(), '"')).toBeNull()
  })

  it('does NOT auto-close a single quote', () => {
    expect(insertBracket(buildState(), "'")).toBeNull()
  })
})
