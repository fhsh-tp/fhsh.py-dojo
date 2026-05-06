# python-ch2-2-2-content Specification

## Purpose

Defines the content requirements for tutorial section 2-2 of the Python self-learning course at FHSH. This section teaches `while` conditional loops — the primary tool for "unknown number of iterations" problems — to zero-base high school learners. The section uses the Collatz Conjecture (3N+1) as the Judge example challenge and includes two practice challenges (IDs 18–19). All Ch1 editorial rules (P-1 through K-1) apply.

## ADDED Requirements

### Requirement: Section 2-2 file exists with correct frontmatter

The file `docs/tutor/py/ch2/2-2.md` SHALL exist with valid VitePress frontmatter containing: `layout: doc`, `chapter: 2`, `section: "2-2"`, and `createdTime` in ISO 8601 format with `+08:00` timezone offset.

#### Scenario: Frontmatter fields are present and valid

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-2.md` is parsed successfully with all required frontmatter fields (`layout`, `chapter`, `section`, `createdTime`)

#### Scenario: Section identifier matches filename

- **WHEN** the frontmatter of `docs/tutor/py/ch2/2-2.md` is read
- **THEN** the `section` field SHALL equal `"2-2"` and the `chapter` field SHALL equal `2`


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 content covers while loops only within T-1 boundaries

Section 2-2 SHALL teach the `while` conditional loop as its single knowledge point. The section SHALL NOT introduce `break`, `continue`, `list`, `dict`, or `tuple`, as these concepts are not yet taught at this point in the curriculum. The `for` loop and `range()` function ARE available (taught in 2-1) and SHALL be referenced as contrast when helpful.

#### Scenario: Forbidden terms are absent from teaching content

- **WHEN** the prose and code blocks of `docs/tutor/py/ch2/2-2.md` are scanned for introduced terms
- **THEN** `break`, `continue`, `list`, `dict`, and `tuple` SHALL NOT appear as newly introduced concepts (they SHALL only appear in comments explicitly explaining what is NOT covered yet)

#### Scenario: While loop is the sole new knowledge point

- **WHEN** the section's H2-level structural outline is reviewed
- **THEN** there SHALL be exactly one primary teaching target: the `while` loop syntax and condition-based termination


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 opening connects from 2-1 with a clear motivation bridge

The opening of section 2-2 SHALL transition from the "known iterations" paradigm of `for` + `range()` (section 2-1) to the "unknown iterations" need addressed by `while`. The opening SHALL include a concept origin story (概念溯源) explaining why humans invented condition-based loops: to solve the problem of applying the same logic repeatedly to different data without knowing in advance how many repetitions are needed.

#### Scenario: Opening references the for-loop limitation

- **WHEN** the opening section of 2-2 is read
- **THEN** it SHALL contain a contrast explaining that `for` + `range()` requires knowing the count in advance, and `while` is needed when the termination condition is data-dependent

#### Scenario: Concept origin story addresses human motivation

- **WHEN** the 概念溯源 block is read
- **THEN** it SHALL explain that humans dislike repetitive mechanical labor and that loops exist to solve "same logic, different data, repeated indefinitely" problems


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 while loop teaching includes syntax, semantics, and trace table

The `while` loop syntax SHALL be introduced with a minimal annotated example. The section SHALL include at least one execution trace table (追蹤表) showing variable state changes across iterations, conforming to the M-1 mental model rule. The trace table MUST show at minimum: iteration number, loop condition value, and relevant variable values at start and end of each iteration.

#### Scenario: Trace table shows step-by-step execution

- **WHEN** the while loop teaching section is read
- **THEN** a markdown table with columns for iteration/step, condition (True/False), and key variable values SHALL be present

#### Scenario: Syntax annotation explains each part

- **WHEN** the while loop syntax block is presented
- **THEN** inline comments or an accompanying numbered list SHALL explain: the condition expression, the loop body indentation, and how Python checks the condition before each iteration


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 includes error prevention for infinite loops (E-1 compliance)

The section SHALL address the infinite loop pitfall immediately after introducing the `while` syntax. The warning SHALL explain that if the loop variable is never updated inside the body, the condition never becomes `False` and the program hangs. A concrete bad-code example (lacking the update step) followed by a corrected version SHALL be shown.

#### Scenario: Infinite loop warning appears near syntax introduction

- **WHEN** the `while` syntax is first introduced
- **THEN** a WARNING or TIP container SHALL appear within the same H2/H3 subsection warning about the infinite loop pitfall

#### Scenario: Bad-code and good-code pair illustrates the pitfall

- **WHEN** the infinite loop warning section is read
- **THEN** it SHALL contain a fenced code block showing the incorrect pattern (missing update) alongside a corrected version, with explanatory prose between them


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 Judge walkthrough uses Collatz Conjecture (3N+1) as example challenge (ID 17)

The section SHALL contain a full Judge解題實戰 walkthrough for challenge ID 17: the Collatz Conjecture (3N+1 problem). The walkthrough SHALL: (a) explain the problem statement, (b) present the algorithm logic before showing code, (c) provide a step-by-step trace table for a concrete input (e.g., N=6), (d) show the complete Python solution using only `while`, `print`, and arithmetic, and (e) perform a 逐行解讀 line-by-line code reading.

#### Scenario: Collatz problem statement is explained in plain language

- **WHEN** the Judge walkthrough section is read
- **THEN** the 3N+1 rules SHALL be stated explicitly: if N is even → N = N // 2; if N is odd → N = 3 * N + 1; repeat until N equals 1; count the steps

#### Scenario: Collatz trace table shows N=6 execution

- **WHEN** the trace table in the walkthrough is reviewed
- **THEN** it SHALL show the full sequence for N=6: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 with step count = 8

#### Scenario: Solution code uses only taught constructs

- **WHEN** the Python solution code for challenge 17 is reviewed
- **THEN** the code SHALL use only `input()`, `int()`, `while`, `if`/`else`, arithmetic operators (`//`, `%`, `*`, `+`), a counter variable, and `print()` — no `break`, `continue`, `list`, `dict`, or `tuple`

