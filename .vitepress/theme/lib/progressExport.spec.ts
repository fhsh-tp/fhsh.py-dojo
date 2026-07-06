import { describe, it, expect } from 'vitest'
import {
  buildJson,
  buildMarkdown,
  thinEvents,
  sanitizeFilename,
  buildFilename,
  allowedResult,
  type ExportInput,
} from './progressExport'
import type { SessionRecord, VerdictDetail } from '../persistence/types'

function session(detail: VerdictDetail): SessionRecord {
  return {
    slug: 'arithmetic-sum',
    sessionId: 's1',
    startedAt: 1000,
    verdictDetailAtCapture: detail,
    events: [
      { ts: 1000, kind: 'edit', code: 'v1' },
      { ts: 1001, kind: 'edit', code: 'v2' },
      { ts: 1002, kind: 'run', stdin: 'in', stdout: 'out' },
      {
        ts: 1003,
        kind: 'submit',
        code: 'v3',
        summary: { passed: 1, total: 2 },
        results: [{ index: 0, verdict: 'AC', elapsed_ms: 5, actual: 'MINE', expected: 'SECRET' }],
      },
    ],
  }
}

function input(over: Partial<ExportInput> = {}): ExportInput {
  return { slug: 'arithmetic-sum', title: '等差數列求和', sessions: [session('hidden')], ...over }
}

