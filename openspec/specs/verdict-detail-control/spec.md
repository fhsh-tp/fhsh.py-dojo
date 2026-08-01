# verdict-detail-control Specification

## Purpose

Defines how the `verdict_detail` frontmatter field controls the visibility of expected and actual output in test results. In production mode, the verdict detail setting is read from the integrity-protected encrypted pool payload rather than client-side frontmatter, and verdict computation with data stripping is performed by the WASM judge. In development mode, the Pyodide Worker handles stripping based on the frontmatter value.

## Requirements

<!-- @trace
source: judge-expect-hidden
updated: 2026-03-24
code:
  - .vitepress/theme/workers/pyodide.worker.ts
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/composables/useExecutor.ts
  - .vitepress/theme/stores/challenge.ts
  - .vitepress/theme/workers/worker-utils.ts
tests:
  - .vitepress/theme/__tests__/worker-utils.spec.ts
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/pyodide-worker-verdict-detail.spec.ts
-->


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

### Requirement: Verdict Detail Frontmatter Field

Each challenge Markdown file SHALL support an optional `verdict_detail` frontmatter field with values `hidden`, `actual`, or `full`. When omitted, the default value SHALL be `hidden`.

In production mode, the `verdict_detail` value SHALL be read from the encrypted pool payload (where it is integrity-protected by AES-GCM) rather than from client-side frontmatter. The `useProdRunner` composable SHALL obtain this value from the `select_testcases` WASM export return value and expose it as a reactive `verdictDetail` property. `ChallengeView` SHALL pass this pool-derived `verdictDetail` to `TestResultPanel`, NOT the frontmatter-resolved value.

In development mode, the `verdict_detail` value SHALL continue to be resolved from frontmatter via `resolveVerdictDetail()`.

#### Scenario: Field omitted defaults to hidden

- **WHEN** a challenge page has no `verdict_detail` in frontmatter
- **THEN** the system SHALL behave as `verdict_detail: hidden`

#### Scenario: Field set to full

- **WHEN** a challenge page has `verdict_detail: full`
- **THEN** the system SHALL display both expected and actual output on WA verdicts

#### Scenario: Production reads verdict_detail from encrypted pool

- **WHEN** the application runs in production mode
- **THEN** the `verdict_detail` value used for stripping SHALL come from the decrypted pool payload, not from client-side frontmatter

#### Scenario: Production verdictDetail propagates from pool to UI

- **WHEN** the application runs in production mode
- **AND** the pool was generated with `verdict_detail: "actual"`
- **THEN** `useProdRunner` SHALL expose `verdictDetail` as `"actual"` (from `select_testcases` return)
- **AND** `ChallengeView` SHALL pass `"actual"` to `TestResultPanel`'s `verdict-detail` prop
- **AND** the frontmatter value SHALL NOT influence the `TestResultPanel` display

#### Scenario: Frontmatter and pool disagree in production

- **WHEN** the application runs in production mode
- **AND** frontmatter specifies `verdict_detail: full` but the pool was generated with `verdict_detail: hidden`
- **THEN** the system SHALL use the pool's `hidden` value for both WASM judge stripping and UI display
- **AND** the frontmatter value SHALL be ignored

---
### Requirement: Worker Testcase Result Data Stripping

In development mode, the `RunRequest` message SHALL include a `verdictDetail` field (`hidden` | `actual` | `full`). The Worker SHALL compute verdicts and strip result fields based on `verdictDetail`, preserving current behavior.

In production mode, the Pyodide Worker SHALL NOT perform verdict computation or data stripping. It SHALL return raw execution outputs only. Verdict computation and data stripping SHALL be performed by the WASM `judge()` function, which reads the `verdict_detail` value from the encrypted pool payload. The WASM judge SHALL apply the same stripping rules:

When `verdict_detail` is `hidden`, the verdict result SHALL NOT include `expected` or `actual` fields.

When `verdict_detail` is `actual`, the verdict result SHALL include `actual` but SHALL NOT include `expected`.

When `verdict_detail` is `full`, the verdict result SHALL include both `expected` and `actual` fields.

