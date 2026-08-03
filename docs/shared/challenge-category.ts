/**
 * Challenge-category taxonomy — single source of truth for the data layer.
 *
 * `python` is the default self-study track listed on `/challenges`; `apcs`
 * marks challenges targeting the APCS exam, listed on `/apcs-challenges`.
 * Extending the taxonomy means adding a value here first — the resolver, the
 * catalogue pages, and the authoring gate in `challenge-category.test.ts` all
 * key off this constant.
 */
export const CHALLENGE_CATEGORIES = ['python', 'apcs'] as const
export type ChallengeCategory = (typeof CHALLENGE_CATEGORIES)[number]

/**
 * Category → catalogue-page URL. `satisfies Record<ChallengeCategory, …>`
 * makes the compiler reject a map that forgets a URL entry — it does NOT
 * guarantee consumer exhaustiveness (HomeView hardcodes its two sections).
 * The `.md` pages sit outside vue-tsc, so the page-existence scan in
 * `challenge-category.test.ts` and the nav lockstep in `nav.test.ts` are the
 * loud counterparts for those surfaces.
 */
export const CATEGORY_LIST_URL = {
  python: '/challenges',
  apcs: '/apcs-challenges',
} as const satisfies Record<ChallengeCategory, string>

/** Union of the known catalogue-page URLs — a back-navigation target can only be one of these. */
export type CategoryListUrl = (typeof CATEGORY_LIST_URL)[ChallengeCategory]

/**
 * Resolve a raw frontmatter `category` value to a known category.
 *
 * Unlike a blind `as ChallengeCategory` cast, this validates at runtime: an
 * absent, mistyped, or wrong-cased value resolves to `python` rather than
 * being silently trusted — a typo can therefore never make a challenge vanish
 * from both catalogue pages. Authoring typos still fail loudly at test time
 * via the file-scan gate.
 */
export function resolveChallengeCategory(raw: unknown): ChallengeCategory {
  return (CHALLENGE_CATEGORIES as readonly unknown[]).includes(raw)
    ? (raw as ChallengeCategory)
    : 'python'
}
