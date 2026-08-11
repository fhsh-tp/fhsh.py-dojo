import { computed, ref } from 'vue'
import { useExecutorStore } from '../stores/executor'
import type {
  RunRequest,
  TestcaseResult,
  TestcaseStart,
  RunComplete,
  ExecuteRequest,
  ExecuteResult,
  VerdictDetail,
} from '../workers/pyodide.worker'
import { createInterruptChannel, DeadlineWatchdog, DEADLINE_MS, KILL_MARGIN_MS } from '../workers/deadline'

const WALL_CLOCK_KILL_MS = 6_000

/**
 * Manages the Pyodide Worker lifecycle.
 *
 * Creates a fresh Worker on each `run()` call and terminates it on `stop()`.
 * Wall-clock hard kill: if the Worker does not complete within 6 s the main
 * thread terminates it (secondary guard beyond the Worker's own setTimeout).
 */
export function useExecutor() {
  const store = useExecutorStore()
  const workerRef = ref<Worker | null>(null)
  const killTimer = ref<ReturnType<typeof setTimeout> | null>(null)
  // Per-testcase deadline. The Worker blocks inside synchronous Python, so
  // the countdown has to live here on the main thread.
  let watchdog: DeadlineWatchdog | null = null

  const isRunning = computed(() => store.status === 'running')

  function _clearKillTimer() {
    if (killTimer.value !== null) {
      clearTimeout(killTimer.value)
      killTimer.value = null
    }
  }

  function _terminateWorker() {
    workerRef.value?.terminate()
    workerRef.value = null
  }

  function _disposeWatchdog() {
    watchdog?.dispose()
    watchdog = null
  }

  function stop() {
    _clearKillTimer()
    _disposeWatchdog()
    _terminateWorker()
    if (store.status === 'running') {
      store.setDone(store.totalTestcases, store.passedCount)
    }
  }

  async function run(
    code: string,
    testcases: Array<{ input: string; expected_output: string }>,
    verdictDetail: VerdictDetail = 'hidden',
  ): Promise<void> {
    if (store.status === 'running') stop()

    store.setRunning(testcases.length)

    const worker = new Worker(new URL('../workers/pyodide.worker.ts', import.meta.url), {
      type: 'module',
    })
    workerRef.value = worker

    const channel = createInterruptChannel()
    watchdog = new DeadlineWatchdog(channel)

    // Wall-clock hard kill (main-thread side). Retained as the total-time
    // backstop: the per-testcase deadline bounds each case, this bounds the
    // batch and covers a Worker that stops responding altogether.
    const totalBudget = testcases.length * WALL_CLOCK_KILL_MS
    killTimer.value = setTimeout(() => {
      stop()
    }, totalBudget)

    worker.onmessage = (event: MessageEvent<TestcaseStart | TestcaseResult | RunComplete>) => {
      const msg = event.data
      if (msg.type === 'testcase_start') {
        watchdog?.arm(msg.generation)
      } else if (msg.type === 'testcase_result') {
        // The testcase is over the moment its result arrives; leaving the
        // signal raised would interrupt the next one.
        watchdog?.disarm()
        store.addResult(msg)
      } else if (msg.type === 'run_complete') {
        _clearKillTimer()
        _disposeWatchdog()
        store.setDone(msg.total, msg.passed)
        _terminateWorker()
      }
    }

    worker.onerror = () => {
      _clearKillTimer()
      _disposeWatchdog()
      store.setDone(store.totalTestcases, store.passedCount)
      _terminateWorker()
    }

    // Convert reactive Proxy objects to plain structures before postMessage.
    // Structured-clone (used internally by postMessage) cannot handle Vue Proxies.
    const request: RunRequest = {
      type: 'run',
      code,
      testcases: testcases.map((tc) => ({ input: tc.input, expected_output: tc.expected_output })),
      verdictDetail,
      ...(channel.buffer === null ? {} : { interruptBuffer: channel.buffer }),
    }
    worker.postMessage(request)
  }

  /**
   * Execute code with stdin, returning raw stdout (no verdict comparison).
   * Creates a fresh Worker, sends an ExecuteRequest, and resolves on completion.
   * Wall-clock kill timer terminates the Worker after 6 s.
   */
  function execute(code: string, stdin: string): Promise<ExecuteResult> {
    return new Promise((resolve) => {
      const worker = new Worker(new URL('../workers/pyodide.worker.ts', import.meta.url), {
        type: 'module',
      })

      const channel = createInterruptChannel()
      const runWatchdog = new DeadlineWatchdog(channel)

      // The kill timer guards against a Worker that stops responding at all.
      // It starts here, before Pyodide has loaded, so once user code actually
      // begins it is re-armed relative to that moment — otherwise Pyodide's
      // warm-up eats the budget and the kill preempts the deadline, which
      // terminates the Worker instead of producing a timed-out result.
      let timer = setTimeout(onKill, WALL_CLOCK_KILL_MS)

      function onKill() {
        runWatchdog.dispose()
        worker.terminate()
        resolve({
          type: 'execute_result',
          stdout: '',
          elapsed_ms: WALL_CLOCK_KILL_MS,
          error: 'Execution timed out',
        })
      }

      worker.onmessage = (event: MessageEvent<TestcaseStart | ExecuteResult>) => {
        if (event.data.type === 'testcase_start') {
          runWatchdog.arm(event.data.generation)
          clearTimeout(timer)
          timer = setTimeout(onKill, DEADLINE_MS + KILL_MARGIN_MS)
          return
        }
        if (event.data.type === 'execute_result') {
          clearTimeout(timer)
          runWatchdog.dispose()
          worker.terminate()
          resolve(event.data)
        }
      }

      worker.onerror = () => {
        clearTimeout(timer)
        runWatchdog.dispose()
        worker.terminate()
        resolve({
          type: 'execute_result',
          stdout: '',
          elapsed_ms: 0,
          error: 'Worker error',
        })
      }

      const request: ExecuteRequest = {
        type: 'execute',
        code,
        stdin,
        ...(channel.buffer === null ? {} : { interruptBuffer: channel.buffer }),
      }
      worker.postMessage(request)
    })
  }

  return { isRunning, run, stop, execute }
}
