// @vitest-environment node
import { describe, it, expect } from 'vitest'
import {
  parseArgs,
  validateName,
  validateDifficulty,
  validateType,
  validateCategory,
  computeNextId,
  buildContent,
  toTitleCase,
  toAlgorithmName,
  EXERCISE_TYPES,
  CHALLENGE_CATEGORIES,
} from './new-challenge.js'

describe('toTitleCase', () => {
  it('converts kebab-case to Title Case', () => {
    expect(toTitleCase('bubble-sort')).toBe('Bubble Sort')
    expect(toTitleCase('linear-search')).toBe('Linear Search')
    expect(toTitleCase('fibonacci')).toBe('Fibonacci')
  })
})

describe('toAlgorithmName', () => {
  it('replaces hyphens with underscores', () => {
    expect(toAlgorithmName('bubble-sort')).toBe('bubble_sort')
    expect(toAlgorithmName('linear-search')).toBe('linear_search')
    expect(toAlgorithmName('fibonacci')).toBe('fibonacci')
  })
})

describe('parseArgs', () => {
  it('returns null when name is missing', () => {
    expect(parseArgs(['node', 'script.ts'])).toBeNull()
    expect(parseArgs(['node', 'script.ts', '--difficulty', 'easy'])).toBeNull()
  })

  it('parses name and applies defaults', () => {
    const result = parseArgs(['node', 'script.ts', 'bubble-sort'])
    expect(result).toEqual({
      name: 'bubble-sort',
      title: 'Bubble Sort',
      difficulty: 'easy',
      algorithm: 'bubble_sort',
      type: 'basic',
      category: 'python',
    })
  })

  it('accepts explicit --title, --difficulty, --algorithm', () => {
    const result = parseArgs([
      'node',
      'script.ts',
      'linear-search',
      '--title',
      '線性搜尋',
      '--difficulty',
      'medium',
      '--algorithm',
      'linear_search',
    ])
    expect(result).toEqual({
      name: 'linear-search',
      title: '線性搜尋',
      difficulty: 'medium',
      algorithm: 'linear_search',
      type: 'basic',
      category: 'python',
    })
  })

  it('options can appear before the name', () => {
    const result = parseArgs(['node', 'script.ts', '--difficulty', 'hard', 'merge-sort'])
    expect(result?.name).toBe('merge-sort')
    expect(result?.difficulty).toBe('hard')
  })
})

describe('validateName', () => {
  it('returns null for valid kebab-case names', () => {
    expect(validateName('bubble-sort')).toBeNull()
    expect(validateName('fibonacci')).toBeNull()
    expect(validateName('binary-search-tree')).toBeNull()
    expect(validateName('base64')).toBeNull()
  })

  it('returns error for uppercase letters', () => {
    expect(validateName('BubbleSort')).toBe(
      '[new-challenge] ERROR: <name> must be kebab-case (lowercase letters, digits, hyphens only)',
    )
    expect(validateName('Bubble-sort')).not.toBeNull()
  })

  it('returns error for underscore-separated names', () => {
    expect(validateName('bubble_sort')).not.toBeNull()
  })

  it('returns error for names with spaces', () => {
    expect(validateName('bubble sort')).not.toBeNull()
  })
})

describe('validateDifficulty', () => {
  it('returns null for valid difficulties', () => {
    expect(validateDifficulty('easy')).toBeNull()
    expect(validateDifficulty('medium')).toBeNull()
    expect(validateDifficulty('hard')).toBeNull()
  })

  it('returns exact error message for invalid difficulty', () => {
    expect(validateDifficulty('extreme')).toBe(
      '[new-challenge] ERROR: --difficulty must be one of: easy, medium, hard',
    )
    expect(validateDifficulty('')).not.toBeNull()
    expect(validateDifficulty('Easy')).not.toBeNull()
  })
})

