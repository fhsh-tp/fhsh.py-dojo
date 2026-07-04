# challenge-runner-orchestration Specification

## Purpose

Defines the `useChallengeRunner` composable that provides a unified API for challenge testcase loading, student code submission, and verdict retrieval. It abstracts over two internal strategies: a dev strategy using WASM input generation plus Pyodide Worker execution, and a production strategy using encrypted pool decryption plus WASM-based judging.

## Requirements

### Requirement: useChallengeRunner composable provides unified challenge lifecycle API

A `useChallengeRunner` composable SHALL provide a unified API for challenge testcase loading, student code submission, and verdict retrieval. It SHALL abstract over two internal strategies (dev and production) while exposing the same interface. The composable SHALL accept challenge configuration and return reactive bindings. The configuration SHALL include a required `id` field (the per-challenge unique slug, equal to the markdown file basename without `.md`) in addition to `algorithm`, `params`, `generator`, `testcaseCount`, `starterCode`, and `verdictDetail`. The `id` field SHALL be the sole key used by the production strategy to locate the encrypted pool file and to address the WASM pool-judge module. The `algorithm` field SHALL remain available as educational metadata (e.g., for navigation grouping) and SHALL NOT participate in pool fetch URLs, `load_pool` keys, or `judge` keys.

The composable SHALL return:

- `loadTestcases(): Promise<void>` — initiates testcase preparation
- `inputs: Ref<string[]>` — reactive list of testcase input strings
- `submit(code: string): Promise<void>` — runs student code and produces verdicts
- `isReady: Ref<boolean>` — true when testcases are loaded and ready for submission
- `verdictDetail: VerdictDetail` — the resolved verdict detail mode
- `errorMessage: Ref<string>` — error state for display

#### Scenario: Composable returns all required reactive properties

- **WHEN** `useChallengeRunner` is called with valid challenge configuration including a non-empty `id`
- **THEN** it SHALL return `loadTestcases`, `inputs`, `submit`, `isReady`, `verdictDetail`, and `errorMessage`

#### Scenario: Configuration without id fails at type-check

- **WHEN** a caller constructs a `RunnerConfig` object without the `id` field
- **THEN** the TypeScript compiler SHALL emit an error indicating the missing required property
- **AND** the runtime SHALL NOT silently fall back to using `algorithm` as the pool key


<!-- @trace
source: isolate-testcase-pools-per-challenge
updated: 2026-07-04
code:
  - AGENTS.md
  - .github/prompts/spectra-propose.prompt.md
  - CONTRIBUTE.md
  - .vitepress/theme/composables/useApi.ts
  - scripts/generate-key-material.ts
  - .github/prompts/spectra-drift.prompt.md
  - tsconfig.vitest.json
  - .vitepress/sidebar.ts
  - .vitepress/theme/composables/useChallengeRunner.ts
  - .github/prompts/spectra-apply.prompt.md
  - testcase-generator/src/lib.rs
  - tsconfig.node.json
  - .github/skills/spectra-discuss/SKILL.md
  - eslint.config.mjs
  - .github/skills/spectra-ingest/SKILL.md
  - .vitepress/theme/views/ChallengeView.vue
  - scripts/gen-key-material.ts
  - .github/workflows/release.yml
  - CLAUDE.md
  - .github/skills/spectra-drift/SKILL.md
  - docs/challenge/hello-world.md
  - scripts/new-tutor.ts
  - docs/challenge/multiplication-table.md
  - .vitepress/theme/composables/index.ts
  - .spectra.yaml
  - testcase-generator/Cargo.toml
  - Usage.md
  - .github/skills/spectra-apply/SKILL.md
  - package.json
  - scripts/new-challenge.ts
  - docs/shared/tutor.data.ts
  - docs/challenge/prime-check.md
  - scripts/generate-pools.ts
  - README.md
  - docs/shared/exercise-type.ts
  - docs/shared/challenge.data.ts
  - CHANGELOG.md
  - .github/skills/spectra-propose/SKILL.md
  - GEMINI.md
  - .github/workflows/ci.yml
  - .github/prompts/spectra-discuss.prompt.md
  - .github/prompts/spectra-ingest.prompt.md
