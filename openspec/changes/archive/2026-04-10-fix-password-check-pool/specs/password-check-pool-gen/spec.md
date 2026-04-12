## ADDED Requirements

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
