// @vitest-environment node
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { mkdtempSync, rmSync, writeFileSync, existsSync, readdirSync } from 'node:fs'
import { createDecipheriv, randomBytes } from 'node:crypto'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import {
  deriveSlug,
  validateSlug,
  cleanupObsoletePools,
  readChallenge,
  encryptPool,
  collectAndValidateSlugs,
  computePlanTotal,
  MAGIC,
  POOL_VERSION,
} from './generate-pools.js'

describe('deriveSlug', () => {
  it('strips .md suffix from markdown file basename', () => {
    expect(deriveSlug('/abs/path/multiplication-table.md')).toBe('multiplication-table')
    expect(deriveSlug('docs/challenge/star-rectangle.md')).toBe('star-rectangle')
    expect(deriveSlug('foo.md')).toBe('foo')
  })

  it('does not strip non-.md suffix', () => {
    expect(deriveSlug('/path/foo.txt')).toBe('foo.txt')
  })
})

describe('validateSlug', () => {
  it('accepts normal slug', () => {
    expect(() => validateSlug('multiplication-table', '/x/multiplication-table.md')).not.toThrow()
    expect(() => validateSlug('9-9', '/x/9-9.md')).not.toThrow()
  })

  it('rejects empty slug', () => {
    expect(() => validateSlug('', '/x/.md')).toThrow(/empty/i)
  })

  it('rejects uppercase letters', () => {
    expect(() => validateSlug('Multiplication-Table', '/x/Multiplication-Table.md')).toThrow()
  })

  it('rejects path traversal', () => {
    expect(() => validateSlug('../escape', '/x/escape.md')).toThrow()
  })

  it('rejects path separator', () => {
    expect(() => validateSlug('nested/loop', '/x/loop.md')).toThrow()
    expect(() => validateSlug('back\\slash', '/x/slash.md')).toThrow()
  })

  it('rejects underscores and dots (outside allowed set)', () => {
    expect(() => validateSlug('foo_bar', '/x/foo_bar.md')).toThrow()
    expect(() => validateSlug('foo.bar', '/x/foo.bar.md')).toThrow()
  })

  it('rejects slug exceeding 64 characters', () => {
    const long = 'a'.repeat(65)
    expect(() => validateSlug(long, `/x/${long}.md`)).toThrow(/length|long/i)
  })

  it('error message includes the offending file path', () => {
    expect(() => validateSlug('Bad', '/abs/Bad.md')).toThrow(/\/abs\/Bad\.md/)
  })
})

describe('cleanupObsoletePools', () => {
  let tmp: string

  beforeEach(() => {
    tmp = mkdtempSync(join(tmpdir(), 'pools-test-'))
  })

  afterEach(() => {
    rmSync(tmp, { recursive: true, force: true })
  })

  it('deletes .bin files whose basename is not in the valid set', () => {
    writeFileSync(join(tmp, 'multiplication-table.bin'), 'x')
    writeFileSync(join(tmp, 'star-rectangle.bin'), 'x')
    writeFileSync(join(tmp, 'nested-loop.bin'), 'stale')

    const validSlugs = new Set(['multiplication-table', 'star-rectangle'])
    const deleted = cleanupObsoletePools(tmp, validSlugs)

    expect(deleted).toEqual(['nested-loop.bin'])
    expect(existsSync(join(tmp, 'multiplication-table.bin'))).toBe(true)
    expect(existsSync(join(tmp, 'star-rectangle.bin'))).toBe(true)
    expect(existsSync(join(tmp, 'nested-loop.bin'))).toBe(false)
  })

  it('preserves .gitkeep and non-bin files', () => {
    writeFileSync(join(tmp, '.gitkeep'), '')
    writeFileSync(join(tmp, 'README.txt'), 'x')
    writeFileSync(join(tmp, 'orphan.bin'), 'stale')

    const validSlugs = new Set<string>([])
    cleanupObsoletePools(tmp, validSlugs)

    expect(existsSync(join(tmp, '.gitkeep'))).toBe(true)
    expect(existsSync(join(tmp, 'README.txt'))).toBe(true)
    expect(existsSync(join(tmp, 'orphan.bin'))).toBe(false)
  })

  it('does not delete entries inside subdirectories', () => {
    writeFileSync(join(tmp, 'keep.bin'), 'x')
    // mkdtemp does not allow nested dirs without explicit mkdir
    const sub = join(tmp, 'subdir')
    require('node:fs').mkdirSync(sub)
    writeFileSync(join(sub, 'inside.bin'), 'x')

    const validSlugs = new Set(['keep'])
    cleanupObsoletePools(tmp, validSlugs)

    expect(existsSync(join(tmp, 'keep.bin'))).toBe(true)
    expect(existsSync(join(sub, 'inside.bin'))).toBe(true)
  })

  it('returns empty array when pools directory is empty', () => {
    const deleted = cleanupObsoletePools(tmp, new Set(['anything']))
    expect(deleted).toEqual([])
  })

  it('does nothing if pools directory does not exist', () => {
    const missing = join(tmp, 'nonexistent')
    const deleted = cleanupObsoletePools(missing, new Set(['x']))
    expect(deleted).toEqual([])
  })
})

