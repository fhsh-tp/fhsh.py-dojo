// @vitest-environment node
/**
 * Challenge-page math notation gate.
 *
 * Every `docs/challenge/*.md` body MUST express mathematical statements as
 * LaTeX rather than as Unicode symbols or ASCII comparison sequences. A page
 * that regresses fails HERE, naming the file, the line, and the offending
 * token — instead of shipping a body where `1 ≤ n ≤ 1500` sits next to
 * `$1 \le n \le 1500$` on the neighbouring challenge.
 *
 * The blacklist lives in `scripts/latex-notation-rules.json` and is shared
 * with `scripts/latex-notation-survey.py`. Two readers, one rule file.
 *
 * Deliberately implemented natively in TypeScript rather than shelling out to
 * the Python surveyor: `content-regression.test.ts` skips itself when python3
 * is unavailable, and a gate whose whole value is "no silent pass" must not
 * inherit a skip path. Deliberately NO skip guards for the same reason — an
 * empty challenge directory is a failure, not a skip.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { describe, expect, it } from 'vitest'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')
const RULES_PATH = resolve(import.meta.dirname, 'latex-notation-rules.json')

interface RulePattern {
  name: string
  regex: string
  hint: string
}

interface Rules {
  tierA: { symbols: string[]; sequences: string[]; patterns?: RulePattern[] }
  tierB: { symbols: string[] }
  ignoreMarker: string
}

const rules: Rules = JSON.parse(readFileSync(RULES_PATH, 'utf-8'))
const TIER_A = [...rules.tierA.symbols, ...rules.tierA.sequences]
const TIER_B = rules.tierB.symbols
// Bare `<` / `>` cannot be listed as plain tokens: that would also flag HTML
// tags, blockquote markers and `-->`. Requiring an operand on both sides is
// what makes `付款 < 價格` catchable without those false positives. This gap
// is why `quadrant-classifier` was surveyed as "no math symbols" and its seven
// inequalities went unread by anyone.
const TIER_A_PATTERNS = (rules.tierA.patterns ?? []).map((p) => ({
  name: p.name,
  re: new RegExp(p.regex, 'gu'),
}))

export interface Violation {
  file: string
  line: number
  tier: 'A' | 'B' | '$'
  token: string
}

const FENCE_RE = /^[ \t]*```[\s\S]*?^[ \t]*```/gm
const IMAGE_RE = /!\[[^\]]*\]\([^)]*\)/g
const CODESPAN_RE = /(`+)(?:(?!\1)[\s\S])*?\1/g
// Autolinks `<https://…>` / `<a@b.c>` have the exact shape the bare-comparison
// pattern hunts for. No challenge body has one today; strip them anyway so a
// future link does not produce a notation violation nobody can parse.
const AUTOLINK_RE = /<[^>\s]+[:@][^>\s]*>/g
const DISPLAY_RE = /\$\$[\s\S]*?\$\$/g
// Inline math: the opening `$` is not followed by whitespace, the closing `$`
// is not preceded by whitespace, and neither crosses a newline. This is the
// markdown-it family's actual rule, and it is exactly why `movie-ticket`'s
// `$150 | … | $250` was never eaten — every one of those dollar signs has
// whitespace in front of it, so none of them is a legal closing delimiter.
const INLINE_RE = /\$(?!\s)(?:[^$\n\\]|\\.)*?(?<!\s)\$/g
const ESCAPED_DOLLAR = '\u0001ESCAPED_DOLLAR\u0001'

/** Replace a match with the same number of characters so line/column survive. */
function blankOut(text: string, re: RegExp): string {
  return text.replace(re, (m) => m.replace(/[^\n]/g, ' '))
}

/**
 * Split off the body and report the 1-based line number it starts on. A file
 * without frontmatter is treated as all body — never silently skipped, since
 * skipping would make a broken file look clean in the counts.
 */
export function splitBody(text: string): { body: string; startLine: number } {
  if (!text.startsWith('---\n')) return { body: text, startLine: 1 }
  const end = text.indexOf('\n---\n', 4)
  if (end === -1) return { body: text, startLine: 1 }
  const head = text.slice(0, end + 5)
  return { body: text.slice(end + 5), startLine: (head.match(/\n/g)?.length ?? 0) + 1 }
}

/**
 * Build the two scan surfaces. Order matters and is fixed:
 * body → strip fences → strip images → mask escaped `\$` → strip `$$…$$` →
 * strip `$…$`. Stripping math before fences would let a sample-output dollar
 * sign pair with a body formula and swallow a whole paragraph.
 */
