# editor-autocomplete Specification

## Purpose

Defines the CodeMirror editor's autocompletion and bracket auto-closing behavior for Python code. Includes Python keyword and builtin completions, document-local identifier completions, standard library symbol completions with module detail, automatic completion triggering, and bracket auto-closing for parentheses, brackets, and braces.

### Requirement: Python keyword and builtin autocompletion

The editor SHALL provide autocompletion for Python keywords (e.g., `if`, `for`, `def`, `class`, `return`) and built-in functions (e.g., `print`, `len`, `range`, `int`, `str`) sourced from `@codemirror/lang-python`.

#### Scenario: Keyword completion appears on typing

- **WHEN** the user types a partial Python keyword (e.g., `de`)
- **THEN** the completion dropdown SHALL appear and include `def` as a candidate

#### Scenario: Builtin function completion appears on typing

- **WHEN** the user types a partial builtin name (e.g., `pri`)
- **THEN** the completion dropdown SHALL include `print` as a candidate


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Document-local identifier completion

The editor SHALL scan the current document and offer completions for identifiers (variable names, function names) already present in the document.

#### Scenario: Local variable appears as completion candidate

- **WHEN** the user has previously typed `my_key = 3` and then types `my`
- **THEN** the completion dropdown SHALL include `my_key` as a candidate


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Stdlib static completion list

The editor SHALL provide completions for commonly used Python standard library symbols from the following modules: `math`, `string`, `hashlib`, `binascii`, `collections`, `itertools`, `functools`, `re`.

Each module name SHALL appear as a `namespace` type completion with `detail: 'module'`. Each exported symbol SHALL include the module name as the `detail` field.

Function entries in the stdlib list SHALL have an `apply` field ending with `(` to trigger bracket auto-close upon acceptance.

#### Scenario: Stdlib module name appears as completion

- **WHEN** the user types `hash`
- **THEN** the completion dropdown SHALL include `hashlib` with type `namespace` and `detail: 'module'`

#### Scenario: Stdlib symbol appears with module detail

- **WHEN** the user types `sha`
- **THEN** the completion dropdown SHALL include `sha256` with `detail: 'hashlib'`

#### Scenario: Accepting a function completion inserts opening bracket

- **WHEN** the user accepts a function completion entry (e.g., `sha256`)
- **THEN** the editor SHALL insert `sha256(` and `closeBrackets()` SHALL automatically add `)`, placing the cursor inside `sha256(|)`


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Automatic completion trigger

The completion dropdown SHALL activate automatically after each keystroke without requiring a manual trigger key.

#### Scenario: Completion appears without manual trigger

- **WHEN** the user types any character that matches a completion candidate
- **THEN** the completion dropdown SHALL appear automatically


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Bracket auto-closing

The editor SHALL automatically insert the closing counterpart when the user types `(`, `[`, or `{`. Quote characters (`"`, `'`) SHALL NOT be auto-closed.

#### Scenario: Opening parenthesis triggers auto-close

- **WHEN** the user types `(`
- **THEN** the editor SHALL insert `)` and place the cursor between them

#### Scenario: Opening bracket triggers auto-close

- **WHEN** the user types `[`
- **THEN** the editor SHALL insert `]` and place the cursor between them

#### Scenario: Opening brace triggers auto-close

- **WHEN** the user types `{`
- **THEN** the editor SHALL insert `}` and place the cursor between them

#### Scenario: Quotes are NOT auto-closed

- **WHEN** the user types `"` or `'`
- **THEN** the editor SHALL NOT insert a matching closing quote

#### Scenario: Backspace on empty bracket pair deletes both characters

- **WHEN** the cursor is between an empty bracket pair (e.g., `(|)`) and the user presses Backspace
- **THEN** both the opening and closing brackets SHALL be deleted


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Excluded stdlib modules

The stdlib completion list SHALL NOT include `os` or `sys` module entries.

#### Scenario: os module is not offered as completion

- **WHEN** the user types `os`
- **THEN** the completion dropdown SHALL NOT include `os` as a namespace candidate from the stdlib list

#### Scenario: sys module is not offered as completion

- **WHEN** the user types `sy`
- **THEN** the completion dropdown SHALL NOT include `sys` as a namespace candidate from the stdlib list

## Requirements


