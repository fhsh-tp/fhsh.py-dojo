import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useExecutorStore } from '../stores/executor'

describe('useExecutorStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('starts in idle state', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    expect(store.status).toBe('idle')
  })

  it('starts with empty results', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    expect(store.results).toEqual([])
  })

  it('setRunning transitions to running', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    store.setRunning(3)
    expect(store.status).toBe('running')
    expect(store.totalTestcases).toBe(3)
  })

  it('addResult appends a testcase result', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    store.setRunning(2)
    store.addResult({ type: 'testcase_result', index: 0, verdict: 'AC', expected: 'KHOOR', elapsed_ms: 12 })
    expect(store.results).toHaveLength(1)
    expect(store.results[0]?.verdict).toBe('AC')
  })

  it('setDone transitions to done', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    store.setRunning(1)
    store.setDone(1, 1)
    expect(store.status).toBe('done')
    expect(store.passed).toBe(1)
    expect(store.total).toBe(1)
  })

  it('reset clears all state back to idle', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    store.setRunning(2)
    store.addResult({ type: 'testcase_result', index: 0, verdict: 'WA', expected: 'X', elapsed_ms: 5 })
    store.reset()
    expect(store.status).toBe('idle')
    expect(store.results).toEqual([])
    expect(store.passed).toBe(0)
    expect(store.total).toBe(0)
  })

  it('passedCount is computed from results', () => {
    const store = useExecutorStore()
    store.setActiveChallenge('test')
    store.setRunning(3)
    store.addResult({ type: 'testcase_result', index: 0, verdict: 'AC', expected: 'A', elapsed_ms: 1 })
    store.addResult({ type: 'testcase_result', index: 1, verdict: 'WA', expected: 'B', elapsed_ms: 2 })
    store.addResult({ type: 'testcase_result', index: 2, verdict: 'AC', expected: 'C', elapsed_ms: 3 })
    expect(store.passedCount).toBe(2)
  })

  describe('isFullyJudged (real-submission signal)', () => {
    function seed(count: number, resultCount: number) {
      const store = useExecutorStore()
      store.setActiveChallenge('test')
      store.setRunning(count)
      for (let i = 0; i < resultCount; i++) {
        store.addResult({ type: 'testcase_result', index: i, verdict: 'AC', expected: 'X', elapsed_ms: 1 })
      }
      return store
    }

    it('is false while idle or running', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('test')
      expect(store.isFullyJudged).toBe(false) // idle
      store.setRunning(2)
      expect(store.isFullyJudged).toBe(false) // running
    })

    it('is true when done and every testcase produced a result', () => {
      const store = seed(2, 2)
      store.setDone(2, 2)
      expect(store.isFullyJudged).toBe(true)
    })

    it('is true for a genuine fully-judged failing submission (total results, some WA)', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('test')
      store.setRunning(2)
      store.addResult({ type: 'testcase_result', index: 0, verdict: 'AC', expected: 'X', elapsed_ms: 1 })
      store.addResult({ type: 'testcase_result', index: 1, verdict: 'WA', expected: 'Y', elapsed_ms: 1 })
      store.setDone(2, 1)
      expect(store.isFullyJudged).toBe(true)
    })

    it('is false for a prod-path abort: done, 0 results, passed 0 (Stop / crash / timeout)', () => {
      const store = seed(3, 0)
      store.setDone(3, 0) // useProdRunner does this on !outputs
      expect(store.isFullyJudged).toBe(false)
    })

    it('is false for a partial (timed-out mid-stream) judgment', () => {
      const store = seed(5, 3)
      store.setDone(5, 2)
      expect(store.isFullyJudged).toBe(false)
    })

    it('is false for a vacuous 0/0 done', () => {
      const store = seed(0, 0)
      store.setDone(0, 0)
      expect(store.isFullyJudged).toBe(false)
    })
  })

  describe('per-challenge execution state isolation', () => {
    it('shows idle state for a challenge that has not been run', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('challenge-a')
      expect(store.status).toBe('idle')
      expect(store.results).toEqual([])
    })

    it('switching to a new challenge shows empty state', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('challenge-a')
      store.setRunning(2)
      store.addResult({ type: 'testcase_result', index: 0, verdict: 'AC', expected: 'X', elapsed_ms: 5 })
      store.setDone(2, 1)

      store.setActiveChallenge('challenge-b')
      expect(store.status).toBe('idle')
      expect(store.results).toEqual([])
    })

    it('switching back to a challenge preserves its results', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('challenge-a')
      store.setRunning(1)
      store.addResult({ type: 'testcase_result', index: 0, verdict: 'AC', expected: 'X', elapsed_ms: 5 })
      store.setDone(1, 1)

      store.setActiveChallenge('challenge-b')
      store.setActiveChallenge('challenge-a')

      expect(store.status).toBe('done')
      expect(store.results).toHaveLength(1)
      expect(store.results[0]?.verdict).toBe('AC')
    })

    it('different challenges do not share results', () => {
      const store = useExecutorStore()
      store.setActiveChallenge('challenge-a')
      store.setRunning(1)
      store.addResult({ type: 'testcase_result', index: 0, verdict: 'WA', expected: 'X', elapsed_ms: 5 })

      store.setActiveChallenge('challenge-b')
      expect(store.results).toHaveLength(0)
    })
  })
})
