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

// ── testcase_plan ──────────────────────────────────────────────────────

/// One parsed `testcase_plan` entry, ready for generation.
enum PlanEntry {
    /// `count` inputs drawn from the base params deep-merged with `override`.
    Band { count: u64, params: parser::Params },
    /// One input taken verbatim from the declaration.
    Literal(String),
}

/// Weighted size of one plan round: Σ band counts + one per literal.
fn plan_total(entries: &[PlanEntry]) -> u64 {
    entries
        .iter()
        .map(|e| match e {
            PlanEntry::Band { count, .. } => *count,
            PlanEntry::Literal(_) => 1,
        })
        .sum()
}

/// Deep-merge a band override into the base params JSON: recurse where both
/// sides are objects, replace otherwise. Every override key must exist in
/// the base object at its level — a typo must fail loudly, never silently
/// introduce a new param.
fn merge_override(base: &Value, ovr: &Value, path: &str) -> Result<Value, String> {
    match (base, ovr) {
        (Value::Object(b), Value::Object(o)) => {
            let mut out = b.clone();
            for (k, v) in o {
                let child_path = if path.is_empty() {
                    k.clone()
                } else {
                    format!("{path}.{k}")
                };
                let bv = b
                    .get(k)
                    .ok_or_else(|| format!("override references unknown key '{child_path}'"))?;
                out.insert(k.clone(), merge_override(bv, v, &child_path)?);
            }
            Ok(Value::Object(out))
        }
        (_, other) => Ok(other.clone()),
    }
}

/// Parse and validate a `testcase_plan` array against the base params.
///
/// `budget` is the effective per-input budget for pool builds; `None` means
/// hard-cap-only enforcement (the dev entry, mirroring how dev mode has
/// always treated base params). Every band is re-validated through the full
/// `parse_params_value` surface after merging, so a plan can never reach
/// generation with a spec the base parser would reject.
fn parse_testcase_plan(
    plan_v: &Value,
    base_params_v: &Value,
    budget: Option<u64>,
) -> Result<Vec<PlanEntry>, String> {
    let arr = plan_v
        .as_array()
        .ok_or_else(|| "testcase_plan must be a JSON array".to_string())?;
    if arr.is_empty() {
        return Err("testcase_plan must contain at least one entry".to_string());
    }
    let mut entries = Vec::with_capacity(arr.len());
    for (i, entry_v) in arr.iter().enumerate() {
        let obj = entry_v
            .as_object()
            .ok_or_else(|| format!("testcase_plan entry {i}: must be a JSON object"))?;
        let has_count = obj.contains_key("count");
        let has_literal = obj.contains_key("literal");
        if has_count && has_literal {
            return Err(format!(
                "testcase_plan entry {i}: 'count' and 'literal' are mutually exclusive"
            ));
        }
        if has_literal {
            if let Some(k) = obj.keys().find(|k| k.as_str() != "literal") {
                return Err(format!(
                    "testcase_plan entry {i}: unknown field '{k}' (a literal entry allows only 'literal')"
                ));
            }
            let s = obj["literal"]
                .as_str()
                .ok_or_else(|| format!("testcase_plan entry {i}: 'literal' must be a string"))?;
            if s.is_empty() {
                return Err(format!(
                    "testcase_plan entry {i}: 'literal' must be a non-empty string"
                ));
            }
            let len = s.len() as u64;
            if len >= parser::HARD_CAP_BYTES {
                return Err(format!(
                    "testcase_plan entry {i}: literal is {len} bytes, exceeding the {}-byte hard cap",
                    parser::HARD_CAP_BYTES
                ));
            }
            if let Some(b) = budget {
                if len > b {
                    return Err(format!(
                        "testcase_plan entry {i}: literal is {len} bytes, exceeding the {b}-byte input budget"
                    ));
                }
            }
            entries.push(PlanEntry::Literal(s.to_string()));
        } else if has_count {
            if let Some(k) = obj.keys().find(|k| k.as_str() != "count" && k.as_str() != "override") {
                return Err(format!(
                    "testcase_plan entry {i}: unknown field '{k}' (a band entry allows 'count' and 'override')"
                ));
            }
            let count = obj["count"]
                .as_u64()
                .filter(|&c| c >= 1)
                .ok_or_else(|| {
                    format!("testcase_plan entry {i}: 'count' must be a positive integer")
                })?;
            let merged_v = match obj.get("override") {
                None => base_params_v.clone(),
                Some(ovr) => {
                    if !ovr.is_object() {
                        return Err(format!(
                            "testcase_plan entry {i}: 'override' must be a JSON object"
                        ));
                    }
                    merge_override(base_params_v, ovr, "")
                        .map_err(|e| format!("testcase_plan entry {i}: {e}"))?
                }
            };
            let params = parser::parse_params_value(&merged_v)
                .map_err(|e| format!("testcase_plan entry {i}: {e}"))?;
            if let Some(b) = budget {
                let (total, items) = parser::estimate_input_bytes(&params);
                if total > b {
                    return Err(format!(
                        "testcase_plan entry {i}: {}",
                        parser::budget_error(total, b, &items, "input budget")
                    ));
                }
            }
            entries.push(PlanEntry::Band { count, params });
        } else {
            return Err(format!(
                "testcase_plan entry {i}: must declare either 'count' (band) or 'literal'"
            ));
        }
    }
    Ok(entries)
}

