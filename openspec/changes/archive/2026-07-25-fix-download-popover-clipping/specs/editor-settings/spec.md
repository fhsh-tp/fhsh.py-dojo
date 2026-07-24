## MODIFIED Requirements

### Requirement: Editor settings entry point

The challenge page SHALL provide a gear control in the editor action bar that opens a settings popover containing the available toggles. The popover SHALL reflect current settings, SHALL close on an outside click, and SHALL close on the Escape key. The popover SHALL participate in the shared anchored-popover mutual exclusion: opening any other anchored popover SHALL close the settings popover, and opening the settings popover SHALL close any other anchored popover.

#### Scenario: Open and view toggles

- **WHEN** a student clicks the gear control
- **THEN** a popover SHALL appear containing an autocomplete toggle and a bracket auto-close toggle, each reflecting the current setting value

#### Scenario: Dismiss popover

- **WHEN** the popover is open and the student clicks outside it or presses Escape
- **THEN** the popover SHALL close

#### Scenario: Another popover opening closes settings

- **GIVEN** the settings popover is open
- **WHEN** the student opens the download-record popover
- **THEN** the settings popover SHALL close
