## MODIFIED Requirements

### Requirement: Full project build in CI

The workflow SHALL install Rust stable toolchain and wasm-pack.
wasm-pack SHALL be provided by the workflow's toolchain install step (the `jetli/wasm-pack-action` action) and SHALL be resolvable on `PATH` when `build:wasm` runs. The project SHALL NOT declare wasm-pack as an npm dependency, because an npm wasm-pack package places a shim on `node_modules/.bin` that shadows the toolchain-provided binary during pnpm script execution and whose install script fails, breaking dependency installation.
The workflow SHALL install Python 3 using `actions/setup-python@v5` and install Python dependencies from `requirements.txt` using `pip install -r requirements.txt`.
The workflow SHALL install Node.js and pnpm (version from `packageManager` field in `package.json`).
The workflow SHALL run `pnpm install` to install dependencies.
The workflow SHALL run `pnpm build` to execute the full build pipeline (WASM + pools + VitePress).

The Python setup step SHALL be placed before `pnpm build` so that the pool generation subprocess has access to all required Python packages.

#### Scenario: Successful build

- **WHEN** the workflow executes the build step
- **THEN** the `.vitepress/dist/` directory SHALL contain the complete built site including WASM files under `wasm/` and encrypted pool files under `pools/`

#### Scenario: Build failure

- **WHEN** any build step fails
- **THEN** the workflow SHALL fail and SHALL NOT upload any assets to the release

#### Scenario: Python environment is ready before build

- **WHEN** the `pnpm build` step executes
- **THEN** `python3` SHALL be available on `PATH` with `PyYAML` and `pycryptodome` importable

#### Scenario: Pool generation succeeds in CI

- **WHEN** the build step runs `pnpm build` which triggers `build:pools`
- **THEN** the pool generation subprocess SHALL find all required Python packages and generate encrypted pool files without import errors

#### Scenario: wasm-pack comes from the toolchain, not npm

- **WHEN** the workflow installs dependencies and then runs the `build:wasm` stage of `pnpm build`
- **THEN** the wasm-pack used SHALL be the binary installed by the toolchain step on `PATH`, and dependency installation SHALL NOT attempt to download a wasm-pack binary through an npm package
