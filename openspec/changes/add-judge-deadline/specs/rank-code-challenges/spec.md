## MODIFIED Requirements

### Requirement: C-builtin bypass lethality

The testcase plans SHALL contain enough pressure testcases that each bypass enumerated in design D6.a fails: per-query math.factorial (and its math.perm sibling) for rank-code-backfill and un-modded Python-level big-integer products for prize-order-code SHALL exceed 2× the executor total wall budget (native measurement multiplied by conservative factor 2 for Pyodide), and the str()-based digit extraction path SHALL raise ValueError under int_max_str_digits=4300. Verification SHALL be recorded per-bypass in dev-verification-notes.md; bypasses outside the D6.a list are out of scope.

The math.perm-with-Legendre trailing-zero route for prize-order-code (matrix F19/F20, design D6.b) SHALL remain out of scope for testcase-plan tuning: the plans SHALL NOT be modified to defeat it, and its score SHALL NOT be treated as a defect of this challenge's data.

Its acceptance is nevertheless bounded by the per-testcase wall-clock deadline defined by the `judge-deadline` capability, which applies to every submission regardless of how it spends its time. That route builds a product of up to one hundred thousand terms as an exact integer, and its cost is borne inside C rather than in counted operations, so the operation limit never sees it while the clock does. Measured under the deadline on the production path: 12 of 20 entries accepted, seven stopped at the deadline, and 3,880 ms on the slowest entry that completed. The route is therefore a documented alternative that no longer passes in full, and that outcome SHALL be attributed to the platform deadline rather than to this challenge's testcase plan.

#### Scenario: stringify path dies

- **GIVEN** a student solution that builds the full product and calls str() on it
- **WHEN** it runs on any pressure testcase of prize-order-code
- **THEN** the conversion raises ValueError (result exceeds 4300 digits)

#### Scenario: residual bypass is bounded by the deadline, not by the plan

- **GIVEN** the prize-order-code surviving route recorded in design D6.b (math.perm with Legendre trailing-zero counting)
- **WHEN** it runs on the production pool
- **THEN** the entries it completes within the per-testcase deadline are accepted
- **AND** the entries whose wall clock reaches the deadline receive TLE
- **AND** the testcase plan SHALL be unchanged from before the deadline shipped
