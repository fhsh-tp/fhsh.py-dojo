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

The stored settings object SHALL include a `version` field. On read, the system SHALL merge stored values over defaults to fill missing fields and SHALL normalize field types, coercing boolean fields to boolean. Corrupt or partial stored data SHALL NOT cause an exception; it SHALL degrade to a valid settings object.

#### Scenario: Missing field filled from defaults

- **WHEN** the stored settings object lacks the `closeBrackets` field
- **THEN** reading settings SHALL return `closeBrackets` set to its default of enabled

##### Example: partial and corrupt inputs

| Stored value | Result |
| ------------ | ------ |
| `{}` | `{ version: 1, autocomplete: true, closeBrackets: true }` |
| `{ "autocomplete": false }` | `{ version: 1, autocomplete: false, closeBrackets: true }` |
| invalid JSON | defaults returned |

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
