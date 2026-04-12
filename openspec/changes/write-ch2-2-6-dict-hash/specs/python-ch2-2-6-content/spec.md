## ADDED Requirements

### Requirement: Section 2-6 file exists with correct frontmatter

The system SHALL provide a tutorial section file at `docs/tutor/py/ch2/2-6.md` for Module 2 (Chapter 2), Section 2-6 covering Dictionaries and Hash Tables.

The section file MUST have valid frontmatter with:
- `layout: doc`
- `chapter: 2`
- `section: "2-6"`
- `createdTime` in ISO 8601 format with `+08:00` timezone

#### Scenario: Section file has correct frontmatter

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-6.md` is parsed successfully with valid frontmatter fields (`layout`, `chapter`, `section`, `createdTime`)

#### Scenario: Section file appears in ch2 sidebar navigation

- **WHEN** a user visits the Chapter 2 index page
- **THEN** the sidebar displays a link to section 2-6 in the correct order


### Requirement: Section 2-6 covers Dict Key-Value structure as first knowledge point

The section file MUST teach the Dict Key-Value structure as the first knowledge point, covering:
1. Creating a dictionary using `{}` literal syntax and `dict()` constructor
2. Accessing values by key using `d[key]` syntax
3. Adding new key-value pairs
4. Modifying existing values
5. Common beginner pitfalls: `KeyError` when accessing a missing key, and the fix using `.get()`

The knowledge point MUST include exactly one worked example challenge (`字母頻率統計`, id: 41) with a full step-by-step walkthrough, followed by exactly two practice challenges (id: 42 and 43) with hints but no walkthroughs.

#### Scenario: Dict KV structure example is present and linked

- **WHEN** a user reads section 2-6
- **THEN** the Dict KV structure sub-section SHALL contain a `<ChallengeLink>` component pointing to challenge id 41 (字母頻率統計) with a full walkthrough

#### Scenario: Dict KV practice challenges are present and linked

- **WHEN** a user reads section 2-6
- **THEN** the Dict KV structure sub-section SHALL contain `<ChallengeLink>` components pointing to challenge id 42 and id 43, each with a brief hint but no step-by-step walkthrough


### Requirement: Section 2-6 introduces Tuple as an aside (no dedicated challenges)

The section file MUST introduce Tuple as an aside within the Dict KV knowledge point. The aside SHALL:
- Explain that a Tuple is an immutable, ordered sequence (similar to a list, but cannot be modified after creation)
- Show the syntax `t = (1, 2, 3)` and contrast with list syntax
- Note that Tuples are commonly used as dictionary keys when composite keys are needed
- Be clearly marked as supplementary information (not independently tested)

No dedicated practice challenges SHALL be created for Tuple. Tuple SHALL NOT appear as a standalone knowledge point.

#### Scenario: Tuple aside is present in section 2-6

- **WHEN** a user reads section 2-6
- **THEN** a clearly marked aside (e.g., a NOTE or INFO callout) explaining Tuple syntax and immutability SHALL appear within or after the Dict KV structure knowledge point

#### Scenario: No Tuple-only challenge exists

- **WHEN** the six challenge files for section 2-6 (id 41–46) are reviewed
- **THEN** none of them SHALL test Tuple concepts exclusively without also testing Dict concepts


### Requirement: Section 2-6 covers Hash lookup vs Linear Search as second knowledge point

The section file MUST teach the comparison between Hash lookup (O(1)) and Linear Search (O(n)) as the second knowledge point. The content MUST:
1. Reference the linear search concept introduced in section 2-4 as the baseline
2. Explain the conceptual origin: when data reaches millions of records, sequential search causes programs to hang
3. Explain the Hash Map invention: using a key to instantly locate a value in O(1) time
4. Provide a timing demonstration contrasting `in list` vs `in dict` lookup on a large dataset
5. Avoid mathematical notation beyond Big-O notation; use plain-language storytelling for zero-base learners

The knowledge point MUST include exactly one worked example challenge (`落單的數字`, id: 44) with a full step-by-step walkthrough, followed by exactly two practice challenges (id: 45 and 46) with hints but no walkthroughs.

#### Scenario: Hash vs Linear Search example is present and linked

- **WHEN** a user reads section 2-6
- **THEN** the hash lookup sub-section SHALL contain a `<ChallengeLink>` component pointing to challenge id 44 (落單的數字) with a full walkthrough

#### Scenario: Hash vs Linear Search references section 2-4

- **WHEN** the hash vs linear search sub-section is reviewed
- **THEN** it SHALL explicitly mention that linear search was introduced in section 2-4, establishing conceptual continuity

#### Scenario: Hash vs Linear Search practice challenges are present and linked

- **WHEN** a user reads section 2-6
- **THEN** the hash lookup sub-section SHALL contain `<ChallengeLink>` components pointing to challenge id 45 and id 46, each with a brief hint but no step-by-step walkthrough


### Requirement: Six challenge files exist for section 2-6 (IDs 41–46)

The system SHALL provide exactly six challenge files for section 2-6:

- id 41 (`字母頻率統計`) — example, Dict KV structure, medium difficulty
  - Count frequency of each letter in a string using a dict; ignore non-alpha characters
- id 42 — practice, Dict KV structure, easy difficulty
  - A dict-based lookup problem (e.g., word count or simple key lookup)
- id 43 — practice, Dict KV structure, medium difficulty
  - A dict accumulation problem (e.g., grouping or aggregation)
- id 44 (`落單的數字`) — example, Hash lookup vs Linear Search, medium difficulty
  - Find the single number in an array where every other element appears exactly twice; use dict/set for O(1) lookups
- id 45 — practice, Hash lookup / dict, easy difficulty
  - A membership-test problem demonstrating O(1) lookup advantage
- id 46 — practice, Hash lookup / dict, medium difficulty
  - A frequency-based deduplication or counting problem

Each challenge file MUST have:
- `layout: challenge`
- Correct `id` (41–46)
- `title` in Traditional Chinese
- `difficulty: easy` or `difficulty: medium`
- Appropriate `tags` including at least one of `[字典, dict, 雜湊]`
- `algorithm` in snake_case
- `testcase_count: 5` (minimum)
- Valid `params` block with at least one parameter
- A correct `generator` script that reads params and produces the expected output
- A `starter_code` block with a helpful comment hint

#### Scenario: All six challenge files exist

- **WHEN** the challenge directory is scanned
- **THEN** challenge files with ids 41, 42, 43, 44, 45, and 46 SHALL all be present

#### Scenario: Challenge generators produce correct output

- **WHEN** any of the six generators is executed with valid test input matching the params specification
- **THEN** the generator produces the correct expected output for that input

#### Scenario: Example challenges (id 41, 44) use dict-based solutions in generator

- **WHEN** the generator scripts for id 41 and id 44 are reviewed
- **THEN** both generators SHALL use Python dict operations (not just linear list scans) to compute the answer


### Requirement: Section 2-6 image placeholders follow dual-line format rule F-1

Every image placeholder in `docs/tutor/py/ch2/2-6.md` SHALL use the dual-line format:
1. An image link line: `![📷 **圖 N**：description（AI 製圖）](/assets/tutor/py/ch2/figNN.png)`
2. A caption line: `> 📷 **圖 N**：description（AI 製圖）`

The section MUST end with an Image Specification Appendix (`## 圖片規格附錄`) listing the fully expanded AI image generation prompt for each image.

