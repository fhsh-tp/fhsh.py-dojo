## MODIFIED Requirements

### Requirement: WASM module judges student outputs internally

The WASM module SHALL export a `judge(challenge_id: &str, session_id: &str, results: JsValue)` function. The `results` parameter SHALL be an array of `{stdout: string, error?: string, elapsed_ms: number, timed_out?: boolean}` objects, one per testcase in session order; a missing, `undefined`, or `null` `timed_out` SHALL all be treated as not timed out (the field deserializes as an optional boolean precisely because serde-wasm-bindgen does not treat an explicit `undefined`-valued key as absent), so pre-existing callers keep their exact behavior. The function SHALL compare each `stdout` (trimmed trailing whitespace) against the corresponding `expected_output` from the session and return an array of verdict objects.

Verdict determination SHALL follow this precedence: `timed_out: true` → `TLE`; otherwise a non-empty `error` → `RE`; otherwise constant-time output comparison → `AC` or `WA`. The judge SHALL NOT inspect error message text to classify timeouts — the structured `timed_out` field is the only timeout signal.

Each verdict object SHALL contain:
- `verdict`: `AC` | `WA` | `TLE` | `RE`
- `actual`: included only when `verdict_detail` is `actual` or `full`
- `expected`: included only when `verdict_detail` is `full`
- `elapsed_ms`: passed through from input
- `error`: included only for `RE` verdicts; a `TLE` verdict SHALL carry no error message even when the input result contains one (the timeout message embeds the op limit and must not leak)

The string comparison SHALL use constant-time comparison to prevent timing-based answer extraction. After judging, the session data SHALL be zeroized and the session SHALL be invalidated.

#### Scenario: All correct answers produce AC verdicts

- **WHEN** all student outputs match expected outputs (after trimming trailing whitespace)
- **THEN** all verdict objects SHALL have `verdict: "AC"`

#### Scenario: Wrong answer produces WA with verdict_detail=hidden

- **WHEN** a student output does not match and `verdict_detail` is `hidden`
- **THEN** the verdict object SHALL contain `verdict: "WA"` and `elapsed_ms` only, with no `actual` or `expected` field

#### Scenario: Wrong answer produces WA with verdict_detail=full

- **WHEN** a student output does not match and `verdict_detail` is `full`
- **THEN** the verdict object SHALL contain `verdict: "WA"`, `actual`, `expected`, and `elapsed_ms`

#### Scenario: Runtime error produces RE verdict

- **WHEN** a result has a non-empty `error` field and `timed_out` is absent or false
- **THEN** the verdict SHALL be `RE` and the verdict object SHALL carry the error message

#### Scenario: Timed-out result produces TLE verdict

- **WHEN** a result has `timed_out: true`
- **THEN** the verdict SHALL be `TLE` and the verdict object SHALL contain no `error` field, even if the input result also carried an `error` message

#### Scenario: Results without timed_out keep legacy behavior

- **WHEN** the results array objects contain no `timed_out` field at all
- **THEN** every verdict SHALL be identical to the pre-TLE behavior (AC/WA/RE only)

#### Scenario: Explicit undefined timed_out keys do not poison the batch

- **WHEN** result objects carry an explicit `timed_out` key whose value is `undefined` (a shape plain JS object literals naturally produce)
- **THEN** deserialization SHALL succeed and those results SHALL judge as not timed out

#### Scenario: Session invalidated after judging

- **WHEN** `judge` is called with a valid session_id
- **AND** then called again with the same session_id
- **THEN** the second call SHALL return an error indicating the session is invalid
