/**
 * useSessionRecorder — records a single work session's timeline (edit / run /
 * submit events) for one challenge into local persistence.
 *
 * Editor edits are captured by a debounced watcher on the code ref; the
 * debounce interval comes from the challenge frontmatter (see
 * `resolveDebounceMs`). Consecutive identical edits are de-duplicated. Run and
 * submit events are pushed explicitly by the caller. All writes are best-effort
 * (the adapter degrades silently when IndexedDB is unavailable).
 */
import type { Ref, WatchStopHandle } from 'vue'
import { watchDebounced } from '@vueuse/core'
import * as db from '../persistence/db'
import type { SessionEvent, VerdictDetail, SubmitTestcaseResult } from '../persistence/types'

export const DEFAULT_DEBOUNCE_MS = 1000
export const MIN_DEBOUNCE_MS = 100
export const MAX_DEBOUNCE_MS = 10000

/**
 * Resolve the per-challenge editor-capture debounce from a raw frontmatter
 * value. Defaults to 1000ms when absent; non-integer or out-of-range values
 * fall back to the default.
 */
export function resolveDebounceMs(raw: unknown): number {
  const n = typeof raw === 'number' ? raw : Number(raw)
  if (!Number.isInteger(n)) return DEFAULT_DEBOUNCE_MS
  if (n < MIN_DEBOUNCE_MS || n > MAX_DEBOUNCE_MS) return DEFAULT_DEBOUNCE_MS
  return n
}

export interface SessionRecorder {
  recordEdit(code: string): void
  recordRun(stdin: string, stdout: string, error?: string): void
  recordSubmit(
    code: string,
    summary: { passed: number; total: number },
    results: SubmitTestcaseResult[],
  ): void
  stop(): void
}

export interface SessionRecorderOptions {
  slug: string
  /** Reactive editor buffer to watch for debounced edit snapshots. */
  code?: Ref<string>
  debounceMs?: number
  /**
   * Verdict-detail authority that governs answer-key filtering of persisted
   * submit results. Pass a getter (not a fixed value) so the pool's own
   * verdict_detail — the source of truth, only known after the pool loads — is
   * read at capture time rather than a value frozen at mount.
   */
  verdictDetail?: VerdictDetail | (() => VerdictDetail | undefined)
  /** Injectable clock for deterministic tests. */
  now?: () => number
}

export function useSessionRecorder(opts: SessionRecorderOptions): SessionRecorder {
  const now = opts.now ?? (() => Date.now())
  const startedAt = now()
  const sessionId = `${startedAt}-${Math.random().toString(36).slice(2, 8)}`
  const debounceMs = opts.debounceMs ?? DEFAULT_DEBOUNCE_MS
  const vd = opts.verdictDetail
  const readVerdictDetail: () => VerdictDetail | undefined =
    typeof vd === 'function' ? vd : () => vd
  let lastEditCode: string | null = null
  // Serialize appends so rapid successive events don't race on the same
  // session key (each append reads-then-writes the session record).
  let writeChain: Promise<void> = Promise.resolve()

  function append(event: SessionEvent): void {
    writeChain = writeChain.then(() =>
      db.appendEvent(opts.slug, sessionId, event, {
        startedAt,
        verdictDetailAtCapture: readVerdictDetail(),
      }),
    )
  }

  function recordEdit(code: string): void {
    if (code === lastEditCode) return // dedup consecutive identical buffers
    lastEditCode = code
    append({ ts: now(), kind: 'edit', code })
  }

  function recordRun(stdin: string, stdout: string, error?: string): void {
    append({ ts: now(), kind: 'run', stdin, stdout, error })
  }

  function recordSubmit(
    code: string,
    summary: { passed: number; total: number },
    results: SubmitTestcaseResult[],
  ): void {
    lastEditCode = code // the submitted buffer is now the latest known state
    append({ ts: now(), kind: 'submit', code, summary, results })
  }

  let stopWatch: WatchStopHandle | null = null
  if (opts.code) {
    stopWatch = watchDebounced(opts.code, (code) => recordEdit(code), { debounce: debounceMs })
  }

  function stop(): void {
    stopWatch?.()
    stopWatch = null
  }

  return { recordEdit, recordRun, recordSubmit, stop }
}
