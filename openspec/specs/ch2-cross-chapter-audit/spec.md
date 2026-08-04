## Requirements

### Requirement: All Module 2 section files pass EAL 15-rule scan

All section files in `docs/tutor/py/ch2/` SHALL pass a full Editorial Audit Loop scan covering all 15 rules (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, W-1, T-2) with zero violations after a maximum of 3 rounds.

#### Scenario: EAL produces clean pass within 3 rounds

- **WHEN** the EAL workflow is executed on `docs/tutor/py/ch2/`
- **THEN** the violation count SHALL reach zero within 3 scanning rounds


<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->

---
### Requirement: Cross-file kaomoji K-1 compliance across Module 2

Across all section files in Module 2, the same kaomoji SHALL NOT appear more than 3 times total. Each section file SHALL use at least 2 different emotion categories.

#### Scenario: No kaomoji exceeds 3 occurrences across chapter

- **WHEN** all kaomoji in `docs/tutor/py/ch2/*.md` are counted
- **THEN** no single kaomoji pattern SHALL appear more than 3 times across all files combined


<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->

---
### Requirement: Challenge ID continuity across Module 2

All challenge files referenced from Module 2 sections SHALL carry string ids in the challenge id format, and their ordinals (the decimal integer after the category prefix) SHALL be sequential with no gaps or duplicates when sorted numerically within the `py` prefix. Module 2 challenge ordinals SHALL form a contiguous block that starts immediately after Module 1's last ordinal.

#### Scenario: Challenge ordinals form continuous sequence

- **WHEN** all challenge ids referenced from Module 2 are collected and their ordinals sorted
- **THEN** the ordinals SHALL form a continuous integer sequence with no gaps

#### Scenario: Per-chapter ordinal blocks are contiguous

- **WHEN** challenge ordinals are grouped by chapter and sorted
- **THEN** each chapter's ordinals SHALL form a contiguous block with no interleaving from other chapters

---
### Requirement: Image numbering continuity across Module 2

Image numbers (圖 N) across all sections in Module 2 SHALL be globally sequential with no gaps or duplicates.

#### Scenario: Image numbers are sequential across sections

- **WHEN** image numbers are extracted from all `docs/tutor/py/ch2/*.md` files
- **THEN** they SHALL form a continuous sequence starting from 1 (or continuing from previous chapter)


<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->

---
### Requirement: Index links resolve to existing files

Every section link in `docs/tutor/py/ch2/index.md` SHALL resolve to an existing file.

#### Scenario: All index links are valid

- **WHEN** each link in the chapter index is tested
- **THEN** the target file SHALL exist on disk


<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->

---
### Requirement: Section transitions are coherent across Module 2

Each section's closing "下一節預告" paragraph SHALL align with the next section's opening paragraph. The preview topic SHALL match the actual topic taught in the next section.

#### Scenario: Section 2-M closing matches 2-(M+1) opening

- **WHEN** section 2-M's closing paragraph and section 2-(M+1)'s opening paragraph are compared
- **THEN** the topic previewed SHALL match the topic introduced


<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->

---
### Requirement: Frontmatter consistency across Module 2

All section files in Module 2 SHALL have consistent frontmatter: same `chapter` value, sequential `section` values, valid `createdTime` format, and `layout: doc`.

#### Scenario: All frontmatter fields are consistent

- **WHEN** frontmatter of all Module 2 section files is compared
- **THEN** `chapter` SHALL be 2 for all files, `section` values SHALL follow the pattern "2-M", and `createdTime` SHALL be in ISO 8601 with +08:00 timezone

<!-- @trace
source: ch2-editorial-audit
updated: 2026-04-14
code:
  - .vitepress/config.mts
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/guess-number-simple.md
  - docs/challenge/perfect-number.md
  - docs/challenge/inverted-triangle.md
  - docs/challenge/star-rectangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/tutor/py/index.md
  - docs/challenge/pair-count.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/2-4.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/challenge/arithmetic-sum.md
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/challenge/number-pyramid.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/challenge/star-diamond.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/digital-root.md
  - docs/tutor/py/ch2/2-3.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/challenge/star-square.md
  - docs/challenge/gcd-euclid.md
  - docs/tutor/py/ch2/index.md
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-staircase.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖八.png
-->
---
### Requirement: Module 2 sections SHALL NOT use Python features before they are introduced anywhere in Ch1 or earlier Ch2 sections