All image prompts MUST use American stick figure comic style with dialogue-driven panels (no narration boxes), Traditional Chinese (Taiwan) speech bubble text, and English for technical terms.

#### Scenario: Image placeholder has both link and caption lines

- **WHEN** `docs/tutor/py/ch2/2-6.md` is scanned for image placeholders
- **THEN** every `> 📷 **圖 N**` caption line SHALL be immediately preceded by a corresponding image link line

#### Scenario: Image Specification Appendix exists

- **WHEN** the end of `docs/tutor/py/ch2/2-6.md` is reviewed
- **THEN** a `## 圖片規格附錄` section SHALL be present with one fully expanded prompt entry per image placeholder


### Requirement: Section 2-6 follows punctuation style rule P-1

`docs/tutor/py/ch2/2-6.md` SHALL use commas (，) or colons (：) for routine clause separation. The em-dash (`——`) SHALL be reserved exclusively for dramatic emphasis in hooks and humor. Em-dashes SHALL NOT be used for explanatory clauses (use colons) or continuation clauses (use commas).

The following decision checklist SHALL be applied to every `——` occurrence:
1. If `——` is followed by a causal clause (因為/由於/因此) → replace with colon (：)
2. If `——` is followed by a rhetorical or clarifying question → replace with comma (，)
3. If `——` introduces a definition or explanation of the preceding term → replace with colon (：)
4. If `——` introduces a contrast or pivot where the content is genuinely unexpected or humorous → KEEP the em-dash
5. If none of the above apply, default to replacing with comma (，)

