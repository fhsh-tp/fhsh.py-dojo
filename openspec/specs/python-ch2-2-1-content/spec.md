## Requirements

### Requirement: Section 2-1 file exists with correct frontmatter and structure

The file `docs/tutor/py/ch2/2-1.md` SHALL exist with frontmatter fields: `layout: doc`, `title` (display title for the for-loop section), `description` (one-line summary), `chapter: 2`, `section: "2-1"`, `createdTime` in ISO 8601 with `+08:00` timezone, and `challenge` referencing the slug of the primary example challenge.

The file SHALL include a `VISUAL-STYLE-PREFIX` HTML comment immediately after the frontmatter, using the same American stick figure comic style as Chapter 1.

#### Scenario: Section file has valid frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-1.md` SHALL be parsed successfully with all required frontmatter fields (`layout`, `title`, `description`, `chapter`, `section`, `createdTime`, `challenge`) present and non-empty

#### Scenario: Section file appears in sidebar

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar SHALL display a link to section 2-1


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-1 covers for loops and range() as two knowledge points

Section 2-1 SHALL teach exactly two knowledge points:

- **Knowledge Point A**: `for i in range(n)` — basic counting loop (the `for` keyword, `range(n)` producing 0 to n-1, loop body indentation)
- **Knowledge Point B**: `range(start, stop, step)` — the full three-parameter form of `range()`, including negative step for countdown, and off-by-one behavior

Section 2-1 SHALL NOT formally introduce or use the following concepts (T-1 compliance): `while` loops, `break`, `continue`, `for item in list` iteration, nested loops, or any data structure (`list`, `dict`, `tuple`). If any of these concepts MUST be referenced for motivational context, a controlled forward reference SHALL be used (plain-language description + parenthetical explanation + promise of when it will be formally taught).

#### Scenario: Knowledge Point A is taught before Knowledge Point B

- **WHEN** a reader reads section 2-1 sequentially
- **THEN** the `for i in range(n)` concept SHALL appear before the `range(start, stop, step)` concept

#### Scenario: No formal use of while, break, continue, or data structures

- **WHEN** section 2-1 is scanned for the keywords `while`, `break`, `continue`, or `list`/`dict`/`tuple` used as formal teaching terms
- **THEN** zero occurrences SHALL be found outside of controlled forward references

#### Scenario: Controlled forward reference used when list is mentioned

- **WHEN** section 2-1 references the concept of a collection of data before it is formally taught
- **THEN** the reference SHALL use plain language (e.g., "一整排資料") or a controlled forward reference that includes a parenthetical explanation and a statement of when it will be formally taught


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Each knowledge point has a trace table demonstrating loop execution

Every `for` loop code example in section 2-1 that introduces a new loop pattern SHALL be accompanied by a Trace Table showing the value of the loop variable and the output at each iteration. The Trace Table SHALL have columns for iteration number, loop variable value, executed statement, and output. Trace Tables for loops with more than 5 iterations SHALL abbreviate middle rows with `...` but SHALL show at least the first 3 and last 1 iteration.

#### Scenario: Basic for loop has trace table

- **WHEN** the first `for i in range(n)` code example is presented
- **THEN** a Trace Table SHALL immediately follow showing each iteration's `i` value and output

#### Scenario: Long loop trace table is abbreviated

- **WHEN** a loop example iterates more than 5 times
- **THEN** the Trace Table SHALL show at least the first 3 iterations and the last iteration, with `...` indicating omitted middle rows


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-1 has one example challenge and two practice challenges per knowledge point

Section 2-1 SHALL contain exactly 6 challenge references:

- Knowledge Point A (`for i in range(n)`): 1 example challenge with full IPO analysis and step-by-step walkthrough, plus 2 practice challenges with hints only (no walkthrough)
- Knowledge Point B (`range(start, stop, step)`): 1 example challenge with full IPO analysis and step-by-step walkthrough, plus 2 practice challenges with hints only (no walkthrough)