describe('collectAndValidateSlugs', () => {
  it('returns slug → filePath map for valid inputs', () => {
    const map = collectAndValidateSlugs(
      ['multiplication-table.md', 'star-rectangle.md'],
      '/challenges',
    )
    expect(map.get('multiplication-table')).toBe('/challenges/multiplication-table.md')
    expect(map.get('star-rectangle')).toBe('/challenges/star-rectangle.md')
    expect(map.size).toBe(2)
  })

  it('rejects files without a .md extension (defense in depth)', () => {
    // Even if validateSlug's character regex were later relaxed to allow dots,
    // the .md-only enforcement here prevents non-markdown files from minting
    // pools.
    expect(() => collectAndValidateSlugs(['foo.txt'], '/challenges')).toThrow(/\.md/)
    expect(() => collectAndValidateSlugs(['bar'], '/challenges')).toThrow(/\.md/)
  })

  it('throws when two files yield the same slug', () => {
    expect(() => collectAndValidateSlugs(['foo.md', 'foo.md'], '/challenges')).toThrow(/duplicate/i)
  })

  it('error on duplicate names lists both conflicting paths', () => {
    let err: Error | null = null
    try {
      collectAndValidateSlugs(['foo.md', 'foo.md'], '/challenges')
    } catch (e) {
      err = e as Error
    }
    expect(err).not.toBeNull()
    // Both file paths must be present so the operator can locate them
    expect(err!.message).toMatch(/\/challenges\/foo\.md/)
  })

  it('throws when a slug fails shape validation', () => {
    expect(() => collectAndValidateSlugs(['Bad.md'], '/challenges')).toThrow(/Bad/)
  })

  it('throws when slug exceeds length limit', () => {
    const long = `${'a'.repeat(65)}.md`
    expect(() => collectAndValidateSlugs([long], '/challenges')).toThrow(/length|long/i)
  })
})

describe('encryptPool', () => {
  function decryptPool(buf: Buffer, key: Buffer): unknown {
    expect(buf.subarray(0, 6).equals(MAGIC)).toBe(true)
    expect(buf[6]).toBe(POOL_VERSION)
    const nonce = buf.subarray(7, 19)
    const tag = buf.subarray(buf.length - 16)
    const ct = buf.subarray(19, buf.length - 16)
    const decipher = createDecipheriv('aes-256-gcm', key, nonce)
    decipher.setAuthTag(tag)
    const plain = Buffer.concat([decipher.update(ct), decipher.final()]).toString('utf-8')
    return JSON.parse(plain)
  }

  it('encrypts payload with challenge_id equal to the supplied slug', () => {
    const key = randomBytes(32)
    const buf = encryptPool(key, 'multiplication-table', 'hidden', [
      { input: '3', expected_output: '1 2 3' },
    ])
    const payload = decryptPool(buf, key) as { challenge_id: string; verdict_detail: string }
    expect(payload.challenge_id).toBe('multiplication-table')
    expect(payload.challenge_id).not.toBe('nested-loop')
    expect(payload.verdict_detail).toBe('hidden')
  })

  it('round-trips testcases through the pool format', () => {
    const key = randomBytes(32)
    const testcases = [
      { input: '5', expected_output: 'output-5' },
      { input: '7', expected_output: 'output-7' },
    ]
    const buf = encryptPool(key, 'star-rectangle', 'actual', testcases)
    const payload = decryptPool(buf, key) as {
      challenge_id: string
      testcases: Array<{ input: string; expected_output: string }>
    }
    expect(payload.challenge_id).toBe('star-rectangle')
    expect(payload.testcases).toEqual(testcases)
  })

  it('includes plan_block_size only when supplied', () => {
    const key = randomBytes(32)
    const testcases = [{ input: '1', expected_output: 'a' }]

    const planBuf = encryptPool(key, 'plan-ch', 'hidden', testcases, 5)
    const planPayload = decryptPool(planBuf, key) as Record<string, unknown>
    expect(planPayload.plan_block_size).toBe(5)

    const plainBuf = encryptPool(key, 'plain-ch', 'hidden', testcases)
    const plainPayload = decryptPool(plainBuf, key) as Record<string, unknown>
    expect('plan_block_size' in plainPayload).toBe(false)
  })
})

