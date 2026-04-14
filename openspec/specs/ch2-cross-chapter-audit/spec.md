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

All challenge files referenced from Module 2 sections SHALL have sequential IDs with no gaps or duplicates when sorted numerically. Module 2 challenge IDs SHALL form a contiguous block that starts immediately after Module 1's last ID.

#### Scenario: Challenge IDs form continuous sequence

- **WHEN** all challenge IDs referenced from Module 2 are collected and sorted
- **THEN** the IDs SHALL form a continuous integer sequence with no gaps

#### Scenario: Per-chapter ID blocks are contiguous

- **WHEN** challenge IDs are grouped by chapter and sorted
- **THEN** each chapter's IDs SHALL form a contiguous block with no interleaving from other chapters


<!-- @trace
source: renumber-challenge-ids
updated: 2026-04-15
code:
  - docs/tutor/py/ch2/2-4.md
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/number-reverse.md
  - docs/challenge/date-validator.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/sign-check.md
  - docs/challenge/odd-even.md
  - docs/challenge/vending-change.md
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/repeat-greeting.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/factorial.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/target-sum.md
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/first-divisor.md
  - docs/challenge/range-sum.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/countdown.md
  - docs/challenge/password-check.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/number-sum.md
  - docs/challenge/sum-skip-fives.md
-->

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