tests:
  - docs/shared/exercise-type.test.ts
  - .vitepress/plugins/markdown-mermaid.test.ts
  - scripts/new-challenge.test.ts
  - .vitepress/theme/__tests__/useApi.spec.ts
  - scripts/generator-parity.test.ts
  - .vitepress/theme/__tests__/ChallengeView.spec.ts
  - testcase-generator/tests/param_conformance.rs
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
  - scripts/content-regression.test.ts
  - scripts/generate-pools.test.ts
-->

---
### Requirement: Dev strategy uses existing WASM + Pyodide generator flow

When `import.meta.env.MODE === 'development'`, the composable SHALL use the dev strategy:

1. Call WASM `generate_challenge(params_json, count)` to obtain random inputs
2. Spawn a Pyodide Worker with `GenerateRequest` to run generator code and produce `{input, expected_output}[]`
3. On `submit()`, spawn a Pyodide Worker with `RunRequest` containing student code and testcases (with expected_output)
4. Produce verdicts from Worker `TestcaseResult` messages

This preserves the current development experience where generator changes take effect immediately without rebuilding pools.

#### Scenario: Dev mode uses generator from frontmatter

- **WHEN** the app runs in development mode
- **THEN** the composable SHALL read `generator` from frontmatter and execute it via Pyodide Worker to produce expected outputs

#### Scenario: Dev mode submit sends expected_output to Worker

- **WHEN** `submit()` is called in dev mode
- **THEN** the Worker SHALL receive a `RunRequest` containing testcases with `expected_output` for comparison


<!-- @trace
source: secure-challenge-pools
updated: 2026-04-02
code:
  - testcase-generator/src/lib.rs
  - testcase-generator/src/pool.rs
  - testcase-generator/Cargo.toml
  - .vitepress/plugins/strip-generator.ts
  - testcase-generator/src/judge.rs
  - scripts/generate-key-material.ts
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useChallengeRunner.ts
  - package.json
  - .vitepress/config.mts
  - testcase-generator/src/crypto.rs
  - scripts/generate-pools.ts
  - scripts/pool-key.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
-->

---
### Requirement: Prod strategy uses encrypted pool + WASM judge flow

When `import.meta.env.MODE === 'production'`, the composable SHALL use the production strategy:

1. Fetch the encrypted pool file from `/pools/<id>.bin` where `<id>` is the per-challenge slug from the runner configuration
2. Call WASM `load_pool(<id>, data)` to decrypt; the same `<id>` SHALL be passed to all subsequent WASM calls
3. Call WASM `select_testcases(<id>, count)` to get `{inputs, session_id, verdict_detail}` and store the returned `verdict_detail` as the authoritative display setting
4. On `submit()`, spawn a Pyodide Worker with a `RunOnlyRequest` message containing `{type: 'run_only', code, inputs}` — no `expected_output`, no `verdictDetail`, no `testcases` array. The `inputs` array passed via `postMessage` SHALL be a plain JavaScript Array (e.g. created via spread operator or `Array.from`), NOT a Vue reactive Proxy or WASM-backed object, to ensure compatibility with the browser's structured clone algorithm.
5. Collect Worker raw stdout outputs
6. Call WASM `judge(<id>, session_id, outputs)` to obtain verdicts

The production strategy SHALL NOT use the `algorithm` field for any of these calls. Expected output SHALL NOT pass through any JS-accessible variable, `postMessage`, or Pinia store when `verdict_detail` is `hidden` or `actual`.

The composable SHALL expose `verdictDetail` as a reactive value sourced from the pool's `select_testcases` return. It SHALL NOT use the frontmatter-derived `config.verdictDetail` in production mode. This ensures the display behavior is controlled by the integrity-protected pool payload, not by client-side frontmatter that could be tampered with or become inconsistent with the pool.

