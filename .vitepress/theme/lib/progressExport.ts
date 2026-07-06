/**
 * Serialize a challenge's recorded work sessions into a student-downloadable
 * report — Markdown (for pasting to an LLM) and JSON (machine-aggregable).
 *
 * Answer-key safety: results are re-filtered by the verdict-detail level
 * captured with each session, so hidden expected outputs are never emitted even
 * if an upstream regression started including them. Only fields already present
 * in the stored snapshot are serialized.
 */
import type {
  SessionRecord,
  SessionEvent,
  SubmitEvent,
  SubmitTestcaseResult,
  VerdictDetail,
} from '../persistence/types'

export interface ExportIdentity {
  name?: string
  class?: string
}

export interface ExportInput {
  slug: string
  title: string
  difficulty?: string
  sessions: SessionRecord[]
  identity?: ExportIdentity
  /** 'thinned' (default) collapses intermediate micro-edits; 'full' keeps all. */
  mode?: 'thinned' | 'full'
}

const LLM_PREAMBLE =
  '以下是我在這題的作答歷程（依時間排序：edit＝編輯快照、run＝自己執行、submit＝提交判題）。' +
  '請幫我分析我卡在哪、有哪些盲點或誤解，並給我下一步的提示（先不要直接給完整答案）。'

// ── answer-key-safe filtering ───────────────────────────────────────────────

export function allowedResult(r: SubmitTestcaseResult, detail: VerdictDetail | undefined): SubmitTestcaseResult {
  const base: SubmitTestcaseResult = {
    index: r.index,
    verdict: r.verdict,
    elapsed_ms: r.elapsed_ms,
    error: r.error,
  }
  if (detail === 'full') return { ...base, actual: r.actual, expected: r.expected }
  if (detail === 'actual') return { ...base, actual: r.actual }
  return base // hidden / undefined: neither actual nor expected
}

function safeSession(s: SessionRecord): SessionRecord {
  return {
    ...s,
    events: s.events.map((e) =>
      e.kind === 'submit'
        ? ({ ...e, results: e.results.map((r) => allowedResult(r, s.verdictDetailAtCapture)) } as SubmitEvent)
        : e,
    ),
  }
}

// ── thinning ────────────────────────────────────────────────────────────────

/**
 * Collapse runs of consecutive edit events down to only the last edit before
 * each run/submit (and before the end). Run and submit events are always kept.
 */
export function thinEvents(events: SessionEvent[]): SessionEvent[] {
  const out: SessionEvent[] = []
  let pendingEdit: SessionEvent | null = null
  for (const e of events) {
    if (e.kind === 'edit') {
      pendingEdit = e // keep only the latest edit in a burst
    } else {
      if (pendingEdit) {
        out.push(pendingEdit)
        pendingEdit = null
      }
      out.push(e)
    }
  }
  if (pendingEdit) out.push(pendingEdit)
  return out
}

function prepareSessions(input: ExportInput): SessionRecord[] {
  const thinned = input.mode !== 'full'
  return input.sessions.map((s) => {
    const safe = safeSession(s)
    return thinned ? { ...safe, events: thinEvents(safe.events) } : safe
  })
}

// ── filename ────────────────────────────────────────────────────────────────

