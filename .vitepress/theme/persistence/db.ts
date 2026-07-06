/**
 * IndexedDB adapter for local student-progress persistence.
 *
 * SSR-safe by construction: the database connection is opened lazily inside
 * the exported functions, never at module evaluation. All access is guarded by
 * `isAvailable()` and wrapped so that a missing/blocked IndexedDB (private
 * mode, SSR/build) degrades to empty reads and no-op writes rather than
 * throwing — the challenge/run/submit flow must never break because of this.
 */
import { openDB, type IDBPDatabase, type DBSchema } from 'idb'
import type { ProgressRecord, SessionRecord, SessionEvent, VerdictDetail } from './types'

const DB_NAME = 'fhsh-py-dojo-progress'
const DB_VERSION = 1

/** Keep at most this many work sessions per challenge (most recent kept in full). */
export const SESSIONS_PER_CHALLENGE_CAP = 5

interface ProgressDB extends DBSchema {
  progress: { key: string; value: ProgressRecord }
  sessions: {
    key: [string, string]
    value: SessionRecord
    indexes: { 'by-slug': string }
  }
}

let dbPromise: Promise<IDBPDatabase<ProgressDB>> | null = null

/** True when IndexedDB is usable in this environment (client, not private-blocked). */
export function isAvailable(): boolean {
  try {
    return typeof indexedDB !== 'undefined' && indexedDB !== null
  } catch {
    return false
  }
}

function getDb(): Promise<IDBPDatabase<ProgressDB>> {
  if (!dbPromise) {
    dbPromise = openDB<ProgressDB>(DB_NAME, DB_VERSION, {
      upgrade(db, oldVersion) {
        // v1: initial schema. Future versions add their migrations here,
        // keyed off oldVersion, migrating forward or safely resetting.
        if (oldVersion < 1) {
          db.createObjectStore('progress', { keyPath: 'slug' })
          const sessions = db.createObjectStore('sessions', {
            keyPath: ['slug', 'sessionId'],
          })
          sessions.createIndex('by-slug', 'slug')
        }
      },
    })
  }
  return dbPromise
}

export async function getProgress(slug: string): Promise<ProgressRecord | undefined> {
  if (!isAvailable()) return undefined
  try {
    return await (await getDb()).get('progress', slug)
  } catch {
    return undefined
  }
}

export async function getAllProgress(): Promise<ProgressRecord[]> {
  if (!isAvailable()) return []
  try {
    return await (await getDb()).getAll('progress')
  } catch {
    return []
  }
}

export async function upsertProgress(rec: ProgressRecord): Promise<void> {
  if (!isAvailable()) return
  try {
    await (await getDb()).put('progress', rec)
  } catch {
    // best-effort: never surface a persistence failure to the student
  }
}

/**
 * Append an event to a session, creating the session on its first event.
 * When a brand-new session is created, the per-challenge retention cap is
 * enforced so old sessions are pruned.
 */
export async function appendEvent(
  slug: string,
  sessionId: string,
  event: SessionEvent,
  meta: { startedAt: number; verdictDetailAtCapture?: VerdictDetail },
): Promise<void> {
  if (!isAvailable()) return
  try {
    const db = await getDb()
    const key: [string, string] = [slug, sessionId]
    const existing = await db.get('sessions', key)
    if (existing) {
      existing.events.push(event)
      // Converge the session's answer-key authority to the latest known value.
      // The pool's verdict_detail (the source of truth) is only known after the
      // pool loads, so the first (edit) event may capture `undefined`; a later
      // event refreshes it. Only submit events carry answer-key data, and by
      // submit time the pool has always loaded — so the stored authority is
      // correct for every event that could leak.
      if (meta.verdictDetailAtCapture !== undefined) {
        existing.verdictDetailAtCapture = meta.verdictDetailAtCapture
      }
      await db.put('sessions', existing)
    } else {
      await db.put('sessions', {
        slug,
        sessionId,
        startedAt: meta.startedAt,
        verdictDetailAtCapture: meta.verdictDetailAtCapture,
        events: [event],
      })
      await pruneSessions(slug)
    }
  } catch {
    // best-effort
  }
}

export async function listSessions(slug: string): Promise<SessionRecord[]> {
  if (!isAvailable()) return []
  try {
    const all = await (await getDb()).getAllFromIndex('sessions', 'by-slug', slug)
    return all.sort((a, b) => a.startedAt - b.startedAt)
  } catch {
    return []
  }
}

/**
 * Enforce the sessions-per-challenge cap: keep the `keep` most recent sessions
 * (by startedAt) in full, delete the oldest beyond that. Never truncates the
 * event list within a retained session.
 *
 * Assumes single-tab usage. If the same challenge is left open in another tab
 * long enough to become the oldest of >`keep` sessions, it may be pruned there;
 * a later append from that stale tab would then re-create it with only the new
 * event. This rare multi-tab history loss is an accepted trade-off for a
 * best-effort local recorder with no cross-tab coordination.
 */
export async function pruneSessions(slug: string, keep = SESSIONS_PER_CHALLENGE_CAP): Promise<void> {
  if (!isAvailable()) return
  try {
    const db = await getDb()
    const all = (await db.getAllFromIndex('sessions', 'by-slug', slug)).sort(
      (a, b) => a.startedAt - b.startedAt,
    )
    const excess = all.length - keep
    if (excess > 0) {
      const tx = db.transaction('sessions', 'readwrite')
      for (const s of all.slice(0, excess)) {
        await tx.store.delete([s.slug, s.sessionId])
      }
      await tx.done
    }
  } catch {
    // best-effort
  }
}

export async function clearAll(): Promise<void> {
  if (!isAvailable()) return
  try {
    const db = await getDb()
    await db.clear('progress')
    await db.clear('sessions')
  } catch {
    // best-effort
  }
}

/** Test-only: close and drop the cached connection so a fresh fake-indexeddb can be used. */
export async function _resetConnectionForTests(): Promise<void> {
  if (dbPromise) {
    try {
      ;(await dbPromise).close()
    } catch {
      // ignore
    }
  }
  dbPromise = null
}
