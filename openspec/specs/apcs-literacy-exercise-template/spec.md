# apcs-literacy-exercise-template Specification

## Purpose

Defines the structural template and content requirements for APCS literacy-style practice exercises used in sections 1-3 through 2-4. This spec is referenced by `python-ch2-enhanced-exercises` and any other spec that adds or rewrites practice exercises in those sections.

## Requirements

### Requirement: APCS literacy exercise format template structure

Every practice exercise in sections 1-3 through 2-4 SHALL follow this structure, in order. A "practice exercise" is defined as any exercise under a 「自己動手試試」heading, a 「類題」heading, or a standalone full-description exercise block — but NOT a 「Judge 解題實戰」teaching worked-example (which has its own IPO analysis, step-by-step code walkthrough, and Trace Table). The excluded Judge 解題實戰 slugs are: `leap-year`, `number-sum`, `countdown`, `collatz-steps`, `first-divisor`, `skip-multiples`, `nested-triangle`, `multiplication-table`.

1. H3 heading with problem title (`### [題目名稱]`)
2. `<ChallengeLink slug="[slug]" />` component
3. **問題情境** section (mandatory)
4. **🔍 思考引導** section with at least 1 scaffold element (mandatory)
5. **輸入格式** section with per-line specification and value constraints (mandatory)
6. **輸出格式** section with precise output description (mandatory)
7. At least 2 sample I/O pairs as Markdown tables (mandatory)
8. **範例說明** section with step-by-step trace of the most instructive example (mandatory)
9. `> [!NOTE] 老師的提示` callout with 1-3 strategic hints (mandatory)

Each exercise SHALL be separated by a horizontal rule (`---`).

#### Scenario: Complete exercise has all required sections

- **WHEN** a practice exercise in sections 1-3 through 2-4 is parsed
- **THEN** it SHALL contain all 9 structural elements listed above in the specified order

#### Scenario: Exercise sections appear in correct order

- **WHEN** the positions of 問題情境, 思考引導, 輸入格式, 輸出格式, 範例, 範例說明, and 老師的提示 are compared
- **THEN** they SHALL appear in the order specified above, with no sections out of sequence


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Problem narrative uses APCS literacy style

The **問題情境** section of each exercise SHALL:

1. Use a named character (e.g., 小明, 阿華, 小芳) with an identifiable role or situation
2. Describe a real-world scenario that naturally leads to the computational problem
3. Contain between 150 and 300 Chinese characters (excluding punctuation)
4. NOT repeat the same named character across different exercises within the same `.md` file (e.g., all 10 exercises in `1-3.md` SHALL have 10 unique character names)

The scenario categories, in priority order, SHALL be:
1. Student daily life (campus, clubs, exams, part-time work)
2. Math/science class connections (linking to high school curriculum)
3. Game/entertainment scenarios (following APCS convention)

#### Scenario: Narrative has named character

- **WHEN** the 問題情境 text of any exercise is read
- **THEN** it SHALL contain at least one named character (a Chinese name like 小明 or 阿華)

#### Scenario: Narrative meets length requirement

- **WHEN** the Chinese character count of 問題情境 is measured (excluding punctuation and whitespace)
- **THEN** the count SHALL be between 150 and 300

#### Scenario: No duplicate characters within a section

- **WHEN** all named characters in exercises within a single `.md` file are collected
- **THEN** no character name SHALL appear in more than one exercise's 問題情境


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Scaffold section provides at least one scaffold type

The **🔍 思考引導** section SHALL contain at least 1 and at most 3 scaffold elements. Each scaffold element SHALL be one of the following three types:

**Type A — Math Expression (數學表達)**:
- SHALL be wrapped in a blockquote starting with `> 💭 **如果用數學來表達...**`
- SHALL contain at least one LaTeX formula (using `$$...$$` or `$...$` syntax)
- SHALL explain what each variable represents
- SHALL end with a guiding question about translating the formula to Python
- SHALL NOT contain any Python code (keywords, function calls, operators, or code snippets). Note: this restriction applies ONLY to the Type A scaffold element itself; the `老師的提示` section at the end of the exercise MAY contain Python operators and short code fragments as strategic hints.

**Type B — Partial Flowchart (部分流程圖)**:
- SHALL be wrapped in a blockquote starting with `> 🔀 **試著補完這張流程圖...**`
- SHALL contain a Mermaid `flowchart TD` code block
- SHALL have at least 1 and at most 3 nodes containing `???` as placeholder text
- SHALL have no more than 8 total nodes (including placeholder nodes)
- The `???` placeholders SHALL be placed on core logic steps, NOT on boilerplate steps. Core logic steps: any nodes that perform problem-specific computation or decisions (conditions, math operations, counter logic, intermediate variable updates). Boilerplate steps (only these two): reading input from stdin, printing final output to stdout. All other steps (initialization, counter increment, loop variable update) are core logic and eligible for `???` masking.

