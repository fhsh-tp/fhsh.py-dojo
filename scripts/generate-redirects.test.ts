// @vitest-environment node
import { readdirSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, it, expect } from 'vitest'
import { buildRedirects } from './generate-redirects.js'

/** Minimal challenge frontmatter carrying just the id line the generator reads. */
function fm(id: string): string {
  return `---\nlayout: challenge\nid: ${id}\ntitle: stub\n---\n\nbody\n`
}

/** Non-empty lines of the generated `_redirects` payload. */
function lines(output: string): string[] {
  return output.split('\n').filter((l) => l !== '')
}

describe('buildRedirects line format', () => {
  it('emits `/c/<id> /challenge/<slug> 302` for each file', () => {
    const output = buildRedirects([{ name: 'collatz-steps.md', content: fm('py031') }])
    expect(lines(output)).toContain('/c/py031 /challenge/collatz-steps 302')
  })

  it('every line is a 302 rule with a /c/<id> source and a /challenge/<slug> target', () => {
    const output = buildRedirects([
      { name: 'collatz-steps.md', content: fm('py031') },
      { name: 'two-sum.md', content: fm('apcs002') },
    ])
    for (const line of lines(output)) {
      expect(line).toMatch(/^\/c\/(py|apcs)\d{3} \/challenge\/[^ ]+ 302$/)
    }
  })

  it('emits no /challenge/<id>-form source path — the pre-/c/ alias is fully replaced', () => {
    const output = buildRedirects([
      { name: 'collatz-steps.md', content: fm('py031') },
      { name: 'two-sum.md', content: fm('apcs002') },
    ])
    for (const line of lines(output)) {
      expect(line.split(' ')[0]).not.toMatch(/^\/challenge\/(py|apcs)\d{3}$/)
    }
  })
})

describe('buildRedirects coverage', () => {
  it('emits exactly one line per input file, with no duplicate source paths', () => {
    const files = [
      { name: 'alpha.md', content: fm('py001') },
      { name: 'bravo.md', content: fm('py002') },
      { name: 'charlie.md', content: fm('apcs001') },
    ]
    const output = lines(buildRedirects(files))
    expect(output).toHaveLength(files.length)
    const sources = output.map((l) => l.split(' ')[0])
    expect(new Set(sources).size).toBe(files.length)
  })
})

describe('buildRedirects target extension', () => {
  it('targets never carry a .html extension', () => {
    const output = buildRedirects([
      { name: 'alpha.md', content: fm('py001') },
      { name: 'bravo.md', content: fm('apcs003') },
    ])
    expect(output).not.toContain('.html')
  })
})

describe('buildRedirects ordering', () => {
  it('orders lines by id regardless of input order (stable, reproducible)', () => {
    const shuffled = [
      { name: 'cherry.md', content: fm('py010') },
      { name: 'apple.md', content: fm('apcs002') },
      { name: 'banana.md', content: fm('py002') },
    ]
    const output = lines(buildRedirects(shuffled))
    expect(output).toEqual([
      '/c/apcs002 /challenge/apple 302',
      '/c/py002 /challenge/banana 302',
      '/c/py010 /challenge/cherry 302',
    ])
    // Same files in a different order must produce the identical payload.
    expect(buildRedirects([...shuffled].reverse())).toBe(buildRedirects(shuffled))
  })
})

describe('buildRedirects fail-loud validation', () => {
  it('throws naming the file when a challenge file has no id line', () => {
    const files = [
      { name: 'alpha.md', content: fm('py001') },
      { name: 'no-id.md', content: '---\nlayout: challenge\ntitle: nope\n---\n' },
    ]
    expect(() => buildRedirects(files)).toThrow(/no-id\.md/)
  })

  it('throws naming the file when an id does not match the challenge id format', () => {
    const files = [{ name: 'legacy.md', content: fm('12') }]
    expect(() => buildRedirects(files)).toThrow(/legacy\.md/)
  })

  it('throws naming both files when two files share the same id', () => {
    const files = [
      { name: 'first.md', content: fm('py007') },
      { name: 'second.md', content: fm('py007') },
    ]
    expect(() => buildRedirects(files)).toThrow(/first\.md/)
    expect(() => buildRedirects(files)).toThrow(/second\.md/)
  })

  it('throws naming the file when the filename falls outside the slug contract', () => {
    // A space (or worse, a newline) in the slug would corrupt the
    // whitespace-delimited _redirects line format — reject at build time.
    const files = [{ name: 'bad name.md', content: fm('py001') }]
    expect(() => buildRedirects(files)).toThrow(/bad name\.md/)
  })

  it('ignores id lines outside the frontmatter block (body text, code fences)', () => {
    const bodyOnly =
      '---\nlayout: challenge\ntitle: nope\n---\n\n```yaml\nid: py099\n```\nid: py098\n'
    expect(() => buildRedirects([{ name: 'body-id.md', content: bodyOnly }])).toThrow(/body-id\.md/)
  })

  it('throws naming the file when a filename is id-shaped (catalogue identity confusion)', () => {
    // An id-shaped slug no longer collides with the /c/ alias rules, but
    // /challenge/py001 (slug) and /c/py001 (alias) could then name two
    // different challenges — reject at build time.
    const files = [{ name: 'py001.md', content: fm('py055') }]
    expect(() => buildRedirects(files)).toThrow(/py001\.md/)
  })

  it('throws instead of emitting an empty redirects payload when no files are found', () => {
    expect(() => buildRedirects([])).toThrow(/no challenge markdown files/)
  })
})

describe('buildRedirects against the real docs/challenge/', () => {
  it('emits one redirect line per challenge markdown file', async () => {
    const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
    const challengeDir = join(projectRoot, 'docs', 'challenge')
    const mdFiles = readdirSync(challengeDir).filter((f) => f.endsWith('.md'))
    const { readChallengeFiles } = await import('./generate-redirects.js')
    const output = lines(buildRedirects(readChallengeFiles(challengeDir)))
    expect(output).toHaveLength(mdFiles.length)
  })
})
