#!/usr/bin/env npx tsx
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

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
  return null
}

export function validateDifficulty(difficulty: string): string | null {
  if (!['easy', 'medium', 'hard'].includes(difficulty)) {
    return `[new-challenge] ERROR: --difficulty must be one of: easy, medium, hard`
  }
  return null
}

export interface ParsedArgs {
  name: string
  title: string
  difficulty: string
  algorithm: string
}

export function parseArgs(argv: string[]): ParsedArgs | null {
  const args = argv.slice(2)
  let name = ''
  let title: string | null = null
  let difficulty = 'easy'
  let algorithm: string | null = null

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--title' && i + 1 < args.length) {
      title = args[++i]!
    } else if (args[i] === '--difficulty' && i + 1 < args.length) {
      difficulty = args[++i]!
    } else if (args[i] === '--algorithm' && i + 1 < args.length) {
      algorithm = args[++i]!
    } else if (!args[i]!.startsWith('--')) {
      name = args[i]!
    }
  }

  if (!name) return null

  return {
    name,
    title: title ?? toTitleCase(name),
    difficulty,
    algorithm: algorithm ?? toAlgorithmName(name),
  }
}

export function computeNextId(fileContents: string[]): number {
  let maxId = 0
  for (const content of fileContents) {
    const match = content.match(/^id:\s*(\d+)/m)
    if (match) {
      const id = parseInt(match[1]!, 10)
      if (id > maxId) maxId = id
    }
  }
  return maxId + 1
}

export interface BuildContentOptions {
  id: number
  name: string
  title: string
  difficulty: string
  algorithm: string
}

export function buildContent({ id, title, difficulty, algorithm }: BuildContentOptions): string {
  return `---
layout: challenge
id: ${id}
title: ${title}
difficulty: ${difficulty}
tags: []
algorithm: ${algorithm}
testcase_count: 5
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
      'Usage: pnpm new-challenge <name> [--title <title>] [--difficulty easy|medium|hard] [--algorithm <algorithm>]',
    )
    process.exit(1)
  }

  const { name, title, difficulty, algorithm } = parsed

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

  const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
  const challengeDir = join(projectRoot, 'docs', 'challenge')
  const outPath = join(challengeDir, `${name}.md`)

  if (existsSync(outPath)) {
    console.error(
      `[new-challenge] ERROR: docs/challenge/${name}.md already exists. Aborting to prevent overwrite.`,
    )
    process.exit(1)
  }

  let fileContents: string[] = []
  if (existsSync(challengeDir)) {
    fileContents = readdirSync(challengeDir)
      .filter((f) => f.endsWith('.md'))
      .map((f) => readFileSync(join(challengeDir, f), 'utf-8'))
  }
  const id = computeNextId(fileContents)

  const content = buildContent({ id, name, title, difficulty, algorithm })

  mkdirSync(challengeDir, { recursive: true })
  writeFileSync(outPath, content, 'utf-8')
  console.log(`[new-challenge] Created: docs/challenge/${name}.md`)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main()
}