function scanSurfaces(body: string): {
  withSpans: string
  withoutSpans: string
  bareDollar: number
} {
  let stage = blankOut(body, FENCE_RE)
  stage = blankOut(stage, IMAGE_RE)
  stage = blankOut(stage, AUTOLINK_RE)
  stage = stage.split('\\$').join(ESCAPED_DOLLAR)
  stage = blankOut(stage, DISPLAY_RE)
  stage = blankOut(stage, INLINE_RE)
  const bareDollar = (stage.match(/\$/g) ?? []).length
  const withSpans = stage.split(ESCAPED_DOLLAR).join('  ')
  return { withSpans, withoutSpans: blankOut(withSpans, CODESPAN_RE), bareDollar }
}

/** Escape-hatch: a marker comment exempts the next non-blank line. */
function ignoredLines(body: string, startLine: number): Set<number> {
  const out = new Set<number>()
  const lines = body.split('\n')
  lines.forEach((line, i) => {
    if (!line.includes(rules.ignoreMarker) || !line.includes('<!--')) return
    for (let j = i + 1; j < lines.length; j += 1) {
      if (lines[j]?.trim()) {
        out.add(startLine + j)
        return
      }
    }
  })
  return out
}

export function findViolations(file: string, text: string): Violation[] {
  const { body, startLine } = splitBody(text)
  const { withSpans, withoutSpans, bareDollar } = scanSurfaces(body)
  const skip = ignoredLines(body, startLine)
  const hits: Violation[] = []

  const sweep = (surface: string, tokens: string[], tier: 'A' | 'B') => {
    surface.split('\n').forEach((line, i) => {
      const lineNo = startLine + i
      if (skip.has(lineNo)) return
      for (const token of tokens) {
        let from = 0
        for (;;) {
          const at = line.indexOf(token, from)
          if (at === -1) break
          hits.push({ file, line: lineNo, tier, token })
          from = at + token.length
        }
      }
    })
  }

  sweep(withSpans, TIER_A, 'A')
  withSpans.split('\n').forEach((line, i) => {
    const lineNo = startLine + i
    if (skip.has(lineNo)) return
    for (const p of TIER_A_PATTERNS) {
      p.re.lastIndex = 0
      for (const m of line.matchAll(p.re))
        hits.push({ file, line: lineNo, tier: 'A', token: m[0].trim() })
    }
  })
  sweep(withoutSpans, TIER_B, 'B')

  if (bareDollar > 0) {
    // Locate them so the message can point at a line rather than just a count.
    withSpans.split('\n').forEach((line, i) => {
      const lineNo = startLine + i
      if (skip.has(lineNo)) return
      for (let at = line.indexOf('$'); at !== -1; at = line.indexOf('$', at + 1)) {
        hits.push({ file, line: lineNo, tier: '$', token: '$' })
      }
    })
  }

  return hits.sort((a, b) => a.line - b.line || a.tier.localeCompare(b.tier))
}

/**
 * Commands MathJax renders and this project actually uses. An unknown command
 * renders as raw source in the student's face, so an unrecognised one is a
 * failure rather than a warning — extend this list deliberately when a new
 * command is genuinely needed.
 */
const KNOWN_COMMANDS = new Set([
  'le',
  'ge',
  'lt',
  'gt',
  'ne',
  'neq',
  'leq',
  'geq',
  'approx',
  'times',
  'cdot',
  'cdots',
  'dots',
  'ldots',
  'div',
  'pm',
  'mp',
  'sum',
  'prod',
  'int',
  'frac',
  'dfrac',
  'sqrt',
  'lfloor',
  'rfloor',
  'lceil',
  'rceil',
  'text',
  'bmod',
  'pmod',
  'log',
  'max',
  'min',
  'quad',
  'qquad',
])

export interface SyntaxProblem {
  file: string
  kind: string
  detail: string
}

/**
 * Catch formulas that are syntactically broken. The gate above proves the page
 * stopped using Unicode symbols; this proves what replaced them actually
 * renders. A malformed formula fails silently in Markdown — the reader just
 * sees `$2^{D-1$` — so nothing but an explicit check finds it.
 */
