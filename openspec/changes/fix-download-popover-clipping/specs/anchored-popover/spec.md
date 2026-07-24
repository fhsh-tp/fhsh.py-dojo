## ADDED Requirements

### Requirement: Anchored upward popover positioning

A shared anchored-popover mechanism SHALL position popover panels so they escape ancestor overflow clipping: the panel SHALL be rendered outside the clipping ancestor (teleported to the document body) with fixed positioning, its bottom edge placed above the anchor control's top edge and its right edge aligned to the anchor control's right edge, so the panel opens upward from its anchor. Computed offsets SHALL be clamped to keep at least 8px between the panel and the viewport edges. The mechanism SHALL cap the panel's height to the vertical space available above the anchor (derived from the anchor's live position, not from a viewport-height constant) and let the panel scroll its content internally when taller — so the panel top cannot extend beyond the viewport even when the anchor sits high (e.g. the results panel dragged tall on a short viewport).

#### Scenario: Panel fully visible despite clipped ancestor

- **GIVEN** an anchor control inside an overflow-hidden, height-constrained container
- **WHEN** the popover is opened at the container's default height
- **THEN** the panel SHALL be fully visible above the anchor without expanding the container

#### Scenario: Small viewport clamping

- **WHEN** the computed position would place the panel within 8px of a viewport edge
- **THEN** the offset SHALL be clamped so the panel keeps at least 8px from that edge

#### Scenario: Anchor high in a short viewport

- **GIVEN** the anchor sits high on the screen (e.g. the results panel dragged to its maximum height on a short viewport)
- **WHEN** the popover opens and the panel's natural height exceeds the space above the anchor
- **THEN** the panel SHALL cap its height to that space and scroll internally instead of extending beyond the viewport top

### Requirement: Popover dismissal and repositioning

An open anchored popover SHALL close when a mousedown occurs outside both the anchor and the panel, and SHALL close when the Escape key is pressed. Dismissal SHALL use the mousedown phase (not click) so that grabbing an adjacent drag handle closes the popover before the drag moves the anchor. Outside-mousedown detection SHALL be delivered in the event capture phase, so an intermediate control that stops event propagation (e.g. a layout-collapse control using a stop modifier) cannot bypass dismissal and leave the panel detached from a moved anchor. While open, the popover SHALL track the anchor's on-screen position and reposition the panel when a layout change moves the anchor without any mousedown (e.g. a keyboard-activated layout toggle), so the panel never detaches visually. Dismissal SHALL NOT be driven by focus leaving the anchor/panel: teleported panels sit outside the anchor's DOM order, so a focus-based close would break keyboard navigation and misfire when a click on non-focusable panel content resets focus to the document body. The panel SHALL be repositioned when the window is resized while open. All document and window listeners and any tracking loop SHALL be stopped when the owning component unmounts.

#### Scenario: Outside interaction closes before drag

- **GIVEN** an open popover whose anchor sits near a drag-resize handle
- **WHEN** the user presses the mouse button on the drag handle
- **THEN** the popover SHALL close before the drag changes the anchor's position

#### Scenario: Propagation-stopping control cannot bypass dismissal

- **GIVEN** an open popover and a page control that stops mousedown propagation (such as the panel-collapse chevron)
- **WHEN** the user presses the mouse button on that control
- **THEN** the popover SHALL still close

#### Scenario: Layout shift without mousedown keeps the panel attached

- **GIVEN** an open popover
- **WHEN** a layout change moves the anchor without producing a mousedown (such as a keyboard-activated collapse control)
- **THEN** the panel SHALL reposition to stay visually attached to the anchor

#### Scenario: Escape closes

- **WHEN** the user presses Escape while a popover is open
- **THEN** the popover SHALL close

### Requirement: Popover focus management

Opening an anchored popover SHALL move keyboard focus to the panel, so that the Tab key reaches the panel's controls even though the teleported panel sits outside the anchor's DOM order. When the popover closes while focus is inside the panel, focus SHALL return to the anchor; when the popover closes because the user interacted elsewhere, focus SHALL NOT be stolen from the element the user moved to.

#### Scenario: Keyboard user reaches panel controls

- **WHEN** a student opens a popover
- **THEN** focus SHALL move to the panel and a subsequent Tab SHALL reach the panel's first control

#### Scenario: Escape returns focus to the anchor

- **GIVEN** focus is on a control inside an open panel
- **WHEN** the student presses Escape
- **THEN** the popover SHALL close and focus SHALL return to the anchor control

#### Scenario: Outside click does not steal focus back

- **GIVEN** an open popover
- **WHEN** the student clicks a control elsewhere on the page
- **THEN** the popover SHALL close and focus SHALL remain with the clicked control

### Requirement: Mutual exclusion between anchored popovers

At most one anchored popover SHALL be open at a time. Opening an anchored popover SHALL automatically close any other anchored popover that is currently open, without requiring the popover components to reference each other.

#### Scenario: Opening one closes the other

- **GIVEN** popover A is open
- **WHEN** the user opens popover B
- **THEN** popover A SHALL close and popover B SHALL be open
