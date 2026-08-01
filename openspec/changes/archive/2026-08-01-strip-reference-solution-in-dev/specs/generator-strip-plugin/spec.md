## REMOVED Requirements

### Requirement: VitePress plugin strips generator field in production builds

**Reason**: Superseded by the answer-bearing-fields requirement below, which records that reference_solution has also been stripped in production builds since 2026-07-27 and unifies both fields plus the fail-loud post-strip assertions under one contract.

### Requirement: Plugin does not modify files in development mode

**Reason**: Superseded by the development-mode requirement below: reference_solution has no client-side consumer in any mode and leaked the full model solution through the dev server, so dev mode now strips it while continuing to pass generator through for the dev judging strategy.

## ADDED Requirements

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

### Requirement: Development mode strips reference_solution while passing generator through

When running vitepress dev, a serve-mode plugin instance SHALL strip only the `reference_solution` field from challenge frontmatter. The `generator` field and every other frontmatter field SHALL pass through with unchanged values so the dev judging strategy in useChallengeRunner can execute the generator at runtime. The post-strip assertions SHALL apply in serve mode too, parameterized to the serve-mode strip list, so an altered generator aborts the module transform with a thrown error instead of silently serving damaged frontmatter.

#### Scenario: Generator field available in dev mode

- **WHEN** vitepress dev is running and a challenge page module is served
- **THEN** frontmatter.generator SHALL contain the Python generator code exactly as written in the Markdown file

#### Scenario: reference_solution absent in dev mode

- **WHEN** vitepress dev is running and a challenge page module is served
- **THEN** the served module SHALL NOT contain the reference_solution key nor its Python content