/// Emit one full plan round into `out`, drawing band values from `rng` in
/// declaration order. Shared by the pool (blocked) and dev (single-round)
/// paths so ordering can never drift between them.
fn push_plan_round<R: rand::Rng>(entries: &[PlanEntry], rng: &mut R, out: &mut Vec<String>) {
    for e in entries {
        match e {
            PlanEntry::Band { count, params } => {
                for _ in 0..*count {
                    out.push(rng::generate_input(params, rng));
                }
            }
            PlanEntry::Literal(s) => out.push(s.clone()),
        }
    }
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
    let mut plan_v: Option<&Value> = None;

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
                let n = val.as_u64().ok_or_else(|| {
                    "pool spec: 'input_budget' must be a positive integer".to_string()
                })?;
                if n == 0 {
                    return Err(
                        "pool spec: 'input_budget' must be >= 1 (omit the field to use the default; 0 does not mean unlimited)".to_string()
                    );
                }
                budget = Some(n);
            }
            "testcase_plan" => plan_v = Some(val),
            other => {
                return Err(format!(
                    "pool spec: unknown field '{other}' (allowed: params, seed, input_budget, testcase_plan)"
                ));
            }
        }
    }

    let params_v = params_v.ok_or_else(|| "pool spec: missing required field 'params'".to_string())?;
    let params = parser::parse_params_value(params_v)?;

    let effective_budget = budget.unwrap_or(DEFAULT_INPUT_BUDGET);
    // `>=` mirrors the parser's hard-cap check: accepted estimates are always
    // strictly below HARD_CAP_BYTES, so a budget equal to the cap would be an
    // accepted-yet-unreachable configuration (a silent cliff). The budget
    // itself remains an inclusive bound (`total > effective_budget` below).
    if effective_budget >= parser::HARD_CAP_BYTES {
        return Err(format!(
            "pool spec: input_budget ({effective_budget}) must be strictly below the {}-byte hard cap",
            parser::HARD_CAP_BYTES
        ));
    }
    // For plan specs every generated input flows through a band's merged
    // params (each gated below), so the base-params estimate is not a
    // generation bound — gating it against the budget would falsely reject
    // bases that bands only ever tighten. The hard cap on the base was
    // already enforced by `parse_params_value` above.
    let plan = match plan_v {
        Some(pv) => Some(parse_testcase_plan(pv, params_v, Some(effective_budget))?),
        None => {
            let (total, items) = parser::estimate_input_bytes(&params);
            if total > effective_budget {
                return Err(parser::budget_error(total, effective_budget, &items, "input budget"));
            }
            None
        }
    };

    let mut rng: SmallRng = match seed {
        Some(s) => {
            // Effective seed covers the caller-provided seed string (the
            // challenge slug) and the params content, so editing any declared
            // bound automatically reshuffles the pool. When a testcase_plan
            // is declared its content joins the hash (editing a band bound or
            // literal reshuffles too); without a plan the hash input stays
            // byte-identical to the previous engine version, so existing
            // non-plan pools reproduce exactly.
            let params_json = serde_json::to_string(params_v)
                .map_err(|e| format!("failed to serialize params: {e}"))?;
            let h = match plan_v {
                None => fnv1a64(&[s.as_bytes(), &[0u8], params_json.as_bytes()]),
                Some(pv) => {
                    let plan_json = serde_json::to_string(pv)
                        .map_err(|e| format!("failed to serialize testcase_plan: {e}"))?;
                    fnv1a64(&[
                        s.as_bytes(),
                        &[0u8],
                        params_json.as_bytes(),
                        &[0u8],
                        plan_json.as_bytes(),
                    ])
                }
            };
            SmallRng::seed_from_u64(h)
        }
        None => SmallRng::from_entropy(),
    };

    match plan {
        None => Ok((0..count).map(|_| rng::generate_input(&params, &mut rng)).collect()),
        Some(entries) => {
            let total = plan_total(&entries);
            // u64 math first: wasm32 usize is 32-bit, so widen before checking.
            let count_u64 = count as u64;
            if count == 0 || count_u64 % total != 0 {
                return Err(format!(
                    "pool spec: count {count} must be a positive multiple of the plan total {total}"
                ));
            }
            let blocks = count_u64 / total;
            let mut out = Vec::with_capacity(count);
            for _ in 0..blocks {
                push_plan_round(&entries, &mut rng, &mut out);
            }
            Ok(out)
        }
    }
}

