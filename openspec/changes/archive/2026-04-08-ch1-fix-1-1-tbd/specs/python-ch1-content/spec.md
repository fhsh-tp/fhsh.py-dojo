## ADDED Requirements

### Requirement: Chapter 1 section 1-1 opening addresses learner motivation rule O-1

The opening section of `docs/tutor/py/ch1/1-1.md` (content between the frontmatter and the learning objectives) SHALL address the question "Why learn programming?" before introducing technical concepts. The opening SHALL include a personal anecdote from the instructor (learning programming for allowance money) and a positive payoff ("opened a new world"). The opening SHALL be longer than a single paragraph to provide adequate rapport-building for zero-base learners.

#### Scenario: Opening contains motivation before technical content

- **WHEN** a reader begins section 1-1
- **THEN** the first substantive content after the H1 heading SHALL answer "why learn programming" with a personal story, before any mention of programming languages, compilers, or computer science concepts

#### Scenario: Opening includes instructor personal anecdote

- **WHEN** the opening motivation section is reviewed
- **THEN** it SHALL contain an anecdote about the instructor's first motivation for learning programming (allowance money from parent) and a positive transformation statement

---

### Requirement: Chapter 1 section 1-1 code examples match walkthrough text rule W-1

Every fenced code block in `docs/tutor/py/ch1/1-1.md` that is followed by a line-by-line walkthrough SHALL have exact correspondence between the code shown and the walkthrough description. The walkthrough SHALL NOT describe syntax or operations that differ from the code block it references.

#### Scenario: Hello World solution code matches walkthrough

- **WHEN** the "Judge 解題實戰" section presents a Python solution followed by a "逐行解讀" walkthrough
- **THEN** every line referenced in the walkthrough SHALL appear verbatim in the code block, and the code block SHALL produce the correct expected output when executed

#### Scenario: Code example produces AC output

- **WHEN** the solution code for the "哈囉，世界！" problem is executed with input `Alice`
- **THEN** the output SHALL be exactly `Hello, Alice` (comma after Hello, space after comma, no trailing spaces)

#### Scenario: Solution code uses only comma-separated print arguments

- **WHEN** the solution code for the "哈囉，世界！" problem is reviewed
- **THEN** the code SHALL use `print()` with comma-separated arguments only, and SHALL NOT use the `+` operator for string concatenation, because string concatenation is not yet taught in section 1-1

---

### Requirement: Chapter 1 sections contain no residual TBD markers rule T-2

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from `docs/tutor/py/ch1/1-1.md`. No placeholder or deferred-content markers SHALL remain in published tutorial sections.

#### Scenario: No TBD markers in 1-1.md

- **WHEN** `docs/tutor/py/ch1/1-1.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found
