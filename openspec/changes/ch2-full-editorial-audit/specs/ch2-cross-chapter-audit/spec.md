## ADDED Requirements

### Requirement: EAL workflow executes on all Chapter 2 section files

The Editorial Audit Loop (EAL) workflow SHALL be executed with target directory `docs/tutor/py/ch2/` and the full rule set (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, W-1, T-2) in the fixed scan order defined by the `editorial-audit-loop` spec. The target files SHALL be `2-1.md`, `2-2.md`, `2-3.md`, `2-4.md`, `2-5.md`, `2-6.md`, and `2-7.md`. The workflow SHALL terminate when either zero violations are found or 3 rounds have been completed.

#### Scenario: All seven section files are scanned

- **WHEN** one round of the EAL workflow is executed on `docs/tutor/py/ch2/`
- **THEN** all 7 section files (2-1.md through 2-7.md) SHALL be scanned against every rule in the fixed scan order

#### Scenario: EAL produces structured violation log

- **WHEN** a violation is detected during any round
- **THEN** the violation log entry SHALL include: file path, line number or range, rule ID, violation description, suggested fix, and classification (immediate-fix, content-fix, or structural)

#### Scenario: Violations are fixed between rounds

- **WHEN** a round produces violations classified as immediate-fix or content-fix
- **THEN** all such violations SHALL be fixed before the next round begins

#### Scenario: EAL terminates correctly

- **WHEN** either zero violations are found in a round OR 3 rounds have been completed
- **THEN** the EAL workflow SHALL terminate and produce a summary report

---

### Requirement: Cross-chapter kaomoji audit X-1

The audit SHALL collect all kaomoji occurrences across all 7 section files and verify that no single kaomoji appears more than 3 times across the entire chapter. If a kaomoji exceeds the limit, the audit SHALL identify which files contain the duplicates and suggest replacement kaomoji from underused emotional categories.

#### Scenario: Kaomoji within cross-chapter limit

- **WHEN** all 7 section files are scanned for kaomoji
- **THEN** no single kaomoji SHALL appear more than 3 times across all files combined

#### Scenario: Kaomoji exceeds limit

- **WHEN** a kaomoji is found more than 3 times across the chapter
- **THEN** the violation log SHALL identify all occurrences with file paths and line numbers, and suggest specific replacement kaomoji from underused emotional categories

---

### Requirement: Cross-chapter terminology map audit X-2

The audit SHALL build a complete terminology teaching-point map for Chapter 2 and verify that no section uses a formal technical term before its designated teaching point. The map SHALL include:

- 2-1: `for`, `range()`, iteration (迭代)
- 2-2: `while`
- 2-3: `break`, `continue`
- 2-4: list (串列), index (索引), `len()`, `append()`, linear search (線性搜尋)
- 2-5: variable swap (變數交換), nested loop (雙重迴圈/巢狀迴圈), bubble sort (氣泡排序)
- 2-6: dict (字典), key-value, `tuple` (元組), hash (雜湊)

Any usage of a term before its teaching section SHALL be flagged unless it uses a controlled forward reference (plain-language description + parenthetical explanation + promise of when formally taught).

#### Scenario: Term used in correct section or later

- **WHEN** a formal technical term is found in a section at or after its teaching point
- **THEN** no violation SHALL be recorded

#### Scenario: Term used before teaching point without forward reference

- **WHEN** a formal technical term is found in a section before its teaching point AND it does not use a controlled forward reference
- **THEN** a violation SHALL be recorded with the term, the file where found, and the section where it is formally taught

#### Scenario: Controlled forward reference is acceptable

- **WHEN** a formal technical term appears before its teaching point but includes a parenthetical plain-language explanation and a statement of when it will be formally taught
- **THEN** no violation SHALL be recorded

---

### Requirement: Challenge ID continuity audit X-3

The audit SHALL verify that challenge files in `docs/challenge/` with IDs 11 through 46 exist without gaps or duplicates. Each ID SHALL map to exactly one challenge file. The audit SHALL also verify that each challenge file's `id` frontmatter field matches its expected value.

#### Scenario: All 36 challenge IDs present

- **WHEN** the `docs/challenge/` directory is scanned for files with `id` frontmatter values 11 through 46
- **THEN** exactly 36 files SHALL be found, one per ID, with no gaps and no duplicates

