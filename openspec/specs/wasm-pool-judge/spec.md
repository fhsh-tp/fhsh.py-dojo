# wasm-pool-judge Specification

## Purpose

Defines the WASM module's pool decryption, testcase selection, and judging capabilities. The module decrypts AES-256-GCM encrypted pool files, selects random testcases with session tracking, judges student outputs internally using constant-time comparison, and manages obfuscated key material to prevent answer extraction from client-side code.

## Requirements

### Requirement: WASM module decrypts and loads encrypted pool

The WASM module SHALL export a `load_pool(challenge_id: &str, encrypted_data: &[u8])` function that validates the pool binary format (magic bytes, version), extracts the nonce, reconstructs the AES-256-GCM key from obfuscated key material, and decrypts the payload. On successful decryption, the function SHALL verify that the `challenge_id` field embedded in the decrypted payload matches the `challenge_id` argument provided by the caller. If the identities do not match, `load_pool` SHALL return an error indicating the mismatch and SHALL NOT store the pool. On failure (format, decryption, or identity mismatch), the function SHALL return a descriptive error. On success, the pool data SHALL be stored in WASM linear memory indexed by `challenge_id`.

The `challenge_id` argument and the embedded payload `challenge_id` SHALL be a per-challenge unique identifier (the challenge slug, equal to the markdown file basename without `.md`). Callers SHALL NOT pass a category-level identifier such as the frontmatter `algorithm` field when multiple challenges share that value, because doing so allows different challenges to load each other's pools and silently produces incorrect verdicts. The WASM module itself remains agnostic to the meaning of the string; this requirement is a contract on callers and on the build script that produces the encrypted payload.

#### Scenario: Valid pool loads successfully

- **WHEN** `load_pool` is called with a correctly encrypted pool file whose embedded `challenge_id` matches the caller-provided `challenge_id`
- **THEN** the function SHALL return success and the pool SHALL be available for subsequent operations

#### Scenario: Invalid magic bytes rejected

- **WHEN** `load_pool` is called with data that does not start with `CXPOOL`
- **THEN** the function SHALL return an error indicating invalid format

#### Scenario: Tampered data rejected by GCM authentication

- **WHEN** `load_pool` is called with modified ciphertext
- **THEN** AES-GCM decryption SHALL fail and the function SHALL return an authentication error

#### Scenario: Mismatched challenge_id rejected

- **WHEN** `load_pool` is called with `challenge_id` argument `"multiplication-table"` but the decrypted payload contains `challenge_id: "star-rectangle"`
- **THEN** the function SHALL return an error indicating the identity mismatch between the expected and embedded challenge_id
- **AND** the pool SHALL NOT be stored or available for subsequent operations

#### Scenario: Payload challenge_id field is not dead code

- **WHEN** the `PoolPayload` struct is compiled
- **THEN** the `challenge_id` field SHALL NOT carry an `#[allow(dead_code)]` attribute
- **AND** it SHALL be actively read and compared during `load_pool`

#### Scenario: Category-level identifier rejected for cross-challenge pool

- **GIVEN** a pool encrypted with payload `challenge_id: "multiplication-table"`
- **WHEN** a caller invokes `load_pool("nested-loop", data)` using the frontmatter algorithm value instead of the challenge slug
- **THEN** the function SHALL return an identity mismatch error
- **AND** the pool SHALL NOT be stored


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
### Requirement: WASM module selects random testcases with session tracking

The WASM module SHALL export a `select_testcases(challenge_id: &str, count: usize)` function that randomly selects `count` testcases from the loaded pool. It SHALL return a JSON object `{inputs: string[], session_id: string, verdict_detail: string}` where `inputs` contains only the input strings (NOT expected outputs), `session_id` is a unique identifier for this selection, and `verdict_detail` is the pool's verdict detail setting (`"hidden"`, `"actual"`, or `"full"`). The session data (selected indices and expected outputs) SHALL be retained in WASM memory for subsequent judging.