#### Scenario: Line-by-line walkthrough matches solution code

- **WHEN** the 逐行解讀 section is reviewed against the solution code
- **THEN** every line referenced in the walkthrough SHALL appear verbatim in the code block above it


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 includes challenge ID 17 (Collatz 3N+1) as example and IDs 18–19 as practice challenges

The section SHALL link to three Judge challenges: ID 17 as the example walkthrough challenge, and IDs 18 and 19 as independent practice challenges. Practice challenges SHALL be presented with a `<ChallengeLink>` component and a brief hint, but without full step-by-step walkthroughs.

#### Scenario: Example challenge is linked with ChallengeLink

- **WHEN** the Judge walkthrough section references challenge 17
- **THEN** a `<ChallengeLink id="17" />` component SHALL appear in the section

#### Scenario: Practice challenges are linked from section

- **WHEN** the practice area of section 2-2 is read
- **THEN** `<ChallengeLink id="18" />` and `<ChallengeLink id="19" />` SHALL both appear, each accompanied by a brief hint (1–3 sentences)


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Challenge ID 17 (Collatz 3N+1) exists with valid challenge.yaml

The file `challenges/017/challenge.yaml` (or equivalent path per project conventions) SHALL exist with `layout: challenge`, `id: 17`, a title indicating the 3N+1/Collatz problem, `difficulty: medium`, a generator that reads integer N (3 ≤ N ≤ 10000, N odd to ensure non-trivial sequences), computes the Collatz step count, and `starter_code` hinting at the while loop approach.

#### Scenario: Challenge 17 generator produces correct step counts

- **WHEN** the generator for challenge 17 is executed with N=6
- **THEN** the expected output SHALL be `8` (the number of steps from 6 to 1)

#### Scenario: Challenge 17 generator produces correct step counts for odd N

