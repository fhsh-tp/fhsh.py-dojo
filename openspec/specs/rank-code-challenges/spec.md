# rank-code-challenges Specification

## Purpose

TBD - created by archiving change 'add-rank-code-challenge-duo'. Update Purpose after archive.

## Requirements

### Requirement: rank-code-backfill challenge contract

The site SHALL provide a challenge `rank-code-backfill` (category `apcs`, type `competition`, difficulty `medium`) whose input is a first line integer T (1 ≤ T ≤ 500) followed by T lines each containing one integer N (1 ≤ N ≤ 200000), and whose expected output is T lines, where line i is the last non-zero digit of N_i! (the product 1×2×…×N_i with all trailing zeros removed, then the last digit).

#### Scenario: input and output shape

- **GIVEN** a generated testcase with T queries
- **WHEN** the generator computes expected output
- **THEN** it emits exactly T lines, each a single digit in 1..9

##### Example:

| Input | Output |
|-------|--------|
| `3` / `5` / `1` / `10` | `2` / `1` / `8` |

(5! = 120 → strip trailing zeros → 12 → digit 2; 1! = 1 → 1; 10! = 3628800 → 36288 → 8.)


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: prize-order-code challenge contract

The site SHALL provide a challenge `prize-order-code` (category `apcs`, type `competition`, difficulty `hard`) whose input is a first line integer T (1 ≤ T ≤ 3) followed by T pairs of lines, pair i containing N_i (100000 ≤ N_i ≤ 1000000000 for generated bands; literals are permitted to use 1 ≤ N_i) and M_i (0 ≤ M_i ≤ 100000, with M_i ≤ N_i in every testcase), and whose expected output is T lines, where line i is the last non-zero digit of N_i×(N_i−1)×…×(N_i−M_i+1), and the empty product (M_i = 0) yields 1.

#### Scenario: M ≤ N holds by construction

- **GIVEN** generated band parameters with N_min = 100000 and M_max = 100000
- **WHEN** any band testcase is produced
- **THEN** M_i ≤ N_i holds without a runtime constraint solver; small-N cases are covered exclusively by literals

##### Example:

| Input | Output |
|-------|--------|
| `3` / `10` / `2` / `25` / `1` / `7` / `0` | `9` / `5` / `1` |

(P(10,2) = 90 → 9; P(25,1) = 25 → 5, the excess-fives trap; M = 0 → empty product → 1.)


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: answer semantics including factor bookkeeping

The generator and the reference solution SHALL compute the last non-zero digit by tracking the balance of stripped factor-2 counts over factor-5 counts across the multiplied range (either as two separate counts or as a single net difference): with b = c2 − c5 that balance and r the remaining product mod 10, the answer SHALL be r×2^b mod 10 when b > 0, exactly 5 when b < 0, and r when b = 0. For rank-code-backfill (full factorials) the balance never goes negative, and the per-query answers SHALL be produced incrementally in a single ascending pass (whether or not an explicit table is materialized).

#### Scenario: excess fives

- **GIVEN** a range whose factor-5 count exceeds its factor-2 count (e.g. the single term 25)
- **WHEN** the expected answer is computed
- **THEN** the emitted digit is 5


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: TLE cliff via op counter

Each challenge's testcase plan SHALL include pressure testcases on which the naive recomputation strategy exceeds 2× the judge op limit (rank-code-backfill: per-query O(N) recomputation, measured ≥10M ops within the first 20 of 500 queries; prize-order-code: full 1..N product loops at N ≥ 10^8), while the intended solution — measured as the shipped reference_solution verbatim — stays at or below 1/4 of the op limit (measured at most 1,556,493 and 2,325,097 ops respectively at the heaviest corners).

#### Scenario: intended solution headroom

- **GIVEN** the heaviest generated testcase of either challenge
- **WHEN** the shipped reference_solution (the measured intended-solution proxy) runs under the judge's op counter
- **THEN** its op count is at most 2,500,000 (op limit 10,000,000 divided by 4)


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: C-builtin bypass lethality

The testcase plans SHALL contain enough pressure testcases that each bypass enumerated in design D6.a fails: per-query math.factorial (and its math.perm sibling) for rank-code-backfill and un-modded Python-level big-integer products for prize-order-code SHALL exceed 2× the executor total wall budget (native measurement multiplied by conservative factor 2 for Pyodide), and the str()-based digit extraction path SHALL raise ValueError under int_max_str_digits=4300. Verification SHALL be recorded per-bypass in dev-verification-notes.md; bypasses outside the D6.a list are out of scope. The math.perm-with-Legendre trailing-zero route is a documented surviving alternative solution for prize-order-code (matrix F19/F20, design D6.b); it SHALL NOT be treated as a defect, and testcase plans SHALL NOT be tuned against it at the cost of the intended-solution headroom required by the TLE-cliff requirement.

#### Scenario: stringify path dies

- **GIVEN** a student solution that builds the full product and calls str() on it
- **WHEN** it runs on any pressure testcase of prize-order-code
- **THEN** the conversion raises ValueError (result exceeds 4300 digits)

#### Scenario: accepted residual bypass

- **GIVEN** the prize-order-code surviving route recorded in design D6.b (math.perm with Legendre trailing-zero counting)
- **WHEN** it runs on the production pool
- **THEN** it is accepted (20/20 AC) and reported as an accepted alternative, not as a regression or defect


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: independent reference solutions

Each challenge SHALL declare a `reference_solution` implemented independently from its generator (a materially different implementation strategy), and `scripts/content-regression.test.ts` SHALL pass for both challenges against the production encrypted pools.

#### Scenario: regression gate

- **GIVEN** the built production pools
- **WHEN** content-regression runs
- **THEN** both reference solutions produce byte-identical expected output for all 20 testcases of their challenge


<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->

---
### Requirement: literacy-style problem statements

Both problem statements SHALL be set in the shared game-leaderboard universe, open with a check-digit literacy hook (e.g. ISBN or national ID check digits), present the counted quantity as an expanded product (N×(N−1)×…), state input ranges explicitly including a warning that some testcases contain very large values, use the first literal testcase verbatim as the worked example, and SHALL NOT contain any data-structure or algorithm terminology.

#### Scenario: terminology ban

- **GIVEN** either rendered problem statement
- **WHEN** scanned for banned terms (stack, queue, 堆疊, 佇列, 資料結構, 演算法, 動態規劃, 記憶化)
- **THEN** none appear in the statement body

<!-- @trace
source: add-rank-code-challenge-duo
updated: 2026-08-06
code:
  - scripts/_audit_dump_pool.ts
-->