Each example challenge walkthrough SHALL follow the pattern established in 1-1 and 1-2: IPO analysis → code solution → line-by-line explanation → Judge testing instructions → common error troubleshooting.

Each practice challenge SHALL be referenced via `<ChallengeLink slug="..." />` and SHALL include a one-line hint but no step-by-step solution.

#### Scenario: Knowledge Point A has 3 challenges

- **WHEN** section 2-1's Knowledge Point A content area is reviewed
- **THEN** exactly 1 example challenge (full walkthrough) and 2 practice challenges (hint only, with `<ChallengeLink>`) SHALL be present

#### Scenario: Knowledge Point B has 3 challenges

- **WHEN** section 2-1's Knowledge Point B content area is reviewed
- **THEN** exactly 1 example challenge (full walkthrough) and 2 practice challenges (hint only, with `<ChallengeLink>`) SHALL be present

#### Scenario: Example challenge follows established walkthrough pattern

- **WHEN** an example challenge walkthrough is reviewed
- **THEN** it SHALL contain: (1) IPO analysis section, (2) Python code solution in a fenced code block, (3) line-by-line or step-by-step explanation of the code, (4) Judge testing instructions, (5) at least one common error with explanation


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Six challenge files exist with correct generator scripts

Six new challenge files SHALL exist in `docs/challenge/` with sequential IDs starting from 11. Each challenge file SHALL have frontmatter with `layout: challenge`, `id` (11–16), `title`, `difficulty` (easy or medium), `tags`, `algorithm`, `testcase_count` (at least 5), `params` (with type and min/max constraints), `generator` (a working Python script that reads input and produces correct output), and `starter_code`.

Challenge IDs and knowledge point mapping:
- ID 11: Example for `for i in range(n)` — basic counting loop problem
- ID 12: Practice 1 for `for i in range(n)`
- ID 13: Practice 2 for `for i in range(n)`
- ID 14: Example for `range(start, stop, step)` — range parameter problem
- ID 15: Practice 1 for `range(start, stop, step)`
- ID 16: Practice 2 for `range(start, stop, step)`

#### Scenario: All six challenge files exist

- **WHEN** the `docs/challenge/` directory is listed
- **THEN** exactly 6 new files with IDs 11 through 16 SHALL exist alongside the existing 10 challenge files

#### Scenario: Challenge generators produce correct output

- **WHEN** a challenge generator script is executed with valid input matching the params specification
- **THEN** the generator SHALL produce the correct expected output

#### Scenario: Challenge frontmatter is complete

- **WHEN** a new challenge file's frontmatter is parsed
- **THEN** all required fields (`layout`, `id`, `title`, `difficulty`, `tags`, `algorithm`, `testcase_count`, `params`, `generator`, `starter_code`) SHALL be present and valid


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-1 follows all Chapter 1 editorial rules

Section 2-1 SHALL comply with all 12 universal editorial rules defined in the `python-ch1-content` spec:

- P-1 (Punctuation): Em-dashes reserved for dramatic emphasis only; use commas/colons for routine clauses
- T-1 (Terminology): No formal terms before teaching point; controlled forward references when unavoidable
- S-1 (Analogy Bridge): Every analogy preceded by meta-cognitive bridge sentence
- S-2 (Post-Humor Connector): Explicit callback after humor elements within continuous prose
- S-3 (Section Transition): H2 transitions have 2–4 sentences (summary + gap + motivation)
- C-1 (Code Lead-in): Every code block preceded by conversational setup prose
- E-1 (Error Prevention): Common mistakes warned at point of syntax introduction
- M-1 (Mental Model): Compound expressions traced step-by-step (for loops: via Trace Tables)
- F-1 (Image Format): Dual-line format with `![...]()` link + `> 📷` caption
- V-1 (Container Syntax): VitePress containers use `> [!TYPE]` with exclamation mark
- T-3 (No Empty Containers): All visible containers have substantive content
- K-1 (Emotional Punctuation): At least one emotional element per 30 lines, max one per 10 lines; kaomoji variety maintained

