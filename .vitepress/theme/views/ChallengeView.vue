<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useData, useRouter } from 'vitepress'
import { useChallengeStore } from '../stores/challenge'
import { useChallengeRunner, resolveVerdictDetail } from '../composables/useChallengeRunner'
import SplitPane from '../components/layout/SplitPane.vue'
import AppHeader from '../components/layout/AppHeader.vue'
import ProblemPanel from '../components/challenge/ProblemPanel.vue'
import CodeEditor from '../components/editor/CodeEditor.vue'
import RunButton from '../components/editor/RunButton.vue'
import RunModal from '../components/editor/RunModal.vue'
import TestResultPanel from '../components/editor/TestResultPanel.vue'
import { useExecutorStore } from '../stores/executor'

const { frontmatter, page } = useData()
const router = useRouter()
const challengeStore = useChallengeStore()
const executorStore = useExecutorStore()

const code = ref('')
const isRunModalOpen = ref(false)

// Build config from frontmatter
const verdictDetail = resolveVerdictDetail(frontmatter.value.verdict_detail)
const algorithm: string = frontmatter.value.algorithm ?? ''
const starterCode: string = frontmatter.value.starter_code ?? ''

// Derive per-challenge slug from the page path
// (`challenge/<slug>.md` → `<slug>`). This is the canonical key for fetching
// the encrypted pool and addressing the WASM session — independent of
// `algorithm`, which is shared across multiple challenges.
const slug = page.value.relativePath
  .replace(/^challenge\//, '')
  .replace(/\.md$/, '')

const runner = useChallengeRunner({
  id: slug,
  algorithm,
  params: frontmatter.value.params ?? {},
  generator: frontmatter.value.generator ?? '',
  testcaseCount: frontmatter.value.testcase_count ?? 5,
  starterCode,
  verdictDetail,
})

const defaultStdin = computed(() => {
  const challenge = challengeStore.currentChallenge
  return challenge?.testcases[0]?.input ?? ''
})

// ── Bottom panel resizable height ──────────────────────────────────────────
const MIN_BOTTOM_HEIGHT = 80
const DEFAULT_BOTTOM_HEIGHT = 224

const bottomHeight = ref(DEFAULT_BOTTOM_HEIGHT)
const rightContainerHeight = ref(0)
const rightContainerRef = ref<HTMLElement | null>(null)

const maxBottomHeight = computed(() =>
  Math.max(MIN_BOTTOM_HEIGHT, rightContainerHeight.value * 0.5),
)
const clampedBottomHeight = computed(() =>
  Math.min(maxBottomHeight.value, Math.max(MIN_BOTTOM_HEIGHT, bottomHeight.value)),
)

let ro: ResizeObserver | null = null
const dragging = ref(false)
let dragStartY = 0
let dragStartHeight = 0

function startDrag(e: MouseEvent) {
  dragging.value = true
  dragStartY = e.clientY
  dragStartHeight = clampedBottomHeight.value
  e.preventDefault()
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', stopDrag)
}

function onMouseMove(e: MouseEvent) {
  if (!dragging.value) return
  const delta = dragStartY - e.clientY
  bottomHeight.value = dragStartHeight + delta
}

function stopDrag() {
  dragging.value = false
  bottomHeight.value = clampedBottomHeight.value
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', stopDrag)
}

onMounted(() => {
  if (rightContainerRef.value) {
    ro = new ResizeObserver((entries) => {
      rightContainerHeight.value = entries[0]?.contentRect.height ?? 0
    })
    ro.observe(rightContainerRef.value)
  }

  // Key per-challenge result snapshots by slug, not algorithm — otherwise all
  // challenges sharing an `algorithm` value (e.g. all `nested-loop` challenges)
  // would share a single results bucket.
  executorStore.setActiveChallenge(slug)
  code.value = starterCode

  // Fire-and-forget: load testcases in background
  runner.loadTestcases()
})

onUnmounted(() => {
  runner.cleanup()
  ro?.disconnect()
  ro = null
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', stopDrag)
})

async function handleSubmit() {
  await runner.submit(code.value)
}
</script>

<template>
  <div class="h-screen flex flex-col bg-slate-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 overflow-hidden">
    <div v-if="runner.errorMessage.value" class="flex items-center justify-center h-full">
      <div class="text-center">
        <p class="text-xl text-red-500 dark:text-red-400 mb-4">{{ runner.errorMessage.value }}</p>
        <button class="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-gray-800 dark:hover:bg-gray-700 rounded" @click="router.go('/')">
          返回列表
        </button>
      </div>
    </div>

    <template v-else>
      <AppHeader
        :title="frontmatter.title ?? '載入中...'"
        :difficulty="frontmatter.difficulty ?? ''"
      />

      <div class="flex-1 overflow-hidden">
        <SplitPane>
          <template #left>
            <ProblemPanel />
          </template>

          <template #right>
            <div ref="rightContainerRef" class="flex flex-col h-full" :class="dragging ? 'select-none' : ''">
              <div class="flex-1 overflow-hidden">
                <CodeEditor v-model="code" />
              </div>
              <!-- Drag handle: between editor and bottom panel -->
              <div
                data-drag-handle
                class="h-1.5 shrink-0 cursor-row-resize bg-slate-200 hover:bg-blue-400/60 dark:bg-gray-800 dark:hover:bg-emerald-600/60 transition-colors"
                @mousedown="startDrag"
              />
              <!-- Bottom panel: button bar + results, height controlled by drag -->
              <div
                class="shrink-0 flex flex-col overflow-hidden"
                :style="{ height: `${clampedBottomHeight}px` }"
              >
                <div class="shrink-0 border-t border-slate-200 dark:border-gray-800 p-3 flex items-center gap-3">
                  <!-- Run button: always enabled, opens modal -->
                  <button
                    data-testid="run-btn"
                    class="px-4 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded font-medium text-sm transition-colors cursor-pointer flex items-center gap-1.5"
                    @click="isRunModalOpen = true"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.5 5.653c0-1.427 1.529-2.33 2.779-1.643l11.54 6.347c1.295.712 1.295 2.573 0 3.286L7.28 19.99c-1.25.687-2.779-.217-2.779-1.643V5.653Z" clip-rule="evenodd" />
                    </svg>
                    執行
                  </button>
                  <!-- Submit button: disabled until testcases ready -->
                  <RunButton
                    :is-running="runner.isRunning.value"
                    :is-ready="runner.isReady.value"
                    :progress="executorStore.results.length"
                    :total="executorStore.totalTestcases"
                    @run="handleSubmit"
                    @stop="runner.stop"
                  />
                  <span v-if="executorStore.status === 'done'" class="text-sm text-slate-500 dark:text-gray-400">
                    得分：{{ executorStore.passed }} / {{ executorStore.total }}
                  </span>
                </div>
                <TestResultPanel :results="executorStore.results" :status="executorStore.status" :verdict-detail="runner.verdictDetail.value" />
              </div>
            </div>
          </template>
        </SplitPane>
      </div>
    </template>

    <RunModal
      :code="code"
      :default-stdin="defaultStdin"
      :is-open="isRunModalOpen"
      @close="isRunModalOpen = false"
    />
  </div>
</template>
