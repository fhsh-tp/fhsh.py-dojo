#!/usr/bin/env npx tsx
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  CHALLENGE_ID_PATTERN,
  CATEGORY_ID_PREFIX,
  challengeIdOrdinal,
  extractFrontmatterId,
} from '../docs/shared/challenge-id.js'

// ── Pure helpers ──────────────────────────────────────────────────────────

export function toTitleCase(kebab: string): string {
  return kebab
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

export function toAlgorithmName(kebab: string): string {
  return kebab.replace(/-/g, '_')
}

export function validateName(name: string): string | null {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name)) {
    return `[new-challenge] ERROR: <name> must be kebab-case (lowercase letters, digits, hyphens only)`
  }
  // An id-shaped slug (e.g. py001) would blur the catalogue identity: its
  // /challenge/ page and the /c/ alias could name two different challenges.
  // generate-redirects fails the build on this too; rejecting it here stops
  // the file from being scaffolded in the first place.
  if (CHALLENGE_ID_PATTERN.test(name)) {
    return `[new-challenge] ERROR: <name> must not be id-shaped (like py001); an id-shaped slug would blur the catalogue identity (its /challenge/ page and the /c/ alias could name different challenges)`
  }
  return null
}

export function validateDifficulty(difficulty: string): string | null {
  if (!['easy', 'medium', 'hard'].includes(difficulty)) {
    return `[new-challenge] ERROR: --difficulty must be one of: easy, medium, hard`
  }
  return null
}

/**
 * Implemented exercise types accepted by the scaffold in this version.
 *
 * The full extensible taxonomy also registers `fill_in_blank` and `gamified`
 * (deferred to a future version) and `guided` (future placeholder, design
 * pending). Those values are documented in the `challenge-exercise-type` spec
 * and the challenge-author skill but are intentionally NOT accepted here until
 * they have templates, so an unknown type fails loudly rather than producing a
 * half-implemented challenge.
 */
export const EXERCISE_TYPES = ['basic', 'competition'] as const
export type ExerciseType = (typeof EXERCISE_TYPES)[number]

export function validateType(type: string): string | null {
  if (!(EXERCISE_TYPES as readonly string[]).includes(type)) {
    return `[new-challenge] ERROR: --type must be one of: ${EXERCISE_TYPES.join(', ')}`
  }
  return null
}

/**
 * Challenge categories accepted by the scaffold.
 *
 * `docs/shared/challenge-category.ts` is the data-layer single source of truth;
 * this file keeps its own copy of the list for build-time scaffolding, and
 * `scripts/new-challenge.test.ts` asserts the two stay in lockstep.
 */
export const CHALLENGE_CATEGORIES = ['python', 'apcs'] as const
export type ChallengeCategory = (typeof CHALLENGE_CATEGORIES)[number]

export function isChallengeCategory(v: string): v is ChallengeCategory {
  return (CHALLENGE_CATEGORIES as readonly string[]).includes(v)
}

export function validateCategory(category: string): string | null {
  if (!isChallengeCategory(category)) {
    return `[new-challenge] ERROR: --category must be one of: ${CHALLENGE_CATEGORIES.join(', ')}`
  }
  return null
}

export interface ParsedArgs {
  name: string
  title: string
  difficulty: string
  algorithm: string
  type: string
  category: string
}

