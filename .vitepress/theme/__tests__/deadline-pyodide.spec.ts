// @vitest-environment node
/**
 * Real-Pyodide integration tests for the deadline interrupt.
 *
 * The unit tests around `DeadlineWatchdog` prove the main-thread half: that a
 * signal gets written at the right time, to the right slot, for the right
 * generation. They cannot prove the half that actually matters — that writing
 * that signal stops Python, that the exception is catchable by the handler
 * rather than escaping it, and that the runtime survives to judge the next
 * testcase. Those are properties of Pyodide, so they need Pyodide.
 *
 * This suite is why the change does not need to touch the operation counter:
 * it demonstrates that the two recorded counter bypasses (freezing the tracer,
 * diluting the count by flattening iterations onto one line) are both stopped
 * by a clock they cannot reach.
 *
 * Runs against `node_modules/pyodide`, the same build the site self-hosts.
 * Skips rather than fails when that package is absent, following the
 * preflight-skip pattern used by the other integration suites.
 */
import { Worker } from 'node:worker_threads'
import { createRequire } from 'node:module'
import { describe, it, expect, beforeAll, afterAll } from 'vitest'

import { INTERRUPT_SIGNAL, SLOT_SIGNAL, SLOT_GENERATION } from '../workers/deadline'

const require = createRequire(import.meta.url)

let pyodideAvailable = true
try {
  require.resolve('pyodide/pyodide.mjs')
} catch {
  pyodideAvailable = false
}

/** Short budget so the suite stays fast; the mechanism is scale-free. */
const BUDGET_MS = 800

/**
 * Watchdog thread. The main thread is blocked inside synchronous Python for
 * the whole of each trial — exactly as the judge Worker is — so the countdown
 * cannot live there.
 */
const WATCHDOG_SOURCE = `
const { parentPort, workerData } = require('node:worker_threads')
const view = new Uint8Array(workerData.sab)
parentPort.on('message', (m) => {
  setTimeout(() => {
    if (view[${SLOT_GENERATION}] === m.generation) view[${SLOT_SIGNAL}] = ${INTERRUPT_SIGNAL}
  }, m.budgetMs)
})
`

/**
 * A loop that far outlasts the budget but still terminates on its own.
 *
 * Sizing is a two-sided constraint. Too large and "the interrupt regressed"
 * stops being a fast red and becomes a hung suite. Too small and the test goes
 * flaky: when the whole suite runs in parallel the watchdog thread can be
 * starved for seconds, and at 30M iterations the loop was observed finishing
 * (4,473 ms) before a delayed interrupt landed. This size keeps the loop well
 * over ten seconds of work so a late interrupt still arrives first, while a
 * genuine regression fails in seconds rather than minutes.
 */
const RUNAWAY_ITERATIONS = 150_000_000
const RUNAWAY = `i = 0\nwhile i < ${RUNAWAY_ITERATIONS}: i += 1\n"COMPLETED"`

interface Trial {
  outcome: 'returned' | 'raised'
  value: string
  errorType: string | undefined
  elapsedMs: number
}

