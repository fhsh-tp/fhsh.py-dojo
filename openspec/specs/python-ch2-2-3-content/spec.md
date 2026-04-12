# python-ch2-2-3-content Specification

## Purpose

Defines requirements for section 2-3 of the Python tutorial (break and continue loop control), including the tutorial document, six challenge files (IDs 20–25), and all associated editorial and structural rules.

## Requirements

### Requirement: Section 2-3 file exists with correct frontmatter

The system SHALL provide a tutorial section file at `docs/tutor/py/ch2/2-3.md`. The file MUST have valid frontmatter with `layout: doc`, `chapter: 2`, `section: "2-3"`, and `createdTime` in ISO 8601 with `+08:00` timezone.

#### Scenario: Section file has correct frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-3.md` is parsed successfully with frontmatter fields `layout: doc`, `chapter: 2`, `section: "2-3"`, and a valid `createdTime`

#### Scenario: Section file appears in sidebar navigation

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar displays a link to section 2-3 in the correct position relative to 2-1, 2-2, and 2-4


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 covers break and continue as two knowledge points

The section file MUST cover `break` and `continue` as two distinct knowledge points. The opening of the section SHALL contain a transition from section 2-2 (while loops) that motivates the need to control loops mid-execution. The break knowledge point SHALL be introduced first, followed by continue.

#### Scenario: Opening transition references prior section

- **WHEN** a reader begins section 2-3
- **THEN** the opening paragraph SHALL explicitly reference what was learned in 2-2 (while loops) and motivate loop control as a new design pattern, not merely a while extension

#### Scenario: Two knowledge points are clearly delineated

- **WHEN** a reader reads section 2-3
- **THEN** `break` and `continue` SHALL each have their own H2-level section heading, example challenge, and practice challenges


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Break knowledge point includes example and trace table

The break knowledge point SHALL demonstrate `break` used inside both a `for` loop and a `while` loop. The explanation SHALL include a trace table (M-1) showing iteration-by-iteration execution, marking which iteration triggers the break and what the loop state is at that point.

#### Scenario: Break example demonstrates for loop usage

- **WHEN** the break knowledge point presents its example code
- **THEN** at least one code block SHALL show `break` inside a `for` loop with `range()`

#### Scenario: Break example demonstrates while loop usage

- **WHEN** the break knowledge point presents its example code
- **THEN** at least one code block SHALL show `break` inside a `while` loop

#### Scenario: Trace table shows break execution

- **WHEN** the break example trace table is reviewed
- **THEN** the table SHALL have columns for iteration/step number, loop variable or condition state, action (continue / break), and any output, with the row where break fires clearly marked


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Continue knowledge point includes example and trace table

The continue knowledge point SHALL demonstrate `continue` used inside both a `for` loop and a `while` loop. The explanation SHALL include a trace table (M-1) showing which iterations are skipped and which proceed normally.

#### Scenario: Continue example demonstrates for loop usage

- **WHEN** the continue knowledge point presents its example code
- **THEN** at least one code block SHALL show `continue` inside a `for` loop with `range()`

#### Scenario: Continue example demonstrates while loop usage

- **WHEN** the continue knowledge point presents its example code
- **THEN** at least one code block SHALL show `continue` inside a `while` loop

#### Scenario: Trace table shows continue skipping

- **WHEN** the continue example trace table is reviewed
- **THEN** the table SHALL have columns for iteration/step number, condition result, action (skip / proceed), and output, with skipped iterations clearly marked


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Six challenge files exist for section 2-3 (IDs 20–25)

The system SHALL provide six challenge files for section 2-3. IDs 20–21 are the break example (ID 20) and break practice pair (IDs 21–22). IDs 23–25 are the continue example (ID 23) and continue practice pair (IDs 24–25).

Specifically:
- ID 20 (`break-example`) — break example challenge, difficulty: easy
- ID 21 (`break-practice-1`) — break practice 1, difficulty: easy
- ID 22 (`break-practice-2`) — break practice 2, difficulty: medium
- ID 23 (`continue-example`) — continue example challenge, difficulty: easy
- ID 24 (`continue-practice-1`) — continue practice 1, difficulty: easy
- ID 25 (`continue-practice-2`) — continue practice 2, difficulty: medium

Each challenge file MUST have `layout: challenge`, a valid numeric `id`, `title`, `difficulty`, `tags`, `algorithm` (kebab-case slug), `testcase_count` (minimum 5), `params` with at least one parameter of type `int`, a correct `generator` script, and `starter_code`.

#### Scenario: All six challenge files exist and are valid

- **WHEN** the challenge files for section 2-3 are loaded
- **THEN** all six files (IDs 20–25) exist at `docs/challenge/` with valid frontmatter and parseable generator scripts

#### Scenario: Challenge generators use only taught constructs

- **WHEN** any generator script for IDs 20–25 is reviewed for T-1 compliance
- **THEN** the generator SHALL use only `int`, `input()`, `print()`, `for`, `range()`, `while`, `break`, `continue`, and basic arithmetic/comparison operators — NOT `list`, `dict`, `tuple`, or any construct not yet introduced in Ch1 or Ch2 sections 2-1 through 2-3

