## MODIFIED Requirements

### Requirement: Testcase plan partitioning

The print-farm-schedule challenge SHALL declare a testcase_plan of exactly 20 entries per run, in this declaration order: 1 statement-example literal entry first (m=2, n=4, durations `2 3 5 7`), then 9 warm-up band cases (hand-computable scale), then 8 stress band cases, then 2 literal boundary entries covering the more-printers-than-jobs boundary and the single-job boundary. The pillbox-reminder challenge SHALL declare a testcase_plan of exactly 20 entries per run, in this declaration order: 1 statement-example literal entry first (Q=2, periods `3 5`, K=6), then 9 warm-up band cases, then 8 stress band cases, then 2 literal boundary entries covering the single-reminder (K=1) boundary and the simultaneous-tie boundary. For both challenges the first entry SHALL be the statement example so that the run panel's default stdin (derived from the first testcase) equals the worked example in the statement. The pillbox-reminder stress band SHALL be shaped so that a per-minute time-axis scan exceeds the 10M op budget (TLE) while both a linear scan over next-fire times and a heap-based solution stay below 500k ops (≥20× margin); the concrete stress bounds SHALL be pinned by an op-count probe measurement before finalization. The print-farm-schedule SHALL NOT impose any efficiency threshold.

#### Scenario: Print-farm first testcase equals statement example

- **WHEN** a judging run is assembled for print-farm-schedule
- **THEN** the first testcase input SHALL be the statement example and the run SHALL contain 20 testcases in declaration order (1 example literal, 9 warm-up, 8 stress, 2 boundary literals)

##### Example: Statement example pinned first

- **GIVEN** the first testcase of any run
- **WHEN** its input is compared to the statement example
- **THEN** it SHALL be exactly `2` / `4` / `2 3 5 7` with expected output `10`

#### Scenario: Pillbox first testcase equals statement example

- **WHEN** a judging run is assembled for pillbox-reminder
- **THEN** the first testcase input SHALL be the statement example and the run SHALL contain 20 testcases in declaration order (1 example literal, 9 warm-up, 8 stress, 2 boundary literals)

##### Example: Pillbox statement example pinned first

- **GIVEN** the first testcase of any run
- **WHEN** its input is compared to the statement example
- **THEN** it SHALL be exactly `2` / `3 5` / `6` with expected output lines `1 2 1 1 2 1`

##### Example: Single-reminder literal entry

- **GIVEN** Q=2, periods `7 9`, K=1
- **WHEN** the simulation runs
- **THEN** the output SHALL be the single line `1`

#### Scenario: Pillbox stress band rejects per-minute scanning

- **WHEN** a solution advances a clock minute-by-minute over a stress-band testcase (periods 30000–50000, K 300–400)
- **THEN** the judge SHALL report TLE for that testcase

#### Scenario: Pillbox stress band accepts event-driven solutions

- **WHEN** a solution computes successive minima over next-fire times (linear scan or heap) on any stress-band testcase
- **THEN** the judge SHALL report AC with an op count at least 20× below the 10M budget
