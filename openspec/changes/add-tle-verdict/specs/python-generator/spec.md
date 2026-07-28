## ADDED Requirements

### Requirement: RunOnly results carry a structured timeout flag

The Worker's `run_only` handler SHALL classify op-limit timeouts at the point where the execution error is first received, by probing the wrapper's op counter state (`_op_count` left in the interpreter globals by the just-failed run): the failure is a timeout if and only if the count exceeds the request's op limit. Classification SHALL NOT match error-message text — a student raising their own `TimeoutError` (whose count is necessarily within the limit) stays an ordinary runtime error with its message preserved. The dev-mode `run` handler SHALL use the same probe so dev and prod classify identically.

When classified as a timeout, the posted `testcase_result` SHALL contain `timed_out: true` and SHALL NOT contain an `error` field (the timeout message embeds the op limit and must not reach the judging layer or the UI). Non-timeout failures SHALL keep the existing shape (`error` set, no `timed_out` key). Successful executions SHALL NOT report `timed_out: true`.

Downstream, the frontend collector SHALL attach the `timed_out` key to the objects passed to the WASM `judge` ONLY when its value is `true` — an explicit `timed_out: undefined` key is not "absent" to serde-wasm-bindgen and would poison the whole batch. Consumers SHALL treat `timed_out` as an opaque boolean.

#### Scenario: Op-limit timeout posts timed_out without error

- **WHEN** a `run_only` testcase execution fails and the interpreter's op count exceeds the request's op limit
- **THEN** the posted `testcase_result` contains `timed_out: true`, an empty `stdout`, and no `error` field

#### Scenario: Ordinary failure keeps the error shape

- **WHEN** a `run_only` testcase execution fails with the op count within the limit
- **THEN** the posted `testcase_result` contains the `error` message and no `timed_out` key

#### Scenario: Student-raised TimeoutError is not a TLE

- **WHEN** student code raises its own `TimeoutError` (or prints timeout-like text) without exceeding the op limit
- **THEN** the result is classified as an ordinary failure with the original error message preserved

#### Scenario: Frontend passes the flag through to the judge

- **WHEN** the production runner collects `run_only` results and calls the WASM `judge`
- **THEN** each timed-out result carries `timed_out: true` and every other result carries NO `timed_out` key at all