**Type C — Step Decomposition (拆解思路)**:
- SHALL be wrapped in a blockquote starting with `> 🧩 **把大問題拆成小問題...**`
- SHALL contain a numbered list of 3 to 5 steps
- SHALL have the last 1 to 2 steps partially or fully hidden with `???`
- Each visible step SHALL be described in one sentence without Python code

#### Scenario: Exercise uses Type A scaffold for formula-based problem

- **WHEN** an exercise involves a mathematical formula or calculation rule (e.g., BMI, discriminant, taxi fare)
- **THEN** its 思考引導 section SHALL contain a Type A (Math Expression) scaffold element

#### Scenario: Exercise uses Type B scaffold for control flow problem

- **WHEN** an exercise primarily tests conditional branching or loop control (e.g., leap year, password validation, guessing game)
- **THEN** its 思考引導 section SHALL contain a Type B (Partial Flowchart) scaffold element

#### Scenario: Exercise uses Type C scaffold for multi-stage problem

- **WHEN** an exercise requires multi-stage processing or can be decomposed into independent sub-problems (e.g., date validation, change-making, nested loop patterns)
- **THEN** its 思考引導 section SHALL contain a Type C (Step Decomposition) scaffold element

#### Scenario: Flowchart does not exceed node limit

- **WHEN** the Mermaid flowchart in a Type B scaffold is parsed
- **THEN** the total number of nodes SHALL NOT exceed 8

#### Scenario: Flowchart hides core logic, not boilerplate

- **WHEN** the `???` placeholders in a Type B scaffold are examined
- **THEN** each `???` SHALL replace a condition check, computation step, or decision outcome — NOT an input read or output print step

#### Scenario: Math scaffold contains no Python code

- **WHEN** the content of a Type A scaffold is examined
- **THEN** it SHALL NOT contain any Python keywords, function calls, or code snippets


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Scaffold type selection follows section-topic mapping

The primary scaffold type for exercises SHALL be selected based on the section's teaching topic:

| Section | Teaching Topic | Primary Scaffold | Rationale |
|---------|---------------|-------------------|-----------|
| 1-3 | if-elif-else | Type B (Flowchart) | Conditional branching visualized as decision trees |
| 1-4 | Module 1 summary | Type C (Decomposition) | Comprehensive problems need step decomposition |
| 2-1 | for loop | Type A (Math) | Sequences and accumulation have natural formulas |
| 2-2 | while loop | Type B (Flowchart) | Indeterminate loops best shown as flow diagrams |
| 2-3 | break/continue | Type B (Flowchart) | Loop control flow requires visual representation |
| 2-4 | Nested loops | Type C (Decomposition) | Complex patterns decompose into outer/inner problems |

Exercises MAY use additional secondary scaffolds when the problem naturally spans multiple categories (e.g., a for-loop problem with a formula AND a multi-stage structure).

#### Scenario: Section 1-3 exercises primarily use flowcharts

- **WHEN** the scaffold types used in section 1-3 exercises are counted
- **THEN** at least 60% of exercises SHALL include a Type B (Flowchart) scaffold

#### Scenario: Section 2-1 exercises primarily use math expressions

- **WHEN** the scaffold types used in section 2-1 exercises are counted
- **THEN** at least 50% of exercises SHALL include a Type A (Math Expression) scaffold

#### Scenario: Section 2-4 exercises primarily use step decomposition

- **WHEN** the scaffold types used in section 2-4 exercises are counted
- **THEN** at least 60% of exercises SHALL include a Type C (Step Decomposition) scaffold


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Example explanation traces computation step by step

The **範例說明** section SHALL:

1. Reference the specific example being traced (e.g., "以範例一為例"). The trace SHALL use the example that best demonstrates the computation process. If the first example is trivially simple (1 computation step or fewer), the trace SHALL use the second example instead.
2. State the input values explicitly
3. Number each computation step (第一步, 第二步, etc.)
4. Show concrete numeric values at each step (not abstract variable names)
5. Conclude with an explicit statement of the final answer

The explanation SHALL NOT contain Python code or implementation details.

#### Scenario: Example explanation shows numbered steps

- **WHEN** the 範例說明 section is parsed
- **THEN** it SHALL contain at least 2 numbered steps with concrete numeric computations

