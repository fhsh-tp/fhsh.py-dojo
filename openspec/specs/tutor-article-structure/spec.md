## ADDED Requirements

### Requirement: Tutor directory follows multi-subject layout

The `docs/tutor/` directory SHALL be organized into subject subdirectories (`py/`, `alg/`, `ds/`). Each subject directory SHALL contain chapter subdirectories named `chN/` (where N is a positive integer). Each chapter directory SHALL contain an `index.md` overview file and section files named `<chapter>-<section>.md` (e.g., `1-1.md`, `1-2.md`).

#### Scenario: Python subject directory structure

- **WHEN** the `docs/tutor/py/` directory is created
- **THEN** it SHALL contain `index.md` as the subject overview and subdirectories `ch1/`, `ch2/`, `ch3/`, `ch4/` corresponding to the four curriculum modules

#### Scenario: Chapter 1 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch1/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `1-1.md`, `1-2.md`, `1-3.md`, `1-4.md` corresponding to the sections in that chapter

#### Scenario: Chapter 2 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch2/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `2-1.md`, `2-2.md`, `2-3.md`, `2-4.md`, `2-5.md`, `2-6.md`, `2-7.md` corresponding to the seven sections in Module 2

#### Scenario: Chapter 2 index lists all seven sections

- **WHEN** the `docs/tutor/py/ch2/index.md` file is rendered
- **THEN** it SHALL display links to all seven sections: 2-1 (for + range), 2-2 (while), 2-3 (break + continue), 2-4 (list + linear search), 2-5 (bubble sort), 2-6 (dict + hash), 2-7 (summary)


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


<!-- @trace
source: write-ch2-2-1-for-range
updated: 2026-04-12
code:
  - docs/challenge/odd-numbers.md
  - package.json
  - docs/challenge/triangle-check.md
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/shared/challenge.data.ts
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/range-sum.md
  - docs/challenge/countdown.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/movie-ticket.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/challenge/repeat-greeting.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-reverse.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadrant-classifier.md
  - docs/public/assets/LOGO-light.png
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/reference.md
  - docs/public/assets/LOGO-dark.png
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-2.md
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/number-sum.md
  - docs/challenge/digit-counter.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/grade-level.md
  - docs/public/assets/LOGO-light.svg
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/tutor/py/ch1/appendix.md
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - docs/challenge/leap-year.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/triangle-classify.md
  - docs/public/assets/LOGO-dark.svg
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/seconds-converter.md
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/challenge/change-calculator.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenges.md
  - docs/challenge/first-divisor.md
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/self-introduction.md
  - docs/public/favicon.svg
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/challenge/factorial.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/hello-world.md
  - docs/challenge/date-validator.md
  - docs/challenge/target-sum.md
  - assets/banner.png
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - .vitepress/sidebar.ts
  - docs/challenge/grade-average.md
  - docs/challenge/password-check.md
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

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

### Requirement: Tutor directory follows multi-subject layout

The `docs/tutor/` directory SHALL be organized into subject subdirectories (`py/`, `alg/`, `ds/`). Each subject directory SHALL contain chapter subdirectories named `chN/` (where N is a positive integer). Each chapter directory SHALL contain an `index.md` overview file and section files named `<chapter>-<section>.md` (e.g., `1-1.md`, `1-2.md`).

#### Scenario: Python subject directory structure

- **WHEN** the `docs/tutor/py/` directory is created
- **THEN** it SHALL contain `index.md` as the subject overview and subdirectories `ch1/`, `ch2/`, `ch3/`, `ch4/` corresponding to the four curriculum modules

#### Scenario: Chapter 1 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch1/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `1-1.md`, `1-2.md`, `1-3.md`, `1-4.md` corresponding to the sections in that chapter

#### Scenario: Chapter 2 directory structure

- **WHEN** a chapter directory `docs/tutor/py/ch2/` is created
- **THEN** it SHALL contain `index.md` as the chapter overview and section files `2-1.md`, `2-2.md`, `2-3.md`, `2-4.md`, `2-5.md`, `2-6.md`, `2-7.md` corresponding to the seven sections in Module 2

#### Scenario: Chapter 2 index lists all seven sections

- **WHEN** the `docs/tutor/py/ch2/index.md` file is rendered
- **THEN** it SHALL display links to all seven sections: 2-1 (for + range), 2-2 (while), 2-3 (break + continue), 2-4 (list + linear search), 2-5 (bubble sort), 2-6 (dict + hash), 2-7 (summary)

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