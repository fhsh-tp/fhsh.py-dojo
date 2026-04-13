/**
 * markdown-it plugin for VitePress that converts mermaid fenced code blocks
 * into `<ClientOnly><MermaidDiagram ... /></ClientOnly>` Vue component markup.
 *
 * Language identifiers handled: `mermaid`, `mmd`
 */

// markdown-it Plugin type — inlined to avoid importing from a package that
// VitePress 2.x does not publicly export (MarkdownItAsync is internal).
// Matches the inline pattern used in strip-generator.ts.
interface Plugin {
  (md: any): void
}

export const mermaidPlugin: Plugin = (md: any): void => {
  // D5: save the original fence rule before overriding
  const originalFence = md.renderer.rules.fence.bind(md.renderer.rules)

  md.renderer.rules.fence = (
    tokens: any[],
    idx: number,
    options: any,
    env: any,
    self: any,
  ): string => {
    const token = tokens[idx]
    const lang = token.info.trim()

    if (lang === 'mermaid' || lang === 'mmd') {
      // D3: wrap in <ClientOnly> (not <Suspense>)
      const encoded = encodeURIComponent(token.content.trim())
      return `<ClientOnly><MermaidDiagram id="mermaid-${idx}" graph="${encoded}" /></ClientOnly>\n`
    }

    // Delegate all other languages to the original renderer
    return originalFence(tokens, idx, options, env, self)
  }
}