export function findSyntaxProblems(file: string, text: string): SyntaxProblem[] {
  const { body } = splitBody(text)
  const scan = blankOut(blankOut(body, FENCE_RE), IMAGE_RE).split('\\$').join('')
  const problems: SyntaxProblem[] = []
  const add = (kind: string, detail: string) => problems.push({ file, kind, detail })

  // Dollar signs must pair up line by line, once display math is set aside.
  blankOut(scan, DISPLAY_RE)
    .split('\n')
    .forEach((line, i) => {
      if ((line.match(/\$/g) ?? []).length % 2 === 1) {
        add('錢字號奇數個', `第 ${i + 1} 行（相對內文）：${line.trim().slice(0, 70)}`)
      }
    })

  for (const formula of scan.match(INLINE_RE) ?? []) {
    const inner = formula.slice(1, -1)
    if (/[≤≥＜＞×−·²³⁴]/.test(inner)) add('公式內殘留 Unicode 記號', formula)
    if (/[一-鿿]/.test(inner)) add('公式內有中文', formula)
    if ((inner.match(/\{/g) ?? []).length !== (inner.match(/\}/g) ?? []).length) {
      add('大括號不配對', formula)
    }
    for (const [, cmd] of inner.matchAll(/\\([a-zA-Z]+)/g)) {
      if (cmd && !KNOWN_COMMANDS.has(cmd)) add(`未知指令 \\${cmd}`, formula)
    }
    // `$2^10$` renders as 2¹·0, not 2¹⁰ — the exponent must be braced.
    if (/\^[0-9A-Za-z]{2,}/.test(inner)) add('指數沒加大括號', formula)
    if (/_[0-9A-Za-z]{2,}/.test(inner)) add('下標沒加大括號', formula)
  }

  if (scan.includes('\\text{'))
    add('公式含 \\text{', 'MathJax 的 CJK 字重與內文不同，中文請留在公式外')
  return problems
}

function describeViolation(v: Violation): string {
  if (v.tier === '$') {
    return `docs/challenge/${v.file}:${v.line} 出現未跳脫的錢字號 "$"，貨幣請寫成 \\$（見 Usage.md 記號分類表）`
  }
  return `docs/challenge/${v.file}:${v.line} 出現 ${v.tier} 級記號 "${v.token}"，請改寫成 LaTeX（見 Usage.md 記號分類表）`
}

describe('challenge math notation', () => {
  const files = readdirSync(CHALLENGES_DIR).filter((f) => f.endsWith('.md'))

  it('finds challenge pages to check', () => {
    // An empty directory would make every other assertion below vacuously
    // true. Fail loudly instead.
    expect(files.length).toBeGreaterThan(0)
  })

  it('every challenge body uses LaTeX for math statements', () => {
    const all: Violation[] = []
    for (const file of files) {
      all.push(...findViolations(file, readFileSync(join(CHALLENGES_DIR, file), 'utf-8')))
    }
    // Report EVERY violation, not just the first — whoever fixes these needs
    // the complete list, and a per-file failure would hide files 2..n.
    const byFile = new Set(all.map((v) => v.file))
    const report = [
      `${all.length} 處違規，散布於 ${byFile.size} 個檔案：`,
      ...all.map(describeViolation),
    ].join('\n')
    expect(all.length, report).toBe(0)
  })

  it('every formula is syntactically renderable', () => {
    const all: SyntaxProblem[] = []
    for (const file of files) {
      all.push(...findSyntaxProblems(file, readFileSync(join(CHALLENGES_DIR, file), 'utf-8')))
    }
    const report = [
      `${all.length} 個公式語法問題：`,
      ...all.map((p) => `docs/challenge/${p.file} — ${p.kind}：${p.detail}`),
    ].join('\n')
    expect(all.length, report).toBe(0)
  })
})

