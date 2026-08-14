# ball-drop-challenge Specification

## Purpose

TBD - created by archiving change 'add-exhibit-route-duo'. Update Purpose after archive.

## Requirements

### Requirement: Pinball track predict I/O contract
The challenge `pinball-track-predict` SHALL accept input of: first line integer T (T >= 1); then T lines each holding two integers `D I` with 2 <= D <= 17 and 1 <= I <= 10000000 (trace B1/B1b). The machine has D layers in total: layers 1 through D-1 hold flippers, layer k holding 2^(k-1) of them, every flipper initially pointing left; layer D is a row of 2^(D-1) bags numbered 1..2^(D-1) from left to right. A ball follows the direction of each flipper it meets and flips that flipper to the other side; after passing layer D-1 it falls into a bag. The wording SHALL NOT describe the machine as having D layers of flippers, which would imply 2^D bags and make the walk length ambiguous (trace B1). The ball count MAY exceed the bag count: the machine state is periodic with period 2^(D-1), so bag(D, I) equals bag(D, ((I-1) mod 2^(D-1)) + 1) and the problem is well defined for every I (trace B1b). Every prediction SHALL be evaluated on a freshly reset machine, and each line SHALL produce exactly one output line holding the bag number.

#### Scenario: Four-layer machine, first period and beyond
- **GIVEN** the lines `4 1`, `4 2`, `4 3`, `4 8`, `4 11`
- **WHEN** each prediction is evaluated
- **THEN** the outputs are `1`, `5`, `3`, `8`, `3` (the first period fills the bags in the order 1,5,3,7,2,6,4,8 and ball 11 repeats ball 3)

#### Scenario: Smallest machine
- **GIVEN** the lines `2 1` and `2 2`
- **WHEN** each prediction is evaluated
- **THEN** the outputs are `1` and `2`

#### Scenario: Ball count beyond the bag count
- **GIVEN** a line whose I exceeds 2^(D-1)
- **WHEN** the prediction is evaluated
- **THEN** the output equals the output for ball ((I-1) mod 2^(D-1)) + 1

---
### Requirement: Pinball track predict testcase plan
The challenge `pinball-track-predict` SHALL declare a 20-entry all-literal `testcase_plan` and SHALL NOT declare `input_budget` (every entry is at most 51 bytes; trace B10). Entries 1-15 SHALL each total at most 1,000,000 ball-steps (measured maximum 994,999), so every per-ball style passes. Entries 16-20 SHALL each total at least 15,000,000 balls (measured minimum 15,464,112) and at most 70,000,000 ball-steps (measured maximum 67,440,568). The ball floor is what kills per-ball simulation; there SHALL be no step floor, because the per-testcase soft wall flag never fires for synchronous code and piling on steps only lengthens a doomed submission's wait toward the cumulative kill (trace C3/C4b/B5b). Every entry SHALL hold at least two lines with no repeated `D I` pair, SHALL contain at least one line with I >= 2, and SHALL contain at least one line whose bag number differs from I, from 1, from 2^(D-1) and from the period-reduced ball number (trace B9/B9b). In the killer band every single line with I above 100,000 SHALL additionally satisfy, line by line, that I is not a multiple of 2^(D-1), that its bag is not 2^(D-1), that its bag is not the period-reduced ball number, and that its period is at least 16 — a per-entry existential check is not sufficient, and a period of 8 or less leaves so few admissible residues that the answer collapses into a function of I modulo 2 or 4, which a two-line guess reproduces exactly (trace B9b/R2-1). Each killer entry SHALL also contain at least one line with I above 100,000 whose period equals the largest period the declared range admits, so that a solution hardcoding a fixed modulus is discriminated; the assertion wall SHALL verify the whole fixed-period family, exempting only moduli at or above 2^(17-1), the largest period of the declared range. Keying the exemption on the shipped data instead of the range lets a modulus that merely happens to cover the shipped lines pass while being wrong inside the stated range (trace B9c/R2-2). Every entry SHALL keep the sum of 2^(D-1) over its lines at or below 600,000 (measured maximum 98,368) and the modelled cost of the period route at or below 8,000,000 traced ops (measured maximum 6,469,478), where that model assumes the most expensive reasonable spelling — simulating a whole period to build a lookup table, whose cost is independent of the ball number — because modelling it as min(ball number, period) would kill exactly the spelling that carries the intended insight (trace B8). Entry 1 SHALL be byte-identical to the worked example on the challenge page and SHALL by itself expose the echo, constant, no-reverse, flipped-parity and extra-layer misreadings. The plan SHALL cover D = 2, D = 17, I = 1, I = 2^(D-1) and I > 2^(D-1). All literal content SHALL be produced by `curation/plan014.py` from `curation/semantics014.py` and embedded byte-for-byte by `curation/assemble.py` (trace C8).

#### Scenario: Assertion wall blocks shipping
- **GIVEN** any change to the entry table in `curation/plan014.py`
- **WHEN** `python3 plan014.py` runs
- **THEN** it recomputes ball and step totals, both accepted routes' cost models, the per-line degeneracy checks, the fixed-period family, every wrong-route score and the boundary coverage, and exits non-zero without writing literals if any contract is violated

