<script setup lang="ts">
import { useRouter, useData } from 'vitepress'
import type { CategoryListUrl } from '../../../../docs/shared/challenge-category'

const props = withDefaults(
  defineProps<{
    title: string
    difficulty: string
    // Union of known catalogue pages — an arbitrary navigation target is
    // unrepresentable, so a future caller cannot inject one.
    backUrl?: CategoryListUrl
  }>(),
  { backUrl: '/challenges' },
)

const router = useRouter()
const { isDark } = useData()

function toggleDark() {
  isDark.value = !isDark.value
}

const difficultyClass: Record<string, string> = {
  easy: 'bg-green-200 text-green-800 dark:bg-green-700 dark:text-green-100',
  medium: 'bg-yellow-200 text-yellow-800 dark:bg-yellow-700 dark:text-yellow-100',
  hard: 'bg-red-200 text-red-800 dark:bg-red-700 dark:text-red-100',
  mystery: 'bg-gray-700 text-gray-100 dark:bg-gray-700 dark:text-gray-200',
}

const difficultyLabel: Record<string, string> = {
  easy: '簡單',
  medium: '中等',
  hard: '困難',
  mystery: '未知',
}
</script>

<template>
  <header
    class="flex items-center gap-3 border-b border-blue-800 px-4 py-3 shrink-0 bg-blue-900 dark:bg-transparent dark:border-gray-800"
  >
    <button
      class="text-blue-200 hover:text-white dark:text-gray-400 dark:hover:text-gray-200 text-sm transition-colors cursor-pointer"
      aria-label="返回列表"
      @click="router.go(props.backUrl)"
    >
      ← 返回
    </button>

    <span class="text-blue-700 dark:text-gray-600">|</span>

    <h1 class="font-semibold text-blue-50 dark:text-gray-100 truncate">{{ props.title }}</h1>

    <span
      v-if="props.difficulty"
      class="px-2 py-0.5 rounded text-xs font-medium shrink-0"
      :class="difficultyClass[props.difficulty] ?? 'bg-blue-700 text-blue-100 dark:bg-gray-700 dark:text-gray-200'"
    >
      {{ difficultyLabel[props.difficulty] ?? props.difficulty }}
    </span>

    <!-- Dark/light mode toggle -->
    <button
      data-testid="theme-toggle"
      class="ml-auto text-blue-200 hover:text-white dark:text-gray-400 dark:hover:text-gray-200 transition-colors cursor-pointer p-1 rounded"
      :aria-label="isDark ? '切換 light mode' : '切換 dark mode'"
      @click="toggleDark"
    >
      <!-- Sun icon: shown in dark mode to indicate "switch to light" -->
      <svg
        v-if="isDark"
        xmlns="http://www.w3.org/2000/svg"
        class="w-4 h-4"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <circle cx="12" cy="12" r="5" />
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
      </svg>
      <!-- Moon icon: shown in light mode to indicate "switch to dark" -->
      <svg
        v-else
        xmlns="http://www.w3.org/2000/svg"
        class="w-4 h-4"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
      </svg>
    </button>
  </header>
</template>
