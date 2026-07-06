import { beforeEach, afterEach, describe, it, expect, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { IDBFactory } from 'fake-indexeddb'
import { useProgressStore } from './progress'
import * as dbAdapter from '../persistence/db'

beforeEach(async () => {
  setActivePinia(createPinia())
  vi.stubGlobal('indexedDB', new IDBFactory())
  await dbAdapter._resetConnectionForTests()
})
afterEach(async () => {
  await dbAdapter._resetConnectionForTests()
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('progress store', () => {
  it('does not touch IndexedDB in the store setup body (SSR-safe)', () => {
    const spy = vi.spyOn(dbAdapter, 'getAllProgress')
    const store = useProgressStore() // instantiation runs the setup body
    expect(store.initialised).toBe(false)
    expect(spy).not.toHaveBeenCalled() // no IO until init()
  })

  it('records a full-AC submit as completed, reactively and persisted', async () => {
    const store = useProgressStore()
    await store.init()
    await store.recordSubmit('a', 3, 3, 100)
    expect(store.isCompleted('a')).toBe(true)
    expect(store.completedCount).toBe(1)
    expect((await dbAdapter.getProgress('a'))?.status).toBe('completed')
  })

  it('records a partial submit as attempted, not completed', async () => {
    const store = useProgressStore()
    await store.init()
    await store.recordSubmit('a', 1, 3, 100)
    expect(store.isCompleted('a')).toBe(false)
    expect(store.completedCount).toBe(0)
  })

  it('keeps firstCompletedAt fixed and never downgrades a completed challenge', async () => {
    const store = useProgressStore()
    await store.init()
    await store.recordSubmit('a', 3, 3, 100)
    await store.recordSubmit('a', 1, 3, 200) // later partial re-attempt
    expect(store.isCompleted('a')).toBe(true)
    expect(store.records['a']?.firstCompletedAt).toBe(100)
  })

  it('degrades to empty state with no-op persistence when IndexedDB is unavailable', async () => {
    vi.stubGlobal('indexedDB', undefined)
    await dbAdapter._resetConnectionForTests()
    const store = useProgressStore()
    await store.init()
    expect(store.completedCount).toBe(0)
    await expect(store.recordSubmit('a', 3, 3, 100)).resolves.toBeUndefined() // never throws
  })
})