Additionally, W-1 (Code/Walkthrough Match) SHALL apply: every code block followed by a walkthrough SHALL have exact correspondence between the code shown and the walkthrough description. T-2 (No Residual Placeholder Markers) SHALL apply: no deferred-content HTML comments or placeholder markers SHALL remain in the published file.

#### Scenario: P-1 compliance — no routine em-dashes

- **WHEN** section 2-1 is scanned for `——` (em-dash) occurrences
- **THEN** every em-dash SHALL be used exclusively for dramatic emphasis or comedic timing; explanatory and causal clauses SHALL use colons or commas

#### Scenario: C-1 compliance — no naked code blocks

- **WHEN** section 2-1 is scanned for fenced code blocks
- **THEN** every code block SHALL have at least one sentence of prose between it and the nearest preceding heading

#### Scenario: K-1 compliance — emotional punctuation density

- **WHEN** section 2-1's prose (excluding code, tables, images) is divided into 30-line blocks
- **THEN** each block SHALL contain at least one emotional punctuation element (kaomoji, joke, student dialogue); no 10-line block SHALL contain more than one

#### Scenario: F-1 compliance — image dual-line format

- **WHEN** section 2-1 is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding `![📷 **圖 N**...](path)` image link line


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-1 opening connects to Module 1 finale hook

The opening of section 2-1 (content between frontmatter and learning objectives) SHALL reference the "100 行 input vs 3 行迴圈" scenario established in 1-4's Module 2 preview. The opening SHALL NOT rebuild motivation from scratch but SHALL build on the existing curiosity established in 1-4.

#### Scenario: Opening references 1-4 preview

- **WHEN** a reader begins section 2-1
- **THEN** the opening content SHALL contain a reference to the contrast between repetitive code and loops as previewed in the Module 1 summary

#### Scenario: Opening does not repeat Module 1 motivation

- **WHEN** the opening is reviewed
- **THEN** it SHALL NOT re-explain "why learn programming" or re-introduce the Judge system (these were covered in 1-1)


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Section 2-1 includes Image Specification Appendix

Section 2-1 SHALL end with an Image Specification Appendix containing the full prompt for each image placeholder in the section. Each entry SHALL include: image number, type (四格漫畫/概念圖/etc.), intent (pedagogical purpose), full prompt (using the VISUAL-STYLE-PREFIX), and notes.

#### Scenario: Every image placeholder has a corresponding appendix entry

- **WHEN** image placeholders in section 2-1 are cross-referenced with the Image Specification Appendix
- **THEN** every `![📷 **圖 N**...]` placeholder SHALL have a matching appendix entry with complete prompt text

<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Knowledge Point B includes range parameter reduction consolidation and arithmetic progression callout

Section 2-1 SHALL contain a subsection under `## range() 的完整用法` titled `### range 的三種寫法，其實是同一招`, positioned after the `### range(start, stop, step)：指定步長` subsection and before the `### 常見錯誤：差一錯誤` subsection.

This subsection SHALL:

1. Frame the three forms of `range()` as **three convenient call styles** that the language provides for three common scenarios, rather than as a single form with "omitted" parameters. The three styles are: full form `range(start, stop, step)`, two-argument form `range(start, stop)` (used when the step is `1`), and one-argument form `range(stop)` (used when both the start is `0` and the step is `1`).
2. Use a step-by-step narrative structure that introduces the three styles in order of increasing parameter count: first show one-argument form, then two-argument, then full form, OR present the full form and then explain how the shorter forms cover the most common defaults — but in either order, the prose SHALL avoid claiming that the shorter forms are "really" the full form with hidden default arguments.
3. Include two fenced code block examples that show the three forms producing equivalent sequences in their respective common scenarios — for example, `range(5)` for "from 0 with step 1", `range(3, 7)` for "from start with step 1", and `range(0, 10, 2)` for "with explicit step".
4. Include a diagram (ASCII inside a fenced code block, or Mermaid) that summarises the three styles side-by-side with a short label for each (e.g., "shortest", "with start", "with step"), without using the word 「省略」 (omission) or claiming hidden defaults.
5. End with a `> [!TIP] 📌 數學小彩蛋` VitePress container that connects `range` output to arithmetic progressions (等差數列), mapping `start` to 首項 (a₁) and `step` to 公差 (d), and quoting the Python Tutorial 4.3 definition: "It generates arithmetic progressions."

