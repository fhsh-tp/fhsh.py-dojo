### Requirement: Mystery difficulty has explicit UI label and styling in all components

All components that display a difficulty badge SHALL include an explicit entry for `'mystery'` in their `difficultyLabel` and `difficultyClass` mappings. The label for mystery SHALL be `'未知'`. The styling SHALL use a neutral gray color scheme consistent with each component's existing fallback style.

Components that MUST include mystery mappings: `ChallengeCard.vue`, `ChallengeLink.vue`, `AppHeader.vue`.

#### Scenario: ChallengeCard renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** ChallengeCard SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`

#### Scenario: ChallengeLink renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** ChallengeLink SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`

#### Scenario: AppHeader renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** AppHeader SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`


<!-- @trace
source: challenge-audit-cleanup
updated: 2026-04-12
code:
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/date-validator.md
  - docs/challenge/leap-year.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/sidebar.ts
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/self-introduction.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/change-calculator.md
  - docs/challenge/skip-multiples.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/beverage-cashier.md
  - docs/shared/challenge.data.ts
  - docs/challenge/quadrant-classifier.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-average.md
  - .vitepress/theme/components/layout/AppHeader.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/range-sum.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-level.md
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/factorial.md
  - docs/challenge/password-check.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/digit-counter.md
  - docs/challenges.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/countdown.md
  - docs/challenge/number-sum.md
  - docs/challenge/odd-even.md
  - docs/challenge/target-sum.md
  - docs/challenge/number-reverse.md
  - docs/challenge/hello-world.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/challenge/taxi-fare.md
  - docs/challenge/vending-change.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/collatz-steps.md
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/challenge/triangle-check.md
  - .vitepress/theme/components/challenge/ChallengeCard.vue
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

### Requirement: Data loader provides fallback values for algorithm and params

The content loader in `docs/shared/challenge.data.ts` SHALL provide fallback values for `algorithm` and `params` when they are absent from challenge frontmatter. `algorithm` SHALL default to `''` (empty string) and `params` SHALL default to `{}` (empty object). This ensures runtime values match the `DataChallenge` interface contract where both fields are required.

#### Scenario: Challenge without algorithm in frontmatter

- **WHEN** a challenge markdown file does not have `algorithm` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `algorithm` equal to `''`

#### Scenario: Challenge without params in frontmatter

- **WHEN** a challenge markdown file does not have `params` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `params` equal to `{}`


<!-- @trace
source: challenge-audit-cleanup
updated: 2026-04-12
code:
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/date-validator.md
  - docs/challenge/leap-year.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/sidebar.ts
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/self-introduction.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/change-calculator.md
  - docs/challenge/skip-multiples.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/beverage-cashier.md
  - docs/shared/challenge.data.ts
  - docs/challenge/quadrant-classifier.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-average.md
  - .vitepress/theme/components/layout/AppHeader.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/range-sum.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-level.md
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/factorial.md
  - docs/challenge/password-check.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/digit-counter.md
  - docs/challenges.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/countdown.md
  - docs/challenge/number-sum.md
  - docs/challenge/odd-even.md
  - docs/challenge/target-sum.md
  - docs/challenge/number-reverse.md
  - docs/challenge/hello-world.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/challenge/taxi-fare.md
  - docs/challenge/vending-change.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/collatz-steps.md
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/challenge/triangle-check.md
  - .vitepress/theme/components/challenge/ChallengeCard.vue
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

### Requirement: Search filter removes redundant null guards

The search filtering logic in `ChallengeListView.vue` SHALL NOT use nullish coalescing (`??`) on fields that are guaranteed to be present by the `Challenge` type definition. Specifically, `c.tags` (required `string[]`), `c.description` (loader provides `''` default), and `c.chapter` (loader provides `''` default) SHALL be accessed directly without `?? []` or `?? ''` guards.

#### Scenario: Search filter accesses tags directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.tags.some(...)` without a `?? []` guard

#### Scenario: Search filter accesses description directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.description.toLowerCase()` without a `?? ''` guard

#### Scenario: Search filter accesses chapter directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.chapter.toLowerCase()` without a `?? ''` guard

## Requirements