#### Scenario: Routine clause uses comma or colon instead of em-dash

- **WHEN** `docs/tutor/py/ch2/2-6.md` contains a clause explaining a preceding term
- **THEN** the em-dash SHALL be replaced with a colon

#### Scenario: Dramatic em-dash for comedic timing is preserved

- **WHEN** `docs/tutor/py/ch2/2-6.md` contains an em-dash used for comedic timing or narrative surprise in a hook paragraph
- **THEN** the em-dash SHALL be preserved


### Requirement: Section 2-6 follows terminology forward-reference rule T-1

`docs/tutor/py/ch2/2-6.md` SHALL NOT use a formal technical term before its designated teaching point. Concepts already taught in Chapter 1 (print, input, variables, if/elif/else, for, while, break, continue, list, function basics) and earlier Chapter 2 sections (string methods, list operations, linear search from 2-4) ARE available for use without restriction.

If a concept not yet formally taught MUST be referenced, the section SHALL use a plain-language description OR a controlled forward reference (term introduced, immediately explained in parentheses, with a statement of when it will be properly taught).

#### Scenario: Available prior concepts are used freely

- **WHEN** `docs/tutor/py/ch2/2-6.md` uses `for` loop, `list`, or other already-taught concepts
- **THEN** no additional explanation or forward-reference qualifier is required for those terms

#### Scenario: Unknown term is explained on first use

- **WHEN** `docs/tutor/py/ch2/2-6.md` introduces a new technical term not taught in prior sections
- **THEN** the term SHALL be immediately followed by a plain-language explanation in parentheses


### Requirement: Section 2-6 follows analogy bridge rule S-1

Every analogy or metaphor in `docs/tutor/py/ch2/2-6.md` SHALL be preceded by a meta-cognitive bridge — one sentence explaining WHY the comparison is being made, before the comparison itself.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** section 2-6 introduces an analogy (e.g., a hash map compared to a phone book index)
- **THEN** the preceding sentence SHALL state the purpose of the analogy before the comparison is drawn


### Requirement: Section 2-6 follows post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions), the next sentence SHALL include an explicit callback connector that resumes the narrative thread.

When a humor element appears at the end of an H3 sub-section and the next structural element is a new H3 heading, the connector requirement is relaxed: the H3 heading itself serves as a structural boundary.

#### Scenario: Joke followed by connector before resuming exposition

- **WHEN** `docs/tutor/py/ch2/2-6.md` contains a parenthetical joke or kaomoji within a continuous prose block
- **THEN** the immediately following sentence SHALL contain an explicit connector linking back to the expository point

#### Scenario: Humor at H3 boundary with topic change

- **WHEN** a humor element is the last content of an H3 sub-section AND the next H3 introduces a substantially different sub-topic
- **THEN** the first sentence of prose under the new H3 SHALL include a brief transition phrase


### Requirement: Section 2-6 follows section transition rule S-3

Transitions between major conceptual sections (H2-level boundaries) in `docs/tutor/py/ch2/2-6.md` SHALL contain 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap or limitation, and (c) motivate the next section. Single-sentence transitions SHALL only be used between sub-steps within the same H2 section.

#### Scenario: Major section transition has adequate scaffolding

- **WHEN** an H2 section ends and the next H2 section begins in 2-6.md
- **THEN** the transition block SHALL contain 2–4 sentences covering summary, gap identification, and motivation