#### Scenario: Challenge generators produce correct output

- **WHEN** a generator script is executed with valid test input matching its params specification
- **THEN** the generator produces the correct expected output for that input


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 challenges are linked from the tutorial section

Tutorial section `docs/tutor/py/ch2/2-3.md` MUST reference all six challenge IDs (20–25) via `<ChallengeLink>` components. Example challenges (IDs 20, 23) SHALL appear in the example sub-section with a walkthrough context. Practice challenges (IDs 21–22, 24–25) SHALL appear in practice sub-sections with a brief hint but no step-by-step walkthrough.

#### Scenario: Example challenges linked with walkthrough context

- **WHEN** a reader reads the break knowledge point example sub-section
- **THEN** a `<ChallengeLink id="20" />` component SHALL be present, accompanied by at least one code walkthrough sentence

#### Scenario: Continue example challenge linked

- **WHEN** a reader reads the continue knowledge point example sub-section
- **THEN** a `<ChallengeLink id="23" />` component SHALL be present

#### Scenario: Practice challenges linked with hints only

- **WHEN** a reader reads the practice area for break or continue
- **THEN** `<ChallengeLink>` components for the respective practice IDs SHALL be present with a brief hint (1–2 sentences) and no detailed walkthrough


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows T-1 terminology forward-reference rule

Section 2-3 SHALL NOT use `list`, `dict`, or `tuple` as formal terms or in code examples. `for`, `range()`, and `while` are available (taught in 2-1 and 2-2). Any concept not yet taught SHALL use a plain-language description or a controlled forward reference.

#### Scenario: No premature use of list, dict, or tuple

- **WHEN** `docs/tutor/py/ch2/2-3.md` is scanned for occurrences of `list`, `dict`, or `tuple` in code blocks or formal definitions
- **THEN** zero such occurrences SHALL be found in code examples or as formal technical terms being taught


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows punctuation style rule P-1

Section 2-3 SHALL use the same punctuation conventions established in Ch1 rule P-1: commas (，) or colons (：) for routine clause separation; em-dash (——) reserved exclusively for dramatic emphasis in hooks and humor. The P-1 decision checklist SHALL be applied to every em-dash occurrence.

#### Scenario: Explanatory em-dash replaced with colon

- **WHEN** section 2-3 contains an em-dash followed by an explanatory or definitional clause
- **THEN** the em-dash SHALL be replaced with a colon (：)

#### Scenario: Dramatic em-dash preserved

- **WHEN** section 2-3 contains an em-dash used for comedic timing or narrative surprise
- **THEN** the em-dash SHALL be preserved


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows analogy bridge rule S-1

Every analogy or metaphor in section 2-3 SHALL be preceded by a meta-cognitive bridge sentence explaining why the comparison is being made.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** section 2-3 introduces an analogy for break or continue behavior
- **THEN** the preceding sentence SHALL state the purpose of the analogy before the comparison itself


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions), the next sentence SHALL include an explicit callback connector that resumes the narrative thread, unless the humor element ends an H3 sub-section boundary.

#### Scenario: Joke followed by connector

- **WHEN** section 2-3 contains a kaomoji or parenthetical joke within a continuous prose block
- **THEN** the immediately following sentence SHALL contain an explicit connector linking back to the expository point


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows section transition rule S-3

Transitions between the break knowledge point (H2) and the continue knowledge point (H2) SHALL contain 2–4 sentences that summarize break, identify its limitation, and motivate continue. Single-sentence transitions SHALL only be used between H3 sub-steps within the same H2.

#### Scenario: Major section transition between break and continue

- **WHEN** the break H2 section ends and the continue H2 section begins
- **THEN** the transition block SHALL contain 2–4 sentences covering summary of break, gap or limitation, and motivation for continue


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 code blocks follow conversational lead-in rule C-1

Every fenced code block in section 2-3 SHALL be preceded by at least one sentence of conversational setup. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** section 2-3 contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading (H2/H3) and the opening code fence


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows error prevention rule E-1

Common beginner mistakes specific to break and continue (e.g., using break when continue is intended, forgetting that continue still re-evaluates the loop condition in a while loop, infinite loop created by incorrect continue placement) SHALL be addressed immediately after the syntax is introduced, not deferred to an end-of-section error list.

#### Scenario: Break pitfall warned at point of introduction

- **WHEN** section 2-3 introduces break syntax
- **THEN** a warning or note about at least one common beginner mistake SHALL appear within the same sub-section

#### Scenario: Continue pitfall warned at point of introduction

- **WHEN** section 2-3 introduces continue syntax
- **THEN** a warning or note about the risk of continue causing an infinite while loop (if the loop variable update is placed after continue) SHALL appear within the same sub-section


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 trace tables follow mental model rule M-1

