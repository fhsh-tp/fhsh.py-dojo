// @vitest-environment node
/**
 * Unit tests for the data-layer challenge-category resolution, plus the
 * all-challenge authoring gate.
 *
 * The resolver locks in the runtime-safe behaviour the data loader relies on:
 * an absent or mistyped `category` resolves to `python` instead of being
 * silently trusted, so a typo can never make a challenge disappear from both
 * catalogue pages. The file-scan gate is the loud counterpart: any
 * `docs/challenge/*.md` declaring an unknown category fails HERE, naming the
 * file — same philosophy as the params conformance gate.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { describe, it, expect } from 'vitest'
import yaml from 'js-yaml'

import { CATEGORY_LIST_URL, CHALLENGE_CATEGORIES, resolveChallengeCategory } from './challenge-category.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../challenge')

describe('CHALLENGE_CATEGORIES', () => {
  it('lists exactly the implemented categories', () => {
    expect([...CHALLENGE_CATEGORIES]).toEqual(['python', 'apcs'])
  })
})

describe('resolveChallengeCategory', () => {
  it('preserves a known value', () => {
    expect(resolveChallengeCategory('python')).toBe('python')
    expect(resolveChallengeCategory('apcs')).toBe('apcs')
  })

  it('resolves an absent value to python', () => {
    expect(resolveChallengeCategory(undefined)).toBe('python')
    expect(resolveChallengeCategory(null)).toBe('python')
  })

  it('resolves a mistyped or wrong-cased value to python (no silent trust)', () => {
    for (const bad of ['apsc', 'APCS', 'Python', 'ds', '', 42, {}, []]) {
      expect(resolveChallengeCategory(bad)).toBe('python')
    }
  })
})

describe('category → catalogue page contract', () => {
  // The `.md` catalogue pages sit outside vue-tsc's project, so the exhaustive
  // `CATEGORY_LIST_URL` Record cannot protect them at compile time — this scan
  // is their loud counterpart: extending the taxonomy without giving the new
  // category a page that filters on it fails HERE, naming the category.
  it('every category has an existing catalogue page filtering on it', () => {
    for (const cat of CHALLENGE_CATEGORIES) {
      const pagePath = resolve(import.meta.dirname, `..${CATEGORY_LIST_URL[cat]}.md`)
      const content = readFileSync(pagePath, 'utf-8')
      expect(content, `${pagePath} must filter on category '${cat}'`).toContain(
        `c.category === '${cat}'`,
      )
    }
  })
})

describe('challenge category authoring gate', () => {
  const files = readdirSync(CHALLENGES_DIR).filter((f) => f.endsWith('.md'))

  it('at least one challenge file exists', () => {
    expect(files.length).toBeGreaterThan(0)
  })

  // One case per file (mirroring challenge-params.test.ts) so a broken
  // frontmatter YAML fails with the file's name in the case title instead of
  // an anonymous YAMLException.
  it.each(files)('%s: declares a known category (or none)', (file) => {
    const content = readFileSync(join(CHALLENGES_DIR, file), 'utf-8')
    const frontmatterBlock = content.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1]
    if (frontmatterBlock === undefined) return
    const fm = yaml.load(frontmatterBlock) as Record<string, unknown> | null
    const category = fm?.category
    if (category !== undefined) {
      expect(
        [...CHALLENGE_CATEGORIES] as unknown[],
        `unknown category ${JSON.stringify(category)} in ${file}`,
      ).toContain(category)
    }
  })
})