<!-- @trace
source: codemirror-autocomplete
updated: 2026-03-16
code:
  - .vitepress/theme/components/editor/CodeEditor.vue
  - .vitepress/theme/composables/pythonCompletions.ts
  - package.json
tests:
  - .vitepress/theme/__tests__/pythonCompletions.spec.ts
  - .vitepress/theme/__tests__/CodeEditor.spec.ts
-->

### Requirement: Python keyword and builtin autocompletion

The editor SHALL provide autocompletion for Python keywords (e.g., `if`, `for`, `def`, `class`, `return`) and built-in functions (e.g., `print`, `len`, `range`, `int`, `str`) sourced from `@codemirror/lang-python`.

#### Scenario: Keyword completion appears on typing

- **WHEN** the user types a partial Python keyword (e.g., `de`)
- **THEN** the completion dropdown SHALL appear and include `def` as a candidate

#### Scenario: Builtin function completion appears on typing

- **WHEN** the user types a partial builtin name (e.g., `pri`)
- **THEN** the completion dropdown SHALL include `print` as a candidate

---
### Requirement: Document-local identifier completion

The editor SHALL scan the current document and offer completions for identifiers (variable names, function names) already present in the document.

#### Scenario: Local variable appears as completion candidate

- **WHEN** the user has previously typed `my_key = 3` and then types `my`
- **THEN** the completion dropdown SHALL include `my_key` as a candidate

---
### Requirement: Stdlib static completion list

The editor SHALL provide completions for commonly used Python standard library symbols from the following modules: `math`, `string`, `hashlib`, `binascii`, `collections`, `itertools`, `functools`, `re`.

Each module name SHALL appear as a `namespace` type completion with `detail: 'module'`. Each exported symbol SHALL include the module name as the `detail` field.

Function entries in the stdlib list SHALL have an `apply` field ending with `(` to trigger bracket auto-close upon acceptance.

#### Scenario: Stdlib module name appears as completion

- **WHEN** the user types `hash`
- **THEN** the completion dropdown SHALL include `hashlib` with type `namespace` and `detail: 'module'`

#### Scenario: Stdlib symbol appears with module detail

- **WHEN** the user types `sha`
- **THEN** the completion dropdown SHALL include `sha256` with `detail: 'hashlib'`

#### Scenario: Accepting a function completion inserts opening bracket

- **WHEN** the user accepts a function completion entry (e.g., `sha256`)
- **THEN** the editor SHALL insert `sha256(` and `closeBrackets()` SHALL automatically add `)`, placing the cursor inside `sha256(|)`

---
### Requirement: Automatic completion trigger

The completion dropdown SHALL activate automatically after each keystroke without requiring a manual trigger key.

#### Scenario: Completion appears without manual trigger

- **WHEN** the user types any character that matches a completion candidate
- **THEN** the completion dropdown SHALL appear automatically

---
### Requirement: Bracket auto-closing

The editor SHALL automatically insert the closing counterpart when the user types `(`, `[`, or `{`. Quote characters (`"`, `'`) SHALL NOT be auto-closed.

#### Scenario: Opening parenthesis triggers auto-close

- **WHEN** the user types `(`
- **THEN** the editor SHALL insert `)` and place the cursor between them

#### Scenario: Opening bracket triggers auto-close

- **WHEN** the user types `[`
- **THEN** the editor SHALL insert `]` and place the cursor between them

#### Scenario: Opening brace triggers auto-close

- **WHEN** the user types `{`
- **THEN** the editor SHALL insert `}` and place the cursor between them

#### Scenario: Quotes are NOT auto-closed

- **WHEN** the user types `"` or `'`
- **THEN** the editor SHALL NOT insert a matching closing quote

#### Scenario: Backspace on empty bracket pair deletes both characters

- **WHEN** the cursor is between an empty bracket pair (e.g., `(|)`) and the user presses Backspace
- **THEN** both the opening and closing brackets SHALL be deleted

---
### Requirement: Excluded stdlib modules

The stdlib completion list SHALL NOT include `os` or `sys` module entries.

#### Scenario: os module is not offered as completion

- **WHEN** the user types `os`
- **THEN** the completion dropdown SHALL NOT include `os` as a namespace candidate from the stdlib list

#### Scenario: sys module is not offered as completion

- **WHEN** the user types `sy`
- **THEN** the completion dropdown SHALL NOT include `sys` as a namespace candidate from the stdlib list