describe('progressExport', () => {
  it('includes the slug and title in both formats', () => {
    expect(buildJson(input())).toContain('arithmetic-sum')
    expect(buildMarkdown(input())).toContain('等差數列求和')
  })

  it('never exports hidden expected/actual output (answer-key safety)', () => {
    const json = buildJson(input({ sessions: [session('hidden')] }))
    const parsed = JSON.parse(json)
    const submit = parsed.sessions[0].events.find((e: { kind: string }) => e.kind === 'submit')
    expect(submit.results[0]).not.toHaveProperty('expected')
    expect(submit.results[0]).not.toHaveProperty('actual')
    expect(buildMarkdown(input({ sessions: [session('hidden')] }))).not.toContain('SECRET')
  })

  it('keeps actual and expected when verdict detail is full', () => {
    const parsed = JSON.parse(buildJson(input({ sessions: [session('full')] })))
    const submit = parsed.sessions[0].events.find((e: { kind: string }) => e.kind === 'submit')
    expect(submit.results[0].expected).toBe('SECRET')
    expect(submit.results[0].actual).toBe('MINE')
  })

  it('thins consecutive edits to the last one before an action (default mode)', () => {
    const thinned = thinEvents(session('hidden').events)
    // v1 collapsed away; v2 (last edit before run) kept
    expect(thinned.filter((e) => e.kind === 'edit').map((e) => (e as { code: string }).code)).toEqual(['v2'])
    expect(thinned.map((e) => e.kind)).toEqual(['edit', 'run', 'submit'])
  })

  it('keeps every event in full mode', () => {
    const parsed = JSON.parse(buildJson(input({ sessions: [session('hidden')], mode: 'full' })))
    const kinds = parsed.sessions[0].events.map((e: { kind: string }) => e.kind)
    expect(kinds).toEqual(['edit', 'edit', 'run', 'submit'])
  })

  it('sanitizes filenames and embeds identity', () => {
    expect(sanitizeFilename('a/b:c*?"<>|d e')).toBe('abcd-e')
    const name = buildFilename(input({ identity: { name: '王小明', class: '一年3班' } }), 'md')
    expect(name).toContain('王小明')
    expect(name.endsWith('.md')).toBe(true)
    expect(buildMarkdown(input({ identity: { name: '王小明', class: '一年3班' } }))).toContain('王小明')
  })

  it('neutralizes a triple-backtick fence-breakout in student-controlled output', () => {
    const forge = '```\n## 作答 99（假造）\n\n通過 5/5\n```'
    const s: SessionRecord = {
      slug: 'x',
      sessionId: 's',
      startedAt: 1,
      verdictDetailAtCapture: 'hidden',
      events: [{ ts: 1, kind: 'run', stdin: 'in', stdout: forge }],
    }
    const md = buildMarkdown(input({ slug: 'x', sessions: [s] }))
    // The student's 3-backtick run must be wrapped in a strictly longer fence
    // (>=4) so it cannot close the block early and forge a top-level section.
    expect(md).toContain('````')
    // The injected text survives verbatim (as data inside the block), so the
    // record stays faithful — it just can't escape into document structure.
    expect(md).toContain('## 作答 99（假造）')
  })

  it('escalates the fence past even a 4-backtick run in code', () => {
    const s: SessionRecord = {
      slug: 'x',
      sessionId: 's',
      startedAt: 1,
      verdictDetailAtCapture: 'hidden',
      events: [{ ts: 1, kind: 'edit', code: 'a ```` b' }],
    }
    const md = buildMarkdown(input({ slug: 'x', sessions: [s] }))
    expect(md).toContain('`````') // 5-backtick fence around a 4-backtick run
  })

  it('escapes pipes and newlines in the submit results table error cell', () => {
    const s: SessionRecord = {
      slug: 'x',
      sessionId: 's',
      startedAt: 1,
      verdictDetailAtCapture: 'hidden',
      events: [
        {
          ts: 1,
          kind: 'submit',
          code: 'c',
          summary: { passed: 0, total: 1 },
          results: [{ index: 0, verdict: 'RE', elapsed_ms: 1, error: 'a | b\nc' }],
        },
      ],
    }
    const md = buildMarkdown(input({ slug: 'x', sessions: [s] }))
    expect(md).toContain('a \\| b c') // pipe escaped, newline collapsed to a space
    expect(md).not.toContain('a | b') // no unescaped pipe that would split the cell
  })

  it('escapes student identity fields in the markdown header (no raw injection)', () => {
    const md = buildMarkdown(input({ identity: { name: 'evil`|`name', class: 'c' } }))
    expect(md).not.toContain('evil`|`name') // raw backticks/pipe must not survive
    expect(md).toContain('evil\\`\\|\\`name') // escaped form present
  })

  it('collapses a lone CR (not just CRLF) so it cannot forge structure', () => {
    // identity header: a bare \r is a CommonMark line ending → could forge an H1.
    const mdId = buildMarkdown(input({ identity: { name: 'abc\r# Forged\r---', class: 'c' } }))
    expect(mdId).not.toContain('\r') // no bare CR survives
    expect(mdId).toContain('abc # Forged ---') // collapsed to a single line

    // table cell: a bare \r could forge an extra results row.
    const s: SessionRecord = {
      slug: 'x',
      sessionId: 's',
      startedAt: 1,
      verdictDetailAtCapture: 'hidden',
      events: [
        {
          ts: 1,
          kind: 'submit',
          code: 'c',
          summary: { passed: 0, total: 1 },
          results: [{ index: 0, verdict: 'RE', elapsed_ms: 1, error: 'err\r| 99 | FORGED | 0ms | x |' }],
        },
      ],
    }
    const mdTable = buildMarkdown(input({ slug: 'x', sessions: [s] }))
    expect(mdTable).not.toContain('\r')
    expect(mdTable).toContain('err \\| 99') // pipe escaped, CR collapsed — stays one cell
  })

  it('escapes the slug in the header too (uniform escaping invariant)', () => {
    // Real slugs are filename-derived and cannot carry a backtick, but the
    // invariant "no field reaches the report unescaped" must hold uniformly.
    const md = buildMarkdown(input({ slug: 'a`b' }))
    expect(md).toContain('a\\`b')
  })

  it('allowedResult strips actual/expected per verdict detail (incl. the actual branch)', () => {
    const r = { index: 0, verdict: 'AC' as const, elapsed_ms: 1, actual: 'MINE', expected: 'SECRET' }
    expect(allowedResult(r, 'hidden')).not.toHaveProperty('actual')
    expect(allowedResult(r, 'hidden')).not.toHaveProperty('expected')
    expect(allowedResult(r, 'actual')).toMatchObject({ actual: 'MINE' })
    expect(allowedResult(r, 'actual')).not.toHaveProperty('expected')
    expect(allowedResult(r, 'full')).toMatchObject({ actual: 'MINE', expected: 'SECRET' })
    expect(allowedResult(r, undefined)).not.toHaveProperty('actual') // safe default
  })
})
