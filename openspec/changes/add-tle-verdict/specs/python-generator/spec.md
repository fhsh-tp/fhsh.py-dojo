## ADDED Requirements

### Requirement: RunOnly results carry a structured timeout flag

The Worker's `run_only` handler SHALL classify op-limit timeouts at the point where the execution error is first received: when a testcase execution fails with the op-count guard's timeout signature (the same signature the dev-mode `run` handler already recognizes), the posted `testcase_result` SHALL contain `timed_out: true` and SHALL NOT contain an `error` field (the timeout message embeds the op limit and must not reach the judging layer or the UI). Non-timeout failures SHALL keep the existing shape (`error` set, no `timed_out` or `timed_out: false`). Successful executions SHALL NOT report `timed_out: true`. Classification SHALL happen only in the Worker — downstream consumers (the frontend collector and the WASM judge) SHALL treat `timed_out` as an opaque boolean.

#### Scenario: Op-limit timeout posts timed_out without error

- **WHEN** a `run_only` testcase execution fails with the op-count guard's timeout signature
- **THEN** the posted `testcase_result` contains `timed_out: true`, an empty `stdout`, and no `error` field

#### Scenario: Ordinary failure keeps the error shape

- **WHEN** a `run_only` testcase execution fails without the timeout signature
- **THEN** the posted `testcase_result` contains the `error` message and does not contain `timed_out: true`

#### Scenario: Frontend passes the flag through to the judge

- **WHEN** the production runner collects `run_only` results and calls the WASM `judge`
- **THEN** each collected result SHALL preserve the `timed_out` value exactly as posted by the Worker