- **WHEN** the generator for challenge 17 is executed with N=27
- **THEN** the expected output SHALL be `111` (the Collatz sequence length from 27 to 1)

#### Scenario: Challenge 17 params restrict to valid Collatz inputs

- **WHEN** the challenge 17 params specification is reviewed
- **THEN** the `n` parameter SHALL have `type: int`, `min` of at least 2, and `max` of at most 10000


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Challenge ID 18 (practice 1) exists with valid challenge.yaml

The file for challenge ID 18 SHALL exist with `layout: challenge`, `id: 18`, a `while`-loop-based problem appropriate for zero-base learners, `difficulty: easy`, a correct generator, and `starter_code`. The problem SHALL be solvable using only `while`, `if`/`else`, arithmetic, `input()`, and `print()` — no `break`, `continue`, `list`, or `dict`.

#### Scenario: Challenge 18 generator produces correct output

- **WHEN** the generator for challenge 18 is executed with valid param inputs
- **THEN** the output matches the expected answer computed by the reference algorithm

#### Scenario: Challenge 18 is solvable with only taught constructs

- **WHEN** the reference solution for challenge 18 is reviewed
- **THEN** it SHALL use only `while`, `if`/`elif`/`else`, arithmetic operators, `input()`, `int()`, and `print()` with no forbidden terms


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Challenge ID 19 (practice 2) exists with valid challenge.yaml

The file for challenge ID 19 SHALL exist with `layout: challenge`, `id: 19`, a `while`-loop-based problem appropriate for zero-base learners, `difficulty: easy`, a correct generator, and `starter_code`. The problem SHALL be solvable using only `while`, `if`/`else`, arithmetic, `input()`, and `print()` — no `break`, `continue`, `list`, or `dict`.

#### Scenario: Challenge 19 generator produces correct output

- **WHEN** the generator for challenge 19 is executed with valid param inputs
- **THEN** the output matches the expected answer computed by the reference algorithm

#### Scenario: Challenge 19 is solvable with only taught constructs

- **WHEN** the reference solution for challenge 19 is reviewed
- **THEN** it SHALL use only `while`, `if`/`elif`/`else`, arithmetic operators, `input()`, `int()`, and `print()` with no forbidden terms


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 follows all Ch1 editorial rules (P-1 through K-1)

All editorial rules established in the `python-ch1-content` spec SHALL apply to section 2-2 with scope extended to `docs/tutor/py/ch2/2-2.md`. Specifically:

- **P-1**: Punctuation style — em-dash reserved for dramatic emphasis only; use colons and commas for clauses
- **T-1**: Terminology forward reference — no concept used before its teaching point
- **S-1**: Analogy bridge — every analogy preceded by a meta-cognitive setup sentence
- **S-2**: Post-humor connector — humor elements followed by explicit callback connectors
- **S-3**: Section transition — H2-level transitions contain 2–4 sentences (summary + gap + motivation)
- **C-1**: Conversational lead-in — every code block preceded by at least one sentence of setup
- **E-1**: Error prevention at point of introduction — pitfalls warned immediately when syntax is introduced
- **M-1**: Mental model trace — compound expressions and loop mechanics explained with step-by-step traces
- **W-1**: Code-walkthrough correspondence — walkthrough text matches code verbatim
- **T-2**: No residual placeholder markers — all deferred-content comments resolved before publication
- **F-1**: Image placeholder dual-line format — `![...]()` link line + `> 📷` caption line
- **V-1**: VitePress container syntax — `> [!TYPE]` with exclamation mark
- **T-3**: No empty UI elements — containers with empty bodies hidden in HTML comments
- **K-1**: Emotional punctuation density — kaomoji/jokes present but not excessive; variety across emotional categories

#### Scenario: P-1 punctuation rule is satisfied in 2-2.md

- **WHEN** `docs/tutor/py/ch2/2-2.md` is reviewed for em-dash usage
- **THEN** em-dashes SHALL appear only for dramatic emphasis; clause separations SHALL use commas or colons

#### Scenario: M-1 trace tables are present for while loop examples

