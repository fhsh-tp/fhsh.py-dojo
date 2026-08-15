## ADDED Requirements

### Requirement: Access point layout plan I/O contract
The challenge `ap-layout-plan` SHALL accept a single line holding one integer n with 1 <= n <= 1000 (trace D7/E7), and SHALL emit exactly n lines, the k-th of which is the number of ways to place two access points on distinct cells of a k-by-k grid such that they do not interfere. Placements are unordered: swapping the two access points does not produce a second arrangement. Two cells interfere when their relative position, expressed as a row difference and a column difference, is one of the eight offsets listed on the challenge page; the page SHALL present those eight offsets as an explicit table and SHALL NOT describe them as the move of any game piece (trace D6). The k-th line equals `k*k*(k*k-1)/2 - 4*(k-1)*(k-2)` for k >= 3 and `k*k*(k*k-1)/2` for k < 3 (trace E1). The upper bound is 1000 rather than a larger value because at n = 3000 three natural spellings of one and the same row-offset counting algorithm straddle the operation limit, so a student's verdict would depend on spelling rather than on algorithm (trace E7).

#### Scenario: Worked example
- **GIVEN** the input `8`
- **WHEN** the submission is judged
- **THEN** the output is the eight lines `0`, `6`, `28`, `96`, `252`, `550`, `1056`, `1848`

#### Scenario: Smallest site
- **GIVEN** the input `1`
- **THEN** the output is the single line `0`, because two access points cannot occupy one cell

#### Scenario: Branch boundary
- **GIVEN** the input `3`
- **THEN** the third line is `28`, not `36`; a submission whose guard on the k < 3 branch is inverted prints `36` and is discriminated by this entry (trace E9)

---
### Requirement: Access point layout plan testcase plan
The challenge `ap-layout-plan` SHALL declare a 20-entry all-literal `testcase_plan` holding the values `8, 1, 2, 3, 4, 6, 21, 72, 249, 250, 325, 400, 475, 550, 625, 700, 775, 850, 925, 1000` (trace E2). Entry 1 SHALL be byte-identical to the worked example on the challenge page and SHALL by itself expose every wrong route contracted below (trace E3). The plan SHALL cover n = 1, 2, 3 and 4, because the closed form branches at k = 3 and a submission that special-cases only k = 3 must be caught. At least ten entries SHALL hold n >= 250, and the largest entry SHALL equal the declared upper bound. All twenty values SHALL be pairwise distinct and SHALL be produced mechanically by the entry-derivation routine in the challenge's assertion wall rather than hand-picked, so that a change to the bound regenerates the whole plan instead of leaving stale values behind (trace C8).

The assertion wall SHALL additionally verify, and refuse to emit literals without, both of the following: that all three spellings of the row-offset counting route stay within the operation limit on the largest entry with the most expensive of them retaining a margin of at least three (trace E6), and that the per-cell scanning route dies on at least twelve of the twenty entries (trace E8).

#### Scenario: Assertion wall blocks shipping
- **GIVEN** any change to the bound or to the entry-derivation rule
- **WHEN** the assertion wall runs
- **THEN** it recomputes every route score, every operation count and every coverage check, and exits non-zero without writing literals if any contract is violated

#### Scenario: Regeneration is byte-identical
- **GIVEN** the emitted literals are deleted
- **WHEN** the assertion wall and the assembler are run again
- **THEN** the regenerated frontmatter fragment is byte-for-byte identical to the shipped one

---
### Requirement: Access point layout plan cost ladder and bypass disposition
The binding cost gate for `ap-layout-plan` SHALL be the operation counter, not the wall clock. The wall clock is not discriminating here: the process start floor measures 14.53 ms while the reference route's algorithmic increment is 0.86 ms, and the three accepted spellings consume 4.62, 3.18 and 5.01 percent of the per-testcase deadline (trace E11).

The closed-form route is the REFERENCE and SHALL score 20/20 at 3,010 operations, 0.030 percent of the limit (trace E4). Row-offset counting is an ACCEPTED ALTERNATIVE and SHALL keep scoring 20/20 **in every reasonable spelling**, verified in three: an explicit inner loop at 1,008,010 operations, a generator-expression sum at 1,510,510, and an extracted helper function at 2,509,511 (trace E5). Budgeting this route from its cheapest spelling would be an error, because the route must survive rather than die; the most expensive checked spelling therefore sets the margin, which is 3.98 (trace E6).

Per-cell scanning over all eight offsets is KILLED and SHALL score 8/20, measured in a cross-origin-isolated browser, dying from the ninth entry onward. It dies against the **operation limit**, not against the wall-clock deadline: the ninth entry consumes 216,759,740 operations against a limit of ten million, and every dying entry takes about 1,950 ms regardless of its input size, which is the fixed cost of exhausting the operation budget rather than the 5,000 ms deadline (trace E8). Four wrong routes SHALL score exactly 1/20, 2/20, 2/20 and 0/20: treating placements as ordered, omitting the interference subtraction, inverting the k < 3 guard, and iterating from zero (trace E9).

