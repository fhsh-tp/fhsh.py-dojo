## MODIFIED Requirements

### Requirement: Testcase plan partitioning

The print-farm-schedule challenge SHALL declare a testcase_plan of exactly 20 entries per run: 10 warm-up band cases (hand-computable scale), 8 stress band cases, and 2 literal boundary entries covering the more-printers-than-jobs boundary and the single-job boundary. The pillbox-reminder challenge SHALL declare a testcase_plan of exactly 6 entries per run: 3 warm-up band cases, 2 stress band cases, and 1 literal entry covering the simultaneous-tie boundary. The pillbox-reminder stress band SHALL be shaped so that a per-minute time-axis scan exceeds the 10M op budget (TLE) while both a linear scan over next-fire times and a heap-based solution stay below 500k ops (≥20× margin); the concrete stress bounds SHALL be pinned by an op-count probe measurement before finalization. The print-farm-schedule SHALL NOT impose any efficiency threshold.

#### Scenario: Print-farm run size and literal boundaries

- **WHEN** a judging run is assembled for print-farm-schedule
- **THEN** it SHALL contain 20 testcases in declaration order (10 warm-up, then 8 stress, then 2 literals)

##### Example: Single-job literal entry

- **GIVEN** m=2, n=1, durations `7`
- **WHEN** the simulation runs
- **THEN** the output SHALL be `7`

#### Scenario: Pillbox stress band rejects per-minute scanning

- **WHEN** a solution advances a clock minute-by-minute over a stress-band testcase (periods 30000–50000, K 300–400)
- **THEN** the judge SHALL report TLE for that testcase

#### Scenario: Pillbox stress band accepts event-driven solutions

- **WHEN** a solution computes successive minima over next-fire times (linear scan or heap) on any stress-band testcase
- **THEN** the judge SHALL report AC with an op count at least 20× below the 10M budget
