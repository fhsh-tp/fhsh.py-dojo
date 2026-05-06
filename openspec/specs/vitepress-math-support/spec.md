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