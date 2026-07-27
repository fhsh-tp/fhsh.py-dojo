## MODIFIED Requirements

### Requirement: Rust WASM generates random inputs only

The `generate_challenge(params_json, count)` WASM function SHALL accept `params_json: &str` (JSON-serialized params object from frontmatter) and `count: usize` (number of testcases). It SHALL deserialize the params, generate `count` random input strings (one per testcase), and return an object containing only `inputs: Vec<String>`. It SHALL NOT compute `expected_output`. `indexmap::IndexMap` SHALL be used to preserve key order.

Rendering contract: each scalar param SHALL render as one block in declaration order, blocks joined by newline. A scalar param without `count` renders as a single line; a param with `count > 1` renders its values joined by `count.separator` (a separator of `"\n"` therefore spans multiple lines). A group param renders its inner params in declaration order once per repetition, repetitions joined by newline.

Each non-group `ParamSpec` variant SHALL support an optional `count` field of type `CountSpec`. `CountSpec` SHALL support two mutually exclusive sizing modes:
- Range mode: `min: usize` (default 1), `max: usize` (default 1) — actual count picked uniformly at random in `[min, max]`.
- Linked mode: `from: String` — actual count equals the value already generated for the referenced param (see the count linkage requirement).
- `separator: String` — delimiter used to join multiple values (default: `" "`).

Declaring `from` together with an explicit `min` or `max` SHALL be a parse error. The entire `count` field SHALL default to range mode `{ min: 1, max: 1, separator: " " }` when omitted, preserving backward compatibility.

The supported `ParamSpec` variants SHALL be: `Int`, `AlphaUpper`, `AlphaLower`, `AlphaMixed`, `HexString`, `PrintableAscii`, `Enum`, `Group`, and optionally `Faker` (when the `faker` Cargo feature is enabled). Challenge frontmatter params MUST use only these valid type names: `int`, `alpha_upper`, `alpha_lower`, `alpha_mixed`, `hex_string`, `printable_ascii`, `enum`, `group`, and `faker`. Using any other type name SHALL result in a deserialization error. Unknown fields on any param spec, count spec, or top-level pool spec object SHALL be rejected at parse time (deny unknown fields).

#### Scenario: generate_challenge returns inputs in param order

- **WHEN** `generate_challenge` is called with params JSON `{"plaintext": {...}, "shift": {...}}`
- **THEN** each input string is `"{plaintext_value}\n{shift_value}"` in that key order

#### Scenario: generate_challenge respects count parameter

- **WHEN** `generate_challenge` is called with `count = 5`
- **THEN** the returned `inputs` array contains exactly 5 strings

#### Scenario: CountSpec with min and max generates variable number of values

- **WHEN** a param is declared with `count: { min: 2, max: 5 }`
- **THEN** the generated line for that param contains between 2 and 5 values joined by separator (inclusive)

#### Scenario: Omitting count preserves existing behavior

- **WHEN** a param is declared without a `count` field
- **THEN** the param generates exactly 1 value with no separator (identical to previous behavior)

#### Scenario: Invalid type name causes deserialization error

- **WHEN** frontmatter params contain `type: string` or `type: hex`
- **THEN** parsing returns an error indicating unknown variant with the list of valid variants

#### Scenario: Unknown field is rejected instead of silently ignored

- **WHEN** a param declares `count: { from: "n" }` against a parser build that predates linked mode, or any spec carries a misspelled field such as `min_lenght`
- **THEN** parsing SHALL fail with an unknown-field error rather than silently applying defaults

#### Scenario: Newline separator renders one value per line

- **WHEN** a param is declared with `count: { from: "n", separator: "\n" }` and the generated value of `n` is 4
- **THEN** the rendered block for that param contains exactly 4 lines, one value per line

## ADDED Requirements

### Requirement: Group construct repeats a nested param block

The params model SHALL support a `group` param: `{ "type": "group", "repeat": "<param-name>", "params": { ... } }`. The group's inner `params` object SHALL follow the same rules as top-level params except that a group MUST NOT contain another group (maximum nesting depth 1). The group SHALL render its inner params once per repetition; the repetition count SHALL equal the value already generated for the param referenced by `repeat`.

Reference legality for `repeat` and `count.from` SHALL be validated at parse time:
- The referenced param MUST be declared before the referencing host, in the same scope or (for hosts inside a group) at top level. Within one group repetition, inner params MAY reference earlier inner params of the same repetition; each repetition resolves independently.
- The referenced param MUST be a scalar `int` (no `count` field, or a fixed `count` of exactly 1) with `min >= 0`.
- Referencing a group, an undeclared name, or a later-declared name SHALL be a parse error.

#### Scenario: Competition-style nested format is expressible

- **WHEN** params declare `t` (int) followed by a group with `repeat: t` whose inner params are `n` (int) and `nums` (int with `count: { from: "n", separator: "\n" }`)
- **THEN** each generated input renders as: first line `t`, then for each of the `t` repetitions one line `n` followed by exactly `n` lines each containing one integer

#### Scenario: Zero repetitions renders an empty group block

