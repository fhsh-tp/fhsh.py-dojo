## ADDED Requirements

### Requirement: Challenge body math statements use LaTeX

The Markdown body of a challenge page — everything after the closing frontmatter delimiter — SHALL express mathematical statements as LaTeX inside MathJax delimiters. A mathematical statement is a constraint, an arithmetic expression, an assignment, an exponent, a signed numeric value, or a variable letter standing for a quantity in the problem.

Text that appears verbatim in the challenge's input or output SHALL remain in backticks and SHALL NOT be converted. Numbers that are part of ordinary prose rather than part of an expression SHALL remain plain text.

#### Scenario: A range constraint is written as LaTeX

- **WHEN** a challenge body states the bounds of an input value
- **THEN** the bounds SHALL be written as an inequality inside `$...$`
- **AND** the Unicode characters `≤` and `≥` SHALL NOT appear in the body

##### Example: notation decision table

| Context | Source form | Required form | Rule |
| ------- | ----------- | ------------- | ---- |
| Range constraint | `1 ≤ T ≤ 3` | `$1 \le T \le 3$` | mathematical statement |
| Constraint wrongly in backticks | `` `1 <= n <= 1000` `` | `$1 \le n \le 1000$` | mathematical statement |
| Arithmetic expression | `N×(N−1)×…×(N−M+1)` | `$N \times (N-1) \times \cdots \times (N-M+1)$` | mathematical statement |
| Assignment | `以 N=10 為例` | `以 $N = 10$ 為例` | mathematical statement |
| Exponent | `2^(D−1)` | `$2^{D-1}$` | mathematical statement |
| Large number | `1000000000` | `$10^9$` | mathematical statement |
| Signed value in a table cell | `−2` | `$-2$` | mathematical statement |
| Variable letter in prose | `` 輸出 `n` 行 `` | `輸出 $n$ 行` | mathematical statement |
| Input line format | `` `D I` `` | `` `D I` `` | verbatim input token |
| Output string | `` `Two Real Roots` `` | `` `Two Real Roots` `` | verbatim output token |
| Literal glyph in a diagram | `` `·` `` | `` `·` `` | verbatim token |
| Prose number | `去掉尾端的 0 得到 9` | `去掉尾端的 0 得到 9` | not an expression |
| Tilde range | `1~9` | `1~9` | Chinese typography, not a math symbol |

### Requirement: Chinese words are not placed inside math delimiters

When a formula mixes Chinese words with mathematical notation, only the mathematical fragment SHALL be wrapped in math delimiters. Chinese words SHALL remain outside the delimiters and SHALL NOT be wrapped in `\text{}`.

#### Scenario: A formula containing Chinese terms is split

- **WHEN** a challenge body contains a formula whose operands are named in Chinese
- **THEN** only the mathematical fragment SHALL be wrapped in `$...$`

##### Example: BMI formula

- **GIVEN** the source text `BMI = 體重(kg) / 身高(m)²`
- **WHEN** the page is converted
- **THEN** the result SHALL be `BMI = 體重(kg) / 身高(m)$^2$`
- **AND** the result SHALL NOT be `$\text{BMI} = \dfrac{\text{體重}}{\text{身高}^2}$`

### Requirement: Currency dollar signs are escaped

A dollar sign used as a currency symbol in a challenge body SHALL be escaped as `\$` so that it cannot pair with a math delimiter on the same page.

#### Scenario: A price is written in a challenge body

- **WHEN** a challenge body states a price such as 150 dollars
- **THEN** the dollar sign SHALL be written as `\$`
- **AND** an unescaped dollar sign that is not part of a matched `$...$` or `$$...$$` pair SHALL NOT remain in the body

### Requirement: Frontmatter is not altered by notation changes

Converting a challenge body to LaTeX notation SHALL NOT modify any frontmatter field. The `params`, `generator`, `testcase_plan`, and `reference_solution` fields feed the encrypted testcase pool hash, so altering them would require regenerating the pools and the WASM artifacts.

#### Scenario: A converted page keeps its frontmatter byte-identical

