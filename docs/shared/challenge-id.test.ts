import { describe, it, expect } from 'vitest'
import {
  CHALLENGE_ID_PATTERN,
  CATEGORY_ID_PREFIX,
  challengeIdOrdinal,
  compareChallengeId,
  extractFrontmatterId,
} from './challenge-id'
import { CHALLENGE_CATEGORIES } from './challenge-category'

describe('CHALLENGE_ID_PATTERN', () => {
  it.each(['py001', 'py054', 'apcs003', 'apcs999'])('accepts %s', (id) => {
    expect(CHALLENGE_ID_PATTERN.test(id)).toBe(true)
  })

  it.each(['py1', 'py0001', '3', '003', 'PY001', 'apcs01', 'py001x', ''])(
    'rejects %s',
    (id) => {
      expect(CHALLENGE_ID_PATTERN.test(id)).toBe(false)
    },
  )
})

describe('CATEGORY_ID_PREFIX', () => {
  it('covers every challenge category', () => {
    for (const cat of CHALLENGE_CATEGORIES) {
      expect(CATEGORY_ID_PREFIX[cat]).toBeTruthy()
    }
  })

  it('maps python to py and apcs to apcs', () => {
    expect(CATEGORY_ID_PREFIX.python).toBe('py')
    expect(CATEGORY_ID_PREFIX.apcs).toBe('apcs')
  })

  it('no prefix is a prefix of another (keeps startsWith search unambiguous per prefix)', () => {
    const prefixes = Object.values(CATEGORY_ID_PREFIX)
    for (const a of prefixes) {
      for (const b of prefixes) {
        if (a !== b) expect(a.startsWith(b)).toBe(false)
      }
    }
  })
})

describe('challengeIdOrdinal', () => {
  it.each([
    ['py001', 1],
    ['py003', 3],
    ['py054', 54],
    ['apcs005', 5],
  ] as const)('parses %s as %d', (id, ordinal) => {
    expect(challengeIdOrdinal(id)).toBe(ordinal)
  })

  it('returns NaN when the id has no digits', () => {
    expect(challengeIdOrdinal('py')).toBeNaN()
    expect(challengeIdOrdinal('')).toBeNaN()
  })
})

describe('compareChallengeId', () => {
  it('orders same-prefix ids by ordinal (zero-padding makes lexicographic = numeric)', () => {
    const shuffled = ['py010', 'py002', 'py054', 'py001']
    expect([...shuffled].sort(compareChallengeId)).toEqual([
      'py001',
      'py002',
      'py010',
      'py054',
    ])
  })

  it('descending sort yields highest ordinals first (homepage latest lists)', () => {
    const ids = ['py052', 'py054', 'py001', 'py053']
    const desc = [...ids].sort((a, b) => compareChallengeId(b, a))
    expect(desc.slice(0, 3)).toEqual(['py054', 'py053', 'py052'])
  })

  it('pins the cross-prefix boundary: apcs sorts before py, with no user-facing meaning', () => {
    expect(compareChallengeId('apcs005', 'py001')).toBeLessThan(0)
  })

  it('equal ids compare as 0', () => {
    expect(compareChallengeId('py001', 'py001')).toBe(0)
  })
})

describe('extractFrontmatterId', () => {
  it('reads the id from the frontmatter block', () => {
    expect(extractFrontmatterId('---\nid: py003\ntitle: foo\n---\n\nbody')).toBe('py003')
  })

  it('ignores an id line in body text or fenced code blocks', () => {
    const content = '---\ntitle: no-id-here\n---\n\n```yaml\nid: py999\n```\nid: apcs001\n'
    expect(extractFrontmatterId(content)).toBeNull()
  })

  it('returns null when there is no frontmatter block', () => {
    expect(extractFrontmatterId('id: py001\n')).toBeNull()
  })
})