describe('computeNextId', () => {
  it('returns <prefix>001 when no file carries the prefix', () => {
    expect(computeNextId([], 'py')).toBe('py001')
    expect(
      computeNextId([{ name: 'foo.md', content: '---\nid: py012\ntitle: foo\n---' }], 'apcs'),
    ).toBe('apcs001')
  })

  it('returns max ordinal + 1 within the prefix, zero-padded', () => {
    const files = [
      { name: 'a.md', content: '---\nid: py003\ntitle: foo\n---' },
      { name: 'b.md', content: '---\nid: py001\ntitle: bar\n---' },
      { name: 'c.md', content: '---\nid: py007\ntitle: baz\n---' },
    ]
    expect(computeNextId(files, 'py')).toBe('py008')
  })

  it('counts categories independently (spec example: py001–py054 + apcs001–apcs005 → apcs006)', () => {
    const files = [
      { name: 'a.md', content: '---\nid: py054\ntitle: a\n---' },
      { name: 'b.md', content: '---\nid: apcs005\ntitle: b\n---' },
    ]
    expect(computeNextId(files, 'apcs')).toBe('apcs006')
    expect(computeNextId(files, 'py')).toBe('py055')
  })

  it('fails loudly, naming the file, when an existing id does not match the id format', () => {
    const files = [{ name: 'legacy.md', content: '---\nid: 12\ntitle: old\n---' }]
    expect(() => computeNextId(files, 'py')).toThrow(/legacy\.md/)
  })

  it('fails loudly, naming the file, when a challenge file has no id line', () => {
    const files = [{ name: 'no-id.md', content: '---\ntitle: nope\n---' }]
    expect(() => computeNextId(files, 'py')).toThrow(/no-id\.md/)
  })

  it('ignores id lines outside the frontmatter block', () => {
    const files = [
      { name: 'body-id.md', content: '---\ntitle: nope\n---\n\n```yaml\nid: py099\n```\n' },
    ]
    expect(() => computeNextId(files, 'py')).toThrow(/body-id\.md/)
  })

  it('fails loudly instead of emitting an out-of-format id when the prefix is exhausted at 999', () => {
    const files = [{ name: 'max.md', content: '---\nid: py999\ntitle: max\n---' }]
    expect(() => computeNextId(files, 'py')).toThrow(/py1000/)
  })
})

describe('buildContent', () => {
  const base = {
    id: 'py001',
    name: 'bubble-sort',
    title: 'Bubble Sort',
    difficulty: 'easy',
    algorithm: 'bubble_sort',
    type: 'basic',
    category: 'python',
  }

  it('produces valid YAML frontmatter with all required fields', () => {
    const content = buildContent(base)
    expect(content).toContain('layout: challenge')
    expect(content).toContain('id: py001')
    expect(content).toContain('title: Bubble Sort')
    expect(content).toContain('difficulty: easy')
    expect(content).toContain('algorithm: bubble_sort')
    expect(content).toContain('testcase_count: 5')
    expect(content).toContain('params:')
    expect(content).toContain('generator: |')
    expect(content).toContain('starter_code: |')
  })

  it('includes default params skeleton with int type', () => {
    const content = buildContent(base)
    expect(content).toContain('type: int')
    expect(content).toContain('min: 1')
    expect(content).toContain('max: 10')
  })

  it('generator reads n and prints it (no syntax error)', () => {
    const content = buildContent(base)
    expect(content).toContain('n = int(input())')
    expect(content).toContain('print(n)')
  })

  it('starter_code has stub function and input read', () => {
    const content = buildContent(base)
    expect(content).toContain('def solve():')
    expect(content).toContain('n = int(input())')
  })

  it('includes all markdown body sections', () => {
    const content = buildContent(base)
    expect(content).toContain('## Bubble Sort')
    expect(content).toContain('### 演算法說明')
    expect(content).toContain('### 輸入說明')
    expect(content).toContain('### 輸出說明')
    expect(content).toContain('### 範例')
  })

  it('frontmatter is fenced with --- delimiters', () => {
    const content = buildContent(base)
    expect(content.startsWith('---\n')).toBe(true)
    const secondFence = content.indexOf('---\n', 4)
    expect(secondFence).toBeGreaterThan(4)
  })

  it('tags field is empty array', () => {
    const content = buildContent(base)
    expect(content).toContain('tags: []')
  })

  it('emits the resolved exercise type in frontmatter', () => {
    expect(buildContent({ ...base, type: 'basic' })).toContain('type: basic')
    expect(buildContent({ ...base, type: 'competition' })).toContain('type: competition')
  })

  it('emits the resolved category in frontmatter', () => {
    expect(buildContent({ ...base, category: 'python' })).toContain('category: python')
    expect(buildContent({ ...base, category: 'apcs' })).toContain('category: apcs')
  })

  it('places the category line right after the difficulty line', () => {
    const content = buildContent(base)
    expect(content).toMatch(/^difficulty: easy\ncategory: python$/m)
  })
})

describe('validateType', () => {
  it('accepts the implemented exercise types', () => {
    expect(validateType('basic')).toBeNull()
    expect(validateType('competition')).toBeNull()
  })

  it('rejects deferred / future / unknown types with a descriptive error', () => {
    for (const bad of ['gamified', 'fill_in_blank', 'guided', 'nonsense', '']) {
      const err = validateType(bad)
      expect(err, `expected '${bad}' to be rejected`).not.toBeNull()
      expect(err).toContain('--type')
    }
  })

  it('exposes exactly the implemented values in EXERCISE_TYPES', () => {
    expect([...EXERCISE_TYPES]).toEqual(['basic', 'competition'])
  })
})

