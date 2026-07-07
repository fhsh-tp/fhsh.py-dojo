import { describe, it, expect } from 'vitest'
import { EditorState, Compartment } from '@codemirror/state'
import { EditorView } from '@codemirror/view'
import { history, undo } from '@codemirror/commands'
import { fontSizeThemeSpec, FONT_SIZE_DEFAULT } from '../composables/editorConfig'

// Uses the REAL CodeMirror stack (not the mocked CodeEditor unit test) to verify
// how CodeEditor.vue's fontSize compartment behaves.
describe('editor font size (Requirement: Adjustable editor font size)', () => {
  it('fontSizeThemeSpec produces the exact CodeMirror theme shape', () => {
    expect(fontSizeThemeSpec(16)).toEqual({ '&': { fontSize: '16px' } })
    expect(fontSizeThemeSpec(FONT_SIZE_DEFAULT)).toEqual({ '&': { fontSize: '14px' } })
  })

  it('renders the configured font size onto the editor DOM and updates it live on reconfigure', () => {
    // The real proof that the theme WINS and reaches the DOM (design.md: "reconfigure
    // 後 DOM 反映新字級"): mount a real EditorView, read the resolved font size off the
    // editor root, reconfigure the fontSize compartment, and read it again.
    const parent = document.createElement('div')
    document.body.appendChild(parent)
    const c = new Compartment()
    const view = new EditorView({
      state: EditorState.create({
        doc: 'abc',
        extensions: [c.of(EditorView.theme(fontSizeThemeSpec(14)))],
      }),
      parent,
    })
    try {
      expect(getComputedStyle(view.dom).fontSize).toBe('14px')
      view.dispatch({ effects: c.reconfigure(EditorView.theme(fontSizeThemeSpec(20))) })
      expect(getComputedStyle(view.dom).fontSize).toBe('20px')
    } finally {
      view.destroy()
      parent.remove()
    }
  })

  it('preserves cursor and doc when the font size reconfigures (no rebuild)', () => {
    const c = new Compartment()
    let state = EditorState.create({
      doc: 'abcdef',
      selection: { anchor: 3 },
      extensions: [c.of(EditorView.theme(fontSizeThemeSpec(14)))],
    })

    state = state.update({ effects: c.reconfigure(EditorView.theme(fontSizeThemeSpec(20))) }).state

    expect(state.selection.main.anchor).toBe(3)
    expect(state.doc.toString()).toBe('abcdef')
  })

  it('preserves undo history across a font size reconfigure', () => {
    // Reconfiguring the fontSize compartment must not disturb the history() state:
    // an edit made before the reconfigure must still be undoable afterwards.
    const c = new Compartment()
    let state = EditorState.create({
      doc: '',
      extensions: [history(), c.of(EditorView.theme(fontSizeThemeSpec(14)))],
    })
    // an edit that history() records
    state = state.update({ changes: { from: 0, insert: 'hello' } }).state
    expect(state.doc.toString()).toBe('hello')

    // change the font size (compartment reconfigure only — no doc change)
    state = state.update({ effects: c.reconfigure(EditorView.theme(fontSizeThemeSpec(20))) }).state

    // undo still reverts the pre-reconfigure edit → history survived
    let undoneState: EditorState | null = null
    const applied = undo({
      state,
      dispatch: (tr) => {
        undoneState = tr.state
      },
    })
    expect(applied).toBe(true)
    expect(undoneState).not.toBeNull()
    expect((undoneState as unknown as EditorState).doc.toString()).toBe('')
  })
})
