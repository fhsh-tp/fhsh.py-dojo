## ADDED Requirements

### Requirement: Download panel opens as an anchored upward popover

The download-record panel SHALL be presented via the shared anchored-popover mechanism: it SHALL open upward from the download control, fully visible at the challenge page's default layout height without requiring the student to expand the run/submit results area, on desktop and tablet viewports alike. On viewports too short for the full panel, the panel SHALL constrain its height and scroll internally rather than extend beyond the viewport top.

#### Scenario: Visible without expanding results area

- **GIVEN** a challenge page at its default layout height
- **WHEN** the student activates the download-record control
- **THEN** the entire panel (identity fields, full-export toggle, and download buttons) SHALL be visible without any further layout adjustment

#### Scenario: Short viewport scrolls internally

- **WHEN** the viewport is too short to display the full panel above the control
- **THEN** the panel SHALL cap its height and scroll its own content instead of overflowing the viewport

### Requirement: Download panel form state survives reopen

Values entered in the download panel (name, class, full-export toggle) SHALL be retained when the panel is closed and reopened within the same challenge page visit, including closes triggered by outside clicks or Escape.

#### Scenario: Identity fields retained after accidental dismiss

- **GIVEN** a student has typed a name into the panel
- **WHEN** the panel closes because the student clicks elsewhere, and the student reopens it
- **THEN** the previously entered name SHALL still be present
