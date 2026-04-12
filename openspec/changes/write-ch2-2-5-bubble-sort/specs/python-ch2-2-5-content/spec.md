## ADDED Requirements

### Requirement: Section 2-5 file exists with correct frontmatter

The system SHALL provide a tutorial section file `docs/tutor/py/ch2/2-5.md` for Chapter 2, Section 2-5 (串列進階與氣泡排序). The file MUST have valid frontmatter with `layout: doc`, `chapter: 2`, `section: "2-5"`, `title`, `description`, and `createdTime` in ISO 8601 with `+08:00` timezone offset.

#### Scenario: Section file has valid frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-5.md` is parsed successfully with all required frontmatter fields: `layout`, `chapter`, `section`, `title`, `description`, `createdTime`

#### Scenario: Section appears in Chapter 2 sidebar

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar SHALL display a link to section 2-5

---

### Requirement: Section 2-5 teaches three knowledge points in prerequisite order

The tutorial section SHALL teach the three knowledge points in strict dependency order: (1) variable swap (`a, b = b, a`), (2) nested loops (雙重迴圈), (3) bubble sort algorithm (氣泡排序法). Variable swap and nested loops MUST be fully introduced before bubble sort is presented, as bubble sort depends on both concepts.

#### Scenario: Knowledge points appear in correct order

- **WHEN** the section content is read from top to bottom
- **THEN** variable swap content SHALL precede nested loop content, which SHALL precede bubble sort content

#### Scenario: Bubble sort section references swap and nested loops

- **WHEN** the bubble sort section is reviewed
- **THEN** it SHALL explicitly reference both the variable swap technique and the nested loop structure taught earlier in the same section

---

### Requirement: Section 2-5 respects T-1 terminology boundary constraints

The tutorial section SHALL NOT use `dict`, `tuple`, or list comprehension syntax anywhere. The following constructs are available and SHALL be used as needed: `for`, `while`, `range()`, `break`, `continue`, `list`, `len()`, and integer/string/float variables. No built-in `.sort()` or `sorted()` SHALL appear anywhere in the tutorial content or code examples.

#### Scenario: Forbidden constructs are absent

- **WHEN** the section file is scanned for forbidden syntax
- **THEN** zero occurrences of `dict`, `tuple`, list comprehension (`[... for ... in ...]`), `.sort()`, or `sorted()` SHALL be found

#### Scenario: Available constructs are used correctly

- **WHEN** the section introduces bubble sort
- **THEN** the implementation SHALL use only `for`, `while`, `range()`, `list` indexing, and the `a, b = b, a` swap idiom

---

### Requirement: Variable swap knowledge point has one example and two practice challenges

The section SHALL provide one example challenge (Judge id: 32) that demonstrates the variable swap idiom `a, b = b, a`, and link to two practice challenges (ids: 33, 34) that require students to apply variable swapping independently. All three challenges MUST be linked via `<ChallengeLink>` components.

#### Scenario: Variable swap example challenge is linked from section

- **WHEN** a user reads the variable swap subsection of 2-5
- **THEN** a `<ChallengeLink>` component pointing to the example challenge (id: 32) SHALL be present

#### Scenario: Variable swap practice challenges are linked from section

- **WHEN** a user reads the practice area for variable swap
- **THEN** two `<ChallengeLink>` components pointing to practice challenges (ids: 33, 34) SHALL be present with brief hints but no step-by-step walkthrough

---

### Requirement: Nested loop knowledge point has one example and two practice challenges

The section SHALL provide one example challenge (id: 35) that demonstrates nested `for` loops, and link to two practice challenges (ids: 36, 37) for independent practice. All three challenges MUST be linked via `<ChallengeLink>` components. The nested loop example SHALL show iteration counts (outer × inner) explicitly to build intuition before bubble sort.

#### Scenario: Nested loop example challenge is linked from section

- **WHEN** a user reads the nested loop subsection of 2-5
- **THEN** a `<ChallengeLink>` component pointing to the nested loop example (id: 35) SHALL be present

