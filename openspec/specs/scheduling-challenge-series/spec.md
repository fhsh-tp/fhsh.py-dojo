# scheduling-challenge-series Specification

## Purpose

TBD - created by archiving change 'add-scheduling-challenges'. Update Purpose after archive.

## Requirements

### Requirement: Print-farm dispatch semantics

The print-farm-schedule challenge SHALL define the following simulation: given m printers (numbered 1..m) and n jobs arriving in input order with integer durations, each job SHALL be assigned to the printer whose next-free time is earliest; when multiple printers share the earliest next-free time, the printer with the smallest number SHALL take the job. A printer SHALL run each assigned job contiguously starting at its next-free time. The expected output SHALL be a single integer on one line: the maximum completion time across all printers (makespan), measured from t=0.

#### Scenario: Sequential dispatch with tie at start

- **WHEN** all printers are free at t=0 and a job arrives
- **THEN** printer 1 SHALL take the job (smallest number wins the tie)

##### Example: Two printers, four jobs

- **GIVEN** m=2, n=4, durations `2 3 5 7`
- **WHEN** jobs are dispatched in input order
- **THEN** job1→printer1 (0–2), job2→printer2 (0–3), job3→printer1 (2–7), job4→printer2 (3–10), and the output SHALL be `10`

#### Scenario: More printers than jobs

- **WHEN** m exceeds n
- **THEN** every job SHALL start at t=0 on distinct printers and the output SHALL equal the maximum single duration

##### Example: Literal boundary entry

- **GIVEN** m=3, n=2, durations `5 9`
- **WHEN** the simulation runs
- **THEN** the output SHALL be `9`

---
### Requirement: Pillbox periodic event semantics

The pillbox-reminder challenge SHALL define the following simulation: Q medicines are registered in input order and the i-th registered medicine SHALL have the implicit ID i (1..Q); the input SHALL NOT contain explicit IDs. Medicine i with period p_i SHALL fire reminder events at minutes p_i×1, p_i×2, p_i×3, and so on. The expected output SHALL be the IDs of the first K events ordered by (time ascending, ID ascending), printed one ID per line, exactly K lines. Events at the same minute SHALL be ordered by ascending ID.

#### Scenario: Interleaved periods

- **WHEN** two medicines with different periods fire at distinct times
- **THEN** the output SHALL list IDs in strict firing-time order

##### Example: Periods 3 and 5

- **GIVEN** Q=2, periods `3 5`, K=6
- **WHEN** events fire at t=3(#1), 5(#2), 6(#1), 9(#1), 10(#2), 12(#1)
- **THEN** the output SHALL be the six lines `1`, `2`, `1`, `1`, `2`, `1`

#### Scenario: Simultaneous events tie-break

- **WHEN** multiple medicines fire at the same minute
- **THEN** their IDs SHALL be printed in ascending order before any later event

##### Example: Triple tie via literal entry

- **GIVEN** Q=3, periods `2 3 6`, K=12
- **WHEN** t=6 and t=12 each fire all three medicines simultaneously
- **THEN** the output SHALL be the twelve lines `1 2 1 1 2 3 1 2 1 1 2 3` (shown space-joined; each ID on its own line)

---
### Requirement: Input format contracts

The print-farm-schedule stdin SHALL be exactly three lines: line 1 the integer m, line 2 the integer n, line 3 the n durations space-separated. The pillbox-reminder stdin SHALL be exactly three lines: line 1 the integer Q, line 2 the Q periods space-separated, line 3 the integer K. Numeric list lines SHALL use a single space as separator, produced by the params engine count.from mechanism.

#### Scenario: Params engine renders one block per parameter

- **WHEN** the testcase generator renders a testcase for either challenge
- **THEN** each declared parameter SHALL occupy its own line and list parameters SHALL render space-separated on a single line

---
### Requirement: Testcase plan partitioning

The print-farm-schedule challenge SHALL declare a testcase_plan of exactly 20 entries per run, in this declaration order: 1 statement-example literal entry first (m=2, n=4, durations `2 3 5 7`), then 9 warm-up band cases (hand-computable scale), then 8 stress band cases, then 2 literal boundary entries covering the more-printers-than-jobs boundary and the single-job boundary. The pillbox-reminder challenge SHALL declare a testcase_plan of exactly 6 entries per run, in this declaration order: 1 statement-example literal entry first (Q=2, periods `3 5`, K=6), then 2 warm-up band cases, then 2 stress band cases, then 1 literal entry covering the simultaneous-tie boundary. For both challenges the first entry SHALL be the statement example so that the run panel's default stdin (derived from the first testcase) equals the worked example in the statement. The pillbox-reminder stress band SHALL be shaped so that a per-minute time-axis scan exceeds the 10M op budget (TLE) while both a linear scan over next-fire times and a heap-based solution stay below 500k ops (≥20× margin); the concrete stress bounds SHALL be pinned by an op-count probe measurement before finalization. The print-farm-schedule SHALL NOT impose any efficiency threshold.

#### Scenario: Print-farm first testcase equals statement example

- **WHEN** a judging run is assembled for print-farm-schedule
- **THEN** the first testcase input SHALL be the statement example and the run SHALL contain 20 testcases in declaration order (1 example literal, 9 warm-up, 8 stress, 2 boundary literals)

##### Example: Statement example pinned first

- **GIVEN** the first testcase of any run
- **WHEN** its input is compared to the statement example
- **THEN** it SHALL be exactly `2` / `4` / `2 3 5 7` with expected output `10`

#### Scenario: Pillbox first testcase equals statement example

- **WHEN** a judging run is assembled for pillbox-reminder
- **THEN** the first testcase input SHALL be the statement example and the run SHALL contain 6 testcases in declaration order (1 example literal, 2 warm-up, 2 stress, 1 tie literal)

##### Example: Pillbox statement example pinned first

- **GIVEN** the first testcase of any run
- **WHEN** its input is compared to the statement example
- **THEN** it SHALL be exactly `2` / `3 5` / `6` with expected output lines `1 2 1 1 2 1`

#### Scenario: Pillbox stress band rejects per-minute scanning

- **WHEN** a solution advances a clock minute-by-minute over a stress-band testcase (periods 30000–50000, K 300–400)
- **THEN** the judge SHALL report TLE for that testcase

#### Scenario: Pillbox stress band accepts event-driven solutions

- **WHEN** a solution computes successive minima over next-fire times (linear scan or heap) on any stress-band testcase
- **THEN** the judge SHALL report AC with an op count at least 20× below the 10M budget


<!-- @trace
source: pin-pillbox-example-first
updated: 2026-08-02
code:
  - docs/challenge/pillbox-reminder.md
-->

---
### Requirement: Literacy statement and dual-implementation validation

Both challenge statements and tags SHALL describe only the real-world processing pattern and SHALL NOT contain solution-revealing vocabulary (Chinese equivalents of: sort, queue, stack, heap, priority, scan, time-axis simulation, data structure). Tags SHALL be exactly 模擬 and 排程. Each challenge SHALL declare a reference_solution implemented with a strategy different from its generator (scanning vs heapq), and content-regression SHALL verify the reference_solution produces expected output on the production pool.

#### Scenario: Statement audit finds no forbidden vocabulary

- **WHEN** the challenge markdown body and tags are checked against the forbidden vocabulary list
- **THEN** zero occurrences SHALL be found

#### Scenario: Cross-validation via different implementations

- **WHEN** content-regression runs the reference_solution against the production pool
- **THEN** every testcase SHALL match the generator-produced expected output