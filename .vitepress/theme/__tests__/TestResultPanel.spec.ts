import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TestResultPanel from '../components/editor/TestResultPanel.vue'
import type { TestcaseResult } from '../workers/pyodide.worker'

function makeResult(verdict: string, overrides?: Partial<TestcaseResult>): TestcaseResult {
  return {
    type: 'testcase_result',
    index: 0,
    verdict: verdict as TestcaseResult['verdict'],
    elapsed_ms: 10,
    actual: 'X',
    expected: 'Y',
    error: '',
    ...overrides,
  }
}

describe('TestResultPanel', () => {
  it('renders AC row with a checkmark SVG', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [makeResult('AC')], status: 'done' },
    })
    const row = wrapper.find('tbody tr')
    expect(row.find('svg').exists()).toBe(true)
  })

  it('renders WA row with a failure SVG', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [makeResult('WA')], status: 'done' },
    })
    const row = wrapper.find('tbody tr')
    expect(row.find('svg').exists()).toBe(true)
  })

  it('shows nothing when results are empty and status is idle', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [], status: 'idle' },
    })
    expect(wrapper.find('table').exists()).toBe(false)
  })

  it('has light mode base border class (Requirement: TestResultPanel and RunButton apply dual-theme styles)', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [makeResult('AC')], status: 'done' },
    })
    const root = wrapper.find('[data-testid="result-panel"]')
    expect(root.classes()).toContain('border-slate-200')
  })

  it('has dark mode border class', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [makeResult('AC')], status: 'done' },
    })
    const root = wrapper.find('[data-testid="result-panel"]')
    expect(root.classes()).toContain('dark:border-gray-800')
  })

  it('does NOT have fixed max-h-56 class (Requirement: TestResultPanel removes fixed max-height)', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [makeResult('AC')], status: 'done' },
    })
    expect(wrapper.find('.max-h-56').exists()).toBe(false)
  })
})

describe('TestResultPanel verdictDetail display modes', () => {
  it('hidden mode: WA detail column shows no expected or actual', () => {
    const result = makeResult('WA', { actual: undefined, expected: undefined })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done', verdictDetail: 'hidden' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    expect(detailCell.text()).toBe('')
  })

  it('actual mode: WA detail column shows only actual output', () => {
    const result = makeResult('WA', { actual: 'HELLO', expected: undefined })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done', verdictDetail: 'actual' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    expect(detailCell.text()).toContain('HELLO')
    expect(detailCell.text()).not.toContain('預期')
  })

  it('full mode: WA detail column shows both expected and actual', () => {
    const result = makeResult('WA', { actual: 'HELLO', expected: 'KHOOR' })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done', verdictDetail: 'full' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    expect(detailCell.text()).toContain('預期')
    expect(detailCell.text()).toContain('KHOOR')
    expect(detailCell.text()).toContain('HELLO')
  })

  it('defaults to hidden when verdictDetail prop is omitted', () => {
    const result = makeResult('WA', { actual: 'HELLO', expected: 'KHOOR' })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    // Default hidden: no detail shown
    expect(detailCell.text()).toBe('')
  })

  it('AC verdict shows no detail regardless of verdictDetail mode', () => {
    const result = makeResult('AC', { actual: 'KHOOR', expected: 'KHOOR' })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done', verdictDetail: 'full' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    expect(detailCell.text()).toBe('')
  })

  it('RE verdict always shows error message regardless of verdictDetail', () => {
    const result = makeResult('RE', { error: 'NameError: x', actual: undefined, expected: undefined })
    const wrapper = mount(TestResultPanel, {
      props: { results: [result], status: 'done', verdictDetail: 'hidden' },
    })
    const detailCell = wrapper.findAll('td').at(3)!
    expect(detailCell.text()).toContain('NameError: x')
  })
})

describe('TestResultPanel — interrupted batch honesty', () => {
  // A cumulative-kill truncation used to render as "3 / 3 通過" with three
  // green rows, because the denominator was the number of REPORTED results.
  // The run had 20 testcases; 17 never reported.
  const reported = [makeResult('AC', { index: 0 }), makeResult('AC', { index: 1 }), makeResult('AC', { index: 2 })]

  it('renders one row per testcase of the challenge, not per reported result', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: reported, status: 'done', total: 20 },
    })
    expect(wrapper.findAll('tbody tr')).toHaveLength(20)
  })

  it('scores against the total testcase count', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: reported, status: 'done', total: 20 },
    })
    expect(wrapper.text()).toContain('3 / 20')
  })

  it('does not colour a truncated run as a full pass', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: reported, status: 'done', total: 20 },
    })
    const summary = wrapper.find('[data-testid="result-summary"]')
    expect(summary.classes().join(' ')).not.toContain('text-green')
  })

  it('marks never-reported testcases as not executed, visually distinct from a pass', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: reported, status: 'done', total: 20 },
    })
    const rows = wrapper.findAll('tbody tr')
    expect(rows[19]!.attributes('data-verdict')).toBe('none')
    expect(rows[0]!.attributes('data-verdict')).toBe('AC')
  })

  it('falls back to the reported count when total is not supplied', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: reported, status: 'done' },
    })
    expect(wrapper.findAll('tbody tr')).toHaveLength(3)
    expect(wrapper.text()).toContain('3 / 3')
  })
})

describe('TestResultPanel — truncated run still renders', () => {
  // The cumulative batch kill terminates the Worker mid-run. On the production
  // path the store can end up `done` with no results at all, and the panel's
  // root v-if used to unmount the whole table in exactly that state — so the
  // honest-denominator fix rendered nothing and the student saw only a score.
  it('renders the table when the run finished having reported nothing', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [], status: 'done', total: 20 },
    })
    expect(wrapper.find('[data-testid="result-panel"]').exists()).toBe(true)
    expect(wrapper.findAll('tbody tr')).toHaveLength(20)
    expect(wrapper.findAll('[data-verdict="none"]')).toHaveLength(20)
  })

  it('scores a fully truncated run against the real total', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [], status: 'done', total: 20 },
    })
    expect(wrapper.text()).toContain('0 / 20')
  })

  it('still stays hidden before a run has started', () => {
    const wrapper = mount(TestResultPanel, {
      props: { results: [], status: 'idle', total: 20 },
    })
    expect(wrapper.find('[data-testid="result-panel"]').exists()).toBe(false)
  })
})
