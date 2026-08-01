# generator-strip-plugin Specification

## Purpose

Defines a VitePress/Vite plugin pair that strips answer-bearing fields from challenge Markdown frontmatter before they reach the browser, with fail-loud post-strip assertions. Production builds strip both `generator` (computes expected outputs) and `reference_solution` (a complete correct solution used only by build-time tests); development mode strips only `reference_solution`, passing `generator` through so the dev judging strategy can execute it at runtime.

## Requirements

### Requirement: Plugin operates on Markdown transform hook

The plugin SHALL use Vite's `transform` hook (or VitePress's markdown processing pipeline) to modify frontmatter. It SHALL only process files matching `**/challenge/**/*.md` to avoid affecting non-challenge Markdown content.

#### Scenario: Non-challenge Markdown unaffected

- **WHEN** a non-challenge Markdown file (e.g., `docs/index.md`) is processed
- **THEN** the plugin SHALL NOT modify its frontmatter

<!-- @trace
source: secure-challenge-pools
updated: 2026-04-02
code:
  - testcase-generator/src/lib.rs
  - testcase-generator/src/pool.rs
  - testcase-generator/Cargo.toml
  - .vitepress/plugins/strip-generator.ts
  - testcase-generator/src/judge.rs
  - scripts/generate-key-material.ts
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useChallengeRunner.ts
  - package.json
  - .vitepress/config.mts
  - testcase-generator/src/crypto.rs
  - scripts/generate-pools.ts
  - scripts/pool-key.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
-->

---
### Requirement: Production builds strip all answer-bearing frontmatter fields

A Vite plugin registered in .vitepress/config.mts SHALL intercept challenge Markdown module processing during production builds (vitepress build) and remove both the `generator` and `reference_solution` fields from YAML frontmatter before it reaches the client bundle. The plugin SHALL NOT modify the source .md files on disk. After stripping, the plugin SHALL re-parse the frontmatter and SHALL abort the build if a stripped field survives at any nesting depth, if any other field was altered, or if the frontmatter is no longer a valid YAML mapping.

#### Scenario: Answer fields absent in production page data

- **WHEN** vitepress build completes and a challenge page's JavaScript chunk is inspected
- **THEN** the page data SHALL contain neither a `generator` property nor a `reference_solution` property

#### Scenario: Other frontmatter fields preserved

- **WHEN** the plugin strips the answer-bearing fields
- **THEN** every other frontmatter field (such as title, params, starter_code, algorithm, testcase_count, testcase_plan, input_budget, difficulty, tags, id, layout, description) SHALL remain intact with unchanged values

#### Scenario: Assertion failure aborts the build

- **WHEN** the post-strip re-parse detects a surviving stripped field, an altered non-stripped field, or invalid YAML
- **THEN** the plugin SHALL throw so the build fails instead of publishing the bundle


<!-- @trace
source: strip-reference-solution-in-dev
updated: 2026-08-01
code:
  - .vitepress/plugins/strip-generator.ts
tests:
  - .vitepress/plugins/__tests__/strip-generator.spec.ts
-->

---
### Requirement: Development mode strips reference_solution while passing generator through

When running vitepress dev, a serve-mode plugin instance SHALL strip only the `reference_solution` field from challenge frontmatter. The `generator` field and every other frontmatter field SHALL pass through with unchanged values so the dev judging strategy in useChallengeRunner can execute the generator at runtime. The post-strip assertions SHALL apply in serve mode too, parameterized to the serve-mode strip list, so an altered generator aborts the module transform with a thrown error instead of silently serving damaged frontmatter.

#### Scenario: Generator field available in dev mode

- **WHEN** vitepress dev is running and a challenge page module is served
- **THEN** frontmatter.generator SHALL contain the Python generator code exactly as written in the Markdown file

#### Scenario: reference_solution absent in dev mode

- **WHEN** vitepress dev is running and a challenge page module is served
- **THEN** the served module SHALL NOT contain the reference_solution key nor its Python content

<!-- @trace
source: strip-reference-solution-in-dev
updated: 2026-08-01
code:
  - .vitepress/plugins/strip-generator.ts
tests:
  - .vitepress/plugins/__tests__/strip-generator.spec.ts
-->