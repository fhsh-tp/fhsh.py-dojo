import { beforeEach, afterEach, describe, it, expect, vi } from 'vitest'
import { IDBFactory } from 'fake-indexeddb'
import * as db from './db'
import type { ProgressRecord } from './types'

function progress(slug: string, over: Partial<ProgressRecord> = {}): ProgressRecord {
  return { slug, status: 'attempted', lastAttemptAt: 1, bestPassed: 0, total: 3, ...over }
}

beforeEach(async () => {
  vi.stubGlobal('indexedDB', new IDBFactory())
  await db._resetConnectionForTests()
})
afterEach(async () => {
  await db._resetConnectionForTests()
  vi.unstubAllGlobals()
})

describe('persistence adapter', () => {
  it('reports available when indexedDB is present', () => {
    expect(db.isAvailable()).toBe(true)
  })

  it('upserts and reads back a progress record (v1 schema stores created)', async () => {
    await db.upsertProgress(progress('arithmetic-sum', { status: 'completed', firstCompletedAt: 5, bestPassed: 3, total: 3 }))
    const got = await db.getProgress('arithmetic-sum')
    expect(got?.status).toBe('completed')
    expect(got?.firstCompletedAt).toBe(5)
  })

  it('getAllProgress returns every stored record', async () => {
    await db.upsertProgress(progress('a'))
    await db.upsertProgress(progress('b'))
    expect((await db.getAllProgress()).map((r) => r.slug).sort()).toEqual(['a', 'b'])
  })

  it('appendEvent creates a session then appends to it in order', async () => {
    await db.appendEvent('a', 's1', { ts: 1, kind: 'edit', code: 'x' }, { startedAt: 1 })
    await db.appendEvent('a', 's1', { ts: 2, kind: 'run', stdin: '', stdout: 'o' }, { startedAt: 1 })
    const sessions = await db.listSessions('a')
    expect(sessions).toHaveLength(1)
    expect(sessions[0]?.events.map((e) => e.kind)).toEqual(['edit', 'run'])
  })

  it('prunes the oldest sessions beyond the cap, keeping recent ones whole', async () => {
    for (let i = 1; i <= 6; i++) {
      await db.appendEvent('a', `s${i}`, { ts: i, kind: 'edit', code: `c${i}` }, { startedAt: i })
      await db.appendEvent('a', `s${i}`, { ts: i + 100, kind: 'edit', code: `c${i}b` }, { startedAt: i })
    }
    const sessions = await db.listSessions('a')
    expect(sessions.map((s) => s.sessionId)).toEqual(['s2', 's3', 's4', 's5', 's6']) // s1 pruned
    expect(sessions.every((s) => s.events.length === 2)).toBe(true) // events intact, not truncated
  })

  it('appendEvent converges verdictDetailAtCapture to the latest known value', async () => {
    await db.appendEvent('a', 's1', { ts: 1, kind: 'edit', code: 'x' }, { startedAt: 1 })
    expect((await db.listSessions('a'))[0]?.verdictDetailAtCapture).toBeUndefined()
    // A later event carrying the now-known pool authority refreshes it...
    await db.appendEvent('a', 's1', { ts: 2, kind: 'edit', code: 'y' }, { startedAt: 1, verdictDetailAtCapture: 'full' })
    expect((await db.listSessions('a'))[0]?.verdictDetailAtCapture).toBe('full')
    // ...and a subsequent undefined must NOT clobber the established authority.
    await db.appendEvent('a', 's1', { ts: 3, kind: 'edit', code: 'z' }, { startedAt: 1 })
    expect((await db.listSessions('a'))[0]?.verdictDetailAtCapture).toBe('full')
  })

  it('versioned schema: opening at a higher version runs the upgrade and preserves data', async () => {
    await db.upsertProgress(progress('keep'))
    await db._resetConnectionForTests() // close the v1 connection so a v2 open is not blocked
    const { openDB } = await import('idb')
    let oldSeen = -1
    const d2 = await openDB('fhsh-py-dojo-progress', 2, {
      upgrade(database, oldVersion) {
        oldSeen = oldVersion
        if (!database.objectStoreNames.contains('future')) database.createObjectStore('future')
      },
    })
    expect(oldSeen).toBe(1) // migrated forward from the existing v1
    expect(await d2.get('progress', 'keep')).toBeDefined() // existing data preserved
    d2.close()
  })

  it('degrades to empty reads and no-op writes when indexedDB is unavailable', async () => {
    vi.stubGlobal('indexedDB', undefined)
    await db._resetConnectionForTests()
    expect(db.isAvailable()).toBe(false)
    await expect(db.upsertProgress(progress('y'))).resolves.toBeUndefined() // no throw
    await expect(db.appendEvent('y', 's', { ts: 1, kind: 'edit', code: 'x' }, { startedAt: 1 })).resolves.toBeUndefined()
    expect(await db.getProgress('y')).toBeUndefined()
    expect(await db.getAllProgress()).toEqual([])
    expect(await db.listSessions('y')).toEqual([])
  })
})