The `verdict_detail` field in the return value SHALL reflect the value embedded in the encrypted pool payload at generation time. This value is integrity-protected by AES-GCM and SHALL be the authoritative source of truth for production mode display behavior.

#### Scenario: Correct number of inputs returned

- **WHEN** `select_testcases("caesar_encrypt", 10)` is called on a pool with 200 entries
- **THEN** the result SHALL contain exactly 10 input strings and a non-empty session_id

#### Scenario: Expected outputs not exposed in return value

- **WHEN** `select_testcases` returns its result
- **THEN** the returned JSON SHALL NOT contain any `expected_output` field

#### Scenario: Pool not loaded returns error

- **WHEN** `select_testcases` is called for a challenge_id that has not been loaded
- **THEN** the function SHALL return an error

#### Scenario: Return value includes verdict_detail from pool

- **WHEN** `select_testcases` is called on a pool that was generated with `verdict_detail: "actual"`
- **THEN** the returned JSON SHALL include `verdict_detail: "actual"`
- **AND** this value SHALL match the `verdict_detail` embedded in the encrypted pool payload

#### Scenario: Default verdict_detail is hidden

- **WHEN** `select_testcases` is called on a pool that was generated without an explicit `verdict_detail`
- **THEN** the returned JSON SHALL include `verdict_detail: "hidden"`


<!-- @trace
source: prod-runner-convergence
updated: 2026-04-04
code:
  - .vitepress/theme/workers/pyodide.worker.ts
  - .vitepress/theme/composables/useChallengeRunner.ts
  - testcase-generator/src/pool.rs
  - .vitepress/theme/views/ChallengeView.vue
  - testcase-generator/src/lib.rs
  - testcase-generator/src/judge.rs
tests:
  - .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts
  - .vitepress/theme/__tests__/ChallengeView-verdict-detail.spec.ts
  - .vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts
-->

---
### Requirement: WASM module judges student outputs internally

The WASM module SHALL export a `judge(challenge_id: &str, session_id: &str, results: JsValue)` function. The `results` parameter SHALL be an array of `{stdout: string, error?: string, elapsed_ms: number, timed_out?: boolean}` objects, one per testcase in session order; a missing, `undefined`, or `null` `timed_out` SHALL all be treated as not timed out (the field deserializes as an optional boolean precisely because serde-wasm-bindgen does not treat an explicit `undefined`-valued key as absent), so pre-existing callers keep their exact behavior. The function SHALL compare each `stdout` (trimmed trailing whitespace) against the corresponding `expected_output` from the session and return an array of verdict objects.

Verdict determination SHALL follow this precedence: `timed_out: true` → `TLE`; otherwise a non-empty `error` → `RE`; otherwise constant-time output comparison → `AC` or `WA`. The judge SHALL NOT inspect error message text to classify timeouts — the structured `timed_out` field is the only timeout signal.

Each verdict object SHALL contain:
- `verdict`: `AC` | `WA` | `TLE` | `RE`
- `actual`: included only when `verdict_detail` is `actual` or `full`
- `expected`: included only when `verdict_detail` is `full`
- `elapsed_ms`: passed through from input
- `error`: included only for `RE` verdicts; a `TLE` verdict SHALL carry no error message even when the input result contains one (the timeout message embeds the op limit and must not leak)

The string comparison SHALL use constant-time comparison to prevent timing-based answer extraction. After judging, the session data SHALL be zeroized and the session SHALL be invalidated.

#### Scenario: All correct answers produce AC verdicts

- **WHEN** all student outputs match expected outputs (after trimming trailing whitespace)
- **THEN** all verdict objects SHALL have `verdict: "AC"`

#### Scenario: Wrong answer produces WA with verdict_detail=hidden

- **WHEN** a student output does not match and `verdict_detail` is `hidden`
- **THEN** the verdict object SHALL contain `verdict: "WA"` and `elapsed_ms` only, with no `actual` or `expected` field

#### Scenario: Wrong answer produces WA with verdict_detail=full

- **WHEN** a student output does not match and `verdict_detail` is `full`
- **THEN** the verdict object SHALL contain `verdict: "WA"`, `actual`, `expected`, and `elapsed_ms`