#### Scenario: Prod mode fetches encrypted pool by slug

- **WHEN** the app runs in production mode and a challenge page with slug `multiplication-table` loads
- **THEN** the composable SHALL fetch `/pools/multiplication-table.bin` and pass it to WASM `load_pool` with the same slug
- **AND** the composable SHALL NOT fetch `/pools/<algorithm>.bin` for any value of `<algorithm>`

#### Scenario: Pool fetch failure surfaces without algorithm fallback

- **WHEN** `fetch('/pools/<id>.bin')` returns a non-OK response or throws
- **THEN** the composable SHALL set `errorMessage` to indicate the pool could not be loaded
- **AND** the composable SHALL NOT retry with `/pools/<algorithm>.bin` or any other URL

#### Scenario: Prod mode does not expose expected_output in JS when hidden

- **WHEN** `verdict_detail` is `hidden` and the production strategy is active
- **THEN** no JS variable, `postMessage` payload, or Pinia store SHALL contain `expected_output` at any point

#### Scenario: Prod mode submit sends RunOnlyRequest to Worker

- **WHEN** `submit()` is called in production mode
- **THEN** the Worker SHALL receive a `RunOnlyRequest` message with `{type: 'run_only', code, inputs}` containing no `expected_output`, no `verdictDetail`, and no `testcases` array

#### Scenario: Prod mode inputs passed to Worker are structured-clone-compatible

- **WHEN** the prod runner calls `postMessage` to send a `RunOnlyRequest` to the Pyodide Worker
- **THEN** the `inputs` field SHALL be a plain JavaScript Array of strings, NOT a Vue reactive Proxy or WASM-returned object
- **AND** the `postMessage` call SHALL NOT throw a `DataCloneError`

#### Scenario: Prod mode verdictDetail comes from pool

- **WHEN** the production strategy calls `select_testcases` and receives `verdict_detail: "actual"` from the pool
- **THEN** the composable's exposed `verdictDetail` value SHALL be `"actual"`
- **AND** the frontmatter-derived `config.verdictDetail` SHALL NOT be used for UI display decisions

#### Scenario: Prod mode verdictDetail updates on re-select

- **WHEN** a session is consumed by `judge()` and `select_testcases` is called again
- **THEN** the composable's exposed `verdictDetail` SHALL reflect the latest `select_testcases` return value


<!-- @trace
source: isolate-testcase-pools-per-challenge
updated: 2026-07-04
code:
  - AGENTS.md
  - .github/prompts/spectra-propose.prompt.md
  - CONTRIBUTE.md
  - .vitepress/theme/composables/useApi.ts
  - scripts/generate-key-material.ts
  - .github/prompts/spectra-drift.prompt.md
  - tsconfig.vitest.json
  - .vitepress/sidebar.ts
  - .vitepress/theme/composables/useChallengeRunner.ts
  - .github/prompts/spectra-apply.prompt.md
  - testcase-generator/src/lib.rs
  - tsconfig.node.json
  - .github/skills/spectra-discuss/SKILL.md
  - eslint.config.mjs
  - .github/skills/spectra-ingest/SKILL.md
  - .vitepress/theme/views/ChallengeView.vue
  - scripts/gen-key-material.ts
  - .github/workflows/release.yml
  - CLAUDE.md
  - .github/skills/spectra-drift/SKILL.md
  - docs/challenge/hello-world.md
  - scripts/new-tutor.ts
  - docs/challenge/multiplication-table.md
  - .vitepress/theme/composables/index.ts
  - .spectra.yaml
  - testcase-generator/Cargo.toml
  - Usage.md
  - .github/skills/spectra-apply/SKILL.md
  - package.json
  - scripts/new-challenge.ts
  - docs/shared/tutor.data.ts
  - docs/challenge/prime-check.md
  - scripts/generate-pools.ts
  - README.md
  - docs/shared/exercise-type.ts
  - docs/shared/challenge.data.ts
  - CHANGELOG.md
  - .github/skills/spectra-propose/SKILL.md
  - GEMINI.md
  - .github/workflows/ci.yml
  - .github/prompts/spectra-discuss.prompt.md
  - .github/prompts/spectra-ingest.prompt.md
