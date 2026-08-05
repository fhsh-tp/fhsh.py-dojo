## ADDED Requirements

### Requirement: Elimination semantics and aggregate output

The gem-blast-playtest challenge SHALL define the following semantics: a board is a string of lowercase letters where each letter is a gem color; whenever two adjacent gems have the same color, that pair is removed and the two sides close up, and removal SHALL cascade until no adjacent equal pair remains (equivalent to LeetCode 1047 pair reduction). The residue of a board is the length of the string after all cascading removals. The expected output SHALL be T lines, one per playtest round, where line i is a single integer: the maximum residue across the N boards of round i. A residue of 0 SHALL be a legal output value.

#### Scenario: Cascading pair removal reduces a board to its residue

- **WHEN** a board string is reduced by repeatedly removing adjacent equal pairs until none remain
- **THEN** the reported value for that board equals the final string length, independent of removal order

##### Example: Board residues

| Board | Residue | Notes |
| ----- | ------- | ----- |
| abba | 0 | bb removed, then aa cascades |
| aaa | 1 | only one pair removable |
| aabcc | 1 | aa then cc removed, b remains |
| abcba | 5 | no adjacent equal pair exists |
| a | 1 | single gem, nothing to remove |

#### Scenario: Round aggregation takes the maximum residue

- **WHEN** a round contains N boards with residues r1..rN
- **THEN** the output line for that round is max(r1..rN)

##### Example: Two rounds

- **GIVEN** round 1 boards [abba, abcba, aabcc] and round 2 boards [aa, abba]
- **WHEN** the generator processes both rounds
- **THEN** the output is two lines: 5 then 0

### Requirement: Literacy framing without data-structure terminology

The student-visible surface of the challenge (body text, title, description, tags, examples) SHALL present the scenario of a playtester measuring difficulty of match-two gem boards, and SHALL NOT contain the strings stack, 堆疊, 資料結構, deque, or 佇列, and SHALL NOT name any concrete data structure or library as the required solution technique. The body SHALL state the input bounds T <= 3, N <= 5 per round, and board length between 1 and 40000, and SHALL include a sentence noting that some testcases contain very long boards.

#### Scenario: Student-visible surface stays literacy-framed

- **WHEN** the challenge page renders the body, tags, and description
- **THEN** no data-structure terminology appears anywhere in the student-visible surface, and the stated bounds match the testcase plan maxima

### Requirement: Frontmatter contract

The challenge file docs/challenge/gem-blast-playtest.md SHALL declare: layout challenge, scaffold-assigned id with prefix apcs, title 寶石消除關卡測試, difficulty medium, category apcs, type competition, algorithm gem_blast_playtest, input_budget 42000 (sized to sit just above the worst-case stress-band entry so the budget gate tracks the advertised 40000 board-length ceiling), an empty-string starter_code, a one-sentence description, and tags free of data-structure terminology. The frontmatter SHALL NOT declare testcase_count. The params SHALL declare, in order: t as int with min 1 and max 3; rounds as group with repeat from t, containing n as int with min 1 and max 5, and boards as alpha_lower with min_len 3, max_len 50, and count from n with separator newline.

#### Scenario: Params pass the engine smoke gate

- **WHEN** scripts/challenge-params.test.ts runs against the challenge file
- **THEN** the params declaration is accepted by the testcase-generator engine with no unknown type or field errors

### Requirement: Twenty-entry banded testcase plan

The challenge SHALL declare a testcase_plan with exactly 20 entries in this fixed order: (1) one example literal identical to the first worked example in the challenge body, containing a round whose maximum residue is 0; (2) a warmup band of 9 entries using the base params ranges; (3) a random stress band of 5 entries overriding t to fixed 1, n to fixed 1, and boards to min_len 30000 and max_len 40000; (4) three nested-annihilation literals with pairwise-distinct board lengths 30000, 34001, and 38002; (5) two boundary literals: a single one-gem board with expected output 1, and a multi-board round where every board fully annihilates with expected output 0. A nested-annihilation board SHALL be built around a core of w concatenated with reverse(w), where w is a prefix of a two-letter alternating string, so that at every reduction step the only removable pair inside the core sits at its center and the core fully annihilates. The three nested-annihilation literals SHALL use pairwise-distinct letter pairs, pairwise-distinct board lengths drawn from inside the stress band range, and pairwise-distinct residues 0, 1, and 2 (produced by attaching sentinel gems, of colors absent from the core letter pair, that survive reduction), so that no single hardcoded input-to-output mapping, length-keyed branch, or constant-output shortcut covers more than one of the three entries.

