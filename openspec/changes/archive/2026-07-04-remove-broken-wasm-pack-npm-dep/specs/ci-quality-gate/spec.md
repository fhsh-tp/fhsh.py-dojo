## ADDED Requirements

### Requirement: CI dependency install needs no wasm-pack binary

The CI verify workflow SHALL install dependencies with `pnpm install --frozen-lockfile` and this step SHALL succeed without downloading or building a wasm-pack binary. Because verification does not build WASM and wasm-pack is not an npm dependency, the install step SHALL NOT require `--ignore-scripts` to complete. The install-step comment SHALL state that wasm-pack is provided by cargo for local development and by `jetli/wasm-pack-action` for the release workflow, not by npm.

#### Scenario: Install succeeds without a wasm-pack download

- **WHEN** the CI verify job runs its dependency install step
- **THEN** `pnpm install --frozen-lockfile` SHALL complete successfully without executing any wasm-pack install script and without downloading a wasm-pack binary

#### Scenario: No ignore-scripts workaround is needed

- **WHEN** the CI verify job installs dependencies after the npm wasm-pack dependency has been removed
- **THEN** the install SHALL NOT pass `--ignore-scripts`, and the workflow SHALL still reach the typecheck, lint, vitest, and cargo test steps
