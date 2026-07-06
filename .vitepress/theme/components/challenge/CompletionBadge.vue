<script setup lang="ts">
// Presentational-only completion badge. Kept prop-free and Pinia-free so it is
// trivially testable; the container decides whether to render it.
withDefaults(defineProps<{ label?: string }>(), { label: '已完成' })
</script>

<template>
  <span
    data-testid="completion-badge"
    class="inline-flex items-center gap-1 rounded-full bg-green-100 text-green-700 border border-green-200 px-1.5 py-0.5 text-xs font-medium shrink-0 dark:bg-green-900/60 dark:text-green-300 dark:border-green-800"
    :aria-label="label"
    :title="label"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="w-3 h-3 shrink-0"
      viewBox="0 0 20 20"
      fill="currentColor"
      aria-hidden="true"
    >
      <path
        fill-rule="evenodd"
        d="M16.704 5.29a1 1 0 010 1.42l-7.5 7.5a1 1 0 01-1.42 0l-3.5-3.5a1 1 0 111.42-1.42l2.79 2.79 6.79-6.79a1 1 0 011.42 0z"
        clip-rule="evenodd"
      />
    </svg>
    <span class="sr-only">{{ label }}</span>
  </span>
</template>
