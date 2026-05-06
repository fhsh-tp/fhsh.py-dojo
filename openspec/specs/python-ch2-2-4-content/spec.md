# python-ch2-2-4-content Specification

## Purpose

Defines requirements for section 2-4 of the Python tutorial (nested loops — 巢狀迴圈), including the tutorial document, 8–10 challenge files for nested loop pattern printing and applications, all associated trace tables, image placeholders, and editorial compliance rules.

## Requirements

### Requirement: Section 2-4 file exists with correct frontmatter and structure

The file `docs/tutor/py/ch2/2-4.md` SHALL exist with frontmatter fields: `layout: doc`, `title` (display title for the nested loops section), `description` (one-line summary), `chapter: 2`, `section: "2-4"`, `createdTime` in ISO 8601 with `+08:00` timezone, and `challenge` referencing the slug of the primary example challenge.

The file SHALL include a `VISUAL-STYLE-PREFIX` HTML comment immediately after the frontmatter, using the same American stick figure comic style as Chapter 1 and sections 2-1 through 2-3.

#### Scenario: Section file has valid frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-4.md` SHALL be parsed successfully with all required frontmatter fields (`layout`, `title`, `description`, `chapter`, `section`, `createdTime`, `challenge`) present and non-empty

#### Scenario: Section file appears in sidebar

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar SHALL display a link to section 2-4


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-4 covers nested loops as two knowledge points

Section 2-4 SHALL teach exactly two knowledge points:

- **Knowledge Point A**: 雙重 for 迴圈基礎 — How to place one `for` loop inside another, the execution order (outer loop controls rows, inner loop controls columns), indentation rules for nested blocks, and pattern printing (right triangle of `*`, rectangle of `*`, multiplication table 九九乘法表).
- **Knowledge Point B**: 巢狀迴圈應用 — Combining nested loops with conditionals (`if` inside inner loop), counting patterns (pairs that satisfy a condition), advanced pattern printing (isosceles triangle, inverted triangle, diamond), and performance intuition ("if outer runs N times and inner runs M times, total is N×M").

Section 2-4 SHALL NOT formally introduce or use the following concepts (T-1 compliance): `list`, `dict`, `tuple`, `def` (functions), recursion, list comprehension, or `enumerate`. If any of these concepts MUST be referenced for motivational context, a controlled forward reference SHALL be used (plain-language description + parenthetical explanation + promise of when it will be formally taught in a specific future section).

#### Scenario: Knowledge Point A is taught before Knowledge Point B

- **WHEN** a reader reads section 2-4 sequentially
- **THEN** the basic nested for loop concept (pattern printing, multiplication table) SHALL appear before the application concepts (conditional combinations, counting patterns, advanced patterns)

#### Scenario: No formal use of list, dict, functions, or advanced constructs

- **WHEN** section 2-4 is scanned for the keywords `list`, `dict`, `tuple`, `def`, `lambda`, `enumerate`, or list comprehension syntax `[x for x in ...]`
- **THEN** zero occurrences SHALL be found outside of controlled forward references

#### Scenario: Multiplication table uses nested for loop with proper formatting

- **WHEN** the multiplication table example is presented
- **THEN** the code SHALL use two nested `for` loops with `range()`, and the output SHALL be formatted as a grid with aligned columns


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Each knowledge point has a trace table demonstrating nested loop execution

Every nested `for` loop code example in section 2-4 that introduces a new loop pattern SHALL be accompanied by a Trace Table showing the value of outer and inner loop variables, the condition (if any), and the output at each iteration.

The Trace Table SHALL have columns for: outer iteration, inner iteration, loop variable values, condition result (if applicable), and output/action. Trace Tables for nested loops with combined iterations exceeding 15 SHALL abbreviate middle rows with `...` but SHALL show at least the first 6 iterations (covering at least 2 complete outer iterations) and the last 2 iterations.

#### Scenario: Basic nested loop has trace table

- **WHEN** the first nested `for` loop code example is presented (e.g., right triangle pattern)
- **THEN** a Trace Table SHALL immediately follow showing each iteration's outer variable, inner variable, and output

