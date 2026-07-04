## Problem

The project declares `wasm-pack` as an npm devDependency (`wasm-pack: ^0.14.0`) and allows its install script via `allowBuilds: wasm-pack: true` in the pnpm workspace config. This npm wrapper package's installer downloads its prebuilt binary from the `drager/wasm-pack` GitHub repository, which publishes zero release assets (the actual binaries live under `rustwasm/wasm-pack`). The postinstall therefore returns HTTP 404 on every platform.

Two verified consequences:

1. A plain `pnpm install --frozen-lockfile` fails inside the wasm-pack postinstall (the CI verify job hit this and was red until a temporary `--ignore-scripts` workaround was added). The release workflow still runs a plain install and would fail the same way once triggered.
2. Even when the install script is skipped, `node_modules/.bin/wasm-pack` remains a broken shim (its `node_modules/wasm-pack/binary/` directory is empty). Because pnpm puts `node_modules/.bin` first on PATH, running `build:wasm` resolves `wasm-pack` to this broken shim instead of the globally cargo-installed binary (local dev) or the binary the release workflow installs via `jetli/wasm-pack-action`. Observed: `pnpm exec which wasm-pack` returns `./node_modules/.bin/wasm-pack`, and `pnpm exec wasm-pack --version` prints `Error fetching release: 404`.

As a result, local `pnpm dev` / `pnpm build` / `build:wasm` and the release workflow's install + build are all broken by this dependency (release is merely latent because no tag has been pushed since the dependency was added).

## Root Cause

The npm `wasm-pack` wrapper package downloads its binary from a repository that hosts no release assets, so its postinstall always 404s; and its bin shim shadows any working wasm-pack already on PATH. The dependency provides no value to this project, which sources wasm-pack from cargo (local development) and from `jetli/wasm-pack-action` (release CI). It is purely harmful.

## Proposed Solution

Remove the harmful npm `wasm-pack` dependency and let `wasm-pack` resolve from PATH:

1. Remove `wasm-pack` from the devDependencies in `package.json`.
2. Remove the `wasm-pack` entry from `allowBuilds` in `pnpm-workspace.yaml` (drop the now-empty `allowBuilds` block if nothing else remains).
3. Regenerate `pnpm-lock.yaml` so the lockfile no longer contains wasm-pack and its transitive dependencies.
4. Revert the CI verify install step in `.github/workflows/ci.yml` from the temporary `--ignore-scripts` form back to a plain frozen install, and update the step comment to state that wasm-pack is provided by cargo (local) and by `jetli/wasm-pack-action` (release CI), never by npm.
5. Document in `CONTRIBUTE.md` (and the README environment prerequisites) that wasm-pack is a local prerequisite installed via cargo, and is no longer provided by pnpm.
6. Leave `.github/workflows/release.yml` unchanged — it already installs wasm-pack via `jetli/wasm-pack-action`; removing the shadowing npm shim restores both its install and its `build:wasm` step.

## Non-Goals

- Not changing the wasm-pack version or switching install mechanism (local cargo and CI `jetli/wasm-pack-action` stay as-is).
- Not modifying the `testcase-generator` Rust code or the emitted WASM artifacts.
- Not touching Pyodide or the encrypted testcase pools.
- Not changing the body of the `build:wasm` script itself.

## Success Criteria

- After removal, a plain frozen install (no `--ignore-scripts`) succeeds locally and in CI with no wasm-pack postinstall step.
- `pnpm exec which wasm-pack` resolves to the cargo-installed global binary, not a `node_modules` shim.
- `build:wasm` runs the PATH wasm-pack and completes a WASM build.
- The CI verify workflow stays green (typecheck, lint, vitest, cargo test).
- The release workflow's install and build steps are no longer shadowed by a broken npm shim; `build:wasm` uses the `jetli`-provided wasm-pack.

## Impact

- Affected specs:
  - release-dist-packaging (modified: full-build requirement clarifies wasm-pack provenance)
  - ci-quality-gate (modified: dependency install needs no wasm-pack binary)
- Affected code:
  - Modified:
    - package.json
    - pnpm-workspace.yaml
    - pnpm-lock.yaml
    - .github/workflows/ci.yml
    - CONTRIBUTE.md
    - README.md
  - New: (none)
  - Removed: (none)
