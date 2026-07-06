/**
 * Derive the per-challenge slug (the markdown file basename, no extension)
 * from a content-loader `url`.
 *
 * This is the single, central place slug is parsed — both the catalogue loader
 * (from a content-loader `url`) and `ChallengeView` (from `page.relativePath`)
 * call it, instead of re-parsing at the presentation layer. The parse is robust
 * to:
 *   - a configured VitePress `base` prefix (e.g. `/py-dojo/`),
 *   - `cleanUrls` (a trailing `.html` present or absent), and
 *   - a raw source `relativePath` (a trailing `.md`, e.g. `challenge/foo.md`).
 *
 * It keys off the `/challenge/` path segment when present, falling back to the
 * last path segment otherwise, so both call sites resolve to the same slug.
 */
export function deriveChallengeSlug(url: string): string {
  const noExt = url.replace(/\.(html|md)$/, '').replace(/\/$/, '')
  const marker = '/challenge/'
  const idx = noExt.lastIndexOf(marker)
  return idx >= 0 ? noExt.slice(idx + marker.length) : (noExt.split('/').pop() ?? '')
}
