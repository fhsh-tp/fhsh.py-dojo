## ADDED Requirements

### Requirement: Exhibit route rebuild I/O contract
The challenge `exhibit-route-rebuild` SHALL accept input of: first line integer T (T >= 1); then T groups, each of three lines — a line `M n` (M is 1 or 2, 1 <= n <= 1500), a line of n room ids, and a second line of n room ids (trace A1/A8). Room ids SHALL be a random permutation of 1..n, never the sorted order of any check-in sequence (trace A7). When M = 1 the two id lines are guide A's and guide B's check-in orders and the output SHALL be guide C's order; when M = 2 they are guide B's and guide C's orders and the output SHALL be guide A's order (trace A1). Guide A checks in on entering a room, then covers the left branch, then the right branch; guide B covers the left branch, checks in, then covers the right branch; guide C covers the left branch, then the right branch, then checks in. Each group SHALL produce exactly one output line of n ids separated by single spaces. Both mappings are injective when ids are pairwise distinct, so every group has exactly one valid answer (trace A13). The layout depth of every shipped group SHALL be at most 300 (trace A5), derived from the measured 994-frame recursion ceiling (trace C6).

#### Scenario: Mode 1 rebuild
- **GIVEN** a group `1 7` with first line `2 1 5 3 6 4 7` and second line `3 5 1 6 2 7 4`
- **WHEN** the group is processed
- **THEN** the output line is `3 5 6 1 7 4 2`

#### Scenario: Mode 2 rebuild
- **GIVEN** a group `2 7` with first line `6 1 2 4 3 5 7` and second line `6 1 4 2 5 7 3`
- **WHEN** the group is processed
- **THEN** the output line is `3 2 1 6 4 7 5`

#### Scenario: Single-room group
- **GIVEN** a group with n = 1
- **WHEN** the group is processed
- **THEN** the output line is that single id, in both modes

---
### Requirement: Exhibit route rebuild testcase plan
The challenge `exhibit-route-rebuild` SHALL declare a 20-entry all-literal `testcase_plan` with `input_budget: 63488` (trace C7/A8), every entry at most 50,000 bytes (measured maximum 20,588). Entries 1-10 SHALL contain mode 1 groups only; entry 11 SHALL be a single mode 2 group; entries 12-20 SHALL each hold five groups containing both modes, and their nine mode sequences SHALL be pairwise distinct (trace D4/A16). Mixing is what caps the mode-marker-read-once route at 11/20; pairwise-distinct sequences are what cap the wider family that reads only the first marker and infers the rest from position at 12/20, since the best rule keyed on (group count, first mode, position) can only match the most frequent sequence per key. Were all nine sequences identical, that family would score 20/20. Entries 1 and 11 are the challenge page's two worked examples and SHALL be byte-identical to them; they are exempt from discrimination duty, and every other entry SHALL have a largest group of n >= 20 (trace A15). The n >= 20 rule does not by itself defeat shape enumeration — enumeration is only infeasible above roughly n = 9 — it keeps small groups from being the sole carriers of discrimination; the actual defence is the pair of zero-rebuild routes contracted at 2/20 below, which the data must falsify entry by entry. Every entry with two or more groups SHALL contain at least two distinct structural signatures, at least one group that is not a single path, and at least one group whose mirror image has a different structure (trace A9/A10); shape names SHALL NOT be used for these checks, because the spine family degenerates to a plain chain at n <= 120. Every entry containing a mode 2 group SHALL contain a mode 2 group that is not a single path and has n >= 3, since left-chain mode 2 groups are immune to the mode-blind misreading (trace A14). The plan SHALL cover n = 1 and SHALL include at least one group with n >= 1000 (measured maximum 1400). All literal content SHALL be produced by `curation/plan013.py` from `curation/semantics013.py` and embedded byte-for-byte by `curation/assemble.py`, never hand-edited (trace C8).

#### Scenario: Assertion wall blocks shipping
- **GIVEN** any change to the entry table, shapes or seeds in `curation/plan013.py`
- **WHEN** `python3 plan013.py` runs
- **THEN** it recomputes every route score and structural check, and exits non-zero without writing literals if any contract in the wall is violated

---
### Requirement: Exhibit route rebuild wrong-route discrimination
The shipped 20 entries SHALL hold every wrong route at its contracted score, verified mechanically per entry by `curation/plan013.py`, whose `CAPS` dictionary is the authoritative route list (trace A6): mode-blind exactly 10/20; mode-marker-read-once exactly 11/20; mode 2 taking guide C's first id as the entrance at most 10/20; mode 2 expanding the left side before the right at most 10/20 (trace A6b — a consistent global left/right renaming is a symmetry of the problem, produces the correct output, and SHALL NOT be hunted); sorted-ids-as-second-sequence exactly 0/20; first-group-only exactly 2/20 (the two single-group example entries); reverse-first, echo-second, echo-first, reverse-second and descending-sort exactly 0/20; the shape-dictionary route that only runs forward walks and never rebuilds exactly 2/20, and the same route extended with exhaustive shape enumeration for small groups likewise exactly 2/20 (example entries only). The family that reads only the first mode marker and infers the remaining modes from position SHALL score at most 12/20, verified by computing the best achievable rule rather than one hand-written spelling. The `.exp` files produced alongside each literal SHALL be the sole source of expected output in these comparisons.

#### Scenario: Mode-blind solution scores exactly half
- **GIVEN** a solution that applies the mode 1 rebuild to every group regardless of the marker
- **WHEN** it is judged against the full 20-entry block
- **THEN** it passes entries 1-10 and fails entries 11-20, scoring 10/20

#### Scenario: Positional mode guessing cannot clear the ladder
- **GIVEN** any solution that reads only the first group's mode marker and derives every other group's mode from its position
- **WHEN** it is judged against the full 20-entry block
- **THEN** it scores at most 12/20, because the nine mixed entries carry pairwise distinct mode sequences

#### Scenario: Shape-dictionary route cannot clear the ladder
- **GIVEN** a solution that generates the fixed shape families for the given n, matches them against the input by forward walks and prints the third sequence without rebuilding anything
- **WHEN** it is judged against the full 20-entry block
- **THEN** it clears only the two example entries, scoring 2/20

---
### Requirement: Exhibit route rebuild performance envelope and bypass disposition
The `reference_solution` SHALL stay within 100,000 traced ops on the worst shipped entry (measured 37,537) and the `generator` within 150,000 (measured 71,663), both far below the 10,000,000 per-testcase limit (trace C1/A0). Two routes are ACCEPTED ALTERNATIVES and SHALL keep scoring 20/20: the C-level route that locates the entrance with `list.index()` and recurses over slices (measured 25,036 ops on the worst shipped entry — cheaper than the reference, because builtin work is not traced, trace C2/A3), and the mirror route that solves mode 2 by reversing both sequences, running the mode 1 rebuild and reversing the result (measured 77,609 ops, trace A12). No op cliff SHALL be built for this challenge: the pure-Python scanning variant would need an n ~ 6000 chain to exceed the limit, which violates the depth bound (trace A4). The challenge page SHALL NOT claim any route impossible, SHALL make no performance promise beyond the stated depth bound, and SHALL NOT imply that the two modes must each be implemented separately (trace A12/D6).

#### Scenario: Deepest shipped layout does not break plain recursion
- **GIVEN** a recursive rebuild that uses one stack frame per layout level and does not raise the interpreter recursion limit
- **WHEN** it runs on the depth-300 entry
- **THEN** it completes without RecursionError (measured 17,847 ops, entry 19)
