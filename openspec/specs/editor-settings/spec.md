# editor-settings Specification

## Purpose

TBD - created by archiving change 'add-editor-settings'. Update Purpose after archive.

## Requirements

### Requirement: Persistent editor settings

The system SHALL persist editor preference settings in `localStorage`, shared across all challenges and work sessions. Settings SHALL be read synchronously so the editor applies the user's choices on first render without flashing default behavior first.

#### Scenario: Settings persist across reloads

- **WHEN** a student changes an editor setting and reloads the page
- **THEN** the editor SHALL reflect the previously chosen setting

#### Scenario: Settings shared across challenges

- **WHEN** a student changes a setting on one challenge and navigates to another challenge
- **THEN** the other challenge's editor SHALL reflect the same setting

---
### Requirement: Default settings preserve current behavior

The system SHALL default both `autocomplete` and `closeBrackets` to enabled. A student who has never changed settings SHALL experience the same editor behavior as before this capability existed.

#### Scenario: First-time student sees defaults

- **WHEN** a student opens a challenge with no stored editor settings
- **THEN** autocomplete and bracket auto-closing SHALL both be enabled

---
### Requirement: Settings data contract with defaults merge and normalization

The stored settings object SHALL include a `version` field set to the current schema version of 2. On read, the system SHALL merge stored values over defaults to fill missing fields and SHALL normalize field types: boolean fields SHALL be coerced to boolean, and the numeric `fontSize` field SHALL be coerced to a valid integer by rounding to the nearest integer and clamping to the inclusive range 10 to 24, falling back to its default of 14 when the stored value is not a finite number. A stored object from schema version 1 (lacking `fontSize`) SHALL upgrade to version 2 by filling `fontSize` from its default while preserving the existing `autocomplete` and `closeBrackets` choices. Corrupt or partial stored data SHALL NOT cause an exception; it SHALL degrade to a valid settings object.

#### Scenario: Missing field filled from defaults

- **WHEN** the stored settings object lacks the `closeBrackets` field
- **THEN** reading settings SHALL return `closeBrackets` set to its default of enabled

#### Scenario: Version 1 object upgrades without losing choices

- **WHEN** the stored object is `{ version: 1, autocomplete: false }`
- **THEN** reading settings SHALL return `{ version: 2, autocomplete: false, closeBrackets: true, fontSize: 14 }`

##### Example: partial, corrupt, and numeric inputs

| Stored value | Result |
| ------------ | ------ |
| `{}` | `{ version: 2, autocomplete: true, closeBrackets: true, fontSize: 14 }` |
| `{ "autocomplete": false }` | `{ version: 2, autocomplete: false, closeBrackets: true, fontSize: 14 }` |
| `{ "fontSize": 100 }` | `fontSize` clamped to `24` |
| `{ "fontSize": 3 }` | `fontSize` clamped to `10` |
| `{ "fontSize": 15.6 }` | `fontSize` rounded to `16` |
| `{ "fontSize": "big" }` | `fontSize` falls back to `14` |
| invalid JSON | defaults returned, including `fontSize: 14` |

---
### Requirement: SSR-safe settings access

Accessing editor settings during server-side rendering SHALL NOT touch `localStorage` and SHALL return default values. When `localStorage` is unavailable (for example private-browsing mode), reads SHALL degrade to defaults and writes SHALL be no-ops, without breaking the editor or the challenge flow.

#### Scenario: SSR returns defaults

- **WHEN** editor settings are accessed in an environment without `window`
- **THEN** default settings SHALL be returned and no `localStorage` access SHALL occur

---
### Requirement: Live application without editor rebuild

Changing an editor setting SHALL take effect immediately via CodeMirror compartment reconfiguration, without recreating the editor view, preserving the cursor position and undo history.

#### Scenario: Toggle preserves cursor and history

- **WHEN** a student toggles a setting while editing
- **THEN** the setting SHALL apply immediately AND the cursor position and undo history SHALL be preserved

---
### Requirement: Editor settings entry point

The challenge page SHALL provide a gear control in the editor action bar that opens a settings popover containing the available toggles. The popover SHALL reflect current settings, SHALL close on an outside click, and SHALL close on the Escape key.

#### Scenario: Open and view toggles

- **WHEN** a student clicks the gear control
- **THEN** a popover SHALL appear containing an autocomplete toggle and a bracket auto-close toggle, each reflecting the current setting value

#### Scenario: Dismiss popover

- **WHEN** the popover is open and the student clicks outside it or presses Escape
- **THEN** the popover SHALL close

---
### Requirement: Adjustable editor font size

The system SHALL expose a numeric `fontSize` editor setting, expressed in pixels, that controls the code editor's font size. It SHALL default to 14, matching the editor's pre-existing appearance. Valid values SHALL be integers within the inclusive range 10 to 24; the system SHALL clamp out-of-range values to the nearest bound and SHALL round non-integer values to the nearest integer. Changing the font size SHALL take effect immediately via CodeMirror compartment reconfiguration, without recreating the editor view, preserving cursor position and undo history. The settings popover SHALL provide a stepper control — a decrease button, a current-value display, and an increase button — to adjust the font size, with the decrease button disabled at the minimum and the increase button disabled at the maximum. Resetting settings to defaults SHALL restore the font size to 14.

#### Scenario: Default font size matches prior appearance

- **WHEN** a student opens a challenge with no stored font size
- **THEN** the editor SHALL render text at 14px

#### Scenario: Increasing font size applies live

- **WHEN** a student clicks the increase control while editing
- **THEN** the editor font size SHALL grow by one step immediately AND the cursor position and undo history SHALL be preserved

##### Example: one increase step

- **GIVEN** the current font size is 14 and the cursor is at offset 5
- **WHEN** the student clicks the increase control once
- **THEN** the font size SHALL become 15px AND the cursor SHALL remain at offset 5

#### Scenario: Stepper respects bounds

- **WHEN** the font size is at 24, the maximum
- **THEN** the increase control SHALL be disabled

#### Scenario: Out-of-range stored value is clamped on read

- **WHEN** the stored font size is 100
- **THEN** reading settings SHALL return a font size of 24
