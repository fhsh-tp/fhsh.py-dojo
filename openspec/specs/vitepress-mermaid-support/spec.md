# vitepress-mermaid-support Specification

## Purpose

TBD - created by archiving change 'setup-vitepress-mermaid-math'. Update Purpose after archive.

## Requirements

### Requirement: Mermaid code blocks render as SVG diagrams

Markdown files containing fenced code blocks with the `mermaid` language identifier SHALL be rendered as interactive SVG diagrams in both the VitePress dev server and the production build output.

#### Scenario: Flowchart renders in dev server

- **WHEN** a Markdown file contains a fenced code block with language `mermaid` and valid flowchart syntax
- **THEN** the VitePress dev server SHALL display the code block as a rendered SVG flowchart diagram
- **AND** the raw Mermaid source text SHALL NOT be visible to the user

#### Scenario: Mindmap renders in production build

- **WHEN** the VitePress site is built with `vitepress build`
- **AND** a Markdown file contains a fenced code block with language `mermaid` and valid mindmap syntax
- **THEN** the generated HTML SHALL contain a rendered SVG mindmap diagram

#### Scenario: Invalid Mermaid syntax shows error gracefully

- **WHEN** a Markdown file contains a fenced code block with language `mermaid` and invalid syntax
- **THEN** the page SHALL NOT crash
- **AND** an error indicator SHALL be displayed in place of the diagram


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
### Requirement: Mermaid plugin is registered via withMermaid wrapper

The VitePress configuration in `.vitepress/config.mts` SHALL use the `withMermaid()` wrapper from `vitepress-plugin-mermaid` to register the Mermaid rendering plugin.

#### Scenario: Config uses withMermaid wrapper

- **WHEN** `.vitepress/config.mts` is inspected
- **THEN** the default export SHALL be wrapped with `withMermaid()` from `vitepress-plugin-mermaid`


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
### Requirement: Mermaid packages are installed as devDependencies

The `package.json` SHALL list `vitepress-plugin-mermaid` and `mermaid` as `devDependencies`.

#### Scenario: Packages present in devDependencies

- **WHEN** `package.json` is inspected
- **THEN** `devDependencies` SHALL contain `vitepress-plugin-mermaid` and `mermaid`

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