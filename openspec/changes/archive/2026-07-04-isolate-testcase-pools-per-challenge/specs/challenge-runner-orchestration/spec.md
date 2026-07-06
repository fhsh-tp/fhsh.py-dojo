## MODIFIED Requirements

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
