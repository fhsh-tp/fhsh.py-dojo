<script setup lang="ts">
import { computed } from 'vue'
import { data as challenges } from '../../../../docs/shared/challenge.data'

const props = defineProps<{ slug: string }>()

const challenge = computed(() =>
  challenges.find(c => c.url.replace(/\.html$/, '') === `/challenge/${props.slug}`)
)

const difficultyLabel: Record<string, string> = {
  easy: '基礎',
  medium: '進階',
  hard: '挑戰',
  mystery: '未知',
}

const difficultyClass: Record<string, string> = {
  easy: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300',
  medium: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300',
  hard: 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300',
  mystery: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300',
}
</script>

<template>
  <div class="challenge-link my-4">
    <!-- Known challenge -->
    <a
      v-if="challenge"
      :href="challenge.url"
      target="_blank"
      class="challenge-link__card"
    >
      <span class="challenge-link__icon">⚔️</span>
      <span class="challenge-link__title">{{ challenge.title }}</span>
      <span
        class="challenge-link__badge"
        :class="difficultyClass[challenge.difficulty] ?? 'bg-gray-100 text-gray-600'"
      >
        {{ difficultyLabel[challenge.difficulty] ?? challenge.difficulty }}
      </span>
      <span class="challenge-link__arrow">→</span>
    </a>

    <!-- Unknown slug fallback -->
    <div v-else class="challenge-link__placeholder">
      <span class="challenge-link__icon">⚔️</span>
      <span class="challenge-link__title">挑戰題目尚未建立</span>
    </div>
  </div>
</template>

<style scoped>
.challenge-link__card {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  background: var(--vp-c-bg-soft);
  transition: border-color 0.2s, background 0.2s;
}

.challenge-link__card:hover {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg-elv);
}

.challenge-link__placeholder {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 8px;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg-soft);
}

.challenge-link__title {
  flex: 1;
  font-weight: 500;
}

.challenge-link__badge {
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.challenge-link__arrow {
  color: var(--vp-c-text-3);
}
</style>
