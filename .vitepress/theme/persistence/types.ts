/**
 * Shared persistence data shapes for local student-progress storage.
 *
 * These are the durable contract between the IndexedDB adapter, the Pinia
 * store, the session recorder, and the export layer. Keep them backward
 * compatible with the on-disk schema version (see `db.ts` DB_VERSION).
 */

export type ProgressStatus = 'completed' | 'attempted'

/** Per-challenge completion record. Keyed by slug. */
export interface ProgressRecord {
  slug: string
  status: ProgressStatus
  /** epoch ms of first full-AC completion; set once, never reset. */
  firstCompletedAt?: number
  /** epoch ms of the most recent submit. */
  lastAttemptAt: number
  /** best passed count observed across attempts. */
  bestPassed: number
  /** testcase total observed at the record's latest write. */
  total: number
}

/** Verdict detail level captured with a session, mirrors the worker's contract. */
export type VerdictDetail = 'hidden' | 'actual' | 'full'
export type Verdict = 'AC' | 'WA' | 'TLE' | 'RE'

/** A single editor snapshot (full buffer) taken by the debounced recorder. */
export interface EditEvent {
  ts: number
  kind: 'edit'
  code: string
}

/** A freeform "Run" (execute with custom stdin) event. */
export interface RunEvent {
  ts: number
  kind: 'run'
  stdin: string
  stdout: string
  error?: string
}

/** One testcase outcome inside a submit event. `actual`/`expected` only present when verdict detail allows. */
export interface SubmitTestcaseResult {
  index: number
  verdict: Verdict
  elapsed_ms: number
  error?: string
  actual?: string
  expected?: string
}

/** A judged submission event. */
export interface SubmitEvent {
  ts: number
  kind: 'submit'
  code: string
  summary: { passed: number; total: number }
  results: SubmitTestcaseResult[]
}

/** Discriminated union of everything recorded on a work session's timeline. */
export type SessionEvent = EditEvent | RunEvent | SubmitEvent

/** One work session for one challenge: an ordered timeline of events. */
export interface SessionRecord {
  slug: string
  sessionId: string
  startedAt: number
  /** verdict detail in force when this session was captured, for export-time re-verification. */
  verdictDetailAtCapture?: VerdictDetail
  events: SessionEvent[]
}
