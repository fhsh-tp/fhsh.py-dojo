## ADDED Requirements

### Requirement: Block selection for plan pools

When a loaded pool's payload declares `plan_block_size = k`, `select_testcases` SHALL validate that `k > 0`, that the pool's testcase count is a positive multiple of `k`, and that the requested `count` equals `k` exactly — failing with a descriptive error otherwise. It SHALL then select one block uniformly at random and return that block's testcases in their stored order without shuffling. Pools without `plan_block_size` SHALL keep the existing shuffle-and-truncate selection unchanged.

#### Scenario: plan pool returns an ordered block

- **WHEN** a pool has 200 testcases with `plan_block_size: 5` and `select_testcases(id, 5)` is called
- **THEN** the returned 5 inputs are one of the 40 stored blocks, in stored order

#### Scenario: count mismatch on plan pool is refused

- **WHEN** the pool declares `plan_block_size: 5` and the caller requests 10
- **THEN** selection fails with an error stating the required count is 5

#### Scenario: corrupt block structure is refused

- **WHEN** the pool declares `plan_block_size: 6` but holds 200 testcases (not a multiple of 6)
- **THEN** selection fails with a descriptive error instead of returning a partial block

#### Scenario: non-plan pools behave as before

- **WHEN** a pool without `plan_block_size` is loaded
- **THEN** `select_testcases` performs the existing uniform shuffle-and-truncate selection
