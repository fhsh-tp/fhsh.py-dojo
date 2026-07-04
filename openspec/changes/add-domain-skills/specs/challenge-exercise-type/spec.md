## ADDED Requirements

### Requirement: Challenge frontmatter supports an extensible exercise-type taxonomy

Challenge frontmatter SHALL support an optional `type` field naming the exercise type. The taxonomy SHALL be extensible and SHALL define the following registered values with their status: `basic` (implemented), `competition` (implemented), `fill_in_blank` (deferred to a future version), `gamified` (deferred to a future version), and `guided` (future placeholder, design pending). Only `basic` and `competition` SHALL be accepted by tooling in this version; the deferred and future values SHALL be documented but SHALL NOT be accepted by the validator or emitted by the scaffold until implemented. When the `type` field is absent, the exercise type SHALL be treated as `basic`.

#### Scenario: Absent type defaults to basic

- **WHEN** a challenge frontmatter omits the `type` field
- **THEN** the exercise type SHALL be treated as `basic`

#### Scenario: Registered implemented values are accepted

- **WHEN** a challenge declares `type: competition`
- **THEN** the value SHALL be accepted as a valid exercise type

##### Example: taxonomy status

- **GIVEN** the exercise-type taxonomy
- **WHEN** an implementer inspects the registered values
- **THEN** `basic` and `competition` are implemented, `fill_in_blank` and `gamified` are deferred, and `guided` is a future placeholder

### Requirement: Scaffold script validates and emits the exercise type

The `pnpm new-challenge` scaffold SHALL accept a `--type` flag. It SHALL default the type to `basic` when `--type` is not supplied. It SHALL validate the supplied type against the implemented values `basic` and `competition`, and SHALL exit with a non-zero status and a descriptive error message when the type is not one of those values. The generated challenge file SHALL include a `type` field in its frontmatter reflecting the resolved type.

#### Scenario: Default type when flag omitted

- **WHEN** a user runs `pnpm new-challenge my-challenge` without `--type`
- **THEN** the generated frontmatter SHALL contain `type: basic`

#### Scenario: Explicit competition type

- **WHEN** a user runs `pnpm new-challenge my-challenge --type competition`
- **THEN** the generated frontmatter SHALL contain `type: competition`

#### Scenario: Invalid type is rejected

- **WHEN** a user runs `pnpm new-challenge my-challenge --type gamified`
- **THEN** the script SHALL print a descriptive error and exit with a non-zero status
- **AND** it SHALL NOT create the challenge file

### Requirement: Data loader resolves exercise type with a basic default

The challenge data loader `docs/shared/challenge.data.ts` SHALL expose the exercise type on its data-layer challenge object. It SHALL resolve a missing `type` to `basic`, so that the existing challenges that predate the `type` field remain valid without modification. The exercise-type value SHALL be typed by a union of the implemented values.

#### Scenario: Existing challenge without type resolves to basic

- **WHEN** the data loader transforms a challenge whose frontmatter has no `type`
- **THEN** the resulting data object's `type` SHALL be `basic`

#### Scenario: Declared type is preserved

- **WHEN** the data loader transforms a challenge whose frontmatter declares `type: competition`
- **THEN** the resulting data object's `type` SHALL be `competition`
