/**
 * Per-testcase wall-clock deadline for judged Python execution.
 *
 * Why this exists: the Worker's own 5 s flag was a `setTimeout` macrotask, and
 * for synchronous student code the continuation after `await` (a microtask)
 * always ran `clearTimeout` before an expired timer callback could fire. The
 * flag therefore never produced a TLE verdict, which left the operation
 * counter as the only cost gate — and the counter has two measured bypasses
 * (freezing it with `sys.settrace(None)`, and diluting it by flattening loop
 * iterations onto one source line). Both bypasses beat the counter; neither
 * beats a clock.
 *
 * The clock lives here, split across two layers:
 *
 *  1. Interrupt (promptness). The main thread — which is never blocked while
 *     Python runs inside the Worker — writes the Pyodide interrupt signal into
 *     a `SharedArrayBuffer` when the deadline elapses. Pyodide checks that
 *     buffer inside its evaluation loop and raises, so the offending testcase
 *     stops at the deadline instead of consuming the whole batch budget.
 *  2. Elapsed adjudication (authority). Whatever the executing code did about
 *     the interrupt, a testcase whose measured elapsed time exceeded the
 *     deadline is judged TLE. This is also the whole mechanism when
 *     `SharedArrayBuffer` is unavailable, which is why the interrupt layer is
 *     allowed to be absent without failing the run.
 */

/**
 * Wall-clock budget for a single testcase, in milliseconds.
 *
 * Pinned by measurement, not chosen. Every shipped challenge's
 * `reference_solution` was submitted through the production path served by
 * Cloudflare's local runtime; the slowest single testcase across all sixteen
 * was 376 ms (prize-order-code). The two routes the operation counter cannot
 * see — one that freezes the tracer with `sys.settrace(None)`, one that
 * delegates the quadratic work to `str.replace` — both run past 5 s on
 * gem-blast's heavy entries. 5,000 ms therefore sits 13.3x above the slowest
 * honest solution and below both bypasses.
 *
 * The value is also the one the platform always intended: the inert
 * `setTimeout` flag this capability replaces was set to the same 5 s.
 *
 * Re-derive with `openspec/changes/add-judge-deadline/measure/sweep.sh` before
 * changing it, and re-check the two bounds rather than the single number.
 */
export const DEADLINE_MS = 5_000

/** Value Pyodide reads as SIGINT from the interrupt buffer. */
export const INTERRUPT_SIGNAL = 2

/** Byte offset Pyodide polls for the interrupt signal. */
export const SLOT_SIGNAL = 0

/**
 * Byte offset holding the generation of the currently-armed testcase. An
 * expiry belonging to a finished testcase compares its captured generation
 * against this slot and stays silent when they differ, so a late timer can
 * never interrupt a later testcase.
 */
export const SLOT_GENERATION = 1

export interface InterruptChannel {
  /** False when the environment cannot provide a `SharedArrayBuffer`. */
  supported: boolean
  /** Passed to the Worker so Pyodide can poll it; null when unsupported. */
  buffer: SharedArrayBuffer | null
  /** Main-thread view over `buffer`; null when unsupported. */
  view: Uint8Array | null
}

/**
 * One-shot latch so the degraded path is reported to a developer exactly once
 * per page, rather than once per submission.
 */
let degradationReported = false

/** Reset the one-shot degradation latch. Test-only seam. */
export function resetDegradationNotice(): void {
  degradationReported = false
}

/**
 * Allocate the shared interrupt channel.
 *
 * `SharedArrayBuffer` requires cross-origin isolation. When the response
 * headers are absent the constructor is simply not defined, and judging must
 * continue on elapsed adjudication alone — a missing clock would be worse than
 * a late one. The situation is a deployment defect, not a student-facing
 * error, so it is reported to the console and nowhere else.
 */
export function createInterruptChannel(): InterruptChannel {
  const unsupported: InterruptChannel = { supported: false, buffer: null, view: null }

  if (typeof SharedArrayBuffer === 'undefined') {
    reportDegradation('SharedArrayBuffer is unavailable')
    return unsupported
  }

  try {
    const buffer = new SharedArrayBuffer(2)
    return { supported: true, buffer, view: new Uint8Array(buffer) }
  } catch (err) {
    // Some environments expose the constructor but refuse allocation.
    reportDegradation(`SharedArrayBuffer allocation failed: ${String(err)}`)
    return unsupported
  }
}

function reportDegradation(reason: string): void {
  if (degradationReported) return
  degradationReported = true
  console.warn(
    `[judge-deadline] ${reason}. Per-testcase deadlines will be adjudicated from elapsed ` +
      `time after each testcase finishes instead of interrupting it. Serve the site with ` +
      `Cross-Origin-Opener-Policy: same-origin and Cross-Origin-Embedder-Policy: require-corp ` +
      `to restore prompt interruption.`,
  )
}

/**
 * Arms and disarms the per-testcase deadline from the main thread.
 *
 * Arming is strictly scoped to the window in which user code is executing.
 * Leaving the signal raised across the runtime's own initialisation or
 * teardown was measured to land the interrupt inside Pyodide's asyncio
 * machinery and leave the runtime unusable for every subsequent testcase.
 */
export class DeadlineWatchdog {
  private timer: ReturnType<typeof setTimeout> | null = null
  private readonly channel: InterruptChannel
  private readonly deadlineMs: number

  constructor(channel: InterruptChannel, deadlineMs: number = DEADLINE_MS) {
    this.channel = channel
    this.deadlineMs = deadlineMs
  }

  /**
   * Start the countdown for one testcase. Clears any signal left raised by the
   * previous testcase so the next execution does not inherit an interrupt.
   */
  arm(generation: number): void {
    this.cancelTimer()

    const view = this.channel.view
    if (view === null) return

    const slot = generation & 0xff
    view[SLOT_SIGNAL] = 0
    view[SLOT_GENERATION] = slot

    this.timer = setTimeout(() => {
      this.timer = null
      // Silent when the armed generation has moved on: this expiry belongs to
      // a testcase that already finished.
      if (view[SLOT_GENERATION] !== slot) return
      view[SLOT_SIGNAL] = INTERRUPT_SIGNAL
    }, this.deadlineMs)
  }

  /** Stop the countdown for the current testcase and lower the signal. */
  disarm(): void {
    this.cancelTimer()
    const view = this.channel.view
    if (view === null) return
    view[SLOT_SIGNAL] = 0
  }

  /** Release the watchdog for good; safe to call more than once. */
  dispose(): void {
    this.cancelTimer()
  }

  private cancelTimer(): void {
    if (this.timer !== null) {
      clearTimeout(this.timer)
      this.timer = null
    }
  }
}

/**
 * Authoritative deadline verdict, measured outside the Python runtime.
 *
 * Applied after every testcase regardless of how it ended: student code that
 * catches the interrupt and keeps going still exceeded its budget, and code
 * that ran without an interrupt channel at all is judged by this alone.
 */
export function exceededDeadline(elapsedMs: number, deadlineMs: number = DEADLINE_MS): boolean {
  return elapsedMs > deadlineMs
}