- **WHEN** the while loop introduction and Collatz walkthrough are reviewed
- **THEN** at least two trace tables SHALL be present: one for the basic while loop concept and one for the Collatz sequence

#### Scenario: T-1 boundary is respected for 2-2 constructs

- **WHEN** all code examples and prose in 2-2.md are scanned
- **THEN** `break`, `continue`, `list`, `dict`, and `tuple` SHALL NOT appear as taught or used constructs

#### Scenario: K-1 emotional density is balanced in 2-2.md

- **WHEN** prose blocks of 30 lines in 2-2.md are reviewed
- **THEN** at least one kaomoji or humor element SHALL be present per 30-line block, with no more than one per 10-line block


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---

### Requirement: Section 2-2 includes Image Specification Appendix

The file `docs/tutor/py/ch2/2-2.md` SHALL end with an Image Specification Appendix section containing fully expanded Nano Banana Pro–style prompts for each image placeholder used in the section. All image prompts SHALL use American stick figure comic style, dialogue-driven panels (no narration boxes), Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Appendix contains entry for each image placeholder

- **WHEN** the Image Specification Appendix of 2-2.md is read
- **THEN** it SHALL contain one entry per `![...]()` image link in the section body, with a fully expanded prompt string

#### Scenario: Image prompts follow visual style prefix

- **WHEN** an image prompt in the appendix is read
- **THEN** the prompt SHALL begin with the chapter 2 visual style prefix and include panel-by-panel descriptions with stick figure dialogue

## Requirements


<!-- @trace
source: write-ch2-2-2-while
updated: 2026-04-12
code:
  - docs/challenge/range-sum.md
  - docs/public/assets/LOGO-dark.png
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/assets/LOGO-light.png
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/grade-level.md
  - docs/challenge/triangle-check.md
  - docs/challenge/date-validator.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/movie-ticket.md
  - assets/banner.png
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sum-skip-fives.md
  - package.json
  - docs/challenge/change-calculator.md
  - docs/challenge/grade-average.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/triangle-classify.md
  - docs/challenge/skip-multiples.md
  - .vitepress/sidebar.ts
  - docs/challenge/countdown.md
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/leap-year.md
  - docs/public/favicon.svg
  - docs/challenge/seconds-converter.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/password-check.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/challenge/self-introduction.md
  - docs/challenge/sign-check.md
  - docs/challenges.md
  - docs/challenge/odd-even.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/factorial.md
  - docs/challenge/vending-change.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/number-reverse.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/tutor/py/ch1/1-3.md
  - docs/shared/challenge.data.ts
  - docs/challenge/beverage-cashier.md
  - docs/challenge/digit-sum-skip.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/parrot-echo.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch2/2-3.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

### Requirement: Section 2-2 file exists with correct frontmatter

The file `docs/tutor/py/ch2/2-2.md` SHALL exist with valid VitePress frontmatter containing: `layout: doc`, `chapter: 2`, `section: "2-2"`, and `createdTime` in ISO 8601 format with `+08:00` timezone offset.