export function parseArgs(argv: string[]): ParsedArgs | null {
  const args = argv.slice(2)
  let name = ''
  let title: string | null = null
  let difficulty = 'easy'
  let algorithm: string | null = null
  let type = 'basic'
  let category = 'python'

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!
    // Support both `--flag value` and `--flag=value`; without the `=` split an
    // inline value (e.g. `--type=competition`) would be silently dropped and the
    // flag's default kept — a footgun for a field that must reject unknown values.
    let flag = arg
    let inlineVal: string | null = null
    if (arg.startsWith('--') && arg.includes('=')) {
      const eq = arg.indexOf('=')
      flag = arg.slice(0, eq)
      inlineVal = arg.slice(eq + 1)
    }
    const takeValue = (): string | null => {
      if (inlineVal !== null) return inlineVal
      const next = i + 1 < args.length ? args[i + 1]! : null
      // An adjacent `--flag` is never a value: consuming it would silently
      // swallow the flag (`--title --category apcs` → title '--category').
      // Leave it unconsumed so it is parsed as its own flag; the current flag
      // falls back to its default or sentinel. Use `--flag=value` to pass a
      // literal leading-dash value.
      if (next === null || next.startsWith('--')) return null
      return args[++i]!
    }

    if (flag === '--title') {
      const v = takeValue()
      if (v !== null) title = v
    } else if (flag === '--difficulty') {
      // Validated flags treat a trailing flag with no value as an error, not a
      // silent default: the sentinel fails the flag's own validator, which
      // prints the documented "must be one of" message and exits non-zero.
      // (`--title`/`--algorithm` keep their documented default fallback.)
      difficulty = takeValue() ?? '<missing>'
    } else if (flag === '--algorithm') {
      const v = takeValue()
      if (v !== null) algorithm = v
    } else if (flag === '--type') {
      type = takeValue() ?? '<missing>'
    } else if (flag === '--category') {
      category = takeValue() ?? '<missing>'
    } else if (!arg.startsWith('--')) {
      name = arg
    }
  }

  if (!name) return null

  return {
    name,
    title: title ?? toTitleCase(name),
    difficulty,
    algorithm: algorithm ?? toAlgorithmName(name),
    type,
    category,
  }
}

export interface ChallengeFile {
  name: string
  content: string
}

/**
 * Next id for a category prefix: max existing ordinal within that prefix + 1,
 * zero-padded to 3 digits. Fails loudly (naming the file) on a missing or
 * malformed id — a silently skipped file would corrupt the numbering, the
 * exact failure mode the old integer regex had after the string-id migration.
 */
export function computeNextId(files: ChallengeFile[], prefix: string): string {
  let maxOrdinal = 0
  for (const { name, content } of files) {
    // Scoped to the frontmatter block, so an `id:` line in body text or a
    // fenced code block can never be picked up.
    const id = extractFrontmatterId(content)
    if (id === null) {
      throw new Error(
        `[new-challenge] ERROR: ${name} has no id line; fix the file before scaffolding.`,
      )
    }
    if (!CHALLENGE_ID_PATTERN.test(id)) {
      throw new Error(
        `[new-challenge] ERROR: ${name} has id '${id}' which does not match the challenge id format (e.g. py001); fix the file before scaffolding.`,
      )
    }
    if (id.startsWith(prefix) && /^\d/.test(id.slice(prefix.length))) {
      const ordinal = challengeIdOrdinal(id)
      if (ordinal > maxOrdinal) maxOrdinal = ordinal
    }
  }
  const next = `${prefix}${String(maxOrdinal + 1).padStart(3, '0')}`
  // Output-side guard: closes both silent-invalid paths at once — an
  // unregistered/undefined prefix ("undefined001") and prefix exhaustion past
  // 999 ("py1000"). Without this the bad id is written to disk and only
  // explodes later in build:redirects or the ledger gate.
  if (!CHALLENGE_ID_PATTERN.test(next)) {
    throw new Error(
      `[new-challenge] ERROR: computed next id '${next}' does not match the challenge id format; the '${prefix}' prefix is invalid or its 999-ordinal capacity is exhausted.`,
    )
  }
  return next
}

export interface RetiredLedger {
  slugs: string[]
  ids: string[]
}

/** Same "refusing to scaffold" contract as the corrupt-JSON path below. */
function ledgerError(path: string, detail: string): Error {
  return new Error(
    `[new-challenge] retired ledger at ${path} ${detail}; refusing to scaffold. ` +
      `Fix the file to re-enable the retired-slug/id reuse guard.`,
  )
}

