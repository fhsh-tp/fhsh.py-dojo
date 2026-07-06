<script setup lang="ts">
import { useRouter } from 'vitepress'
import type { Challenge } from '../../types.d/challenge.type.ts'
import CompletionBadge from './CompletionBadge.vue'

const props = defineProps<{ challenge: Challenge; completed?: boolean }>()
const router = useRouter()

const difficultyClass: Record<string, string> = {
  easy: 'bg-green-100 text-green-700 border-green-200 dark:bg-green-900/60 dark:text-green-300 dark:border-green-800',
  medium: 'bg-yellow-100 text-yellow-700 border-yellow-200 dark:bg-yellow-900/60 dark:text-yellow-300 dark:border-yellow-800',
  hard: 'bg-red-100 text-red-700 border-red-200 dark:bg-red-900/60 dark:text-red-300 dark:border-red-800',
  mystery: 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700',
}

const difficultyLabel: Record<string, string> = {
  easy: '簡單',
  medium: '中等',
  hard: '困難',
  mystery: '未知',
}
</script>

<template>
  <button
    class="text-left bg-white border border-blue-200 rounded-lg p-4 hover:border-blue-500 hover:shadow-[0_2px_12px_rgba(59,130,246,0.15)] dark:bg-gray-900 dark:border-gray-800 dark:hover:border-emerald-500 dark:hover:bg-gray-800/80 dark:hover:shadow-[0_0_14px_rgba(52,211,153,0.25)] transition-all duration-200 cursor-pointer"
    @click="router.go(props.challenge.url)"
  >
    <div class="flex items-start justify-between gap-2 mb-2">
      <h2 class="font-semibold text-gray-900 dark:text-gray-100 leading-tight">{{ props.challenge.title }}</h2>
      <div class="flex items-center gap-1.5 shrink-0">
      <CompletionBadge v-if="props.completed" />
      <span
        class="px-2 py-0.5 rounded border text-xs font-medium shrink-0"
        :class="difficultyClass[props.challenge.difficulty] ?? 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'"
      >
        {{ difficultyLabel[props.challenge.difficulty] ?? props.challenge.difficulty }}
      </span>
      </div>
    </div>
    <div class="flex flex-wrap gap-1 mt-2">
      <span
        v-for="tag in props.challenge.tags"
        :key="tag"
        class="px-1.5 py-0.5 bg-blue-50 text-blue-600 border border-blue-100 dark:bg-gray-800 dark:text-gray-400 dark:border-0 rounded text-xs"
      >
        {{ tag }}
      </span>
    </div>
  </button>
</template>
