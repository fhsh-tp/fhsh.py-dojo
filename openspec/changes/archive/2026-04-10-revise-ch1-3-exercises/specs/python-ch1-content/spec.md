## MODIFIED Requirements

### Requirement: Practice challenges exist for independent work

The system SHALL provide practice challenges linked from tutorial sections via `<ChallengeLink>` components:

- `self-introduction` (id: 4), `parrot-echo` (id: 5) — linked from 1-1
- `grade-average` (id: 6), `change-calculator` (id: 7), `seconds-converter` (id: 8) — linked from 1-2
- `grade-level` (id: 9), `triangle-check` (id: 10) — linked from 1-3

Additionally, section 1-3 SHALL link the following scaffolded practice challenges organized in four difficulty tiers:

**Tier 1 (★☆☆)**:
- `odd-even` (id: 26), `sign-check` (id: 27)

**Tier 2 (★★☆)**:
- `grade-level` (id: 9), `bmi-classifier` (id: 28), `quadrant-classifier` (id: 29)

**Tier 3 (★★★)**:
- `triangle-classify` (id: 30), `quadratic-discriminant` (id: 31), `taxi-fare` (id: 32), `movie-ticket` (id: 33)

**Tier 4 (★★★★)**:
- `date-validator` (id: 34)

Each practice challenge MUST have valid params and a correct generator. Tutorial sections MUST reference practice challenges via `<ChallengeLink>` with a brief situational context and a hint (but no step-by-step walkthrough). Each tier MUST have a brief introduction explaining the skill level and target competencies.

#### Scenario: Practice challenges are accessible from tutorial sections

- **WHEN** a user reads a tutorial section's practice area
- **THEN** ChallengeLink components resolve to valid challenge pages

#### Scenario: Practice challenge generators produce correct output

- **WHEN** a practice challenge generator is executed with valid test input
- **THEN** the generator produces the correct expected output

#### Scenario: Section 1-3 displays four-tier scaffolding

- **WHEN** a user reads the practice section of 1-3.md
- **THEN** exercises are organized under four clearly labeled tier headings (★☆☆ through ★★★★) with increasing difficulty

#### Scenario: Each exercise has situational context

- **WHEN** a user reads an exercise description in the practice section
- **THEN** the description SHALL contain 3-5 lines of engaging real-world or mathematical context before the ChallengeLink