#### Scenario: Frontmatter fields are present and valid

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-2.md` is parsed successfully with all required frontmatter fields (`layout`, `chapter`, `section`, `createdTime`)

#### Scenario: Section identifier matches filename

- **WHEN** the frontmatter of `docs/tutor/py/ch2/2-2.md` is read
- **THEN** the `section` field SHALL equal `"2-2"` and the `chapter` field SHALL equal `2`

---
### Requirement: Section 2-2 content covers while loops only within T-1 boundaries

Section 2-2 SHALL teach the `while` conditional loop as its single knowledge point. The section SHALL NOT introduce `break`, `continue`, `list`, `dict`, or `tuple`, as these concepts are not yet taught at this point in the curriculum. The `for` loop and `range()` function ARE available (taught in 2-1) and SHALL be referenced as contrast when helpful.

#### Scenario: Forbidden terms are absent from teaching content

- **WHEN** the prose and code blocks of `docs/tutor/py/ch2/2-2.md` are scanned for introduced terms
- **THEN** `break`, `continue`, `list`, `dict`, and `tuple` SHALL NOT appear as newly introduced concepts (they SHALL only appear in comments explicitly explaining what is NOT covered yet)

#### Scenario: While loop is the sole new knowledge point

- **WHEN** the section's H2-level structural outline is reviewed
- **THEN** there SHALL be exactly one primary teaching target: the `while` loop syntax and condition-based termination

---
### Requirement: Section 2-2 opening connects from 2-1 with a clear motivation bridge

The opening of section 2-2 SHALL transition from the "known iterations" paradigm of `for` + `range()` (section 2-1) to the "unknown iterations" need addressed by `while`. The opening SHALL include a concept origin story (概念溯源) explaining why humans invented condition-based loops: to solve the problem of applying the same logic repeatedly to different data without knowing in advance how many repetitions are needed.

#### Scenario: Opening references the for-loop limitation

- **WHEN** the opening section of 2-2 is read
- **THEN** it SHALL contain a contrast explaining that `for` + `range()` requires knowing the count in advance, and `while` is needed when the termination condition is data-dependent

#### Scenario: Concept origin story addresses human motivation

- **WHEN** the 概念溯源 block is read
- **THEN** it SHALL explain that humans dislike repetitive mechanical labor and that loops exist to solve "same logic, different data, repeated indefinitely" problems

---
### Requirement: Section 2-2 while loop teaching includes syntax, semantics, and trace table

The `while` loop syntax SHALL be introduced with a minimal annotated example. The section SHALL include at least one execution trace table (追蹤表) showing variable state changes across iterations, conforming to the M-1 mental model rule. The trace table MUST show at minimum: iteration number, loop condition value, and relevant variable values at start and end of each iteration.

#### Scenario: Trace table shows step-by-step execution

- **WHEN** the while loop teaching section is read
- **THEN** a markdown table with columns for iteration/step, condition (True/False), and key variable values SHALL be present

#### Scenario: Syntax annotation explains each part

- **WHEN** the while loop syntax block is presented
- **THEN** inline comments or an accompanying numbered list SHALL explain: the condition expression, the loop body indentation, and how Python checks the condition before each iteration

---
### Requirement: Section 2-2 includes error prevention for infinite loops (E-1 compliance)

The section SHALL address the infinite loop pitfall immediately after introducing the `while` syntax. The warning SHALL explain that if the loop variable is never updated inside the body, the condition never becomes `False` and the program hangs. A concrete bad-code example (lacking the update step) followed by a corrected version SHALL be shown.

#### Scenario: Infinite loop warning appears near syntax introduction

- **WHEN** the `while` syntax is first introduced
- **THEN** a WARNING or TIP container SHALL appear within the same H2/H3 subsection warning about the infinite loop pitfall

#### Scenario: Bad-code and good-code pair illustrates the pitfall

- **WHEN** the infinite loop warning section is read
- **THEN** it SHALL contain a fenced code block showing the incorrect pattern (missing update) alongside a corrected version, with explanatory prose between them

---
### Requirement: Section 2-2 Judge walkthrough uses Collatz Conjecture (3N+1) as example challenge (ID 17)

The section SHALL contain a full Judge解題實戰 walkthrough for challenge ID 17: the Collatz Conjecture (3N+1 problem). The walkthrough SHALL: (a) explain the problem statement, (b) present the algorithm logic before showing code, (c) provide a step-by-step trace table for a concrete input (e.g., N=6), (d) show the complete Python solution using only `while`, `print`, and arithmetic, and (e) perform a 逐行解讀 line-by-line code reading.

#### Scenario: Collatz problem statement is explained in plain language

- **WHEN** the Judge walkthrough section is read
- **THEN** the 3N+1 rules SHALL be stated explicitly: if N is even → N = N // 2; if N is odd → N = 3 * N + 1; repeat until N equals 1; count the steps

#### Scenario: Collatz trace table shows N=6 execution

- **WHEN** the trace table in the walkthrough is reviewed
- **THEN** it SHALL show the full sequence for N=6: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 with step count = 8

#### Scenario: Solution code uses only taught constructs

- **WHEN** the Python solution code for challenge 17 is reviewed
- **THEN** the code SHALL use only `input()`, `int()`, `while`, `if`/`else`, arithmetic operators (`//`, `%`, `*`, `+`), a counter variable, and `print()` — no `break`, `continue`, `list`, `dict`, or `tuple`

