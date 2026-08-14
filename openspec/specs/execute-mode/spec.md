# execute-mode Specification

## Purpose

Defines the "Run" execute mode that allows users to run their code against custom stdin input in a modal dialog, separate from the "Submit" judge flow. Includes the `ExecuteRequest` Worker protocol, `RunModal` UI, split button layout, and the `useExecutor` composable with wall-clock timeout.

## Requirements

### Requirement: Execute Request Worker Protocol

The Pyodide Worker SHALL accept an `ExecuteRequest` message with type `execute`, containing `code` (string), `stdin` (string), and optional `opLimit` (number, default 10,000,000).

The Worker SHALL respond with a single `ExecuteResult` message containing `stdout` (string), optional `error` (string), and `elapsed_ms` (number).

The Worker SHALL reuse the same sandbox guard, op-count TLE guard, and namespace cleanup as the existing `run` handler. The Worker SHALL NOT perform verdict comparison.

#### Scenario: Successful execution

- **WHEN** the Worker receives an `ExecuteRequest` with valid Python code and stdin
- **THEN** the Worker SHALL execute the code with the provided stdin, capture stdout, and respond with `{ type: 'execute_result', stdout: <captured>, elapsed_ms: <ms> }`

#### Scenario: Runtime error during execution

- **WHEN** the Worker receives an `ExecuteRequest` and the user code raises an exception
- **THEN** the Worker SHALL respond with `{ type: 'execute_result', stdout: '', error: <error message>, elapsed_ms: <ms> }`

#### Scenario: Operation limit exceeded

- **WHEN** the Worker receives an `ExecuteRequest` and the code exceeds the op limit
- **THEN** the Worker SHALL respond with `{ type: 'execute_result', stdout: '', error: <timeout message>, elapsed_ms: <ms> }`


<!-- @trace
source: add-execute-mode
updated: 2026-03-24
code:
  - .vitepress/theme/composables/useExecutor.ts
  - .vitepress/theme/components/editor/RunModal.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/workers/pyodide.worker.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-execute.spec.ts
  - .vitepress/theme/__tests__/RunModal.spec.ts
  - .vitepress/theme/__tests__/useExecutor.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
-->

---
### Requirement: Run Modal UI

The system SHALL provide a `RunModal` component that opens when the user clicks the "Run" button.

The modal SHALL contain an editable textarea for stdin input, pre-filled with the first testcase's input when testcases are available, or empty string when testcases are not yet generated.

The modal SHALL contain a read-only output area that displays stdout after execution, or an error message if execution failed.

The modal SHALL remain open after execution completes, allowing the user to modify stdin and re-execute.

#### Scenario: Open modal with testcases ready

- **WHEN** testcases are generated and the user clicks "Run"
- **THEN** the modal SHALL open with the stdin textarea pre-filled with testcase[0].input

#### Scenario: Open modal before testcases ready

- **WHEN** testcases are not yet generated and the user clicks "Run"
- **THEN** the modal SHALL open with the stdin textarea empty

#### Scenario: Execute code in modal

- **WHEN** the user clicks "Execute" in the modal
- **THEN** the system SHALL send an `ExecuteRequest` to a fresh Worker, display a loading state, and show the stdout result in the output area upon completion

#### Scenario: Re-execute with modified input

- **WHEN** the user modifies the stdin textarea and clicks "Execute" again
- **THEN** the system SHALL execute the code with the updated stdin and replace the previous output

#### Scenario: Close modal during execution

- **WHEN** the user closes the modal while execution is in progress
- **THEN** the system SHALL terminate the active Worker immediately


<!-- @trace
source: add-execute-mode
updated: 2026-03-24
code:
  - .vitepress/theme/composables/useExecutor.ts
  - .vitepress/theme/components/editor/RunModal.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/workers/pyodide.worker.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-execute.spec.ts
  - .vitepress/theme/__tests__/RunModal.spec.ts
  - .vitepress/theme/__tests__/useExecutor.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
-->

---
### Requirement: Button Layout Split

The button bar SHALL display two separate buttons: "Run" (triggers modal) and "Submit" (triggers existing judge flow).

The "Run" button SHALL be positioned before the "Submit" button.

The "Run" button SHALL be enabled regardless of testcase readiness. The "Submit" button SHALL remain disabled until testcases are generated, preserving existing behavior.

#### Scenario: Both buttons visible

- **WHEN** the challenge page loads
- **THEN** both "Run" and "Submit" buttons SHALL be visible in the button bar

#### Scenario: Run button enabled before testcases

- **WHEN** testcases are not yet generated
- **THEN** the "Run" button SHALL be enabled and the "Submit" button SHALL be disabled with a loading indicator

#### Scenario: Submit triggers judge flow

- **WHEN** testcases are generated and the user clicks "Submit"
- **THEN** the system SHALL execute the existing judge flow with all testcases, identical to the current behavior


<!-- @trace
source: add-execute-mode
updated: 2026-03-24
code:
  - .vitepress/theme/composables/useExecutor.ts
  - .vitepress/theme/components/editor/RunModal.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/workers/pyodide.worker.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-execute.spec.ts
  - .vitepress/theme/__tests__/RunModal.spec.ts
  - .vitepress/theme/__tests__/useExecutor.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
-->

---
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
