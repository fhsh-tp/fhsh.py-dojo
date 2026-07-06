import { describe, it, expect } from 'vitest'
import { deriveChallengeSlug } from './challenge-slug'

describe('deriveChallengeSlug', () => {
  it('strips the /challenge/ prefix and .html suffix', () => {
    expect(deriveChallengeSlug('/challenge/arithmetic-sum.html')).toBe('arithmetic-sum')
  })

  it('handles cleanUrls (no .html suffix)', () => {
    expect(deriveChallengeSlug('/challenge/arithmetic-sum')).toBe('arithmetic-sum')
  })

  it('strips a .md suffix (the source relativePath form ChallengeView passes)', () => {
    // ChallengeView calls deriveChallengeSlug(`/${page.relativePath}`), i.e.
    // `/challenge/arithmetic-sum.md`, so it must resolve to the same slug as the
    // catalogue derives from the rendered url — the two can never diverge.
    expect(deriveChallengeSlug('/challenge/arithmetic-sum.md')).toBe('arithmetic-sum')
  })

  it('is immune to a configured base prefix', () => {
    expect(deriveChallengeSlug('/py-dojo/challenge/bmi-classifier.html')).toBe('bmi-classifier')
  })

  it('handles a trailing slash', () => {
    expect(deriveChallengeSlug('/challenge/countdown/')).toBe('countdown')
  })

  it('falls back to the last path segment when no /challenge/ marker exists', () => {
    expect(deriveChallengeSlug('/foo/bar.html')).toBe('bar')
  })
})
