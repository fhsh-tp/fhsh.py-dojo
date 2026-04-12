## MODIFIED Requirements

### Requirement: buildTutorSidebar generates multi-sidebar at build time

`config.mts` SHALL export a `buildTutorSidebar(docsDir: string)` function that scans the `docs/tutor/` directory tree and returns a VitePress multi-sidebar object (keyed by URL path prefix).

The function SHALL:
1. Enumerate all subject directories directly under `docs/tutor/`
2. For each subject, enumerate all `chN/` directories
3. For each chapter, collect `.md` files excluding `index.md`, sorted alphabetically by filename
4. Read each file's frontmatter `title` field using `gray-matter` or equivalent YAML front matter parser
5. Place `index.md` as the first item in each chapter's sidebar group
6. Generate sidebar keys for both `/tutor/<subject>/` (all chapters) and `/tutor/<subject>/chN/` (single chapter)

`themeConfig.sidebar` in `config.mts` SHALL be set to the return value of `buildTutorSidebar(srcDir)`.

#### Scenario: Python chapter generates correct sidebar

- **WHEN** `docs/tutor/py/ch1/` contains `index.md`, `1-1.md`, `1-2.md`, `1-3.md`
- **THEN** the sidebar at key `/tutor/py/ch1/` SHALL contain four items in the order: `index.md`, `1-1.md`, `1-2.md`, `1-3.md`, with titles taken from each file's frontmatter `title` field

#### Scenario: Empty tutor directory produces empty sidebar

- **WHEN** `docs/tutor/` contains no subject subdirectories (or they contain no `.md` files)
- **THEN** `buildTutorSidebar()` SHALL return an empty object `{}` without throwing an error

#### Scenario: No sidebar for challenge pages

- **WHEN** a user navigates to any page under `/challenge/`
- **THEN** no sidebar SHALL be rendered (the multi-sidebar object SHALL NOT contain a `/challenge/` key)

#### Scenario: appendix appears in sidebar before reference

- **WHEN** a chapter directory contains both `appendix.md` and `reference.md`
- **THEN** `buildTutorSidebar()` SHALL include `appendix.md` in the sidebar items, positioned before `reference.md` (alphabetical order: `a` < `r` ensures this naturally)

## REMOVED Requirements

### Requirement: appendix.md is excluded from sidebar

**Reason**: Appendix pages contain reference content (keywords table, image specification disclosure) that students benefit from navigating to directly via the sidebar. The original exclusion was overly conservative.
**Migration**: Remove the `f !== 'appendix.md'` filter condition from `buildTutorSidebar` in `.vitepress/config.mts`. The natural alphabetical sort (`a < r`) ensures `appendix.md` appears before `reference.md` automatically.

#### Scenario: appendix.md is no longer filtered out

- **WHEN** `docs/tutor/py/ch1/` contains `appendix.md`
- **THEN** `buildTutorSidebar()` SHALL include `appendix.md` as a sidebar item (this requirement is removed — the old exclusion behaviour SHALL NOT exist)