function readLedgerField(
  path: string,
  raw: Record<string, unknown>,
  field: 'slugs' | 'ids',
  isValid: (v: string) => boolean,
  expected: string,
): string[] {
  const value = raw[field]
  // An ABSENT field is legitimate (nothing retired yet) and defaults to [].
  // A field that is PRESENT but not an array is not: silently defaulting it
  // to [] is the same disarmed guard this function exists to prevent.
  if (value === undefined) return []
  if (!Array.isArray(value)) {
    throw ledgerError(path, `has a "${field}" field that is present but not an array`)
  }
  const out: string[] = []
  for (let i = 0; i < value.length; i++) {
    const entry: unknown = value[i]
    if (typeof entry !== 'string' || !isValid(entry)) {
      throw ledgerError(
        path,
        `has an invalid "${field}"[${i}] entry ${JSON.stringify(entry)}; expected ${expected}`,
      )
    }
    out.push(entry)
  }
  return out
}

/**
 * Read the retired ledger, failing closed on anything it cannot trust.
 *
 * The guard is only as strong as the parse. `JSON.parse` returns `any`, so a
 * ledger carrying pre-migration entries (`"ids": [59]`, `"59"`, `"PY059"`) or
 * a non-array field (`"ids": "py059"`) used to sail through an
 * `Array.isArray` check and then never match `includes` — turning BOTH the
 * scaffold guard and the content-regression assertion into silent no-ops at
 * once. Every layer is therefore checked: root object, field container,
 * element type, element format.
 *
 * Unknown keys (`_comment`) are ignored by design — the ledger is
 * hand-edited. This is the single choke point: any future reader of the
 * ledger JSON must go through here rather than parsing the file itself.
 */
export function loadRetiredLedger(path: string): RetiredLedger {
  if (!existsSync(path)) return { slugs: [], ids: [] }
  let raw: unknown
  try {
    raw = JSON.parse(readFileSync(path, 'utf-8'))
  } catch (err) {
    // Fail closed: a corrupt ledger must NOT silently disable the reuse guard.
    throw new Error(
      `[new-challenge] retired ledger at ${path} is not valid JSON; refusing to scaffold. ` +
        `Fix the file to re-enable the retired-slug/id reuse guard. ` +
        `(${err instanceof Error ? err.message : String(err)})`,
    )
  }
  if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) {
    // Without this, a `null` root threw a bare TypeError ("Cannot read
    // properties of null") that told the author nothing actionable.
    throw ledgerError(path, 'is not a JSON object')
  }
  const obj = raw as Record<string, unknown>
  return {
    // Retired slugs are HISTORICAL records: validated as non-empty strings
    // only, deliberately NOT against SLUG_PATTERN. Tightening the live slug
    // contract must never retroactively brick the scaffold on an entry that
    // was correct when it was retired.
    slugs: readLedgerField(path, obj, 'slugs', (s) => s.length > 0, 'a non-empty slug string'),
    // Ids ARE format-checked, because the failure this guards against is
    // exactly a `59` / `"59"` / `"PY059"` entry that `includes` can never
    // match. This is not a new class of risk: computeNextId and
    // buildRedirects already refuse any id outside CHALLENGE_ID_PATTERN.
    ids: readLedgerField(
      path,
      obj,
      'ids',
      (s) => CHALLENGE_ID_PATTERN.test(s),
      'a challenge id string like "py059" (NOT a number)',
    ),
  }
}

/**
 * Reject reuse of a retired slug or id. Local student progress is keyed by
 * slug; a reused slug would silently inherit a former challenge's stored
 * progress, and a reused id would revive a retired catalogue identity.
 */
export function checkRetired(name: string, id: string, ledger: RetiredLedger): string | null {
  if (ledger.slugs.includes(name)) {
    return `[new-challenge] ERROR: slug '${name}' is retired; reusing it would inherit a former challenge's stored progress. Choose a different name.`
  }
  if (ledger.ids.includes(id)) {
    return `[new-challenge] ERROR: id ${id} is retired; reusing it would revive a retired catalogue identity and its /c/<id> alias.`
  }
  return null
}

export interface BuildContentOptions {
  id: string
  name: string
  title: string
  difficulty: string
  algorithm: string
  type: string
  category: string
}

