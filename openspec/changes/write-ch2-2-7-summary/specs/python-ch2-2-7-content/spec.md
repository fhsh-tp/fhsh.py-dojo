# python-ch2-2-7-content Specification

## Purpose

Defines the content requirements for `docs/tutor/py/ch2/2-7.md`, the Module 2 summary section. This section has no new knowledge points and no challenges. Its purpose is to consolidate all Module 2 concepts (sections 2-1 through 2-6), provide a self-check table for learner verification, and preview Module 3 topics.

## ADDED Requirements

### Requirement: Section 2-7 file exists with correct frontmatter

The system SHALL provide a tutorial section file at `docs/tutor/py/ch2/2-7.md` with the following frontmatter fields:
- `layout`: fixed value `doc`
- `title`: the display title for the Module 2 summary
- `description`: a one-line summary string
- `chapter`: integer value `2`
- `section`: string value `"2-7"`
- `createdTime`: ISO 8601 datetime string with UTC+8 offset

The `challenge` frontmatter field SHALL NOT be present, as this section has no associated challenge.

#### Scenario: Section file has correct frontmatter

- **WHEN** VitePress builds the site and parses `docs/tutor/py/ch2/2-7.md`
- **THEN** the file SHALL be parsed successfully with all required frontmatter fields (`layout`, `title`, `description`, `chapter: 2`, `section: "2-7"`, `createdTime`) present and non-empty, and SHALL NOT include a `challenge` field

#### Scenario: Section file appears in Chapter 2 navigation

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar SHALL display a link to section 2-7 as the final entry in the Chapter 2 section list

---

### Requirement: Section 2-7 contains a Module 2 knowledge map

The `docs/tutor/py/ch2/2-7.md` file MUST contain a knowledge map that covers all six content sections (2-1 through 2-6). The knowledge map SHALL be rendered as a text-based tree diagram (fenced code block using plain text indentation). The map SHALL include at minimum:
- 2-1 topics: `for` loops, `range()`, iteration pattern
- 2-2 topics: `while` loops, loop condition, infinite loop guard
- 2-3 topics: `break`, `continue`, early exit and skip patterns
- 2-4 topics: Lists (list literal, indexing, append, len), linear search algorithm
- 2-5 topics: Advanced list operations (slicing, sorting, nested lists), bubble sort algorithm
- 2-6 topics: Dictionaries (key-value pairs, dict literal, lookup), hash table concept

The knowledge map SHALL be preceded by an image placeholder (dual-line format per rule F-1) showing an AI-generated infographic version.

#### Scenario: Knowledge map text tree is present

- **WHEN** `docs/tutor/py/ch2/2-7.md` is reviewed
- **THEN** the file SHALL contain a fenced plain-text block with a tree diagram that lists all six sections (2-1 through 2-6) as branches with their key concepts as leaves

#### Scenario: Knowledge map image placeholder is present

- **WHEN** the knowledge map section is reviewed
- **THEN** an image placeholder in dual-line format SHALL precede the text tree diagram, referencing the planned image path at `/assets/tutor/py/ch2/`

---

### Requirement: Section 2-7 contains a self-check table

The `docs/tutor/py/ch2/2-7.md` file MUST contain a self-check table in Markdown table format. The table SHALL include at minimum 15 rows covering concrete skills from Module 2 (sections 2-1 through 2-6). Each row SHALL follow the format: `| # | 能力 | 你會了嗎？ |` with a checkbox `☐` in the third column.

Skills covered SHALL include (but are not limited to):
- Ability to write a `for` loop with `range()`
- Ability to write a `while` loop with a correct termination condition
- Ability to use `break` to exit a loop early
- Ability to use `continue` to skip an iteration
- Ability to create and index a list
- Ability to use `append()` and `len()` on a list
- Ability to implement linear search
- Ability to sort a list and understand bubble sort logic
- Ability to create and look up values in a dictionary
- Ability to explain what a hash table is conceptually

#### Scenario: Self-check table is present and complete

- **WHEN** `docs/tutor/py/ch2/2-7.md` is reviewed
- **THEN** the file SHALL contain a Markdown table with a header row `| # | 能力 | 你會了嗎？ |` and at least 15 data rows, each with a `☐` checkbox in the third column

#### Scenario: Self-check table covers all six sections

- **WHEN** the self-check table rows are categorized by their source section
- **THEN** skills from each of the six sections (2-1, 2-2, 2-3, 2-4, 2-5, 2-6) SHALL be represented by at least one row

---

### Requirement: Section 2-7 contains a Module 3 preview

The `docs/tutor/py/ch2/2-7.md` file MUST contain a Module 3 preview section. The preview SHALL introduce the following Module 3 topics with brief plain-language descriptions:
- Functions (函式): defining reusable code blocks
- Binary search (二元搜尋): efficient search in sorted data
- Recursion (遞迴): functions that call themselves

