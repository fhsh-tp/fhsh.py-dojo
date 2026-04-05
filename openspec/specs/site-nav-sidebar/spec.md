## ADDED Requirements

### Requirement: nav.yml defines static top navigation

A YAML file at `.vitepress/nav.yml` SHALL define the VitePress top navigation array. `config.mts` SHALL load this file at build time using `js-yaml` (`yaml.load(fs.readFileSync(…))`) and assign it to `themeConfig.nav`.

The `nav.yml` SHALL define the following structure:

```yaml
- text: 教學
  items:
    - text: Python 自學
      link: /tutor/py/
    - text: 演算法
      link: /tutor/alg/
    - text: 資料結構
      link: /tutor/ds/
- text: 挑戰題庫
  link: /challenge/
```

#### Scenario: nav.yml is loaded by config.mts

- **WHEN** VitePress builds the site
- **THEN** the top navigation SHALL display the items defined in `.vitepress/nav.yml`

#### Scenario: nav.yml file is missing

- **WHEN** `.vitepress/nav.yml` does not exist
- **THEN** `config.mts` SHALL fall back to an empty array `[]` without throwing an error


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

---

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

## Requirements


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

### Requirement: nav.yml defines static top navigation

A YAML file at `.vitepress/nav.yml` SHALL define the VitePress top navigation array. `config.mts` SHALL load this file at build time using `js-yaml` (`yaml.load(fs.readFileSync(…))`) and assign it to `themeConfig.nav`.

The `nav.yml` SHALL define the following structure:

```yaml
- text: 教學
  items:
    - text: Python 自學
      link: /tutor/py/
    - text: 演算法
      link: /tutor/alg/
    - text: 資料結構
      link: /tutor/ds/
- text: 挑戰題庫
  link: /challenge/
```

#### Scenario: nav.yml is loaded by config.mts

- **WHEN** VitePress builds the site
- **THEN** the top navigation SHALL display the items defined in `.vitepress/nav.yml`

#### Scenario: nav.yml file is missing

- **WHEN** `.vitepress/nav.yml` does not exist
- **THEN** `config.mts` SHALL fall back to an empty array `[]` without throwing an error

---
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