tests:
  - docs/shared/exercise-type.test.ts
  - .vitepress/plugins/markdown-mermaid.test.ts
  - scripts/new-challenge.test.ts
  - .vitepress/theme/__tests__/useApi.spec.ts
  - scripts/generator-parity.test.ts
  - .vitepress/theme/__tests__/ChallengeView.spec.ts
  - testcase-generator/tests/param_conformance.rs
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
  - scripts/content-regression.test.ts
  - scripts/generate-pools.test.ts
-->

---
### Requirement: ChallengeView delegates to useChallengeRunner

`ChallengeView.vue` SHALL NOT directly call `useWasm()`, spawn generator Workers, store `localTestcases`, or manage verdict logic. It SHALL use `useChallengeRunner` as the sole interface for testcase lifecycle. The view SHALL only be responsible for UI layout, user interaction, and passing data between `useChallengeRunner` and UI components.

#### Scenario: ChallengeView does not import useWasm directly

- **WHEN** inspecting `ChallengeView.vue` imports
- **THEN** it SHALL NOT import `useWasm` or `GenerateRequest`

#### Scenario: ChallengeView does not hold expected_output

- **WHEN** inspecting `ChallengeView.vue` variables
- **THEN** no variable SHALL contain `expected_output` data

<!-- @trace
source: secure-challenge-pools
updated: 2026-04-02
code:
  - testcase-generator/src/lib.rs
  - testcase-generator/src/pool.rs
  - testcase-generator/Cargo.toml
  - .vitepress/plugins/strip-generator.ts
  - testcase-generator/src/judge.rs
  - scripts/generate-key-material.ts
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useChallengeRunner.ts
  - package.json
  - .vitepress/config.mts
  - testcase-generator/src/crypto.rs
  - scripts/generate-pools.ts
  - scripts/pool-key.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
-->

---
### Requirement: Prod runner stop cancels in-flight submission and settles Promise

When the production runner's `stop()` is called while `runStudentCode` is in-flight, the runner SHALL cancel the pending `killTimer`, terminate the worker, and cause the `runStudentCode` Promise to settle (resolve with `null`). After `stop()` returns, `isRunning` SHALL be `false` and the `submit()` Promise SHALL NOT remain pending indefinitely.

#### Scenario: Stop during prod submission settles Promise

- **WHEN** `submit()` is in progress in the production runner and `stop()` is called
- **THEN** the `killTimer` SHALL be cleared
- **AND** the worker SHALL be terminated
- **AND** the `runStudentCode` Promise SHALL resolve with `null`
- **AND** `isRunning` SHALL be `false`

#### Scenario: Stop when no submission is in-flight is a no-op

- **WHEN** `stop()` is called on the production runner while no submission is running
- **THEN** the call SHALL have no effect and SHALL NOT throw

#### Scenario: KillTimer does not fire after stop

- **WHEN** `stop()` is called during an in-flight prod submission
- **THEN** the `killTimer` callback SHALL NOT execute after `stop()` completes

<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useChallengeRunner.ts
tests:
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
-->


<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useRemoteChallenge.ts
  - testcase-generator/src/pool.rs
  - README.md
  - .vitepress/theme/workers/pyodide.worker.ts
  - testcase-generator/src/judge.rs
  - .vitepress/plugins/strip-generator.ts
  - tsconfig.app.json
  - .vitepress/theme/views/ChallengeView.vue
  - tsconfig.node.json
  - testcase-generator/src/lib.rs
  - .vitepress/theme/components/editor/CodeEditor.vue
  - requirements.txt
  - package.json
  - .vitepress/theme/composables/useChallengeRunner.ts
  - scripts/generate-pools.ts
  - .github/workflows/release.yml
  - scripts/generate-key-material.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
-->

---
### Requirement: Dev runner stop cancels in-flight submission and settles Promise