describe('parseArgs --type', () => {
  it('defaults the type to basic when --type is omitted', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge'])
    expect(parsed?.type).toBe('basic')
  })

  it('parses an explicit --type', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--type', 'competition'])
    expect(parsed?.type).toBe('competition')
  })

  it('parses the --type=value equals syntax (not silently dropped)', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--type=competition'])
    expect(parsed?.type).toBe('competition')
  })

  it('supports the equals syntax for other flags too', () => {
    const parsed = parseArgs([
      'node',
      'new-challenge',
      'merge-sort',
      '--difficulty=hard',
      '--title=合併排序',
    ])
    expect(parsed?.difficulty).toBe('hard')
    expect(parsed?.title).toBe('合併排序')
  })
})

describe('validateCategory', () => {
  it('returns null for valid categories', () => {
    expect(validateCategory('python')).toBeNull()
    expect(validateCategory('apcs')).toBeNull()
  })

  it('returns exact error message for invalid category', () => {
    expect(validateCategory('foo')).toBe(
      '[new-challenge] ERROR: --category must be one of: python, apcs',
    )
    expect(validateCategory('')).not.toBeNull()
    expect(validateCategory('Python')).not.toBeNull()
  })
})

describe('parseArgs --category', () => {
  it('defaults the category to python when --category is omitted', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge'])
    expect(parsed?.category).toBe('python')
  })

  it('parses an explicit --category', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--category', 'apcs'])
    expect(parsed?.category).toBe('apcs')
  })

  it('parses the --category=value equals syntax (not silently dropped)', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--category=apcs'])
    expect(parsed?.category).toBe('apcs')
  })
})

describe('trailing validated flag with no value fails its validator (no silent default)', () => {
  // A forgotten value on a validated flag must not silently scaffold with the
  // default: the sentinel value fails the flag's own validator, which prints
  // the documented "must be one of" message and exits non-zero in main().
  it('trailing --category is rejected by validateCategory', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--category'])
    expect(parsed).not.toBeNull()
    expect(validateCategory(parsed!.category)).toBe(
      '[new-challenge] ERROR: --category must be one of: python, apcs',
    )
  })

  it('trailing --difficulty is rejected by validateDifficulty', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--difficulty'])
    expect(parsed).not.toBeNull()
    expect(validateDifficulty(parsed!.difficulty)).toBe(
      '[new-challenge] ERROR: --difficulty must be one of: easy, medium, hard',
    )
  })

  it('trailing --type is rejected by validateType', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--type'])
    expect(parsed).not.toBeNull()
    expect(validateType(parsed!.type)).not.toBeNull()
  })

  it('trailing --title keeps its documented default fallback', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--title'])
    expect(parsed?.title).toBe('My Challenge')
  })

  it('an adjacent --flag is never swallowed as a value', () => {
    // Regression: `foo --title --category apcs` used to yield title
    // '--category', name 'apcs' (overwriting foo), category 'python'.
    const parsed = parseArgs(['node', 'new-challenge', 'foo', '--title', '--category', 'apcs'])
    expect(parsed?.name).toBe('foo')
    expect(parsed?.title).toBe('Foo')
    expect(parsed?.category).toBe('apcs')
  })

  it('--flag=value still passes a literal leading-dash value explicitly', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'foo', '--title=--weird'])
    expect(parsed?.title).toBe('--weird')
  })
})

describe('--category scaffold scenarios', () => {
  it('omitting --category scaffolds frontmatter containing category: python', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge'])
    expect(parsed).not.toBeNull()
    expect(validateCategory(parsed!.category)).toBeNull()
    const content = buildContent({ id: 'py001', ...parsed! })
    expect(content).toContain('category: python')
  })

  it('--category apcs scaffolds frontmatter containing category: apcs', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--category', 'apcs'])
    expect(parsed).not.toBeNull()
    expect(validateCategory(parsed!.category)).toBeNull()
    const content = buildContent({ id: 'py001', ...parsed! })
    expect(content).toContain('category: apcs')
  })

  it('--category foo is rejected with the exact error message (main exits 1)', () => {
    const parsed = parseArgs(['node', 'new-challenge', 'my-challenge', '--category', 'foo'])
    expect(parsed?.category).toBe('foo')
    expect(validateCategory(parsed!.category)).toBe(
      '[new-challenge] ERROR: --category must be one of: python, apcs',
    )
  })
})

describe('EXERCISE_TYPES lockstep', () => {
  it('matches the data-layer exercise-type list', async () => {
    const shared = await import('../docs/shared/exercise-type.js')
    expect([...EXERCISE_TYPES]).toEqual([...shared.EXERCISE_TYPES])
  })
})

describe('CHALLENGE_CATEGORIES lockstep', () => {
  it('matches the data-layer challenge-category list', async () => {
    const shared = await import('../docs/shared/challenge-category.js')
    expect([...CHALLENGE_CATEGORIES]).toEqual([...shared.CHALLENGE_CATEGORIES])
  })
})
