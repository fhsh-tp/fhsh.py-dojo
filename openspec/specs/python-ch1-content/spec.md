# python-ch1-content Specification

## Purpose

TBD - created by archiving change 'write-python-chapter-1'. Update Purpose after archive.

## Requirements

### Requirement: Chapter 1 section files exist with correct structure

The system SHALL provide four tutorial section files for Module 1 (Chapter 1) at `docs/tutor/py/ch1/`:
- `1-1.md` — I/O basics (print, input, Judge system)
- `1-2.md` — Variables, data types, arithmetic operators
- `1-3.md` — Boolean values and flow control (if-elif-else, flowcharts)
- `1-4.md` — Module 1 summary and self-check

Each section file MUST have valid frontmatter with `layout: doc`, `chapter: 1`, `section` matching the filename, and `createdTime` in ISO 8601 with `+08:00` timezone.

#### Scenario: Section files have correct frontmatter

- **WHEN** VitePress builds the site
- **THEN** all four section files are parsed successfully with valid frontmatter fields (layout, chapter, section, createdTime)

#### Scenario: Section files appear in sidebar navigation

- **WHEN** a user visits the Chapter 1 index page
- **THEN** the sidebar displays links to all four sections in order (1-1, 1-2, 1-3, 1-4)


<!-- @trace
source: write-python-chapter-1
updated: 2026-04-07
code:
  - docs/challenge/self-introduction.md
  - docs/challenge/beverage-cashier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/index.md
  - refs/Python-self_learning-outline.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/challenge/grade-level.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/hello-world.md
-->

---
### Requirement: Chapter 1 index links to all sections

The `docs/tutor/py/ch1/index.md` file MUST contain links to all four sections including the summary section (1-4).

#### Scenario: Index page lists all sections

- **WHEN** a user visits `/tutor/py/ch1/`
- **THEN** the page displays links to 1-1, 1-2, 1-3, and 1-4


<!-- @trace
source: write-python-chapter-1
updated: 2026-04-07
code:
  - docs/challenge/self-introduction.md
  - docs/challenge/beverage-cashier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/index.md
  - refs/Python-self_learning-outline.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/challenge/grade-level.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/hello-world.md
-->

---
### Requirement: Example challenges exist with working generators

The system SHALL provide three example challenges for Chapter 1:
- `hello-world` (id: 1) — string I/O
- `beverage-cashier` (id: 2) — integer arithmetic
- `leap-year` (id: 3) — conditional logic

Each challenge file MUST have `layout: challenge`, valid `params`, a correct `generator` script, and `starter_code`.

#### Scenario: Example challenge generators produce correct output

- **WHEN** the generator script is executed with valid test input matching the params specification
- **THEN** the generator produces the correct expected output for that input

#### Scenario: Example challenges are linked from tutorial sections

- **WHEN** a user reads section 1-1, 1-2, or 1-3
- **THEN** the section contains a `<ChallengeLink>` component pointing to the corresponding example challenge


<!-- @trace
source: write-python-chapter-1
updated: 2026-04-07
code:
  - docs/challenge/self-introduction.md
  - docs/challenge/beverage-cashier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/index.md
  - refs/Python-self_learning-outline.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/challenge/grade-level.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/hello-world.md
-->

---
### Requirement: Practice challenges exist for independent work

The system SHALL provide seven practice challenges:
- `self-introduction` (id: 4), `parrot-echo` (id: 5) — linked from 1-1
- `grade-average` (id: 6), `change-calculator` (id: 7), `seconds-converter` (id: 8) — linked from 1-2
- `grade-level` (id: 9), `triangle-check` (id: 10) — linked from 1-3

Each practice challenge MUST have valid params and a correct generator. Tutorial sections MUST reference practice challenges via `<ChallengeLink>` with a brief hint but no step-by-step walkthrough.

#### Scenario: Practice challenges are accessible from tutorial sections

- **WHEN** a user reads a tutorial section's practice area
- **THEN** ChallengeLink components resolve to valid challenge pages

#### Scenario: Practice challenge generators produce correct output

- **WHEN** a practice challenge generator is executed with valid test input
- **THEN** the generator produces the correct expected output


<!-- @trace
source: write-python-chapter-1
updated: 2026-04-07
code:
  - docs/challenge/self-introduction.md
  - docs/challenge/beverage-cashier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/index.md
  - refs/Python-self_learning-outline.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/challenge/grade-level.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/hello-world.md
-->

---
### Requirement: Image placeholders with Nano Banana Pro prompts

Each tutorial section MUST contain image placeholders using the markdown format `![圖N：description（AI 製圖）](figNN.png "prompt")`. Each section file MUST end with an Image Specification Appendix containing the fully expanded prompt for each image.

All image prompts MUST use American stick figure comic style with dialogue-driven panels (no narration boxes), Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Images follow visual style prefix convention

- **WHEN** an image prompt is read from the Image Specification Appendix
- **THEN** the prompt begins with the chapter's visual style prefix and includes panel-by-panel descriptions

#### Scenario: Visual rhythm rule is met

- **WHEN** a tutorial section is reviewed
- **THEN** every H2 section contains at least one visual element and no more than five consecutive paragraphs of pure text exist without a visual element

<!-- @trace
source: write-python-chapter-1
updated: 2026-04-07
code:
  - docs/challenge/self-introduction.md
  - docs/challenge/beverage-cashier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/index.md
  - refs/Python-self_learning-outline.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/challenge/grade-level.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/hello-world.md
-->