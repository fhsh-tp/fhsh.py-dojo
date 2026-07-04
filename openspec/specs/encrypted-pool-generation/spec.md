# encrypted-pool-generation Specification

## Purpose

Defines the build-time pipeline that generates encrypted testcase pool files for each challenge. The build script runs Python generators via subprocess, packages input/output pairs into AES-256-GCM encrypted binary pools, and generates obfuscated Rust key material for the WASM module to use at runtime.

## Requirements

### Requirement: Build script generates encrypted testcase pools

A build script (`scripts/generate-pools.ts`) SHALL read all `docs/challenge/*.md` files, parse frontmatter to extract `params`, `generator`, `testcase_count`, `algorithm`, and `verdict_detail` fields. For each challenge, it SHALL derive a `slug` from the markdown file basename (the filename with the `.md` extension removed). The build script SHALL generate a configurable number of random inputs (default: 200) using the existing WASM `generate_challenge()` function or equivalent param-based generation, execute the `generator` Python code via subprocess for each input to produce `expected_output`, and package all `{input, expected_output}` pairs into an encrypted binary pool file. The pool file SHALL be named `<slug>.bin` (NOT `<algorithm>.bin`), ensuring each challenge owns an independent pool even when multiple challenges declare the same `algorithm` value.

The build script SHALL declare its Python runtime and third-party package dependencies via a `requirements.txt` file at the project root. The `requirements.txt` file SHALL list `PyYAML` with a version constraint. No third-party cryptography library (e.g., `pycryptodome`) SHALL be required as a standard dependency.

Before processing any challenge files, the build script SHALL perform a preflight check that verifies the Python 3 runtime is available and the `yaml` package can be imported. If the preflight check fails, the build script SHALL exit with a non-zero code and print an actionable error message that includes the exact installation command (`pip install -r requirements.txt`).

#### Scenario: Pool file created per challenge slug

- **WHEN** the build script runs
- **THEN** one `.bin` file SHALL be created in `docs/public/pools/` for each challenge markdown file, named `<slug>.bin` where `<slug>` is the markdown filename with the `.md` extension removed

##### Example: nested-loop algorithm group produces independent pools

- **GIVEN** eight challenge files all declare `algorithm: nested-loop`: `inverted-triangle.md`, `isosceles-triangle.md`, `multiplication-table.md`, `nested-triangle.md`, `number-pyramid.md`, `pair-count.md`, `star-diamond.md`, `star-rectangle.md`
- **WHEN** the build script runs
- **THEN** `docs/public/pools/` SHALL contain all eight files: `inverted-triangle.bin`, `isosceles-triangle.bin`, `multiplication-table.bin`, `nested-triangle.bin`, `number-pyramid.bin`, `pair-count.bin`, `star-diamond.bin`, `star-rectangle.bin`
- **AND** no `nested-loop.bin` SHALL be produced

#### Scenario: Pool payload challenge_id equals slug

- **WHEN** the build script encrypts a pool for a challenge with slug `multiplication-table` and `algorithm: nested-loop`
- **THEN** the plaintext payload's `challenge_id` field SHALL equal `"multiplication-table"`
- **AND** the `challenge_id` field SHALL NOT equal `"nested-loop"`

#### Scenario: JSON factory format is supported

- **WHEN** a generator outputs a JSON string `{"input": "...", "expected_output": "..."}`
- **THEN** the build script SHALL parse the JSON and use the transformed `input` and `expected_output` values in the pool

#### Scenario: Build script fails on generator error

- **WHEN** a generator script raises a Python exception for any input
- **THEN** the build script SHALL report the error with challenge name and input details, and exit with a non-zero code

#### Scenario: Preflight check passes with Python and PyYAML installed

- **WHEN** the build script starts and Python 3 is available with `PyYAML` installed
- **THEN** the preflight check SHALL pass silently and pool generation SHALL proceed

#### Scenario: Preflight check fails when Python is missing

- **WHEN** the build script starts and the `python3` command is not found
- **THEN** the build script SHALL exit with a non-zero code and print an error message indicating that Python 3 is required

