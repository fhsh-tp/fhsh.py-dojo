## ADDED Requirements

### Requirement: Chapter 1 sections follow punctuation style rule P-1

Each tutorial section in `docs/tutor/py/ch1/` SHALL use commas (，) or colons (：) for routine clause separation. The em-dash (`——`) SHALL be reserved exclusively for dramatic emphasis in hooks and humor. Em-dashes SHALL NOT be used for explanatory clauses (use colons) or continuation clauses (use commas).

#### Scenario: Routine clause uses comma or colon instead of em-dash

- **WHEN** a tutorial section contains a clause that explains a preceding term (e.g., "X的用途——它會...")
- **THEN** the em-dash SHALL be replaced with a colon (e.g., "X的用途：它會...")

#### Scenario: Dramatic em-dash is preserved

- **WHEN** a tutorial section contains an em-dash used for comedic timing or narrative surprise in a hook paragraph
- **THEN** the em-dash SHALL be preserved

---

### Requirement: Chapter 1 sections follow terminology forward-reference rule T-1

Tutorial sections SHALL NOT use a formal technical term before its designated teaching point. If a concept MUST be referenced before being formally taught, the section SHALL use a plain-language description OR a controlled forward reference (term introduced, immediately explained in parentheses, with a statement of when it will be properly taught).

#### Scenario: Term used before teaching point is replaced with plain language

- **WHEN** a section references a concept (e.g., "變數") that is formally introduced in a later section
- **THEN** the reference SHALL use a plain-language equivalent (e.g., "資料儲存空間") instead of the formal term

#### Scenario: Controlled forward reference includes explanation and promise

- **WHEN** a formal term MUST be used before its teaching point (unavoidable forward reference)
- **THEN** the term SHALL be immediately followed by a parenthetical plain-language explanation AND a statement indicating which section will formally teach it (e.g., "...這個**變數（Variable）**...（下一節會正式介紹）")

---

### Requirement: Chapter 1 sections follow analogy bridge rule S-1

Every analogy or metaphor in a tutorial section SHALL be preceded by a meta-cognitive bridge — one sentence explaining WHY the comparison is being made, before the comparison itself.

#### Scenario: Analogy has meta-cognitive setup

- **WHEN** a tutorial section introduces an analogy (e.g., calculator analogy for print(), locker analogy for variables)
- **THEN** the preceding sentence SHALL state the purpose of the analogy (e.g., "Why am I talking about calculators? Because...")

---

### Requirement: Chapter 1 sections follow post-humor connector rule S-2

After humor elements (kaomoji, parenthetical jokes, comedic digressions), the next sentence SHALL include an explicit callback connector that resumes the narrative thread (e.g., "沒錯！", "回到正題", or a reference to the pre-joke assertion).

#### Scenario: Joke followed by connector before resuming exposition

- **WHEN** a tutorial section contains a parenthetical joke or kaomoji-decorated comedic aside
- **THEN** the immediately following sentence SHALL contain an explicit connector that links back to the expository point preceding the joke

---

### Requirement: Chapter 1 sections follow section transition rule S-3

Transitions between major conceptual sections (H2-level boundaries) SHALL contain 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap or limitation, and (c) motivate the next section. Single-sentence transitions SHALL only be used between sub-steps within the same H2 section.

#### Scenario: Major section transition has adequate scaffolding

- **WHEN** an H2 section ends and the next H2 section begins
- **THEN** the transition block (between the closing `---` and the next `##` heading) SHALL contain 2–4 sentences covering summary, gap identification, and motivation

#### Scenario: Sub-step transition within same section is concise

- **WHEN** a transition occurs between H3 sub-steps within the same H2 section
- **THEN** the transition SHALL be 1–2 sentences

---

### Requirement: Chapter 1 code blocks follow conversational lead-in rule C-1

Every fenced code block (` ```python ``` `) in a tutorial section SHALL be preceded by at least one sentence of conversational setup that establishes context for why the code is being shown. No code block SHALL immediately follow a heading without intervening prose.

#### Scenario: Code block has lead-in text

- **WHEN** a tutorial section contains a fenced Python code block
- **THEN** at least one sentence of prose SHALL appear between the nearest preceding heading (H2/H3) and the opening code fence

---

### Requirement: Chapter 1 sections follow error prevention rule E-1

Common beginner syntax mistakes (e.g., quote mixing, `=` vs `==` confusion, missing `int()` conversion) SHALL be addressed immediately after the syntax is first introduced, not deferred exclusively to a "common errors" section at the end of a problem walkthrough.

#### Scenario: Syntax pitfall warned at point of introduction

- **WHEN** a tutorial section introduces a syntax element that has a known high-frequency beginner mistake
- **THEN** a warning or note about the mistake SHALL appear within the same sub-section where the syntax is first taught

---

### Requirement: Chapter 1 code examples follow mental model rule M-1

When a code example implicitly demonstrates a fundamental evaluation concept (e.g., inside-out expression evaluation, operator precedence), the tutorial section SHALL make the concept explicit with a step-by-step trace showing the evaluation order.

#### Scenario: Expression evaluation is traced step-by-step

- **WHEN** a code example contains a compound expression (e.g., `print(1+1)`, `int(input())`, compound boolean expressions)
- **THEN** the accompanying explanation SHALL include a numbered trace showing each evaluation step (e.g., "Step 1: Python evaluates 1+1 → 2. Step 2: Python calls print(2) → prints '2'")

#### Scenario: Later sections callback to earlier mental model

- **WHEN** a later section uses the same evaluation pattern introduced in an earlier section
- **THEN** the explanation SHALL include a brief callback reference to the earlier example (e.g., "Remember how print(1+1) evaluates from inside out? int(input()) works the same way")
