# python-ch2-enhanced-exercises Specification

## Purpose

Defines requirements for adding and reformatting APCS literacy-style practice problems in sections 1-3, 1-4, 2-1, 2-2, 2-3, and 2-4. Each section receives additional 「自己動手試試」problems and/or reformatted existing exercises, with corresponding challenge files.

## Requirements

### Requirement: Section 2-1 receives 2-4 additional APCS-style practice problems

Section 2-1 (`docs/tutor/py/ch2/2-1.md`) SHALL have 2 to 4 new practice problems appended to its existing 「自己動手試試」section. Each new problem SHALL follow the APCS beginner transition format:

1. Problem title as H3 heading
2. `<ChallengeLink slug="..." />` component
3. 「題目說明」in conversational tone describing a scenario involving `for` loops with `range()`
4. 「輸入格式」section with line-by-line input specification
5. 「輸出格式」section with exact output requirements
6. At least 2 sample I/O pairs in table format
7. Simple constraints (e.g., 1 ≤ N ≤ 100)
8. `> [!NOTE] 老師的提示` with a strategic hint

**Recommended topics** (implementer SHALL select from these or create equivalents of similar difficulty):
- 等差數列求和（arithmetic sequence sum using for loop with step）
- 數字金字塔（print numbers 1 to N in pyramid pattern using for loop）
- 星星正方形（print N×N square of stars）
- 倒數偶數（print even numbers from N down to 2 using range with negative step）

Each new problem SHALL have a corresponding `docs/challenge/<slug>.md` file with valid YAML frontmatter.

#### Scenario: 2-1 has 8-10 total practice problems after enhancement

- **WHEN** all ChallengeLink components in section 2-1 are counted
- **THEN** the total SHALL be between 8 and 10 (existing 6 + new 2-4)

#### Scenario: New problems follow APCS transition format

- **WHEN** the newly added problems in 2-1 are parsed
- **THEN** each SHALL contain separate 「輸入格式」and「輸出格式」headings, at least 2 sample I/O pairs, and a constraint statement


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-2 receives 3-5 additional APCS-style practice problems

Section 2-2 (`docs/tutor/py/ch2/2-2.md`) SHALL have 3 to 5 new practice problems appended to its existing 「自己動手試試」section. Format requirements are identical to those in the 2-1 enhancement requirement above.

**Recommended topics** (implementer SHALL select from these or create equivalents):
- 猜數字遊戲簡化版（simplified number guessing: while loop reads guesses until correct, output guess count）
- 最大公因數 GCD（Euclidean algorithm using while loop）
- 數位根（digital root: repeatedly sum digits until single digit remains）
- 完美數判斷（determine if a number is perfect: sum of proper divisors equals the number）
- Collatz 進階版（count steps for multiple inputs, extending the existing collatz-steps challenge）

Each new problem SHALL have a corresponding `docs/challenge/<slug>.md` file.

#### Scenario: 2-2 has 6-8 total practice problems after enhancement

- **WHEN** all ChallengeLink components in section 2-2 are counted
- **THEN** the total SHALL be between 6 and 8 (existing 3 + new 3-5)


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-3 receives 2-4 additional APCS-style practice problems

Section 2-3 (`docs/tutor/py/ch2/2-3.md`) SHALL have 2 to 4 new practice problems appended to its existing 「自己動手試試」section. Format requirements are identical to those in the 2-1 enhancement requirement above.

**Recommended topics** (implementer SHALL select from these or create equivalents):
- 質數判斷（prime number check using for loop with break）
- 完美數進階（find all perfect numbers in range 1 to N using nested logic with continue）
- 最小因數搜尋進階版（find smallest prime factor using break, extending first-divisor）
- 密碼強度進階版（multi-criteria password validation with continue for skipping checks）

Each new problem SHALL have a corresponding `docs/challenge/<slug>.md` file.

#### Scenario: 2-3 has 8-10 total practice problems after enhancement

- **WHEN** all ChallengeLink components in section 2-3 are counted
- **THEN** the total SHALL be between 8 and 10 (existing 6 + new 2-4)


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: All enhanced exercise challenge files follow the standard format

Every new challenge file created for the 2-1/2-2/2-3 enhancement SHALL follow the established challenge file format:

