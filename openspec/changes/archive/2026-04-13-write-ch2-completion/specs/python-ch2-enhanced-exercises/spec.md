## ADDED Requirements

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

---

### Requirement: New exercises are appended without modifying existing content

The new practice problems SHALL be appended at the end of each section's existing 「自己動手試試」block, after all currently existing practice problems. The existing content (text, code blocks, ChallengeLinks) in sections 2-1, 2-2, and 2-3 SHALL NOT be modified, deleted, or reordered.

#### Scenario: Existing content is preserved

- **WHEN** the diff of 2-1.md, 2-2.md, and 2-3.md is reviewed
- **THEN** the diff SHALL show only additions (new lines) at the end of the 「自己動手試試」section, with zero deletions or modifications to existing lines

#### Scenario: New problems appear after existing ones

- **WHEN** ChallengeLink components are listed in document order
- **THEN** all existing ChallengeLinks SHALL appear before all newly added ChallengeLinks

---

### Requirement: APCS beginner transition format template

All new practice problems for sections 2-1, 2-2, 2-3, and 2-4 SHALL follow this format template:

```
### [題目名稱]

<ChallengeLink slug="[slug]" />

**題目說明**：[保留對話語氣的敘事情境，2-3 句描述問題背景與要求]

**輸入格式**：
第一行：[逐行說明每一行的輸入內容與型別] (限制：[值域範圍，如 1 ≤ N ≤ 100])

**輸出格式**：
[精確描述輸出內容、格式、換行規則]

**範例一**：

| 輸入 | 輸出 |
|------|------|
| [sample input] | [sample output] |

**範例二**：

| 輸入 | 輸出 |
|------|------|
| [sample input] | [sample output] |

> [!NOTE] 老師的提示
> [1-2 句策略性提示，不含完整解法]
```

#### Scenario: Practice problem follows template

- **WHEN** a new practice problem is added to sections 2-1, 2-2, 2-3, or 2-4
- **THEN** it SHALL contain all template sections: 題目說明, 輸入格式 (with constraints), 輸出格式, at least 2 sample I/O pairs, and a teacher hint