#### Scenario: Multiplication table has abbreviated trace table

- **WHEN** the multiplication table example is presented (9×9 = 81 iterations)
- **THEN** the Trace Table SHALL show the first 6 iterations (outer=1 inner=1,2,...; outer=2 inner=1,...), then `...`, then the last 2 iterations (outer=9 inner=8,9)


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-4 includes 4 AI image specifications

Section 2-4 SHALL include exactly 4 image placeholders in the article body, using the dual-line format (F-1 rule): `![圖N：描述（AI 製圖）](/assets/tutor/py/ch2/figNN.png)` followed by `> 📷 **圖 N**：描述（AI 製圖）`.

The 4 images SHALL cover:
1. A hook/opening image (Hook type) — humorous illustration of the concept of "loops inside loops"
2. An explanation image (Explanation type) — visual diagram showing nested loop execution flow (outer/inner relationship)
3. An analogy image (Analogy type) — daily-life analogy for nested loops (e.g., checking every seat in every row of a theater)
4. A tutorial image (Tutorial type) — visual showing pattern printing process step by step

Each image SHALL have a complete specification in the appendix (`docs/tutor/py/ch2/appendix.md`) including: 類型, 意圖, 完整 Prompt (with VISUAL-STYLE-PREFIX expanded), and 備註.

#### Scenario: All 4 images use dual-line format

- **WHEN** section 2-4 is scanned for image placeholders
- **THEN** exactly 4 image placeholders SHALL be found, each using the dual-line format (markdown image link + blockquote caption)

#### Scenario: Image numbering is globally sequential within chapter

- **WHEN** image numbers in section 2-4 are compared with previous sections (2-1, 2-2, 2-3)
- **THEN** the numbering SHALL continue sequentially from where 2-3 ended (no gaps, no duplicates)


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-4 has 8-10 Judge challenges in APCS beginner transition format

Section 2-4 SHALL include 8 to 10 Judge challenges: 2 example problems (例題) with full step-by-step solutions and 6-8 practice problems (類題) with only problem statements and hints.

**Example problems (例題) format:**
1. Judge 解題實戰 section with full IPO analysis (Step 1: 分析 IPO, Step 2: 寫程式碼, Step 3: 逐行解讀, Step 4: 常見錯誤)
2. `<ChallengeLink slug="..." />` component for Judge submission
3. Complete solution code with line-by-line walkthrough

**Practice problems (類題) format:**
1. Problem title with `<ChallengeLink slug="..." />` component
2. Problem statement (題目說明) in conversational tone
3. Explicit 「輸入格式」section with line-by-line input specification
4. Explicit 「輸出格式」section with exact output requirements
5. 2-3 sample I/O pairs in table format
6. Simple constraints (e.g., 1 ≤ N ≤ 100)
7. `> [!NOTE] 老師的提示` with a hint (NOT the full solution)

**Challenge file format:** Each challenge SHALL have a corresponding `docs/challenge/<slug>.md` file with YAML frontmatter containing: `layout: challenge`, `id` (sequential integer), `title`, `difficulty` (easy/medium/hard), `tags`, `algorithm`, `testcase_count`, `params` with type/min/max, `generator` (Python code), `starter_code`, `chapter: ch2`, `description`.

**Topic distribution:**
- Example 1 (例題一): 星星直角三角形 — nested for loop producing a right triangle pattern
- Example 2 (例題二): 九九乘法表 — nested for loop with formatted multiplication table output
- Practice problems SHALL cover: rectangle pattern, inverted triangle, isosceles triangle, number pyramid, diamond pattern, pair counting (find all pairs (i,j) satisfying a condition), and optionally: nested loop with accumulation

#### Scenario: Section contains 2 example problems with full solutions

- **WHEN** section 2-4 is parsed
- **THEN** exactly 2 「Judge 解題實戰」subsections SHALL be found, each containing IPO analysis, complete solution code, line-by-line walkthrough, and common errors

#### Scenario: Section contains 6-8 practice problems