#### Scenario: Line-by-line walkthrough matches solution code

- **WHEN** the 逐行解讀 section is reviewed against the solution code
- **THEN** every line referenced in the walkthrough SHALL appear verbatim in the code block above it

---
### Requirement: Section 2-2 includes challenge ID 17 (Collatz 3N+1) as example and IDs 18–19 as practice challenges

The section SHALL link to three Judge challenges: ID 17 as the example walkthrough challenge, and IDs 18 and 19 as independent practice challenges. Practice challenges SHALL be presented with a `<ChallengeLink>` component and a brief hint, but without full step-by-step walkthroughs.

#### Scenario: Example challenge is linked with ChallengeLink

- **WHEN** the Judge walkthrough section references challenge 17
- **THEN** a `<ChallengeLink id="17" />` component SHALL appear in the section

#### Scenario: Practice challenges are linked from section

- **WHEN** the practice area of section 2-2 is read
- **THEN** `<ChallengeLink id="18" />` and `<ChallengeLink id="19" />` SHALL both appear, each accompanied by a brief hint (1–3 sentences)

---
### Requirement: Challenge ID 17 (Collatz 3N+1) exists with valid challenge.yaml

The file `challenges/017/challenge.yaml` (or equivalent path per project conventions) SHALL exist with `layout: challenge`, `id: 17`, a title indicating the 3N+1/Collatz problem, `difficulty: medium`, a generator that reads integer N (3 ≤ N ≤ 10000, N odd to ensure non-trivial sequences), computes the Collatz step count, and `starter_code` hinting at the while loop approach.

#### Scenario: Challenge 17 generator produces correct step counts

- **WHEN** the generator for challenge 17 is executed with N=6
- **THEN** the expected output SHALL be `8` (the number of steps from 6 to 1)

#### Scenario: Challenge 17 generator produces correct step counts for odd N

- **WHEN** the generator for challenge 17 is executed with N=27
- **THEN** the expected output SHALL be `111` (the Collatz sequence length from 27 to 1)

#### Scenario: Challenge 17 params restrict to valid Collatz inputs

- **WHEN** the challenge 17 params specification is reviewed
- **THEN** the `n` parameter SHALL have `type: int`, `min` of at least 2, and `max` of at most 10000

---
### Requirement: Challenge ID 18 (practice 1) exists with valid challenge.yaml

The file for challenge ID 18 SHALL exist with `layout: challenge`, `id: 18`, a `while`-loop-based problem appropriate for zero-base learners, `difficulty: easy`, a correct generator, and `starter_code`. The problem SHALL be solvable using only `while`, `if`/`else`, arithmetic, `input()`, and `print()` — no `break`, `continue`, `list`, or `dict`.

#### Scenario: Challenge 18 generator produces correct output

- **WHEN** the generator for challenge 18 is executed with valid param inputs
- **THEN** the output matches the expected answer computed by the reference algorithm

#### Scenario: Challenge 18 is solvable with only taught constructs

- **WHEN** the reference solution for challenge 18 is reviewed
- **THEN** it SHALL use only `while`, `if`/`elif`/`else`, arithmetic operators, `input()`, `int()`, and `print()` with no forbidden terms

---
### Requirement: Challenge ID 19 (practice 2) exists with valid challenge.yaml

The file for challenge ID 19 SHALL exist with `layout: challenge`, `id: 19`, a `while`-loop-based problem appropriate for zero-base learners, `difficulty: easy`, a correct generator, and `starter_code`. The problem SHALL be solvable using only `while`, `if`/`else`, arithmetic, `input()`, and `print()` — no `break`, `continue`, `list`, or `dict`.

