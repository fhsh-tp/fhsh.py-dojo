import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, type VueWrapper } from '@vue/test-utils'
import { createPinia, setActivePinia, type Pinia } from 'pinia'
import { IDBFactory } from 'fake-indexeddb'
import ChallengeListView from '../views/ChallengeListView.vue'
import * as dbAdapter from '../persistence/db'

vi.mock('vitepress', () => ({
  useRouter: () => ({ go: vi.fn() }),
}))

const mockChallenges = [
  { id: 1, slug: 'caesar-encrypt', title: '凱薩加密', url: '/challenge/caesar-encrypt', difficulty: 'easy', tags: ['classical'] },
  { id: 2, slug: 'rsa', title: 'RSA', url: '/challenge/rsa', difficulty: 'hard', tags: ['asymmetric'] },
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
      expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 2')
    })
  })

  it('ignores completed records whose slug is not on this page', async () => {
    await dbAdapter.upsertProgress({ ...completedRecord, slug: 'not-on-this-page' })
    const w = mountView()
    await flushPromises()
    await vi.waitFor(() => {
      expect(w.find('[data-testid="completed-count"]').text()).toContain('0 / 2')
    })
  })

  it('completed count stays page-scoped regardless of the active difficulty filter', async () => {
    await dbAdapter.upsertProgress(completedRecord)
    const w = mountView()
    await vi.waitFor(() => {
      expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 2')
    })
    const hardBtn = w.findAll('button').find((b) => b.text() === '困難')
    await hardBtn?.trigger('click')
    await flushPromises()
    expect(w.find('[data-testid="completed-count"]').text()).toContain('1 / 2')
  })
})