- **WHEN** a challenge page is converted to LaTeX notation
- **THEN** every line from the opening frontmatter delimiter through the closing frontmatter delimiter SHALL be unchanged
- **AND** no testcase pool or WASM rebuild SHALL be required

##### Example: which lines may change

- **GIVEN** `docs/challenge/pair-count.md`, whose closing frontmatter delimiter is on line 36 and whose body starts on line 37
- **WHEN** the page is converted
- **THEN** every changed line reported by a line-level diff SHALL have a line number of 37 or greater
- **AND** the SHA-256 of the frontmatter slice SHALL be identical before and after

### Requirement: A test enforces the notation rules

The test suite run by the project's test command SHALL fail when any challenge body violates the notation rules. The check SHALL classify forbidden symbols into two tiers.

Tier A symbols — `≤`, `≥`, `＜`, `＞`, and the ASCII sequences `<=` and `>=` — SHALL be forbidden everywhere in the body, including inside inline code spans, because in a challenge body they can only express a constraint.

Tier B symbols — `×`, `−`, `·`, `≠`, `≈`, `⌊`, `⌋`, `⌈`, `⌉`, `√`, `∑`, `∞`, `²`, `³`, `⁴`, `ⁿ` — SHALL be forbidden in prose but SHALL be permitted inside inline code spans, because they can denote a literal glyph.

The scan surface SHALL be computed in this order: take the body after the closing frontmatter delimiter, remove fenced code blocks, remove image syntax, then remove matched `$...$` and `$$...$$` spans. Any other order produces false positives.

A line preceded by an HTML comment containing `latex-lint-ignore-next-line` SHALL be excluded from the check.

#### Scenario: A tier A symbol fails the test

- **WHEN** a challenge body contains `1 <= n <= 1000` inside an inline code span
- **THEN** the test SHALL fail
- **AND** the failure message SHALL name the file, the line number, and the offending symbol

#### Scenario: A tier B symbol inside a code span passes

- **WHEN** a challenge body refers to a diagram glyph as `` `·` ``
- **THEN** the test SHALL pass

#### Scenario: Every violation is reported

- **WHEN** three challenge bodies each contain a forbidden symbol
- **THEN** the test SHALL report all three
- **AND** the test SHALL NOT stop at the first violation

##### Example: the pre-conversion baseline

- **GIVEN** the 53 unconverted challenge pages present before this change
- **WHEN** the test runs
- **THEN** the failure list SHALL contain 53 entries, one per file
- **AND** the list SHALL include `prize-order-code`, `movie-ticket`, and `print-farm-schedule`
- **AND** the entry for `print-farm-schedule` SHALL cite its six prose `≤` occurrences and SHALL NOT cite its `` `·` `` code span

#### Scenario: The ignore marker suppresses one line

- **WHEN** a line is immediately preceded by an HTML comment containing `latex-lint-ignore-next-line`
- **THEN** that line SHALL be excluded from the check
- **AND** the following lines SHALL still be checked

### Requirement: The authoring guide documents the notation rules

The challenge authoring guide SHALL document the notation decision table in the section describing the Markdown body structure, so that an author sees the rules while writing rather than after the test fails.

#### Scenario: An author consults the authoring guide

- **WHEN** an author reads the section of the authoring guide that describes the Markdown body structure
- **THEN** the section SHALL contain the notation decision table
- **AND** each row of the table SHALL correspond to a case that occurs in an existing challenge page

##### Example: rows that must be traceable to a real page

| Table row | Challenge page it is drawn from |
| --------- | ------------------------------- |
| Range constraint | `prize-order-code` |
| Constraint wrongly in backticks | `ap-layout-plan` |
| Arithmetic expression | `rank-code-backfill` |
| Exponent | `bmi-classifier` |
| Input line format stays in backticks | `pinball-track-predict` |
| Output string stays in backticks | `quadratic-discriminant` |
| Literal glyph stays in backticks | `print-farm-schedule` |
| Tilde range stays plain | `movie-ticket` |