#### Scenario: Runtime error produces RE verdict

- **WHEN** a result has a non-empty `error` field and `timed_out` is absent or false
- **THEN** the verdict SHALL be `RE` and the verdict object SHALL carry the error message

#### Scenario: Timed-out result produces TLE verdict

- **WHEN** a result has `timed_out: true`
- **THEN** the verdict SHALL be `TLE` and the verdict object SHALL contain no `error` field, even if the input result also carried an `error` message

#### Scenario: Results without timed_out keep legacy behavior

- **WHEN** the results array objects contain no `timed_out` field at all
- **THEN** every verdict SHALL be identical to the pre-TLE behavior (AC/WA/RE only)

#### Scenario: Explicit undefined timed_out keys do not poison the batch

- **WHEN** result objects carry an explicit `timed_out` key whose value is `undefined` (a shape plain JS object literals naturally produce)
- **THEN** deserialization SHALL succeed and those results SHALL judge as not timed out

#### Scenario: Session invalidated after judging

- **WHEN** `judge` is called with a valid session_id
- **AND** then called again with the same session_id
- **THEN** the second call SHALL return an error indicating the session is invalid

---
### Requirement: WASM module conditionally exposes expected output

The WASM module SHALL export a `get_expected(challenge_id: &str, session_id: &str, index: usize)` function. When the pool's `verdict_detail` is `full`, it SHALL return the expected output string for the given testcase index. When `verdict_detail` is `hidden` or `actual`, it SHALL return `None` (null in JS).

#### Scenario: get_expected returns value when verdict_detail is full

- **WHEN** the pool was encrypted with `verdict_detail: "full"` and `get_expected` is called
- **THEN** the function SHALL return the expected output string

#### Scenario: get_expected returns null when verdict_detail is hidden

- **WHEN** the pool was encrypted with `verdict_detail: "hidden"` and `get_expected` is called
- **THEN** the function SHALL return null


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
### Requirement: WASM key material uses obfuscated XOR split storage

The encryption key SHALL be stored in the WASM binary as 4 pairs of 8-byte constant arrays. Each pair consists of a key segment XORed with a random mask and the mask itself. The key reconstruction function SHALL XOR each segment with its mask and concatenate the results to form the 32-byte key. After use, the reconstructed key SHALL be zeroized using the `zeroize` crate.

#### Scenario: Key reconstruction produces correct key

- **WHEN** the WASM module reconstructs the key from obfuscated segments
- **THEN** the result SHALL equal the original encryption key used during pool generation

#### Scenario: Key is zeroized after decryption

- **WHEN** pool decryption completes
- **THEN** the reconstructed key in memory SHALL be overwritten with zeros

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
### Requirement: Block selection for plan pools

When a loaded pool's payload declares `plan_block_size = k`, `select_testcases` SHALL validate that `k > 0`, that the pool's testcase count is a positive multiple of `k`, and that the requested `count` equals `k` exactly — failing with a descriptive error otherwise. It SHALL then select one block uniformly at random and return that block's testcases in their stored order without shuffling. Pools without `plan_block_size` SHALL keep the existing shuffle-and-truncate selection unchanged.

#### Scenario: plan pool returns an ordered block

- **WHEN** a pool has 200 testcases with `plan_block_size: 5` and `select_testcases(id, 5)` is called
- **THEN** the returned 5 inputs are one of the 40 stored blocks, in stored order

#### Scenario: count mismatch on plan pool is refused

- **WHEN** the pool declares `plan_block_size: 5` and the caller requests 10
- **THEN** selection fails with an error stating the required count is 5

#### Scenario: corrupt block structure is refused

- **WHEN** the pool declares `plan_block_size: 6` but holds 200 testcases (not a multiple of 6)
- **THEN** selection fails with a descriptive error instead of returning a partial block

#### Scenario: non-plan pools behave as before

- **WHEN** a pool without `plan_block_size` is loaded
- **THEN** `select_testcases` performs the existing uniform shuffle-and-truncate selection
