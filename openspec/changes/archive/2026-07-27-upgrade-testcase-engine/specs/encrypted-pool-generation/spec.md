## MODIFIED Requirements

### Requirement: Build script generates encrypted testcase pools

A build script (`scripts/generate-pools.ts`) SHALL read all `docs/challenge/*.md` files, parse frontmatter to extract `params`, `generator`, `testcase_count`, `algorithm`, `verdict_detail`, and optional `input_budget` fields. For each challenge, it SHALL derive a `slug` from the markdown file basename (the filename with the `.md` extension removed). The build script SHALL generate a configurable number of random inputs (default: 200) by calling the WASM `generate_pool_inputs` entry with a spec object whose `seed` is the challenge slug, making pool content deterministic for identical challenge declarations. Input generation SHALL have exactly one implementation (the Rust/WASM engine); the build script SHALL NOT embed a Python reimplementation of param-based input generation. The WASM module SHALL be loaded lazily in Node via dynamic import of the web-target glue and byte-buffer initialization; module resolution SHALL NOT use a static import path, so that unit tests of the build script's pure helpers run without the WASM artifact.

The build script SHALL continue to execute the `generator` Python code via subprocess for each input to produce `expected_output`, and package all `{input, expected_output}` pairs into an encrypted binary pool file named `<slug>.bin` (NOT `<algorithm>.bin`), ensuring each challenge owns an independent pool even when multiple challenges declare the same `algorithm` value.

The build script SHALL declare its Python runtime and third-party package dependencies via a `requirements.txt` file at the project root. The `requirements.txt` file SHALL list `PyYAML` with a version constraint. No third-party cryptography library (e.g., `pycryptodome`) SHALL be required as a standard dependency.

Before processing any challenge files, the build script SHALL perform a preflight check that verifies: (1) the Python 3 runtime is available and the `yaml` package can be imported; (2) the WASM artifact and its JS glue exist at the expected output location. If any preflight check fails, the build script SHALL exit with a non-zero code and print an actionable error message (for Python: the exact installation command `pip install -r requirements.txt`; for WASM: the exact build command `pnpm build:wasm`). Any input-generation error returned by the WASM engine (parse error, budget violation) SHALL abort the build with a non-zero exit code naming the challenge; the build SHALL NOT continue with a WASM instance that has trapped.

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

#### Scenario: Deterministic pools across consecutive builds

- **WHEN** the build script runs twice with no change to any challenge file or engine source
- **THEN** every produced pool's plaintext payload SHALL be byte-identical between the two runs

#### Scenario: Preflight check fails when WASM artifact is missing

- **WHEN** the build script starts and the WASM artifact has not been built
- **THEN** the build script SHALL exit with a non-zero code and print a message that includes `pnpm build:wasm`

#### Scenario: Preflight check fails when Python is missing

- **WHEN** the build script starts and the `python3` command is not found
- **THEN** the build script SHALL exit with a non-zero code and print an error message indicating that Python 3 is required

#### Scenario: Preflight check fails when PyYAML is missing

- **WHEN** the build script starts and `PyYAML` is not installed
- **THEN** the build script SHALL exit with a non-zero code and print an error message that includes the command `pip install -r requirements.txt`

#### Scenario: Budget violation aborts the build naming the challenge

- **WHEN** any challenge's params worst-case estimate exceeds its applicable input budget
- **THEN** the build script SHALL exit non-zero with an error naming the challenge slug and the per-param byte estimates

## ADDED Requirements

### Requirement: Build pipeline orders key material before WASM before pools

The composite `dev` and `build` scripts in `package.json` SHALL execute in the order: key material generation, then `build:wasm`, then `build:pools`, then the remaining steps. This order SHALL also hold in CI workflows: the verify workflow SHALL install wasm-pack, generate key material, and build the WASM artifact before running the test suite, and the release workflow SHALL inherit the corrected order via the composite `build` script. Rationale: `build:wasm` requires the generated `testcase-generator/src/key_material.rs`, and `build:pools` requires the WASM artifact.

#### Scenario: Clean checkout build succeeds end to end

- **WHEN** `pnpm build` runs on a clean checkout with no generated artifacts present
- **THEN** key material is generated first, the WASM artifact is built second, pools are built third, and the build completes without a missing-artifact failure

#### Scenario: CI verify job provides the WASM artifact before tests

- **WHEN** the CI verify job runs the JS test suite
- **THEN** the WASM artifact has already been built in an earlier step of the same job, so WASM-dependent tests execute instead of failing for a missing artifact