describe('the notation gate itself', () => {
  // Negative controls. A gate without them is not a check: each case below
  // proves the scanner FIRES on the dirty input, and the clean twin proves it
  // does not fire on the legitimate one.
  const fm = '---\nid: x\n---\n'
  const scan = (body: string) => findViolations('fixture.md', fm + body)
  const tokens = (body: string) => scan(body).map((v) => v.token)

  it('catches a tier A symbol in prose', () => {
    expect(tokens('約束是 1 ≤ n ≤ 10。')).toEqual(['≤', '≤'])
  })

  it('catches a tier A sequence even inside an inline code span', () => {
    // This is the `ap-layout-plan` / `marquee-display-count` case: a real
    // constraint wrongly wrapped in backticks. Exempting code spans would
    // let all seven of those slip through.
    expect(tokens('約束 `1 <= n <= 10`。')).toEqual(['<=', '<='])
  })

  it('catches a bare comparison operator between two operands', () => {
    // The gap that let `quadrant-classifier` be surveyed as "no math symbols":
    // seven inequalities written with bare `<` / `>`, so nobody ever read it.
    expect(tokens('若 x > 0 且 y < 0 則在第四象限。')).toEqual(['>', '<'])
  })

  it('catches a bare comparison with Chinese operands', () => {
    expect(tokens('當 付款 < 價格 時退回。')).toEqual(['<'])
  })

  it('catches `!=`', () => {
    expect(tokens('若 `a != b` 則不同。')).toEqual(['!='])
  })

  it('does not flag a markdown blockquote, an HTML comment, or an autolink', () => {
    // These are why `<` and `>` cannot simply be listed as tier A tokens.
    expect(tokens('> 這是引言區塊')).toEqual([])
    expect(tokens('<!-- 一則註解 -->')).toEqual([])
    expect(tokens('詳見 <https://example.com/a> 說明')).toEqual([])
  })

  it('does not flag a comparison already wrapped in LaTeX', () => {
    expect(tokens('若 $x > 0$ 且 $y < 0$ 則在第四象限。')).toEqual([])
  })

  it('catches a tier B symbol in prose', () => {
    expect(tokens('面積是 k × k。')).toEqual(['×'])
  })

  it('exempts a tier B symbol inside an inline code span', () => {
    // `print-farm-schedule` refers to the Gantt chart's idle glyph this way.
    expect(tokens('圖上的 `·` 表示閒置。')).toEqual([])
  })

  it('accepts a converted statement', () => {
    expect(tokens('約束是 $1 \\le n \\le 10$。')).toEqual([])
  })

  it('does not scan fenced code blocks', () => {
    expect(tokens('```\n1 <= n\n```\n')).toEqual([])
  })

  it('does not scan image alt text', () => {
    expect(tokens('![圖 1：`n <= 5` 的樣子](/a.png)')).toEqual([])
  })

  it('honours the ignore marker for exactly one line', () => {
    const body = '<!-- latex-lint-ignore-next-line -->\n`x <= 3`\n`y >= 4`'
    expect(tokens(body)).toEqual(['>='])
  })

  it('reports the line number from the original file, not the scan surface', () => {
    const hits = scan('第一段沒問題。\n\n這裡有 1 ≤ n。')
    expect(hits[0]?.line).toBe(6)
  })

  it('catches an unescaped currency dollar sign', () => {
    expect(tokens('票價 $150 元。')).toEqual(['$'])
  })

  it('accepts an escaped currency dollar sign', () => {
    expect(tokens('票價 \\$150 元。')).toEqual([])
  })

  it('treats a file without frontmatter as all body', () => {
    expect(findViolations('naked.md', '直接就是內文，1 ≤ n。').length).toBe(1)
  })

  // Syntax checks get the same treatment: every rule proves it fires on the
  // broken form and stays quiet on the correct one.
  const syntax = (body: string) => findSyntaxProblems('fixture.md', fm + body).map((p) => p.kind)

  it('accepts a well-formed formula', () => {
    expect(syntax('約束是 $1 \\le n \\le 10^6$，其中 $2^{D-1}$ 個袋子。')).toEqual([])
  })

  it('catches an odd number of dollar signs on a line', () => {
    expect(syntax('約束是 $1 \\le n。')).toEqual(['錢字號奇數個'])
  })

  it('catches an unbraced multi-character exponent', () => {
    // `$2^10$` renders as 2¹·0, which is a different number.
    expect(syntax('共有 $2^10$ 個。')).toEqual(['指數沒加大括號'])
  })

  it('catches an unbalanced brace', () => {
    expect(syntax('共有 $2^{D-1$ 個。')).toContain('大括號不配對')
  })

  it('catches an unknown command', () => {
    expect(syntax('約束是 $1 \\lte n$。')).toContain('未知指令 \\lte')
  })

  it('catches Chinese inside a formula', () => {
    expect(syntax('$1 \\le 座號 \\le 999$')).toContain('公式內有中文')
  })

  it('accepts Chinese kept outside the formula', () => {
    expect(syntax('座號 $1 \\le$ 座號 $\\le 999$')).toEqual([])
  })

  it('catches \\text{} wrapping', () => {
    expect(syntax('$\\text{BMI}$')).toContain('公式含 \\text{')
  })

  it('does not scan fenced code blocks for syntax', () => {
    expect(syntax('```\n$2^10$\n```\n')).toEqual([])
  })
})
