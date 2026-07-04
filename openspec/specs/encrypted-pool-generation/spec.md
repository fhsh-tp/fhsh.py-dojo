# encrypted-pool-generation Specification

## Purpose

Defines the build-time pipeline that generates encrypted testcase pool files for each challenge. The build script runs Python generators via subprocess, packages input/output pairs into AES-256-GCM encrypted binary pools, and generates obfuscated Rust key material for the WASM module to use at runtime.

## Requirements

### Requirement: Build script generates encrypted testcase pools

A build script (`scripts/generate-pools.ts`) SHALL read all `docs/challenge/*.md` files, parse frontmatter to extract `params`, `generator`, `testcase_count`, `algorithm`, and `verdict_detail` fields. For each challenge, it SHALL generate a configurable number of random inputs (default: 200) using the existing WASM `generate_challenge()` function or equivalent param-based generation, execute the `generator` Python code via subprocess for each input to produce `expected_output`, and package all `{input, expected_output}` pairs into an encrypted binary pool file.

The build script SHALL declare its Python runtime and third-party package dependencies via a `requirements.txt` file at the project root. The `requirements.txt` file SHALL list `PyYAML` with a version constraint. No third-party cryptography library (e.g., `pycryptodome`) SHALL be required as a standard dependency.

Before processing any challenge files, the build script SHALL perform a preflight check that verifies the Python 3 runtime is available and the `yaml` package can be imported. If the preflight check fails, the build script SHALL exit with a non-zero code and print an actionable error message that includes the exact installation command (`pip install -r requirements.txt`).

#### Scenario: Pool file created for each challenge

- **WHEN** the build script runs
- **THEN** one `.bin` file SHALL be created in `docs/public/pools/` for each challenge, named `<algorithm>.bin`

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