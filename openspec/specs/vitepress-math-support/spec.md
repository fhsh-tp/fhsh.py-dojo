# vitepress-math-support Specification

## Purpose

TBD - created by archiving change 'setup-vitepress-mermaid-math'. Update Purpose after archive.

## Requirements

### Requirement: LaTeX math expressions render in Markdown

Markdown files containing inline math (`$...$`) and display math (`$$...$$`) syntax SHALL be rendered as formatted mathematical expressions in both the VitePress dev server and the production build output.

#### Scenario: Inline math renders correctly

- **WHEN** a Markdown file contains `$E = mc^2$` within a paragraph
- **THEN** the expression SHALL be rendered as a formatted inline math expression
- **AND** the raw LaTeX source text SHALL NOT be visible to the user

#### Scenario: Display math renders correctly

- **WHEN** a Markdown file contains a `$$...$$` block with LaTeX syntax such as `\frac{-b \pm \sqrt{b^2-4ac}}{2a}`
- **THEN** the expression SHALL be rendered as a centered block-level math expression

#### Scenario: Dollar signs in non-math contexts are not converted

- **WHEN** a Markdown file contains a dollar sign in a code block (e.g., `` `$variable` ``) or escaped with backslash (`\$`)
- **THEN** the dollar sign SHALL NOT be interpreted as math delimiter


<!-- @trace
source: setup-vitepress-mermaid-math
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - docs/challenge/quadratic-discriminant.md
  - docs/.vitepress/cache/deps/vue.js
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/challenge/password-check.md
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - package.json
  - docs/.vitepress/cache/deps/package.json
  - .vitepress/config.mts
-->

---
### Requirement: Math support is enabled via markdown config

The VitePress configuration in `.vitepress/config.mts` SHALL set `markdown.math` to `true` to enable LaTeX math rendering.

#### Scenario: Config enables math

- **WHEN** `.vitepress/config.mts` is inspected
- **THEN** the `markdown` configuration object SHALL contain `math: true`


<!-- @trace
source: setup-vitepress-mermaid-math
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - docs/challenge/quadratic-discriminant.md
  - docs/.vitepress/cache/deps/vue.js
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/challenge/password-check.md
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - package.json
  - docs/.vitepress/cache/deps/package.json
  - .vitepress/config.mts
-->

---
### Requirement: MathJax package is installed as devDependency

The `package.json` SHALL list `markdown-it-mathjax3` (version `^4`) as a `devDependency`.

#### Scenario: Package present in devDependencies

- **WHEN** `package.json` is inspected
- **THEN** `devDependencies` SHALL contain `markdown-it-mathjax3` with version constraint `^4`

<!-- @trace
source: setup-vitepress-mermaid-math
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - docs/challenge/quadratic-discriminant.md
  - docs/.vitepress/cache/deps/vue.js
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - docs/challenge/password-check.md
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - package.json
  - docs/.vitepress/cache/deps/package.json
  - .vitepress/config.mts
-->

---
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
