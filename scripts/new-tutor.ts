#!/usr/bin/env npx tsx
import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { join, resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

// ── Pure helpers ──────────────────────────────────────────────────────────────

export function getFormattedDate(): string {
  const now = new Date()
  const offset = 8 * 60 * 60 * 1000
  const utc8Date = new Date(now.getTime() + offset)
  return utc8Date.toISOString().replace(/\.(\d{3})Z$/, '+08:00')
}

export function validateChapter(chapter: string): string | null {
  if (!/^ch\d+$/.test(chapter)) {
    return `[new-tutor] ERROR: <chapter> must be in the format chN (e.g., ch1, ch2)`
  }
  return null
}

export function parseChapterNumber(chapter: string): number {
  return parseInt(chapter.replace(/^ch/, ''), 10)
}

export interface ParsedArgs {
  subject: string
  chapter: string
  section: string
  title: string
  description: string
  challenge: string | null
}

export function parseArgs(argv: string[]): ParsedArgs | null {
  const args = argv.slice(2)
  let subject = ''
  let chapter = ''
  let section = ''
  let title: string | null = null
  let description = ''
  let challenge: string | null = null

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--title' && i + 1 < args.length) {
      title = args[++i]
    } else if (args[i] === '--description' && i + 1 < args.length) {
      description = args[++i]
    } else if (args[i] === '--challenge' && i + 1 < args.length) {
      challenge = args[++i]
    } else if (!args[i].startsWith('--')) {
      if (!subject) subject = args[i]
      else if (!chapter) chapter = args[i]
      else if (!section) section = args[i]
    }
  }

  if (!subject || !chapter || !section) return null

  return {
    subject,
    chapter,
    section,
    title: title ?? section,
    description,
    challenge,
  }
}

export function buildContent(opts: {
  subject: string
  chapter: string
  section: string
  title: string
  description: string
  challenge: string | null
  createdTime: string
}): string {
  const { subject, chapter, section, title, description, challenge, createdTime } = opts
  const chapterNum = parseChapterNumber(chapter)
  const isIndex = section === 'index'

  if (isIndex) {
    return `---
layout: doc
title: ${title}
description: ${description}
isIndex: true
---

# ${title}
`
  }

  const challengeLine = challenge ? `challenge: ${challenge}\n` : ''

  return `---
layout: doc
title: ${title}
description: ${description}
chapter: ${chapterNum}
section: "${section}"
createdTime: ${createdTime}
${challengeLine}---

# ${title}

## 概念溯源

說明為什麼需要學這個概念，以及它解決了什麼問題。

## 教學內容

### 語法介紹

\`\`\`python
# 範例程式碼
\`\`\`

### 範例說明

說明範例的運作方式。

## Judge 解題實戰
${challenge ? `\n<ChallengeLink slug="${challenge}" />\n` : '\n（尚無對應挑戰題目）\n'}
`
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main(): void {
  const parsed = parseArgs(process.argv)

  if (!parsed) {
    console.error(
      'Usage: pnpm new-tutor <subject> <chapter> <section> [--title <title>] [--description <desc>] [--challenge <slug>]',
    )
    process.exit(1)
  }

  const { subject, chapter, section, title, description, challenge } = parsed

  const chapterError = validateChapter(chapter)
  if (chapterError) {
    console.error(chapterError)
    process.exit(1)
  }

  const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
  const outDir = join(projectRoot, 'docs', 'tutor', subject, chapter)
  const outPath = join(outDir, `${section}.md`)

  if (existsSync(outPath)) {
    console.error(`[new-tutor] ERROR: ${outPath} already exists. Aborting to prevent overwrite.`)
    process.exit(1)
  }

  const createdTime = getFormattedDate()
  const content = buildContent({ subject, chapter, section, title, description, challenge, createdTime })

  mkdirSync(outDir, { recursive: true })
  writeFileSync(outPath, content, 'utf-8')
  console.log(`[new-tutor] Created: docs/tutor/${subject}/${chapter}/${section}.md`)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main()
}
