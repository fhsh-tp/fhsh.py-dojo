## MODIFIED Requirements

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

---

## ADDED Requirements

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

---

### Requirement: Chapter 1 VitePress custom containers use correct syntax rule V-1

All VitePress custom container callouts in `docs/tutor/py/ch1/` SHALL use the correct syntax `> [!TYPE]` where TYPE is one of `NOTE`, `TIP`, `WARNING`, `DANGER`, `DETAILS`. The exclamation mark (`!`) inside the brackets is mandatory. The pattern `> [TYPE]` without `!` SHALL NOT be used as it will not render correctly.

#### Scenario: Custom container uses correct syntax

- **WHEN** a tutorial section contains a blockquote-based custom container
- **THEN** the opening line SHALL match the pattern `> [!TYPE]` (with exclamation mark)

#### Scenario: Incorrect syntax is detected

- **WHEN** a tutorial section contains a pattern matching `> [WARNING]`, `> [TIP]`, `> [NOTE]`, `> [DANGER]`, or `> [DETAILS]` without the `!`
- **THEN** the pattern SHALL be corrected to include the `!` (e.g., `> [WARNING]` → `> [!WARNING]`)

---

### Requirement: Chapter 1 sections contain no empty UI elements rule T-3

Published tutorial sections in `docs/tutor/py/ch1/` SHALL NOT contain custom container blocks (NOTE, TIP, WARNING, DANGER, DETAILS) where the title line exists but the body content is empty or contains only whitespace. If the content for a container is not yet ready, the entire container block SHALL be wrapped in an HTML comment (e.g., `<!-- DEFERRED: description -->`) so it is invisible to readers.

#### Scenario: Empty container is hidden

- **WHEN** a tutorial section contains a custom container whose body has no substantive content
- **THEN** the entire container block (title and body) SHALL be wrapped in HTML comments (e.g., `<!-- DEFERRED: ... -->`), not left as a visible empty box

#### Scenario: Completed container has content

- **WHEN** a custom container is visible (not inside HTML comments)
- **THEN** the container body SHALL contain at least one sentence of substantive content

---

### Requirement: Chapter 1 sections follow emotional punctuation density rule K-1

Each tutorial section in `docs/tutor/py/ch1/` SHALL maintain a balanced density of emotional punctuation elements (kaomoji, parenthetical jokes, student dialogue interjections). Within any contiguous block of 30 lines of prose (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element SHALL be present. Within any contiguous block of 10 lines of prose, no more than one emotional punctuation element SHALL be present.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose (excluding code, tables, images) is identified in a tutorial section
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a contiguous block of 10 lines of prose is identified in a tutorial section
- **THEN** no more than one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block