#### Scenario: Pool build produces the planned pool

- **WHEN** pnpm build:pools runs
- **THEN** the encrypted pool for gem_blast_playtest contains 10 blocks of 20 testcases each, every entry within the 42000-byte input budget, with the example literal as the first testcase of every block

### Requirement: TLE cliff thresholds

The testcase plan SHALL enforce this performance cliff, verified by replaying the judge tracer semantics (settrace counting all events, 10,000,000-event limit) offline: (a) naive quadratic solution A, which rescans from the start after every removal, SHALL exceed 2x the operation limit on every random stress entry and every nested-annihilation literal; (b) naive quadratic solution B, which repeats full passes until a fixed point, SHALL exceed 2x the operation limit on every nested-annihilation literal; (c) the stack-scan reference implementations SHALL stay at or below 1/50 of the operation limit on every entry of the plan.

#### Scenario: Naive solutions die on stress entries with margin

- **WHEN** the offline tracer probe replays naive solutions A and B against the stress entries
- **THEN** every measured event count for the entries covered by clauses (a) and (b) is at least 20,000,000

#### Scenario: Intended solution survives with margin

- **WHEN** the offline tracer probe replays the stack-scan solution against all 20 entries
- **THEN** every measured event count is at most 200,000

### Requirement: Bypass acceptance after hunt downgrade

The C-builtin str.replace bypass SHALL be treated as an accepted alternative solution: for as long as the worker wall-clock flag remains inert for synchronous student code, the testcase plan SHALL NOT contain any entry whose purpose is to defeat it, and the repair path is tracked in the platform BACKLOG section 2.8 (post-run elapsed-based TLE adjudication); the change that implements that repair SHALL amend this clause through the normal spec-delta process. This clause records the verified platform constraint that motivated the downgrade: the worker 5-second wall-clock flag is a setTimeout macrotask, and for synchronous student code the await continuation (a microtask) always runs clearTimeout before an expired timer callback can fire, so the flag can never produce a TLE verdict for synchronous code. The performance cliff of this challenge is enforced solely by the default settrace op-counter: solutions that disable the tracer (for example sys.settrace(None), an opt-out the platform BACKLOG records as accepted) or that delegate the quadratic work to C builtins are outside the cliff guarantee. The dev-runner measurement that confirmed this (bypass verdict and wall time on the former 60000-length hunt literal) SHALL be recorded in the change design document.

#### Scenario: Bypass passes the full plan

- **WHEN** the str.replace bypass solution is judged against the full 20-entry plan in the dev runner
- **THEN** every entry reports AC and no entry is designated as a bypass hunt entry

### Requirement: Generator and reference-solution division of labor

The generator SHALL implement the elimination semantics with an append-and-pop scan (list used as a growing buffer, comparing against the last element) and aggregate with a variable named best, reading input in the order t, then per round n and n board lines. The reference_solution SHALL implement the same semantics with a preallocated array and top-index two-pointer scan, sharing no scan-loop code shape with the generator. Both SHALL be linear-time per board. The reference_solution SHALL NOT use a quadratic algorithm. During implementation both implementations SHALL be cross-validated on at least 3000 random strings with identical results.

#### Scenario: Automated gates and recorded manual checks validate the reference against the production pool

- **WHEN** scripts/content-regression.test.ts runs with the built pool
- **THEN** the reference_solution output matches the generator expected output on the deterministic 20-of-200 pool sample that gate draws for this slug, the wrapper content smoke test additionally covers pool indices 0, 100, and 199, and every plan position not reached by either gate SHALL be validated in the dev runner during implementation with the result recorded in the change verification notes

#### Scenario: Random cross-validation finds no divergence

- **WHEN** 3000 random lowercase strings of mixed lengths are fed to both scan implementations
- **THEN** the two implementations report identical residues for every string
