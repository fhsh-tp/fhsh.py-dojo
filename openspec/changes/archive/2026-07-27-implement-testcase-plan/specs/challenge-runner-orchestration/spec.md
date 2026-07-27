## ADDED Requirements

### Requirement: Runner supports testcase_plan challenges

`ChallengeConfig` SHALL accept an optional `testcasePlan` array. When present, the effective testcase count SHALL be derived as the plan total (sum of band counts plus number of literal entries) instead of `testcaseCount`. The dev strategy SHALL obtain inputs from the WASM `generate_dev_inputs` entry (one full plan round, declaration order); the prod strategy SHALL request exactly the plan total from `select_testcases`. Challenges without `testcasePlan` SHALL behave exactly as before on both strategies.

#### Scenario: dev strategy renders a plan round

- **WHEN** a plan challenge with plan total 5 loads in dev mode
- **THEN** 5 testcases are generated via `generate_dev_inputs` in plan declaration order and fed to the Python generator for expected outputs

#### Scenario: prod strategy requests the plan total

- **WHEN** a plan challenge with plan total 5 loads in prod mode
- **THEN** the runner calls `select_testcases(id, 5)` and receives one ordered block

#### Scenario: engine error surfaces to the user

- **WHEN** the WASM engine rejects a plan-related call (count mismatch or invalid plan)
- **THEN** the runner surfaces an error message instead of silently degrading to the non-plan path

#### Scenario: non-plan challenges unchanged

- **WHEN** a challenge without `testcasePlan` loads in dev or prod mode
- **THEN** the existing generation and selection flows run unchanged
