## ADDED Requirements

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

### Requirement: Math support is enabled via markdown config

The VitePress configuration in `.vitepress/config.mts` SHALL set `markdown.math` to `true` to enable LaTeX math rendering.

#### Scenario: Config enables math

- **WHEN** `.vitepress/config.mts` is inspected
- **THEN** the `markdown` configuration object SHALL contain `math: true`

### Requirement: MathJax package is installed as devDependency

The `package.json` SHALL list `markdown-it-mathjax3` (version `^4`) as a `devDependency`.

#### Scenario: Package present in devDependencies

- **WHEN** `package.json` is inspected
- **THEN** `devDependencies` SHALL contain `markdown-it-mathjax3` with version constraint `^4`