#### Scenario: Preflight check fails when PyYAML is missing

- **WHEN** the build script starts and `PyYAML` is not installed
- **THEN** the build script SHALL exit with a non-zero code and print an error message that includes the command `pip install -r requirements.txt`


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
### Requirement: Python dependency manifest exists at project root

A `requirements.txt` file SHALL exist at the project root directory. It SHALL list all Python packages required by the pool generation build step. It SHALL contain `PyYAML` with a pinned or minimum version constraint. The file SHALL NOT include packages that are only part of the Python standard library. The file SHALL NOT list `pycryptodome` or any other third-party cryptography library as a standard dependency.

#### Scenario: requirements.txt contains PyYAML

- **WHEN** a user reads `requirements.txt`
- **THEN** it SHALL contain a line specifying `PyYAML` with a version constraint

#### Scenario: All listed packages install successfully

- **WHEN** a user runs `pip install -r requirements.txt` in a clean Python 3.10+ environment
- **THEN** all packages SHALL install without errors


<!-- @trace
source: rebrand-fhsh-py-dojo
updated: 2026-04-05
code:
  - docs/challenge/caesar-advanced.md
  - LICENSE
  - docs/challenge/rsa-basic.md
  - docs/challenge/rail-fence-encrypt.md
  - Usage.md
  - docs/challenge/caesar-custom-table.md
  - .vitepress/config.mts
  - docs/index.md
  - CHANGELOG.md
  - .vitepress/theme/composables/index.ts
  - docs/challenge/enigma-simplified.md
  - docs/challenge/caesar-basic.md
  - README.md
  - docs/challenge/vigenere-encrypt.md
  - requirements.txt
  - package.json
  - docs/challenge/des-ecb-cbc.md
-->

---
### Requirement: Pool binary format uses AES-256-GCM encryption

Each pool file SHALL use the following binary format:
- Bytes 0-5: magic `CXPOOL` (ASCII)
- Byte 6: version number (initially `1`)
- Bytes 7-18: 12-byte random nonce
- Bytes 19+: AES-256-GCM ciphertext with appended 16-byte authentication tag

The plaintext payload SHALL be a JSON object containing `challenge_id` (string), `verdict_detail` (string: `hidden` | `actual` | `full`), and `testcases` (array of `{input: string, expected_output: string}`).

#### Scenario: Pool file starts with correct magic and version

- **WHEN** a pool file is read
- **THEN** the first 6 bytes SHALL equal ASCII `CXPOOL` and byte 7 SHALL equal `0x01`

#### Scenario: Tampered pool file is rejected

- **WHEN** any byte of the ciphertext or nonce is modified
- **THEN** AES-GCM decryption SHALL fail with an authentication error

#### Scenario: verdict_detail is integrity-protected

- **WHEN** an attacker attempts to change the verdict_detail value
- **THEN** the modification SHALL be inside the encrypted payload and any tampering SHALL cause decryption to fail


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
### Requirement: Encryption key is managed as a project secret

The AES-256-GCM encryption key SHALL be stored in a `.env.pool` file (gitignored) as a 64-character hex string. The build script SHALL read the key from this file. If the file does not exist, the build script SHALL generate a random 256-bit key, write it to `.env.pool`, and proceed.

#### Scenario: First build generates key automatically

- **WHEN** `build:pools` runs and `.env.pool` does not exist
- **THEN** a new random 256-bit key SHALL be generated and saved to `.env.pool`

#### Scenario: Subsequent builds reuse existing key

- **WHEN** `build:pools` runs and `.env.pool` exists with a valid key
- **THEN** the existing key SHALL be used for encryption


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
### Requirement: Build script generates obfuscated key material for WASM

After encrypting all pools, the build script SHALL generate `testcase-generator/src/key_material.rs` containing the encryption key split into 4 segments of 8 bytes each, each XORed with a randomly generated compile-time mask. The file SHALL be gitignored. The generated Rust code SHALL provide a function to reconstruct the original key at runtime.

