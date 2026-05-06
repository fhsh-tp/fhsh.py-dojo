<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  graph: string
  id: string
}>()

const svgContent = ref('')
const errorMessage = ref('')
const renderKey = ref(0)
let pendingRender = false
let wasDark = false

async function renderDiagram() {
  if (pendingRender) return
  pendingRender = true
  try {
    const { default: mermaid } = await import('mermaid')
    const isDark = document.documentElement.classList.contains('dark')
    const theme = isDark ? 'dark' : 'default'
    // SECURITY: 'loose' skips DOMPurify sanitization of SVG output.
    // Safe only for developer-authored content checked into Git.
    // Change to 'strict' if rendering user-supplied mermaid diagrams.
    mermaid.initialize({ startOnLoad: false, securityLevel: 'loose', theme })
    const { svg } = await mermaid.render(props.id, decodeURIComponent(props.graph))
    svgContent.value = svg
    renderKey.value++
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : String(err)
  } finally {
    pendingRender = false
  }
}

let observer: MutationObserver | null = null

onMounted(() => {
  wasDark = document.documentElement.classList.contains('dark')
  renderDiagram()

  observer = new MutationObserver(() => {
    const isDark = document.documentElement.classList.contains('dark')
    if (isDark === wasDark) return
    wasDark = isDark
    errorMessage.value = ''
    renderDiagram()
  })
  observer.observe(document.documentElement, { attributeFilter: ['class'] })
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>

<template>
  <pre v-if="errorMessage">{{ errorMessage }}</pre>
  <div v-else :key="renderKey" v-html="svgContent" />
</template>