```yaml
layout: challenge
id: <sequential integer, continuing from highest existing ID>
title: <problem title in Traditional Chinese>
difficulty: easy|medium|hard
tags: [relevant tags]
algorithm: <algorithm slug>
testcase_count: <number of test cases, minimum 5>
params:
  <param_name>:
    type: int|string|float
    min: <minimum value>
    max: <maximum value>
generator: |
  <Python code that generates test cases>
starter_code: |
  <Python code template for students>
chapter: ch2
description: <one-line description>
```

The `generator` code SHALL produce valid test cases that cover:
- Minimum boundary value
- Maximum boundary value
- At least 2 typical cases
- At least 1 edge case (if applicable)

The `starter_code` SHALL contain only `input()` calls and print placeholders — it SHALL NOT contain the solution.

#### Scenario: Challenge IDs are sequential with no gaps

- **WHEN** all challenge files in `docs/challenge/` are sorted by `id`
- **THEN** the IDs SHALL form a continuous sequence with no gaps or duplicates

#### Scenario: Each challenge has at least 5 test cases

- **WHEN** a challenge file's `testcase_count` is read
- **THEN** the value SHALL be at least 5

#### Scenario: Generator code produces valid output

- **WHEN** the `generator` code is executed
- **THEN** it SHALL produce valid input/output pairs that match the problem's specification


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: New exercises are appended without modifying existing content

The new practice problems SHALL be appended at the end of each section's existing 「自己動手試試」block, after all currently existing practice problems. The existing content (text, code blocks, ChallengeLinks) in sections 2-1, 2-2, and 2-3 SHALL NOT be modified, deleted, or reordered.

#### Scenario: Existing content is preserved

- **WHEN** the diff of 2-1.md, 2-2.md, and 2-3.md is reviewed
- **THEN** the diff SHALL show only additions (new lines) at the end of the 「自己動手試試」section, with zero deletions or modifications to existing lines

#### Scenario: New problems appear after existing ones

- **WHEN** ChallengeLink components are listed in document order
- **THEN** all existing ChallengeLinks SHALL appear before all newly added ChallengeLinks


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: APCS beginner transition format template

All practice problems in sections 1-3, 1-4, 2-1, 2-2, 2-3, and 2-4 — including both existing exercises and any exercises added in future changes — SHALL follow the APCS literacy exercise format defined in the `apcs-literacy-exercise-template` spec. "Practice problems" excludes Judge 解題實戰 teaching worked-examples (see `apcs-literacy-exercise-template` spec for the exclusion list).

This replaces the previous "APCS beginner transition format" template. The key differences from the previous format are:

1. **問題情境** replaces **題目說明**: The narrative SHALL be 150-300 Chinese characters (up from 2-3 sentences) and SHALL use a named character in a real-world scenario
2. **🔍 思考引導** is a new mandatory section: Each exercise SHALL include at least 1 scaffold element (Math Expression, Partial Flowchart, or Step Decomposition) as defined in the `apcs-literacy-exercise-template` spec
3. **範例說明** is a new mandatory section: Each exercise SHALL include a step-by-step computation trace of the most instructive example
4. The scope expands from "sections 2-1, 2-2, and 2-3" to "sections 1-3, 1-4, 2-1, 2-2, 2-3, and 2-4"

All other requirements from the `apcs-literacy-exercise-template` spec (input format, output format, sample I/O pairs, teacher hints) SHALL apply.

#### Scenario: Practice problem follows APCS literacy format

- **WHEN** a practice problem in sections 1-3, 1-4, 2-1, 2-2, 2-3, or 2-4 is parsed
- **THEN** it SHALL contain all mandatory sections defined in the `apcs-literacy-exercise-template` spec: 問題情境 (150-300 chars with named character), 思考引導 (with at least 1 scaffold), 輸入格式 (with constraints), 輸出格式, at least 2 sample I/O pairs, 範例說明 (with numbered steps), and 老師的提示

#### Scenario: Existing short-format exercises are upgraded

- **WHEN** an exercise that previously used the short format (1-2 sentence description + hint + ChallengeLink) is found in sections 2-1, 2-2, or 2-3
- **THEN** it SHALL be rewritten to the full APCS literacy format with all mandatory sections

#### Scenario: Section 1-3 tier format is replaced

- **WHEN** section 1-3's exercises are examined after the change
- **THEN** the tier system (★☆☆ through ★★★★) SHALL be removed and all exercises SHALL use the APCS literacy format instead

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