The subsection SHALL comply with all 14 editorial rules applicable to non-opening sections, as defined in the `python-ch2-2-1-content` and `python-ch1-content` specs (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, W-1, T-2). O-1 (Opening Motivation) is not applicable as this is not a section opening.

#### Scenario: Parameter reduction subsection exists in correct position

- **WHEN** the H3 headings under `## range() 的完整用法` are listed in document order
- **THEN** `### range 的三種寫法，其實是同一招` SHALL appear after `### range(start, stop, step)：指定步長` and before `### 常見錯誤：差一錯誤`

#### Scenario: Three forms are presented as convenient styles, not as omissions

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** the prose SHALL describe the three forms as "三種便利寫法" or equivalent neutral phrasing
- **AND** the prose SHALL NOT use the word 「省略」 to describe how `range(5)` relates to `range(0, 5, 1)`
- **AND** the prose SHALL NOT claim that `range(5)` is "really" `range(0, 5, 1)` with default arguments

#### Scenario: Three forms each have a labelled code example

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain at least one code example for each of the three forms (`range(stop)`, `range(start, stop)`, `range(start, stop, step)`), each labelled with the scenario it covers

#### Scenario: Diagram summarises three styles without omission language

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain a diagram (ASCII inside a fenced code block, or Mermaid) showing the three styles side-by-side with neutral labels
- **AND** the diagram annotations SHALL NOT contain the word 「省略」 or any phrase claiming hidden defaults

#### Scenario: Arithmetic progression callout uses correct container syntax and content

- **WHEN** the `> [!TIP]` callout at the end of the subsection is reviewed
- **THEN** it SHALL use `> [!TIP]` syntax (V-1 compliant), contain the exact Python Tutorial quote "It generates arithmetic progressions.", and explicitly map `start` to 首項 (a₁) and `step` to 公差 (d)

#### Scenario: No new kaomoji exceed the per-file limit

- **WHEN** the entire `docs/tutor/py/ch2/2-1.md` file is scanned for kaomoji occurrences after the rewrite
- **THEN** each distinct kaomoji used in the rewritten subsection SHALL appear at most 2 times in the entire file (K-1 compliant)

<!-- @trace
source: enhance-2-1-range-reduction
updated: 2026-04-13
code:
  - docs/tutor/py/ch2/2-1.md
-->

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-1.md
-->
---
### Requirement: Section 2-1 explains the rationale for half-open range intervals

Section `docs/tutor/py/ch2/2-1.md` SHALL contain a NOTE or TIP block that explains WHY `range(start, stop)` excludes `stop` (the half-open interval design). The explanation SHALL list at least the following three rationales, each presented as one short sentence using a concrete example a Taiwan high-school student can verify by hand:

1. **Length is easy to compute**: `range(a, b)` contains exactly `b - a` numbers, so `range(1, 7)` has `7 - 1 = 6` numbers without any +1 or -1 correction.
2. **Empty interval is natural**: `range(5, 5)` represents zero numbers; with closed intervals an empty interval would require an awkward notation such as `[5, 4]`.
3. **Clean splitting**: `range(0, 10)` can be split as `range(0, 5)` followed by `range(5, 10)` with no overlap and no gap, which matches how list slicing and divide-and-conquer algorithms work.

The block SHALL be positioned within or immediately adjacent to the existing "常見錯誤：差一錯誤" subsection so that the rationale appears together with the off-by-one warning. The previous hand-waving phrase "用久了你會發現這個設計其實很方便（後面會解釋為什麼）" SHALL be removed or rewritten so that the section no longer defers the explanation indefinitely.

#### Scenario: Three rationales appear together

- **WHEN** the rationale block in section 2-1 is reviewed
- **THEN** the block SHALL contain three labelled rationales (length, empty interval, clean splitting), each with a concrete numeric example a learner can verify

