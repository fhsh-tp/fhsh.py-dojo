# expression-eval-challenges Specification

## Purpose

TBD - created by archiving change 'add-expression-eval-duo'. Update Purpose after archive.

## Requirements

### Requirement: Snack-bar register challenge (apcs011) I/O contract and semantics
The challenge `snack-bar-register` SHALL accept input of: first line integer T (T >= 1), followed by T lines, each an arithmetic expression whose tokens (non-negative integers and the operators `+ - * /`) are separated by single spaces, with no parentheses and no unary minus (trace C2/C3/A1). For each expression the output SHALL be exactly one line containing one integer, computed under flipped-precedence semantics: the expression is split at `*` and `/` into additive segments; each additive segment is folded left-to-right; segment values are then folded left-to-right with `*` and `/` (trace A1). A single-number line is a valid expression whose value is that number (trace C2).

#### Scenario: Flipped precedence with left-associative additive fold
- **GIVEN** the expression `10 - 4 - 3 + 2 * 6`
- **WHEN** it is evaluated
- **THEN** the output line is `30` ((10-4-3+2)=5, then 5*6) (trace A2)

#### Scenario: Multiplicative segment preceding an additive segment
- **GIVEN** the expression `2 * 3 + 4`
- **WHEN** it is evaluated
- **THEN** the output line is `14` (segments 2 and 3+4=7, then 2*7), which differs from both standard precedence and strict left-to-right evaluation (both 10) (trace A2/A9)

#### Scenario: Negative intermediate value with exact division
- **GIVEN** the expression `1 - 7 / 2`
- **WHEN** it is evaluated
- **THEN** the output line is `-3` ((1-7)=-6, then -6/2) (trace A2/C4)

---
### Requirement: Coupon-stacking challenge (apcs012) I/O contract and semantics
The challenge `coupon-combo-quote` SHALL accept the same token format as apcs011 plus round parentheses as space-separated tokens (trace C2/B1). Evaluation SHALL use flipped precedence with RIGHT-associative additive folding (`a - b + c` = a-(b+c)), left-associative multiplicative folding, and parentheses overriding all grouping; parenthesized content is a complete sub-expression under the same rules (trace B1).

#### Scenario: Right-associative additive fold changes the shared example's answer
- **GIVEN** the expression `10 - 4 - 3 + 2 * 6`
- **WHEN** it is evaluated
- **THEN** the output line is `66` (10-(4-(3+2))=11, then 11*6) — the same expression evaluates to 30 in apcs011, and this contrast SHALL be stated on the challenge page (trace B2)

#### Scenario: Parentheses override flipped precedence
- **GIVEN** the expression `2 + ( 3 * 4 )`
- **WHEN** it is evaluated
- **THEN** the output line is `14` (the parenthesized `3 * 4` is computed first; without parentheses the flipped rules would give (2+3)*4=20) (trace B1)

#### Scenario: Same-level multiplicative chain stays left-associative
- **GIVEN** the expression `( 9 - 5 - 2 ) * 8 / 6`
- **WHEN** it is evaluated
- **THEN** the output line is `8` (inner right-assoc: 9-(5-2)=6, then (6*8)/6 left-folded), while a solution folding the multiplicative chain right-associatively or giving `/` a tighter level than `*` computes a different value (trace B11/B13)

---
### Requirement: Shared value domain and exact-division guarantee
Both challenges SHALL guarantee in their test data: operands are non-negative integers below 10000 (measured max 3791); every intermediate value stays within |value| < 100000 (measured peak 44865); every division under the challenge's own evaluation order is exact with a positive divisor (measured minimum divisor 1); `0 / d` is legal and equals 0 (trace C3/C4). The challenge pages SHALL state these guarantees, including that answers may be negative (trace C3/D6).

#### Scenario: Exact division on a negative dividend
- **GIVEN** the expression `0 - 4 / 2` under apcs011 rules
- **WHEN** it is evaluated
- **THEN** the output line is `-2` ((0-4)=-4, then -4/2), with the division exact

---
### Requirement: Snack-bar register testcase plan and discrimination duties
The challenge `snack-bar-register` SHALL declare a 20-entry all-literal `testcase_plan` with `input_budget: 63488`, entry contents byte-for-byte equal to the curated literal set produced by the deterministic curation script archived with this change (curation/plan_b.py, seeds 1101/1202, post-design-bounty version) (trace A7/C5/C6). Entry 1 SHALL be a literal identical to the worked example on the challenge page (T=5, including the negative-intermediate expression) (trace A2). The literal set SHALL satisfy the assertion wall: standard-precedence evaluation scores <= 3 entries (measured 2); additive-right-assoc misreading <= 4 (measured 1); recursive-descent muldiv-right bug <= 4 (measured 3); divide-tighter-than-multiply misreading <= 4 (measured 4); strict left-to-right evaluation <= 3 (measured 2); and the UNION of all modeled wrong routes <= 6 entries (measured 4) (trace A4/A5/A6/A9/A10/C13).

#### Scenario: Standard-precedence eval scores only the gimme entries
- **GIVEN** a solution that evaluates each line with Python standard precedence
- **WHEN** it is judged against the full 20-entry run
- **THEN** it is accepted on exactly entries 2 and 3 (single numbers and pure-additive lines), scoring 2/20 (trace A4)

