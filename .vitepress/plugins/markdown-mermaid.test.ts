// @vitest-environment node
import { describe, it, expect, beforeEach } from 'vitest'

// RED: This import will fail until markdown-mermaid.ts is created
import { mermaidPlugin } from './markdown-mermaid'

function makeOriginalFence() {
  let called = false
  const fn = (_tokens: unknown[], _idx: number) => {
    called = true
    return '<original-fence/>'
  }
  return { fn, wasCalled: () => called }
}

function createMockMd(originalFence: (...args: unknown[]) => string): any {
  return {
    renderer: {
      rules: {
        fence: originalFence,
      },
    },
  }
}

function callFence(md: any, lang: string, content: string): string {
  return md.renderer.rules.fence(
    [{ info: lang, content, map: null }],
    0,
    {},
    {},
    { renderToken: () => '' },
  )
}

describe('mermaidPlugin', () => {
  let originalFence: ReturnType<typeof makeOriginalFence>
  let md: any

  beforeEach(() => {
    originalFence = makeOriginalFence()
    md = createMockMd(originalFence.fn)
    mermaidPlugin(md)
  })

  it('converts mermaid fence to ClientOnly + MermaidDiagram', () => {
    const result = callFence(md, 'mermaid', 'flowchart LR\nA-->B\n')
    expect(result).toContain('<ClientOnly>')
    expect(result).toContain('<MermaidDiagram')
    expect(result).toContain('</ClientOnly>')
  })

  it('does NOT output a <code> block for mermaid fences', () => {
    const result = callFence(md, 'mermaid', 'flowchart LR\nA-->B\n')
    expect(result).not.toContain('<code')
  })

  it('encodes graph content with encodeURIComponent', () => {
    const content = 'flowchart LR\n  A --> B'
    const result = callFence(md, 'mermaid', content)
    expect(result).toContain(encodeURIComponent(content.trim()))
  })

  it('handles mmd alias the same as mermaid', () => {
    const result = callFence(md, 'mmd', 'flowchart LR\nA-->B\n')
    expect(result).toContain('<ClientOnly>')
    expect(result).toContain('<MermaidDiagram')
  })

  it('delegates non-mermaid fences to original renderer', () => {
    const result = callFence(md, 'js', 'console.log("hi")')
    expect(result).toBe('<original-fence/>')
    expect(originalFence.wasCalled()).toBe(true)
  })

  it('includes id prop based on token index', () => {
    const result = callFence(md, 'mermaid', 'flowchart LR\nA-->B\n')
    expect(result).toContain('id="mermaid-0"')
  })

  it('trims content before encoding', () => {
    const content = '  flowchart LR\n  A-->B\n  '
    const result = callFence(md, 'mermaid', content)
    expect(result).toContain(encodeURIComponent(content.trim()))
    expect(result).not.toContain(encodeURIComponent(content))
  })
})
