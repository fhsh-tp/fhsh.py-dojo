# challenge-completion-tracking Specification

## Purpose

TBD - created by archiving change 'add-student-progress-persistence'. Update Purpose after archive.

## Requirements

### Requirement: Completion recorded on fully-passing submit

The system SHALL record a challenge as completed only when a submission finishes with executor status `done` and all testcases pass. The write path MUST guard on status equal to `done` before evaluating completion, so an aborted run, which can leave passed and total both zero, is never recorded as completed.

#### Scenario: All testcases pass

- **WHEN** a submission completes with status `done`, passed equal to total, and total greater than zero
- **THEN** the challenge progress status becomes `completed` and the first-completion timestamp is set on first completion

#### Scenario: Aborted submission is not completed

- **GIVEN** a submission is started and then stopped before finishing
- **WHEN** the write path runs with executor status still `running` and passed equal to total equal to zero
- **THEN** no completion is recorded

---
### Requirement: Completion shown on catalogue

The catalogue SHALL display a completion badge on each completed challenge's card and a completed-count summary on the list page. The count SHALL be global, independent of the active difficulty or search filter.

#### Scenario: Badge and count reflect stored progress

- **GIVEN** 12 of 54 challenges are stored as completed
- **WHEN** the list page renders on the client
- **THEN** each completed challenge's card shows the badge and the page shows a "12 / 54 completed" style count regardless of the active filter

---
### Requirement: Best-effort progress semantics

Completion data SHALL be treated as best-effort local self-tracking and SHALL NOT be presented as an authoritative grade. Loss of local data through cleared storage or a different device is an accepted limitation.

#### Scenario: Progress absent on a fresh profile

- **WHEN** a student opens the site in a browser profile with no stored progress
- **THEN** zero challenges show as completed, the count reads 0 of 54, and no error is shown
