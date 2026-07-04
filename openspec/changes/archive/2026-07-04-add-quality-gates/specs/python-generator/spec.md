## ADDED Requirements

### Requirement: Frontmatter supports an optional reference solution field

A challenge `.md` frontmatter SHALL support an optional `reference_solution` field, a YAML block scalar holding a Python script that reads stdin and prints the correct output for the challenge independently of the `generator` field. When the field is absent, the challenge SHALL load and behave exactly as before.

#### Scenario: Optional field is backward compatible

- **WHEN** a challenge omits `reference_solution`
- **THEN** the challenge SHALL load and behave exactly as before, and content-layer regression SHALL skip it

### Requirement: Content-layer regression verifies reference solutions pass

An automated test SHALL, for each challenge that declares `reference_solution`, generate sample inputs the same way `scripts/generate-pools.ts` does, compute expected output via the `generator`, compute actual output via the `reference_solution`, and assert the two are equal after trailing-whitespace normalization. This is the offline equivalent of the reference solution earning an Accepted verdict against the production encrypted pool. The test SHALL report a count of challenges skipped for lacking `reference_solution`.

#### Scenario: Correct reference solution passes

- **WHEN** a challenge declares a `reference_solution` that matches its `generator` semantics
- **THEN** the content-layer regression test SHALL pass for that challenge

#### Scenario: Divergent reference solution fails and names the slug

- **WHEN** a challenge `reference_solution` produces output differing from its `generator` for some input
- **THEN** the content-layer regression test SHALL fail and identify the challenge slug

#### Scenario: Missing Python toolchain degrades gracefully

- **WHEN** python3 or PyYAML is unavailable in the environment
- **THEN** the content-layer regression test SHALL skip with a warning rather than failing
