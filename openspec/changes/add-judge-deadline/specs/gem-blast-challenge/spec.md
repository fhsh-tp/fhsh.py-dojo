## MODIFIED Requirements

### Requirement: Bypass acceptance after hunt downgrade

The platform constraint that originally motivated this acceptance no longer holds. The worker 5-second wall-clock flag was a setTimeout macrotask, and for synchronous student code the await continuation (a microtask) always ran clearTimeout before an expired timer callback could fire, so the flag could never produce a TLE verdict for synchronous code. The `judge-deadline` capability replaces that flag with a per-testcase deadline that does not depend on the operation counter and that terminates synchronous Python code.

Consequently: the C-builtin str.replace bypass SHALL be treated as an accepted alternative solution only for as long as its measured single-testcase wall-clock time stays below the per-testcase deadline. The testcase plan SHALL NOT contain any entry whose purpose is to defeat it, and the plan SHALL NOT be modified by the change that introduces the deadline. The measured per-entry wall-clock time of the bypass under the deadline SHALL be recorded in that change's design document, and it determines whether the bypass continues to pass without any change to this challenge's data.

Solutions that disable the tracer (for example `sys.settrace(None)`) are no longer outside the cliff guarantee: the deadline applies to them regardless of their counted operations. Solutions that hardcode outputs keyed to the published literal entries remain outside the cliff guarantee, because the plan ships to the public repo and the client bundle.

#### Scenario: Bypass measured against the full plan under the deadline

- **WHEN** the str.replace bypass solution is judged against the full 20-entry plan after the per-testcase deadline is in force
- **THEN** each entry's wall-clock time SHALL be recorded
- **AND** no entry SHALL be designated as a bypass hunt entry
- **AND** the plan's data SHALL be unchanged from before the deadline shipped

#### Scenario: Tracer-disabling solutions are covered by the deadline

- **WHEN** a solution that calls `sys.settrace(None)` exceeds the per-testcase deadline on an entry of this challenge's plan
- **THEN** that entry SHALL receive a TLE verdict
