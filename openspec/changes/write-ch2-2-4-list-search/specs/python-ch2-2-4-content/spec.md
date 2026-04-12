## ADDED Requirements

### Requirement: Section 2-4 file exists with correct frontmatter

The system SHALL provide a tutorial section file at `docs/tutor/py/ch2/2-4.md` with valid frontmatter containing `layout: doc`, `chapter: 2`, `section: "2-4"`, and `createdTime` in ISO 8601 format with `+08:00` timezone offset.

#### Scenario: Section 2-4 frontmatter is valid

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-4.md` is parsed successfully with frontmatter fields `layout: doc`, `chapter: 2`, `section: "2-4"`, and a valid `createdTime`

#### Scenario: Section 2-4 appears in chapter 2 sidebar

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar displays a link to section 2-4


### Requirement: Section 2-4 covers two knowledge points

The section file `docs/tutor/py/ch2/2-4.md` SHALL cover exactly two knowledge points in order:
1. List basics — creating lists, zero-based indexing, `len()`, `append()`, and `for item in list` iteration
2. Linear Search algorithm — iterating through a list to find a target value or the maximum value and its index

#### Scenario: List basics knowledge point is present

- **WHEN** a reader reads section 2-4
- **THEN** the content SHALL introduce list creation syntax, zero-based indexing, `len()`, `append()`, and `for item in list` iteration as a natural progression from `for i in range()` taught in section 2-1

#### Scenario: Linear Search knowledge point is present

- **WHEN** a reader reads section 2-4
- **THEN** the content SHALL introduce the linear search algorithm as the most intuitive method for finding data in a list, including a worked example of finding the maximum value and its index


### Requirement: Section 2-4 introduces for-item-in-list as natural transition from range-based for

The tutorial SHALL present `for item in list` as a natural evolution of the `for i in range()` pattern taught in section 2-1. The section SHALL explain the conceptual difference: `for i in range()` iterates over indices, while `for item in list` iterates directly over values.

#### Scenario: Transition from range-based for is explained

- **WHEN** a reader encounters the `for item in list` syntax
- **THEN** the section SHALL include a comparison or bridge paragraph connecting it to `for i in range()` from section 2-1, explaining that the new form iterates over values directly


### Requirement: Section 2-4 respects T-1 boundary constraints

Section 2-4 SHALL NOT introduce any of the following concepts that are not yet taught at this point in the curriculum:
- `dict` (dictionary)
- `tuple`
- Nested loops (loops inside loops)
- Bubble sort or any other sorting algorithm
- List comprehension (reserved for Module 4)
- Two-dimensional (nested) lists

#### Scenario: Forbidden concepts are absent

- **WHEN** section 2-4 is reviewed for T-1 compliance
- **THEN** the content SHALL contain no examples, explanations, or code using `dict`, `tuple`, nested loops, bubble sort, list comprehension, or two-dimensional lists

#### Scenario: Available language features are used correctly

- **WHEN** section 2-4 contains code examples
- **THEN** only `for`, `while`, `range()`, `break`, `continue`, list indexing, `len()`, and `append()` SHALL be used as control flow and list operation primitives


### Requirement: Six challenge files exist for section 2-4

The system SHALL provide six challenge files covering the two knowledge points of section 2-4:
- ID 26 (example, List basics)
- ID 27 (practice 1, List basics)
- ID 28 (practice 2, List basics)
- ID 29 (example, Linear Search — find maximum value and its index)
- ID 30 (practice 1, Linear Search)
- ID 31 (practice 2, Linear Search)

Each challenge file MUST have `layout: challenge`, a valid `id`, `title`, `difficulty`, `tags`, `algorithm`, `testcase_count: 5`, `params` with type/min/max, a correct `generator` script, and `starter_code` with a hint comment.

#### Scenario: All six challenge files exist

- **WHEN** the challenge directory is scanned
- **THEN** files for IDs 26 through 31 SHALL exist at `docs/challenge/py/` with valid YAML frontmatter

#### Scenario: Challenge generators produce correct output

- **WHEN** any of the six generator scripts is executed with valid test input matching its params specification
- **THEN** the generator produces the correct expected output for that input

#### Scenario: Challenge IDs are linked from section 2-4

- **WHEN** a reader reaches the knowledge point worked example in section 2-4
- **THEN** the section SHALL contain `<ChallengeLink>` components pointing to the corresponding challenge IDs (26 for List basics example, 29 for Linear Search example)


### Requirement: Section 2-4 challenges are linked with ChallengeLink components

Each of the six challenges for section 2-4 SHALL be referenced from `docs/tutor/py/ch2/2-4.md` using the `<ChallengeLink>` component. Example challenges (IDs 26 and 29) SHALL appear within the main worked-example walkthrough. Practice challenges (IDs 27, 28, 30, 31) SHALL appear in a practice area with a brief hint but no step-by-step solution.

#### Scenario: Example ChallengeLink is embedded in walkthrough

- **WHEN** a reader reads the List basics worked example
- **THEN** a `<ChallengeLink id="26">` SHALL appear linking to the example challenge

#### Scenario: Practice ChallengeLinks appear with hints only

- **WHEN** a reader reads the practice area of either knowledge point
- **THEN** `<ChallengeLink>` components for practice challenges SHALL be present with a hint comment but no full solution walkthrough


### Requirement: Section 2-4 includes image placeholders and Image Specification Appendix

The section file `docs/tutor/py/ch2/2-4.md` SHALL contain image placeholders using dual-line format and SHALL end with an Image Specification Appendix containing fully expanded prompts for each image.

Every image placeholder SHALL use the format:
1. `![📷 **圖 N**：description（AI 製圖）](/assets/tutor/py/ch2/2-4/figNN.png)`
2. `> 📷 **圖 N**：description（AI 製圖）`

All image prompts in the appendix SHALL use American stick figure comic style with dialogue-driven panels (no narration boxes), Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Image placeholders use dual-line format

- **WHEN** section 2-4 is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption SHALL be immediately preceded by a corresponding `![📷 **圖 N**...](path)` image link line

#### Scenario: Visual rhythm rule is satisfied

- **WHEN** section 2-4 is reviewed for visual rhythm
- **THEN** every H2 section SHALL contain at least one visual element and no more than five consecutive paragraphs of pure text SHALL exist without a visual element

#### Scenario: Image Specification Appendix exists

- **WHEN** section 2-4 is read to its end
- **THEN** an Image Specification Appendix section SHALL be present containing the fully expanded prompt for each image used in the section


### Requirement: Section 2-4 follows punctuation style rule P-1

Section 2-4 SHALL use commas (，) or colons (：) for routine clause separation. The em-dash (`——`) SHALL be reserved exclusively for dramatic emphasis in hooks and humor. The decision checklist from rule P-1 SHALL apply:
1. `——` followed by a causal clause → replace with colon (：)
2. `——` followed by a rhetorical or clarifying question → replace with comma (，)
3. `——` introduces a definition or explanation → replace with colon (：)
4. `——` introduces genuine contrast or humor → KEEP
5. Default → replace with comma (，)

#### Scenario: Routine clause uses comma or colon

- **WHEN** section 2-4 contains a clause explaining a preceding term
- **THEN** the em-dash SHALL be replaced with a colon

#### Scenario: Dramatic em-dash is preserved

- **WHEN** section 2-4 contains an em-dash for comedic timing or narrative surprise
- **THEN** the em-dash SHALL be preserved


### Requirement: Section 2-4 follows terminology forward-reference rule T-1

Section 2-4 SHALL NOT use a formal technical term before its designated teaching point. If a concept MUST be referenced before being formally taught, the section SHALL use a plain-language description OR a controlled forward reference (term introduced, immediately explained in parentheses, with a statement of when it will be properly taught).

#### Scenario: Forbidden term is replaced with plain language

- **WHEN** section 2-4 references a concept not yet formally introduced
- **THEN** a plain-language equivalent SHALL be used instead of the formal term

#### Scenario: Unavoidable forward reference includes explanation

- **WHEN** a formal term MUST appear before its teaching point
- **THEN** the term SHALL be followed by a parenthetical explanation and a statement indicating which section will formally teach it


### Requirement: Section 2-4 follows analogy bridge rule S-1

Every analogy or metaphor in section 2-4 SHALL be preceded by a meta-cognitive bridge — one sentence explaining WHY the comparison is being made before the comparison itself.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** section 2-4 introduces an analogy (e.g., a shelf or row of boxes for a list)
- **THEN** the preceding sentence SHALL state the purpose of the analogy


### Requirement: Section 2-4 follows post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions) in section 2-4, the next sentence SHALL include an explicit callback connector that resumes the narrative thread. The H3-boundary relaxation from rule S-2 applies: when a humor element closes an H3 sub-section, the new H3 heading itself serves as a structural boundary and an explicit connector is only required when the new H3 introduces a substantially different sub-topic.

#### Scenario: Joke within prose is followed by connector

- **WHEN** section 2-4 contains a parenthetical joke or kaomoji within a continuous prose block
- **THEN** the immediately following sentence SHALL contain an explicit connector linking back to the expository point


### Requirement: Section 2-4 follows section transition rule S-3

Transitions between major conceptual sections (H2-level boundaries) in section 2-4 SHALL contain 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap or limitation, and (c) motivate the next section.

#### Scenario: H2 transition has adequate scaffolding

- **WHEN** an H2 section ends and the next H2 section begins in section 2-4
- **THEN** the transition block SHALL contain 2–4 sentences covering summary, gap, and motivation


### Requirement: Section 2-4 code blocks follow conversational lead-in rule C-1

Every fenced code block in section 2-4 SHALL be preceded by at least one sentence of conversational setup. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** section 2-4 contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading and the opening code fence


### Requirement: Section 2-4 follows error prevention rule E-1

Common beginner mistakes for list operations SHALL be addressed immediately after the syntax is first introduced. Key pitfalls include: off-by-one indexing errors (accessing index equal to `len(list)`), mutating a list while iterating over it, and confusing list index with list value in linear search.

#### Scenario: Index error pitfall is warned at introduction

- **WHEN** section 2-4 introduces list indexing
- **THEN** a warning about accessing an index beyond `len(list) - 1` SHALL appear within the same sub-section

#### Scenario: Linear search pitfall is warned at introduction

- **WHEN** section 2-4 introduces the linear search pattern
- **THEN** a note distinguishing between the found index and the found value SHALL appear within the same sub-section


### Requirement: Section 2-4 follows mental model rule M-1

When a code example demonstrates a fundamental evaluation concept (such as how `for item in list` assigns each element in sequence, or how a running-maximum comparison updates), section 2-4 SHALL make the concept explicit with a step-by-step trace.

#### Scenario: List iteration is traced step-by-step

- **WHEN** section 2-4 introduces `for item in list`
- **THEN** an accompanying trace SHALL show how `item` takes each value in sequence across iterations

#### Scenario: Running-maximum update is traced

- **WHEN** section 2-4 presents the linear search / find-maximum algorithm
- **THEN** the explanation SHALL include a step-by-step trace showing how the current maximum and its index update across iterations


### Requirement: Section 2-4 follows emotional punctuation density rule K-1

Within any contiguous block of 30 lines of prose in section 2-4 (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element (kaomoji, parenthetical joke, student dialogue interjection) SHALL be present. Within any contiguous block of 10 lines of prose, no more than one such element SHALL be present.

Kaomoji variety SHALL be maintained:
- The same kaomoji SHALL NOT appear more than twice within section 2-4.
- Section 2-4 SHALL use kaomoji from at least two different emotional categories as defined in the `phoenix-popular-science-article-style` kaomoji catalog.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a 30-line prose block is identified in section 2-4
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a 10-line prose block is identified in section 2-4
- **THEN** no more than one emotional punctuation element SHALL be present

#### Scenario: Kaomoji variety is maintained

- **WHEN** section 2-4 is scanned for kaomoji
- **THEN** no single kaomoji SHALL appear more than twice, and kaomoji from at least two emotional categories SHALL be present


### Requirement: Section 2-4 contains no empty UI elements per rule T-3

Published section 2-4 SHALL NOT contain custom container blocks (NOTE, TIP, WARNING, DANGER, DETAILS) where the body content is empty or contains only whitespace. Unready containers SHALL be wrapped in HTML comments.

#### Scenario: No empty containers are visible

- **WHEN** section 2-4 is reviewed
- **THEN** every visible custom container block SHALL contain at least one sentence of substantive content


### Requirement: Section 2-4 VitePress custom containers use correct syntax per rule V-1

All VitePress custom container callouts in section 2-4 SHALL use the syntax `> [!TYPE]` where TYPE is one of `NOTE`, `TIP`, `WARNING`, `DANGER`, `DETAILS`. The pattern `> [TYPE]` without `!` SHALL NOT be used.

#### Scenario: Custom container uses correct syntax

- **WHEN** section 2-4 contains a blockquote-based custom container
- **THEN** the opening line SHALL match the pattern `> [!TYPE]`
