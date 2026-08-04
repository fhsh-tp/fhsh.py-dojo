// @vitest-environment node
/**
 * nav.yml ↔ category catalogue lockstep.
 *
 * `themeConfig.nav` never enters VitePress dead-link detection (that only
 * scans markdown body links), so a renamed catalogue URL or a nav typo would
 * ship a silent 404 entry. This gate binds the nav surface to
 * `CATEGORY_LIST_URL`: every catalogue page must keep a nav entry. One
 * direction only — nav is free to carry non-category links (`/tutor/*`).
 * Premise worth stating: a nav entry is a required surface for every
 * category; a future category that should NOT occupy the nav needs this
 * gate revisited.
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, it, expect } from 'vitest'
import yaml from 'js-yaml'

import { CATEGORY_LIST_URL, CHALLENGE_CATEGORIES } from '../docs/shared/challenge-category.js'

interface NavNode {
  text?: string
  link?: string
  items?: NavNode[]
}

function collectLinks(nodes: NavNode[]): string[] {
  const links: string[] = []
  for (const node of nodes) {
    if (node.link !== undefined) links.push(node.link)
    if (node.items) links.push(...collectLinks(node.items))
  }
  return links
}

describe('nav.yml catalogue lockstep', () => {
  it('every catalogue page URL has a nav entry', () => {
    const navPath = resolve(import.meta.dirname, 'nav.yml')
    const nav = yaml.load(readFileSync(navPath, 'utf-8')) as NavNode[]
    const links = collectLinks(nav)
    for (const cat of CHALLENGE_CATEGORIES) {
      expect(
        links,
        `nav.yml must contain a link to ${CATEGORY_LIST_URL[cat]} (category '${cat}')`,
      ).toContain(CATEGORY_LIST_URL[cat])
    }
  })
})
