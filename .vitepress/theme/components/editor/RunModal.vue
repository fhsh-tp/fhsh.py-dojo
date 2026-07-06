<script setup lang="ts">
import { ref, watch } from 'vue'
import { useExecutor } from '../../composables/useExecutor'

const props = defineProps<{
  code: string
  defaultStdin: string
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'run', payload: { stdin: string; stdout: string; error?: string }): void
}>()

const { execute } = useExecutor()

const stdin = ref(props.defaultStdin)
const stdout = ref('')
const error = ref<string | null>(null)
const isExecuting = ref(false)

// Reset stdin when defaultStdin changes (testcases become ready)
watch(() => props.defaultStdin, (val) => {
  stdin.value = val
})

// Reset output when modal opens
watch(() => props.isOpen, (open) => {
  if (open) {
    stdout.value = ''
    error.value = null
    stdin.value = props.defaultStdin
  }
})

async function handleExecute() {
  if (isExecuting.value) return
  isExecuting.value = true
  stdout.value = ''
  error.value = null

  const result = await execute(props.code, stdin.value)

  if (result.error) {
    error.value = result.error
  } else {
    stdout.value = result.stdout
  }
  isExecuting.value = false
  // Surface the run so the session recorder (in ChallengeView) can capture it.
  emit('run', { stdin: stdin.value, stdout: result.stdout, error: result.error })
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      data-testid="run-modal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="emit('close')"
    >
      <div class="bg-white dark:bg-gray-900 rounded-lg shadow-xl w-full max-w-xl mx-4 flex flex-col max-h-[80vh]">
        <!-- Header -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-slate-200 dark:border-gray-700">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">執行</h3>
          <button
            data-testid="close-btn"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors cursor-pointer"
            @click="emit('close')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <!-- Stdin -->
          <div>
            <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Input (stdin)</label>
            <textarea
              v-model="stdin"
              rows="4"
              class="w-full px-3 py-2 text-sm font-mono bg-slate-50 dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded resize-y text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              placeholder="輸入資料（可留空）"
            />
          </div>

          <!-- Output -->
          <div v-if="stdout || error">
            <label class="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Output</label>
            <pre
              v-if="stdout && !error"
              data-testid="output-area"
              class="w-full px-3 py-2 text-sm font-mono bg-slate-50 dark:bg-gray-800 border border-slate-200 dark:border-gray-700 rounded whitespace-pre-wrap break-words text-gray-900 dark:text-gray-100 max-h-48 overflow-y-auto"
            >{{ stdout }}</pre>
            <pre
              v-if="error"
              data-testid="error-area"
              class="w-full px-3 py-2 text-sm font-mono bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 rounded whitespace-pre-wrap break-words text-red-700 dark:text-red-400 max-h-48 overflow-y-auto"
            >{{ error }}</pre>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-4 py-3 border-t border-slate-200 dark:border-gray-700 flex justify-end">
          <button
            data-testid="execute-btn"
            :disabled="isExecuting"
            class="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-600/50 text-white rounded font-medium text-sm transition-colors cursor-pointer flex items-center gap-1.5"
            @click="handleExecute"
          >
            <svg
              v-if="isExecuting"
              class="w-4 h-4 shrink-0 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="w-4 h-4 shrink-0"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path fill-rule="evenodd" d="M4.5 5.653c0-1.427 1.529-2.33 2.779-1.643l11.54 6.347c1.295.712 1.295 2.573 0 3.286L7.28 19.99c-1.25.687-2.779-.217-2.779-1.643V5.653Z" clip-rule="evenodd" />
            </svg>
            {{ isExecuting ? '執行中...' : '執行' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
