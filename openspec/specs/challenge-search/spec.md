# challenge-search Specification

## Purpose

TBD - created by archiving change 'add-challenge-search'. Update Purpose after archive.

## Requirements

### Requirement: Challenge data model includes chapter and description fields

The `Challenge` interface in `challenge.type.ts` SHALL include a `chapter` field of type `string` (e.g., `"ch1"`, `"ch2"`) and a `description` field of type `string`. Both fields SHALL be optional (defaulting to empty string when absent from frontmatter).

The content loader in `challenge.data.ts` SHALL extract `chapter` and `description` from each challenge markdown file's frontmatter and include them in the loaded data.

#### Scenario: Challenge with chapter and description in frontmatter

- **WHEN** a challenge markdown file has `chapter: ch1` and `description: 讀取名字並打招呼` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `chapter` equal to `"ch1"` and `description` equal to `"讀取名字並打招呼"`

#### Scenario: Challenge without chapter or description in frontmatter

- **WHEN** a challenge markdown file does not have `chapter` or `description` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `chapter` equal to `""` and `description` equal to `""`


<!-- @trace
source: add-challenge-search
updated: 2026-04-10
code:
  - docs/challenge/repeat-greeting.md
  - docs/challenge/leap-year.md
  - docs/challenge/countdown.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/challenge/parrot-echo.md
  - docs/challenge/digit-counter.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/seconds-converter.md
  - docs/challenge/triangle-check.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/vending-change.md
  - assets/banner.png
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/change-calculator.md
  - docs/challenges.md
  - docs/challenge/hello-world.md
  - docs/challenge/sign-check.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/number-reverse.md
  - docs/challenge/grade-level.md
  - docs/challenge/factorial.md
  - docs/challenge/odd-even.md
  - docs/challenge/grade-average.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/range-sum.md
  - docs/shared/challenge.data.ts
  - docs/challenge/target-sum.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/first-divisor.md
  - docs/challenge/date-validator.md
  - docs/challenge/self-introduction.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-sum.md
  - docs/challenge/password-check.md
-->

---
### Requirement: ChallengeListView displays a search input field

The ChallengeListView SHALL render a text search input (`<input type="search">`) above the difficulty filter buttons. The input SHALL span the full width of the container and include a placeholder indicating the searchable fields (e.g., "搜尋題目名稱、說明、標籤、章節...").

#### Scenario: Search input is visible on page load

- **WHEN** the user navigates to the challenge list page
- **THEN** a search input field SHALL be visible above the difficulty filter buttons
- **AND** the input SHALL have an empty value

#### Scenario: Search input has descriptive placeholder

- **WHEN** the search input is empty
- **THEN** the placeholder text SHALL indicate the searchable fields


<!-- @trace
source: add-challenge-search
updated: 2026-04-10
code:
  - docs/challenge/repeat-greeting.md
  - docs/challenge/leap-year.md
  - docs/challenge/countdown.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/challenge/parrot-echo.md
  - docs/challenge/digit-counter.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/seconds-converter.md
  - docs/challenge/triangle-check.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/vending-change.md
  - assets/banner.png
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/change-calculator.md
  - docs/challenges.md
  - docs/challenge/hello-world.md
  - docs/challenge/sign-check.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/number-reverse.md
  - docs/challenge/grade-level.md
  - docs/challenge/factorial.md
  - docs/challenge/odd-even.md
  - docs/challenge/grade-average.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/range-sum.md
  - docs/shared/challenge.data.ts
  - docs/challenge/target-sum.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/first-divisor.md
  - docs/challenge/date-validator.md
  - docs/challenge/self-introduction.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-sum.md
  - docs/challenge/password-check.md
-->

---
### Requirement: Search filters challenges by text matching across multiple fields

When the user types in the search input, the challenge list SHALL be filtered in real time. The query SHALL be normalized by trimming surrounding whitespace and lowercasing before matching. A challenge matches the search query if the normalized query is contained within any of the following lowercased fields: `title`, `description`, `tags` (joined as a single string), or `chapter` — or if the query matches the challenge `id` under the id matching rules below.

Id matching SHALL apply exactly one of two rules, chosen by the shape of the normalized query:

