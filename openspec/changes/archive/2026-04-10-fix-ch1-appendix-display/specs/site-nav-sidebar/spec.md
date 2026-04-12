## MODIFIED Requirements

### Requirement: buildTutorSidebar generates multi-sidebar at build time

`config.mts` SHALL export a `buildTutorSidebar(docsDir: string)` function that scans the `docs/tutor/` directory tree and returns a VitePress multi-sidebar object (keyed by URL path prefix).

The function SHALL:
1. Enumerate all subject directories directly under `docs/tutor/`
2. For each subject, enumerate all `chN/` directories
3. For each chapter, collect `.md` files excluding `index.md` AND excluding `appendix.md`, sorted alphabetically by filename
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

#### Scenario: appendix.md is excluded from sidebar

- **WHEN** a chapter directory contains an `appendix.md` file
- **THEN** `buildTutorSidebar()` SHALL NOT include `appendix.md` in the sidebar items for that chapter

## ADDED Requirements

### Requirement: Inline appendix headings are excluded from VitePress outline

Tutorial section files that contain an Image Specification Appendix section SHALL use an HTML `<h2>` tag instead of a Markdown `##` heading for the appendix title. This ensures VitePress excludes the appendix heading from the page outline (right-side table of contents).

The appendix content below the `<h2>` tag SHALL remain visible in the page body. Only the heading is changed from Markdown to HTML to prevent outline pollution.

#### Scenario: Appendix heading not in page outline

- **WHEN** a user views `1-3.md` or `1-4.md` in the browser
- **THEN** the right-side page outline SHALL NOT contain an "Image Specification Appendix" entry

#### Scenario: Appendix content remains visible

- **WHEN** a user scrolls to the bottom of `1-3.md` or `1-4.md`
- **THEN** the Image Specification Appendix content SHALL still be visible on the page