export function buildContent({
  id,
  title,
  difficulty,
  algorithm,
  type,
  category,
}: BuildContentOptions): string {
  return `---
layout: challenge
id: ${id}
title: ${title}
difficulty: ${difficulty}
category: ${category}
type: ${type}
tags: []
algorithm: ${algorithm}
testcase_count: 5
# editor_capture_debounce_ms（選填）：卡關紀錄捕捉 editor 編輯快照的 debounce 間隔（毫秒）。
# 全域預設 1000，可逐題覆寫（有效範圍 100–10000，非整數或超界值回退預設）。取消下列註解即可調整：
# editor_capture_debounce_ms: 1000
params:
  n:
    type: int
    min: 1
    max: 10
generator: |
  n = int(input())
  print(n)
# reference_solution（選填）：一段獨立於 generator 的正確 Python 解法，供內容層
# 回歸測試（scripts/content-regression.test.ts）驗證「正解對正式加密池能得 AC」。
# 建議與 generator 用不同寫法，才能同時抓出 generator 與正解各自的錯誤。取消下列註解即可啟用：
# reference_solution: |
#   n = int(input())
#   print(n)
starter_code: |
  def solve():
      # 在此實作你的解法
      pass

  n = int(input())
  print(solve())
---

## ${title}

簡短說明此演算法的用途與背景。

### 演算法說明

說明演算法的操作步驟。

### 輸入說明

- 第一行：\`n\`，整數 1~10

### 輸出說明

- 輸出一行結果

### 範例

**輸入：**

\`\`\`
5
\`\`\`

**輸出：**

\`\`\`
5
\`\`\`
`
}

// ── Main (side-effects) ───────────────────────────────────────────────────

function main(): void {
  const parsed = parseArgs(process.argv)

  if (!parsed) {
    console.error(
      'Usage: pnpm new-challenge <name> [--title <title>] [--difficulty easy|medium|hard] [--category python|apcs] [--type basic|competition] [--algorithm <algorithm>]',
    )
    process.exit(1)
  }

  const { name, title, difficulty, algorithm, type, category } = parsed

  const nameError = validateName(name)
  if (nameError) {
    console.error(nameError)
    process.exit(1)
  }

  const difficultyError = validateDifficulty(difficulty)
  if (difficultyError) {
    console.error(difficultyError)
    process.exit(1)
  }

  const typeError = validateType(type)
  if (typeError) {
    console.error(typeError)
    process.exit(1)
  }

  const categoryError = validateCategory(category)
  if (categoryError) {
    console.error(categoryError)
    process.exit(1)
  }

  const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
  const challengeDir = join(projectRoot, 'docs', 'challenge')
  const outPath = join(challengeDir, `${name}.md`)

  if (existsSync(outPath)) {
    console.error(
      `[new-challenge] ERROR: docs/challenge/${name}.md already exists. Aborting to prevent overwrite.`,
    )
    process.exit(1)
  }

  let challengeFiles: ChallengeFile[] = []
  if (existsSync(challengeDir)) {
    challengeFiles = readdirSync(challengeDir)
      .filter((f) => f.endsWith('.md'))
      .map((f) => ({ name: f, content: readFileSync(join(challengeDir, f), 'utf-8') }))
  }
  const prefix = CATEGORY_ID_PREFIX[category as keyof typeof CATEGORY_ID_PREFIX]
  let id: string
  try {
    id = computeNextId(challengeFiles, prefix)
  } catch (err) {
    console.error(err instanceof Error ? err.message : String(err))
    process.exit(1)
  }

  let ledger: RetiredLedger
  try {
    ledger = loadRetiredLedger(join(projectRoot, 'scripts', 'retired-challenges.json'))
  } catch (err) {
    console.error(err instanceof Error ? err.message : String(err))
    process.exit(1)
  }
  const retiredError = checkRetired(name, id, ledger)
  if (retiredError) {
    console.error(retiredError)
    process.exit(1)
  }

  const content = buildContent({ id, name, title, difficulty, algorithm, type, category })

  mkdirSync(challengeDir, { recursive: true })
  writeFileSync(outPath, content, 'utf-8')
  console.log(`[new-challenge] Created: docs/challenge/${name}.md`)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main()
}
