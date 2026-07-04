## MODIFIED Requirements

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
