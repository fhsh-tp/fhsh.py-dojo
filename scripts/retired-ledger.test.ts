import { describe, it, expect } from 'vitest'
import { readFileSync, readdirSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { tmpdir } from 'node:os'
import { fileURLToPath } from 'node:url'
import { checkRetired, loadRetiredLedger } from './new-challenge'
import { CHALLENGE_ID_PATTERN, extractFrontmatterId } from '../docs/shared/challenge-id'

const here = dirname(fileURLToPath(import.meta.url))
const ledgerPath = join(here, 'retired-challenges.json')
const challengeDir = join(here, '..', 'docs', 'challenge')

describe('retired challenge ledger', () => {
  it('flags a reused retired slug and passes a fresh one', () => {
    const ledger = { slugs: ['old-slug'], ids: [] }
    expect(checkRetired('old-slug', 'py099', ledger)).toContain('retired')
    expect(checkRetired('fresh-slug', 'py099', ledger)).toBeNull()
  })

  it('flags a reused retired string id', () => {
    expect(checkRetired('x', 'apcs042', { slugs: [], ids: ['apcs042'] })).toContain('retired')
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

  describe('loadRetiredLedger fails closed on an untrustworthy ledger', () => {
    function loadTmpLedger(json: string) {
      const dir = mkdtempSync(join(tmpdir(), 'retired-ledger-'))
      try {
        const p = join(dir, 'retired-challenges.json')
        writeFileSync(p, json, 'utf-8')
        return loadRetiredLedger(p)
      } finally {
        rmSync(dir, { recursive: true, force: true })
      }
    }

    // Every one of these used to load "successfully" into a ledger whose
    // membership test can never match — the guard silently off, with the
    // not.toContain assertion in the content-regression case vacuously green
    // at the same time.
    it.each([
      ['a legacy numeric id (pre string-id migration)', '{"slugs":[],"ids":[59]}'],
      ['a numeric-string id', '{"slugs":[],"ids":["59"]}'],
      ['a wrong-case id', '{"slugs":[],"ids":["PY059"]}'],
      ['an ids field that is not an array', '{"slugs":[],"ids":"py059"}'],
      ['a slugs field that is not an array', '{"slugs":"caesar-01","ids":[]}'],
      ['a non-string slug entry', '{"slugs":[{"a":1}],"ids":[]}'],
      ['an empty-string slug entry', '{"slugs":[""],"ids":[]}'],
      ['a root that is an array', '[1,2,3]'],
      ['a root that is null', 'null'],
    ])('throws on %s', (_label, json) => {
      expect(() => loadTmpLedger(json)).toThrow(/refusing to scaffold/)
    })

    it('a legacy numeric id can no longer disarm checkRetired', () => {
      // Regression pin for the exact pre-fix behaviour:
      //   loadRetiredLedger -> {ids:[59]}; checkRetired('x','py059') -> null
      expect(() => loadTmpLedger('{"slugs":[],"ids":[59]}')).toThrow(/"ids"\[0\] entry 59/)
    })

    it('accepts a well-formed ledger and ignores unknown keys like _comment', () => {
      expect(loadTmpLedger('{"_comment":"why","slugs":["caesar-01"],"ids":["py059"]}')).toEqual({
        slugs: ['caesar-01'],
        ids: ['py059'],
      })
    })

    it('treats an absent field as empty rather than an error', () => {
      expect(loadTmpLedger('{"slugs":["caesar-01"]}')).toEqual({ slugs: ['caesar-01'], ids: [] })
    })
  })

  it('no active challenge reuses a retired slug or id (content-regression)', () => {
    const ledger = loadRetiredLedger(ledgerPath)
    const files = readdirSync(challengeDir).filter((f) => f.endsWith('.md'))
    expect(files.length).toBeGreaterThan(0)

    // Count every id actually parsed: if the format drifts and the regex stops
    // matching, this assertion fails loudly instead of the per-file checks
    // silently evaporating (the exact fail-open the integer-era regex had).
    let parsed = 0
    for (const f of files) {
      const slug = f.replace(/\.md$/, '')
      expect(ledger.slugs, `active slug '${slug}' is in the retired ledger`).not.toContain(slug)
      const id = extractFrontmatterId(readFileSync(join(challengeDir, f), 'utf-8'))
      expect(id, `challenge '${f}' has no parseable id line`).not.toBeNull()
      expect(
        CHALLENGE_ID_PATTERN.test(id!),
        `challenge '${f}' id '${id}' does not match the challenge id format`,
      ).toBe(true)
      expect(ledger.ids, `active id '${id}' is in the retired ledger`).not.toContain(id)
      parsed++
    }
    expect(parsed).toBe(files.length)
  })
})
