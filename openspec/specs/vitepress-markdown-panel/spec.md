# vitepress-markdown-panel Specification

## Purpose

Defines the VitePress-based challenge page layout where challenge pages use a custom `layout: challenge` in frontmatter, the left panel renders native VitePress markdown via the `<Content />` component, and all challenge metadata resides entirely in frontmatter with no external TOML files.

## Requirements

### Requirement: Challenge pages use custom VitePress layout

Challenge markdown pages SHALL set `layout: challenge` in frontmatter instead of `layout: false`. The VitePress `Layout.vue` SHALL render `ChallengeView` when `frontmatter.layout === 'challenge'`, bypassing the DefaultTheme layout. The `ChallengeView` component SHALL be registered as the layout entry point, not as inline page content.

Challenge page data SHALL be sourced exclusively from Markdown frontmatter. The active codebase SHALL NOT contain any loader or composable that references TOML-based challenge files (`*.toml`) or the removed `parseChallengeMeta` WASM export.

#### Scenario: Challenge page renders with custom layout

- **WHEN** a user navigates to a challenge page with `layout: challenge` in frontmatter
- **THEN** `Layout.vue` renders `ChallengeView` directly without DefaultTheme wrapping

#### Scenario: Non-challenge pages are unaffected

- **WHEN** a user navigates to any page without `layout: challenge`
- **THEN** `Layout.vue` renders the DefaultTheme layout as before

#### Scenario: No TOML-era challenge loader exists

- **WHEN** the codebase is searched for composables that import TOML challenge files via `import.meta.glob`
- **THEN** zero results SHALL be found


<!-- @trace
source: restore-build-and-static-verification
updated: 2026-04-04
code:
  - .vitepress/theme/views/ChallengeView.vue
  - requirements.txt
  - .vitepress/theme/composables/useChallengeRunner.ts
  - .vitepress/theme/components/editor/CodeEditor.vue
  - scripts/generate-key-material.ts
  - .vitepress/theme/composables/useRemoteChallenge.ts
  - testcase-generator/src/judge.rs
  - testcase-generator/src/lib.rs
  - tsconfig.node.json
  - package.json
  - testcase-generator/src/pool.rs
  - tsconfig.app.json
  - README.md
  - .vitepress/theme/workers/pyodide.worker.ts
  - scripts/generate-pools.ts
  - .github/workflows/release.yml
  - .vitepress/plugins/strip-generator.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
-->

---
### Requirement: Left panel renders VitePress native markdown

The `ProblemPanel` component SHALL render the current page's markdown content using VitePress's `<Content />` component. The challenge `.md` file's body (after frontmatter) SHALL contain the full problem description in standard Markdown. No description text SHALL be stored in the TOML file.

#### Scenario: Problem description is rendered from page content

- **WHEN** a challenge page is loaded
- **THEN** the left panel displays the formatted markdown from the `.md` file body using VitePress's rendering pipeline (including syntax highlighting, prose styles, etc.)

#### Scenario: Description updates without WASM changes

- **WHEN** a challenge author edits the `.md` file body
- **THEN** the updated description is rendered on the next page load without any TOML or WASM changes


<!-- @trace
source: markdown-panel-and-python-generator
updated: 2026-03-13
code:
  - docs/index.md
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/Layout.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useWasm.ts
  - .vitepress/theme/stores/challenge.ts
  - .vitepress/theme/workers/pyodide.worker.ts
  - package.json
  - docs/shared/challenge.data.ts
tests:
  - .vitepress/theme/__tests__/useWasm.spec.ts
  - .vitepress/theme/__tests__/challenge.store.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-generate.spec.ts
-->

---
### Requirement: Challenge metadata lives entirely in frontmatter

All challenge data SHALL reside in the `.md` file only — no TOML files SHALL exist. The frontmatter SHALL contain: `id`, `title`, `difficulty`, `tags`, `algorithm`, `testcase_count`, `params` (object), `generator` (Python string), and `starter_code` (Python string). `ChallengeView` SHALL read all challenge data from `frontmatter` (via `useData()`) rather than from any external file. The `import.meta.glob` TOML loading logic in `ChallengeView` SHALL be removed.

#### Scenario: AppHeader reads title from frontmatter

- **WHEN** a challenge page loads
- **THEN** the AppHeader displays the title from `frontmatter.title` without waiting for WASM generation

#### Scenario: Data loader continues to work from frontmatter

- **WHEN** `challenge.data.ts` builds the challenge catalogue
- **THEN** it reads all metadata from `.md` frontmatter fields as before (no TOML parsing at build time)

#### Scenario: No TOML files exist in the repository

- **WHEN** the migration is complete
- **THEN** the `.vitepress/theme/challenges/` directory and all `.toml` files are deleted

<!-- @trace
source: markdown-panel-and-python-generator
updated: 2026-03-13
code:
  - docs/index.md
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/Layout.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useWasm.ts
  - .vitepress/theme/stores/challenge.ts
  - .vitepress/theme/workers/pyodide.worker.ts
  - package.json
  - docs/shared/challenge.data.ts
tests:
  - .vitepress/theme/__tests__/useWasm.spec.ts
  - .vitepress/theme/__tests__/challenge.store.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-generate.spec.ts
-->

---
### Requirement: ProblemPanel code blocks render with VitePress styles

The `ProblemPanel` wrapper element SHALL include the `vp-doc` CSS class alongside the existing `prose` classes. This SHALL ensure VitePress's built-in code block CSS (including the copy button positioning and appearance) applies correctly within the panel.

The copy button injected by VitePress's markdown transformer SHALL be `position: absolute` inside the code block container, NOT rendered in normal document flow. No visible gap SHALL appear between a paragraph and the code block that follows it due to an unstyled copy button.

#### Scenario: Copy button is visible and correctly positioned

- **WHEN** the challenge problem description contains a fenced code block
- **THEN** a copy button is visible at the top-right corner of the code block (on hover or always-visible, per VitePress defaults)

#### Scenario: No layout gap above code block content

- **WHEN** a code block follows a paragraph (e.g., "**輸入：**") in the problem description
- **THEN** no abnormal vertical gap appears between the paragraph and the code block content

<!-- @trace
source: fix-problem-panel-code-block-styling
updated: 2026-03-13
-->

<!-- @trace
source: fix-problem-panel-code-block-styling
updated: 2026-03-13
code:
  - .vitepress/theme/components/challenge/ProblemPanel.vue
tests:
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->