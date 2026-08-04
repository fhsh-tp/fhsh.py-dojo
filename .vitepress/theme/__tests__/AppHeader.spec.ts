import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import AppHeader from '../components/layout/AppHeader.vue'

const mockIsDark = ref(false)
const mockGo = vi.fn()

vi.mock('vitepress', () => ({
  useRouter: () => ({ go: mockGo }),
  useData: () => ({ isDark: mockIsDark }),
}))

function mountHeader(isDarkVal = false, extraProps: { backUrl?: string } = {}) {
  mockIsDark.value = isDarkVal
  return mount(AppHeader, {
    props: { title: 'Test Challenge', difficulty: 'easy', ...extraProps },
  })
}

describe('AppHeader', () => {
  beforeEach(() => {
    mockIsDark.value = false
    mockGo.mockClear()
  })

  it('renders a theme toggle button (Requirement: AppHeader provides a dark/light mode toggle)', () => {
    const wrapper = mountHeader()
    expect(wrapper.find('[data-testid="theme-toggle"]').exists()).toBe(true)
  })

  it('shows moon icon aria-label in light mode — indicates "switch to dark" (Requirement: Toggle reflects light mode on load)', () => {
    const wrapper = mountHeader(false)
    const btn = wrapper.find('[data-testid="theme-toggle"]')
    expect(btn.attributes('aria-label')).toMatch(/dark/i)
  })

  it('shows sun icon aria-label in dark mode — indicates "switch to light" (Requirement: Toggle reflects current mode)', () => {
    const wrapper = mountHeader(true)
    const btn = wrapper.find('[data-testid="theme-toggle"]')
    expect(btn.attributes('aria-label')).toMatch(/light/i)
  })

  it('toggles isDark when clicked (Requirement: Toggle switches to dark mode)', async () => {
    const wrapper = mountHeader(false)
    await wrapper.find('[data-testid="theme-toggle"]').trigger('click')
    expect(mockIsDark.value).toBe(true)
  })

  it('toggles back to light when clicked in dark mode (Requirement: Toggle switches to light mode)', async () => {
    const wrapper = mountHeader(true)
    await wrapper.find('[data-testid="theme-toggle"]').trigger('click')
    expect(mockIsDark.value).toBe(false)
  })

  it('applies deep navy bg-blue-900 in light mode (Requirement: AppHeader applies dual-theme styles)', () => {
    const wrapper = mountHeader(false)
    expect(wrapper.find('header').classes()).toContain('bg-blue-900')
  })

  it('applies dark:bg-transparent in dark mode via class attribute (Requirement: AppHeader applies dual-theme styles)', () => {
    const wrapper = mountHeader(true)
    expect(wrapper.find('header').classes()).toContain('dark:bg-transparent')
  })

  it('back button navigates to /challenges by default (Requirement: back button targets the list page)', async () => {
    const wrapper = mountHeader()
    await wrapper.find('[aria-label="返回列表"]').trigger('click')
    expect(mockGo).toHaveBeenCalledWith('/challenges')
  })

  it('back button navigates to the provided back-url (Requirement: apcs challenges return to /apcs-challenges)', async () => {
    const wrapper = mountHeader(false, { backUrl: '/apcs-challenges' })
    await wrapper.find('[aria-label="返回列表"]').trigger('click')
    expect(mockGo).toHaveBeenCalledWith('/apcs-challenges')
  })
})
