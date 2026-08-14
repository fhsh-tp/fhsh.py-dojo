<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useData, useRouter } from 'vitepress'
import { useChallengeStore } from '../stores/challenge'
import { useChallengeRunner, resolveVerdictDetail } from '../composables/useChallengeRunner'
import { useSessionRecorder, resolveDebounceMs, type SessionRecorder } from '../composables/useSessionRecorder'
import SplitPane from '../components/layout/SplitPane.vue'
import AppHeader from '../components/layout/AppHeader.vue'
import ProblemPanel from '../components/challenge/ProblemPanel.vue'
import CodeEditor from '../components/editor/CodeEditor.vue'
import RunButton from '../components/editor/RunButton.vue'
import RunModal from '../components/editor/RunModal.vue'
import TestResultPanel from '../components/editor/TestResultPanel.vue'
import DownloadRecordButton from '../components/editor/DownloadRecordButton.vue'
import EditorSettingsPopover from '../components/editor/EditorSettingsPopover.vue'
import { useExecutorStore } from '../stores/executor'
import { useProgressStore } from '../stores/progress'
import { allowedResult } from '../lib/progressExport'
import { deriveChallengeSlug } from '../../../docs/shared/challenge-slug'
import { CATEGORY_LIST_URL, resolveChallengeCategory } from '../../../docs/shared/challenge-category'
import { CHALLENGE_ID_PATTERN } from '../../../docs/shared/challenge-id'

const { frontmatter, page } = useData()
const router = useRouter()
const challengeStore = useChallengeStore()
const executorStore = useExecutorStore()
const progressStore = useProgressStore()

const code = ref('')
const isRunModalOpen = ref(false)
// Work-session recorder — created client-only in onMounted, torn down on unmount.
let recorder: SessionRecorder | null = null

// Build config from frontmatter
const verdictDetail = resolveVerdictDetail(frontmatter.value.verdict_detail)
const algorithm: string = frontmatter.value.algorithm ?? ''
const starterCode: string = frontmatter.value.starter_code ?? ''
// Sanitize-to-'' on a malformed id (same convention as challenge.data.ts):
// the header badge hides itself rather than exposing a bad value.
const challengeId = ((raw: string) => (CHALLENGE_ID_PATTERN.test(raw) ? raw : ''))(
  String(frontmatter.value.id ?? ''),
)

// Category-aware return target, derived from the exhaustive category → page
// map: absent or unknown categories resolve to python and land on /challenges.
const listUrl = CATEGORY_LIST_URL[resolveChallengeCategory(frontmatter.value.category)]

// Derive the per-challenge slug from the page path via the single shared parser
// (the same one the catalogue uses on `challenge.url`), so the slug ChallengeView
// writes progress under can never diverge from the slug the list page reads it
// back under. This is the canonical key for fetching the encrypted pool and
// addressing the WASM session — independent of `algorithm`, which is shared
// across multiple challenges.
const slug = deriveChallengeSlug(`/${page.value.relativePath}`)

const runner = useChallengeRunner({
  id: slug,
  algorithm,
  params: frontmatter.value.params ?? {},
  generator: frontmatter.value.generator ?? '',
  testcaseCount: frontmatter.value.testcase_count ?? 5,
  starterCode,
  verdictDetail,
  // testcase_plan challenges: the runner derives the effective count from the
  // plan itself (testcase_count is mutually exclusive with a plan).
  testcasePlan: frontmatter.value.testcase_plan,
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

  // Client-only: load persisted progress and start the work-session recorder
  // (both open IndexedDB lazily and never run during SSR).
  progressStore.init()
  recorder = useSessionRecorder({
    slug,
    code,
    debounceMs: resolveDebounceMs(frontmatter.value.editor_capture_debounce_ms),
    // Getter, not a fixed value: the pool's own verdict_detail (the source of
    // truth) is only known after the pool loads, later than this mount.
    verdictDetail: () => runner.verdictDetail.value,
  })

  // Fire-and-forget: load testcases in background
  runner.loadTestcases()
})

onUnmounted(() => {
  runner.cleanup()
  recorder?.stop()
  recorder = null
  ro?.disconnect()
  ro = null
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', stopDrag)
})

async function handleSubmit() {
  await runner.submit(code.value)
  // Only a *complete* judgment is recorded. An aborted (Stop), crashed, or
  // timed-out submission also reaches status 'done' but with fewer results than
  // total (empty in prod) — recording it would write a phantom 0/N submission
  // into progress and the downloadable timeline. `isFullyJudged` excludes those.
  if (!executorStore.isFullyJudged) return
  const at = Date.now()
  await progressStore.recordSubmit(slug, executorStore.passed, executorStore.total, at)
  // Record the submit event on the session timeline. Results are re-filtered at
  // store time by the pool's own verdict_detail (the source of truth), so answer
  // keys can never be persisted even if an upstream layer regressed.
  const detail = runner.verdictDetail.value
  recorder?.recordSubmit(
    code.value,
    { passed: executorStore.passed, total: executorStore.total },
    executorStore.results.map((r) =>
      allowedResult(
        {
          index: r.index,
          verdict: r.verdict,
          elapsed_ms: r.elapsed_ms,
          error: r.error,
          actual: r.actual,
          expected: r.expected,
        },
        detail,
      ),
    ),
  )
}

function onRun(payload: { stdin: string; stdout: string; error?: string }) {
  recorder?.recordRun(payload.stdin, payload.stdout, payload.error)
}
</script>

<template>
  <div class="h-screen flex flex-col bg-slate-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 overflow-hidden">
    <div v-if="runner.errorMessage.value" class="flex items-center justify-center h-full">
      <div class="text-center">
        <p class="text-xl text-red-500 dark:text-red-400 mb-4">{{ runner.errorMessage.value }}</p>
        <button class="px-4 py-2 bg-slate-200 hover:bg-slate-300 dark:bg-gray-800 dark:hover:bg-gray-700 rounded" @click="router.go(listUrl)">
          返回列表
        </button>
      </div>
    </div>

    <template v-else>
      <AppHeader
        :title="frontmatter.title ?? '載入中...'"
        :difficulty="frontmatter.difficulty ?? ''"
        :id="challengeId"
        :back-url="listUrl"
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
                  <DownloadRecordButton
                    class="ml-auto"
                    :slug="slug"
                    :title="frontmatter.title ?? slug"
                    :difficulty="frontmatter.difficulty"
                  />
                  <!-- Gear ⚙ opens the editor-settings popover (opens upward from the action bar) -->
                  <EditorSettingsPopover />
                </div>
                <TestResultPanel :results="executorStore.results" :status="executorStore.status" :total="executorStore.totalTestcases" :verdict-detail="runner.verdictDetail.value" />
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
      @run="onRun"
    />
  </div>
</template>
