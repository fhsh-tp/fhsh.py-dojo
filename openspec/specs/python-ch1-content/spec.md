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

---
### Requirement: Chapter 1 sections follow punctuation style rule P-1

Each tutorial section in `docs/tutor/py/ch1/` SHALL use commas (，) or colons (：) for routine clause separation. The em-dash (`——`) SHALL be reserved exclusively for dramatic emphasis in hooks and humor. Em-dashes SHALL NOT be used for explanatory clauses (use colons) or continuation clauses (use commas).

#### Scenario: Routine clause uses comma or colon instead of em-dash

- **WHEN** a tutorial section contains a clause that explains a preceding term (e.g., "X的用途——它會...")
- **THEN** the em-dash SHALL be replaced with a colon (e.g., "X的用途：它會...")

#### Scenario: Dramatic em-dash is preserved

- **WHEN** a tutorial section contains an em-dash used for comedic timing or narrative surprise in a hook paragraph
- **THEN** the em-dash SHALL be preserved


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow terminology forward-reference rule T-1

Tutorial sections SHALL NOT use a formal technical term before its designated teaching point. If a concept MUST be referenced before being formally taught, the section SHALL use a plain-language description OR a controlled forward reference (term introduced, immediately explained in parentheses, with a statement of when it will be properly taught).

#### Scenario: Term used before teaching point is replaced with plain language

- **WHEN** a section references a concept (e.g., "變數") that is formally introduced in a later section
- **THEN** the reference SHALL use a plain-language equivalent (e.g., "資料儲存空間") instead of the formal term

#### Scenario: Controlled forward reference includes explanation and promise

- **WHEN** a formal term MUST be used before its teaching point (unavoidable forward reference)
- **THEN** the term SHALL be immediately followed by a parenthetical plain-language explanation AND a statement indicating which section will formally teach it (e.g., "...這個**變數（Variable）**...（下一節會正式介紹）")


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow analogy bridge rule S-1

Every analogy or metaphor in a tutorial section SHALL be preceded by a meta-cognitive bridge — one sentence explaining WHY the comparison is being made, before the comparison itself.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** a tutorial section introduces an analogy (e.g., calculator analogy for print(), locker analogy for variables)
- **THEN** the preceding sentence SHALL state the purpose of the analogy (e.g., "Why am I talking about calculators? Because...")


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions), the next sentence SHALL include an explicit callback connector that resumes the narrative thread (e.g., "沒錯！", "回到正題", or a reference to the pre-joke assertion).

#### Scenario: Joke followed by connector before resuming exposition

- **WHEN** a tutorial section contains a parenthetical joke or kaomoji-decorated comedic aside
- **THEN** the immediately following sentence SHALL contain an explicit connector that links back to the expository point preceding the joke


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow section transition rule S-3

Transitions between major conceptual sections (H2-level boundaries) SHALL contain 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap or limitation, and (c) motivate the next section. Single-sentence transitions SHALL only be used between sub-steps within the same H2 section.

#### Scenario: Major section transition has adequate scaffolding

- **WHEN** an H2 section ends and the next H2 section begins
- **THEN** the transition block (between the closing `---` and the next `##` heading) SHALL contain 2–4 sentences covering summary, gap identification, and motivation

#### Scenario: Sub-step transition within same section is concise

- **WHEN** a transition occurs between H3 sub-steps within the same H2 section
- **THEN** the transition SHALL be 1–2 sentences


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 code blocks follow conversational lead-in rule C-1

Every fenced code block (` ```python ``` `) in a tutorial section SHALL be preceded by at least one sentence of conversational setup that establishes context for why the code is being shown. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** a tutorial section contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading (H2/H3) and the opening code fence


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow error prevention rule E-1

Common beginner syntax mistakes (e.g., quote mixing, `=` vs `==` confusion, missing `int()` conversion) SHALL be addressed immediately after the syntax is first introduced, not deferred exclusively to a "common errors" section at the end of a problem walkthrough.

#### Scenario: Syntax pitfall warned at point of introduction

- **WHEN** a tutorial section introduces a syntax element that has a known high-frequency beginner mistake
- **THEN** a warning or note about the mistake SHALL appear within the same sub-section where the syntax is first taught


<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 code examples follow mental model rule M-1

When a code example implicitly demonstrates a fundamental evaluation concept (e.g., inside-out expression evaluation, operator precedence), the tutorial section SHALL make the concept explicit with a step-by-step trace showing the evaluation order.

#### Scenario: Expression evaluation is traced step-by-step

- **WHEN** a code example contains a compound expression (e.g., `print(1+1)`, `int(input())`, compound boolean expressions)
- **THEN** the accompanying explanation SHALL include a numbered trace showing each evaluation step (e.g., "Step 1: Python evaluates 1+1 → 2. Step 2: Python calls print(2) → prints '2'")

#### Scenario: Later sections callback to earlier mental model

- **WHEN** a later section uses the same evaluation pattern introduced in an earlier section
- **THEN** the explanation SHALL include a brief callback reference to the earlier example (e.g., "Remember how print(1+1) evaluates from inside out? int(input()) works the same way")

<!-- @trace
source: ch1-polish-1-1
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 section 1-1 opening addresses learner motivation rule O-1

The opening section of `docs/tutor/py/ch1/1-1.md` (content between the frontmatter and the learning objectives) SHALL address the question "Why learn programming?" before introducing technical concepts. The opening SHALL include a personal anecdote from the instructor (learning programming for allowance money) and a positive payoff ("opened a new world"). The opening SHALL be longer than a single paragraph to provide adequate rapport-building for zero-base learners.

#### Scenario: Opening contains motivation before technical content

- **WHEN** a reader begins section 1-1
- **THEN** the first substantive content after the H1 heading SHALL answer "why learn programming" with a personal story, before any mention of programming languages, compilers, or computer science concepts

#### Scenario: Opening includes instructor personal anecdote

- **WHEN** the opening motivation section is reviewed
- **THEN** it SHALL contain an anecdote about the instructor's first motivation for learning programming (allowance money from parent) and a positive transformation statement


<!-- @trace
source: ch1-fix-1-1-tbd
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/appendix.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/1-1/圖二.png
  - .vitepress/theme/custom.css
  - docs/public/assets/tutor/py/1-1/圖四.png
  - .vitepress/theme/index.ts
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/nav.yml
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/challenge/hello-world.md
-->

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


<!-- @trace
source: ch1-fix-1-1-tbd
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/appendix.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/1-1/圖二.png
  - .vitepress/theme/custom.css
  - docs/public/assets/tutor/py/1-1/圖四.png
  - .vitepress/theme/index.ts
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/nav.yml
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/challenge/hello-world.md
-->

---
### Requirement: Chapter 1 sections contain no residual TBD markers rule T-2

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from `docs/tutor/py/ch1/1-1.md`. No placeholder or deferred-content markers SHALL remain in published tutorial sections.

#### Scenario: No TBD markers in 1-1.md

- **WHEN** `docs/tutor/py/ch1/1-1.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found

<!-- @trace
source: ch1-fix-1-1-tbd
updated: 2026-04-08
code:
  - docs/tutor/py/ch1/appendix.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/1-1/圖二.png
  - .vitepress/theme/custom.css
  - docs/public/assets/tutor/py/1-1/圖四.png
  - .vitepress/theme/index.ts
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch1/1-1.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/nav.yml
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/challenge/hello-world.md
-->