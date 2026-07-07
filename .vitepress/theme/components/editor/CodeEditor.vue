<script setup lang="ts">
/**
 * CodeEditor — wraps CodeMirror 6.
 *
 * Uses a div container for CodeMirror and syncs its value with a v-model.
 * CodeMirror is loaded lazily to avoid blocking the initial render; a grey
 * skeleton rectangle is shown while the import resolves.
 *
 * Toggleable behaviours (autocomplete, bracket auto-close) are wrapped in
 * CodeMirror Compartments and driven by `useEditorSettings`. Changing a setting
 * reconfigures the running editor in place — no rebuild, so cursor position and
 * undo history are preserved.
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { EditorView } from '@codemirror/view'
import type { Compartment, Extension } from '@codemirror/state'
import { pythonStdlibCompletions } from '../../composables/pythonCompletions'
import { useEditorSettings } from '../../composables/useEditorSettings'
import { AUTO_CLOSE_BRACKETS, fontSizeThemeSpec } from '../../composables/editorConfig'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const settings = useEditorSettings()

const containerRef = ref<HTMLElement | null>(null)
const isLoading = ref(true)
let editor: EditorView | null = null
let resizeObserver: ResizeObserver | null = null

// Set once CodeMirror has lazy-loaded; referenced by the settings watcher below.
let acCompartment: Compartment | null = null
let bracketCompartment: Compartment | null = null
let fontSizeCompartment: Compartment | null = null
let buildAutocomplete: ((on: boolean) => Extension) | null = null
let buildCloseBrackets: ((on: boolean) => Extension) | null = null
let buildFontSize: ((px: number) => Extension) | null = null

onMounted(async () => {
  if (!containerRef.value) return

  // Lazy-load CodeMirror to avoid bundle bloat in the initial chunk
  const [
    { EditorView, keymap, lineNumbers, drawSelection, dropCursor, rectangularSelection },
    { defaultKeymap, history, historyKeymap, indentWithTab },
    { python, pythonLanguage },
    { oneDark },
    { EditorState, Compartment, Prec },
    { autocompletion, closeBrackets, closeBracketsKeymap },
  ] = await Promise.all([
    import('@codemirror/view'),
    import('@codemirror/commands'),
    import('@codemirror/lang-python'),
    import('@codemirror/theme-one-dark'),
    import('@codemirror/state'),
    import('@codemirror/autocomplete'),
  ])

  // Re-check after the async import: the component may have unmounted.
  if (!containerRef.value) return

  // Compartments make the toggleable extensions reconfigurable in place.
  acCompartment = new Compartment()
  bracketCompartment = new Compartment()
  fontSizeCompartment = new Compartment()
  // Font size lives in its own theme so it can be reconfigured live (no rebuild),
  // keeping cursor position and undo history intact — like the toggles above.
  buildFontSize = (px: number): Extension => EditorView.theme(fontSizeThemeSpec(px))

  // "autocomplete on" registers both the completion UI and the stdlib source;
  // "off" contributes nothing, so no dropdown can appear on any keystroke.
  buildAutocomplete = (on: boolean): Extension =>
    on
      ? [autocompletion(), pythonLanguage.data.of({ autocomplete: pythonStdlibCompletions() })]
      : []
  // Override lang-python's closeBrackets language data (which includes quotes)
  // so only real brackets auto-close — quotes must NOT (editor-autocomplete spec).
  // Prec.highest guarantees this config wins over the language's default.
  buildCloseBrackets = (on: boolean): Extension =>
    on
      ? [
          closeBrackets(),
          Prec.highest(
            pythonLanguage.data.of({ closeBrackets: { brackets: [...AUTO_CLOSE_BRACKETS] } }),
          ),
        ]
      : []

  editor = new EditorView({
    state: EditorState.create({
      doc: props.modelValue,
      extensions: [
        lineNumbers(),
        history(),
        drawSelection(),
        dropCursor(),
        rectangularSelection(),
        EditorState.tabSize.of(4),
        python(),
        acCompartment.of(buildAutocomplete(settings.value.autocomplete)),
        bracketCompartment.of(buildCloseBrackets(settings.value.closeBrackets)),
        fontSizeCompartment.of(buildFontSize(settings.value.fontSize)),
        keymap.of([...closeBracketsKeymap, indentWithTab, ...defaultKeymap, ...historyKeymap]),
        oneDark,
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            emit('update:modelValue', update.state.doc.toString())
          }
        }),
        EditorView.theme({
          '&': { height: '100%' },
          '.cm-scroller': { overflow: 'auto', fontFamily: 'monospace' },
        }),
      ],
    }),
    parent: containerRef.value,
  })

  // ResizeObserver replaces Monaco's automaticLayout
  resizeObserver = new ResizeObserver(() => {
    editor?.requestMeasure()
  })
  resizeObserver.observe(containerRef.value)

  isLoading.value = false
})

// Live-apply setting changes by reconfiguring the compartments — never rebuild
// the editor, so cursor position and undo history survive the toggle. Declared
// at setup scope (not inside the async onMounted) so it disposes with the
// component; it no-ops until the editor and compartments exist.
watch(
  () =>
    [settings.value.autocomplete, settings.value.closeBrackets, settings.value.fontSize] as const,
  ([ac, cb, fs]) => {
    if (
      !editor ||
      !acCompartment ||
      !bracketCompartment ||
      !fontSizeCompartment ||
      !buildAutocomplete ||
      !buildCloseBrackets ||
      !buildFontSize
    )
      return
    editor.dispatch({
      effects: [
        acCompartment.reconfigure(buildAutocomplete(ac)),
        bracketCompartment.reconfigure(buildCloseBrackets(cb)),
        fontSizeCompartment.reconfigure(buildFontSize(fs)),
      ],
    })
  },
)

// Sync external model changes (e.g., when starter code is loaded)
watch(
  () => props.modelValue,
  (newVal) => {
    if (!editor) return
    const current = editor.state.doc.toString()
    if (current !== newVal) {
      editor.dispatch({
        changes: { from: 0, to: current.length, insert: newVal },
      })
    }
  },
)

onUnmounted(() => {
  resizeObserver?.disconnect()
  editor?.destroy()
})
</script>

<template>
  <div class="h-full w-full relative">
    <!-- Skeleton overlay while CodeMirror lazy-imports; container must always exist in DOM -->
    <div v-if="isLoading" class="absolute inset-0 bg-gray-800 animate-pulse rounded z-10" />
    <div ref="containerRef" class="h-full w-full" />
  </div>
</template>
