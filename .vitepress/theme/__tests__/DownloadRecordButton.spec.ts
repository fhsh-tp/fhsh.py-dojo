import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import DownloadRecordButton from '../components/editor/DownloadRecordButton.vue'
import { listSessions } from '../persistence/db'
import { downloadTextFile } from '../lib/download'
import type { SessionRecord } from '../persistence/types'

vi.mock('../persistence/db', () => ({ listSessions: vi.fn() }))
vi.mock('../lib/download', () => ({ downloadTextFile: vi.fn() }))

const listSessionsMock = vi.mocked(listSessions)
const downloadMock = vi.mocked(downloadTextFile)

const storedSessions: SessionRecord[] = [
  {
    slug: 'arithmetic-sum',
    sessionId: 's1',
    startedAt: 1,
    verdictDetailAtCapture: 'hidden',
    events: [{ ts: 1, kind: 'submit', code: 'x', summary: { passed: 1, total: 1 }, results: [] }],
  },
]

describe('DownloadRecordButton', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    listSessionsMock.mockResolvedValue(storedSessions)
  })

  it('has an accessible label and toggles the options panel', async () => {
    const wrapper = mount(DownloadRecordButton, { props: { slug: 'arithmetic-sum', title: '等差數列求和' } })
    const btn = wrapper.find('[data-testid="download-record-btn"]')
    expect(btn.attributes('aria-label')).toBe('下載作答紀錄')
    await btn.trigger('click')
    expect(wrapper.find('[data-testid="download-panel"]').exists()).toBe(true)
  })

  it('downloads a Markdown file built from the stored sessions', async () => {
    const wrapper = mount(DownloadRecordButton, { props: { slug: 'arithmetic-sum', title: '等差數列求和' } })
    await wrapper.find('[data-testid="download-record-btn"]').trigger('click')
    await wrapper.find('[data-testid="download-md"]').trigger('click')
    await flushPromises()
    expect(listSessionsMock).toHaveBeenCalledWith('arithmetic-sum')
    expect(downloadMock).toHaveBeenCalledOnce()
    const call = downloadMock.mock.calls[0]!
    expect(call[0].endsWith('.md')).toBe(true)
    expect(call[1]).toContain('等差數列求和')
    expect(call[2]).toBe('text/markdown')
  })
})
