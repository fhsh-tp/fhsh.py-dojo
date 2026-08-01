# deque-challenge-series Specification

## Purpose

Content contract for the deque challenge series: literacy-oriented challenges whose most natural solution is double-ended access (collections.deque), specifying student-visible framing constraints, input/output formats, banded testcase plans, and the generator versus reference-solution division of labor.

## Requirements

### Requirement: Two-end elimination challenge content
The challenge file for two-end-elimination MUST declare: layout challenge, a site-unique integer id, title 兩端淘汰賽, difficulty medium, type competition, algorithm two_end_elimination, tags containing data structure and deque, a one-sentence description, and an empty-string starter_code. The frontmatter MUST NOT declare testcase_count (mutually exclusive with testcase_plan) and MUST NOT declare verdict_detail (absent means hidden). The challenge body MUST follow the card-restack-count.md narrative structure (problem statement, hands-on walkthrough, input format, output format, example) and MUST instruct students to use collections.deque with the two-end elimination method, and MUST state that oversized testcases will time out slow implementations without promising specific testcase positions.

#### Scenario: Frontmatter passes the params smoke gate
- **WHEN** the challenge-params smoke test (scripts/challenge-params.test.ts) runs over all challenges
- **THEN** two-end-elimination passes with no unknown type or field errors, and declares no testcase_count and no verdict_detail

---
### Requirement: Competition-style input and output format
The challenge input MUST be: first line an integer T (2..3); then for each of the T cases, a first line integer Ni (1..4000) followed by Ni lines each containing one integer in -999..999. The expected output MUST be T lines, each formatted as the maximum value, a single space, then the minimum value of that case, in the declared case order. The maximum MUST precede the minimum.

#### Scenario: Generator reads declared order and emits max before min
- **WHEN** the generator executes against a rendered input
- **THEN** it reads T, then per case reads Ni and Ni integers, and prints one line per case with max first and min second

##### Example: two cases including negatives
- **GIVEN** the input lines: 2, 3, -52, 817, -3, 1, 64
- **WHEN** the generator runs
- **THEN** stdout is exactly two lines: "817 -52" then "64 64"

---
### Requirement: Banded testcase plan with six testcases
The params MUST use group syntax: t as int 2..3; cases as a group with repeat t containing n as int 1..4000 and nums as int -999..999 with count from n and newline separator. input_budget MUST be 65535. The testcase_plan MUST declare exactly three band entries in this order totaling six testcases: a teaching band with count 3 overriding n max to 20, a TLE band with count 2 overriding n min to 2500, and a single-element band with count 1 overriding n min and max both to 1. The plan MUST NOT contain literal entries.

#### Scenario: Pool build produces six-testcase blocks
- **WHEN** pnpm build:pools runs with the declared plan
- **THEN** the pool for two-end-elimination builds without error and each judged submission receives exactly 6 testcases in band declaration order (3 teaching, 2 TLE-scale, 1 single-element)

#### Scenario: Single-element boundary is always covered
- **WHEN** any pool block is selected for judging
- **THEN** exactly one testcase has every Ni equal to 1, and its expected output repeats the same integer twice per case

---
### Requirement: Performance separation between deque solution and quadratic solution
The TLE band values MUST make a flat pure-Python O(n squared) double-loop solution exceed the 10M operation limit (verdict TLE) on both TLE-band testcases, while the reference deque solution and builtin-based solutions MUST pass all six testcases within limits (verdict AC).

#### Scenario: Quadratic solution times out on TLE band
- **WHEN** a flat pure-Python double-loop max/min solution is judged
- **THEN** both TLE-band testcases (n at least 2500) show verdict TLE

#### Scenario: Reference solution passes all testcases
- **WHEN** the reference_solution is judged against the pool
- **THEN** all 6 testcases show verdict AC

---
### Requirement: Generator and reference solution division of labor
The generator MUST compute expected output using builtin max() and min(). The reference_solution MUST solve the task with collections.deque using the two-end elimination method (compare front and back, pop the losing end, last remaining element is the answer; run one pass for max on a copy and one pass for min), deliberately differing from the generator implementation. The reference_solution output MUST match the generator expected output on official pool samples as verified by the content-regression test.

#### Scenario: Content regression validates the teaching algorithm
- **WHEN** pnpm test --run executes the content-regression suite
- **THEN** two-end-elimination is covered (reference_solution declared) and its deque-based output matches the generator expected output on official pool inputs
