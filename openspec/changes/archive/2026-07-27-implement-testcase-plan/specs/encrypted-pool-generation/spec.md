## ADDED Requirements

### Requirement: Plan challenges produce blocked pools

For a challenge declaring `testcase_plan`, the pool build SHALL request `count = floor(POOL_SIZE / plan_total) * plan_total` inputs from the WASM engine (where `plan_total` is the sum of band counts plus the number of literal entries, computed from the frontmatter), and the encrypted pool payload SHALL include `plan_block_size: plan_total`. Challenges without `testcase_plan` SHALL be built exactly as before, with no `plan_block_size` field in their payload.

#### Scenario: plan pool carries block size

- **WHEN** a challenge declares a plan with total 5 and POOL_SIZE is 200
- **THEN** the pool contains 200 testcases (40 blocks of 5) and its payload declares `plan_block_size: 5`

#### Scenario: non-plan pools are unchanged

- **WHEN** a challenge without `testcase_plan` is built by the new pipeline
- **THEN** its encrypted payload has no `plan_block_size` field and its pool content is byte-identical to the previous pipeline's output for the same declaration

### Requirement: readChallenge validates testcase_plan usage

`readChallenge` SHALL read the optional `testcase_plan` frontmatter field and pass it through to the WASM pool spec. It SHALL throw a descriptive error naming the file when the frontmatter declares both `testcase_plan` and `testcase_count`.

#### Scenario: plan passes through to the engine

- **WHEN** a challenge declares `testcase_plan`
- **THEN** the pool spec sent to the WASM engine contains the plan verbatim

#### Scenario: coexistence with testcase_count fails the build

- **WHEN** a challenge declares both `testcase_plan` and `testcase_count`
- **THEN** the build fails with an error naming the file and the mutual-exclusion rule
