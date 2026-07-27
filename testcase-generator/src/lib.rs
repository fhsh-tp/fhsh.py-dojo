mod parser;
mod rng;
mod crypto;
mod judge;
mod key_material;
mod pool;

// Re-exported for reuse and for the `param_conformance` integration test:
// these are the core random-input generation API that `generate_challenge`
// wraps for WASM. Exposing them lets tests exercise the same code path.
pub use parser::parse_params;
pub use rng::generate_input;

use rand::SeedableRng;
use rand::rngs::SmallRng;
use serde::Serialize;
use serde_json::Value;
use wasm_bindgen::prelude::*;

/// Default per-input worst-case budget for pool generation (bytes).
/// Challenges may raise it via the frontmatter `input_budget` field, up to
/// `parser::HARD_CAP_BYTES` which is never overridable.
pub const DEFAULT_INPUT_BUDGET: u64 = 4096;

/// Output of `generate_challenge`: a list of random stdin input strings,
/// one per testcase. The frontend feeds each to the Python generator to
/// produce the corresponding expected output.
#[derive(Serialize)]
struct GeneratedInputs {
    inputs: Vec<String>,
}

/// Generate random input strings from a JSON params specification.
///
/// # Arguments
/// * `params_json` — JSON object mapping param names to ParamSpec objects,
///   in the order they should appear as stdin lines.
/// * `count` — number of testcase inputs to generate.
///
/// # Returns
/// `{ inputs: [string, ...] }` — one input string per testcase.
#[wasm_bindgen]
pub fn generate_challenge(params_json: &str, count: usize) -> Result<JsValue, JsError> {
    let params = parser::parse_params(params_json).map_err(|e| JsError::new(&e))?;
    let mut rng = SmallRng::from_entropy();
    let inputs: Vec<String> = (0..count)
        .map(|_| rng::generate_input(&params, &mut rng))
        .collect();
    let result = GeneratedInputs { inputs };
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsError::new(&e.to_string()))
}

/// Stable 64-bit FNV-1a hash. Used to derive a deterministic RNG seed from
/// the pool-spec seed string + params content; no external dependency and
/// identical results on every platform.
fn fnv1a64(chunks: &[&[u8]]) -> u64 {
    const OFFSET: u64 = 0xcbf29ce484222325;
    const PRIME: u64 = 0x100000001b3;
    let mut h = OFFSET;
    for chunk in chunks {
        for &b in *chunk {
            h ^= b as u64;
            h = h.wrapping_mul(PRIME);
        }
    }
    h
}

/// Core of `generate_pool_inputs`, kept off the WASM boundary so native
/// tests can exercise the full envelope parsing / seeding / budget logic.
pub fn pool_inputs_from_spec(spec_json: &str, count: usize) -> Result<Vec<String>, String> {
    let v: Value = serde_json::from_str(spec_json)
        .map_err(|e| format!("JSON parse error: {e}"))?;
    let obj = v
        .as_object()
        .ok_or_else(|| "pool spec must be a JSON object".to_string())?;

    let mut params_v: Option<&Value> = None;
    let mut seed: Option<&str> = None;
    let mut budget: Option<u64> = None;

    for (key, val) in obj {
        match key.as_str() {
            "params" => params_v = Some(val),
            "seed" => {
                seed = Some(
                    val.as_str()
                        .ok_or_else(|| "pool spec: 'seed' must be a string".to_string())?,
                );
            }
            "input_budget" => {
                budget = Some(val.as_u64().ok_or_else(|| {
                    "pool spec: 'input_budget' must be a non-negative integer".to_string()
                })?);
            }
            "testcase_plan" => {
                return Err(
                    "pool spec: 'testcase_plan' is reserved and not yet implemented".to_string()
                );
            }
            other => {
                return Err(format!(
                    "pool spec: unknown field '{other}' (allowed: params, seed, input_budget)"
                ));
            }
        }
    }

    let params_v = params_v.ok_or_else(|| "pool spec: missing required field 'params'".to_string())?;
    let params = parser::parse_params_value(params_v)?;

    let effective_budget = budget.unwrap_or(DEFAULT_INPUT_BUDGET);
    if effective_budget > parser::HARD_CAP_BYTES {
        return Err(format!(
            "pool spec: input_budget ({effective_budget}) exceeds the {} -byte hard cap",
            parser::HARD_CAP_BYTES
        ));
    }
    let (total, items) = parser::estimate_input_bytes(&params);
    if total > effective_budget {
        return Err(parser::budget_error(total, effective_budget, &items, "input budget"));
    }

    let mut rng: SmallRng = match seed {
        Some(s) => {
            // Effective seed covers both the caller-provided seed string
            // (the challenge slug) and the params content, so editing any
            // declared bound automatically reshuffles the pool.
            let params_json = serde_json::to_string(params_v)
                .map_err(|e| format!("failed to serialize params: {e}"))?;
            SmallRng::seed_from_u64(fnv1a64(&[s.as_bytes(), &[0u8], params_json.as_bytes()]))
        }
        None => SmallRng::from_entropy(),
    };

    Ok((0..count).map(|_| rng::generate_input(&params, &mut rng)).collect())
}