When the dev runner's `stop()` is called while the submission worker is in-flight, the runner SHALL cancel the pending `killTimer` for the submission worker, terminate the submission worker, and cause the `submit()` Promise to settle. `stop()` SHALL also continue to terminate the generator-phase `activeWorker` if it is active. After `stop()` returns, `isRunning` SHALL be `false`.

#### Scenario: Stop during dev submission settles Promise

- **WHEN** `submit()` is in progress in the dev runner and `stop()` is called
- **THEN** the submission worker's `killTimer` SHALL be cleared
- **AND** the submission worker SHALL be terminated
- **AND** `isRunning` SHALL be `false`
- **AND** the `submit()` Promise SHALL NOT remain pending indefinitely

#### Scenario: Stop during dev generator phase terminates activeWorker

- **WHEN** the dev runner is in the generator phase (`loadTestcases` in progress) and `stop()` is called
- **THEN** `activeWorker` SHALL be terminated
- **AND** `isRunning` SHALL be `false`

#### Scenario: Dev killTimer does not fire after stop

- **WHEN** `stop()` is called during an in-flight dev submission
- **THEN** the submission `killTimer` callback SHALL NOT execute after `stop()` completes

<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useChallengeRunner.ts
tests:
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
-->


<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useRemoteChallenge.ts
  - testcase-generator/src/pool.rs
  - README.md
  - .vitepress/theme/workers/pyodide.worker.ts
  - testcase-generator/src/judge.rs
  - .vitepress/plugins/strip-generator.ts
  - tsconfig.app.json
  - .vitepress/theme/views/ChallengeView.vue
  - tsconfig.node.json
  - testcase-generator/src/lib.rs
  - .vitepress/theme/components/editor/CodeEditor.vue
  - requirements.txt
  - package.json
  - .vitepress/theme/composables/useChallengeRunner.ts
  - scripts/generate-pools.ts
  - .github/workflows/release.yml
  - scripts/generate-key-material.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
-->

---
### Requirement: Cleanup cancels all pending timers and workers

The `cleanup()` function for both prod and dev runners SHALL cancel all pending `killTimer` timers, terminate all active workers, and settle any in-flight Promises. After `cleanup()` returns, no stale timer callbacks SHALL fire. This prevents side effects after component unmount.

#### Scenario: Cleanup during prod submission cancels timer

- **WHEN** `cleanup()` is called on the prod runner while a submission is in-flight
- **THEN** the `killTimer` SHALL be cleared
- **AND** the worker SHALL be terminated
- **AND** the in-flight Promise SHALL settle

#### Scenario: Cleanup during dev submission cancels timer

- **WHEN** `cleanup()` is called on the dev runner while a submission is in-flight
- **THEN** the submission `killTimer` SHALL be cleared
- **AND** both the submission worker and any active generator worker SHALL be terminated
- **AND** in-flight Promises SHALL settle

#### Scenario: No stale timer fires after cleanup

- **WHEN** `cleanup()` is called and then sufficient wall-clock time passes for any previously scheduled `killTimer` to fire
- **THEN** no callback SHALL execute from the cleared timers

<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useChallengeRunner.ts
tests:
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
-->

<!-- @trace
source: harden-prod-pool-runner
updated: 2026-04-04
code:
  - .vitepress/theme/composables/useRemoteChallenge.ts
  - testcase-generator/src/pool.rs
  - README.md
  - .vitepress/theme/workers/pyodide.worker.ts
  - testcase-generator/src/judge.rs
  - .vitepress/plugins/strip-generator.ts
  - tsconfig.app.json
  - .vitepress/theme/views/ChallengeView.vue
  - tsconfig.node.json
  - testcase-generator/src/lib.rs
  - .vitepress/theme/components/editor/CodeEditor.vue
  - requirements.txt
  - package.json
  - .vitepress/theme/composables/useChallengeRunner.ts
  - scripts/generate-pools.ts
  - .github/workflows/release.yml
  - scripts/generate-key-material.ts
tests:
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-dev.spec.ts
-->