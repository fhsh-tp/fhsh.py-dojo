## ADDED Requirements

### Requirement: Challenge category taxonomy and resolver

A shared module `docs/shared/challenge-category.ts` SHALL be the single source of truth for the challenge category taxonomy. It SHALL export a constant `CHALLENGE_CATEGORIES` equal to `['python', 'apcs']`, a `ChallengeCategory` union type derived from that constant, and a function `resolveChallengeCategory(raw: unknown): ChallengeCategory`.

`resolveChallengeCategory` SHALL return the raw value when it is one of `CHALLENGE_CATEGORIES`, and SHALL return `'python'` for any other input (absent, `undefined`, `null`, misspelled string, wrong casing, or non-string value). The resolver MUST NOT throw.

A test file SHALL scan every `docs/challenge/*.md` frontmatter and fail — naming the offending file — when a `category` value is present but not in `CHALLENGE_CATEGORIES`, so that authoring typos are caught at test time even though the runtime resolver silently defaults them.

#### Scenario: Known values resolve to themselves

- **WHEN** `resolveChallengeCategory` is called with `'python'` or `'apcs'`
- **THEN** it SHALL return the same value

#### Scenario: Absent or unknown values default to python

- **WHEN** `resolveChallengeCategory` is called with `undefined`, `null`, `'APCS'`, `'apsc'`, or `42`
- **THEN** it SHALL return `'python'` without throwing

#### Scenario: Authoring typo is caught by the file-scan test

- **WHEN** a challenge file declares `category: apsc` and the test suite runs
- **THEN** the category scan test SHALL fail with a message naming that file

### Requirement: Category-filtered catalogue pages

The site SHALL serve two challenge catalogue pages, both rendering the existing `ChallengeListView` component with a filtered subset of the challenge data:

- `docs/challenges.md` (URL `/challenges`, page title `Python 挑戰`) SHALL list exactly the challenges whose resolved category is `'python'`.
- `docs/apcs-challenges.md` (URL `/apcs-challenges`, page title `APCS 挑戰`) SHALL list exactly the challenges whose resolved category is `'apcs'`.

Filtering SHALL happen in each page's `<script setup>` block; `ChallengeListView` SHALL keep its existing contract of rendering whatever `challenges` array it receives. Search and difficulty filtering behavior within each page SHALL remain unchanged. Challenge markdown files MUST NOT be moved or renamed by this split, so every challenge keeps its slug and URL.

#### Scenario: APCS challenges appear only on the APCS page

- **WHEN** a challenge declares `category: apcs`
- **THEN** it SHALL be listed on `/apcs-challenges` and SHALL NOT be listed on `/challenges`

#### Scenario: Unlabeled challenges stay on the Python page

- **WHEN** a challenge omits the `category` field
- **THEN** it SHALL be listed on `/challenges` and SHALL NOT be listed on `/apcs-challenges`

#### Scenario: Every challenge appears on exactly one page

- **WHEN** the two catalogue pages are built from the full challenge data set
- **THEN** the union of the two page listings SHALL equal the full set and their intersection SHALL be empty

### Requirement: Page-scoped completion count

The completion counter rendered by `ChallengeListView` (`已完成 X / Y`) SHALL compute both numerator and denominator from the `challenges` prop the page passed in: `Y` SHALL be the length of that array and `X` SHALL be the number of challenges in that array whose slug the progress store reports as completed. The counter MUST NOT use the store-wide completed count. The store-wide `completedCount` getter SHALL remain in the progress store with unchanged semantics for its existing consumers.

#### Scenario: Completion on one page does not inflate the other

- **WHEN** a student has completed 2 APCS challenges and 0 Python challenges
- **THEN** `/apcs-challenges` SHALL show `已完成 2 / 4` style counts scoped to its own list and `/challenges` SHALL show a numerator of 0

#### Scenario: Counter ignores the active search and difficulty filter

- **WHEN** a search query or difficulty filter narrows the visible cards
- **THEN** the counter SHALL still be computed from the full page-level challenge array, not the filtered view

### Requirement: Category-aware back navigation

On a challenge page, the header back control (`← 返回`) and the error-state `返回列表` button SHALL both navigate to the list page matching the challenge's resolved category: `/challenges` for `'python'` and `/apcs-challenges` for `'apcs'`. `AppHeader` SHALL receive this destination through an optional `backUrl` prop that defaults to `/challenges`. This replaces the previous behavior of navigating to the site root `/`.

#### Scenario: APCS challenge returns to the APCS list

- **WHEN** a student opens a challenge with `category: apcs` and clicks `← 返回`
- **THEN** the router SHALL navigate to `/apcs-challenges`

#### Scenario: Unlabeled challenge returns to the Python list

- **WHEN** a student opens a challenge whose frontmatter omits `category` and clicks `← 返回`
- **THEN** the router SHALL navigate to `/challenges`

#### Scenario: Error state shares the same destination

- **WHEN** a challenge page fails to load and the student clicks the error-state `返回列表` button
- **THEN** the router SHALL navigate to the same category-resolved list URL as the header back control
