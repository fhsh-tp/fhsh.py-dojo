## ADDED Requirements

### Requirement: Tutor directory follows multi-subject layout

The `docs/tutor/` directory SHALL be organized into subject subdirectories (`py/`, `alg/`, `ds/`). Each subject directory SHALL contain chapter subdirectories named `chN/` (where N is a positive integer). Each chapter directory SHALL contain an `index.md` overview file and section files named `<chapter>-<section>.md` (e.g., `1-1.md`, `1-2.md`).

#### Scenario: Python subject directory structure

- **WHEN** the `docs/tutor/py/` directory is created
- **THEN** it SHALL contain `index.md` as the subject overview and subdirectories `ch1/`, `ch2/`, `ch3/`, `ch4/` corresponding to the four curriculum modules

#### Scenario: Chapter directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch1/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `1-1.md`, `1-2.md`, `1-3.md` corresponding to the sections in that chapter

---

### Requirement: Tutor article frontmatter schema

Every tutor section article (non-index `.md` file under `docs/tutor/`) SHALL include the following frontmatter fields:

- `layout`: fixed value `doc`
- `title`: display title string
- `description`: one-line summary string
- `chapter`: integer indicating the module number (1–4)
- `section`: string in the format `"<chapter>-<section>"` (e.g., `"1-1"`)
- `createdTime`: ISO 8601 datetime string with UTC+8 offset (e.g., `2026-04-05T10:00:00+08:00`)
- `challenge` (optional): kebab-case slug of the related challenge file in `docs/challenge/`

Chapter `index.md` files SHALL include `layout: doc`, `title`, `description`, and `isIndex: true`.

#### Scenario: Valid section article frontmatter

- **WHEN** a tutor section file is parsed by VitePress
- **THEN** all required fields (`layout`, `title`, `description`, `chapter`, `section`, `createdTime`) SHALL be present and non-empty

#### Scenario: Challenge field links to existing challenge

- **WHEN** a tutor article frontmatter includes `challenge: <slug>`
- **THEN** the slug SHALL match a file at `docs/challenge/<slug>.md`

#### Scenario: Index page frontmatter

- **WHEN** a chapter `index.md` is parsed
- **THEN** `isIndex: true` SHALL be present and the file SHALL NOT include `section` or `challenge` fields
