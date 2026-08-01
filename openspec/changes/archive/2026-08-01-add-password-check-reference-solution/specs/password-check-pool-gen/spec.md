## ADDED Requirements

### Requirement: Reference solution covers password-check in content regression

The password-check challenge MUST declare a reference_solution implementing the student-facing task: read the correct password, read the attempt limit K, then read guesses one line at a time; on the first match print OK and stop reading; if K guesses are all wrong print LOCKED. The reference_solution MUST NOT read more guess lines than provided (the factory input contains no lines after the correct guess, and exactly K lines when all guesses are wrong). The content-regression test MUST cover password-check by feeding the factory-transformed student inputs to the reference_solution and comparing its output with the factory expected_output. Declaring the reference_solution MUST NOT change the generated pool content: the engine generation request (spec and count built by buildPoolRequest) MUST be byte-identical with and without the field, so the deterministic input sequence is unchanged (encrypted pool files use a random nonce and are never byte-comparable across builds).

#### Scenario: Content regression validates the student-facing solution
- **WHEN** pnpm test --run executes the content-regression suite
- **THEN** password-check is covered (reference_solution declared) and its output matches the factory expected_output (OK or LOCKED) on sampled official pool inputs

#### Scenario: Pool generation request unchanged by the new field
- **WHEN** buildPoolRequest is computed for password-check with and without the reference_solution field
- **THEN** the serialized generation request (spec and count) is byte-identical, proving the deterministic pool input sequence is unchanged
