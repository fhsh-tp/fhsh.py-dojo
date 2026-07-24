import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises, DOMWrapper, type VueWrapper } from '@vue/test-utils'
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

const BTN = '[data-testid="download-record-btn"]'
const PANEL = '[data-testid="download-panel"]'

let wrapper: VueWrapper | null = null

function mountButton() {
  wrapper = mount(DownloadRecordButton, {
    props: { slug: 'arithmetic-sum', title: '等差數列求和' },
    attachTo: document.body,
  })
  return wrapper
}

// The panel is teleported to <body>, so it lives outside the wrapper's subtree.
const panelEl = () => document.querySelector(PANEL) as HTMLElement | null
const dom = (sel: string) => new DOMWrapper(document.querySelector(sel) as Element)
// v-show keeps the panel in the DOM permanently; "open" means it is visible
// (v-show toggles inline `display: none`), not that the element exists.
const panelVisible = () => panelEl() !== null && panelEl()!.style.display !== 'none'

beforeEach(() => {
  vi.clearAllMocks()
  listSessionsMock.mockResolvedValue(storedSessions)
})
afterEach(() => {
  wrapper?.unmount()
  wrapper = null
  // Safety: drop any teleported panel left in <body>.
  document.querySelectorAll(PANEL).forEach((el) => el.remove())
})

describe('DownloadRecordButton (Requirement: Download panel opens as an anchored upward popover)', () => {
  it('has an accessible label and toggles the options panel', async () => {
    const w = mountButton()
    const btn = w.find(BTN)
    expect(btn.attributes('aria-label')).toBe('下載作答紀錄')
    expect(panelVisible()).toBe(false)
    await btn.trigger('click')
    await flushPromises()
    expect(wrapper!.find(BTN).attributes('aria-expanded')).toBe('true')
    expect(panelVisible()).toBe(true)
  })

  it('renders the panel teleported into document.body', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    const panel = panelEl()
    expect(panel).not.toBeNull()
    expect(document.body.contains(panel)).toBe(true)
    // Teleported out of the component subtree: the wrapper no longer finds it.
    expect(w.find(PANEL).exists()).toBe(false)
  })

  it('downloads a Markdown file built from the stored sessions', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    await dom('[data-testid="download-md"]').trigger('click')
    await flushPromises()
    expect(listSessionsMock).toHaveBeenCalledWith('arithmetic-sum')
    expect(downloadMock).toHaveBeenCalledOnce()
    const call = downloadMock.mock.calls[0]!
    expect(call[0].endsWith('.md')).toBe(true)
    expect(call[1]).toContain('等差數列求和')
    expect(call[2]).toBe('text/markdown')
  })

  it('closes on Escape', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    expect(panelVisible()).toBe(true)
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await flushPromises()
    expect(panelVisible()).toBe(false)
  })

  it('closes on an outside mousedown', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    expect(panelVisible()).toBe(true)
    document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(panelVisible()).toBe(false)
  })
})

describe('DownloadRecordButton (Requirement: Download panel form state survives reopen)', () => {
  it('keeps the typed name after an outside-mousedown close and reopen', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    expect(panelVisible()).toBe(true)

    const nameInput = panelEl()!.querySelector('input[type="text"]') as HTMLInputElement
    await new DOMWrapper(nameInput).setValue('王小明')

    document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(panelVisible()).toBe(false)

    await w.find(BTN).trigger('click')
    await flushPromises()
    expect(panelVisible()).toBe(true)
    expect((panelEl()!.querySelector('input[type="text"]') as HTMLInputElement).value).toBe(
      '王小明',
    )
  })

  // The spec scenario names BOTH dismissal paths ("outside clicks or Escape");
  // cover the Escape path explicitly rather than inferring it from v-show.
  it('keeps the typed name after an Escape close and reopen', async () => {
    const w = mountButton()
    await w.find(BTN).trigger('click')
    await flushPromises()
    const nameInput = panelEl()!.querySelector('input[type="text"]') as HTMLInputElement
    await new DOMWrapper(nameInput).setValue('王小明')

    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await flushPromises()
    expect(panelVisible()).toBe(false)

    await w.find(BTN).trigger('click')
    await flushPromises()
    expect((panelEl()!.querySelector('input[type="text"]') as HTMLInputElement).value).toBe(
      '王小明',
    )
  })

  it('constrains panel height from the anchor position (internal scroll on short viewports)', async () => {
    const w = mountButton()
    const anchor = w.find(BTN).element as HTMLElement
    vi.spyOn(anchor, 'getBoundingClientRect').mockReturnValue({
      top: 200,
      right: 900,
      bottom: 0,
      left: 0,
      width: 0,
      height: 0,
      x: 0,
      y: 0,
      toJSON: () => ({}),
    } as DOMRect)
    await w.find(BTN).trigger('click')
    await flushPromises()
    const panel = panelEl()!
    expect(panel.style.maxHeight).toBe('184px') // rect.top − 16
    expect(panel.style.overflowY).toBe('auto')
  })
})
