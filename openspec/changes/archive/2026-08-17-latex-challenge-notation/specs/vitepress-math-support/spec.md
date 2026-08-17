## ADDED Requirements

### Requirement: Inline math shares a line with surrounding text

An inline math expression SHALL be laid out on the same line as the text that surrounds it in the same paragraph. A paragraph containing inline math SHALL NOT grow one line taller per formula.

MathJax renders every expression as an `svg` element. The site's Tailwind preflight sets `svg { display: block }`, which makes each inline expression start its own line. The theme stylesheet SHALL restore the inline default for MathJax output only, scoped so that preflight continues to apply to every other `svg` on the site. Display math is unaffected by this rule, because MathJax sets `display: block` on the `mjx-container` element rather than on the `svg`.

#### Scenario: A sentence with several inline formulas stays on one line

- **WHEN** a rendered page contains a paragraph whose text includes three inline math expressions and whose text is short enough to fit one line
- **THEN** the paragraph SHALL occupy one line box
- **AND** the paragraph height SHALL be less than three times the computed line height

##### Example: bounds sentence

- **GIVEN** the source line `- 第一行：整數 $T$（$T \ge 1$），表示這一筆要預測幾次`
- **WHEN** the page is rendered in a browser
- **THEN** the list item SHALL render as a single line
- **AND** it SHALL NOT render as three lines with each formula on its own line

#### Scenario: The inline rule is scoped to MathJax output

- **WHEN** the computed style of an `svg` produced by MathJax is inspected
- **THEN** its `display` SHALL be `inline`

#### Scenario: Display math is still block-level

- **WHEN** a page contains a `$$...$$` block
- **THEN** the expression SHALL render centred on its own line