/// Generate pool input strings from a full pool-spec object:
/// `{ "params": {…}, "seed": "<slug>", "input_budget": <bytes> }`.
///
/// Unlike `generate_challenge` (browser dev mode, entropy-seeded), this is
/// the build-time entry: with `seed` present the output is deterministic
/// for identical specs, and the configurable input budget is enforced.
/// The top-level key `testcase_plan` is reserved for a future capability
/// and is refused loudly instead of being silently ignored.
#[wasm_bindgen]
pub fn generate_pool_inputs(spec_json: &str, count: usize) -> Result<JsValue, JsError> {
    let inputs = pool_inputs_from_spec(spec_json, count).map_err(|e| JsError::new(&e))?;
    let result = GeneratedInputs { inputs };
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsError::new(&e.to_string()))
}

// ── Pool & Judge WASM API ──────────────────────────────────────────────

/// Load and decrypt an encrypted pool file.
///
/// # Arguments
/// * `challenge_id` — unique identifier for the challenge (e.g., "caesar_encrypt")
/// * `encrypted_data` — raw bytes of the `.bin` pool file
#[wasm_bindgen]
pub fn load_pool(challenge_id: &str, encrypted_data: &[u8]) -> Result<(), JsError> {
    pool::load_pool(challenge_id, encrypted_data).map_err(|e| JsError::new(&e))
}

/// Select random testcases from a loaded pool.
///
/// # Returns
/// `{ inputs: string[], session_id: string, verdict_detail: string }` — inputs only, no expected outputs.
#[wasm_bindgen]
pub fn select_testcases(challenge_id: &str, count: usize) -> Result<JsValue, JsError> {
    let (session_id, inputs, verdict_detail) =
        pool::select_testcases(challenge_id, count).map_err(|e| JsError::new(&e))?;

    #[derive(Serialize)]
    struct SelectResult {
        inputs: Vec<String>,
        session_id: String,
        verdict_detail: String,
    }

    let vd_str = match verdict_detail {
        pool::VerdictDetail::Hidden => "hidden",
        pool::VerdictDetail::Actual => "actual",
        pool::VerdictDetail::Full => "full",
    };

    let result = SelectResult { inputs, session_id, verdict_detail: vd_str.to_string() };
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsError::new(&e.to_string()))
}

/// Get expected output for a specific testcase in a session.
/// Returns `null` if verdict_detail does not allow it.
#[wasm_bindgen]
pub fn get_expected(
    challenge_id: &str,
    session_id: &str,
    index: usize,
) -> Result<JsValue, JsError> {
    let result =
        pool::get_expected(challenge_id, session_id, index).map_err(|e| JsError::new(&e))?;
    match result {
        Some(s) => Ok(JsValue::from_str(&s)),
        None => Ok(JsValue::NULL),
    }
}

