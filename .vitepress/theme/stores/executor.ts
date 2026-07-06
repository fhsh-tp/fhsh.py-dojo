import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { TestcaseResult } from '../workers/pyodide.worker'

export type ExecutorStatus = 'idle' | 'running' | 'done'

type ExecutionSnapshot = {
  status: ExecutorStatus
  results: TestcaseResult[]
  totalTestcases: number
  passed: number
  total: number
}

const emptySnapshot = (): ExecutionSnapshot => ({
  status: 'idle',
  results: [],
  totalTestcases: 0,
  passed: 0,
  total: 0,
})

export const useExecutorStore = defineStore('executor', () => {
  const snapshots = ref<Record<string, ExecutionSnapshot>>({})
  const activeChallengeId = ref<string | null>(null)

  function setActiveChallenge(id: string) {
    activeChallengeId.value = id
    if (!snapshots.value[id]) {
      snapshots.value[id] = emptySnapshot()
    }
  }

  const _current = computed<ExecutionSnapshot>(() =>
    activeChallengeId.value
      ? (snapshots.value[activeChallengeId.value] ?? emptySnapshot())
      : emptySnapshot(),
  )

  const status = computed(() => _current.value.status)
  const results = computed(() => _current.value.results)
  const totalTestcases = computed(() => _current.value.totalTestcases)
  const passed = computed(() => _current.value.passed)
  const total = computed(() => _current.value.total)
  const passedCount = computed(() => _current.value.results.filter((r) => r.verdict === 'AC').length)

  /**
   * True only when the active challenge finished a *complete* judgment: status
   * `done` AND every testcase produced a result (`results.length === total`).
   *
   * This is the authoritative "this was a real submission" signal, independent
   * of dev/prod strategy. An aborted (Stop), crashed (worker error), or
   * timed-out (wall-clock kill) submission also reaches `status === 'done'` but
   * with `passed = 0` and `results` shorter than `total` (empty in prod), so it
   * is correctly excluded — preventing a phantom 0/N "submission" from being
   * recorded into progress or the downloadable session timeline.
   */
  const isFullyJudged = computed(
    () =>
      _current.value.status === 'done' &&
      _current.value.total > 0 &&
      _current.value.results.length === _current.value.total,
  )

  function setRunning(count: number) {
    const id = activeChallengeId.value
    if (!id) return
    snapshots.value[id] = {
      status: 'running',
      results: [],
      totalTestcases: count,
      passed: 0,
      total: 0,
    }
  }

  function addResult(result: TestcaseResult) {
    const id = activeChallengeId.value
    if (!id) return
    snapshots.value[id]?.results.push(result)
  }

  function setDone(totalCount: number, passedCount: number) {
    const id = activeChallengeId.value
    const snap = id ? snapshots.value[id] : undefined
    if (snap) {
      snap.status = 'done'
      snap.total = totalCount
      snap.passed = passedCount
    }
  }

  function reset() {
    const id = activeChallengeId.value
    if (id) {
      snapshots.value[id] = emptySnapshot()
    }
  }

  return {
    status,
    results,
    totalTestcases,
    passed,
    total,
    passedCount,
    isFullyJudged,
    setActiveChallenge,
    setRunning,
    addResult,
    setDone,
    reset,
  }
})
