import { ref, onMounted, onUnmounted, nextTick, readonly, type Ref } from 'vue'

/**
 * useAnchoredPopover — shared anchored-popover behavior for action-bar popups.
 *
 * The challenge page's bottom action bar sits inside an `overflow-hidden`,
 * height-clamped flex column: an in-flow popover would be clipped by that
 * ancestor (z-index cannot escape overflow clipping). Callers therefore
 * teleport their panel to <body> and bind `panelStyle`, which positions the
 * panel `fixed`, opening UPWARD from the anchor: panel bottom just above the
 * anchor's top, right edges aligned, clamped to keep 8px from viewport edges,
 * and capped to the vertical space above the anchor (internal scroll beyond).
 *
 * Dismissal listens on `mousedown` (not `click`): the anchors sit next to the
 * drag-resizable results divider, so grabbing the handle must close the popover
 * BEFORE the drag shifts the anchor — otherwise the fixed panel would detach
 * from the (now-moved) anchor for the duration of the drag. The listener is
 * registered in the CAPTURE phase because controls like SplitPane's collapse
 * chevron stop mousedown propagation, which would starve a bubble listener.
 *
 * Layout shifts that move the anchor WITHOUT a mousedown (e.g. keyboard-
 * activated collapse) are handled by an rAF tracker that follows the anchor's
 * rect while the popover is open and repositions the panel when it moves.
 * Deliberately NOT handled via a document `focusin` close: teleported panels
 * sit at the end of <body>, so Tab from the anchor lands outside the panel and
 * a focus-based close would slam the popover shut on keyboard users — and a
 * mousedown on non-focusable text inside the panel resets focus to <body>,
 * which a focus-based close would misread as "outside".
 *
 * Focus management: the panel (callers give it `tabindex="-1"`) receives focus
 * on open so keyboard users Tab straight into its controls; if focus is still
 * inside the panel when it closes, it returns to the anchor.
 *
 * A module-level registry enforces mutual exclusion: opening any anchored
 * popover closes the one currently open, without the components knowing about
 * each other.
 */

interface AnchoredPopoverOptions {
  /** The trigger control the panel anchors to. */
  anchorRef: Ref<HTMLElement | null>
  /** The (teleported) panel element; used for outside-click detection. */
  panelRef: Ref<HTMLElement | null>
}

/** The close function of whichever anchored popover is currently open. */
let activeClose: (() => void) | null = null

export function useAnchoredPopover(options: AnchoredPopoverOptions) {
  const { anchorRef, panelRef } = options
  const isOpen = ref(false)
  const panelStyle = ref<Record<string, string>>({})

  let rafId: number | null = null
  let lastRectKey = ''

  function measureAnchor(): { rect: DOMRect; key: string } | null {
    const anchor = anchorRef.value
    if (!anchor) return null
    const rect = anchor.getBoundingClientRect()
    return { rect, key: `${rect.top}:${rect.right}` }
  }

  function positionPanel() {
    const measured = measureAnchor()
    if (!measured) return
    const { rect, key } = measured
    lastRectKey = key
    panelStyle.value = {
      position: 'fixed',
      bottom: `${Math.max(8, window.innerHeight - rect.top + 8)}px`,
      right: `${Math.max(8, window.innerWidth - rect.right)}px`,
      // Cap the panel to the space actually above the anchor (8px gap to the
      // anchor + 8px viewport margin). The results divider lets users drag the
      // bottom panel tall, so a fixed 100vh-based cap can still overflow the
      // viewport top; deriving from the anchor's live rect cannot. (In this
      // app's layout the bottom panel maxes out at 50% of the container, so
      // rect.top keeps a natural floor and the cap never collapses to ~0.)
      maxHeight: `${Math.max(0, rect.top - 16)}px`,
      overflowY: 'auto',
    }
  }

  function stopTracking() {
    if (rafId !== null) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
  }

  // Follow the anchor while open: any layout change that moves it (divider
  // drag would have closed us via mousedown first, but keyboard-activated
  // collapse or programmatic layout changes produce no mousedown) triggers a
  // reposition on the next frame, so the panel never detaches visually.
  function trackAnchor() {
    rafId = requestAnimationFrame(() => {
      if (!isOpen.value) {
        rafId = null
        return
      }
      const measured = measureAnchor()
      if (measured && measured.key !== lastRectKey) positionPanel()
      trackAnchor()
    })
  }

  function close() {
    const panel = panelRef.value
    const active = document.activeElement
    isOpen.value = false
    if (activeClose === close) activeClose = null
    stopTracking()
    // Hand focus back to the anchor only when it would otherwise be lost with
    // the panel (e.g. Escape while a field is focused). If the user clicked
    // elsewhere, focus already moved and must not be stolen back.
    if (panel && active instanceof HTMLElement && panel.contains(active)) {
      anchorRef.value?.focus()
    }
  }

  async function openPopover() {
    if (activeClose && activeClose !== close) activeClose()
    activeClose = close
    positionPanel()
    isOpen.value = true
    // Re-measure after the panel has rendered, matching the original
    // EditorSettingsPopover behavior for first-open sizing.
    await nextTick()
    positionPanel()
    // Move focus into the panel (callers set tabindex="-1") so Tab reaches its
    // controls: teleported panels live at the end of <body>, outside the
    // anchor's natural tab sequence.
    panelRef.value?.focus({ preventScroll: true })
    stopTracking()
    trackAnchor()
  }

  function toggle() {
    if (isOpen.value) close()
    else void openPopover()
  }

  function isInside(target: Node) {
    return Boolean(anchorRef.value?.contains(target) || panelRef.value?.contains(target))
  }
  // Capture phase — see the header comment for why bubble phase is not enough.
  function onDocumentPointerDown(e: MouseEvent) {
    if (!isOpen.value) return
    if (isInside(e.target as Node)) return
    close()
  }
  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') close()
  }
  function onReposition() {
    if (isOpen.value) positionPanel()
  }

  onMounted(() => {
    document.addEventListener('mousedown', onDocumentPointerDown, true)
    document.addEventListener('keydown', onKeydown)
    window.addEventListener('resize', onReposition)
  })
  onUnmounted(() => {
    document.removeEventListener('mousedown', onDocumentPointerDown, true)
    document.removeEventListener('keydown', onKeydown)
    window.removeEventListener('resize', onReposition)
    stopTracking()
    if (activeClose === close) activeClose = null
  })

  return {
    isOpen: readonly(isOpen),
    panelStyle: readonly(panelStyle),
    toggle,
    close,
  }
}