<!-- @trace
source: challenge-audit-cleanup
updated: 2026-04-12
code:
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/bmi-classifier.md
  - docs/challenge/date-validator.md
  - docs/challenge/leap-year.md
  - docs/challenge/sum-skip-fives.md
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/sidebar.ts
  - docs/challenge/repeat-greeting.md
  - docs/challenge/sign-check.md
  - assets/banner.png
  - docs/public/references/ch1/PISA-2022-Math-Framework.pdf
  - .vitepress/theme/views/ChallengeListView.vue
  - docs/challenge/self-introduction.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/public/references/ch1/Wing-2011-CT-MicrosoftResearch.pdf
  - docs/challenge/seconds-converter.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/1-3.md
  - docs/challenge/change-calculator.md
  - docs/challenge/skip-multiples.md
  - docs/tutor/py/ch1/appendix.md
  - docs/challenge/beverage-cashier.md
  - docs/shared/challenge.data.ts
  - docs/challenge/quadrant-classifier.md
  - docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-average.md
  - .vitepress/theme/components/layout/AppHeader.vue
  - docs/public/references/ch1/Wing-2006-CT.pdf
  - docs/challenge/range-sum.md
  - docs/public/references/ch1/Brennan-Resnick-2012-CT-Assessment.pdf
  - .vitepress/theme/types.d/challenge.type.ts
  - docs/public/references/ch1/Papert-1980-Mindstorms.pdf
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/public/references/ch1/ISTE-CSTA-2011-CT-Definition.pdf
  - .vitepress/config.mts
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/public/references/ch1/Taiwan-108-Tech-Curriculum.pdf
  - docs/challenge/grade-level.md
  - docs/tutor/py/ch1/1-4.md
  - docs/challenge/factorial.md
  - docs/challenge/password-check.md
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/challenge/first-divisor.md
  - docs/challenge/digit-counter.md
  - docs/challenges.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/challenge/countdown.md
  - docs/challenge/number-sum.md
  - docs/challenge/odd-even.md
  - docs/challenge/target-sum.md
  - docs/challenge/number-reverse.md
  - docs/challenge/hello-world.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/challenge/taxi-fare.md
  - docs/challenge/vending-change.md
  - docs/challenge/parrot-echo.md
  - docs/challenge/movie-ticket.md
  - docs/challenge/collatz-steps.md
  - docs/public/references/ch1/Barr-Stephenson-2011-CT-K12.pdf
  - docs/public/references/ch1/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/odd-numbers.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/challenge/triangle-check.md
  - .vitepress/theme/components/challenge/ChallengeCard.vue
  - docs/challenge/digit-sum-skip.md
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
tests:
  - .vitepress/buildTutorSidebar.test.ts
-->

### Requirement: Mystery difficulty has explicit UI label and styling in all components

All components that display a difficulty badge SHALL include an explicit entry for `'mystery'` in their `difficultyLabel` and `difficultyClass` mappings. The label for mystery SHALL be `'未知'`. The styling SHALL use a neutral gray color scheme consistent with each component's existing fallback style.

Components that MUST include mystery mappings: `ChallengeCard.vue`, `ChallengeLink.vue`, `AppHeader.vue`.

#### Scenario: ChallengeCard renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** ChallengeCard SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`

#### Scenario: ChallengeLink renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** ChallengeLink SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`

#### Scenario: AppHeader renders mystery difficulty with proper label

- **WHEN** a challenge has `difficulty: 'mystery'`
- **THEN** AppHeader SHALL display the label `'未知'`
- **AND** the badge SHALL use the explicit mystery styling from `difficultyClass`

---
### Requirement: Data loader provides fallback values for algorithm and params

The content loader in `docs/shared/challenge.data.ts` SHALL provide fallback values for `algorithm` and `params` when they are absent from challenge frontmatter. `algorithm` SHALL default to `''` (empty string) and `params` SHALL default to `{}` (empty object). This ensures runtime values match the `DataChallenge` interface contract where both fields are required.

#### Scenario: Challenge without algorithm in frontmatter

- **WHEN** a challenge markdown file does not have `algorithm` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `algorithm` equal to `''`

#### Scenario: Challenge without params in frontmatter

- **WHEN** a challenge markdown file does not have `params` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `params` equal to `{}`

---
### Requirement: Search filter removes redundant null guards

The search filtering logic in `ChallengeListView.vue` SHALL NOT use nullish coalescing (`??`) on fields that are guaranteed to be present by the `Challenge` type definition. Specifically, `c.tags` (required `string[]`), `c.description` (loader provides `''` default), and `c.chapter` (loader provides `''` default) SHALL be accessed directly without `?? []` or `?? ''` guards.

#### Scenario: Search filter accesses tags directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.tags.some(...)` without a `?? []` guard

#### Scenario: Search filter accesses description directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.description.toLowerCase()` without a `?? ''` guard

#### Scenario: Search filter accesses chapter directly

- **WHEN** the search filter processes a challenge
- **THEN** it SHALL call `c.chapter.toLowerCase()` without a `?? ''` guard