# judge-deadline Specification

## Purpose

TBD - created by archiving change 'add-judge-deadline'. Update Purpose after archive.

## Requirements

### Requirement: Every judged testcase has an enforced wall-clock deadline

The judge SHALL enforce a per-testcase wall-clock deadline on student code in all three execution handlers (`run`, `run_only`, `execute`). The deadline SHALL be a single site-wide constant; it SHALL NOT be configurable per challenge through frontmatter.

Enforcement SHALL NOT depend on the operation counter. A submission that disables the tracer, that flattens loop iterations onto a single source line, or that otherwise reduces its counted operations SHALL still be terminated when it exceeds the deadline.

#### Scenario: Submission exceeding the deadline is terminated and judged TLE

- **WHEN** student code on a single testcase runs longer than the deadline
- **THEN** execution of that testcase SHALL be terminated
- **AND** that testcase SHALL receive a TLE verdict
- **AND** the remaining testcases of the same submission SHALL still be executed

#### Scenario: Deadline holds when the operation counter is disabled

- **WHEN** student code calls `sys.settrace(None)` at its start and then runs longer than the deadline on a testcase
- **THEN** that testcase SHALL receive a TLE verdict

#### Scenario: Deadline holds when operation cost is diluted by source layout

- **WHEN** student code performs its loop iterations on a single source line so that the operation counter records at most one event per iteration batch, and runs longer than the deadline on a testcase
- **THEN** that testcase SHALL receive a TLE verdict

#### Scenario: Submission within the deadline is unaffected

- **WHEN** student code completes a testcase in less than the deadline
- **THEN** the verdict SHALL be determined by output comparison and the operation limit exactly as before this capability existed

---
### Requirement: The deadline is enforced by an interrupt buffer armed per testcase

The judge SHALL enforce the deadline by writing an interrupt request into a `SharedArrayBuffer` registered with the Pyodide runtime, from a JavaScript context that is not blocked by the executing Python code. The interrupt SHALL cause the running Python code to raise, and the Pyodide runtime SHALL remain usable for subsequent testcases.

The interrupt request SHALL be armed immediately before user code begins executing and disarmed immediately after it stops. It SHALL NOT be left armed across the runtime's own initialisation or teardown work. Each arming SHALL carry a generation identifier so that a scheduled expiry belonging to an earlier testcase cannot interrupt a later one.

#### Scenario: Runtime survives an interrupt and continues

- **WHEN** a testcase is terminated by the deadline
- **THEN** the following testcase SHALL execute normally and produce its verdict

#### Scenario: Consecutive interrupts do not corrupt the batch

- **WHEN** several consecutive testcases of one submission each exceed the deadline
- **THEN** every testcase of the submission SHALL still produce a result
- **AND** the number of reported results SHALL equal the number of testcases

#### Scenario: Stale expiry does not affect a later testcase

- **WHEN** the expiry belonging to a finished testcase fires while a later testcase is executing
- **THEN** the later testcase SHALL NOT be interrupted by it

---
### Requirement: Student code cannot suppress the deadline verdict

A testcase whose measured elapsed time exceeds the deadline SHALL receive a TLE verdict regardless of how the executing code responded to the interrupt. The judge SHALL adjudicate on elapsed time measured outside the Python runtime, in addition to the interrupt mechanism.

#### Scenario: Catching the interrupt does not yield a pass

- **WHEN** student code wraps its computation in an exception handler that catches the interrupt and continues, and its elapsed time on a testcase exceeds the deadline
- **THEN** that testcase SHALL receive a TLE verdict

---
### Requirement: Judging degrades rather than fails without SharedArrayBuffer

When `SharedArrayBuffer` is unavailable in the running environment, judging SHALL proceed without the interrupt mechanism and SHALL adjudicate the deadline from measured elapsed time alone. The degraded state SHALL be observable to a developer inspecting the console; it SHALL NOT be silent, and it SHALL NOT surface as an error to the student.

#### Scenario: Deadline still adjudicated without the interrupt mechanism

- **WHEN** the environment does not provide `SharedArrayBuffer` and student code exceeds the deadline on a testcase
- **THEN** that testcase SHALL receive a TLE verdict after the code finishes running
- **AND** no error SHALL be shown to the student attributing the situation to the environment

---
### Requirement: Production judging receives the deadline verdict

The `run_only` handler used by the production strategy SHALL report a terminated testcase through the structured timeout flag already consumed by the WASM judge, so that the production verdict for such a testcase is TLE rather than RE or WA.

#### Scenario: Production path reports TLE

- **WHEN** a submission exceeds the deadline on a testcase in production mode
- **THEN** the worker SHALL report that testcase with the structured timeout flag set
- **AND** the WASM judge SHALL return the TLE verdict for it

---
### Requirement: The deadline constant is derived from measurement of shipped challenges

The deadline constant SHALL be selected so that it exceeds the largest single-testcase wall-clock time measured, in a browser, across the `reference_solution` of every shipped challenge and every route recorded as co-opted in a shipped challenge's specification, by a stated safety factor. The selected value SHALL also be below the single-testcase wall-clock time of the two recorded bypass routes.

If no value satisfies both bounds, the change SHALL record the conflict and SHALL retain the previous behavior rather than select a value that would change the verdict of any shipped challenge.

#### Scenario: Shipped challenges keep their verdicts

- **WHEN** the `reference_solution` of any shipped challenge is submitted in a browser after this capability ships
- **THEN** its score SHALL equal the score recorded for it before this capability shipped

---
### Requirement: Interrupted batches are displayed honestly

When a submission is terminated by the cumulative batch limit before all testcases have reported, the result table SHALL use the total number of testcases as its denominator, and testcases that never reported SHALL be displayed as not executed rather than omitted.

#### Scenario: Truncated batch does not appear fully passed

- **WHEN** a submission is terminated by the cumulative batch limit after some testcases have reported passes and the rest have not reported
- **THEN** the result table SHALL show one row per testcase of the challenge
- **AND** the rows that never reported SHALL be visually distinct from passing rows
