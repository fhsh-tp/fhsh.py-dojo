## MODIFIED Requirements

### Requirement: Tutor directory follows multi-subject layout

The `docs/tutor/` directory SHALL be organized into subject subdirectories (`py/`, `alg/`, `ds/`). Each subject directory SHALL contain chapter subdirectories named `chN/` (where N is a positive integer). Each chapter directory SHALL contain an `index.md` overview file and section files named `<chapter>-<section>.md` (e.g., `1-1.md`, `1-2.md`).

#### Scenario: Python subject directory structure

- **WHEN** the `docs/tutor/py/` directory is created
- **THEN** it SHALL contain `index.md` as the subject overview and subdirectories `ch1/`, `ch2/`, `ch3/`, `ch4/` corresponding to the four curriculum modules

#### Scenario: Chapter 1 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch1/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `1-1.md`, `1-2.md`, `1-3.md`, `1-4.md` corresponding to the sections in that chapter

#### Scenario: Chapter 2 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch2/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `2-1.md`, `2-2.md`, `2-3.md`, `2-4.md`, `2-5.md`, `2-6.md`, `2-7.md` corresponding to the seven sections in Module 2

#### Scenario: Chapter 2 index lists all seven sections

- **WHEN** the `docs/tutor/py/ch2/index.md` file is rendered
- **THEN** it SHALL display links to all seven sections: 2-1 (for + range), 2-2 (while), 2-3 (break + continue), 2-4 (list + linear search), 2-5 (bubble sort), 2-6 (dict + hash), 2-7 (summary)
