# password-check-pool-gen Specification

## Purpose

Contract for the password-check challenge's JSON-factory pool generation: the generator self-produces complete input/output pairs (including guess lines beyond declared params), pools build without runtime errors covering both OK and LOCKED outcomes, and a student-facing reference_solution keeps the challenge covered by the content-regression suite.

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

---
### Requirement: Reference solution covers password-check in content regression

The password-check challenge MUST declare a reference_solution implementing the student-facing task: read the correct password, read the attempt limit K, then read guesses one line at a time; on the first match print OK and stop reading; if K guesses are all wrong print LOCKED. The reference_solution MUST NOT read more guess lines than provided (the factory input contains no lines after the correct guess, and exactly K lines when all guesses are wrong). The content-regression test MUST cover password-check by feeding the factory-transformed student inputs to the reference_solution and comparing its output with the factory expected_output. Declaring the reference_solution MUST NOT change the generated pool content: the engine generation request (spec and count built by buildPoolRequest) MUST be byte-identical with and without the field, so the deterministic input sequence is unchanged (encrypted pool files use a random nonce and are never byte-comparable across builds).

#### Scenario: Content regression validates the student-facing solution
- **WHEN** pnpm test --run executes the content-regression suite
- **THEN** password-check is covered (reference_solution declared) and its output matches the factory expected_output (OK or LOCKED) on sampled official pool inputs

#### Scenario: Pool generation request unchanged by the new field
- **WHEN** buildPoolRequest is computed for password-check with and without the reference_solution field
- **THEN** the serialized generation request (spec and count) is byte-identical, proving the deterministic pool input sequence is unchanged

<!-- @trace
source: add-password-check-reference-solution
updated: 2026-08-01
code:
  - docs/challenge/password-check.md
-->