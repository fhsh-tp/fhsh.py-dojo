# challenge-type-unification Specification

## Purpose

TBD - created by archiving change 'challenge-type-safety'. Update Purpose after archive.

## Requirements

### Requirement: Challenge type in challenge.type.ts is the single source of truth for view-layer fields

The `Challenge` interface in `.vitepress/theme/types.d/challenge.type.ts` SHALL be the canonical definition for all view-layer fields. The `tags` field SHALL be required (`string[]`), not optional. The `difficulty` field SHALL use the strict union `'easy' | 'medium' | 'hard' | 'mystery'` without a trailing `| string`.

The data-layer module `docs/shared/challenge.data.ts` SHALL NOT define its own `Challenge` interface. Instead, it SHALL import `Challenge` from `challenge.type.ts` and define a `DataChallenge` interface that extends `Challenge` with data-only fields (`algorithm: string`, `params: object`, `testcase_count?: number`, `type: ExerciseType`). The `type` field carries the resolved exercise type and SHALL default to `basic` when the source frontmatter omits it.

#### Scenario: View-layer type has required tags and strict difficulty

- **WHEN** a component imports `Challenge` from `challenge.type.ts`
- **THEN** the `tags` field SHALL be `string[]` (required, not optional)
- **AND** the `difficulty` field SHALL accept only `'easy'`, `'medium'`, `'hard'`, or `'mystery'`

#### Scenario: Data-layer type extends view-layer type

- **WHEN** `challenge.data.ts` defines its data-layer type
- **THEN** it SHALL use `interface DataChallenge extends Challenge` to inherit view-layer fields
- **AND** it SHALL add `algorithm: string`, `params: object`, `testcase_count?: number`, and `type: ExerciseType` as data-only fields

#### Scenario: No duplicate Challenge interface in data loader

- **WHEN** `challenge.data.ts` is inspected
- **THEN** there SHALL be exactly zero standalone `Challenge` interface definitions (only the imported one and the extending `DataChallenge`)

---
### Requirement: Numeric fallbacks in content loader use nullish coalescing

The content loader in `docs/shared/challenge.data.ts` SHALL use nullish coalescing (`??`) instead of logical OR (`||`) for the `id` and `testcase_count` fields, so that `0` is preserved as a valid value rather than being silently replaced by the default.

#### Scenario: Frontmatter id of 0 is preserved

- **WHEN** a challenge markdown file has `id: 0` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `id` equal to `0`

#### Scenario: Frontmatter testcase_count of 0 is preserved

- **WHEN** a challenge markdown file has `testcase_count: 0` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `testcase_count` equal to `0`

#### Scenario: Missing id falls back to index-based default

- **WHEN** a challenge markdown file does not have `id` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `id` equal to `idx + 1`

#### Scenario: Missing testcase_count falls back to 5

- **WHEN** a challenge markdown file does not have `testcase_count` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `testcase_count` equal to `5`

<!-- @trace
source: challenge-type-safety
updated: 2026-04-10
code:
  - docs/challenge/odd-numbers.md
  - assets/banner.png
  - docs/challenge/date-validator.md
  - docs/challenge/collatz-steps.md
  - docs/challenge/countdown.md
  - docs/challenge/factorial.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/range-sum.md
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/challenge/seconds-converter.md
  - docs/challenge/leap-year.md
  - docs/challenge/sign-check.md
  - docs/challenge/beverage-cashier.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/change-calculator.md
  - docs/challenge/bmi-classifier.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/skip-multiples.md
  - docs/challenge/grade-level.md
  - docs/challenge/odd-even.md
  - docs/challenge/digit-counter.md
  - docs/challenge/first-divisor.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/grade-average.md
  - docs/challenge/target-sum.md
  - docs/challenge/number-sum.md
  - docs/challenge/quadratic-discriminant.md
  - docs/challenge/repeat-greeting.md
  - docs/challenge/quadrant-classifier.md
  - docs/challenge/vending-change.md
  - docs/challenges.md
  - docs/shared/challenge.data.ts
  - docs/challenge/triangle-check.md
  - docs/challenge/self-introduction.md
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/digit-sum-skip.md
  - docs/challenge/hello-world.md
  - docs/challenge/number-reverse.md
  - docs/challenge/password-check.md
  - docs/challenge/triangle-classify.md
-->