/// Core of `generate_dev_inputs`: one full plan round, entropy-seeded.
/// Dev mode mirrors its historical params handling — hard cap only, the
/// configurable pool budget is not enforced here.
pub fn dev_inputs_from_spec(spec_json: &str) -> Result<Vec<String>, String> {
    let v: Value = serde_json::from_str(spec_json)
        .map_err(|e| format!("JSON parse error: {e}"))?;
    let obj = v
        .as_object()
        .ok_or_else(|| "dev spec must be a JSON object".to_string())?;

    let mut params_v: Option<&Value> = None;
    let mut plan_v: Option<&Value> = None;
    for (key, val) in obj {
        match key.as_str() {
            "params" => params_v = Some(val),
            "testcase_plan" => plan_v = Some(val),
            other => {
                return Err(format!(
                    "dev spec: unknown field '{other}' (allowed: params, testcase_plan)"
                ));
            }
        }
    }
    let params_v =
        params_v.ok_or_else(|| "dev spec: missing required field 'params'".to_string())?;
    // Full base validation (including the hard cap) before touching the plan.
    parser::parse_params_value(params_v)?;
    let plan_v = plan_v.ok_or_else(|| {
        "dev spec: missing 'testcase_plan' — non-plan challenges use generate_challenge"
            .to_string()
    })?;
    let entries = parse_testcase_plan(plan_v, params_v, None)?;

    let mut rng = SmallRng::from_entropy();
    let mut out = Vec::with_capacity(plan_total(&entries) as usize);
    push_plan_round(&entries, &mut rng, &mut out);
    Ok(out)
}

