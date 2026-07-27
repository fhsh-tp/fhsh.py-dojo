## REMOVED Requirements

### Requirement: Rust and Python input generators conform to identical ParamSpec constraints

**Reason**: The Python input generator embedded in `scripts/generate-pools.ts` is removed; build-time input generation now calls the same Rust/WASM engine used at runtime, so there is no second implementation whose constraint conformance could diverge.

**Migration**: Constraint conformance for the single remaining implementation stays covered by `testcase-generator/tests/param_conformance.rs`. Declaration-level coverage across all challenge content moves to the new all-challenge params conformance gate (`scripts/challenge-params.test.ts`) specified under the `python-generator` capability.

### Requirement: The set of supported parameter types is kept in sync

**Reason**: With exactly one input-generation implementation, there is no second type set to keep in sync; the requirement's subject no longer exists.

**Migration**: Content-side drift (a challenge declaring a type the engine does not support) is caught by the all-challenge params conformance gate (`scripts/challenge-params.test.ts`), which fails naming the offending challenge file. Engine-side type documentation drift is covered by the Usage.md contract updates in this change.
