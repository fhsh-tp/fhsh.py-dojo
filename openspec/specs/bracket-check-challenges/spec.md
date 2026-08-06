# bracket-check-challenges Specification

## Purpose

TBD - created by archiving change 'add-bracket-check-duo'. Update Purpose after archive.

## Requirements

### Requirement: Prop-box packing check challenge (1a) I/O contract
The challenge `prop-box-packing` SHALL accept input of: first line integer T (1 <= T <= 5), followed by T lines, each a record string of length 1..62000 containing only characters from `()[]{}` (trace C7). For each record the output SHALL be exactly one line: `OK` when the record is fully matched, `NG` otherwise (trace A1/A2). A record is fully matched when scanning left to right, every closing character pairs with the nearest unpaired opening character of the same kind, and no opening character remains unpaired at the end (trace A1).

#### Scenario: Interleaved kinds are rejected
- **GIVEN** the record `([)]`
- **WHEN** the record is checked
- **THEN** the output line is `NG` (the `)` at scan time pairs against `[`, kind mismatch)

#### Scenario: Nested and concatenated mix is accepted
- **GIVEN** the record `([{}])()`
- **WHEN** the record is checked
- **THEN** the output line is `OK`

#### Scenario: Leftover opener is rejected
- **GIVEN** the record `(((`
- **WHEN** the record is checked
- **THEN** the output line is `NG`

---
### Requirement: Prop-box packing testcase plan
The challenge `prop-box-packing` SHALL declare a 20-entry `testcase_plan` with `input_budget: 63488` (trace C3/C4) whose bracket-kind bands are: entries 1-3 use only `()`, entries 4-12 use only `()[]`, entries 13-20 may use `()[]{}`  (trace C5). Entry 1 SHALL be a literal identical to the worked example shown in the challenge page (trace C6). Entries 4, 9, 12, 15, 18 SHALL each be a short literal containing at least one interleave trap that fools per-kind counting, and entries 17 and 19 SHALL be long trap literals (~28K and ~35K characters: a seeded random balanced string with an interleave pattern injected mid-string, keeping per-kind counts balanced and running counts non-negative), so that counting-only solutions first fail at entry 4 and fail on exactly the seven entries 4, 9, 12, 15, 17, 18, 19 (trace A3). The traps SHALL cover both adjacency types: adjacent traps (`([)]` / `[(])` / `(([))]` / `{[}]` / `([{)]}` families) and non-adjacent traps (`([())]` / `{[{}}]` families, where the violating closer's preceding character is another closer) placed in entries 9 and 15 and injected into both long traps, so that neither hybrid short-line-only checkers (trace A9) nor count-plus-bad-bigram C-level shortcuts can reach 20/20 (trace A3/A9). Entry 20 SHALL be a literal stress case: a mixed-kind deep nest of depth 31000 (~62KB) (trace A6). Random band entries SHALL use enum-soup generation with per-band `values`/`count` overrides, and every band SHALL contain at least one literal whose expected verdict is `OK` (trace C8/A7/A8).

#### Scenario: Counting-only solution fails on exactly the seven trap entries
- **GIVEN** a solution that only counts opens/closes per kind with a non-negative running check
- **WHEN** it is judged against a full 20-entry run
- **THEN** it first fails at entry 4 and fails on exactly entries 4, 9, 12, 15, 17, 18, 19, scoring 13/20 (on random soup entries the counter coincidentally agrees with the truth; only balanced-but-interleaved traps — short and long — expose it) (trace A3)

---
### Requirement: Prop-box packing performance envelope and bypass disposition
The reference stack-scan solution SHALL stay within 2,500,000 traced ops on the worst entry (measured 217,022 ops at 62KB, trace A5). C-backed shrink routes (repeated `str.replace` loop; find-and-slice deletion loop) are ACCEPTED ALTERNATIVES: measured against the shipped entry-20 literal (mixed-kind depth 31000) at 62,018 ops / 2.1s native and 310,030 ops / 1.4s native respectively, below the op limit and not economically wall-killable within the 65536-byte input hard cap (even 20 all-stress entries would cost ~70s in Pyodide, under the 120s budget); the single-kind `()` shape at the same depth is this route's worse case (93,017 ops / 5.5s native), kept only as a conservative upper bound (trace A4). The challenge page SHALL NOT claim any route is impossible; it SHALL make no performance promises beyond measured facts (trace A4).

#### Scenario: Deep-nest stress does not kill the reference
- **GIVEN** the 62KB depth-31000 stress literal of entry 20
- **WHEN** the reference solution runs under the 10M op limit
- **THEN** it completes with at most 2,500,000 traced ops and millisecond-scale wall time

---
### Requirement: Magazine typeset check challenge (1b) I/O contract
The challenge `magazine-typeset-check` SHALL accept input of: first line integer T (1 <= T <= 5), followed by T lines, each a manuscript string of length 1..62000 that mixes noise characters (lowercase letters, digits, `.,;` — no spaces, to keep `input().strip()` harmless) with brackets from `()[]{}`  (trace C7/B3). For each manuscript the output SHALL be exactly one line containing a single integer: the 1-based position (counting every character of the original string, noise included) of the first pairing failure, or `0` when all brackets pair (trace B1/B2). The first pairing failure SHALL be resolved by exactly three branches (trace B1): (i) scanning left to right, the first closing bracket that arrives when no unpaired opener exists or the nearest unpaired opener has a different kind -> output that closing bracket's position; (ii) if scanning completes with unpaired openers remaining -> output the position of the earliest unpaired opener; (iii) otherwise -> output 0.

#### Scenario: Mismatched closer position is reported
- **GIVEN** the manuscript `x([y)z]`
- **WHEN** the manuscript is checked
- **THEN** the output is `5` (the `)` at position 5 arrives while the nearest unpaired opener is `[`)

#### Scenario: Earliest leftover opener position is reported
- **GIVEN** the manuscript `((a`
- **WHEN** the manuscript is checked
- **THEN** the output is `1` (both openers unpaired; the earliest is at position 1)

#### Scenario: Manuscript without brackets is clean
- **GIVEN** a manuscript containing no bracket characters
- **WHEN** the manuscript is checked
- **THEN** the output is `0` (trace B7)

---
### Requirement: Magazine typeset testcase plan
The challenge `magazine-typeset-check` SHALL declare a 20-entry `testcase_plan` with `input_budget: 63488` following the same bracket-kind bands as 1a (entries 1-3 `()`, 4-12 `()[]`, 13-20 `()[]{}`; noise characters allowed in every entry) (trace C4/C5/B3). Entry 1 SHALL be a literal identical to the challenge page's worked example (trace C6). Entries 14, 15, 16, 18, 19, 20 SHALL be six pairwise-distinct killer literals from the irregular mixed-kind noisy family (seeded random warmup of noise and complete pairs; leftover killers bury one unpaired opener U after the warmup so the expected answer equals U's non-formulaic position; then m mixed-kind outer openers, k mixed-kind inner pairs and reversed closers, all with sprinkled noise) with parameters (seed,m,k,leftover->answer): K14(1414,2000,5000,->29), K15(1515,2000,6250,->27), K16(1616,2000,5000,0), K18(1818,2500,4000,->18), K19(1919,1600,6250,0), K20(2020,2000,5000,->23); every killer SHALL satisfy the lean-ops lower bound m*2k >= 20,000,000, force a full-line scan (no early mismatch), and expose no uniform-run shape signature that would let a shape-detecting shortcut skip the scan (trace B4/B8). One entry SHALL be a literal containing at least one manuscript line with no bracket characters at all (whose expected output is 0) (trace B7). Random band entries SHALL use enum-soup generation whose value set mixes the band's bracket kinds with the noise set (lowercase letters, digits, `.,;`; no spaces) (trace B8/C8).

