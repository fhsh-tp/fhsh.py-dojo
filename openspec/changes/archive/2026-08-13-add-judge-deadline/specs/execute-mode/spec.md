## MODIFIED Requirements

### Requirement: Execute Composable Method

The `useExecutor` composable SHALL expose an `execute(code: string, stdin: string): Promise<ExecuteResult>` method.

This method SHALL create a fresh Worker, send an `ExecuteRequest`, and resolve the Promise with the `ExecuteResult` response.

The method SHALL apply a wall-clock kill timer (6 seconds). If the timer fires, the Worker SHALL be terminated and the Promise SHALL resolve with an error result.

The `execute` handler SHALL additionally apply the per-testcase deadline defined by the `judge-deadline` capability to the single execution it performs. When that deadline is reached, the running Python code SHALL be terminated and the Promise SHALL resolve with a timed-out result, without terminating the Worker. The 6-second kill timer SHALL remain as the outer bound covering the case where the Worker itself becomes unresponsive.

#### Scenario: Successful execute call

- **WHEN** `execute(code, stdin)` is called
- **THEN** a fresh Worker SHALL be created, the `ExecuteRequest` sent, and the Promise SHALL resolve with `{ stdout, elapsed_ms }`

#### Scenario: Wall-clock timeout

- **WHEN** the Worker does not respond within 6 seconds
- **THEN** the Worker SHALL be terminated and the Promise SHALL resolve with `{ stdout: '', error: 'Execution timed out', elapsed_ms: 6000 }`

#### Scenario: Deadline reached before the Worker kill timer

- **WHEN** code run through `execute` exceeds the per-testcase deadline but the Worker remains responsive
- **THEN** the Python execution SHALL be terminated at the deadline
- **AND** the Promise SHALL resolve with a timed-out result whose `elapsed_ms` reflects the deadline rather than the 6-second kill timer
- **AND** the Worker SHALL NOT be terminated
