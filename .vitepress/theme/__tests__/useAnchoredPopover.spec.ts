import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount, flushPromises, type VueWrapper } from '@vue/test-utils'
import { defineComponent, h, ref } from 'vue'
import { useAnchoredPopover } from '../composables/useAnchoredPopover'

/**
 * Host component factory: mounts a trigger button and (when open) a panel div,
 * wired through useAnchoredPopover. Panel is rendered in-tree (not teleported)
 * because positioning math, dismissal, and exclusion are all DOM-location
 * agnostic — Teleport behavior is covered by the component specs.
 */
function makeHost() {
  return defineComponent({
    setup(_, { expose }) {
      const anchorRef = ref<HTMLElement | null>(null)
      const panelRef = ref<HTMLElement | null>(null)
      const pop = useAnchoredPopover({ anchorRef, panelRef })
      expose({ pop })
      return () =>
        h('div', [
          h('button', { ref: anchorRef, class: 'anchor', onClick: pop.toggle }, 'open'),
          pop.isOpen.value
            ? h('div', { ref: panelRef, class: 'panel', tabindex: '-1', style: pop.panelStyle.value }, [
                h('input', { class: 'inner' }),
              ])
            : null,
        ])
    },
  })
}

type HostVm = { pop: ReturnType<typeof useAnchoredPopover> }

const wrappers: VueWrapper[] = []

function mountHost() {
  const w = mount(makeHost(), { attachTo: document.body })
  wrappers.push(w)
  return w
}

function stubAnchorRect(w: VueWrapper, rect: Partial<DOMRect>) {
  const el = w.find('.anchor').element as HTMLElement
  vi.spyOn(el, 'getBoundingClientRect').mockReturnValue({
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    width: 0,
    height: 0,
    x: 0,
    y: 0,
    toJSON: () => ({}),
    ...rect,
  } as DOMRect)
}

function setViewport(width: number, height: number) {
  Object.defineProperty(window, 'innerWidth', { value: width, configurable: true })
  Object.defineProperty(window, 'innerHeight', { value: height, configurable: true })
}

async function open(w: VueWrapper) {
  await w.find('.anchor').trigger('click')
  await flushPromises()
}

afterEach(() => {
  wrappers.splice(0).forEach((w) => w.unmount())
  vi.restoreAllMocks()
})

describe('useAnchoredPopover (Requirement: Anchored upward popover positioning)', () => {
  it('positions the panel above the anchor, right-aligned (fixed)', async () => {
    setViewport(1440, 900)
    const w = mountHost()
    stubAnchorRect(w, { top: 500, right: 800 })
    await open(w)
    const style = (w.vm as unknown as HostVm).pop.panelStyle.value
    expect(style.position).toBe('fixed')
    // bottom = innerHeight − rect.top + 8 = 900 − 500 + 8
    expect(style.bottom).toBe('408px')
    // right = innerWidth − rect.right = 1440 − 800
    expect(style.right).toBe('640px')
  })

  it('caps the panel height to the space above the anchor and scrolls internally', async () => {
    setViewport(1440, 900)
    const w = mountHost()
    stubAnchorRect(w, { top: 250, right: 800 })
    await open(w)
    const style = (w.vm as unknown as HostVm).pop.panelStyle.value
    // maxHeight = rect.top − 16 (8px gap above the anchor + 8px viewport margin)
    expect(style.maxHeight).toBe('234px')
    expect(style.overflowY).toBe('auto')
  })

  it('clamps maxHeight at 0 when the anchor sits at the viewport top', async () => {
    setViewport(1440, 900)
    const w = mountHost()
    stubAnchorRect(w, { top: 10, right: 800 })
    await open(w)
    expect((w.vm as unknown as HostVm).pop.panelStyle.value.maxHeight).toBe('0px')
  })

  it('re-measures the anchor after the panel renders (second positioning pass wins)', async () => {
    setViewport(1440, 900)
    const w = mountHost()
    const el = w.find('.anchor').element as HTMLElement
    const mk = (top: number, right: number) =>
      ({ top, right, bottom: 0, left: 0, width: 0, height: 0, x: 0, y: 0, toJSON: () => ({}) }) as DOMRect
    // First (pre-open) measurement differs from the post-nextTick one: the final
    // style must reflect the SECOND rect, proving the double-positioning pass
    // required by design D2 is still in place.
    vi.spyOn(el, 'getBoundingClientRect').mockReturnValueOnce(mk(500, 800)).mockReturnValue(mk(400, 700))
    await open(w)
    const style = (w.vm as unknown as HostVm).pop.panelStyle.value
    expect(style.bottom).toBe(`${900 - 400 + 8}px`)
    expect(style.right).toBe(`${1440 - 700}px`)
  })

  it('clamps offsets to keep at least 8px from viewport edges', async () => {
    setViewport(1024, 768)
    const w = mountHost()
    // Anchor below the viewport bottom and past the right edge → raw values negative.
    stubAnchorRect(w, { top: 790, right: 1100 })
    await open(w)
    const style = (w.vm as unknown as HostVm).pop.panelStyle.value
    expect(style.bottom).toBe('8px')
    expect(style.right).toBe('8px')
  })

  it('repositions on window resize while open', async () => {
    setViewport(1440, 900)
    const w = mountHost()
    stubAnchorRect(w, { top: 500, right: 800 })
    await open(w)
    setViewport(1000, 600)
    window.dispatchEvent(new Event('resize'))
    await flushPromises()
    const style = (w.vm as unknown as HostVm).pop.panelStyle.value
    expect(style.bottom).toBe(`${600 - 500 + 8}px`)
    expect(style.right).toBe(`${1000 - 800}px`)
  })
})

