import { beforeEach, afterEach, describe, it, expect, vi } from 'vitest'
import { ref, nextTick } from 'vue'
import { IDBFactory } from 'fake-indexeddb'
import { useSessionRecorder, resolveDebounceMs } from './useSessionRecorder'
import * as db from '../persistence/db'
import type { SessionEvent } from '../persistence/types'

beforeEach(async () => {
  vi.stubGlobal('indexedDB', new IDBFactory())
  await db._resetConnectionForTests()
})
afterEach(async () => {
  await db._resetConnectionForTests()
  vi.unstubAllGlobals()
})

async function allEvents(slug: string): Promise<SessionEvent[]> {
  const sessions = await db.listSessions(slug)
  return sessions.flatMap((s) => s.events)
}

describe('resolveDebounceMs', () => {
  it('defaults to 1000 when the field is absent', () => {
    expect(resolveDebounceMs(undefined)).toBe(1000)
  })
  it('honours a valid in-range override', () => {
    expect(resolveDebounceMs(300)).toBe(300)
  })
  it('falls back to default for non-integer values', () => {
    expect(resolveDebounceMs(1.5)).toBe(1000)
    expect(resolveDebounceMs('abc')).toBe(1000)
  })
  it('falls back to default for out-of-range values', () => {
    expect(resolveDebounceMs(50)).toBe(1000)
    expect(resolveDebounceMs(99999)).toBe(1000)
  })
})

describe('useSessionRecorder', () => {
  it('records edit/run/submit events in order and de-dups identical edits', async () => {
    let t = 0
    const rec = useSessionRecorder({ slug: 'a', now: () => ++t })
    rec.recordEdit('code1')
    rec.recordEdit('code1') // identical → deduped
    rec.recordRun('stdin', 'stdout')
    rec.recordSubmit('code2', { passed: 3, total: 3 }, [{ index: 0, verdict: 'AC', elapsed_ms: 1 }])
    await vi.waitFor(async () => {
      expect((await allEvents('a')).map((e) => e.kind)).toEqual(['edit', 'run', 'submit'])
    })
  })

  it('captures a debounced edit snapshot from the code ref', async () => {
    const code = ref('start')
    const rec = useSessionRecorder({ slug: 'b', code, debounceMs: 20 })
    code.value = 'typed'
    await nextTick()
    await vi.waitFor(
      async () => {
        const events = await allEvents('b')
        expect(events.some((e) => e.kind === 'edit' && e.code === 'typed')).toBe(true)
      },
      { timeout: 500 },
    )
    rec.stop()
  })

  it('resolves verdictDetail lazily from a getter and converges to the latest authority', async () => {
    // Simulates the pool's verdict_detail being unknown at mount ('hidden') then
    // becoming known ('full') after the pool loads, before the submit.
    let detail: 'hidden' | 'full' = 'hidden'
    let t = 0
    const rec = useSessionRecorder({ slug: 'vd', now: () => ++t, verdictDetail: () => detail })
    rec.recordEdit('c1')
    await vi.waitFor(async () => expect((await db.listSessions('vd'))[0]).toBeDefined())
    detail = 'full'
    rec.recordSubmit('c2', { passed: 1, total: 1 }, [{ index: 0, verdict: 'AC', elapsed_ms: 1 }])
    await vi.waitFor(async () => {
      expect((await db.listSessions('vd'))[0]?.verdictDetailAtCapture).toBe('full')
    })
  })
})