Every Python feature used in any code block, hint, or example inside `docs/tutor/py/ch2/*.md` SHALL have been formally introduced (with a teaching block, NOTE/TIP, or dedicated subsection) in either Chapter 1 (`docs/tutor/py/ch1/*.md`) OR an earlier section of Chapter 2 (`docs/tutor/py/ch2/*.md` whose section number is lower than the current file's section number).

The cross-chapter audit SHALL specifically verify the following features are introduced before first use:

| Feature | First-use file | Required introduction location |
| ------- | -------------- | ------------------------------ |
| String concatenation `+` (str + str) | first appearance in any Ch2 file | Ch1 1-2 (per `python-ch1-content` Section 1-2 string operator subsection) |
| String repetition `*` (str * int) | first appearance in any Ch2 file | Ch1 1-2 (per `python-ch1-content` Section 1-2 string operator subsection) |
| Escape character `\t` in string literal | Ch2 2-4 multiplication-table example | Ch2 2-4 NOTE block before first `\t` usage (per `python-ch2-2-4-content`) |
| Escape character `\n` in string literal | first appearance in any Ch2 file | mentioned in the `\t` NOTE block as a sibling escape character, OR a dedicated NOTE if it appears before the `\t` example |
| f-string syntax `f"..."` | Ch2 2-4 multiplication-table example | Ch2 2-4 NOTE block before first f-string usage (per `python-ch2-2-4-content`) |
| f-string format spec `:N` (width padding) | Ch2 2-4 multiplication-table example | Ch2 2-4 f-string NOTE block (per `python-ch2-2-4-content`) |

The audit SHALL flag any Ch2 file that uses one of these features without the corresponding introduction being present at or before the use site.

#### Scenario: String concatenation in Ch2 has Ch1 1-2 introduction

- **WHEN** any Ch2 section file contains a code block, hint, or example that uses string `+` to concatenate two strings
- **AND** Ch1 1-2 has been audited for the string-operator subsection required by `python-ch1-content`
- **THEN** the audit SHALL pass for that Ch2 file's string-concatenation usage

#### Scenario: String repetition in Ch2 has Ch1 1-2 introduction

- **WHEN** any Ch2 section file contains `"<string>" * <int>` (string repetition by integer)
- **AND** Ch1 1-2 has been audited for the string-operator subsection required by `python-ch1-content`
- **THEN** the audit SHALL pass for that Ch2 file's string-repetition usage

#### Scenario: \t escape character in Ch2 has 2-4 introduction

- **WHEN** Ch2 2-4 contains a code block using the `\t` escape character
- **AND** Ch2 2-4 contains the NOTE block required by `python-ch2-2-4-content`
- **THEN** the audit SHALL pass for the `\t` usage

#### Scenario: f-string in Ch2 has 2-4 introduction

- **WHEN** Ch2 2-4 contains a code block using f-string syntax `f"..."`
- **AND** Ch2 2-4 contains the NOTE block required by `python-ch2-2-4-content`
- **THEN** the audit SHALL pass for the f-string usage

#### Scenario: Audit fails on missing introduction

- **WHEN** any Ch2 file uses one of the listed features
- **AND** the required introduction location does not contain the feature's introduction
- **THEN** the audit SHALL report a Critical violation identifying the file, line, and feature

##### Example: violation report

| File | Line | Feature | Status |
| ---- | ---- | ------- | ------ |
| `docs/tutor/py/ch2/2-4.md` | 461 | f-string `f"{i*j:4}"` | requires NOTE block before line 461 |
| `docs/tutor/py/ch2/2-4.md` | 170 | escape `\t` | requires NOTE block before line 170 |
| `docs/tutor/py/ch2/2-4.md` | 56 | string repetition `"*" * i` | requires Ch1 1-2 introduction (see `python-ch1-content`) |

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/
  - docs/tutor/py/ch1/
-->

---
### Requirement: Module 2 hints SHALL NOT introduce syntax that is forbidden by per-section specs

The cross-chapter audit SHALL verify that the "老師的提示" NOTE blocks in any Ch2 section do not contain Python syntax that has been explicitly forbidden in that section's per-section spec (e.g., `python-ch2-2-4-content` forbids unpacking `*`, list/dict/tuple literals, comprehensions, `def`, `lambda`, slicing, walrus in 2-4 hints).

#### Scenario: Forbidden syntax in hint triggers audit failure

- **WHEN** the cross-chapter audit scans a Ch2 file's "老師的提示" NOTE blocks
- **AND** a hint contains syntax forbidden by that section's per-section spec
- **THEN** the audit SHALL report a Critical violation citing the per-section spec and the forbidden syntax

<!-- @trace
source: review-ch1-ch2-coherence
updated: 2026-05-06
code:
  - docs/tutor/py/ch2/
-->