A route that expands the pair count through `math.factorial` is a KNOWN RESIDUE that this change SHALL NOT work around. It scores **0/20** in the browser, with all twenty entries reported as not executed, while consuming only 577 operations (trace E10). The mechanism is narrower than the claim that a C call can never be interrupted: a `math.factorial` call whose argument is moderate returns quickly, and any expensive work after it runs at bytecode level and **is** interrupted cleanly, which a bounded variant demonstrates by receiving a clean timeout at 5,041 ms and scoring 19/20 (trace W3). What kills the run is a single C call with an argument so large that it never returns, so the interrupt flag is never examined; the worker then dies and **every** result is discarded, leaving the student with no partial credit rather than with the score the surviving entries earned (trace W4). The page recovers on the next submission (trace W5). This is the same family as the operation-counter evasions recorded against earlier challenges and belongs to an engine-level change.

The challenge page SHALL NOT claim any route impossible, and any performance remark it makes SHALL be limited to the measured statement about scanning every pair of cells.

#### Scenario: Every spelling of the accepted route survives
- **GIVEN** a submission that counts interfering pairs by row offset, written with an explicit loop, with a generator-expression sum, or with an extracted helper
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores 20/20

#### Scenario: Scanning every cell dies on the large entries
- **GIVEN** a submission that, for each side length, visits every cell and tests all eight offsets
- **WHEN** it is judged against the full 20-entry block
- **THEN** it passes the first eight entries and is stopped from the ninth onward for exceeding the operation limit, scoring 8/20

---
### Requirement: Marquee display count I/O contract and discrimination
The challenge `marquee-display-count` SHALL accept a single line holding two space-separated integers n and k with 1 <= n <= 1000000 and 0 <= k <= n, and SHALL emit one line holding the number of distinct pictures the board can show, reduced modulo 1000000007. The board has n cells, each either lit or dark, of which k named cells are permanently dark; the answer is therefore `2^(n-k)` reduced modulo 1000000007, and equals 1 when k = n (trace F1). The page SHALL express the reduction as taking the remainder after division by 1000000007 and SHALL NOT use modular or binary terminology (trace D6).

This challenge SHALL NOT carry a cost cliff (trace D2). Its discrimination is that the number of free cells is n - k rather than n. The three-argument power route and the linear doubling loop SHALL both score 20/20, at 7 and 2,000,009 operations respectively, the latter on the entry `1000000 0` (trace F3); computing the full integer before reducing SHALL likewise score 20/20 at 7 operations.

The plan SHALL hold twenty pairwise distinct literals, the first being `5 2`, and SHALL cover k = 0, k = n, n = 1 and n = 1000000 (trace F2). Four wrong routes SHALL score exactly 2/20, 0/20, 0/20 and 6/20: ignoring k, mistaking the free count for k, printing n - k itself, and omitting the reduction (trace F4). The route that ignores k SHALL NOT be required to reach 0/20: the plan must cover k = 0, and that route is correct precisely there, so the two requirements are mutually exclusive and the k = 0 entries are held to the minimum of two (trace F5). The route that omits the reduction scores 6/20 only on entries where n - k <= 29, four of which the coverage contract forces into the plan; on the remaining entries it raises an integer-to-string conversion error (trace F6).

#### Scenario: Worked example
- **GIVEN** the input `5 2`
- **THEN** the output is `8`

#### Scenario: Every cell is broken
- **GIVEN** an entry where k equals n
- **THEN** the output is `1`

#### Scenario: Ignoring the broken cells is caught
- **GIVEN** a submission that computes the count from n alone
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores 2/20, passing only the two entries where k is zero

---
### Requirement: Fair token exchange I/O contract and discrimination
The challenge `fair-token-exchange` SHALL accept a single line holding one integer n with 1 <= n <= 1000000000, and SHALL emit one line holding the number of rank promotions successfully completed. The number of orderings of n people is the count of rank-one tokens; twelve tokens of one rank exchange for a single token of the next rank only when they exactly fill a batch, and the answer counts how many such rank promotions can be completed (trace G1). The page SHALL NOT use factorial, base, prime-factor or modular vocabulary; it SHALL speak of the number of different orders in which people can line up, and of exchanging twelve tokens for one (trace D5/D6).

The answer equals the smaller of half the accumulated share of two and the accumulated share of three, each share being the sum of n divided by successive powers of that number, with the halving rounded down. The plan SHALL hold twenty pairwise distinct literals, the first being `9`, and SHALL cover n = 1, n = 11 and n = 1000000000, with at least five entries at or above 100000000 (trace G2).