describe.skipIf(!pyodideAvailable)('deadline interrupt against real Pyodide', () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let pyodide: any
  let watchdog: Worker
  let view: Uint8Array
  let generation = 0

  beforeAll(async () => {
    const { loadPyodide } = await import('pyodide/pyodide.mjs')
    pyodide = await loadPyodide({ stdout: () => {}, stderr: () => {} })

    const sab = new SharedArrayBuffer(2)
    view = new Uint8Array(sab)
    pyodide.setInterruptBuffer(view)

    watchdog = new Worker(WATCHDOG_SOURCE, { eval: true, workerData: { sab } })
  }, 120_000)

  afterAll(async () => {
    await watchdog?.terminate()
  })

  /** Arm, run synchronously, disarm — the judge's exact sequence. */
  function trial(code: string, budgetMs = BUDGET_MS): Trial {
    generation = (generation + 1) & 0xff
    view[SLOT_SIGNAL] = 0
    view[SLOT_GENERATION] = generation
    watchdog.postMessage({ generation, budgetMs })

    const started = Date.now()
    try {
      const result = pyodide.runPython(code)
      return { outcome: 'returned', value: String(result), errorType: undefined, elapsedMs: Date.now() - started }
    } catch (err) {
      return {
        outcome: 'raised',
        value: '',
        errorType: (err as { type?: string }).type,
        elapsedMs: Date.now() - started,
      }
    } finally {
      view[SLOT_SIGNAL] = 0
      generation = (generation + 1) & 0xff
      view[SLOT_GENERATION] = generation
    }
  }

  it('lets code that finishes inside the budget return normally', () => {
    const r = trial('sum(range(1000))')
    expect(r.outcome).toBe('returned')
    expect(r.elapsedMs).toBeLessThan(BUDGET_MS)
  }, 30_000)

  it('stops a runaway loop at the deadline with an exception the caller can catch', () => {
    const r = trial(RUNAWAY)
    expect(r.outcome).toBe('raised')
    expect(r.errorType).toBe('KeyboardInterrupt')
    expect(r.elapsedMs).toBeGreaterThanOrEqual(BUDGET_MS)
    expect(r.elapsedMs).toBeLessThan(BUDGET_MS * 4)
  }, 30_000)

  it('stops code that froze the operation counter with sys.settrace(None)', () => {
    // The counter records 5 operations for this submission for the whole run;
    // the op limit can never fire. The clock is unaffected.
    const r = trial(`import sys\nsys.settrace(None)\n${RUNAWAY}`)
    expect(r.outcome).toBe('raised')
    expect(r.errorType).toBe('KeyboardInterrupt')
  }, 30_000)

  it('stops code that diluted its operation cost by flattening onto one line', () => {
    const flattened = `i = 0\nwhile i < ${RUNAWAY_ITERATIONS}: i += 1; i += 1; i += 1; i += 1; i += 1; i += 1; i += 1; i += 1\n"COMPLETED"`
    const r = trial(flattened)
    expect(r.outcome).toBe('raised')
    expect(r.errorType).toBe('KeyboardInterrupt')
  }, 30_000)

  it.each([
    ['bare except', `i = 0\ntry:\n    while i < ${RUNAWAY_ITERATIONS}: i += 1\nexcept: pass\n"SURVIVED"`],
    ['except KeyboardInterrupt', `i = 0\ntry:\n    while i < ${RUNAWAY_ITERATIONS}: i += 1\nexcept KeyboardInterrupt: pass\n"SURVIVED"`],
    ['except BaseException', `i = 0\ntry:\n    while i < ${RUNAWAY_ITERATIONS}: i += 1\nexcept BaseException: pass\n"SURVIVED"`],
    [
      'retry loop around the computation',
      `i = 0\nfor _ in range(1000):\n    try:\n        while i < ${RUNAWAY_ITERATIONS}: i += 1\n        break\n    except BaseException: pass\n"SURVIVED"`,
    ],
  ])('student code cannot swallow the interrupt with %s', (_label, code) => {
    const r = trial(code)
    expect(r.outcome).toBe('raised')
    expect(r.value).not.toBe('SURVIVED')
  }, 30_000)

  it('leaves the runtime usable for the next testcase after an interrupt', () => {
    trial(RUNAWAY)
    const after = trial('sum(range(1000))')
    expect(after.outcome).toBe('returned')
    expect(after.value).toBe('499500')
  }, 30_000)

  it('survives consecutive interrupts without corrupting the batch', () => {
    const outcomes = [trial(RUNAWAY), trial(RUNAWAY), trial(RUNAWAY)].map((r) => r.outcome)
    expect(outcomes).toEqual(['raised', 'raised', 'raised'])

    const after = trial('sum(range(10))')
    expect(after.outcome).toBe('returned')
    expect(after.value).toBe('45')
  }, 60_000)

  it('does not interrupt a testcase whose generation has moved on', () => {
    // Arm generation N with a budget, let it lapse without running anything,
    // then run a short testcase under generation N+1.
    generation = (generation + 1) & 0xff
    view[SLOT_SIGNAL] = 0
    view[SLOT_GENERATION] = generation
    watchdog.postMessage({ generation, budgetMs: 1 })

    // Move the armed generation on, as disarm-then-arm does between testcases.
    generation = (generation + 1) & 0xff
    view[SLOT_GENERATION] = generation

    const r = trial('sum(range(1000))')
    expect(r.outcome).toBe('returned')
  }, 30_000)
})