- **WHEN** a group's `repeat` references an int param whose generated value is 0
- **THEN** the group contributes no lines to the rendered input

#### Scenario: Forward reference is a parse error

- **WHEN** a param declares `count: { from: "n" }` and `n` is declared after that param
- **THEN** parsing SHALL fail with an error naming the illegal forward or unknown reference

#### Scenario: Non-scalar-int reference is a parse error

- **WHEN** `repeat` or `count.from` references a param that is not type `int`, or an int with `count.max > 1`, or an int with `min < 0`
- **THEN** parsing SHALL fail with an error naming the violated reference rule

#### Scenario: Nested group is a parse error

- **WHEN** a group's inner params contain another `type: group` param
- **THEN** parsing SHALL fail with a nesting-depth error

#### Scenario: Nested params are validated recursively

- **WHEN** a group's inner params contain an `enum` with an empty `values` array
- **THEN** parsing SHALL fail with the same validation error that an equivalent top-level declaration produces

### Requirement: Pool input generation is deterministic and budget-enforced

A WASM entry `generate_pool_inputs(spec_json, count)` SHALL accept a pool spec object `{ "params": { ... }, "seed": <string, optional>, "input_budget": <bytes, optional> }` and return `inputs: Vec<String>` like `generate_challenge`. When `seed` is present, the RNG SHALL be seeded from a stable 64-bit FNV-1a hash over the seed string, a zero byte, and the serialized params content, so that identical spec objects always produce identical inputs across builds and platforms. When `seed` is absent, entropy seeding SHALL be used. The top-level key `testcase_plan` SHALL be recognized as reserved: its presence SHALL produce an explicit "reserved, not yet implemented" error rather than silent acceptance, and any other unknown top-level key SHALL be an unknown-field parse error.

Input size SHALL be governed by a worst-case estimate computed at parse time from declared bounds (digit width for ints including sign, `max_len` for string types, longest value for enums, multiplied by the count upper bound — `count.max` or the referenced param's `max` — plus separators, and group inner totals multiplied by the repeat reference's `max`). The estimate SHALL be an upper bound on actual rendered bytes. `parse_params` SHALL unconditionally reject specs whose estimate exceeds the hard cap of 65536 bytes. `generate_pool_inputs` SHALL additionally enforce the configurable budget: default 4096 bytes, overridable via `input_budget` up to the hard cap; declaring `input_budget` above the hard cap SHALL be a parse error. Budget violations SHALL fail with an error that itemizes the per-param estimate.

#### Scenario: Same spec yields identical pools across builds

- **WHEN** `generate_pool_inputs` is called twice with an identical spec object containing a `seed`
- **THEN** both calls return byte-identical `inputs`

#### Scenario: Changing params content changes the sequence

- **WHEN** the same `seed` string is used but any params content differs
- **THEN** the generated inputs differ (the effective seed incorporates params content)

#### Scenario: Default budget rejects oversized declarations

- **WHEN** a spec without `input_budget` declares bounds whose worst-case estimate exceeds 4096 bytes
- **THEN** `generate_pool_inputs` fails with an error listing per-param byte estimates

#### Scenario: Hard cap cannot be overridden

- **WHEN** a spec declares `input_budget: 100000`
- **THEN** parsing fails with an error stating the 65536-byte hard cap

#### Scenario: Reserved testcase_plan key is refused loudly

- **WHEN** a spec object contains a `testcase_plan` key
- **THEN** `generate_pool_inputs` fails with an error stating the field is reserved and not yet implemented

### Requirement: Invalid specs fail at parse time instead of trapping at generation time

All spec validation — inverted ranges (`min > max`, `min_len > max_len`, `count.min > count.max`), empty enum values, reference legality, nesting depth, unknown fields, and budget caps — SHALL be performed by `parse_params` (or the pool spec parser) and reported as readable errors. Generation SHALL NOT be reachable with a spec that can panic the WASM instance; the previously observed `RuntimeError: unreachable` trap for `min > max` SHALL be replaced by a parse error.

#### Scenario: Inverted int range is a parse error, not a trap

- **WHEN** a param declares `{ "type": "int", "min": 9, "max": 1 }`
- **THEN** parsing returns a readable range error and no WASM trap occurs

#### Scenario: WASM instance stays usable after a rejected spec

- **WHEN** a call fails due to any parse-time validation error
- **THEN** a subsequent call with a valid spec on the same instance succeeds

### Requirement: Every challenge params declaration passes the engine parser

A test (`scripts/challenge-params.test.ts`) SHALL enumerate all `docs/challenge/*.md` files, extract each `params` declaration, and assert that the WASM parser accepts it and that its worst-case input estimate passes the applicable budget. The test SHALL fail (not skip) when the WASM artifact is missing, and SHALL fail when zero challenge files are found.

#### Scenario: A challenge with an unsupported type is caught at test time

- **WHEN** any challenge declares a param type or field the engine parser rejects
- **THEN** the test fails naming the challenge file and the parse error

#### Scenario: Missing WASM artifact is a failure, not a skip

- **WHEN** the test runs in an environment where the WASM artifact has not been built
- **THEN** the test fails with an actionable message instead of skipping