All trace tables in section 2-3 SHALL make the step-by-step execution model explicit. For break, the trace SHALL show the iteration where the condition is met and the loop terminates. For continue, the trace SHALL show which iterations are skipped and which produce output.

#### Scenario: Break trace table is complete

- **WHEN** the break knowledge point trace table is reviewed
- **THEN** the table SHALL cover every iteration from loop start through the break-triggering iteration, with no rows omitted

#### Scenario: Continue trace table is complete

- **WHEN** the continue knowledge point trace table is reviewed
- **THEN** the table SHALL cover every iteration from loop start to loop end, marking each row as either "skipped (continue)" or "executed"


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 image placeholders follow dual-line format rule F-1

Every image placeholder in section 2-3 SHALL use the dual-line format: an image link line `![📷 **圖 N**：description（AI 製圖）](/assets/tutor/py/ch2/figNN.png)` followed by a caption line `> 📷 **圖 N**：description（AI 製圖）`. Single-line caption-only format SHALL NOT be used.

#### Scenario: Image placeholder has both link and caption

- **WHEN** section 2-3 is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding image link line


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 uses correct VitePress custom container syntax rule V-1

All VitePress custom containers in section 2-3 SHALL use the syntax `> [!TYPE]` with the exclamation mark. The pattern `> [TYPE]` without `!` SHALL NOT be used.

#### Scenario: Custom container syntax is correct

- **WHEN** section 2-3 is scanned for blockquote-based custom containers
- **THEN** every opening line SHALL match `> [!TYPE]` with the exclamation mark present


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 has no empty UI elements rule T-3

Section 2-3 SHALL NOT contain custom container blocks where the body content is empty or whitespace-only. Unfinished containers SHALL be wrapped in HTML comments.

#### Scenario: No empty containers in 2-3

- **WHEN** section 2-3 is scanned for custom container blocks
- **THEN** every visible container SHALL have at least one sentence of substantive body content


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 has no residual TBD markers rule T-2

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from `docs/tutor/py/ch2/2-3.md`.

#### Scenario: No TBD markers in 2-3.md

- **WHEN** `docs/tutor/py/ch2/2-3.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 follows emotional punctuation density rule K-1

Section 2-3 SHALL maintain balanced emotional punctuation density. Within any contiguous block of 30 lines of prose (excluding code, tables, images), at least one emotional punctuation element (kaomoji, parenthetical joke, student dialogue interjection) SHALL be present. Within any contiguous block of 10 lines of prose, no more than one such element SHALL be present. Kaomoji variety rules apply: the same kaomoji SHALL NOT appear more than twice within section 2-3, and the section SHALL use kaomoji from at least two different emotional categories.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose is identified in section 2-3
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a contiguous block of 10 lines of prose is identified in section 2-3
- **THEN** no more than one such element SHALL be present

#### Scenario: Kaomoji variety is maintained

- **WHEN** section 2-3 is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice, and kaomoji from at least two different emotional categories SHALL be present


<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-3 ends with an Image Specification Appendix

The file `docs/tutor/py/ch2/2-3.md` MUST end with an Image Specification Appendix section containing the fully expanded AI image generation prompt for every image placeholder used in the section. All image prompts MUST use the American stick figure comic style with dialogue-driven panels, Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Appendix lists all image prompts

- **WHEN** section 2-3 is reviewed
- **THEN** the final section of the file SHALL be an appendix titled "圖片規格附錄" (or equivalent) containing one entry per image placeholder, each with a fully expanded generation prompt

#### Scenario: Image prompts use correct visual style

- **WHEN** an image prompt from the appendix is reviewed
- **THEN** the prompt SHALL specify American stick figure comic style, dialogue-driven panels (no narration boxes), Traditional Chinese speech bubble text, and English for technical terms

<!-- @trace
source: write-ch2-2-3-loop-control
updated: 2026-04-12
code:
  - docs/challenge/parrot-echo.md
  - docs/challenge/target-sum.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/collatz-steps.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/change-calculator.md
  - .vitepress/config.mts
  - docs/challenge/odd-even.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/leap-year.md
  - docs/challenges.md
  - package.json
  - docs/public/favicon.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/grade-average.md
  - docs/challenge/hello-world.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/vending-change.md
  - docs/challenge/seconds-converter.md
  - docs/public/assets/LOGO-dark.svg
  - docs/tutor/py/ch1/reference.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/countdown.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/public/assets/LOGO-light.svg
  - docs/challenge/digit-counter.md
  - docs/challenge/self-introduction.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/triangle-check.md
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/LOGO-light.png
  - docs/tutor/py/ch1/1-4.md
  - docs/shared/challenge.data.ts
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/factorial.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/sum-skip-fives.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch2/2-2.md
  - docs/public/assets/LOGO-dark.png
  - docs/challenge/date-validator.md
  - docs/challenge/grade-level.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/number-reverse.md
  - docs/challenge/taxi-fare.md
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/number-sum.md
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/skip-multiples.md
  - docs/challenge/bmi-classifier.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->