- **WHEN** the 「自己動手試試」section of 2-4 is parsed
- **THEN** 6 to 8 practice problems SHALL be found, each with a ChallengeLink component, explicit input/output format, and sample I/O

#### Scenario: All challenge files exist with valid frontmatter

- **WHEN** each ChallengeLink slug in section 2-4 is resolved
- **THEN** a corresponding `docs/challenge/<slug>.md` file SHALL exist with valid YAML frontmatter containing all required fields

#### Scenario: Practice problems use APCS beginner transition format

- **WHEN** a practice problem in section 2-4 is read
- **THEN** it SHALL contain separate 「輸入格式」and「輸出格式」headings, at least 2 sample I/O pairs, and a constraint statement with value ranges

#### Scenario: Each knowledge point has dedicated example and practice problems

- **WHEN** challenges are grouped by knowledge point
- **THEN** Knowledge Point A SHALL have at least 1 example problem (例題) with full IPO walkthrough AND at least 2 practice problems (類題) with hints only
- **AND** Knowledge Point B SHALL have at least 1 example problem (例題) with full IPO walkthrough AND at least 2 practice problems (類題) with hints only


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-4 follows all 15 editorial rules

Section 2-4 SHALL comply with all 15 editorial rules defined in the phoenix-popular-science-article-style:

- P-1: Em-dashes only for dramatic effect; routine clauses use commas or colons
- T-1: No technical terms before their teaching point
- S-1: Every analogy preceded by a meta-cognitive bridge sentence
- S-2: After humor elements, next sentence includes explicit recovery connective
- S-3: H2 transitions have 2-4 sentences (summary + gap + motivation); H3 transitions have 1-2 sentences
- C-1: Every code block preceded by conversational lead-in
- E-1: Common beginner errors warned at point of introduction
- M-1: Implicit concepts shown with step-by-step trace tables
- W-1: Code and line-by-line walkthroughs match exactly
- T-2: No TBD markers
- F-1: Image placeholders use dual-line format
- V-1: VitePress containers use `> [!TYPE]` syntax
- T-3: No empty UI elements
- K-1: Kaomoji density (1 per 30 prose lines min, 1 per 10 lines max; same kaomoji ≤2 per file, ≤3 per chapter; ≥2 emotion categories per file)

Additionally:
- At least 2 different reader dialogue voice types (A-E) per section
- Self-deprecation moment in each H2 section
- All content in Traditional Chinese (Taiwan usage); first technical term occurrence includes English

#### Scenario: P-1 compliance — no routine em-dashes

- **WHEN** section 2-4 is scanned for `——`
- **THEN** every occurrence SHALL be in a dramatic/humorous context (hook, punchline), not in routine explanatory clauses

#### Scenario: K-1 compliance — kaomoji density and variety

- **WHEN** kaomoji elements in section 2-4 are counted per 30-line prose window
- **THEN** at least 1 element SHALL be present in every 30-line window, and no 10-line window SHALL contain more than 1 element
- **AND** the same kaomoji SHALL appear at most 2 times in the file
- **AND** at least 2 different emotion categories SHALL be represented

#### Scenario: C-1 compliance — no heading-to-code jumps

- **WHEN** section 2-4 is scanned for fenced code blocks
- **THEN** every code block SHALL be preceded by at least one sentence of conversational prose (not just a heading)

<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->
---
### Requirement: Section 2-4 introduces escape character `\t` and f-string before first use

Section `docs/tutor/py/ch2/2-4.md` SHALL contain a NOTE block (or two adjacent NOTE blocks) that explains the `\t` escape character and the `f"..."` f-string syntax BEFORE the first code block in the section that uses either feature.

The escape-character explanation SHALL:
1. State that `\t` inside a string literal represents the **Tab** character (製表符).
2. State that `\t` advances the cursor to the next tab stop, which is the standard mechanism for column alignment in console output.
3. Mention briefly that strings can contain other backslash-prefixed special characters (called 跳脫字元 / escape characters), with `\n` (newline) named as an example, so the learner has a category label rather than thinking `\t` is a one-off symbol.