---
### Requirement: Coupon-stacking testcase plan and discrimination duties
The challenge `coupon-combo-quote` SHALL declare a 20-entry all-literal `testcase_plan` with `input_budget: 63488`, entry contents byte-for-byte equal to the curated literal set produced by the same archived curation script (curation/plan_b.py): entries 1-8 contain no parentheses and entries 9-20 all contain parentheses (trace B8). Every entry from 9 to 20 SHALL contain at least one line matching an additive operator directly before an opening parenthesis, and SHALL contain at least one parenthesis-bearing line that also carries a same-level two-operator multiplicative chain whose left-fold value differs from both the right-fold and the divide-tighter readings (the PKline discrimination family) (trace B8/B11/B13). The literal set SHALL satisfy the assertion wall: standard-precedence evaluation <= 3 (measured 1); additive-left-assoc (operator-swap) route <= 4 (measured 1); uniform muldiv-right bug <= 4 (measured 3); divide-tighter misreading <= 4 (measured 3); parens-revert-to-standard-rules route <= 8 (measured 8); two-code-path hybrid (correct on paren-free lines, muldiv-right bug on paren lines) <= 8 (measured 8); and the union of all modeled wrong routes <= 9 entries (measured 8, equal to the paren-free structural floor) (trace B3/B5/B7/B11/B12/B13/C13).

#### Scenario: Two-code-path hybrid scores exactly the paren-free floor on the shipped literals
- **GIVEN** a solution that branches on whether a line contains `(`, evaluating paren-free lines correctly and paren lines with a right-recursive muldiv parser
- **WHEN** it is judged against the full 20-entry run
- **THEN** it is accepted on exactly entries 1-8, scoring 8/20, because every paren entry carries a PKline discriminator (trace B13)

---
### Requirement: Score-ladder disposition and co-opted routes
Semantically CORRECT alternative routes SHALL be co-opted as clever solutions and not hunted by test data: the operator-swap dunder eval (20/20 on apcs011), the regex-parenthesize-then-eval route (20/20 on apcs011), the lexically-patched power-encoding route E3' (20/20 on apcs012, fuzz-verified 1200/1200), and C-level rewrite loops (trace A3/A11/B4/C8). The challenge pages SHALL NOT mention these routes and SHALL NOT claim any route is impossible or that any score cap is structural (trace B4, design bounty F2). The 8/20 floor shared by parens-degrading routes on apcs012 equals the paren-free entry count and is accepted as deserved partial credit (trace B12/B13).

#### Scenario: Operator-swap eval on apcs012 is killed by associativity, not co-opted
- **GIVEN** the operator-swap dunder eval route that is correct on apcs011
- **WHEN** it is judged against apcs012's full 20-entry run
- **THEN** it is accepted on exactly entry 2, scoring 1/20, because Python's `*`/`/` are left-associative while apcs012 requires right-associative additive folding (trace B3)

---
### Requirement: Challenge-page language constraints
Both challenge pages SHALL use their independent life scenarios (apcs011: a snack-bar cash register with quirky firmware; apcs012: coupon stacking where discount coupons compound and bundle packages group) and SHALL NOT contain any data-structure terminology (stack, tree, LIFO, or their Chinese equivalents 堆疊/樹) (trace C11). The apcs012 page SHALL express right-associativity as "each coupon applies to the already-computed result of everything to its right", accompanied by a step-by-step worked breakdown of `10 - 4 - 3 + 2 * 6`; phrasing that only says "apply from the last coupon backwards" is insufficient because it admits a sequential-reapplication misreading (trace B14). Both pages SHALL state the value-domain guarantees of trace C3/C4, and the deep-nesting entries SHALL be framed as extreme historical-data edge cases without scenario justification (trace D6/F13).

#### Scenario: Right-associativity rule is stated unambiguously
- **GIVEN** the apcs012 challenge page rules section
- **WHEN** a reader follows the stated rule on `9 - 5 - 2`
- **THEN** the worked steps show 5-2 computed first and then 9-(3), yielding 6, with no alternative sequential reading available (trace B1/B14)

---
### Requirement: Verification and measurement discipline
Both challenges SHALL declare a `reference_solution` implemented independently of the generator (shunting-yard to RPN), and content-regression SHALL verify generator/reference agreement on the shipped encrypted pools (trace B10). After the challenge files ship, every V-table cell that has a standalone executable route file (V1-V5 and V7-V12: 11 route IDs, totaling 14 route-runs across the two challenges) SHALL be re-measured end-to-end in the browser judge (dev e2e), and the trace matrix ship-e2e column SHALL be filled from those measurements in the same change; cells without a standalone route file — V6 (uniform muldiv-right, both challenges) and V8 on `snack-bar-register` — SHALL remain recorded as design-probe only in the matrix, their behaviour covered by the archived curation script's per-entry predictor asserts (curation/plan_b.py, report in curation/report_b.json) and, on `coupon-combo-quote`, additionally bracketed end-to-end by the V8 and V10 measured runs; any later literal or generator modification SHALL mark affected measurements STALE and re-measure before commit (trace V1-V12, design I-5).

#### Scenario: Reference solutions agree across the full literal set
- **GIVEN** the generator and the independent RPN reference solution
- **WHEN** both are run over all 40 curated literals
- **THEN** their outputs are identical on every line
