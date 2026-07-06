import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as dbAdapter from '../persistence/db'
import type { ProgressRecord } from '../persistence/types'

/**
 * Reactive store for local student progress.
 *
 * SSR-safe: the setup body below MUST NOT touch IndexedDB. All persistence IO
 * lives in actions, and `init()` is only ever called from a component
 * `onMounted` hook (client-only). When IndexedDB is unavailable the store still
 * works in memory for the current session; nothing is durably stored.
 */
export const useProgressStore = defineStore('progress', () => {
  // --- no IndexedDB access here (SSR-safe) ---
  const records = ref<Record<string, ProgressRecord>>({})
  const initialised = ref(false)

  /** Load persisted progress into reactive state. Call from onMounted. */
  async function init(): Promise<void> {
    if (initialised.value) return
    const all = await dbAdapter.getAllProgress()
    const map: Record<string, ProgressRecord> = {}
    for (const r of all) map[r.slug] = r
    records.value = map
    initialised.value = true
  }

  function isCompleted(slug: string): boolean {
    return records.value[slug]?.status === 'completed'
  }

  /** Global completed count, independent of any UI filter. */
  const completedCount = computed(
    () => Object.values(records.value).filter((r) => r.status === 'completed').length,
  )

  /**
   * Record a judged submission outcome. Marks completed only when the run
   * fully passed (total > 0 and passed === total); once completed a challenge
   * never downgrades and `firstCompletedAt` is fixed. Best-effort persist.
   */
  async function recordSubmit(
    slug: string,
    passed: number,
    total: number,
    at: number,
  ): Promise<void> {
    const prev = records.value[slug]
    const nowCompleted = total > 0 && passed === total
    const completed = nowCompleted || prev?.status === 'completed'
    const rec: ProgressRecord = {
      slug,
      status: completed ? 'completed' : 'attempted',
      firstCompletedAt: prev?.firstCompletedAt ?? (nowCompleted ? at : undefined),
      lastAttemptAt: at,
      bestPassed: Math.max(prev?.bestPassed ?? 0, passed),
      total,
    }
    records.value = { ...records.value, [slug]: rec }
    await dbAdapter.upsertProgress(rec)
  }

  return {
    records,
    initialised,
    init,
    isCompleted,
    completedCount,
    recordSubmit,
  }
})
