## REMOVED Requirements

### Requirement: Two-end elimination challenge content
**Reason**: The result-output task (max min) is solvable by a naive O(n) single scan, so the deque teaching goal and the elimination-tournament framing collapsed; the challenge is reworked into a literacy-oriented process-log task under a new name.
**Migration**: Superseded by "Buffer audit challenge content".

### Requirement: Competition-style input and output format
**Reason**: The one-line-per-case "max min" output is computable without any double-ended process; replaced by a two-line process-log output whose content is only derivable by simulating two-end removals.
**Migration**: Superseded by "Competition-style input and process-log output".

### Requirement: Banded testcase plan with six testcases
**Reason**: The TLE-scale band (n >= 2500) targeted a strawman O(n squared) solution nobody writes naturally, and doubled pool size for no teaching value; the plan is rescaled with a mid-size band instead.
**Migration**: Superseded by "Rescaled banded testcase plan with six testcases".

### Requirement: Performance separation between deque solution and quadratic solution
**Reason**: In the process-log task there is no natural slow-but-correct solution to punish with TLE; the separation axis moves from performance (TLE) to semantics (WA for result-only solutions).
**Migration**: Superseded by "Semantic separation between process-log solutions and result-only solutions".

### Requirement: Generator and reference solution division of labor
**Reason**: The generator can no longer use builtin max()/min() because the expected output is a process log, not a result; the division of labor is redefined as two-pointer generator vs deque reference solution.
**Migration**: Superseded by "Two-pointer generator and deque reference solution division of labor".

## ADDED Requirements

### Requirement: Buffer audit challenge content
The challenge file for buffer-audit-log MUST declare: layout challenge, id 56, title 緩衝區稽核日誌, difficulty medium, type competition, algorithm buffer_audit_log, tags containing data structure and 模擬, a one-sentence description, and an empty-string starter_code. The frontmatter MUST NOT declare testcase_count and MUST NOT declare verdict_detail. The challenge body MUST follow the series narrative structure (problem statement, hands-on walkthrough, input format, output format, example) and MUST present a literacy-oriented scenario: an edge device stores sensor readings in order in a bounded buffer whose hardware only allows inspecting and removing one reading at either end (oldest or newest), with an audit rule requiring every removal to be logged. The student-visible surface (body text, tags, description, examples) MUST NOT contain the strings deque or 雙端佇列, and MUST NOT name any concrete data structure or library as the required solution.

#### Scenario: Frontmatter passes the params smoke gate
- **WHEN** the challenge-params smoke test (scripts/challenge-params.test.ts) runs over all challenges
- **THEN** buffer-audit-log passes with no unknown type or field errors, and declares no testcase_count and no verdict_detail

#### Scenario: No solution-structure leakage on student-visible surface
- **WHEN** the challenge file is searched for the strings deque and 雙端佇列
- **THEN** there are zero occurrences outside the reference_solution frontmatter block

### Requirement: Competition-style input and process-log output
The challenge input MUST be: first line an integer T (2..3); then for each of the T cases, a first line integer Ni (1..400) followed by Ni lines each containing one integer in -999..999. The expected output MUST be exactly two lines per case (2T lines total), each line containing exactly Ni space-separated integers. Line one of a case is the peak-round audit log: repeatedly compare the oldest and newest ends, remove and log the smaller end (on ties remove the newest end), until one reading survives; the line lists the removed readings in removal order followed by the survivor, which MUST equal the case maximum. Line two is the valley-round audit log over a fresh replay of the same case: remove and log the larger end (on ties remove the newest end); the survivor MUST equal the case minimum. For a single-element case (Ni = 1) both lines MUST consist of that single reading.

#### Scenario: Process log is emitted for each case in declared order
- **WHEN** the generator executes against a rendered input
- **THEN** it reads T, then per case reads Ni and Ni integers, and prints two lines per case (peak-round log then valley-round log) in the declared case order

##### Example: four readings with negatives
- **GIVEN** one case with readings in order: 3, -5, 8, 1
- **WHEN** the peak round and valley round run
- **THEN** the two output lines are exactly "1 3 -5 8" and "3 1 8 -5"

##### Example: tie removes the newest end
- **GIVEN** one case with readings in order: 5, 2, 5
- **WHEN** the peak round and valley round run
- **THEN** the two output lines are exactly "5 2 5" and "5 5 2"

##### Example: single reading
- **GIVEN** one case with the single reading 64
- **WHEN** the peak round and valley round run
- **THEN** both output lines are exactly "64"

### Requirement: Rescaled banded testcase plan with six testcases
The params MUST use group syntax: t as int 2..3; cases as a group with repeat t containing n as int 1..400 and nums as int -999..999 with count from n and newline separator. input_budget MUST be 8192. The testcase_plan MUST declare exactly three band entries in this order totaling six testcases: a teaching band with count 3 overriding n max to 20, a mid-size band with count 2 overriding n min to 200, and a single-element band with count 1 overriding n min and max both to 1. The plan MUST NOT contain literal entries and MUST NOT contain any band with n above 400.

#### Scenario: Pool build produces six-testcase blocks
- **WHEN** pnpm build:pools runs with the declared plan
- **THEN** the pool for buffer-audit-log builds without error and each judged submission receives exactly 6 testcases in band declaration order (3 teaching, 2 mid-size, 1 single-element)

#### Scenario: Single-element boundary is always covered
- **WHEN** any pool block is selected for judging
- **THEN** exactly one testcase has every Ni equal to 1, and each of its cases expects two identical one-number lines

### Requirement: Semantic separation between process-log solutions and result-only solutions
A correct process-simulating solution (whether implemented with collections.deque or with two index pointers) MUST receive AC on all six testcases. A result-only solution that outputs one "max min" line per case — the natural solution to the previous task semantics — MUST receive WA on every testcase, because the expected output is the two-line process log which cannot be derived without simulating the two-end removal order.

#### Scenario: Reference solution passes all testcases
- **WHEN** the reference_solution is judged against the pool
- **THEN** all 6 testcases show verdict AC

#### Scenario: Result-only legacy solution fails every testcase
- **WHEN** a solution printing one line per case with the maximum, a space, and the minimum is judged
- **THEN** all 6 testcases show verdict WA

### Requirement: Two-pointer generator and deque reference solution division of labor
The generator MUST simulate the removal process using two index pointers over the reading list (no collections.deque import, and no builtin max()/min() used to produce the answer), assembling each log line by joining collected values with single spaces. The reference_solution MUST simulate the same process with collections.deque using front/back inspection and popleft()/pop() removals, one fresh copy per round. Both implementations MUST produce identical output on official pool samples as verified by the content-regression test.

#### Scenario: Content regression validates both implementations agree
- **WHEN** pnpm test --run executes the content-regression suite
- **THEN** buffer-audit-log is covered (reference_solution declared) and the deque-based output matches the two-pointer generator expected output on official pool inputs
