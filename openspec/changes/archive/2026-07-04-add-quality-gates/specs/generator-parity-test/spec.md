## ADDED Requirements

### Requirement: Rust and Python input generators conform to identical ParamSpec constraints

An automated test suite SHALL verify that, for a shared set of ParamSpec fixtures covering every supported parameter type and the count and multiple_of variants, both the Rust input generator (in the `testcase-generator` crate) and the Python input generator (used by `scripts/generate-pools.ts`) produce outputs satisfying the same declared constraints: character set, length range, value range, count range, separator, and multiple_of. Because the two implementations use different random number generators, the test SHALL assert constraint conformance rather than byte-identical output.

#### Scenario: Both generators satisfy the same constraints

- **WHEN** the parity test generates many samples for a `hex_string` ParamSpec with min_len 4 and max_len 8 from both implementations
- **THEN** every sample from each implementation SHALL contain only `0-9a-f` characters with length within the range 4 to 8

### Requirement: The set of supported parameter types is kept in sync

The parity test SHALL assert that the set of parameter `type` values supported by the Rust generator equals the set supported by the Python generator, except for entries in an explicit allow-list of documented divergences such as the Rust-only `faker` type. Adding a new type to one implementation without updating the other or the allow-list SHALL cause the test to fail.

#### Scenario: Unsynchronized new type fails the test

- **WHEN** a new parameter type is added to the Rust generator but not to the Python generator and not to the allow-list
- **THEN** the parity test SHALL fail and identify the unsynchronized type
