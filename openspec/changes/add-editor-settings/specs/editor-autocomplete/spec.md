## MODIFIED Requirements

### Requirement: Automatic completion trigger

When the `autocomplete` editor setting is enabled (the default), the completion dropdown SHALL activate automatically after each keystroke without requiring a manual trigger key. When the `autocomplete` setting is disabled, the editor SHALL NOT display the completion dropdown on any keystroke.

#### Scenario: Completion appears without manual trigger

- **WHEN** the `autocomplete` setting is enabled AND the user types any character that matches a completion candidate
- **THEN** the completion dropdown SHALL appear automatically

#### Scenario: Completion suppressed when disabled

- **WHEN** the `autocomplete` setting is disabled AND the user types a character that would match a completion candidate
- **THEN** the editor SHALL NOT display the completion dropdown

### Requirement: Bracket auto-closing

When the `closeBrackets` editor setting is enabled (the default), the editor SHALL automatically insert the closing counterpart when the user types `(`, `[`, or `{`. Quote characters (`"`, `'`) SHALL NOT be auto-closed. When the `closeBrackets` setting is disabled, the editor SHALL NOT auto-insert any closing bracket.

#### Scenario: Opening parenthesis triggers auto-close

- **WHEN** the `closeBrackets` setting is enabled AND the user types `(`
- **THEN** the editor SHALL insert `)` and place the cursor between them

#### Scenario: Opening bracket triggers auto-close

- **WHEN** the `closeBrackets` setting is enabled AND the user types `[`
- **THEN** the editor SHALL insert `]` and place the cursor between them

#### Scenario: Opening brace triggers auto-close

- **WHEN** the `closeBrackets` setting is enabled AND the user types `{`
- **THEN** the editor SHALL insert `}` and place the cursor between them

#### Scenario: Quotes are NOT auto-closed

- **WHEN** the user types `"` or `'`
- **THEN** the editor SHALL NOT insert a matching closing quote

#### Scenario: Backspace on empty bracket pair deletes both characters

- **WHEN** the cursor is between an empty bracket pair (e.g., `(|)`) and the user presses Backspace
- **THEN** both the opening and closing brackets SHALL be deleted

#### Scenario: Auto-close suppressed when disabled

- **WHEN** the `closeBrackets` setting is disabled AND the user types `(`
- **THEN** the editor SHALL NOT insert a closing `)`