#### Scenario: Challenge ID mismatch detected

- **WHEN** a challenge file's `id` frontmatter value does not match the expected sequential ID
- **THEN** a violation SHALL be recorded identifying the file and the mismatched ID

---

### Requirement: Image numbering continuity audit X-4

The audit SHALL verify that image placeholder numbering across all 7 section files has no duplicates. Each section SHALL use a distinct numbering range or a chapter-wide sequential numbering scheme. No two image placeholders across different sections SHALL share the same number.

#### Scenario: No duplicate image numbers across sections

- **WHEN** all `![📷 **圖 N**` placeholders across 2-1.md through 2-7.md are collected
- **THEN** no two placeholders SHALL have the same N value

#### Scenario: Image appendix entries match placeholders

- **WHEN** each section's Image Specification Appendix is cross-referenced with its image placeholders
- **THEN** every placeholder SHALL have a corresponding appendix entry and vice versa

---

### Requirement: Index link verification audit X-5

The audit SHALL verify that every link in `docs/tutor/py/ch2/index.md` resolves to an existing file in the `docs/tutor/py/ch2/` directory.

#### Scenario: All index links resolve

- **WHEN** `docs/tutor/py/ch2/index.md` is parsed for internal links
- **THEN** all 7 section links SHALL resolve to existing `.md` files

---

### Requirement: Frontmatter consistency audit X-6

The audit SHALL verify that all 7 section files have consistent frontmatter: `chapter: 2`, `section` in format `"2-N"` matching the filename, `createdTime` in ISO 8601 with `+08:00` timezone, and `layout: doc`. The summary section (2-7) SHALL NOT have a `challenge` field. Content sections (2-1 through 2-6) SHALL each have a `challenge` field referencing a valid slug.

#### Scenario: All section files have consistent frontmatter

- **WHEN** all 7 section files' frontmatter is parsed
- **THEN** every file SHALL have `layout: doc`, `chapter: 2`, `section` matching `"2-N"` where N matches the filename, and `createdTime` in ISO 8601 with `+08:00` timezone

#### Scenario: Challenge field presence matches section type

- **WHEN** content sections (2-1 through 2-6) are checked
- **THEN** each SHALL have a `challenge` field referencing a slug that matches a file in `docs/challenge/`
- **WHEN** the summary section (2-7) is checked
- **THEN** it SHALL NOT have a `challenge` field

---

### Requirement: Section transition coherence audit X-7

The audit SHALL verify that each section's closing preview and the next section's opening are thematically coherent. Specifically:

- 2-1 closing SHALL mention `while` or conditional looping; 2-2 opening SHALL reference it
- 2-2 closing SHALL mention loop control or `break`/`continue`; 2-3 opening SHALL reference it
- 2-3 closing SHALL mention data management or lists; 2-4 opening SHALL reference it
- 2-4 closing SHALL mention sorting or ordering; 2-5 opening SHALL reference it
- 2-5 closing SHALL mention fast lookup or dictionaries; 2-6 opening SHALL reference it
- 2-6 closing SHALL mention module summary or review; 2-7 opening SHALL reference it

#### Scenario: Adjacent sections have coherent transitions

- **WHEN** the last H2 section of file 2-N.md and the opening of file 2-(N+1).md are compared (for N = 1 through 6)
- **THEN** the closing preview keywords SHALL be referenced in the next section's opening content

#### Scenario: Transition gap detected

- **WHEN** a section's closing preview topic does not match the next section's opening topic
- **THEN** a violation SHALL be recorded identifying both files and the mismatched topics

---

### Requirement: Audit summary report is produced

After the EAL workflow terminates, a summary report SHALL be produced containing: number of rounds executed, per-round violation count, cross-chapter check results (pass/fail for each of X-1 through X-7), and (if applicable) a detailed list of remaining structural violations with recommended follow-up change names and scopes.

#### Scenario: Clean audit produces passing report

- **WHEN** the EAL terminates with zero violations and all cross-chapter checks pass
- **THEN** the summary report SHALL state "zero violations" and "all cross-chapter checks passed"

#### Scenario: Structural violations produce follow-up recommendations

- **WHEN** the EAL terminates with remaining structural violations
- **THEN** the summary report SHALL list each structural violation with: file path, rule ID, description, and a recommended follow-up change name and scope description
