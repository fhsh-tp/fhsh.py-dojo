<script setup lang="ts">
import { computed } from 'vue'
import type { TestcaseResult, VerdictDetail } from '../../workers/pyodide.worker'
import type { ExecutorStatus } from '../../stores/executor'

const props = withDefaults(defineProps<{
  results: TestcaseResult[]
  status: ExecutorStatus
  verdictDetail?: VerdictDetail
  /**
   * Testcases the challenge actually has. When the cumulative batch limit
   * terminates a run, the Worker dies mid-batch and the testcases after it
   * never report — scoring or rendering against `results.length` then shows a
   * truncated run as a full pass. Defaults to the reported count so callers
   * that genuinely have no total keep the old behaviour.
   */
  total?: number
}>(), {
  verdictDetail: 'hidden',
  total: 0,
})

const verdictStyle: Record<string, string> = {
  AC: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
  WA: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/30',
  TLE: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30',
  RE: 'text-orange-600 bg-orange-100 dark:text-orange-400 dark:bg-orange-900/30',
}

const passedCount = computed(() => props.results.filter((r) => r.verdict === 'AC').length)

/** Denominator for both the score and the row count. */
const totalCount = computed(() => (props.total > 0 ? props.total : props.results.length))

/**
 * One entry per testcase of the challenge. Indices the run never reached are
 * `null`, and render as an explicit not-executed row rather than vanishing.
 */
const rows = computed<Array<TestcaseResult | null>>(() => {
  const byIndex = new Map(props.results.map((r) => [r.index, r]))
  return Array.from({ length: totalCount.value }, (_, i) => byIndex.get(i) ?? null)
})

const allPassed = computed(() => passedCount.value === totalCount.value)
</script>

<template>
  <div
    v-if="props.results.length > 0 || props.status === 'running' || (props.status === 'done' && totalCount > 0)"
    data-testid="result-panel"
    class="border-t border-slate-200 dark:border-gray-800 flex-1 overflow-auto"
  >
    <!-- Score summary when done -->
    <div
      v-if="props.status === 'done'"
      data-testid="result-summary"
      class="px-4 py-2 bg-slate-50 dark:bg-gray-900 border-b border-slate-200 dark:border-gray-800 text-sm"
      :class="allPassed ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'"
    >
      <span class="text-slate-500 dark:text-gray-400">結果：</span>
      <span>{{ passedCount }} / {{ totalCount }} 通過</span>
    </div>

    <!-- Per-testcase rows -->
    <table class="w-full text-xs">
      <thead>
        <tr class="text-slate-400 dark:text-gray-500 border-b border-slate-200 dark:border-gray-800">
          <th class="text-left px-4 py-1.5 font-normal w-12">#</th>
          <th class="text-left px-2 py-1.5 font-normal w-20">結果</th>
          <th class="text-left px-2 py-1.5 font-normal w-20">時間</th>
          <th class="text-left px-2 py-1.5 font-normal">詳細</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(result, rowIndex) in rows"
          :key="rowIndex"
          :data-verdict="result?.verdict ?? 'none'"
          class="border-b border-slate-100 dark:border-gray-800/50"
        >
          <td class="px-4 py-1.5 text-slate-400 dark:text-gray-500">{{ rowIndex + 1 }}</td>
          <td class="px-2 py-1.5">
            <!-- Never reached: the run was cut short before this testcase. -->
            <span v-if="result === null" class="flex items-center gap-1 text-slate-400 dark:text-gray-600">
              <span class="px-1.5 py-0.5 rounded font-bold bg-slate-100 dark:bg-gray-800">未執行</span>
            </span>
            <span v-else class="flex items-center gap-1">
              <!-- AC: checkmark -->
              <svg
                v-if="result.verdict === 'AC'"
                xmlns="http://www.w3.org/2000/svg"
                class="w-3.5 h-3.5 text-green-500 dark:text-green-400 shrink-0"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              <!-- WA / RE / TLE: x-mark -->
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="w-3.5 h-3.5 shrink-0"
                :class="{
                  'text-red-500 dark:text-red-400': result.verdict === 'WA' || result.verdict === 'RE',
                  'text-yellow-500 dark:text-yellow-400': result.verdict === 'TLE',
                }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span
                class="px-1.5 py-0.5 rounded font-bold"
                :class="verdictStyle[result.verdict] ?? 'text-slate-500 dark:text-gray-400'"
              >
                {{ result.verdict }}
              </span>
            </span>
          </td>
          <td class="px-2 py-1.5 text-slate-400 dark:text-gray-500">
            {{ result === null ? '—' : `${result.elapsed_ms.toFixed(0)} ms` }}
          </td>
          <td class="px-2 py-1.5 text-slate-500 dark:text-gray-400 font-mono truncate max-w-xs">
            <template v-if="result === null" />
            <template v-else-if="result.verdict === 'WA' && props.verdictDetail === 'full'">
              預期 <span class="text-green-600 dark:text-green-400">{{ result.expected }}</span>，
              實際 <span class="text-red-500 dark:text-red-400">{{ result.actual }}</span>
            </template>
            <template v-else-if="result.verdict === 'WA' && props.verdictDetail === 'actual'">
              實際 <span class="text-red-500 dark:text-red-400">{{ result.actual }}</span>
            </template>
            <template v-else-if="result.verdict === 'RE'">
              {{ result.error }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
