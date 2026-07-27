/**
 * VitePress Vite plugin that strips answer-bearing fields from challenge
 * Markdown frontmatter during production builds: `generator` (computes
 * expected outputs) and `reference_solution` (a complete correct solution,
 * used only by the offline content-regression test). Shipping either would
 * hand students the answer.
 *
 * In dev mode the plugin is a no-op, preserving the current development flow.
 */
// Vite Plugin type — inlined to avoid pnpm hoisting dependency on vite package.
// This file is consumed by .vitepress/config.mts where vite is available at runtime.
interface Plugin {
  name: string
  enforce?: 'pre' | 'post'
  apply?: 'build' | 'serve'
  transform?(code: string, id: string): { code: string; map: null } | null
}

/**
 * Match challenge Markdown files only.
 * Paths look like: /path/to/docs/challenge/caesar-basic.md
 */
const CHALLENGE_RE = /\/challenge\/[^/]+\.md$/

/**
 * Frontmatter fields that must never reach the production bundle.
 */
const STRIPPED_FIELDS = ['generator', 'reference_solution'] as const

/**
 * Match a frontmatter field (YAML block scalar or inline). Handles both
 * `field: |` / `field: >` (block scalar: matched until the next unindented
 * line) and `field: "..."` (inline).
 */
function blockRe(field: string): RegExp {
  return new RegExp(`^${field}:\\s*[|>]-?\\s*\\n(?:[ \\t]+.*\\n?)*`, 'm')
}
function inlineRe(field: string): RegExp {
  return new RegExp(`^${field}:\\s*.+\\n?`, 'm')
}

export function stripGenerator(): Plugin {
  return {
    name: 'strip-generator',
    enforce: 'pre',
    apply: 'build', // only in production builds

    transform(code: string, id: string) {
      if (!CHALLENGE_RE.test(id)) return null
      if (!id.endsWith('.md')) return null

      // Find frontmatter boundaries
      const fmMatch = code.match(/^---\n([\s\S]*?)\n---/)
      if (!fmMatch) return null

      const fmStart = 4 // after "---\n"
      const fmEnd = fmStart + fmMatch[1]!.length
      let frontmatter = code.slice(fmStart, fmEnd)

      // Try block scalar first, then inline, for every stripped field
      for (const field of STRIPPED_FIELDS) {
        frontmatter = frontmatter.replace(blockRe(field), '')
        frontmatter = frontmatter.replace(inlineRe(field), '')
      }

      // Reconstruct the file
      const result = '---\n' + frontmatter + '\n---' + code.slice(fmEnd + 4) // +4 for "\n---"
      return { code: result, map: null }
    },
  }
}