The preview SHALL motivate learners by connecting Module 2 skills to Module 3 concepts (e.g., lists learned in Module 2 enable binary search in Module 3). The preview SHALL end with an image placeholder (dual-line format per rule F-1) showing an AI-generated comic hook for Module 3.

#### Scenario: Module 3 preview section is present

- **WHEN** `docs/tutor/py/ch2/2-7.md` is reviewed
- **THEN** the file SHALL contain a section introducing at least three Module 3 topics: functions, binary search, and recursion

#### Scenario: Module 3 preview image placeholder is present

- **WHEN** the Module 3 preview section is reviewed
- **THEN** an image placeholder in dual-line format SHALL be present, referencing the planned image path at `/assets/tutor/py/ch2/`

---

### Requirement: Section 2-7 contains an Image Specification Appendix

The `docs/tutor/py/ch2/2-7.md` file MUST end with an `## Image Specification Appendix` section. For each image placeholder used in the section, the appendix SHALL include:
- Image number and type label (e.g., `### 圖 N`)
- `- **類型**`: image category (e.g., 四格漫畫（Recap）, 資訊圖表)
- `- **意圖**`: one-sentence description of the image's pedagogical intent
- `- **完整 Prompt**`: the full AI image generation prompt, beginning with the chapter's visual style prefix
- `- **備註**`: optional notes on composition or emphasis

All image prompts SHALL use the American stick figure comic strip visual style prefix (consistent with Chapter 1 and Chapter 2 sections). Speech bubble text SHALL be in Traditional Chinese (Taiwan usage), with technical terms in English.

#### Scenario: Appendix exists and covers all image placeholders

- **WHEN** `docs/tutor/py/ch2/2-7.md` is scanned for image placeholders and the Image Specification Appendix
- **THEN** every `> 📷 **圖 N**` placeholder in the body SHALL have a corresponding `### 圖 N` entry in the appendix

#### Scenario: All image prompts use the chapter visual style prefix

- **WHEN** a prompt in the Image Specification Appendix is reviewed
- **THEN** the `完整 Prompt` field SHALL begin with the American stick figure comic strip style prefix used throughout Chapter 2

---

### Requirement: Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)

The `docs/tutor/py/ch2/2-7.md` file MUST comply with the editorial rules established in the `python-ch1-content` specification:

- **P-1** (Punctuation): em-dashes (`——`) SHALL be used only for dramatic emphasis; routine clause separation SHALL use commas or colons
- **T-1** (Terminology forward reference): formal technical terms SHALL NOT be used before their designated teaching point without a controlled forward reference
- **S-1** (Analogy bridge): every analogy SHALL be preceded by a meta-cognitive bridge sentence
- **S-2** (Post-humor connector): after humor elements, the next sentence SHALL include an explicit callback connector (with the H3-boundary relaxation rule applied)
- **S-3** (Section transition): transitions between H2-level sections SHALL contain 2–4 sentences covering summary, gap, and motivation
- **C-1** (Code block lead-in): every fenced code block SHALL be preceded by at least one sentence of conversational setup
- **F-1** (Image placeholder dual-line format): every image placeholder SHALL use the dual-line format (image link line + caption line)
- **V-1** (VitePress container syntax): custom containers SHALL use `> [!TYPE]` syntax with the exclamation mark
- **T-3** (No empty UI elements): custom container blocks SHALL NOT have empty bodies
- **K-1** (Emotional punctuation density): within any 30-line prose block at least one emotional element SHALL be present; within any 10-line prose block no more than one emotional element SHALL be present; kaomoji variety rules SHALL apply

#### Scenario: P-1 rule is satisfied

- **WHEN** `docs/tutor/py/ch2/2-7.md` is scanned for em-dash usage
- **THEN** every `——` occurrence SHALL be in a dramatic emphasis context; explanatory or causal clauses SHALL use colons or commas instead

#### Scenario: F-1 rule is satisfied

- **WHEN** `docs/tutor/py/ch2/2-7.md` is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding `![📷 **圖 N**...](path)` image link line

#### Scenario: V-1 rule is satisfied

- **WHEN** `docs/tutor/py/ch2/2-7.md` is scanned for VitePress custom containers
- **THEN** every container opening line SHALL match the pattern `> [!TYPE]` with an exclamation mark

#### Scenario: K-1 emotional density rule is satisfied

- **WHEN** any contiguous 30-line prose block in `docs/tutor/py/ch2/2-7.md` is reviewed
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: K-1 kaomoji variety rule is satisfied

- **WHEN** `docs/tutor/py/ch2/2-7.md` is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice in the file, and the file SHALL use kaomoji from at least two different emotional categories