#### Scenario: Challenge 19 generator produces correct output

- **WHEN** the generator for challenge 19 is executed with valid param inputs
- **THEN** the output matches the expected answer computed by the reference algorithm

#### Scenario: Challenge 19 is solvable with only taught constructs

- **WHEN** the reference solution for challenge 19 is reviewed
- **THEN** it SHALL use only `while`, `if`/`elif`/`else`, arithmetic operators, `input()`, `int()`, and `print()` with no forbidden terms

---
### Requirement: Section 2-2 follows all Ch1 editorial rules (P-1 through K-1)

All editorial rules established in the `python-ch1-content` spec SHALL apply to section 2-2 with scope extended to `docs/tutor/py/ch2/2-2.md`. Specifically:

- **P-1**: Punctuation style — em-dash reserved for dramatic emphasis only; use colons and commas for clauses
- **T-1**: Terminology forward reference — no concept used before its teaching point
- **S-1**: Analogy bridge — every analogy preceded by a meta-cognitive setup sentence
- **S-2**: Post-humor connector — humor elements followed by explicit callback connectors
- **S-3**: Section transition — H2-level transitions contain 2–4 sentences (summary + gap + motivation)
- **C-1**: Conversational lead-in — every code block preceded by at least one sentence of setup
- **E-1**: Error prevention at point of introduction — pitfalls warned immediately when syntax is introduced
- **M-1**: Mental model trace — compound expressions and loop mechanics explained with step-by-step traces
- **W-1**: Code-walkthrough correspondence — walkthrough text matches code verbatim
- **T-2**: No residual placeholder markers — all deferred-content comments resolved before publication
- **F-1**: Image placeholder dual-line format — `![...]()` link line + `> 📷` caption line
- **V-1**: VitePress container syntax — `> [!TYPE]` with exclamation mark
- **T-3**: No empty UI elements — containers with empty bodies hidden in HTML comments
- **K-1**: Emotional punctuation density — kaomoji/jokes present but not excessive; variety across emotional categories

#### Scenario: P-1 punctuation rule is satisfied in 2-2.md

- **WHEN** `docs/tutor/py/ch2/2-2.md` is reviewed for em-dash usage
- **THEN** em-dashes SHALL appear only for dramatic emphasis; clause separations SHALL use commas or colons

#### Scenario: M-1 trace tables are present for while loop examples

- **WHEN** the while loop introduction and Collatz walkthrough are reviewed
- **THEN** at least two trace tables SHALL be present: one for the basic while loop concept and one for the Collatz sequence

#### Scenario: T-1 boundary is respected for 2-2 constructs

- **WHEN** all code examples and prose in 2-2.md are scanned
- **THEN** `break`, `continue`, `list`, `dict`, and `tuple` SHALL NOT appear as taught or used constructs

#### Scenario: K-1 emotional density is balanced in 2-2.md

- **WHEN** prose blocks of 30 lines in 2-2.md are reviewed
- **THEN** at least one kaomoji or humor element SHALL be present per 30-line block, with no more than one per 10-line block

---
### Requirement: Section 2-2 includes Image Specification Appendix

The file `docs/tutor/py/ch2/2-2.md` SHALL end with an Image Specification Appendix section containing fully expanded Nano Banana Pro–style prompts for each image placeholder used in the section. All image prompts SHALL use American stick figure comic style, dialogue-driven panels (no narration boxes), Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Appendix contains entry for each image placeholder

- **WHEN** the Image Specification Appendix of 2-2.md is read
- **THEN** it SHALL contain one entry per `![...]()` image link in the section body, with a fully expanded prompt string

#### Scenario: Image prompts follow visual style prefix

- **WHEN** an image prompt in the appendix is read
- **THEN** the prompt SHALL begin with the chapter 2 visual style prefix and include panel-by-panel descriptions with stick figure dialogue