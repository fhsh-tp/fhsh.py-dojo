## ADDED Requirements

### Requirement: Pinball track predict I/O contract
The challenge `pinball-track-predict` SHALL accept input of: first line integer T (T >= 1); then T lines each holding two integers `D I` with 2 <= D <= 20 and 1 <= I <= 10000000 (trace B1/B1b). The machine has D layers in total: layers 1 through D-1 hold flippers, layer k holding 2^(k-1) of them, every flipper initially pointing left; layer D is a row of 2^(D-1) bags numbered 1..2^(D-1) from left to right. A ball follows the direction of each flipper it meets and flips that flipper to the other side; after passing layer D-1 it falls into a bag. The wording SHALL NOT describe the machine as having D layers of flippers, which would imply 2^D bags and make the walk length ambiguous (trace B1). The ball count MAY exceed the bag count: the machine state is periodic with period 2^(D-1), so bag(D, I) equals bag(D, ((I-1) mod 2^(D-1)) + 1) and the problem is well defined for every I (trace B1b). Every prediction SHALL be evaluated on a freshly reset machine, and each line SHALL produce exactly one output line holding the bag number.

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
The challenge `pinball-track-predict` SHALL declare a 20-entry all-literal `testcase_plan` and SHALL NOT declare `input_budget` (every entry is at most 50 bytes; trace B10). Entries 1-14 SHALL each total at most 1,000,000 ball-steps, where a ball-step is one ball descending one layer (measured maximum 994,999), so that every per-ball style passes. Entries 15-20 SHALL each total at least 20,000,000 balls (measured minimum 20,051,251) and at most 45,000,000 ball-steps (measured maximum 40,985,330): the ball floor is what kills per-ball simulation and the step ceiling is what keeps a doomed submission's total wall time far below the cumulative kill budget (trace B5/B7/C4b). Every entry SHALL hold at least two lines with no repeated `D I` pair, so that answering only the first line scores 0/20 and a memo dictionary cannot halve the cost; SHALL contain at least one line with I >= 2; and SHALL contain at least one line whose bag number differs from I, from 1, from 2^(D-1) and from the period-reduced ball number, so no zero-insight constant or echo route can clear it (trace B9/B9b). Note that bag(D, I) equals I exactly when (I-1) is a palindrome over D-1 bit positions, which is why entries may not consist solely of such lines. Every entry in the killer band SHALL keep its largest period-reduced ball count at or below 100,000, so the accepted period-reduction route keeps passing (trace B8). Entry 1 SHALL be byte-identical to the worked example on the challenge page and SHALL by itself expose the echo, constant, no-reverse, flipped-parity and extra-layer misreadings. The plan SHALL cover D = 2, D = 20, I = 1, I = 2^(D-1) and I > 2^(D-1). All literal content SHALL be produced by `curation/plan014.py` from `curation/semantics014.py` and embedded byte-for-byte by `curation/assemble.py` (trace C8).

#### Scenario: Assertion wall blocks shipping
- **GIVEN** any change to the entry table in `curation/plan014.py`
- **WHEN** `python3 plan014.py` runs
- **THEN** it recomputes ball and step totals, the accepted routes' cost models, every wrong-route score and the boundary coverage, and exits non-zero without writing literals if any contract is violated

---
### Requirement: Pinball track predict cost ladder and bypass disposition
Per-ball simulation SHALL score exactly 14/20. The bound SHALL be derived from the cheapest style the op counter can be made to see rather than a typical one: because the counter records one event per executed source line, a per-ball descent flattened onto a single line costs about one traced op per ball, roughly twenty times less than the compact-loop style (trace C2/B3). All three styles were measured on the shipped block and all three pass entries 1-14 and trip on entries 15-20: the ordinary style (worst entry 2,526 ms, whole block 23,061 ms), the single-line-loop style (5,021 / 33,480 ms) and a per-D flattened adversarial style (5,066 / 27,759 ms) (trace B6). The value range 1 <= I <= 10000000 is load-bearing: under the older range I <= 2^(D-1) no entry composition can separate per-ball simulation from the accepted level-wise route, because the latter costs about four times more per line and trips first (trace B4). Two routes are ACCEPTED ALTERNATIVES and SHALL keep scoring 20/20: level-wise counting over the whole machine, whose budget SHALL be computed from its most expensive reasonable spelling rather than its tersest (explicit if/else, measured 3,932,655 ops and 1,038 ms on the worst shipped entry), and period reduction followed by simulation of the reduced ball count (measured 4,683,393 ops and 1,110 ms) (trace B8). The `generator` and the `reference_solution` SHALL each stay within 1,000 traced ops on every shipped entry (measured maximum 200), implemented independently of each other — parity descent versus period reduction plus reversed reading (trace B2/B10). The challenge page SHALL NOT claim any route impossible; its performance reminder SHALL state only the measured fact that per-ball simulation, including compacted and flattened spellings, exceeds the operation limit on the later entries.

#### Scenario: Every per-ball spelling dies on the killer band
- **GIVEN** a solution that simulates ball by ball from the first ball, in the ordinary, compacted, or flattened spelling
- **WHEN** it is judged against the full 20-entry block
- **THEN** it passes entries 1-14 and receives TLE on entries 15-20, scoring 14/20

#### Scenario: Accepted alternatives survive
- **GIVEN** a solution that counts balls level by level over the whole machine, or one that reduces the ball number by the period and then simulates
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores 20/20

#### Scenario: Doomed submission stays inside the cumulative budget
- **GIVEN** the most expensive doomed per-ball spelling
- **WHEN** it runs the whole 20-entry block
- **THEN** its total wall time stays far below the cumulative kill budget of testcase count times 6,000 ms (measured 33,480 ms against 120,000 ms), so the run finishes and reports a real score instead of being terminated mid-block

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
