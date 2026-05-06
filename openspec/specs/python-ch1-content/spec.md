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


<!-- @trace
source: revise-ch1-3-exercises
updated: 2026-04-10
code:
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
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

To reduce ambiguity, the following decision checklist SHALL be applied when evaluating each `——` occurrence:

1. If `——` is followed by a causal clause (因為/由於/因此) → replace with colon (：)
2. If `——` is followed by a rhetorical or clarifying question → replace with comma (，)
3. If `——` introduces a definition or explanation of the preceding term → replace with colon (：)
4. If `——` introduces a contrast or pivot where the content after the dash is genuinely unexpected or humorous → KEEP the em-dash
5. If none of the above apply, default to replacing with comma (，)

#### Scenario: Routine clause uses comma or colon instead of em-dash

- **WHEN** a tutorial section contains a clause that explains a preceding term (e.g., "X的用途——它會...")
- **THEN** the em-dash SHALL be replaced with a colon (e.g., "X的用途：它會...")

#### Scenario: Dramatic em-dash is preserved

- **WHEN** a tutorial section contains an em-dash used for comedic timing or narrative surprise in a hook paragraph
- **THEN** the em-dash SHALL be preserved

#### Scenario: Causal clause following em-dash

- **WHEN** a tutorial section contains `——因為` or `——由於` or `——因此`
- **THEN** the em-dash SHALL be replaced with a colon (e.g., "大概會崩潰：因為在數學裡...")

#### Scenario: Term definition following em-dash

- **WHEN** a tutorial section contains a pattern where a bolded technical term is immediately followed by `——` and a plain-language restatement (e.g., "**Flow Control**——讓程式根據條件...")
- **THEN** the em-dash SHALL be replaced with a colon (e.g., "**Flow Control**：讓程式根據條件...")


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
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

When a humor element appears at the end of an H3 sub-section and the next structural element is a new H3 heading, the connector requirement SHALL be relaxed: the H3 heading itself serves as a structural boundary. In this case, if the first sentence of prose under the new H3 heading naturally continues the topic, no explicit callback connector is required. However, if the new H3 introduces a substantially different sub-topic, the first sentence of prose under that heading SHALL include a brief connector or transition phrase.

#### Scenario: Joke followed by connector before resuming exposition

- **WHEN** a tutorial section contains a parenthetical joke or kaomoji-decorated comedic aside within a continuous prose block
- **THEN** the immediately following sentence SHALL contain an explicit connector that links back to the expository point preceding the joke

#### Scenario: Humor at H3 boundary with same-topic continuation

- **WHEN** a humor element is the last content of an H3 sub-section AND the next H3 sub-section continues the same overarching topic
- **THEN** no explicit callback connector is required; the heading boundary provides sufficient structural separation

#### Scenario: Humor at H3 boundary with topic change

