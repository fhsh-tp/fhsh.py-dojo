## ADDED Requirements

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

### Requirement: Data loader provides fallback values for algorithm and params

The content loader in `docs/shared/challenge.data.ts` SHALL provide fallback values for `algorithm` and `params` when they are absent from challenge frontmatter. `algorithm` SHALL default to `''` (empty string) and `params` SHALL default to `{}` (empty object). This ensures runtime values match the `DataChallenge` interface contract where both fields are required.

#### Scenario: Challenge without algorithm in frontmatter

- **WHEN** a challenge markdown file does not have `algorithm` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `algorithm` equal to `''`

#### Scenario: Challenge without params in frontmatter

- **WHEN** a challenge markdown file does not have `params` in its frontmatter
- **THEN** the loaded DataChallenge object SHALL have `params` equal to `{}`

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