/** Remove characters invalid in filenames across common OSes. */
export function sanitizeFilename(name: string): string {
  return name
    .replace(/[/\\:*?"<>|]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

export function buildFilename(input: ExportInput, ext: 'md' | 'json'): string {
  const parts = [sanitizeFilename(input.title || input.slug)]
  if (input.identity?.name) parts.push(sanitizeFilename(input.identity.name))
  if (input.identity?.class) parts.push(sanitizeFilename(input.identity.class))
  return `${parts.filter(Boolean).join('-') || 'record'}.${ext}`
}

// ── JSON ────────────────────────────────────────────────────────────────────

export function buildJson(input: ExportInput): string {
  const payload = {
    slug: input.slug,
    title: input.title,
    difficulty: input.difficulty,
    identity: input.identity,
    mode: input.mode ?? 'thinned',
    sessions: prepareSessions(input),
  }
  return JSON.stringify(payload, null, 2)
}

// ── Markdown-safe interpolation ─────────────────────────────────────────────

/**
 * Wrap arbitrary (student-controlled) text in a fenced code block whose fence is
 * strictly longer than any backtick run inside the content, per CommonMark's
 * variable-length-fence rule. `stdout`/`error`/`code` come from a full Python
 * REPL and are 100% attacker-controlled; without this a student could emit
 * ``` to close the fence early and forge document structure (e.g. a fake
 * "通過 5/5" submission) or break out into raw HTML in a permissive renderer.
 */
function codeBlock(content: string, lang = ''): string {
  const longestRun = (content.match(/`+/g) ?? []).reduce((m, r) => Math.max(m, r.length), 0)
  const fence = '`'.repeat(Math.max(3, longestRun + 1))
  return `${fence}${lang}\n${content}\n${fence}`
}

/** Escape a value for one Markdown table cell (pipes split cells, newlines break the row). */
function tableCell(s: string): string {
  // `[\r\n]+` (not `\r?\n`): CommonMark treats a lone CR as a line ending too,
  // so a bare `\r` must also be collapsed or it could forge an extra table row.
  return s.replace(/\\/g, '\\\\').replace(/\|/g, '\\|').replace(/[\r\n]+/g, ' ')
}

/**
 * Escape a value for safe inline Markdown (student identity fields in the
 * header). Collapses newlines and backslash-escapes the structural characters
 * (`\` `` ` `` `|`) so a crafted name/class cannot forge structure or inject
 * into the LLM-bound report — the same uniform escaping story as the event body.
 */
function inlineText(s: string): string {
  // `[\r\n]+` (not `\r?\n`): a lone CR is a CommonMark line ending too, so it
  // must be collapsed or a crafted name could break out of the header line.
  return s.replace(/[\r\n]+/g, ' ').replace(/([\\`|])/g, '\\$1')
}

// ── Markdown ────────────────────────────────────────────────────────────────

function renderEvent(e: SessionEvent): string {
  const ts = new Date(e.ts).toISOString()
  if (e.kind === 'edit') {
    return `#### ✏️ 編輯 · ${ts}\n\n${codeBlock(e.code, 'python')}\n`
  }
  if (e.kind === 'run') {
    const err = e.error ? `\n**錯誤：**\n\n${codeBlock(e.error)}\n` : ''
    return `#### ▶️ 執行 · ${ts}\n\n**輸入：**\n\n${codeBlock(e.stdin)}\n\n**輸出：**\n\n${codeBlock(e.stdout)}\n${err}`
  }
  // submit
  const rows = e.results
    .map((r) => `| ${r.index} | ${r.verdict} | ${r.elapsed_ms.toFixed(0)}ms | ${tableCell(r.error ?? '')} |`)
    .join('\n')
  return (
    `#### ✅ 提交 · ${ts} · 通過 ${e.summary.passed}/${e.summary.total}\n\n` +
    `${codeBlock(e.code, 'python')}\n\n` +
    `| # | 判定 | 耗時 | 錯誤 |\n|---|---|---|---|\n${rows}\n`
  )
}

export function buildMarkdown(input: ExportInput): string {
  const sessions = prepareSessions(input)
  const header = [
    `# 作答歷程：${input.title}`,
    '',
    input.identity?.name || input.identity?.class
      ? `> 學生：${inlineText(input.identity?.name ?? '')}\u3000${inlineText(input.identity?.class ?? '')}`.trim()
      : null,
    `> 題目 slug：\`${inlineText(input.slug)}\`${input.difficulty ? `\u3000難度：${input.difficulty}` : ''}`,
    '',
    '---',
    '',
    LLM_PREAMBLE,
    '',
    '---',
    '',
  ]
    .filter((l) => l !== null)
    .join('\n')

  const body = sessions
    .map((s, i) => {
      const events = s.events.map(renderEvent).join('\n')
      return `## 作答 ${i + 1}（${new Date(s.startedAt).toISOString()}）\n\n${events}`
    })
    .join('\n\n')

  return `${header}\n${body}\n`
}
