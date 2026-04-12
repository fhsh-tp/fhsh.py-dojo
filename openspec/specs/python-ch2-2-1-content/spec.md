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