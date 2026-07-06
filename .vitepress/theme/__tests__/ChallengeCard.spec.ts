import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ChallengeCard from '../components/challenge/ChallengeCard.vue'

vi.mock('vitepress', () => ({
  useRouter: () => ({ go: vi.fn() }),
}))

const mockChallenge = {
  id: 1,
  title: '凱薩加密',
  url: '/challenge/caesar-encrypt',
  difficulty: 'easy',
  tags: ['classical'],
}

function mountCard() {
  return mount(ChallengeCard, {
    props: { challenge: mockChallenge },
  })
}

describe('ChallengeCard', () => {
  // Dual-theme tests (Requirement: ChallengeCard applies dual-theme styles)
  it('has white bg as light mode base class', () => {
    const wrapper = mountCard()
    expect(wrapper.find('button').classes()).toContain('bg-white')
  })

  it('has dark:bg-gray-900 for dark mode background', () => {
    const wrapper = mountCard()
    expect(wrapper.find('button').classes()).toContain('dark:bg-gray-900')
  })

  it('has light mode blue border base class', () => {
    const wrapper = mountCard()
    expect(wrapper.find('button').classes()).toContain('border-blue-200')
  })

  it('has dark mode neon glow hover effect (Requirement: ChallengeCard applies dual-theme styles)', () => {
    const wrapper = mountCard()
    const classes = wrapper.find('button').classes()
    expect(classes.some((c) => c.includes('dark:hover:shadow'))).toBe(true)
  })

  it('easy badge has light mode base class (Requirement: difficulty badge colors adapt to theme)', () => {
    const wrapper = mountCard()
    const badge = wrapper.find('span.px-2')
    expect(badge.classes()).toContain('bg-green-100')
  })

  it('easy badge has dark mode class', () => {
    const wrapper = mountCard()
    const badge = wrapper.find('span.px-2')
    expect(badge.classes().some((c) => c.includes('dark:bg-green-900'))).toBe(true)
  })

  it('has cursor-pointer class', () => {
    const wrapper = mountCard()
    expect(wrapper.find('button').classes()).toContain('cursor-pointer')
  })

  it('has transition class for smooth hover animation', () => {
    const wrapper = mountCard()
    const btn = wrapper.find('button')
    expect(btn.classes().some((c) => c.startsWith('transition'))).toBe(true)
  })

  it('renders difficulty badge', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('簡單')
  })

  it('renders tags', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('classical')
  })

  // Completion badge (Requirement: Completion shown on catalogue)
  it('shows the completion badge when completed', () => {
    const wrapper = mount(ChallengeCard, {
      props: { challenge: mockChallenge, completed: true },
    })
    expect(wrapper.find('[data-testid="completion-badge"]').exists()).toBe(true)
  })

  it('hides the completion badge when not completed', () => {
    expect(mountCard().find('[data-testid="completion-badge"]').exists()).toBe(false)
  })
})