#### Scenario: Nested loop practice challenges are linked from section

- **WHEN** a user reads the practice area for nested loops
- **THEN** two `<ChallengeLink>` components pointing to practice challenges (ids: 36, 37) SHALL be present

---

### Requirement: Bubble sort knowledge point has one example and two practice challenges

The section SHALL provide one example challenge (id: 38, 頒獎典禮) that demonstrates descending-order bubble sort, and link to two practice challenges (ids: 39, 40) for independent practice. All three challenges MUST be linked via `<ChallengeLink>` components.

#### Scenario: Bubble sort example challenge is linked from section

- **WHEN** a user reads the bubble sort subsection of 2-5
- **THEN** a `<ChallengeLink>` component pointing to the 頒獎典禮 example (id: 38) SHALL be present

#### Scenario: Bubble sort practice challenges are linked from section

- **WHEN** a user reads the bubble sort practice area
- **THEN** two `<ChallengeLink>` components pointing to practice challenges (ids: 39, 40) SHALL be present

---

### Requirement: Bubble sort section contains step-by-step swap trace (M-1)

The bubble sort explanation SHALL include a concrete step-by-step trace showing how the algorithm swaps adjacent elements pass by pass on a small example array (3–5 elements). Each step of the trace MUST show the array state before and after each swap, and label which pass (第幾輪) is being executed. This satisfies the mental model rule M-1 from Chapter 1 editorial guidelines.

#### Scenario: Bubble sort trace shows pass-by-pass array states

- **WHEN** the bubble sort explanation is reviewed
- **THEN** it SHALL contain a numbered trace showing: array before pass N, which adjacent pair was compared, whether a swap occurred, and array after pass N — for at least 2 complete passes on a concrete example

#### Scenario: Trace uses the same swap idiom taught earlier

- **WHEN** the bubble sort trace explains a swap step
- **THEN** it SHALL reference the `a, b = b, a` idiom taught in the variable swap knowledge point

---

### Requirement: Nine challenge files exist with correct structure (IDs 32–40)

The system SHALL provide nine challenge files in `docs/challenge/` with IDs 32 through 40. Each challenge file MUST have `layout: challenge`, a valid `id`, `title`, `difficulty`, `tags`, `algorithm` slug, `testcase_count` of at least 5, `params` with typed constraints, a correct `generator` script, and `starter_code` with a hint comment. No challenge generator SHALL use `.sort()` or `sorted()` in its solution (the generator produces reference output; it MUST compute results using bubble sort or equivalent explicit swap logic).

#### Scenario: All nine challenge files exist

- **WHEN** the docs/challenge/ directory is scanned
- **THEN** exactly nine new files corresponding to IDs 32–40 SHALL be present

#### Scenario: Challenge generators produce correct output

- **WHEN** a challenge generator is executed with valid test input matching the params specification
- **THEN** the generator SHALL produce the correct expected output for that input

#### Scenario: Challenge files have required frontmatter fields

- **WHEN** a challenge file for IDs 32–40 is parsed
- **THEN** it SHALL contain: `layout: challenge`, `id`, `title`, `difficulty`, `tags`, `algorithm`, `testcase_count`, `params`, `generator`, `starter_code`

---

### Requirement: 頒獎典禮 challenge (id: 38) uses descending bubble sort with list input

The 頒獎典禮 example challenge (id: 38) SHALL read N student scores from input and output them sorted in descending order (highest to lowest). The generator MUST implement this using explicit bubble sort logic (nested loops + swap). The `params` SHALL include `n` (number of students, min 3, max 8) and `scores` (list of integers, each 0–100). The challenge description MUST explicitly state that built-in `.sort()` is forbidden (嚴禁使用內建 `.sort()`).

#### Scenario: 頒獎典禮 sorts scores descending

- **WHEN** the generator receives n=3 and scores=[72, 95, 84]
- **THEN** the output SHALL be the three scores in descending order: 95, 84, 72 (one per line)

