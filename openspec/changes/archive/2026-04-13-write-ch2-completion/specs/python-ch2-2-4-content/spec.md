## ADDED Requirements

### Requirement: Section 2-4 file exists with correct frontmatter and structure

The file `docs/tutor/py/ch2/2-4.md` SHALL exist with frontmatter fields: `layout: doc`, `title` (display title for the nested loops section), `description` (one-line summary), `chapter: 2`, `section: "2-4"`, `createdTime` in ISO 8601 with `+08:00` timezone, and `challenge` referencing the slug of the primary example challenge.

The file SHALL include a `VISUAL-STYLE-PREFIX` HTML comment immediately after the frontmatter, using the same American stick figure comic style as Chapter 1 and sections 2-1 through 2-3.

#### Scenario: Section file has valid frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-4.md` SHALL be parsed successfully with all required frontmatter fields (`layout`, `title`, `description`, `chapter`, `section`, `createdTime`, `challenge`) present and non-empty

#### Scenario: Section file appears in sidebar

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar SHALL display a link to section 2-4

---

### Requirement: Section 2-4 covers nested loops as two knowledge points

Section 2-4 SHALL teach exactly two knowledge points:

- **Knowledge Point A**: 雙重 for 迴圈基礎 — How to place one `for` loop inside another, the execution order (outer loop controls rows, inner loop controls columns), indentation rules for nested blocks, and pattern printing (right triangle of `*`, rectangle of `*`, multiplication table `九九乘法表`).
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
