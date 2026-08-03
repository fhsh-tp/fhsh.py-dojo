## ADDED Requirements

### Requirement: Challenge data model includes category field

The `Challenge` interface in `challenge.type.ts` SHALL include a required `category` field of type `'python' | 'apcs'` (the `ChallengeCategory` union exported by `docs/shared/challenge-category.ts`). The content loader transform in `docs/shared/challenge.data.ts` SHALL populate this field by passing the raw frontmatter `category` value through `resolveChallengeCategory`, so downstream consumers always receive a valid category and never a raw frontmatter string.

#### Scenario: Loader normalizes the category field

- **WHEN** the content loader transforms a challenge whose frontmatter omits `category` or carries an unknown value
- **THEN** the resulting `Challenge` object SHALL have `category: 'python'`

#### Scenario: Declared apcs category flows through

- **WHEN** the content loader transforms a challenge with `category: apcs`
- **THEN** the resulting `Challenge` object SHALL have `category: 'apcs'`