#### Scenario: 頒獎典禮 challenge description forbids .sort()

- **WHEN** the challenge file for id: 38 is reviewed
- **THEN** the description body SHALL contain a notice that `.sort()` and `sorted()` are forbidden

---

### Requirement: Section 2-5 follows punctuation style rule P-1

Each tutorial section SHALL use commas (，) or colons (：) for routine clause separation. The em-dash (`——`) SHALL be reserved exclusively for dramatic emphasis in hooks and humor. Em-dashes SHALL NOT be used for explanatory clauses (use colons) or continuation clauses (use commas).

#### Scenario: Routine clause uses comma or colon instead of em-dash

- **WHEN** the section contains a clause that explains a preceding term
- **THEN** the em-dash SHALL be replaced with a colon

#### Scenario: Dramatic em-dash is preserved

- **WHEN** the section contains an em-dash used for comedic timing or narrative surprise
- **THEN** the em-dash SHALL be preserved

---

### Requirement: Section 2-5 follows terminology boundary rule T-1 (no forward references)

Tutorial section 2-5 SHALL NOT use any technical term before its designated teaching point within the section itself. Concepts introduced later in the same section (e.g., bubble sort) SHALL NOT be mentioned in the variable swap or nested loop subsections unless using plain-language descriptions.

#### Scenario: Variable swap subsection does not mention bubble sort by name

- **WHEN** the variable swap subsection is reviewed
- **THEN** the term "氣泡排序" SHALL NOT appear before the bubble sort subsection

---

### Requirement: Section 2-5 follows analogy bridge rule S-1

Every analogy or metaphor in the tutorial section SHALL be preceded by a meta-cognitive bridge — one sentence explaining WHY the comparison is being made, before the comparison itself.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** the section introduces an analogy (e.g., comparing bubble sort to sorting playing cards)
- **THEN** the preceding sentence SHALL state the purpose of the analogy

---

### Requirement: Section 2-5 follows post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions), the next sentence SHALL include an explicit callback connector that resumes the narrative thread.

#### Scenario: Joke followed by connector before resuming exposition

- **WHEN** the section contains a parenthetical joke within a continuous prose block
- **THEN** the immediately following sentence SHALL contain an explicit connector linking back to the expository point preceding the joke

---

### Requirement: Section 2-5 follows section transition rule S-3

Transitions between the three major knowledge-point H2 sections SHALL contain 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap or limitation, and (c) motivate the next knowledge point.

#### Scenario: Transition from variable swap to nested loops

- **WHEN** the variable swap H2 section ends and the nested loop H2 section begins
- **THEN** a transition block SHALL summarize swap, identify that single-loop iteration is insufficient for sorting, and motivate nested loops

#### Scenario: Transition from nested loops to bubble sort

- **WHEN** the nested loop H2 section ends and the bubble sort H2 section begins
- **THEN** a transition block SHALL summarize nested loops, identify the need for comparison-based ordering, and motivate the bubble sort algorithm

---

### Requirement: Section 2-5 code blocks follow conversational lead-in rule C-1

Every fenced code block in the tutorial section SHALL be preceded by at least one sentence of conversational setup establishing context. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** the section contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading (H2/H3) and the opening code fence

---

### Requirement: Section 2-5 follows error prevention rule E-1

Common beginner mistakes for each knowledge point SHALL be addressed immediately at the point of introduction: (a) for variable swap: the naive temporary variable approach vs. the Pythonic `a, b = b, a`; (b) for nested loops: off-by-one errors in `range()`; (c) for bubble sort: forgetting to reduce the inner loop range by the pass number.

#### Scenario: Swap pitfall is warned at introduction

- **WHEN** the variable swap syntax is first introduced
- **THEN** the section SHALL mention the naive temporary-variable approach and explain why `a, b = b, a` is more Pythonic

#### Scenario: Bubble sort inner-range pitfall is warned

- **WHEN** bubble sort loop structure is introduced
- **THEN** the section SHALL note the optimization of reducing the inner loop bound by the pass count