#### Scenario: key_material.rs is generated with obfuscated constants

- **WHEN** the build script completes pool generation
- **THEN** `testcase-generator/src/key_material.rs` SHALL exist containing 4 pairs of `const` arrays (segment + mask) and a reconstruction function

#### Scenario: key_material.rs is not committed to version control

- **WHEN** checking `.gitignore`
- **THEN** the pattern `key_material.rs` SHALL be listed

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
### Requirement: Build script validates slug uniqueness and shape

The build script SHALL enforce that every challenge slug is unique across the entire `docs/challenge/` directory and conforms to a safe filename pattern (`^[a-z0-9-]+$`, length 1–64). If two challenge files would produce the same slug, or any slug is empty, contains path separators (`/`, `\`), parent-directory tokens (`..`), or characters outside the allowed set, the build script SHALL exit with a non-zero code and print an error message that identifies the offending file paths. The script SHALL NOT silently fall back to algorithm-based naming.

#### Scenario: Duplicate slug detected

- **WHEN** the build script encounters two challenge files that yield the same slug
- **THEN** the script SHALL exit with a non-zero code
- **AND** the error message SHALL include both conflicting file paths

#### Scenario: Slug containing path separator rejected

- **WHEN** a challenge file produces a slug containing `/`, `\`, or `..`
- **THEN** the script SHALL exit with a non-zero code without writing any pool file derived from that slug

#### Scenario: Slug outside allowed character set rejected

- **WHEN** a challenge file produces a slug that does not match `^[a-z0-9-]+$`
- **THEN** the script SHALL exit with a non-zero code

##### Example: slug validation matrix

| Slug input                | Result  | Notes                                  |
| ------------------------- | ------- | -------------------------------------- |
| `multiplication-table`    | accept  | normal case                            |
| `9-9`                     | accept  | digits and hyphens permitted           |
| ``                        | reject  | empty slug                             |
| `Multiplication-Table`    | reject  | uppercase not allowed                  |
| `../escape`               | reject  | parent-directory traversal             |
| `nested/loop`             | reject  | path separator                         |
| 65 lowercase characters    | reject  | exceeds length limit                   |


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
### Requirement: Build script cleans up obsolete pool files

After successfully writing per-slug pool files, the build script SHALL scan `docs/public/pools/` for `*.bin` entries whose basename (without `.bin`) is NOT in the set of slugs processed during the current build run, and SHALL delete those obsolete files. Non-`.bin` files (such as `.gitkeep`) and subdirectories SHALL NOT be deleted. The cleanup step SHALL run ONLY when every challenge in the current build run produced a pool successfully (i.e. `success > 0` AND `failed === 0`); a partial failure SHALL leave all existing `.bin` files in place, because the failed challenges' previous pools are the user's only fallback until the failure is fixed.

#### Scenario: Stale algorithm-named pool removed

- **GIVEN** `docs/public/pools/nested-loop.bin` exists from a prior build
- **AND** the current build produces `multiplication-table.bin`, `star-rectangle.bin`, and other per-slug pools
- **WHEN** the build script completes successfully with zero failures
- **THEN** `docs/public/pools/nested-loop.bin` SHALL be deleted
- **AND** every per-slug pool SHALL remain

#### Scenario: Non-bin files preserved

- **GIVEN** `docs/public/pools/.gitkeep` exists
- **WHEN** the cleanup step runs
- **THEN** `.gitkeep` SHALL remain

#### Scenario: Cleanup skipped after total build failure

- **WHEN** the build run produces zero successful pools
- **THEN** the cleanup step SHALL NOT run
- **AND** previously generated pool files SHALL remain on disk

#### Scenario: Cleanup skipped after partial build failure

- **GIVEN** the current build run produces 3 successful pools and 2 failures
- **WHEN** the script reaches the cleanup phase
- **THEN** the cleanup step SHALL NOT run
- **AND** all existing `.bin` files (including those for the 2 failed challenges) SHALL remain on disk
- **AND** the script SHALL log a warning that cleanup was skipped due to partial failure

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