1. If the normalized query consists solely of decimal digits, it SHALL match a challenge whose id ordinal (the decimal integer obtained by stripping the id's leading non-digit characters) equals the query parsed as a decimal integer.
2. Otherwise, it SHALL match a challenge whose id starts with the normalized query.

Text-field matching and id matching SHALL be combined with OR: a challenge is shown when either matches. Because each catalogue page receives a category-filtered challenge list, id matching never crosses categories on a page.

#### Scenario: Search matches by title

- **WHEN** the user types "飲料" in the search input
- **THEN** only challenges whose title contains "飲料" SHALL be displayed

#### Scenario: Search matches by tag

- **WHEN** the user types "input" in the search input
- **THEN** all challenges that have "input" in their tags array SHALL be displayed

#### Scenario: Search matches by chapter

- **WHEN** the user types "ch1" in the search input
- **THEN** all challenges with `chapter` equal to `"ch1"` SHALL be displayed

#### Scenario: Search matches by description

- **WHEN** the user types "收銀" in the search input
- **THEN** challenges whose description contains "收銀" SHALL be displayed

#### Scenario: Pure-digit query matches id ordinal exactly

- **WHEN** the user types "3", "03", or "003" on the Python catalogue page
- **THEN** the challenge with id py003 SHALL be displayed via the id rule, together with any challenge whose text fields contain the query

##### Example: Digit query matrix on the Python page

| query | id-rule matches |
| --- | --- |
| 3 | py003 |
| 03 | py003 |
| 003 | py003 |
| 55 | (none — Python page has ordinals 1–54) |

#### Scenario: Non-digit query matches id by prefix

- **WHEN** the user types "py00" on the Python catalogue page
- **THEN** challenges py001 through py009 SHALL be displayed via the id rule

#### Scenario: Unpadded prefixed query does not match via id

- **WHEN** the user types "py3" on the Python catalogue page
- **THEN** no challenge SHALL be displayed via the id rule, because "py3" is not a prefix of any zero-padded id and is not a pure-digit query

#### Scenario: Search with no matches

- **WHEN** the user types a query that matches no challenge
- **THEN** the empty state message "沒有符合條件的挑戰。" SHALL be displayed

---
### Requirement: Search and difficulty filter work together as intersection

When both a search query and a difficulty filter are active, the displayed challenges SHALL be the intersection (AND) of both filters. A challenge MUST match the search query AND the selected difficulty to be shown.

#### Scenario: Combined search and difficulty filter

- **WHEN** the user selects difficulty "easy" AND types "ch1" in the search input
- **THEN** only challenges that are both easy difficulty AND belong to ch1 SHALL be displayed

#### Scenario: Clear search restores difficulty-only filter

- **WHEN** the user has both search query and difficulty filter active
- **AND** the user clears the search input
- **THEN** the list SHALL show all challenges matching the selected difficulty


<!-- @trace
source: add-challenge-search
updated: 2026-04-10
code:
  - docs/challenge/repeat-greeting.md
  - docs/challenge/leap-year.md
  - docs/challenge/countdown.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/challenge/parrot-echo.md
  - docs/challenge/digit-counter.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/seconds-converter.md
  - docs/challenge/triangle-check.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/vending-change.md
  - assets/banner.png
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/change-calculator.md
  - docs/challenges.md
  - docs/challenge/hello-world.md
  - docs/challenge/sign-check.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/number-reverse.md
  - docs/challenge/grade-level.md
  - docs/challenge/factorial.md
  - docs/challenge/odd-even.md
  - docs/challenge/grade-average.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/range-sum.md
  - docs/shared/challenge.data.ts
  - docs/challenge/target-sum.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/first-divisor.md
  - docs/challenge/date-validator.md
  - docs/challenge/self-introduction.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-sum.md
  - docs/challenge/password-check.md
-->

---
### Requirement: Challenge frontmatter includes chapter and description

Each challenge markdown file in `docs/challenge/*.md` SHALL include `chapter` and `description` fields in its YAML frontmatter. The `chapter` field SHALL use the format `ch<N>` matching the tutorial chapter the challenge belongs to. The `description` field SHALL be a one-sentence summary of the challenge.

#### Scenario: Existing challenge files have chapter and description

- **WHEN** the challenge data is loaded
- **THEN** each challenge that has been updated SHALL have a non-empty `chapter` and `description` value

<!-- @trace
source: add-challenge-search
updated: 2026-04-10
code:
  - docs/challenge/repeat-greeting.md
  - docs/challenge/leap-year.md
  - docs/challenge/countdown.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/challenge/parrot-echo.md
  - docs/challenge/digit-counter.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/seconds-converter.md
  - docs/challenge/triangle-check.md
  - docs/challenge/odd-numbers.md
  - docs/challenge/vending-change.md
  - assets/banner.png
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/change-calculator.md
  - docs/challenges.md
  - docs/challenge/hello-world.md
  - docs/challenge/sign-check.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/number-reverse.md
  - docs/challenge/grade-level.md
  - docs/challenge/factorial.md
  - docs/challenge/odd-even.md
  - docs/challenge/grade-average.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/range-sum.md
  - docs/shared/challenge.data.ts
  - docs/challenge/target-sum.md
  - docs/challenge/triangle-classify.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/first-divisor.md
  - docs/challenge/date-validator.md
  - docs/challenge/self-introduction.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/number-sum.md
  - docs/challenge/password-check.md
-->

---
### Requirement: Challenge data model includes category field

The `Challenge` interface in `challenge.type.ts` SHALL include a required `category` field of type `'python' | 'apcs'` (the `ChallengeCategory` union exported by `docs/shared/challenge-category.ts`). The content loader transform in `docs/shared/challenge.data.ts` SHALL populate this field by passing the raw frontmatter `category` value through `resolveChallengeCategory`, so downstream consumers always receive a valid category and never a raw frontmatter string.

#### Scenario: Loader normalizes the category field

- **WHEN** the content loader transforms a challenge whose frontmatter omits `category` or carries an unknown value
- **THEN** the resulting `Challenge` object SHALL have `category: 'python'`

#### Scenario: Declared apcs category flows through

- **WHEN** the content loader transforms a challenge with `category: apcs`
- **THEN** the resulting `Challenge` object SHALL have `category: 'apcs'`
