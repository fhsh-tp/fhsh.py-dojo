## ADDED Requirements

### Requirement: Section 1-4 contains a comprehensive Judge exercise

Section `docs/tutor/py/ch1/1-4.md` SHALL contain a "模組一畢業考" section positioned after the self-check table and before the "模組二預告" section. This section SHALL include:

1. A celebratory framing as a "graduation exam" for Module 1
2. An explanation of how the exercise integrates skills from all three sections (I/O from 1-1, arithmetic from 1-2, conditionals from 1-3)
3. A brief problem description for the vending machine change exercise
4. A `<ChallengeLink slug="vending-change" />` component
5. A hint about the greedy decomposition approach using `//` and `%`

The section SHALL use Phoenix's conversational tone with kaomoji, consistent with the rest of Module 1.

#### Scenario: Comprehensive exercise appears in correct position

- **WHEN** a user reads section 1-4
- **THEN** the "模組一畢業考" section SHALL appear after the self-check table and before the "模組二預告" section

#### Scenario: Exercise cross-references all three sections

- **WHEN** a user reads the comprehensive exercise description
- **THEN** the description SHALL explicitly reference skills from 1-1 (input/output), 1-2 (arithmetic operators `//` and `%`), and 1-3 (if-else conditional)

#### Scenario: ChallengeLink resolves to valid challenge

- **WHEN** a user clicks the ChallengeLink for `vending-change`
- **THEN** the link SHALL resolve to a valid challenge page at `/challenge/vending-change`
