## ADDED Requirements

### Requirement: Exam-collection challenge content

The challenge file `docs/challenge/exam-collect-verify.md` MUST declare: layout challenge, a scaffold-assigned unique integer id, title 收卷順序驗證, difficulty medium, category apcs, type competition, algorithm exam_collect_verify, tags containing data structure and 模擬, a one-sentence description, input_budget 63488, and an empty-string starter_code. The frontmatter MUST NOT declare testcase_count (the testcase_plan defines the count) and MUST NOT declare verdict_detail. The challenge body MUST follow the series narrative structure (problem statement, hands-on walkthrough, input format, output format, example) and MUST present a literacy-oriented scenario: two proctors collect exam papers from the two ends of one row of seats, one paper at a time from either end, each collected paper placed on top of a single growing pile; the task is to verify which of M reported top-to-bottom pile orders could be genuine. The student-visible surface (body text, tags, description, examples) MUST NOT contain the strings deque, 雙端佇列, stack, or 堆疊, and MUST NOT name any concrete data structure or library as the required solution. The body MUST state three explicit guarantees: seat numbers within a row are pairwise distinct, a report lists the pile from top to bottom, and seat numbers are in 1..999.

#### Scenario: Frontmatter passes the params smoke gate

- **WHEN** the challenge-params smoke test (scripts/challenge-params.test.ts) runs over all challenges
- **THEN** exam-collect-verify passes with no unknown type or field errors

#### Scenario: No solution-structure leakage on student-visible surface

- **WHEN** the challenge file is searched for the strings deque, 雙端佇列, stack, 堆疊
- **THEN** there are zero occurrences outside the frontmatter generator/reference_solution blocks

---

### Requirement: Exam-collection report-verification semantics

The challenge input for exam-collect-verify MUST be: first line an integer T (1..10); then for each of the T datasets, a first line with two integers N and M (1 ≤ N ≤ 800, 1 ≤ M ≤ 50) separated by one space, a second line with N pairwise-distinct seat numbers (values in 1..999) separated by single spaces listing the row from podium end to window end, followed by M report lines each containing exactly N space-separated values. The expected output MUST be exactly T lines, line i containing a single integer: the number of legal reports in dataset i. A report is legal if and only if there exists a sequence of removals, each taking the current leftmost or rightmost remaining paper of the row and placing it on top of one pile, such that reading the final pile from top to bottom yields exactly the report; equivalently, the reversal of the report is obtainable by repeatedly taking the leftmost or rightmost remaining element of the source row. A report containing a duplicated value, a value absent from the source row, or any value making the multiset differ from the source row is not legal. Because source values are pairwise distinct, the two-pointer greedy over the reversed report (match left end, else right end, else fail) SHALL be the defining decision procedure; its verdict has been exhaustively verified equal to brute-force reachability for all N ≤ 6 plus randomized N = 7,8 samples.

#### Scenario: Legal and illegal reports are counted per dataset

- **WHEN** the generator executes against a rendered input
- **THEN** it emits one integer per dataset, in dataset order, each counting exactly the legal reports of that dataset

##### Example: Statement example, first dataset

- **GIVEN** source row `3 1 4 2` and reports `4 1 3 2`, `2 3 1 4`, `3 4 1 2`, `4 4 1 2`
- **WHEN** legality is decided
- **THEN** `4 1 3 2` is legal (collect right, left, left, right); `2 3 1 4` is illegal (it is the collection order, not the pile); `3 4 1 2` is illegal (a permutation no end-taking sequence can produce); `4 4 1 2` is illegal (duplicated seat number); the output line is `1`

##### Example: Statement example, second dataset

- **GIVEN** source row `5 9` and reports `9 5`, `5 9`
- **WHEN** legality is decided
- **THEN** both reports are legal (for N ≤ 2 every permutation of the row is producible) and the output line is `2`

#### Scenario: Reversal-trap report is rejected

- **WHEN** a report equals a valid collection order whose reversal is not itself producible as a pile reading
- **THEN** the report is counted illegal; a solution that forgets to reverse the report before end-matching yields a different count on such datasets

---

### Requirement: Exam-collection testcase plan with twenty entries

The testcase_plan MUST contain exactly 20 entries in five ordered bands: (1) one literal entry pinned first whose content equals the statement example (two datasets, answers 1 and 2) so the run dialog's default stdin matches the walkthrough; (2) nine handcrafted discrimination literal entries with N in 5..12, each containing at least one reversal-trap report line alongside legal, non-producible-permutation, and non-permutation lines; (3) four curated band entries sharing the single declared params shape T=1, N=6, M=8, where the source is an enum over 10 handcrafted seat-number permutations and each of the eight report lines q1..q8 is an enum over 10 curated candidates; (4) three stress literal entries with T=1, N=800, M=18 covering an all-legal dataset, a long-shared-prefix near-miss dataset, and a mixed dataset; (5) three boundary literal entries covering N=1, M=1, and T=10 with mixed small-N datasets. Every curated band candidate MUST be a permutation of its dataset's source value set, and for every source permutation in the enum library, the union of the eight candidate libraries MUST contain at least one report whose verdict differs between the correct reversed semantics and the forgot-to-reverse semantics (curation guarantee). All rendered inputs MUST stay within the declared statement bounds.

#### Scenario: Pool blocks differ under band randomization

- **WHEN** pnpm build:pools renders the 200-entry pool (10 blocks of 20)
- **THEN** at least two blocks differ in content, so a solution that replays 20 memorized outputs cannot pass every block

#### Scenario: Stress entries defeat exponential enumeration without flaky verdict bands

- **WHEN** a solution enumerates all end-taking sequences (2^N frontier growth)
- **THEN** on each stress entry the enumeration exceeds twice the 10,000,000 judge limit astronomically under the settrace counting model (probe-verified doubling per element, first over-limit N ≈ 23, stress N = 800), while the two-pointer solution stays at or below one hundredth of the limit on every entry, and a correct quadratic Python-loop scanner measures at most 0.7x the limit on every stress entry — a stable pass by design, because within the declared seat-number domain (max 999 distinct values) and the per-input byte budget, a quadratic kill could only reach a 1.0-1.2x flaky band, which is worse than a documented pass

---

### Requirement: Exam-collection dual implementation and verification

The frontmatter generator MUST decide legality by reversing each report and running the two-pointer greedy against the source row, and MUST print one count per dataset. The reference_solution MUST decide legality with an independent position-interval method sharing no traversal logic with the generator: build a seat-number-to-position map of the source row; the first (top) report value fixes the starting position; every subsequent value's position must extend the current contiguous interval by exactly one on the left or right outside edge; unknown values and revisited positions fail naturally. Both implementations MUST agree on: exhaustive comparison against brute-force end-taking search for all source/report permutation pairs with N ≤ 6, and 3000 randomized N=800 trials; content-regression (scripts/content-regression.test.ts) MUST prove the reference_solution reaches Accepted on the full encrypted pool.

#### Scenario: Implementations agree and regression passes

- **WHEN** the cross-validation script and pnpm test gates run
- **THEN** exhaustive N ≤ 6 comparison, 3000 randomized N=800 trials, challenge-params, and content-regression all pass with zero mismatches
