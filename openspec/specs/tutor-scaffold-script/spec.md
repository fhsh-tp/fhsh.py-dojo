## ADDED Requirements

### Requirement: CLI script scaffolds a new tutor article file

A script at `scripts/new-tutor.ts` SHALL accept positional command-line arguments and generate a `docs/tutor/<subject>/<chapter>/<section>.md` file containing a valid frontmatter skeleton and Markdown body template.

The script SHALL accept the following arguments:
1. `<subject>` (required) — target subject directory name (e.g., `py`, `alg`, `ds`)
2. `<chapter>` (required) — chapter directory name in the format `chN` (e.g., `ch1`, `ch2`)
3. `<section>` (required) — section file name without `.md` (e.g., `1-1`, `index`)
4. `--title <string>` (optional) — display title; defaults to title-cased `<section>`
5. `--description <string>` (optional) — one-line description; defaults to empty string
6. `--challenge <slug>` (optional) — related challenge slug; omitted from frontmatter if not provided

The generated frontmatter SHALL include: `layout: doc`, `title`, `description`, `chapter` (integer extracted from `<chapter>` argument), `section`, `createdTime` (UTC+8 ISO 8601 timestamp at generation time). If `--challenge` is provided, a `challenge` field SHALL be appended.

When `<section>` is `index`, the script SHALL generate an index page: frontmatter SHALL include `isIndex: true` and SHALL NOT include `section` or `challenge` fields.

The script SHALL exit with a non-zero code and a descriptive error message if:
- Any required argument (`<subject>`, `<chapter>`, `<section>`) is missing
- `<chapter>` does not match the pattern `ch<N>` where N is a positive integer
- The output file already exists (to prevent accidental overwrite)

#### Scenario: Generate section scaffold with defaults

- **WHEN** `pnpm new-tutor py ch1 1-1 --title "環境安裝"` is executed
- **THEN** `docs/tutor/py/ch1/1-1.md` SHALL be created with `layout: doc`, `title: 環境安裝`, `chapter: 1`, `section: "1-1"`, and a `createdTime` field containing the current UTC+8 timestamp

#### Scenario: Generate section scaffold with challenge link

- **WHEN** `pnpm new-tutor py ch1 1-1 --title "環境安裝" --challenge hello-world` is executed
- **THEN** the generated file SHALL include `challenge: hello-world` in its frontmatter

#### Scenario: Generate index page scaffold

- **WHEN** `pnpm new-tutor py ch1 index --title "模組一：與電腦溝通的基礎"` is executed
- **THEN** `docs/tutor/py/ch1/index.md` SHALL be created with `isIndex: true` and SHALL NOT contain `section` or `challenge` fields

#### Scenario: Output file already exists

- **WHEN** the target file already exists
- **THEN** the script SHALL exit with code 1 and print `[new-tutor] ERROR: <path> already exists. Aborting to prevent overwrite.`

#### Scenario: Invalid chapter format

- **WHEN** `<chapter>` is not in the form `ch<N>` (e.g., `chapter1` or `1`)
- **THEN** the script SHALL exit with code 1 and print `[new-tutor] ERROR: <chapter> must be in the format chN (e.g., ch1, ch2)`


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

### Requirement: npm script entry runs the tutor generator

`package.json` SHALL contain a script entry named `new-tutor` that executes `scripts/new-tutor.ts` via `npx tsx`, passing all additional CLI arguments through.

#### Scenario: Invocation via pnpm

- **WHEN** `pnpm new-tutor py ch1 1-1` is run from the project root
- **THEN** `scripts/new-tutor.ts` SHALL execute with `py`, `ch1`, `1-1` as positional arguments

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

### Requirement: CLI script scaffolds a new tutor article file

A script at `scripts/new-tutor.ts` SHALL accept positional command-line arguments and generate a `docs/tutor/<subject>/<chapter>/<section>.md` file containing a valid frontmatter skeleton and Markdown body template.

The script SHALL accept the following arguments:
1. `<subject>` (required) — target subject directory name (e.g., `py`, `alg`, `ds`)
2. `<chapter>` (required) — chapter directory name in the format `chN` (e.g., `ch1`, `ch2`)
3. `<section>` (required) — section file name without `.md` (e.g., `1-1`, `index`)
4. `--title <string>` (optional) — display title; defaults to title-cased `<section>`
5. `--description <string>` (optional) — one-line description; defaults to empty string
6. `--challenge <slug>` (optional) — related challenge slug; omitted from frontmatter if not provided

The generated frontmatter SHALL include: `layout: doc`, `title`, `description`, `chapter` (integer extracted from `<chapter>` argument), `section`, `createdTime` (UTC+8 ISO 8601 timestamp at generation time). If `--challenge` is provided, a `challenge` field SHALL be appended.

When `<section>` is `index`, the script SHALL generate an index page: frontmatter SHALL include `isIndex: true` and SHALL NOT include `section` or `challenge` fields.

The script SHALL exit with a non-zero code and a descriptive error message if:
- Any required argument (`<subject>`, `<chapter>`, `<section>`) is missing
- `<chapter>` does not match the pattern `ch<N>` where N is a positive integer
- The output file already exists (to prevent accidental overwrite)

#### Scenario: Generate section scaffold with defaults

- **WHEN** `pnpm new-tutor py ch1 1-1 --title "環境安裝"` is executed
- **THEN** `docs/tutor/py/ch1/1-1.md` SHALL be created with `layout: doc`, `title: 環境安裝`, `chapter: 1`, `section: "1-1"`, and a `createdTime` field containing the current UTC+8 timestamp

#### Scenario: Generate section scaffold with challenge link

- **WHEN** `pnpm new-tutor py ch1 1-1 --title "環境安裝" --challenge hello-world` is executed
- **THEN** the generated file SHALL include `challenge: hello-world` in its frontmatter

#### Scenario: Generate index page scaffold

- **WHEN** `pnpm new-tutor py ch1 index --title "模組一：與電腦溝通的基礎"` is executed
- **THEN** `docs/tutor/py/ch1/index.md` SHALL be created with `isIndex: true` and SHALL NOT contain `section` or `challenge` fields

#### Scenario: Output file already exists

- **WHEN** the target file already exists
- **THEN** the script SHALL exit with code 1 and print `[new-tutor] ERROR: <path> already exists. Aborting to prevent overwrite.`

#### Scenario: Invalid chapter format

- **WHEN** `<chapter>` is not in the form `ch<N>` (e.g., `chapter1` or `1`)
- **THEN** the script SHALL exit with code 1 and print `[new-tutor] ERROR: <chapter> must be in the format chN (e.g., ch1, ch2)`

---
### Requirement: npm script entry runs the tutor generator

`package.json` SHALL contain a script entry named `new-tutor` that executes `scripts/new-tutor.ts` via `npx tsx`, passing all additional CLI arguments through.

#### Scenario: Invocation via pnpm

- **WHEN** `pnpm new-tutor py ch1 1-1` is run from the project root
- **THEN** `scripts/new-tutor.ts` SHALL execute with `py`, `ch1`, `1-1` as positional arguments