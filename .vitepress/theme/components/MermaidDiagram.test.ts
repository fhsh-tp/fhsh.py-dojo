// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'

// vi.mock is hoisted above module-scope declarations, so use vi.hoisted()
// to ensure the mock references are initialized before the factory runs.
const { mockRender, mockInitialize } = vi.hoisted(() => ({
  mockRender: vi.fn(),
  mockInitialize: vi.fn(),
}))

vi.mock('mermaid', () => ({
  default: {
    initialize: mockInitialize,
    render: mockRender,
  },
}))

// RED: This import will fail until MermaidDiagram.vue is created
import MermaidDiagram from './MermaidDiagram.vue'

describe('MermaidDiagram', () => {
  beforeEach(() => {
    mockRender.mockReset()
    mockInitialize.mockReset()
    mockRender.mockResolvedValue({ svg: '<svg><g>test diagram</g></svg>' })
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('accepts graph (URI-encoded) and id props', () => {
    const graph = encodeURIComponent('flowchart LR\nA-->B')
    const wrapper = mount(MermaidDiagram, {
      props: { graph, id: 'mermaid-0' },
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('calls mermaid.initialize on mount', async () => {
    const graph = encodeURIComponent('flowchart LR\nA-->B')
    mount(MermaidDiagram, { props: { graph, id: 'mermaid-0' } })
    await vi.waitFor(() => {
      expect(mockInitialize).toHaveBeenCalledWith(
        expect.objectContaining({
          startOnLoad: false,
          securityLevel: 'loose',
        }),
      )
    })
  })

  it('calls mermaid.render with id and decoded graph on mount', async () => {
    const originalGraph = 'flowchart LR\nA-->B'
    const graph = encodeURIComponent(originalGraph)
    mount(MermaidDiagram, { props: { graph, id: 'mermaid-0' } })
    await vi.waitFor(() => {
      expect(mockRender).toHaveBeenCalledWith('mermaid-0', originalGraph)
    })
  })

  it('renders SVG content into the DOM after mount', async () => {
    const graph = encodeURIComponent('flowchart LR\nA-->B')
    const wrapper = mount(MermaidDiagram, {
      props: { graph, id: 'mermaid-0' },
    })
    await vi.waitFor(() => {
      expect(wrapper.html()).toContain('<svg>')
    })
  })

  it('shows <pre> with error message when mermaid.render throws', async () => {
    mockRender.mockRejectedValue(new Error('invalid syntax'))
    const graph = encodeURIComponent('invalid!!!')
    const wrapper = mount(MermaidDiagram, {
      props: { graph, id: 'mermaid-err' },
    })
    await vi.waitFor(() => {
      expect(wrapper.find('pre').exists()).toBe(true)
      expect(wrapper.find('pre').text()).toContain('invalid syntax')
    })
  })
})
