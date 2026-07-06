<script setup lang="ts">
import { ref } from 'vue'
import * as db from '../../persistence/db'
import { buildMarkdown, buildJson, buildFilename, type ExportInput } from '../../lib/progressExport'
import { downloadTextFile } from '../../lib/download'

const props = defineProps<{
  slug: string
  title: string
  difficulty?: string
}>()

const open = ref(false)
const name = ref('')
const cls = ref('')
const full = ref(false)
const busy = ref(false)

async function download(format: 'md' | 'json') {
  if (busy.value) return
  busy.value = true
  try {
    const sessions = await db.listSessions(props.slug)
    const input: ExportInput = {
      slug: props.slug,
      title: props.title,
      difficulty: props.difficulty,
      sessions,
      identity: { name: name.value.trim() || undefined, class: cls.value.trim() || undefined },
      mode: full.value ? 'full' : 'thinned',
    }
    const content = format === 'md' ? buildMarkdown(input) : buildJson(input)
    const mime = format === 'md' ? 'text/markdown' : 'application/json'
    downloadTextFile(buildFilename(input, format), content, mime)
    open.value = false
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="relative">
    <button
      data-testid="download-record-btn"
      aria-label="下載作答紀錄"
      class="px-3 py-1.5 text-sm rounded font-medium border border-slate-300 text-slate-600 hover:bg-slate-100 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800 transition-colors cursor-pointer"
      @click="open = !open"
    >
      下載紀錄
    </button>

    <div
      v-if="open"
      data-testid="download-panel"
      class="absolute right-0 z-40 mt-2 w-64 rounded-lg border border-slate-200 bg-white p-3 shadow-lg dark:border-gray-700 dark:bg-gray-900"
    >
      <label class="block text-xs text-slate-500 dark:text-gray-400 mb-1">姓名（選填）</label>
      <input
        v-model="name"
        type="text"
        maxlength="40"
        class="w-full mb-2 px-2 py-1 text-sm rounded border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      />
      <label class="block text-xs text-slate-500 dark:text-gray-400 mb-1">班級（選填）</label>
      <input
        v-model="cls"
        type="text"
        maxlength="40"
        class="w-full mb-2 px-2 py-1 text-sm rounded border border-slate-200 dark:border-gray-700 bg-slate-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      />
      <label class="flex items-center gap-2 text-xs text-slate-600 dark:text-gray-300 mb-3">
        <input v-model="full" type="checkbox" />
        完整版（含所有編輯快照，預設為瘦身版）
      </label>
      <div class="flex gap-2">
        <button
          data-testid="download-md"
          :disabled="busy"
          class="flex-1 px-2 py-1.5 text-sm rounded bg-sky-600 hover:bg-sky-500 text-white font-medium cursor-pointer disabled:opacity-50"
          @click="download('md')"
        >
          Markdown
        </button>
        <button
          data-testid="download-json"
          :disabled="busy"
          class="flex-1 px-2 py-1.5 text-sm rounded border border-slate-300 dark:border-gray-700 text-slate-600 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-gray-800 font-medium cursor-pointer disabled:opacity-50"
          @click="download('json')"
        >
          JSON
        </button>
      </div>
    </div>
  </div>
</template>