- **WHEN** a humor element is the last content of an H3 sub-section AND the next H3 sub-section introduces a substantially different sub-topic
- **THEN** the first sentence of prose under the new H3 heading SHALL include a brief transition phrase (e.g., "接下來換個方向" or a reference linking to the previous sub-section's conclusion)


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
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

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from `docs/tutor/py/ch1/1-1.md` and `docs/tutor/py/ch1/appendix.md`. No placeholder or deferred-content markers SHALL remain in published tutorial sections of Chapter 1.

#### Scenario: No TBD markers in 1-1.md

- **WHEN** `docs/tutor/py/ch1/1-1.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found

#### Scenario: No TBD markers in appendix.md

- **WHEN** `docs/tutor/py/ch1/appendix.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found


<!-- @trace
source: ch1-appendix-keywords-table
updated: 2026-04-12
code:
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch1/1-4.md
  - .vitepress/config.mts
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Chapter 1 image placeholders follow dual-line format rule F-1

Every image placeholder in `docs/tutor/py/ch1/` SHALL use a dual-line format consisting of:

1. An image link line: `![📷 **圖 N**：description（AI 製圖）](/assets/tutor/py/ch1/figNN.png)`
2. A caption line: `> 📷 **圖 N**：description（AI 製圖）`

If the image file has not yet been generated, the image link SHALL still be present with the planned filename as a placeholder path. Single-line caption-only format (`> 📷 ...` without the preceding `![](...)`) SHALL NOT be used.

#### Scenario: Image placeholder has both link and caption

- **WHEN** a tutorial section is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding `![📷 **圖 N**...](path)` image link line

#### Scenario: Ungenerated image still has link placeholder

- **WHEN** an image file has not yet been created
- **THEN** the image link line SHALL still exist with the planned filename (e.g., `![📷 **圖 9**：...](/assets/tutor/py/ch1/圖九.png)`) so that the format is consistent and the path is ready when the file is generated

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 VitePress custom containers use correct syntax rule V-1

All VitePress custom container callouts in `docs/tutor/py/ch1/` SHALL use the correct syntax `> [!TYPE]` where TYPE is one of `NOTE`, `TIP`, `WARNING`, `DANGER`, `DETAILS`. The exclamation mark (`!`) inside the brackets is mandatory. The pattern `> [TYPE]` without `!` SHALL NOT be used as it will not render correctly.

#### Scenario: Custom container uses correct syntax

- **WHEN** a tutorial section contains a blockquote-based custom container
- **THEN** the opening line SHALL match the pattern `> [!TYPE]` (with exclamation mark)

#### Scenario: Incorrect syntax is detected

- **WHEN** a tutorial section contains a pattern matching `> [WARNING]`, `> [TIP]`, `> [NOTE]`, `> [DANGER]`, or `> [DETAILS]` without the `!`
- **THEN** the pattern SHALL be corrected to include the `!` (e.g., `> [WARNING]` → `> [!WARNING]`)

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections contain no empty UI elements rule T-3

Published tutorial sections in `docs/tutor/py/ch1/` SHALL NOT contain custom container blocks (NOTE, TIP, WARNING, DANGER, DETAILS) where the title line exists but the body content is empty or contains only whitespace. If the content for a container is not yet ready, the entire container block SHALL be wrapped in an HTML comment (e.g., `<!-- DEFERRED: description -->`) so it is invisible to readers.

#### Scenario: Empty container is hidden

- **WHEN** a tutorial section contains a custom container whose body has no substantive content
- **THEN** the entire container block (title and body) SHALL be wrapped in HTML comments (e.g., `<!-- DEFERRED: ... -->`), not left as a visible empty box

#### Scenario: Completed container has content

- **WHEN** a custom container is visible (not inside HTML comments)
- **THEN** the container body SHALL contain at least one sentence of substantive content

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: Chapter 1 sections follow emotional punctuation density rule K-1

Each tutorial section in `docs/tutor/py/ch1/` SHALL maintain a balanced density of emotional punctuation elements (kaomoji, parenthetical jokes, student dialogue interjections). Within any contiguous block of 30 lines of prose (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element SHALL be present. Within any contiguous block of 10 lines of prose, no more than one emotional punctuation element SHALL be present.

Additionally, kaomoji variety SHALL be maintained:

- The same kaomoji SHALL NOT appear more than twice within a single section file.
- Across all files within the same chapter (e.g., `1-1.md` through `1-4.md`), the same kaomoji SHALL NOT appear more than three times.
- Each section file SHALL use kaomoji from at least two different emotional categories as defined in the `phoenix-popular-science-article-style` kaomoji catalog: Resigned, Celebration, Shock, Frustration, Sadness, Cute, Mischievous, Confusion.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose (excluding code, tables, images) is identified in a tutorial section
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a contiguous block of 10 lines of prose is identified in a tutorial section
- **THEN** no more than one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Kaomoji is not overused within a single file

- **WHEN** a tutorial section file is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice in that file

#### Scenario: Kaomoji is not overused across a chapter

- **WHEN** all section files within a chapter are scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than three times across the entire chapter

#### Scenario: Kaomoji emotional variety is maintained

- **WHEN** a tutorial section file is scanned for kaomoji emotional categories
- **THEN** the file SHALL contain kaomoji from at least two different emotional categories

<!-- @trace
source: ch1-full-eal-pass
updated: 2026-04-09
code:
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch1/1-1.md
  - phoenix-popular-science-article-style-enhance.md
  - docs/tutor/py/ch1/1-2.md
  - docs/tutor/py/ch1/1-3.md
-->

---
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

<!-- @trace
source: revise-ch1-4-exercise
updated: 2026-04-10
code:
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
-->

---
### Requirement: Mathematical expressions in section 1-3 use LaTeX syntax

Section `1-3.md` SHALL use LaTeX inline math syntax (`$...$`) for all mathematical expressions, including but not limited to quadratic equation notation (`$ax^2 + bx + c = 0$`), discriminant formula (`$D = b^2 - 4ac$`), and squared terms (`$b^2$`). Unicode superscript characters (e.g., `²`) SHALL NOT be used for mathematical notation.

#### Scenario: Quadratic equation formula renders as LaTeX

- **WHEN** a reader views section 1-3 in the browser
- **AND** the section discusses the quadratic equation
- **THEN** the formula SHALL be rendered as formatted LaTeX math (`$ax^2 + bx + c = 0$`) rather than plain Unicode text (`ax² + bx + c = 0`)

#### Scenario: Discriminant formula renders as LaTeX

- **WHEN** a reader views section 1-3 in the browser
- **AND** the section discusses the discriminant
- **THEN** the formula SHALL be rendered as formatted LaTeX math (`$D = b^2 - 4ac$`) rather than plain Unicode text (`D = b² − 4ac`)

<!-- @trace
source: convert-math-to-latex
updated: 2026-04-10
code:
  - docs/challenge/password-check.md
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/package.json
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/.vitepress/cache/deps/vue.js
  - docs/tutor/py/ch1/1-4.md
  - .vitepress/config.mts
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/challenge/quadratic-discriminant.md
  - package.json
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
-->

---
### Requirement: Section 1-3 uses Mermaid flowchart for leap year logic

Section `1-3.md` SHALL use a Mermaid `flowchart TD` diagram to illustrate the leap year decision logic, replacing the existing ASCII art flowchart. The Mermaid diagram SHALL preserve the same logical structure: three sequential divisibility checks (400, 100, 4) with Yes/No branches leading to 閏年 or 平年 outcomes. The diagram SHALL include a custom Mermaid theme configuration for consistent visual styling.

#### Scenario: Leap year flowchart renders as Mermaid SVG

- **WHEN** a reader views section 1-3 in the browser
- **AND** the page reaches the flowchart section
- **THEN** the leap year decision logic SHALL be displayed as a rendered Mermaid flowchart SVG
- **AND** no ASCII art code block SHALL be present for this diagram

#### Scenario: Flowchart preserves correct decision logic

- **WHEN** the Mermaid flowchart is inspected
- **THEN** it SHALL contain three diamond-shaped decision nodes for `year % 400 == 0`, `year % 100 == 0`, and `year % 4 == 0`
- **AND** each decision node SHALL have Yes and No branches
- **AND** the terminal nodes SHALL display 閏年 or 平年


<!-- @trace
source: convert-ascii-to-mermaid
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - package.json
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/.vitepress/cache/deps/vue.js
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/package.json
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/challenge/password-check.md
-->

---
### Requirement: Section 1-4 uses Mermaid mindmap for knowledge map

Section `1-4.md` SHALL use a Mermaid `mindmap` diagram to illustrate the Module 1 knowledge map, replacing the existing ASCII art tree. The Mermaid diagram SHALL preserve the same hierarchical structure: root node 程式語言（Python） branching into three sections (1-1 I/O 基礎, 1-2 資料與運算, 1-3 流程控制) with their respective skill nodes.

#### Scenario: Knowledge map renders as Mermaid SVG

- **WHEN** a reader views section 1-4 in the browser
- **AND** the page reaches the knowledge map section
- **THEN** the Module 1 knowledge map SHALL be displayed as a rendered Mermaid mindmap SVG
- **AND** no ASCII art code block SHALL be present for this diagram

#### Scenario: Mindmap preserves all skill nodes

- **WHEN** the Mermaid mindmap is inspected
- **THEN** it SHALL contain a root node for 程式語言（Python）
- **AND** it SHALL contain three branch nodes for the three sections
- **AND** each branch SHALL list the same skill items as the original ASCII tree

<!-- @trace
source: convert-ascii-to-mermaid
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - package.json
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/.vitepress/cache/deps/vue.js
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/package.json
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/challenge/password-check.md
-->

---
### Requirement: Chapter 1 appendix image specifications use ordered lists

The `docs/tutor/py/ch1/appendix.md` file's "Image Specification Appendix" section SHALL format each image's property entries as an ordered list using standard Markdown numbered syntax (`1. 2. 3. 4.`), not as unordered bullet lists.

Each image entry SHALL contain exactly four ordered items in the following fixed sequence:
1. **類型**：image type and narrative role (e.g., 四格漫畫（Hook）)
2. **意圖**：teaching intent — what concept this image reinforces
3. **完整 Prompt**：the full English AI generation prompt
4. **備註**：production notes for rendering or composition

This ordered list format SHALL be compatible with standard Markdown as rendered by both VitePress and Slidev (no Slidev-specific extensions required; plain `1. 2. 3. 4.` syntax is sufficient).

#### Scenario: Image specification entries render as numbered list

- **WHEN** a user visits `docs/tutor/py/ch1/appendix.md` in the browser
- **THEN** each image's property block (類型, 意圖, 完整 Prompt, 備註) MUST be rendered as a numbered ordered list with items 1 through 4

#### Scenario: Ordered list is valid Slidev-compatible Markdown

- **WHEN** the appendix content is imported into a Slidev presentation file
- **THEN** the ordered list SHALL render correctly without requiring any Slidev-specific syntax, because standard Markdown `1. Item` numbered lists are natively supported by Slidev

<!-- @trace
source: show-appendix-in-sidebar
updated: 2026-04-12
code:
  - docs/tutor/py/ch1/appendix.md
-->

<!-- @trace
source: show-appendix-in-sidebar
updated: 2026-04-12
code:
  - .vitepress/config.mts
  - .vitepress/sidebar.ts
  - docs/tutor/py/ch1/appendix.md
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

---
### Requirement: Chapter 1 appendix contains Python keywords reference table

The file `docs/tutor/py/ch1/appendix.md` SHALL contain a dedicated H1 section titled `# Python Keywords Table` that presents a complete reference table for all Python 3.13 reserved words.

The table SHALL list every hard keyword returned by `keyword.kwlist` (35 entries: `False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`) and every soft keyword returned by `keyword.softkwlist` (4 entries: `_`, `case`, `match`, `type`), for a total of 39 rows.

The table SHALL be grouped by semantic category using H2 subheadings (for example: 常數值 / 邏輯運算 / 條件判斷 / 迴圈控制 / 函式與類別 / 例外處理 / 匯入 / 範圍與作用域 / 非同步 / 其他 / 軟關鍵字). Each row SHALL contain at minimum: the keyword itself, a one-line Traditional Chinese description, and a "first-taught" column indicating the chapter/section where the keyword is introduced or `—` if not yet taught.

The appendix SHALL include an introductory paragraph before the table explaining:
1. What "reserved words" are and why Python forbids using them as identifiers
2. A concrete `SyntaxError` example showing what happens if a learner tries `if = 3`
3. A pedagogical note distinguishing hard keywords from soft keywords (soft keywords are reserved only in specific contexts)

Keywords introduced in Chapter 1 (`True`, `False`, `and`, `or`, `not`, `if`, `elif`, `else`) SHALL be visually marked (e.g., with a checkmark emoji or the cell value `1-3`) so learners can self-assess progress.

#### Scenario: Appendix contains all 39 Python 3.13 keywords

- **WHEN** `docs/tutor/py/ch1/appendix.md` is rendered as HTML
- **THEN** the `# Python Keywords Table` section SHALL contain at least one row per keyword in `keyword.kwlist` and `keyword.softkwlist` under Python 3.13 (39 rows total)

#### Scenario: Chapter 1 taught keywords are marked

- **WHEN** a learner reads the keywords table after finishing section 1-3
- **THEN** the rows for `True`, `False`, `and`, `or`, `not`, `if`, `elif`, and `else` SHALL display a "first-taught" indicator pointing to section `1-3` (or an equivalent visual marker)

#### Scenario: Reserved word explanation precedes the table

- **WHEN** the appendix is read top-to-bottom
- **THEN** an explanatory paragraph defining "reserved words" and showing a `SyntaxError` example SHALL appear before the first keyword row of the table

#### Scenario: Soft keywords are distinguished from hard keywords

- **WHEN** the keywords table is rendered
- **THEN** soft keywords (`_`, `case`, `match`, `type`) SHALL be placed under a distinct subheading or column value that clearly identifies them as "soft" / context-sensitive keywords separate from hard keywords

<!-- @trace
source: ch1-appendix-keywords-table
updated: 2026-04-12
code:
  - docs/tutor/py/ch1/appendix.md
-->

<!-- @trace
source: ch1-appendix-keywords-table
updated: 2026-04-12
code:
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
  - .vitepress/sidebar.ts
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch1/1-4.md
  - .vitepress/config.mts
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->
---
### Requirement: Section 1-2 introduces string operators (concatenation and repetition)

Section `docs/tutor/py/ch1/1-2.md` SHALL include a dedicated subsection that formally introduces two string operators before any later chapter uses them:

1. **String concatenation `+`**: explains that `"Hello" + " " + "World"` produces `"Hello World"` and that the `+` operator on strings means joining (not arithmetic addition).
2. **String repetition with integer `*`**: explains that `"*" * 5` produces `"*****"` and that multiplying a string by a positive integer N repeats the string N times.

The subsection SHALL contrast string `+`/`*` with numeric `+`/`*` (same operator symbols, different semantics) and SHALL include at least one common-error note (e.g., `"abc" * 0` yields the empty string; `"abc" + 1` raises `TypeError`).

The subsection SHALL be positioned after the introduction of `str` (字串) within the existing "資料型別" H2 section and before the "input() 的型別陷阱" subsection, so that string operations are taught immediately after string type and before any I/O cast example.

#### Scenario: Section 1-2 contains string operator subsection

- **WHEN** the H3 headings under the "資料型別" H2 section of `docs/tutor/py/ch1/1-2.md` are listed in document order
- **THEN** an H3 subsection that introduces `+` (concatenation) and `*` (repetition) on strings SHALL appear after the H3 that introduces the three basic types and before the H3 that introduces `int(input())` cast usage

#### Scenario: String concatenation example produces correct output

- **WHEN** the code example `print("Hello" + " " + "World")` from the new subsection is executed
- **THEN** the output SHALL be exactly `Hello World` (one space between Hello and World, no trailing whitespace)

#### Scenario: String repetition example produces correct output

- **WHEN** the code example `print("*" * 5)` from the new subsection is executed
- **THEN** the output SHALL be exactly `*****` (five asterisks, no trailing whitespace)

#### Scenario: Subsection includes operator-overloading contrast note

- **WHEN** the new subsection is reviewed
- **THEN** it SHALL contain explicit prose stating that the `+` and `*` operators have different semantics for strings (join, repeat) versus numbers (add, multiply), so that a learner can answer the question "why does `+` join strings instead of adding them?"

#### Scenario: Subsection includes a common-error note

- **WHEN** the new subsection is reviewed
- **THEN** it SHALL include at least one warning, NOTE, or inline example of a common pitfall — for example, that `"abc" + 1` raises `TypeError` because `+` cannot mix str and int, and that `"abc" * 0` yields an empty string

##### Example: behavior table

| Expression | Result | Notes |
| ---------- | ------ | ----- |
| `"Hello" + "World"` | `"HelloWorld"` | concatenation, no implicit space |
| `"abc" * 3` | `"abcabcabc"` | repetition by positive integer |
| `"abc" * 0` | `""` | empty string |
| `"abc" + 1` | `TypeError` | cannot mix str and int with `+` |
| `"abc" * 1.5` | `TypeError` | repetition factor must be int, not float |

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch1/1-2.md
-->
