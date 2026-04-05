## MODIFIED Requirements

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

---

### Requirement: Python dependency manifest exists at project root

A `requirements.txt` file SHALL exist at the project root directory. It SHALL list all Python packages required by the pool generation build step. It SHALL contain `PyYAML` with a pinned or minimum version constraint. The file SHALL NOT include packages that are only part of the Python standard library. The file SHALL NOT list `pycryptodome` or any other third-party cryptography library as a standard dependency.

#### Scenario: requirements.txt contains PyYAML

- **WHEN** a user reads `requirements.txt`
- **THEN** it SHALL contain a line specifying `PyYAML` with a version constraint

#### Scenario: All listed packages install successfully

- **WHEN** a user runs `pip install -r requirements.txt` in a clean Python 3.10+ environment
- **THEN** all packages SHALL install without errors

## REMOVED Requirements

### Requirement: Generator with external Python dependencies executes correctly

**Reason**: Python 自學道場的標準題目生成器不使用密碼學套件（`pycryptodome`）。此 scenario 描述的是密碼學挑戰的特定需求，在新專案中不再適用。
**Migration**: 若特定題目確實需要第三方套件，題目作者應手動將該套件加入 `requirements.txt`，並在題目說明中記載此依賴。

#### Scenario: pycryptodome is not required by default

- **WHEN** the build script runs pool generation for standard Python 自學道場 challenges
- **THEN** the build script SHALL NOT require `pycryptodome` to be installed and SHALL NOT verify `Crypto.Cipher.DES` import during preflight
