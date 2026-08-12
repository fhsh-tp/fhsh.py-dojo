## MODIFIED Requirements

### Requirement: Bypass acceptance after hunt downgrade

The platform constraint that originally motivated this acceptance no longer holds. The worker 5-second wall-clock flag was a setTimeout macrotask, and for synchronous student code the await continuation (a microtask) always ran clearTimeout before an expired timer callback could fire, so the flag could never produce a TLE verdict for synchronous code. The `judge-deadline` capability replaces that flag with a per-testcase deadline that does not depend on the operation counter and that terminates synchronous Python code. This clause is amended here as the original clause required.

The C-builtin str.replace bypass SHALL continue to be treated as an accepted alternative solution. Its acceptance is now bounded by the per-testcase deadline of the `judge-deadline` capability rather than by the inertness of the former flag. Measured on the production path under the deadline, in its cheapest reasonable spelling (scanning only the characters present in the input rather than the full alphabet), the bypass scores 20 of 20 with a slowest single entry of 3,115 ms: it passes the full plan unchanged. The testcase plan SHALL NOT contain any entry whose purpose is to defeat it, and the plan SHALL NOT be modified by the change that introduces the deadline. The measured per-entry wall-clock time of the bypass SHALL be recorded in that change's design document.

Solutions that disable the tracer (for example `sys.settrace(None)`) are no longer outside the cliff guarantee: the deadline applies to them regardless of their counted operations, and such a solution was measured at 17 of 20 with three entries stopped by the deadline. Solutions that hardcode outputs keyed to the published literal entries remain outside the cliff guarantee, because the plan ships to the public repo and the client bundle.

#### Scenario: Bypass passes the full plan under the deadline

- **WHEN** the str.replace bypass solution is judged against the full 20-entry plan after the per-testcase deadline is in force
- **THEN** every entry SHALL report AC
- **AND** each entry's wall-clock time SHALL be recorded
- **AND** no entry SHALL be designated as a bypass hunt entry
- **AND** the plan's data SHALL be unchanged from before the deadline shipped

#### Scenario: Tracer-disabling solutions are covered by the deadline

- **WHEN** a solution that calls `sys.settrace(None)` exceeds the per-testcase deadline on an entry of this challenge's plan
- **THEN** that entry SHALL receive a TLE verdict
