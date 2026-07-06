# progress-record-export Specification

## Purpose

TBD - created by archiving change 'add-student-progress-persistence'. Update Purpose after archive.

## Requirements

### Requirement: Student-initiated download in two formats

The system SHALL let a student download their recorded work for a challenge as a Markdown document intended for LLM analysis, including a canned prompt preamble, and as a JSON document suitable for machine aggregation.

#### Scenario: Download produces a file

- **WHEN** a student activates the download-record control on a challenge
- **THEN** a file is downloaded containing the challenge slug, title, and the recorded session data

---
### Requirement: Thinned export by default with full toggle

The default export SHALL be a thinned view that keeps meaningful change points and the last buffer before each run and submit, collapsing intermediate micro-edits. The student SHALL be able to switch to a full, untrimmed export. The full untrimmed timeline SHALL remain stored regardless of export choice.

#### Scenario: Default is thinned

- **WHEN** a student downloads without changing options
- **THEN** the exported document is the thinned view rather than every stored micro-edit

#### Scenario: Full export available

- **WHEN** the student selects the full option
- **THEN** the export contains every stored event for the session

---
### Requirement: Optional identity for teacher handoff

The export SHALL allow the student to optionally include a name and class, embedding them in the document content and the suggested filename. Filenames containing non-ASCII challenge titles SHALL have characters invalid in filenames removed.

#### Scenario: Identity embedded when provided

- **GIVEN** a student enters a name and class
- **WHEN** they download the record
- **THEN** the name and class appear in the document and the suggested filename, with invalid filename characters removed

---
### Requirement: Answer keys never exported

The export SHALL serialise only fields already present in the stored session snapshot and SHALL NOT include any hidden expected output. Each stored attempt SHALL carry the verdict-detail level captured at record time so the export re-verifies allowed fields at serialization.

#### Scenario: Hidden expected output excluded

- **GIVEN** a challenge whose verdict detail is hidden, so the student never saw expected output
- **WHEN** the student exports the record
- **THEN** the exported document contains no expected-output field for any testcase
