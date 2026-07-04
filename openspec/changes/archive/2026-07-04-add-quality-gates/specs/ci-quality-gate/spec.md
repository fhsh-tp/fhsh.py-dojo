## ADDED Requirements

### Requirement: Continuous integration verifies pushes and pull requests

A GitHub Actions workflow SHALL run on every push and pull_request targeting the `staging` and `main` branches. The workflow SHALL execute, in a single job, TypeScript type checking, ESLint and Prettier checks, the Vitest test suite, and the Rust `cargo test` suite for the `testcase-generator` crate. If any step exits non-zero, the workflow SHALL fail and report a non-zero status.

#### Scenario: Passing change reports success

- **WHEN** a pull request targets `staging` and all of typecheck, lint, vitest, and cargo test succeed
- **THEN** the CI workflow SHALL report a successful status

#### Scenario: Failing test blocks the change

- **WHEN** a pushed commit causes any Vitest or cargo test to fail
- **THEN** the CI workflow SHALL exit non-zero and report a failed status

#### Scenario: CI verifies without building site artifacts

- **WHEN** the CI workflow runs
- **THEN** it SHALL NOT execute `build:wasm`, `build:pyodide`, or `build:pools`, because the verification steps do not require those artifacts

### Requirement: Lint is runnable locally and in CI

The project SHALL provide a `lint` script in `package.json` that runs ESLint over `.vitepress/` and `scripts/` TypeScript and Vue sources and runs `prettier --check`. The Rust lint SHALL run `cargo clippy` treating warnings as errors. A developer SHALL be able to reproduce the CI lint result locally by running the `lint` script.

#### Scenario: Local lint reproduces CI

- **WHEN** a developer runs the `lint` script locally
- **THEN** it SHALL execute the same ESLint and Prettier checks that CI runs