---

### Requirement: Section 2-5 follows mental model trace rule M-1

When a code example implicitly demonstrates a fundamental algorithmic concept, the section SHALL make the concept explicit with a step-by-step trace. For bubble sort this means a full pass-by-pass trace on a small array showing element comparisons and swaps.

#### Scenario: Bubble sort trace shows evaluation order

- **WHEN** the bubble sort code example is presented
- **THEN** the accompanying explanation SHALL include a numbered trace showing each comparison and swap per pass (e.g., "Pass 1, Step 1: compare scores[0]=72 and scores[1]=95, no swap needed...")

---

### Requirement: Section 2-5 contains image placeholders with dual-line format (F-1)

Every image placeholder in `docs/tutor/py/ch2/2-5.md` SHALL use the dual-line format: (1) an image link line `![📷 **圖 N**：description（AI 製圖）](/assets/tutor/py/ch2/figNN.png)` and (2) a caption line `> 📷 **圖 N**：description（AI 製圖）`. Single-line caption-only format SHALL NOT be used.

#### Scenario: Image placeholder has both link and caption

- **WHEN** the section is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding image link line

---

### Requirement: Section 2-5 ends with Image Specification Appendix

The section file SHALL end with an `## 圖片規格附錄 (Image Specification Appendix)` section containing fully expanded Nano Banana Pro prompt strings for each image placeholder. Each prompt MUST follow the American stick figure comic style with dialogue-driven panels, Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Appendix contains prompts for all images

- **WHEN** the Image Specification Appendix is reviewed
- **THEN** it SHALL contain one entry per image placeholder used in the section, with a complete prompt string

---

### Requirement: Section 2-5 has visual rhythm — at least one visual per H2 section (visual rhythm rule)

Each H2-level section in `docs/tutor/py/ch2/2-5.md` SHALL contain at least one visual element (image placeholder or diagram-style code block). No more than five consecutive paragraphs of pure text SHALL exist without a visual element.

#### Scenario: Each H2 section has at least one visual

- **WHEN** the section is reviewed per H2 block
- **THEN** each H2 block SHALL contain at least one image placeholder

---

### Requirement: Section 2-5 follows VitePress custom container syntax rule V-1

All VitePress custom container callouts SHALL use the correct syntax `> [!TYPE]` where TYPE is one of `NOTE`, `TIP`, `WARNING`, `DANGER`, `DETAILS`. The exclamation mark is mandatory.

#### Scenario: Custom container uses correct syntax

- **WHEN** the section contains a blockquote-based custom container
- **THEN** the opening line SHALL match the pattern `> [!TYPE]`

---

### Requirement: Section 2-5 contains no residual TBD markers (T-2)

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from the section file.

#### Scenario: No TBD markers in 2-5.md

- **WHEN** `docs/tutor/py/ch2/2-5.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found

---

### Requirement: Section 2-5 contains no empty UI elements (T-3)

Published tutorial sections SHALL NOT contain custom container blocks where the title line exists but the body content is empty or contains only whitespace.

#### Scenario: Empty container is hidden

- **WHEN** a custom container has no substantive body content
- **THEN** the entire container block SHALL be wrapped in HTML comments

---

### Requirement: Section 2-5 follows emotional punctuation density rule K-1

Within any contiguous block of 30 lines of prose (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element (kaomoji, parenthetical joke, or student dialogue interjection) SHALL be present. Within any contiguous block of 10 lines of prose, no more than one emotional punctuation element SHALL be present. The same kaomoji SHALL NOT appear more than twice within the section file. The section SHALL use kaomoji from at least two different emotional categories.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose is identified in the section
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present

#### Scenario: Kaomoji is not overused within the file

- **WHEN** the section file is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice in that file

#### Scenario: Kaomoji emotional variety is maintained

- **WHEN** the section file is scanned for kaomoji emotional categories
- **THEN** the file SHALL contain kaomoji from at least two different emotional categories