### Requirement: Section 2-6 code blocks follow conversational lead-in rule C-1

Every fenced code block in `docs/tutor/py/ch2/2-6.md` SHALL be preceded by at least one sentence of conversational setup that establishes context for why the code is being shown. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** `docs/tutor/py/ch2/2-6.md` contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading (H2/H3) and the opening code fence


### Requirement: Section 2-6 follows error prevention rule E-1

Common beginner pitfalls with dicts (e.g., `KeyError` on missing key, mutating a dict while iterating, using mutable types as keys) SHALL be addressed immediately after the syntax is first introduced, not deferred exclusively to a "common errors" section.

#### Scenario: KeyError pitfall warned at point of introduction

- **WHEN** `docs/tutor/py/ch2/2-6.md` introduces `d[key]` access syntax
- **THEN** a warning about `KeyError` and the `.get()` alternative SHALL appear within the same sub-section


### Requirement: Section 2-6 code examples follow mental model rule M-1

When a code example implicitly demonstrates a fundamental evaluation concept (e.g., hashing, O(1) vs O(n) complexity), the tutorial section SHALL make the concept explicit with a step-by-step trace or timing comparison showing the difference.

#### Scenario: Hash lookup O(1) is traced or demonstrated

- **WHEN** the hash vs linear search sub-section presents a timing comparison code block
- **THEN** the accompanying explanation SHALL include a step-by-step description or measurement output showing that dict lookup is significantly faster than list search on large data


### Requirement: Section 2-6 VitePress custom containers use correct syntax rule V-1

All VitePress custom container callouts in `docs/tutor/py/ch2/2-6.md` SHALL use the correct syntax `> [!TYPE]` where TYPE is one of `NOTE`, `TIP`, `WARNING`, `DANGER`, `DETAILS`. The exclamation mark (`!`) inside the brackets is mandatory.

#### Scenario: Custom container uses correct syntax

- **WHEN** `docs/tutor/py/ch2/2-6.md` contains a blockquote-based custom container
- **THEN** the opening line SHALL match the pattern `> [!TYPE]` (with exclamation mark)


### Requirement: Section 2-6 contains no empty UI elements (rule T-3)

`docs/tutor/py/ch2/2-6.md` SHALL NOT contain custom container blocks where the title line exists but the body content is empty or contains only whitespace.

#### Scenario: Every visible container has substantive content

- **WHEN** a custom container is visible in `docs/tutor/py/ch2/2-6.md`
- **THEN** the container body SHALL contain at least one sentence of substantive content


### Requirement: Section 2-6 contains no residual TBD markers (rule T-2)

`docs/tutor/py/ch2/2-6.md` SHALL contain no `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs or standalone `<!-- TBD ... -->` comments. All placeholder or deferred-content markers SHALL be resolved before publication.

#### Scenario: No TBD markers in 2-6.md

- **WHEN** `docs/tutor/py/ch2/2-6.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found


### Requirement: Section 2-6 follows emotional punctuation density rule K-1

`docs/tutor/py/ch2/2-6.md` SHALL maintain a balanced density of emotional punctuation elements (kaomoji, parenthetical jokes, student dialogue interjections). Within any contiguous block of 30 lines of prose (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element SHALL be present. Within any contiguous block of 10 lines of prose, no more than one emotional punctuation element SHALL be present.

Kaomoji variety SHALL be maintained:
- The same kaomoji SHALL NOT appear more than twice within the section file
- The section file SHALL use kaomoji from at least two different emotional categories (Resigned, Celebration, Shock, Frustration, Sadness, Cute, Mischievous, Confusion)

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose (excluding code, tables, images) is identified in `docs/tutor/py/ch2/2-6.md`
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a contiguous block of 10 lines of prose is identified in `docs/tutor/py/ch2/2-6.md`
- **THEN** no more than one emotional punctuation element SHALL be present within that block

#### Scenario: Kaomoji variety is maintained

- **WHEN** `docs/tutor/py/ch2/2-6.md` is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice, and the file SHALL contain kaomoji from at least two different emotional categories
