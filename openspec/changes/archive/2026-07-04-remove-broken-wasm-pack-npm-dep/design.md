## Context

WASM for this project is built by the `build:wasm` script (`wasm-pack build testcase-generator ...`). wasm-pack itself is a Rust tool. The repository obtains it two ways today: local developers install it with cargo (it lands at `~/.cargo/bin/wasm-pack`), and the release workflow installs it with `jetli/wasm-pack-action`. Neither path needs an npm package.

Despite that, `package.json` also declares an npm `wasm-pack` devDependency and `pnpm-workspace.yaml` allow-lists its build script. That npm wrapper downloads its binary from `drager/wasm-pack`, a repo with zero release assets, so its postinstall 404s on every platform, and its `node_modules/.bin/wasm-pack` shim (with an empty `binary/` dir) shadows the working PATH binary during `pnpm` script execution. This is the root cause of both the install failure the CI verify job hit and the latent breakage of `build:wasm` locally and in release CI.

## Goals / Non-Goals

**Goals:**

- Remove the npm `wasm-pack` dependency so `pnpm install --frozen-lockfile` succeeds with no binary download and no `--ignore-scripts` workaround.
- Ensure `wasm-pack` invoked by `build:wasm` resolves to the PATH binary (cargo locally, jetli in release CI), not a broken npm shim.
- Keep the CI verify workflow green and restore the release workflow's install + build behavior.
- Record wasm-pack as an explicit local prerequisite so contributors are not surprised by a missing command.

**Non-Goals:**

- Not changing the wasm-pack version or the mechanism that provides it (cargo locally, jetli in CI).
- Not modifying `testcase-generator` Rust code, the WASM output, Pyodide, or the encrypted pools.
- Not altering the body of the `build:wasm` script.

## Decisions

### Remove the npm wasm-pack dependency rather than pin or repoint it

The npm wrapper downloads from a repository (`drager/wasm-pack`) that hosts no releases, so every version 404s — pinning a different version cannot help. Overriding the download URL would couple the project to an unofficial workaround. The dependency has no positive role because wasm-pack already comes from cargo/jetli. Removing it is the only fix that also eliminates the PATH-shadowing shim.

### Revert the CI `--ignore-scripts` workaround once the root cause is gone

The verify job's install was temporarily changed to `pnpm install --frozen-lockfile --ignore-scripts` to skip the failing wasm-pack postinstall. After removing the dependency, `allowBuilds` is empty and no dependency build script runs, so the plain frozen install is safe again. Reverting keeps the workflow honest and removes an obsolete workaround; the step comment is updated to explain wasm-pack provenance.

### Document cargo as the local wasm-pack source

Because wasm-pack is no longer pulled by pnpm, a first-time contributor running `build:wasm` without a cargo-installed wasm-pack would see a "command not found". The contribution guide and README prerequisites state that wasm-pack is installed via cargo, matching the existing Rust toolchain requirement.

## Implementation Contract

**Observable behavior (after fix):**

- `pnpm install --frozen-lockfile` (no `--ignore-scripts`) completes successfully locally and in CI, with no wasm-pack postinstall and no HTTP 404.
- `pnpm exec which wasm-pack` resolves to the cargo global binary (e.g. under `~/.cargo/bin`), not `./node_modules/.bin/wasm-pack`.
- `pnpm build:wasm` runs the PATH wasm-pack and produces the WASM output under `docs/public/wasm/`.
- The CI verify workflow passes typecheck, lint, vitest, and cargo test.

**Interface / data shape:**

- `package.json` devDependencies no longer contains a `wasm-pack` entry.
- `pnpm-workspace.yaml` no longer lists `wasm-pack` under `allowBuilds`; if `allowBuilds` becomes empty, the block is removed.
- `pnpm-lock.yaml` no longer contains `wasm-pack` or its transitive-only dependencies.
- The CI verify install step is `pnpm install --frozen-lockfile` (no `--ignore-scripts`), with a comment naming cargo/jetli as the wasm-pack source.
- `CONTRIBUTE.md` and `README.md` list wasm-pack (installed via cargo) as a local build prerequisite.

**Failure modes:**

- A contributor without a cargo-installed wasm-pack who runs `build:wasm` gets a shell "command not found" for wasm-pack; the documented prerequisite tells them to install it via cargo. This is expected and is not a regression (the npm dependency never produced a working binary either).
- If the lockfile is not regenerated after editing `package.json`, `pnpm install --frozen-lockfile` fails with a lockfile-mismatch error; regenerating the lockfile in the same change prevents this.

**Acceptance criteria:**

- `pnpm install --frozen-lockfile` exits zero with no wasm-pack postinstall line in its output.
- `pnpm exec which wasm-pack` does not print a `node_modules/.bin` path.
- `pnpm typecheck`, `pnpm lint`, `pnpm test --run`, and `cargo test --manifest-path testcase-generator/Cargo.toml` all pass.
- Grep confirms no `wasm-pack` entry remains in `package.json` devDependencies, `pnpm-workspace.yaml` allowBuilds, or as a top-level package in `pnpm-lock.yaml`.

**Scope boundaries:**

- In scope: `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `.github/workflows/ci.yml`, `CONTRIBUTE.md`, `README.md`, and the two spec deltas.
- Out of scope: `.github/workflows/release.yml` (unchanged), `testcase-generator/` Rust sources, the WASM/Pyodide/pool artifacts, and the `build:wasm` script body.

## Risks / Trade-offs

- [Contributor friction] Removing the npm dependency makes wasm-pack an explicit prerequisite → mitigated by documenting `cargo install wasm-pack` in CONTRIBUTE.md and README, alongside the already-required Rust toolchain.
- [Lockfile churn] Regenerating `pnpm-lock.yaml` produces a diff → the change deliberately includes the regenerated lockfile so `--frozen-lockfile` stays valid.
- [Reverting `--ignore-scripts`] If any future dependency legitimately needs an allow-listed build script, `--ignore-scripts` would have skipped it → not a concern now (allowBuilds is empty after this change); reverting restores default behavior and any future need is handled by a targeted `allowBuilds` entry, not a blanket skip.