#### Scenario: Backward-scan naive dies on every killer entry
- **GIVEN** a solution that, for each closing bracket, linearly scans backward for the nearest unmatched opener
- **WHEN** it is judged against a full 20-entry run
- **THEN** it exceeds the 10,000,000 op limit exactly on entries 14, 15, 16, 18, 19, 20 and scores 14/20 — including the leanest 1-op-per-iteration variant (measured minimum 23,190,670 ops on K19) (trace B4)

---
### Requirement: Magazine typeset performance envelope
The reference stack-scan solution SHALL stay within 2,500,000 traced ops on the worst entry (measured 100,789 ops for the reference_solution on the largest shipped killer K15; the generator measures 67,337 ops on the same entry; both far below the threshold, trace B5). Pure character-deletion shrink routes lose original positions, but the equal-length whiteout variant (replacing matched adjacent pairs with same-length filler via C-level replace loops, then scanning the residue) is a measured ACCEPTED ALTERNATIVE (20/20, ~51K ops and 0.17s native on killer entries); neither rationale SHALL appear as an impossibility claim in the challenge page (trace B6).

#### Scenario: Killer literals do not kill the reference
- **GIVEN** the six killer literals
- **WHEN** the reference solution runs under the 10M op limit
- **THEN** every killer entry completes within 2,500,000 traced ops with the expected outputs 29/27/0/18/0/23 for entries 14/15/16/18/19/20

---
### Requirement: Shared authoring constraints for the bracket duo
Both challenge pages SHALL use their life scenarios (1a theater prop-box packing log; 1b school-magazine typesetting checker) without any data-structure terminology (no stack/堆疊/樹 or algorithm-name keywords) (trace C1, batch requirement). Both challenges SHALL be `category: apcs`, `type: competition`, `difficulty: medium` (trace C2), and SHALL declare a `reference_solution` implemented independently from the `generator` (different data layout), verified by the content-regression suite (trace C9). Both starter_code blocks SHALL read the input but emit no output, so an unmodified submission scores 0/20 (trace C10). The 1b challenge page's performance reminder SHALL be limited to the measured-true claim about per-character backward rescanning loops and SHALL NOT promise any route impossible (trace B10). Challenge ids SHALL be assigned by the `pnpm new-challenge` scaffold, never hand-written (trace C1).

#### Scenario: Content regression passes for both challenges
- **GIVEN** both challenges declare generator and reference_solution
- **WHEN** `scripts/content-regression.test.ts` runs against the built production pools
- **THEN** both reference solutions' outputs match the generators' expected outputs on all sampled entries
