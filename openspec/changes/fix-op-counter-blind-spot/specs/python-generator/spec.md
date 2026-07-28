## ADDED Requirements

### Requirement: Op-count guard covers flat top-level code

The Python wrapper produced by `buildWrappedCode` SHALL count operations executed in the module frame itself (flat top-level user code), not only in frames created after `sys.settrace` is installed. After installing the global tracer, the wrapper SHALL also attach the tracer to the currently executing frame so that line events in flat top-level code are counted. When the count exceeds `opLimit`, the wrapper SHALL raise `TimeoutError` with a message containing "Operation limit exceeded", identically for flat top-level code and function-wrapped code. For code that does not exceed the limit, the captured `_output` SHALL be byte-identical to the pre-fix wrapper's output.

#### Scenario: Flat top-level loop exceeding the limit is terminated

- **WHEN** flat top-level user code (no function definitions) executes more line events than `opLimit`
- **THEN** execution raises `TimeoutError` containing "Operation limit exceeded" instead of running to completion or being silently killed by the outer wall-clock budget

#### Scenario: Function-wrapped code behavior is unchanged

- **WHEN** user code defines a function and calls it, exceeding `opLimit` inside the function
- **THEN** execution raises `TimeoutError` containing "Operation limit exceeded", matching pre-fix behavior

#### Scenario: Normal flat code output is unaffected

- **WHEN** flat top-level user code completes within `opLimit`
- **THEN** the captured `_output` equals the code's stdout exactly as before the fix

### Requirement: Generator execution is exempt from the op-count guard

`buildWrappedCode` SHALL accept `opLimit: number | null`. When `opLimit` is `null`, the produced wrapper SHALL contain no tracer definition and no `sys.settrace` installation, while keeping the sandbox guard and stdin/stdout redirection unchanged. The Worker's `generate` handler SHALL execute generator code with `opLimit: null`. The `run`, `run_only`, and `execute` handlers SHALL keep the default limit of 10,000,000 operations.

#### Scenario: Generator with heavy computation is not killed

- **WHEN** the `generate` handler executes a trusted generator whose line-event count exceeds 10,000,000
- **THEN** generation completes normally because no op-count guard is injected

#### Scenario: Exempt wrapper keeps sandbox and I/O behavior

- **WHEN** `buildWrappedCode` is called with `opLimit: null`
- **THEN** the produced wrapper still blocks `js`/`pyodide` imports and still captures stdout into `_output`

### Requirement: Worker resets interpreter trace state before each execution

The wrapper's own `sys.settrace(None)` teardown executes only when user code completes normally; an ordinary user exception (the routine RE path) skips it and leaks the installed tracer into the shared interpreter. The leaked tracer — whose globals dict is cleared between runs — then kills the NEXT execution in its 'call' event with an unrelated NameError before its first line runs, falsely failing a correct testcase (self-healing after one poisoned run). To prevent this, every Worker handler (`run`, `run_only`, `execute`, `generate`) SHALL clear the interpreter's trace state by executing `sys.settrace(None)` before clearing globals and running the next wrapped code. The reset SHALL run before `globals.clear()` so the stale tracer's own state is still intact and the reset itself cannot be poisoned.

#### Scenario: An errored testcase does not poison the next

- **WHEN** testcase A raises an ordinary exception (e.g. IndexError) and testcase B with correct code runs next in the same interpreter
- **THEN** testcase B SHALL produce its correct output instead of failing with a stale-tracer NameError

#### Scenario: Reset precedes every execution

- **WHEN** any handler processes multiple inputs in one request
- **THEN** each input's execution SHALL be preceded by a trace-state reset followed by globals clearing

### Requirement: Real challenge content passes through the judging wrapper

The test suite SHALL execute the `reference_solution` of every challenge that declares one THROUGH `buildWrappedCode` (default op limit, tracing active) against sampled production-pool inputs, asserting the output matches the generator's expected output. This guards the actual judging execution path with real content — the content-regression suite runs solutions in a bare python3 subprocess and never exercises the wrapper.

#### Scenario: Reference solution survives the wrapper on real inputs

- **WHEN** a challenge declares `reference_solution` and the smoke suite runs it through the wrapper on sampled pool inputs
- **THEN** execution completes without error and the output matches the generator's expected output

### Requirement: Op-count guard is verified by executing real Python

The test suite SHALL include integration tests that execute the wrapper produced by `buildWrappedCode` with a real Python interpreter (system `python3`), asserting runtime behavior rather than wrapper string shape. The tests SHALL cover at minimum: a flat top-level loop exceeding the limit (fails with "Operation limit exceeded"), normal flat code (correct `_output`, no error), function-wrapped code exceeding the limit, and an exempt (`opLimit: null`) run of an over-limit loop completing normally. When `python3` is unavailable, these executions MAY be skipped following the same preflight pattern as the content-regression suite.

#### Scenario: Flat-code enforcement is proven by execution

- **WHEN** the integration test runs the wrapped flat over-limit loop under `python3`
- **THEN** the process fails and its stderr contains "Operation limit exceeded"

#### Scenario: String-shape assertions alone are insufficient

- **WHEN** the op-count guard behavior changes such that flat code is no longer counted
- **THEN** at least one integration test fails, even if the wrapper still textually contains `sys.settrace`