describe('computePlanTotal', () => {
  it('sums band counts and counts each literal as one', () => {
    const plan = [
      { count: 3, override: { n: { max: 20 } } },
      { count: 2, override: { n: { min: 2500 } } },
      { literal: '1\n1\n-999\n' },
    ]
    expect(computePlanTotal(plan, 'deque.md')).toBe(6)
  })

  it('rejects a band without a positive integer count', () => {
    expect(() => computePlanTotal([{ count: 0 }], 'x.md')).toThrow(/x\.md/)
    expect(() => computePlanTotal([{ count: 1.5 }], 'x.md')).toThrow(/positive integer/)
    expect(() => computePlanTotal([{}], 'x.md')).toThrow(/count/)
  })

  it('rejects an empty plan', () => {
    expect(() => computePlanTotal([], 'x.md')).toThrow(/at least one/)
  })
})

describe('readChallenge', () => {
  let tmp: string

  beforeEach(() => {
    tmp = mkdtempSync(join(tmpdir(), 'readch-test-'))
  })

  afterEach(() => {
    rmSync(tmp, { recursive: true, force: true })
  })

  it('returns slug derived from the markdown file basename', () => {
    const filePath = join(tmp, 'multiplication-table.md')
    writeFileSync(
      filePath,
      `---
algorithm: nested-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 9
generator: |
  n = int(input())
  print(n)
---

body
`,
      'utf-8',
    )

    const ch = readChallenge(filePath)
    expect(ch.slug).toBe('multiplication-table')
    expect(ch.algorithm).toBe('nested-loop')
  })

  function writeChallenge(dir: string, name: string, extraFm: string): string {
    const filePath = join(dir, name)
    writeFileSync(
      filePath,
      `---
algorithm: deque-scan
${extraFm}
params:
  n:
    type: int
    min: 1
    max: 9
generator: |
  n = int(input())
  print(n)
---

body
`,
      'utf-8',
    )
    return filePath
  }

  it('reads testcase_plan through verbatim', () => {
    const filePath = writeChallenge(
      tmp,
      'plan-ok.md',
      `testcase_plan:
  - count: 3
    override:
      n:
        max: 5
  - literal: "7\\n"`,
    )
    const ch = readChallenge(filePath)
    expect(ch.testcase_plan).toEqual([
      { count: 3, override: { n: { max: 5 } } },
      { literal: '7\n' },
    ])
  })

  it('rejects testcase_plan coexisting with testcase_count', () => {
    const filePath = writeChallenge(
      tmp,
      'plan-conflict.md',
      `testcase_count: 5
testcase_plan:
  - count: 3`,
    )
    expect(() => readChallenge(filePath)).toThrow(/mutually exclusive/)
    expect(() => readChallenge(filePath)).toThrow(/plan-conflict\.md/)
  })

  it('accepts an absent testcase_plan with a declared testcase_count', () => {
    const filePath = writeChallenge(tmp, 'plain.md', 'testcase_count: 5')
    const ch = readChallenge(filePath)
    expect(ch.testcase_plan).toBeUndefined()
    expect(ch.testcase_count).toBe(5)
  })

  it('rejects an invalid verdict_detail with the allowed values', () => {
    const filePath = writeChallenge(tmp, 'vd-typo.md', 'verdict_detail: ful')
    expect(() => readChallenge(filePath)).toThrow(/hidden, actual, full/)
    expect(() => readChallenge(filePath)).toThrow(/vd-typo\.md/)
  })

  it('defaults verdict_detail to hidden when absent', () => {
    const filePath = writeChallenge(tmp, 'vd-absent.md', 'testcase_count: 5')
    expect(readChallenge(filePath).verdict_detail).toBe('hidden')
  })
})