The reference route and two accepted spellings SHALL score 20/20 at 155, 156 and 166 operations (trace G3). Applying the published base-ten trailing-zero rule SHALL score exactly 2/20 (trace G4).

Three routes that take only one side of the minimum SHALL score 11/20, 11/20 and 12/20, and **12/20 is the lowest attainable maximum for this family**; no choice of entries can push it lower (trace G5). The proof is structural: since the answer is a minimum of two quantities, on every entry at least one of the two single-quantity routes is correct, so their scores sum to twenty plus the number of entries where the two quantities tie; the three entries the coverage contract forces into the plan are all ties, which floors the better of the two at twelve. A fourth route, taking the minimum without the halving, produces output identical to the share-of-three route on every input and therefore cannot be discriminated separately (trace G6). The assertion wall SHALL lock the attained bound so that a later change to the plan cannot silently raise it.

A route that materialises the ordering count through `math.factorial` and divides repeatedly is a KNOWN RESIDUE of the same family as the one recorded for `ap-layout-plan`: it scores **0/20** in the browser, with all twenty entries reported as not executed, while consuming 98,699 operations, 0.99 percent of the limit (trace G7). A local measurement that applies the deadline to per-entry timings reports 13/20 for this route; that figure is an artefact of the projection method, which cannot model a worker that dies and discards results already earned, and SHALL NOT be quoted. Its infeasibility at large n rests on memory rather than on time — the integer alone occupies 314 megabytes at n = 100000000 and 3,556,832,228 bytes at n = 1000000000 — because the time extrapolation was not reproducible across runs while the memory figures were identical (trace G8).

#### Scenario: Worked example
- **GIVEN** the input `9`
- **THEN** the output is `3`

#### Scenario: No exchange is possible
- **GIVEN** the input `1`
- **THEN** the output is `0`

#### Scenario: The base-ten rule fails
- **GIVEN** a submission that counts how many times ten divides the ordering count
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores 2/20

---
### Requirement: Shared authoring constraints for the counting trio
All three challenges SHALL be `category: apcs` and `type: competition`, with `ap-layout-plan` and `marquee-display-count` at `difficulty: easy` and `fair-token-exchange` at `difficulty: medium`; their ids SHALL be assigned by the `pnpm new-challenge` scaffold rather than hand-written (trace D1). The `easy` label on `ap-layout-plan` is a maintainer decision taken with full knowledge that brute-force enumeration cannot pass: the label measures the depth of the mathematical reasoning, which sits inside the senior-high curriculum, not the depth of the programming technique (trace D4). It is the series' first `easy` challenge carrying a cost cliff, and this SHALL NOT be treated as a defect.

All three pages, slugs and `algorithm` values SHALL be free of data-structure and algorithm terminology in both English and Chinese. The assembler SHALL enforce this over every fragment it emits and SHALL refuse to write any file when a term is hit, leaving all previously emitted fragments untouched (trace C7). It SHALL likewise refuse when its input contains an expected-answer key or a comment inside a testcase plan, so that neither answers nor the identity of the discriminating routes can leak into shipped frontmatter.

All three SHALL declare a `reference_solution` implemented independently of the `generator` and verified by `scripts/content-regression.test.ts`, and all three `starter_code` fields SHALL be the empty string so the editor loads blank. No page SHALL contain a number that is not traceable to a fact id in `trace-matrix.md`.

Operation counts SHALL be produced by exactly one implementation, the faithful reproduction of the judge's tracer kept with this change; that reproduction counts every trace event without filtering event type or filename and keeps tracing nested calls, and its self-test fails if any of those properties is lost (trace C2). Counts written into documents SHALL be taken from a fresh interpreter process, because a module's first import is charged to the testcase that triggers it (trace C4). Wall-clock figures SHALL be sampled at least seven times with the minimum reported, and SHALL be labelled as estimates wherever they are projected onto the browser, since only the operation count transfers unchanged (trace C3/C5).

Production builds strip only `generator` and `reference_solution`, so the literal test inputs of all three challenges reach the client bundle and are in any case public in the repository. This is a pre-existing project-level residue shared with the earlier all-literal challenges, is recorded as such, and SHALL NOT be worked around by weakening the test data (trace C6).

#### Scenario: Banned term blocks assembly
- **GIVEN** an algorithm identifier or page fragment containing a banned term
- **WHEN** the assembler runs
- **THEN** it exits non-zero, names the offending terms, and writes no fragment at all

#### Scenario: Content regression covers all three challenges
- **GIVEN** all three challenges declare a generator and a reference solution
- **WHEN** the content regression test runs against the built production pools
- **THEN** all three reference solutions match their generator's expected output on every sampled entry