#### Scenario: Indefinite deferral phrase is removed

- **WHEN** section 2-1 is scanned for the phrase pattern "用久了你會發現這個設計其實很方便（後面會解釋為什麼）"
- **THEN** zero occurrences SHALL remain

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Section 2-1 includes a "range is not a list" note

Section `docs/tutor/py/ch2/2-1.md` SHALL contain a NOTE block that addresses the common beginner confusion of treating `range(n)` as a list. The block SHALL:

1. Show that `print(range(5))` outputs `range(0, 5)`, not `0 1 2 3 4` or `[0, 1, 2, 3, 4]`.
2. Explain in one sentence that `range` is a "lazy sequence" object that produces numbers on demand rather than storing them eagerly.
3. Show that `list(range(5))` produces `[0, 1, 2, 3, 4]` for the case where the learner wants to inspect the full sequence — and explicitly mark `list` as a forward reference (taught in a later chapter).

The block MUST appear after the three-form `range()` teaching is complete and before the section's "本節小結" closing summary, so that learners encounter the clarification while the `range()` material is still fresh.

#### Scenario: Note explains print(range(n)) output

- **WHEN** the "range is not a list" note in section 2-1 is reviewed
- **THEN** it SHALL contain a code example or inline statement showing that `print(range(5))` outputs `range(0, 5)`

#### Scenario: Note shows list(range(n)) inspection method

- **WHEN** the "range is not a list" note in section 2-1 is reviewed
- **THEN** it SHALL contain a code example or inline statement showing that `list(range(5))` outputs `[0, 1, 2, 3, 4]`, with `list` marked as a forward reference

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Section 2-1 uses unified step terminology

Section `docs/tutor/py/ch2/2-1.md` SHALL use a single, unified terminology for describing the `step` parameter of `range()`:

- For positive `step` (forward iteration): the section SHALL use the phrase pattern "每次加 N" (where N is the absolute value).
- For negative `step` (backward iteration): the section SHALL use the phrase pattern "每次減 N" (where N is the absolute value, no negative sign in the phrase).
- The Mathematical synonym 「步長」may be used in formal definitions and 「公差」may be used in arithmetic-progression contexts, but the running prose SHALL consistently use 「每次加 N」/「每次減 N」.

The following alternative phrases SHALL NOT appear when describing `step` in section 2-1: 「每次跳 N」, 「每次增加 N」, 「每隔 N 遍」, 「每次加 -N」.

In particular, the existing description "如果你想『每隔 2 遍寫一次』" is technically incorrect (it describes a strided sequence with stride 3, not 2) and SHALL be rewritten to use the unified phrase 「每次加 2」.

#### Scenario: Step terminology is unified to "每次加 N" / "每次減 N"

- **WHEN** section 2-1 is scanned for descriptions of the `step` parameter
- **THEN** every description SHALL use the phrase pattern 「每次加 N」 (positive step) or 「每次減 N」 (negative step)

#### Scenario: Misleading "每隔 N 遍" phrase is removed

- **WHEN** section 2-1 is scanned for the phrase 「每隔 2 遍寫一次」 or similar 「每隔 N 遍」 patterns referring to `step`
- **THEN** zero occurrences SHALL remain

#### Scenario: Negative step is described with positive magnitude

- **WHEN** section 2-1 describes a `range(...)` call with a negative `step`
- **THEN** the prose SHALL describe the behavior as "每次減 |step|" (using the absolute value), not as "每次加 -|step|"

##### Example: replacement table

| Old phrase | Replacement |
| ---------- | ----------- |
| 「如果你想『每隔 2 遍寫一次』」 | 「如果你想『每次加 2』，產生像 0, 2, 4, 6, 8 這樣的數列」 |
| 「`i` 每次跳 2」 | 「`i` 每次加 2」 |
| 「每次加 -2」 | 「每次減 2」 |
| 「從 1 開始，每次跳 2」 | 「從 1 開始，每次加 2」 |

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-1.md
-->