/// Judge student outputs against expected outputs for a session.
///
/// # Arguments
/// * `challenge_id` — must match the session's challenge
/// * `session_id` — from `select_testcases`
/// * `results` — array of `{ stdout, error?, elapsed_ms }` objects
///
/// # Returns
/// Array of `{ verdict, actual?, expected?, elapsed_ms, error? }` objects.
/// The session is invalidated after this call.
#[wasm_bindgen(js_name = "judge")]
pub fn judge_wasm(
    challenge_id: &str,
    session_id: &str,
    results: JsValue,
) -> Result<JsValue, JsError> {
    let student_results: Vec<judge::StudentResult> =
        serde_wasm_bindgen::from_value(results).map_err(|e| JsError::new(&e.to_string()))?;

    let verdicts =
        judge::judge(challenge_id, session_id, student_results).map_err(|e| JsError::new(&e))?;

    serde_wasm_bindgen::to_value(&verdicts).map_err(|e| JsError::new(&e.to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generate_challenge_returns_correct_count() {
        let json = r#"{"shift": {"type": "int", "min": 1, "max": 25}}"#;
        let params = parser::parse_params(json).unwrap();
        let mut rng = SmallRng::seed_from_u64(42);
        let inputs: Vec<String> = (0..5)
            .map(|_| rng::generate_input(&params, &mut rng))
            .collect();
        assert_eq!(inputs.len(), 5);
        for input in &inputs {
            let v: i64 = input.parse().unwrap();
            assert!((1..=25).contains(&v));
        }
    }

    #[test]
    fn generate_challenge_invalid_params_json() {
        let result = parser::parse_params("not json");
        assert!(result.is_err());
    }

    // ── generate_pool_inputs envelope ───────────────────────────────────

    const DEQUE_SPEC: &str = r#"{
        "seed": "find-min-max",
        "params": {
            "t": {"type": "int", "min": 2, "max": 4},
            "cases": {"type": "group", "repeat": "t", "params": {
                "n": {"type": "int", "min": 1, "max": 6},
                "nums": {"type": "int", "min": -999, "max": 999, "count": {"from": "n", "separator": "\n"}}
            }}
        }
    }"#;

    #[test]
    fn pool_inputs_deterministic_for_same_spec() {
        let a = pool_inputs_from_spec(DEQUE_SPEC, 10).unwrap();
        let b = pool_inputs_from_spec(DEQUE_SPEC, 10).unwrap();
        assert_eq!(a, b, "same spec + seed must be byte-identical");
    }

    #[test]
    fn pool_inputs_change_when_params_change() {
        let changed = DEQUE_SPEC.replace(r#""max": 6"#, r#""max": 7"#);
        let a = pool_inputs_from_spec(DEQUE_SPEC, 10).unwrap();
        let b = pool_inputs_from_spec(&changed, 10).unwrap();
        assert_ne!(a, b, "params content change must reshuffle the sequence");
    }

    #[test]
    fn pool_inputs_change_when_seed_changes() {
        let reseeded = DEQUE_SPEC.replace("find-min-max", "another-slug");
        let a = pool_inputs_from_spec(DEQUE_SPEC, 10).unwrap();
        let b = pool_inputs_from_spec(&reseeded, 10).unwrap();
        assert_ne!(a, b, "different seed must reshuffle the sequence");
    }

    #[test]
    fn pool_inputs_reserved_testcase_plan_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": []}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("reserved"), "got: {err}");
    }

    #[test]
    fn pool_inputs_unknown_top_level_field_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "sead": "typo"}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("unknown field 'sead'"), "got: {err}");
    }

    #[test]
    fn pool_inputs_missing_params_is_refused() {
        let err = pool_inputs_from_spec(r#"{"seed": "x"}"#, 1).unwrap_err();
        assert!(err.contains("missing required field 'params'"), "got: {err}");
    }

    #[test]
    fn pool_inputs_default_budget_enforced() {
        // 5000 single-digit values exceed the 4096-byte default budget but
        // stay under the hard cap, so only the pool entry rejects it.
        let spec = r#"{"params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}}}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("input budget"), "got: {err}");
        assert!(err.contains("per-param estimate"), "got: {err}");
        // The same params parse fine standalone (dev mode only enforces the hard cap).
        assert!(parser::parse_params(r#"{"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}}"#).is_ok());
    }

    #[test]
    fn pool_inputs_budget_override_allows_larger_inputs() {
        let spec = r#"{"input_budget": 16384, "params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}}}"#;
        let inputs = pool_inputs_from_spec(spec, 2).unwrap();
        assert_eq!(inputs.len(), 2);
    }

    #[test]
    fn pool_inputs_budget_above_hard_cap_is_refused() {
        let spec = r#"{"input_budget": 100000, "params": {"n": {"type": "int"}}}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("hard cap"), "got: {err}");
    }

    #[test]
    fn pool_inputs_without_seed_still_generates() {
        let spec = r#"{"params": {"n": {"type": "int", "min": 1, "max": 9}}}"#;
        let inputs = pool_inputs_from_spec(spec, 3).unwrap();
        assert_eq!(inputs.len(), 3);
    }
}