/// Generate pool input strings from a full pool-spec object:
/// `{ "params": {…}, "seed": "<slug>", "input_budget": <bytes> }`.
///
/// Unlike `generate_challenge` (browser dev mode, entropy-seeded), this is
/// the build-time entry: with `seed` present the output is deterministic
/// for identical specs, and the configurable input budget is enforced.
/// With a `testcase_plan` declared, `count` must be a positive multiple of
/// the plan total and the output consists of consecutive blocks, each block
/// following the plan entry declaration order.
#[wasm_bindgen]
pub fn generate_pool_inputs(spec_json: &str, count: usize) -> Result<JsValue, JsError> {
    let inputs = pool_inputs_from_spec(spec_json, count).map_err(|e| JsError::new(&e))?;
    let result = GeneratedInputs { inputs };
    serde_wasm_bindgen::to_value(&result).map_err(|e| JsError::new(&e.to_string()))
}

/// Dev-mode entry for `testcase_plan` challenges: one full plan round
/// (`{ inputs }` with plan-total entries, declaration order), entropy-seeded
/// for practice variety. Refuses specs without a plan — those keep using
/// `generate_challenge`.
#[wasm_bindgen]
pub fn generate_dev_inputs(spec_json: &str) -> Result<JsValue, JsError> {
    let inputs = dev_inputs_from_spec(spec_json).map_err(|e| JsError::new(&e))?;
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

    // ── testcase_plan ───────────────────────────────────────────────────

    /// Fixed-value bands make ordering assertions deterministic regardless
    /// of the RNG: band A always renders "100", band B always "200".
    const PLAN_SPEC: &str = r#"{
        "seed": "plan-fixture",
        "params": {"a": {"type": "int", "min": 1, "max": 999}},
        "testcase_plan": [
            {"count": 2, "override": {"a": {"min": 100, "max": 100}}},
            {"count": 1, "override": {"a": {"min": 200, "max": 200}}},
            {"literal": "L\n"}
        ]
    }"#;

    #[test]
    fn plan_empty_array_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": []}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("at least one entry"), "got: {err}");
    }

    #[test]
    fn plan_non_array_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": {"count": 1}}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("must be a JSON array"), "got: {err}");
    }

    #[test]
    fn plan_block_order_follows_declaration() {
        let out = pool_inputs_from_spec(PLAN_SPEC, 8).unwrap();
        assert_eq!(
            out,
            vec!["100", "100", "200", "L\n", "100", "100", "200", "L\n"],
            "each block must follow plan declaration order"
        );
    }

    #[test]
    fn plan_count_zero_band_is_refused_with_index() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": [{"count": 1}, {"count": 0}]}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("entry 1"), "got: {err}");
        assert!(err.contains("positive integer"), "got: {err}");
    }

    #[test]
    fn plan_empty_literal_is_refused_with_index() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": [{"literal": ""}]}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("entry 0"), "got: {err}");
        assert!(err.contains("non-empty"), "got: {err}");
    }

    #[test]
    fn plan_mixed_count_and_literal_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": [{"count": 2, "literal": "x"}]}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("mutually exclusive"), "got: {err}");
    }

    #[test]
    fn plan_unknown_entry_field_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": [{"count": 2, "overide": {}}]}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("unknown field 'overide'"), "got: {err}");
    }

    #[test]
    fn plan_entry_without_count_or_literal_is_refused() {
        let spec = r#"{"params": {"n": {"type": "int"}}, "testcase_plan": [{}]}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("either 'count' (band) or 'literal'"), "got: {err}");
    }

    #[test]
    fn plan_override_unknown_key_names_the_path() {
        let spec = r#"{
            "params": {"cases": {"type": "group", "repeat": "t", "params": {"n": {"type": "int", "min": 1, "max": 5}}},
                       "t": {"type": "int", "min": 1, "max": 2}},
            "testcase_plan": [{"count": 1, "override": {"cases": {"params": {"m": {"max": 3}}}}}]
        }"#;
        // NOTE: params order above puts `cases` first so the reference check
        // fails? No — `repeat: "t"` must reference a PRIOR param, so keep the
        // legal order: t first, then cases.
        let spec = spec.replace(
            r#""cases": {"type": "group", "repeat": "t", "params": {"n": {"type": "int", "min": 1, "max": 5}}},
                       "t": {"type": "int", "min": 1, "max": 2}"#,
            r#""t": {"type": "int", "min": 1, "max": 2},
                       "cases": {"type": "group", "repeat": "t", "params": {"n": {"type": "int", "min": 1, "max": 5}}}"#,
        );
        let err = pool_inputs_from_spec(&spec, 1).unwrap_err();
        assert!(err.contains("unknown key 'cases.params.m'"), "got: {err}");
    }

    #[test]
    fn plan_merged_violation_reuses_parser_error() {
        let spec = r#"{
            "params": {"n": {"type": "int", "min": 1, "max": 4000}},
            "testcase_plan": [{"count": 1, "override": {"n": {"min": 5000}}}]
        }"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("entry 0"), "got: {err}");
        assert!(err.contains("min"), "got: {err}");
    }

    #[test]
    fn plan_band_budget_overflow_names_the_entry() {
        // Base fits the default 4096-byte budget; band 1 raises the count so
        // the merged worst case blows it. Base-only gating would miss this.
        let spec = r#"{
            "params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 10}}},
            "testcase_plan": [
                {"count": 1},
                {"count": 1, "override": {"n": {"count": {"max": 5000}}}}
            ]
        }"#;
        let err = pool_inputs_from_spec(spec, 2).unwrap_err();
        assert!(err.contains("entry 1"), "got: {err}");
        assert!(err.contains("input budget"), "got: {err}");
    }

    #[test]
    fn plan_literal_budget_overflow_names_the_entry() {
        let big = "x".repeat(5000);
        let spec = format!(
            r#"{{"params": {{"n": {{"type": "int"}}}}, "testcase_plan": [{{"literal": "{big}"}}]}}"#
        );
        let err = pool_inputs_from_spec(&spec, 1).unwrap_err();
        assert!(err.contains("entry 0"), "got: {err}");
        assert!(err.contains("input budget"), "got: {err}");
    }

    #[test]
    fn plan_band_over_budget_base_alone_is_accepted() {
        // Inverse of the band-overflow case: the base estimate exceeds the
        // default budget, but the only band tightens it back under. Plan
        // specs are gated per band, not on the base estimate.
        let spec = r#"{
            "params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}},
            "testcase_plan": [{"count": 1, "override": {"n": {"count": {"max": 10}}}}]
        }"#;
        let inputs = pool_inputs_from_spec(spec, 3).unwrap();
        assert_eq!(inputs.len(), 3);
    }

    #[test]
    fn plan_count_must_be_multiple_of_total() {
        // Plan total 6 (3 + 2 + literal) does not divide 200 — mirrors the
        // spec scenario: the error must carry both numbers.
        let spec = r#"{
            "params": {"a": {"type": "int", "min": 1, "max": 999}},
            "testcase_plan": [
                {"count": 3},
                {"count": 2, "override": {"a": {"max": 500}}},
                {"literal": "L\n"}
            ]
        }"#;
        let err = pool_inputs_from_spec(spec, 200).unwrap_err();
        assert!(err.contains("200"), "got: {err}");
        assert!(err.contains("plan total 6"), "got: {err}");
    }

    #[test]
    fn plan_seeded_output_is_deterministic() {
        let a = pool_inputs_from_spec(PLAN_SPEC, 8).unwrap();
        let b = pool_inputs_from_spec(PLAN_SPEC, 8).unwrap();
        assert_eq!(a, b);
    }

    #[test]
    fn plan_edit_reshuffles_band_values() {
        // Use a wide band so actual random draws (not fixed values) prove the
        // reshuffle: editing a band bound must change the sequence.
        let wide = r#"{
            "seed": "plan-fixture",
            "params": {"a": {"type": "int", "min": 1, "max": 999}},
            "testcase_plan": [{"count": 4, "override": {"a": {"max": 900}}}]
        }"#;
        let edited = wide.replace(r#""max": 900"#, r#""max": 901"#);
        let a = pool_inputs_from_spec(wide, 8).unwrap();
        let b = pool_inputs_from_spec(&edited, 8).unwrap();
        assert_ne!(a, b, "editing a band bound must reshuffle the pool");
    }

    #[test]
    fn non_plan_seed_derivation_is_unchanged() {
        // Snapshot taken from the engine BEFORE testcase_plan support landed
        // (commit 5ade019 era). Guards D3: non-plan specs must keep their
        // exact sequences so existing pools reproduce byte-identically.
        let out = pool_inputs_from_spec(DEQUE_SPEC, 3).unwrap();
        assert_eq!(
            out,
            vec![
                "2\n2\n-697\n970\n4\n472\n233\n-436\n-49",
                "2\n2\n-221\n732\n5\n-331\n732\n916\n94\n420",
                "2\n5\n170\n414\n768\n-808\n444\n1\n-813",
            ],
        );
    }

    // ── generate_dev_inputs ─────────────────────────────────────────────

    #[test]
    fn dev_inputs_return_one_ordered_round() {
        let spec = r#"{
            "params": {"a": {"type": "int", "min": 1, "max": 999}},
            "testcase_plan": [
                {"count": 2, "override": {"a": {"min": 100, "max": 100}}},
                {"count": 1, "override": {"a": {"min": 200, "max": 200}}},
                {"literal": "L\n"}
            ]
        }"#;
        let out = dev_inputs_from_spec(spec).unwrap();
        assert_eq!(out, vec!["100", "100", "200", "L\n"]);
    }

    #[test]
    fn dev_inputs_without_plan_is_refused() {
        let err = dev_inputs_from_spec(r#"{"params": {"n": {"type": "int"}}}"#).unwrap_err();
        assert!(err.contains("generate_challenge"), "got: {err}");
    }

    #[test]
    fn dev_inputs_unknown_field_is_refused() {
        let err = dev_inputs_from_spec(
            r#"{"params": {"n": {"type": "int"}}, "seed": "x", "testcase_plan": [{"count": 1}]}"#,
        )
        .unwrap_err();
        assert!(err.contains("unknown field 'seed'"), "got: {err}");
    }

    #[test]
    fn dev_inputs_skip_pool_budget_but_keep_hard_cap() {
        // 5000 single-digit values exceed the 4096-byte default pool budget —
        // dev mode accepts that (hard cap only), mirroring dev params rules.
        let spec = r#"{
            "params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}},
            "testcase_plan": [{"count": 2}]
        }"#;
        let out = dev_inputs_from_spec(spec).unwrap();
        assert_eq!(out.len(), 2);
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
    fn pool_inputs_budget_equal_to_hard_cap_is_refused() {
        // L-R3-3: parser rejects estimates >= cap, so a budget of exactly the
        // cap would be accepted-yet-unreachable — refuse the cliff instead.
        let spec = r#"{"input_budget": 65536, "params": {"n": {"type": "int"}}}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("strictly below"), "got: {err}");
    }

    #[test]
    fn pool_inputs_budget_zero_is_refused_with_guidance() {
        // L-R3-4: mirror the TS-side rule in the engine itself.
        let spec = r#"{"input_budget": 0, "params": {"n": {"type": "int"}}}"#;
        let err = pool_inputs_from_spec(spec, 1).unwrap_err();
        assert!(err.contains("0 does not mean unlimited"), "got: {err}");
    }

    #[test]
    fn pool_inputs_without_seed_still_generates() {
        let spec = r#"{"params": {"n": {"type": "int", "min": 1, "max": 9}}}"#;
        let inputs = pool_inputs_from_spec(spec, 3).unwrap();
        assert_eq!(inputs.len(), 3);
    }
}
