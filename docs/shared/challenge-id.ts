import type { ChallengeCategory } from './challenge-category'

/**
 * Challenge id scheme — single source of truth shared by the data layer,
 * the catalogue search, and the build scripts (scaffold, redirects).
 *
 * An id is `<category prefix><3-digit zero-padded ordinal>` (py001, apcs003).
 * Zero-padding makes plain lexicographic comparison equal ordinal order
 * within one prefix; every user-facing list is category-filtered before an
 * order is shown, so the cross-prefix ordering (apcs before py) carries no
 * user-facing meaning.
 */
export const CHALLENGE_ID_PATTERN = /^(py|apcs)\d{3}$/

/**
 * Category → id prefix. Adding a category means registering its prefix here
 * first — the pattern above, the scaffold's per-category numbering, and the
 * redirects generator all key off this map. Prefixes must never be a prefix
 * of one another, or startsWith id search stops distinguishing them; the
 * challenge-id gate test pins that invariant.
 */
export const CATEGORY_ID_PREFIX = {
  python: 'py',
  apcs: 'apcs',
} as const satisfies Record<ChallengeCategory, string>

/** Ordinal of an id: the decimal integer after the leading non-digit prefix. */
export function challengeIdOrdinal(id: string): number {
  return parseInt(id.replace(/^\D*/, ''), 10)
}

/**
 * Comparator for ordering challenges by id. Plain code-unit comparison, NOT
 * locale-aware collation: build output (the redirects file) must be
 * byte-reproducible across machines, and ICU collation varies by runtime.
 */
export function compareChallengeId(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0
}

/** The first `---`…`---` frontmatter block of a markdown file, or null. */
export function extractFrontmatter(content: string): string | null {
  const m = content.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  return m ? m[1]! : null
}

/**
 * The frontmatter `id` value of a challenge markdown file, or null when the
 * frontmatter is missing or has no id line. Scoped to the frontmatter block so
 * an `id:` line in body text or a fenced code block can never be picked up.
 */
export function extractFrontmatterId(content: string): string | null {
  const m = extractFrontmatter(content)?.match(/^id:\s*(\S+)\s*$/m)
  return m ? m[1]! : null
}
