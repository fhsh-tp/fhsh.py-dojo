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
use wasm_bindgen::prelude::*;

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
}
