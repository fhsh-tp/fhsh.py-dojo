<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Challenge } from '../types.d/challenge.type.ts'
import ChallengeCard from '../components/challenge/ChallengeCard.vue'
import { useProgressStore } from '../stores/progress'
import { challengeIdOrdinal } from '../../../docs/shared/challenge-id'

const props = defineProps<{
  challenges: Challenge[]
}>()

// Client-only: load persisted progress after mount (never during SSR).
const progress = useProgressStore()
onMounted(() => {
  progress.init()
})

type Difficulty = 'all' | 'easy' | 'medium' | 'hard'
const selectedDifficulty = ref<Difficulty>('all')
const searchQuery = ref('')

const filtered = computed(() => {
  let result = props.challenges

  if (selectedDifficulty.value !== 'all') {
    result = result.filter((c) => c.difficulty === selectedDifficulty.value)
  }

  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    // Ordinal-aware id rule: a pure-digit query matches the id's ordinal
    // exactly (3/03/003 all hit ordinal 3); anything else prefix-matches the
    // id string. Combined with the text fields below via OR.
    const idMatches = /^\d+$/.test(q)
      ? (c: Challenge) => challengeIdOrdinal(c.id) === parseInt(q, 10)
      : (c: Challenge) => c.id.startsWith(q)
    result = result.filter((c) =>
      c.title.toLowerCase().includes(q)
      || c.description.toLowerCase().includes(q)
      || c.tags.some(t => t.toLowerCase().includes(q))
      || c.chapter.toLowerCase().includes(q)
      || idMatches(c)
    )
  }

  return result
})

// Page-scoped, so a challenge only ever counts toward the catalogue page it
// belongs to. Never use the store-wide `completedCount` getter as a page
// numerator — pairing it with a page-scoped denominator misreports (12 / 4).
const completedInPage = computed(
  () => props.challenges.filter((c) => progress.isCompleted(c.slug)).length,
)

const difficulties: Difficulty[] = ['all', 'easy', 'medium', 'hard']
const difficultyLabel: Record<Difficulty, string> = {
  all: '全部',
  easy: '簡單',
  medium: '中等',
  hard: '困難',
}

const SKELETON_COUNT = 6
</script>

<template>
  <div class="w-full my-10 vp-raw">
    <main class="px-6 py-6 max-w-7xl mx-auto">
      <!-- Search -->
      <input
        v-model="searchQuery"
        type="search"
        placeholder="搜尋題目名稱、編號、說明、標籤、章節..."
        class="w-full mb-4 px-4 py-2 rounded-lg border border-blue-200 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-900 dark:border-gray-700 dark:text-gray-100 dark:placeholder-gray-500 dark:focus:ring-emerald-500 transition-colors"
        maxlength="100"
        aria-label="搜尋挑戰題目"
      />

      <!-- Difficulty filter -->
      <div class="flex gap-2 mb-6" role="toolbar" aria-label="難度篩選">
        <button
          v-for="d in difficulties"
          :key="d"
          class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors"
          :class="
            selectedDifficulty === d
              ? 'bg-blue-600 text-white dark:bg-emerald-500 dark:text-white dark:shadow-[0_0_10px_rgba(16,185,129,0.4)]'
              : 'bg-blue-50 text-blue-600 border border-blue-200 hover:bg-blue-100 dark:bg-gray-800 dark:text-gray-300 dark:border-0 dark:hover:bg-gray-700'
          "
          @click="selectedDifficulty = d"
        >
          {{ difficultyLabel[d] }}
        </button>
      </div>

      <!-- Page-scoped completed count (independent of the active filter) -->
      <p
        data-testid="completed-count"
        class="text-sm text-slate-500 dark:text-gray-400 mb-4"
      >
        已完成 {{ completedInPage }} / {{ props.challenges.length }}
      </p>

      <!-- Challenge grid -->
      <div
        v-if="filtered.length > 0"
        class="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
      >
        <ChallengeCard
          v-for="challenge in filtered"
          :key="challenge.slug"
          :challenge="challenge"
          :completed="progress.isCompleted(challenge.slug)"
        />
      </div>

      <p v-else class="text-slate-400 dark:text-gray-500 text-center py-16">沒有符合條件的挑戰。</p>
    </main>
  </div>
</template>
