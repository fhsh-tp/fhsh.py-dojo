import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import CompletionBadge from '../components/challenge/CompletionBadge.vue'

describe('CompletionBadge', () => {
  it('renders with an accessible completion label', () => {
    const badge = mount(CompletionBadge).find('[data-testid="completion-badge"]')
    expect(badge.exists()).toBe(true)
    expect(badge.attributes('aria-label')).toBe('已完成')
  })
})