The `verdict` field (AC/WA/TLE/RE) SHALL always be included regardless of mode or `verdict_detail` setting.

#### Scenario: Hidden mode strips both fields (production, WASM judge)

- **WHEN** the WASM judge processes results for a pool with `verdict_detail: "hidden"`
- **AND** a testcase produces a WA verdict
- **THEN** the verdict object SHALL contain `verdict: "WA"` and `elapsed_ms` but SHALL NOT contain `expected` or `actual`

#### Scenario: Full mode includes both fields (production, WASM judge)

- **WHEN** the WASM judge processes results for a pool with `verdict_detail: "full"`
- **AND** a testcase produces a WA verdict
- **THEN** the verdict object SHALL contain `verdict`, `expected`, `actual`, and `elapsed_ms`

#### Scenario: Dev mode Worker stripping unchanged

- **WHEN** the Worker receives a RunRequest with `verdictDetail: 'hidden'` in development mode
- **AND** a testcase produces a WA verdict
- **THEN** the `TestcaseResult` message SHALL contain `verdict: 'WA'` and `elapsed_ms` but SHALL NOT contain `expected` or `actual`

---
### Requirement: Challenge Store Data Stripping

In production mode, the `challengeStore` SHALL NOT store `expected_output` in the testcases array under any `verdict_detail` setting. Only `input` values SHALL be stored. Expected output data is managed exclusively within WASM linear memory.

In development mode, the existing behavior SHALL be preserved: when `verdict_detail` is `full`, the store SHALL contain both `input` and `expected_output`; otherwise, only `input`.

No component-local variable in `ChallengeView` SHALL hold `expected_output` in either mode. In dev mode, `expected_output` is held within the `useChallengeRunner` composable's internal state.

#### Scenario: Store never contains expected_output in production

- **WHEN** the application runs in production mode with any `verdict_detail` setting
- **THEN** `challengeStore.currentChallenge.testcases` SHALL contain objects with `input` only and no `expected_output` property

#### Scenario: Store contains full testcases when full in dev mode

- **WHEN** the application runs in development mode with `verdict_detail: "full"`
- **THEN** `challengeStore.currentChallenge.testcases` SHALL contain objects with both `input` and `expected_output`

---
### Requirement: Test Result Panel Verdict Detail Display

The `TestResultPanel` component SHALL accept a `verdictDetail` prop with type `'hidden' | 'actual' | 'full'` defaulting to `'hidden'`.

When `verdictDetail` is `hidden`, the WA detail column SHALL display no additional information beyond the verdict badge.

When `verdictDetail` is `actual`, the WA detail column SHALL display the user's actual output only.

When `verdictDetail` is `full`, the WA detail column SHALL display both expected and actual output, preserving current behavior.

The component SHALL render verdict data identically regardless of whether the data originated from the Pyodide Worker (dev mode) or the WASM judge (production mode).

#### Scenario: Hidden mode shows no detail for WA

- **WHEN** `verdictDetail` is `hidden` and a testcase has verdict WA
- **THEN** the detail column SHALL be empty

#### Scenario: Actual mode shows only user output for WA

- **WHEN** `verdictDetail` is `actual` and a testcase has verdict WA with actual output `HELLO`
- **THEN** the detail column SHALL display `實際 HELLO` without showing expected output

#### Scenario: Full mode shows both for WA

- **WHEN** `verdictDetail` is `full` and a testcase has verdict WA
- **THEN** the detail column SHALL display both expected and actual output

---
### Requirement: Build-time verdict_detail whitelist

`readChallenge` SHALL validate that `verdict_detail`, when declared, is one of `hidden`, `actual`, or `full`, and SHALL throw an error naming the file and the allowed values otherwise. An absent field SHALL keep defaulting to `hidden`.

#### Scenario: typo fails the build

- **WHEN** a challenge declares `verdict_detail: ful`
- **THEN** the pool build fails with an error naming the file and listing the allowed values

#### Scenario: absent field defaults

- **WHEN** a challenge declares no `verdict_detail`
- **THEN** the pool is built with `hidden`