#### Scenario: Degenerate killer data is rejected
- **GIVEN** a killer entry whose large-I lines all sit on multiples of the period, so every answer is the rightmost bag
- **WHEN** the assertion wall runs
- **THEN** it names those lines and exits non-zero, because a solution that prints the rightmost bag for any large ball number would otherwise score 20/20

---
### Requirement: Pinball track predict cost ladder and bypass disposition
Per-ball simulation SHALL score exactly 15/20 for every spelling that executes at least one traced line per ball. Three such spellings were measured on the shipped block by `curation/cost_gate.mjs`, which replays each route through the judge's own tracer and applies the operation limit: the ordinary style, the single-line-loop style and a per-D flattened single-ball style all pass entries 1-15 and trip on entries 16-20 (measured whole-block wall times 17.2, 25.3 and 29.0 seconds; trace B3/B6). The value range 1 <= I <= 10000000 is load-bearing: under the older range I <= 2^(D-1) no entry composition can separate per-ball simulation from the accepted level-wise route (trace B4). Two routes are ACCEPTED ALTERNATIVES and SHALL keep scoring 20/20, each verified in more than one spelling because a co-opted route's budget must come from its most expensive reasonable spelling: level-wise counting over the whole machine (terse and recursive spellings, both checked in `curation/cost_gate.mjs`; the recursive one measures about 13 traced ops per flipper and sets the 600,000-flipper cap) and period reduction followed by simulation (ordinary and bitfield spellings, likewise both checked). The budget for the period route is nevertheless modelled on a spelling nobody checked in — simulating a whole period to build a lookup table, whose cost does not shrink with the ball number — because a budget taken from the cheaper spellings would kill that one (trace B8/B8b). The `generator` SHALL stay within 1,000 traced ops on every shipped entry (measured maximum 234) and the `reference_solution` likewise (measured maximum 146), implemented independently of each other — parity descent versus period reduction plus reversed reading (trace B2/B10). Two evasions of the operation counter are KNOWN RESIDUES that no test data can close and that SHALL NOT be worked around by weakening or inflating the data: batching K balls onto one source line reduces the traced cost to one operation per K balls, and calling `sys.settrace(None)` freezes the counter outright; the per-testcase soft wall flag cannot catch either, because it never fires for synchronous Python (trace C3/C12/C13/B3b). Both are recorded for a separate engine-level change and apply to every operation-limited challenge already on the site. The challenge page SHALL NOT claim any route impossible and its performance reminder SHALL be limited to the measured statement about per-ball simulation spellings.

#### Scenario: Every per-ball spelling with a traced line per ball dies on the killer band
- **GIVEN** a solution that simulates ball by ball from the first ball, in the ordinary, compacted, or single-ball-flattened spelling
- **WHEN** it is judged against the full 20-entry block
- **THEN** it passes entries 1-15 and receives TLE on entries 16-20, scoring 15/20

#### Scenario: Accepted alternatives survive in every spelling
- **GIVEN** a solution that counts balls level by level over the whole machine (terse, beginner or recursive), or one that reduces the ball number by the period and then simulates (ordinary or bitfield)
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores 20/20

#### Scenario: Guessing the rightmost bag for large ball numbers earns no advantage
- **GIVEN** a solution that prints 2^(D-1) whenever I exceeds a threshold and simulates otherwise
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores at most 15/20, no better than honest per-ball simulation

---
### Requirement: Shared authoring constraints for the exhibit route duo
Both challenges SHALL be `category: apcs`, `type: competition`, with `exhibit-route-rebuild` at `difficulty: medium` and `pinball-track-predict` at `difficulty: hard`, and their ids SHALL be assigned by the `pnpm new-challenge` scaffold rather than hand-written (trace C10). Both pages, both slugs and both `algorithm` values SHALL be free of data-structure and algorithm terminology; `curation/assemble.py` SHALL enforce this with a banned-term check over the assembled document, the slug and the algorithm value, and SHALL refuse to write a file on any hit (trace D6). Both challenges SHALL declare a `reference_solution` implemented independently of the `generator` and verified by `scripts/content-regression.test.ts`, and both `starter_code` fields SHALL be the empty string so the editor loads blank (maintainer decision 2026-08-06). Neither page SHALL contain a number that is not traceable to a fact ID in `trace-matrix.md`. Production builds strip only `generator` and `reference_solution`, so the literal test inputs of both challenges reach the client bundle and are in any case public in the repository; this is a pre-existing project-level residue shared with the earlier all-literal challenges, is recorded as such, and SHALL NOT be worked around by weakening the test data (trace C11).

#### Scenario: Banned term blocks assembly
- **GIVEN** a page draft or a generator identifier containing a banned term
- **WHEN** `python3 assemble.py` runs
- **THEN** it aborts with the offending terms listed and writes no challenge file

#### Scenario: Content regression covers both challenges
- **GIVEN** both challenges declare generator and reference_solution
- **WHEN** `scripts/content-regression.test.ts` runs against the built production pools
- **THEN** both reference solutions match their generator's expected output on all sampled entries
