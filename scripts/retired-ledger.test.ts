import { describe, it, expect } from 'vitest'
import { readFileSync, readdirSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { tmpdir } from 'node:os'
import { fileURLToPath } from 'node:url'
import { checkRetired, loadRetiredLedger } from './new-challenge'

const here = dirname(fileURLToPath(import.meta.url))
const ledgerPath = join(here, 'retired-challenges.json')
const challengeDir = join(here, '..', 'docs', 'challenge')

describe('retired challenge ledger', () => {
  it('flags a reused retired slug and passes a fresh one', () => {
    const ledger = { slugs: ['old-slug'], ids: [] }
    expect(checkRetired('old-slug', 99, ledger)).toContain('retired')
    expect(checkRetired('fresh-slug', 99, ledger)).toBeNull()
  })

  it('flags a reused retired id', () => {
    expect(checkRetired('x', 42, { slugs: [], ids: [42] })).toContain('retired')
  })

  it('throws (fail-closed) on a malformed ledger so the reuse guard cannot silently vanish', () => {
    const dir = mkdtempSync(join(tmpdir(), 'retired-ledger-'))
    const bad = join(dir, 'retired-challenges.json')
    writeFileSync(bad, '{ not: valid json', 'utf-8')
    try {
      expect(() => loadRetiredLedger(bad)).toThrow(/not valid JSON/)
    } finally {
      rmSync(dir, { recursive: true, force: true })
    }
  })

  it('no active challenge reuses a retired slug or id (content-regression)', () => {
    const ledger = loadRetiredLedger(ledgerPath)
    const files = readdirSync(challengeDir).filter((f) => f.endsWith('.md'))
    for (const f of files) {
      const slug = f.replace(/\.md$/, '')
      expect(ledger.slugs, `active slug '${slug}' is in the retired ledger`).not.toContain(slug)
      const m = readFileSync(join(challengeDir, f), 'utf-8').match(/^id:\s*(\d+)/m)
      if (m) expect(ledger.ids).not.toContain(parseInt(m[1]!, 10))
    }
  })
})
