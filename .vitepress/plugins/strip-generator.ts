/**
 * VitePress Vite plugin that strips answer-bearing fields from challenge
 * Markdown frontmatter during production builds: `generator` (computes
 * expected outputs) and `reference_solution` (a complete correct solution,
 * used only by the offline content-regression test). Shipping either would
 * hand students the answer.
 *
 * Stripping is structural (line scanning by YAML indentation), not
 * scalar-style regex matching: block-scalar variants (`|`, `>`, `|-`, `|+`,
 * `|2`), header comments, quoted keys, blank lines inside the block, and
 * CRLF line endings are all handled uniformly. A post-strip assertion pass
 * re-parses the frontmatter and refuses to build on ANY discrepancy —
 * a stripped field surviving, another field damaged, or invalid YAML —
 * because the failure mode of this plugin is "publish the answers".
 *
 * In dev mode the plugin is a no-op, preserving the current development flow.
 */
import yaml from 'js-yaml'

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
 * Column-0 key line for a stripped field, tolerating quoted keys
 * (`generator:`, `"generator":`, `'generator':`) and space before the colon.
 */
function keyLineRe(field: string): RegExp {
  return new RegExp(`^(?:${field}|"${field}"|'${field}')[ \\t]*:`)
}

/** A line that starts a new top-level frontmatter entry (not blank, not indented). */
const TOP_LEVEL_LINE = /^[^ \t]/

/**
 * Structural, scalar-style-agnostic strip: delete the field's key line plus
 * every following blank or indented line — i.e. the entire YAML node.
 */
function stripFields(frontmatter: string): string {
  const lines = frontmatter.split('\n')
  const out: string[] = []
  let i = 0
  while (i < lines.length) {
    const line = lines[i]!
    if (!STRIPPED_FIELDS.some((f) => keyLineRe(f).test(line))) {
      out.push(line)
      i++
      continue
    }
    i++ // drop the key line
    // drop the node body: every blank or indented line that follows
    while (i < lines.length && (lines[i]!.trim() === '' || !TOP_LEVEL_LINE.test(lines[i]!))) i++
  }
  return out.join('\n')
}

export function stripGenerator(): Plugin {
  return {
    name: 'strip-generator',
    enforce: 'pre',
    apply: 'build', // only in production builds

    transform(code: string, id: string) {
      if (!CHALLENGE_RE.test(id)) return null
      if (!id.endsWith('.md')) return null

      // Find frontmatter boundaries (tolerate CRLF)
      const fmMatch = code.match(/^---\r?\n([\s\S]*?)\r?\n---/)
      if (!fmMatch) {
        // Fail loud: a challenge file whose frontmatter we cannot locate
        // would ship its generator verbatim.
        if (/^\uFEFF?\s*---/.test(code)) {
          throw new Error(
            `[strip-generator] ${id}: frontmatter delimiters found but not parseable; refusing to build.`,
          )
        }
        return null
      }

      const raw = fmMatch[1]!
      const stripped = stripFields(raw)

      // --- fail-loud post-strip assertions --------------------------------
      let before: unknown
      try {
        before = yaml.load(raw)
      } catch (e) {
        throw new Error(
          `[strip-generator] ${id}: source frontmatter is already invalid YAML ` +
            `(${(e as Error).message.split('\n')[0]}). Fix the file.`,
        )
      }
      let after: unknown
      try {
        after = yaml.load(stripped)
      } catch (e) {
        throw new Error(
          `[strip-generator] ${id}: frontmatter is not valid YAML after stripping ` +
            `(${(e as Error).message.split('\n')[0]}). Refusing to build.`,
        )
      }
      if (after && typeof after === 'object' && before && typeof before === 'object') {
        const a = after as Record<string, unknown>
        const b = before as Record<string, unknown>
        for (const f of STRIPPED_FIELDS) {
          if (f in a) {
            throw new Error(
              `[strip-generator] ${id}: field "${f}" survived stripping. Refusing to build.`,
            )
          }
        }
        for (const k of Object.keys(b)) {
          if ((STRIPPED_FIELDS as readonly string[]).includes(k)) continue
          if (!(k in a) || JSON.stringify(a[k]) !== JSON.stringify(b[k])) {
            throw new Error(
              `[strip-generator] ${id}: field "${k}" was damaged by stripping. Refusing to build.`,
            )
          }
        }
      }
      // --------------------------------------------------------------------

      const fmStart = code.indexOf('\n') + 1
      const fmEnd = fmStart + raw.length
      return { code: code.slice(0, fmStart) + stripped + code.slice(fmEnd), map: null }
    },
  }
}