describe('useAnchoredPopover (Requirement: Popover dismissal and repositioning)', () => {
  it('toggle opens and closes', async () => {
    const w = mountHost()
    const vm = w.vm as unknown as HostVm
    await open(w)
    expect(vm.pop.isOpen.value).toBe(true)
    await w.find('.anchor').trigger('click')
    expect(vm.pop.isOpen.value).toBe(false)
  })

  it('closes on an outside mousedown', async () => {
    const w = mountHost()
    const vm = w.vm as unknown as HostVm
    await open(w)
    document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(vm.pop.isOpen.value).toBe(false)
  })

  it('does not close on a mousedown inside the anchor or the panel', async () => {
    const w = mountHost()
    const vm = w.vm as unknown as HostVm
    await open(w)
    w.find('.anchor').element.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(vm.pop.isOpen.value).toBe(true)
    w.find('.inner').element.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
    await flushPromises()
    expect(vm.pop.isOpen.value).toBe(true)
  })

  it('closes on Escape', async () => {
    const w = mountHost()
    const vm = w.vm as unknown as HostVm
    await open(w)
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await flushPromises()
    expect(vm.pop.isOpen.value).toBe(false)
  })

  it('closes even when an outside control stops mousedown propagation (capture phase)', async () => {
    // SplitPane's collapse chevron uses @mousedown.stop; a bubble-phase document
    // listener would never hear it and the popover would stay open across the
    // layout shift. Capture delivery cannot be stopped by the target's handler.
    const stopper = document.createElement('button')
    stopper.addEventListener('mousedown', (e) => e.stopPropagation())
    document.body.appendChild(stopper)
    try {
      const w = mountHost()
      const vm = w.vm as unknown as HostVm
      await open(w)
      stopper.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
      await flushPromises()
      expect(vm.pop.isOpen.value).toBe(false)
    } finally {
      stopper.remove()
    }
  })

  it('follows the anchor when a layout change moves it without any mousedown', async () => {
    // Keyboard-activated collapse (Enter on the chevron) produces no mousedown;
    // the rAF tracker must reposition the panel when the anchor rect changes.
    setViewport(1440, 900)
    const w = mountHost()
    const el = w.find('.anchor').element as HTMLElement
    const mk = (top: number, right: number) =>
      ({ top, right, bottom: 0, left: 0, width: 0, height: 0, x: 0, y: 0, toJSON: () => ({}) }) as DOMRect
    const spy = vi.spyOn(el, 'getBoundingClientRect').mockReturnValue(mk(500, 800))
    await open(w)
    expect((w.vm as unknown as HostVm).pop.panelStyle.value.right).toBe('640px')
    // The layout shifts (no mousedown, no resize event): anchor moves left.
    spy.mockReturnValue(mk(500, 600))
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
    expect((w.vm as unknown as HostVm).pop.panelStyle.value.right).toBe('840px')
  })

  it('moves focus into the panel on open, and back to the anchor on Escape', async () => {
    const w = mountHost()
    await open(w)
    expect(document.activeElement).toBe(w.find('.panel').element)
    // Focus a field inside the panel, then close via Escape: focus returns to
    // the anchor instead of being dropped to <body> with the panel.
    ;(w.find('.inner').element as HTMLElement).focus()
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await flushPromises()
    expect(document.activeElement).toBe(w.find('.anchor').element)
  })

  it('does not steal focus back when closed by an outside mousedown', async () => {
    const outside = document.createElement('button')
    document.body.appendChild(outside)
    try {
      const w = mountHost()
      await open(w)
      // Simulate the browser moving focus to the clicked element first, then
      // the document-level mousedown handler closing the popover.
      outside.focus()
      document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
      await flushPromises()
      expect((w.vm as unknown as HostVm).pop.isOpen.value).toBe(false)
      expect(document.activeElement).toBe(outside)
    } finally {
      outside.remove()
    }
  })

  it('removes document and window listeners on unmount', async () => {
    const docRemove = vi.spyOn(document, 'removeEventListener')
    const winRemove = vi.spyOn(window, 'removeEventListener')
    const w = mountHost()
    await open(w)
    w.unmount()
    const docEvents = docRemove.mock.calls.map((c) => c[0])
    const winEvents = winRemove.mock.calls.map((c) => c[0])
    expect(docEvents).toContain('mousedown')
    expect(docEvents).toContain('keydown')
    expect(winEvents).toContain('resize')
  })
})

describe('useAnchoredPopover (Requirement: Mutual exclusion between anchored popovers)', () => {
  it('opening one popover closes the other', async () => {
    const a = mountHost()
    const b = mountHost()
    const vmA = a.vm as unknown as HostVm
    const vmB = b.vm as unknown as HostVm
    await open(a)
    expect(vmA.pop.isOpen.value).toBe(true)
    await open(b)
    expect(vmA.pop.isOpen.value).toBe(false)
    expect(vmB.pop.isOpen.value).toBe(true)
  })

  it('unmounting an open popover clears the registry so others still work', async () => {
    const a = mountHost()
    await open(a)
    a.unmount()
    wrappers.splice(wrappers.indexOf(a), 1)
    const b = mountHost()
    const vmB = b.vm as unknown as HostVm
    await open(b)
    expect(vmB.pop.isOpen.value).toBe(true)
  })
})
