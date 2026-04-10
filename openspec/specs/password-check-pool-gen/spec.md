# password-check-pool-gen Specification

## Purpose

TBD - created by archiving change 'fix-password-check-pool'. Update Purpose after archive.

## Requirements

### Requirement: password-check challenge generates valid test pools

The `docs/challenge/password-check.md` challenge SHALL produce a valid encrypted pool file during `generate-pools` execution. The generator SHALL use the JSON factory format to self-produce complete input/output pairs, including dynamically generated guess lines beyond the declared params.

#### Scenario: Pool generation succeeds without errors

- **WHEN** `scripts/generate-pools.ts` processes `password-check.md`
- **THEN** the script SHALL generate the configured number of testcases without `EOFError` or other runtime exceptions
- **AND** the output file `docs/public/pools/password_check.bin` SHALL be created

#### Scenario: Generated testcases cover both outcomes

- **WHEN** the pool is generated with sufficient testcase count
- **THEN** the generated testcases SHALL include cases where the correct password is guessed (output: `OK`) and cases where all attempts fail (output: `LOCKED`)

#### Scenario: Password param uses valid generator type

- **WHEN** the `password` param in frontmatter is inspected
- **THEN** the param type SHALL be a type recognized by `generateInputs()` (such as `printable_ascii`) and SHALL NOT be the unsupported `str` type

<!-- @trace
source: fix-password-check-pool
updated: 2026-04-10
code:
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js.map
  - docs/.vitepress/cache/deps/package.json
  - docs/tutor/py/ch1/1-4.md
  - docs/.vitepress/cache/deps/_metadata.json
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js.map
  - docs/challenge/quadratic-discriminant.md
  - .vitepress/config.mts
  - docs/tutor/py/ch1/1-3.md
  - docs/.vitepress/cache/deps/vue.js
  - docs/.vitepress/cache/deps/vue.js.map
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js.map
  - docs/.vitepress/cache/deps/chunk-5KHNRSJ4.js
  - docs/challenge/password-check.md
  - docs/.vitepress/cache/deps/vitepress___@vueuse_core.js
  - docs/.vitepress/cache/deps/vitepress___@vue_devtools-api.js
  - package.json
-->