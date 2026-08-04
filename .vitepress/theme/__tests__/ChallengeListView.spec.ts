import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, type VueWrapper } from '@vue/test-utils'
import { createPinia, setActivePinia, type Pinia } from 'pinia'
import { IDBFactory } from 'fake-indexeddb'
import ChallengeListView from '../views/ChallengeListView.vue'
import * as dbAdapter from '../persistence/db'
import type { Challenge } from '../types.d/challenge.type'

vi.mock('vitepress', () => ({
  useRouter: () => ({ go: vi.fn() }),
}))

const mockChallenges: Challenge[] = [
  // Chapter values deliberately digit-free so the id-search matrix below can
  // assert the id rule in isolation (a digit query must not leak in via the
  // chapter text-field OR branch).
  { id: 'py001', slug: 'caesar-encrypt', title: '凱薩加密', url: '/challenge/caesar-encrypt', difficulty: 'easy', category: 'python', tags: ['classical'], chapter: 'intro', description: '古典加密入門' },
  { id: 'py002', slug: 'rsa', title: 'RSA', url: '/challenge/rsa', difficulty: 'hard', category: 'python', tags: ['asymmetric'], chapter: 'crypto', description: '非對稱加密' },
  { id: 'py003', slug: 'vigenere', title: '維吉尼亞密碼', url: '/challenge/vigenere', difficulty: 'medium', category: 'python', tags: ['classical'], chapter: 'crypto', description: '多表代換' },
  { id: 'py010', slug: 'hash-basics', title: '雜湊入門', url: '/challenge/hash-basics', difficulty: 'easy', category: 'python', tags: ['hash'], chapter: 'hash', description: '單向函式' },
]
const completedRecord = {
  slug: 'caesar-encrypt', status: 'completed' as const, lastAttemptAt: 1, bestPassed: 3, total: 3, firstCompletedAt: 1,
}

let pinia: Pinia
let wrapper: VueWrapper | null = null

function mountView() {
  wrapper = mount(ChallengeListView, {
    props: { challenges: mockChallenges },
    global: { plugins: [pinia] },
  })
  return wrapper
}

beforeEach(async () => {
  pinia = createPinia()
  setActivePinia(pinia)
  vi.stubGlobal('indexedDB', new IDBFactory())
  await dbAdapter._resetConnectionForTests()
})
afterEach(async () => {
  wrapper?.unmount()
  wrapper = null
  await flushPromises()
  await dbAdapter._resetConnectionForTests()
  vi.unstubAllGlobals()
})

describe('ChallengeListView', () => {
  it('renders filter buttons', () => {
    expect(mountView().findAll('button').length).toBeGreaterThan(0)
  })

  it('active filter button has bg-blue-600 as light mode base (Requirement: ChallengeListView filter buttons apply dual-theme styles)', () => {
    expect(mountView().find('button').classes()).toContain('bg-blue-600')
  })

  it('active filter button has dark:bg-emerald-500 for dark mode', () => {
    expect(mountView().find('button').classes()).toContain('dark:bg-emerald-500')
  })

  it('inactive filter button has bg-blue-50 as light mode base', () => {
    expect(mountView().findAll('button')[1]?.classes()).toContain('bg-blue-50')
  })

  // Completion count (Requirement: Page-scoped completion count)
  it('shows a page-scoped completed count of X / total from stored progress', async () => {
    await dbAdapter.upsertProgress(completedRecord)
    const w = mountView()
    await vi.waitFor(() => {
      expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 4')
    })
  })

  it('ignores completed records whose slug is not on this page', async () => {
    await dbAdapter.upsertProgress({ ...completedRecord, slug: 'not-on-this-page' })
    const w = mountView()
    await flushPromises()
    await vi.waitFor(() => {
      expect(w.find('[data-testid="completed-count"]').text()).toContain('0 / 4')
    })
  })

  it('completed count stays page-scoped regardless of the active difficulty filter', async () => {
    await dbAdapter.upsertProgress(completedRecord)
    const w = mountView()
    await vi.waitFor(() => {
      expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 4')
    })
    const hardBtn = w.findAll('button').find((b) => b.text() === '困難')
    await hardBtn?.trigger('click')
    await flushPromises()
    expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 4')
  })

  // Ordinal-aware id search (Requirement: Search filters challenges by text matching across multiple fields)
  describe('id search', () => {
    async function search(q: string) {
      const w = mountView()
      await w.find('input[type="search"]').setValue(q)
      await flushPromises()
      return w
    }

    function shownIds(w: VueWrapper) {
      return w.findAll('[data-testid="challenge-id"]').map((s) => s.text())
    }

    it.each(['3', '03', '003'])('pure-digit query "%s" matches ordinal 3 exactly', async (q) => {
      expect(shownIds(await search(q))).toEqual(['py003'])
    })

    it('pure-digit query "10" matches only py010 (exact ordinal, not substring)', async () => {
      expect(shownIds(await search('10'))).toEqual(['py010'])
    })

    it('pure-digit query "1" matches only py001 (not py010)', async () => {
      expect(shownIds(await search('1'))).toEqual(['py001'])
    })

    it('prefix query "py00" matches py001–py009 style ids only', async () => {
      expect(shownIds(await search('py00'))).toEqual(['py001', 'py002', 'py003'])
    })

    it('prefix query "py" matches every id on the page', async () => {
      expect(shownIds(await search('py'))).toEqual(['py001', 'py002', 'py003', 'py010'])
    })

    it('unpadded query "py3" matches nothing via the id rule', async () => {
      const w = await search('py3')
      expect(shownIds(w)).toEqual([])
      expect(w.text()).toContain('沒有符合條件的挑戰。')
    })

    it('text-field matching still works alongside id matching', async () => {
      expect(shownIds(await search('凱薩'))).toEqual(['py001'])
    })

    it('query is trimmed before matching', async () => {
      expect(shownIds(await search('  003  '))).toEqual(['py003'])
    })
  })
})
