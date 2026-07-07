## ADDED Requirements

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

## MODIFIED Requirements

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