#### Scenario: Example explanation concludes with answer

- **WHEN** the last sentence of 範例說明 is read
- **THEN** it SHALL state the final output value that matches the example's output column


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Input format uses APCS-standard specification

The **輸入格式** section SHALL:

1. Specify each input line separately (e.g., "第一行：正整數 N")
2. Include data type for each value (整數, 正整數, 非負整數, etc.)
3. Include value range constraints using inequality notation (e.g., 1 ≤ N ≤ 100)
4. For problems with multiple values on one line, specify the separator (always single space)

#### Scenario: Input format has per-line specification

- **WHEN** the 輸入格式 section is parsed
- **THEN** each distinct input SHALL be described on its own line with type and constraint

#### Scenario: Input constraints use inequality notation

- **WHEN** the 輸入格式 section is read
- **THEN** every numeric input SHALL have an explicit range constraint using ≤ notation


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Teacher hint provides strategy without solution

The `> [!NOTE] 老師的提示` section SHALL:

1. Contain 1 to 3 sentences
2. Identify the key concept, algorithm approach, or common pitfall
3. NOT contain complete Python code or pseudocode that constitutes a full solution
4. MAY reference specific concepts from the teaching content (e.g., "還記得 Trace Table 嗎？")

#### Scenario: Hint does not reveal complete solution

- **WHEN** the 老師的提示 content is examined
- **THEN** it SHALL NOT contain a complete algorithm implementation, loop body, or full conditional chain that solves the problem

#### Scenario: Hint identifies a specific strategy

- **WHEN** the 老師的提示 content is read
- **THEN** it SHALL mention at least one of: a key concept name, an algorithm approach, a common mistake to avoid, or a reference to prior teaching material


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Tier-based difficulty labels are removed

Section 1-3's existing tier system (★☆☆ through ★★★★ with Tier 1-4 headings) SHALL be replaced by the APCS literacy exercise format. Exercises SHALL be ordered by ascending difficulty within each section, but SHALL NOT carry explicit difficulty tier markers or star ratings.

#### Scenario: No tier markers in reformatted section 1-3

- **WHEN** the reformatted 1-3 content is searched for tier markers
- **THEN** it SHALL NOT contain any of: ★, ☆, "Tier 1", "Tier 2", "Tier 3", "Tier 4", or H3/H4 headings with tier labels

#### Scenario: Exercises are ordered by ascending difficulty within each subsection

- **WHEN** the exercises within a single subsection grouping (e.g., one `## 自己動手試試！` block) are listed in document order
- **THEN** simpler exercises (fewer scaffold types, simpler input, single concept) SHALL appear before complex exercises (multiple scaffolds, multi-concept, compound logic). Exercises need NOT be reordered across different subsections within the same file.


<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->

---
### Requirement: Existing full-description exercises are augmented not rewritten from scratch

When an exercise already has 題目說明, 輸入格式, 輸出格式, 範例, and 老師的提示 sections (the "full-description" format used in 2-1 through 2-4), the implementer SHALL preserve the existing I/O specification and example data, and ADD the missing sections (問題情境 narrative, 🔍 思考引導 scaffold, 範例說明 trace). The existing 題目說明 content SHALL be incorporated into the new 問題情境 section, expanded to 150-300 characters with a named character and real-world scenario. Existing 老師的提示 content SHALL be reviewed and retained if it meets the new spec, or updated if it reveals a complete solution.

#### Scenario: Full-description exercise preserves existing I/O data

- **WHEN** an exercise that already has 輸入格式, 輸出格式, and sample I/O tables is reformatted
- **THEN** the existing I/O specification and example data SHALL be preserved (values, constraints, and table contents unchanged), and new sections (問題情境, 思考引導, 範例說明) SHALL be added around them

#### Scenario: Full-description exercise expands existing description

- **WHEN** an exercise that already has a 題目說明 is reformatted
- **THEN** the 題目說明 content SHALL be incorporated into the new 問題情境 section with expanded narrative (150-300 characters), NOT deleted and rewritten from scratch

<!-- @trace
source: apcs-literacy-exercise-format
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-3.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch2/2-2.md
  - refs/apcs/04_APCS-程式實作高級題本範例.pdf
  - refs/apcs/02_APCS-程式實作中級題本範例.pdf
  - refs/apcs/01_APCS-程式實作初級題本範例.pdf
  - refs/apcs/03_APCS-程式實作中高級題本範例.pdf
  - refs/apcs/程式識讀_題目範例_Python題本_0915.pdf
  - docs/tutor/py/ch2/2-1.md
-->