The f-string explanation SHALL:
1. State that an `f` prefix on a string literal (e.g., `f"Hello, {name}"`) enables embedded expressions inside `{ ... }` braces.
2. Explain the format-spec form `f"{value:N}"` where `N` is a positive integer that pads the value to at least `N` characters wide (right-aligned by default).
3. Note that f-string was previewed in section 1-2 as "後面才會學" and is now being formally introduced.

The NOTE blocks SHALL be positioned in document order before the first occurrence of `\t` AND before the first occurrence of `f"..."` in section 2-4.

#### Scenario: Escape character note appears before first \t usage

- **WHEN** section 2-4 is parsed in document order
- **THEN** a NOTE block explaining `\t` SHALL appear before the first code block containing the literal `"\t"` or `'\t'`

#### Scenario: F-string note appears before first f"..." usage

- **WHEN** section 2-4 is parsed in document order
- **THEN** a NOTE block explaining f-string syntax (including the `:N` format spec) SHALL appear before the first code block containing an `f"..."` literal

#### Scenario: F-string note covers width format spec

- **WHEN** the f-string NOTE block is reviewed
- **THEN** it SHALL contain at least one example showing `f"{value:N}"` where `N` is a positive integer, with prose explaining that the value is padded to at least `N` characters wide and is right-aligned by default

#### Scenario: Escape character note labels the category

- **WHEN** the `\t` NOTE block is reviewed
- **THEN** it SHALL contain the term 「跳脫字元」 (escape character) and SHALL mention at least one other escape character (e.g., `\n`) as a category example

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-4.md
-->

---
### Requirement: Section 2-4 hints SHALL NOT use unintroduced advanced syntax

The "老師的提示" NOTE blocks attached to practice problems in section `docs/tutor/py/ch2/2-4.md` SHALL NOT introduce or rely on Python syntax that has not yet been formally taught in any preceding section (Ch1 1-1 through Ch2 2-4 inclusive). The following advanced features SHALL NOT appear in 2-4 hints, regardless of brevity:

- Sequence unpacking with `*` in a function call (e.g., `print(*range(1, i+1))` or `print(*sequence)`).
- List, dict, tuple, set literal syntax (e.g., `[1, 2, 3]`, `(1, 2)`, `{1, 2}`).
- List comprehension or generator expression syntax (e.g., `[x for x in ...]`, `(x for x in ...)`).
- Function definition (`def`), lambda (`lambda`), or any callable construction.
- Slicing syntax (`a[i:j]`, `a[::-1]`, etc.).
- The walrus operator `:=`.

If a hint genuinely needs an alternative approach beyond the doubly-nested loop and the string operators introduced in 1-2, the hint SHALL describe it in prose only (e.g., "another approach uses string repetition `"*" * n`") without showing unintroduced syntax.

#### Scenario: No unpacking in 2-4 hints

- **WHEN** the "老師的提示" NOTE blocks in section 2-4 are scanned for the pattern `print(*` or `*range(` or `*list(` or any leading-`*` argument-unpacking usage
- **THEN** zero matches SHALL be found

#### Scenario: No list/comprehension/lambda/slicing in 2-4 hints

- **WHEN** the "老師的提示" NOTE blocks in section 2-4 are scanned for syntax fragments matching list literal `[...]`, list comprehension `[x for ...]`, generator `(x for ...)`, `def `, `lambda `, slicing `[...:...]`, or `:=`
- **THEN** zero matches SHALL be found, except for syntax explicitly listed as taught in or before Ch2 2-4 (e.g., the `[!NOTE]` markdown container which is unrelated to Python list syntax)

#### Scenario: String repetition hint is allowed because 1-2 introduces it

- **WHEN** a "老師的提示" NOTE block in section 2-4 references string repetition such as `"*" * n` or `" " * (n - i)`
- **THEN** the hint SHALL be accepted (this syntax is formally taught in Ch1 1-2 by the `python-ch1-content` capability)

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/2-4.md
-->
