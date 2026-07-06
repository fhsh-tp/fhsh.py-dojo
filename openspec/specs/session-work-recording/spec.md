# session-work-recording Specification

## Purpose

TBD - created by archiving change 'add-student-progress-persistence'. Update Purpose after archive.

## Requirements

### Requirement: Session timeline of edit, run, and submit events

The system SHALL record each work session as a time-ordered list of events discriminated by kind: an `edit` event carrying the full editor buffer, a `run` event carrying stdin, stdout, and any error, and a `submit` event carrying the submitted code and per-testcase verdicts. Because a run result carries no verdict or testcase index, the event type MUST be a discriminated union from the outset.

#### Scenario: Mixed events recorded in order

- **WHEN** a student edits code, runs it with custom input, edits again, and submits
- **THEN** the session contains edit, run, edit, and submit events in chronological order, each tagged with its kind and timestamp

---
### Requirement: Debounced editor capture configurable per challenge

Editor edits SHALL be captured by a debounced watcher on the editor buffer, snapshotting after the buffer has been idle for the configured debounce interval. The interval SHALL be read from the challenge frontmatter field `editor_capture_debounce_ms`, defaulting to 1000 milliseconds when the field is absent; out-of-range or non-integer values SHALL fall back to the default.

#### Scenario: Default debounce applied

- **GIVEN** a challenge whose frontmatter omits `editor_capture_debounce_ms`
- **WHEN** the student pauses typing for at least 1000 milliseconds
- **THEN** one edit snapshot of the current buffer is recorded

#### Scenario: Per-challenge override honoured

- **GIVEN** a challenge whose frontmatter sets `editor_capture_debounce_ms` to 300
- **WHEN** the student pauses typing for at least 300 milliseconds
- **THEN** an edit snapshot is recorded at that finer cadence

---
### Requirement: Consecutive identical edits deduplicated

The recorder SHALL skip an edit snapshot whose buffer content is identical to the previously recorded snapshot, so that no-op change events do not accumulate.

#### Scenario: Unchanged buffer not re-recorded

- **WHEN** a debounce fires but the buffer content equals the last recorded edit
- **THEN** no new edit event is appended

---
### Requirement: Run activity captured through a dedicated seam

The system SHALL capture Run (execute) activity as `run` events even though the execute path does not currently write to the shared executor store. Adding this capture MUST NOT change the observable return contract of the execute function.

#### Scenario: Run recorded without changing execute contract

- **WHEN** a student runs code with custom stdin from the run dialog
- **THEN** a `run` event carrying the stdin, stdout, and any error is appended to the current session, and the run dialog still returns its result to the caller as before
