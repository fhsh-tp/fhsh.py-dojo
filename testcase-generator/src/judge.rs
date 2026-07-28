/// Verdict judging: compare student outputs against expected outputs.
///
/// Comparison uses constant-time equality to prevent timing attacks.
/// After judging, the session is destroyed (one-time use).
use serde::{Deserialize, Serialize};

use crate::pool::{self, VerdictDetail};

/// Input from the frontend: one entry per testcase in session order.
#[derive(Debug, Deserialize)]
pub struct StudentResult {
    pub stdout: String,
    #[serde(default)]
    pub error: Option<String>,
    pub elapsed_ms: f64,
    /// Structured timeout flag set by the Worker's run_only handler.
    /// Defaults to false so pre-TLE callers keep their exact behavior.
    #[serde(default)]
    pub timed_out: bool,
}

/// Verdict for a single testcase, returned to the frontend.
#[derive(Debug, Serialize)]
pub struct VerdictResult {
    pub verdict: &'static str,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub actual: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub expected: Option<String>,
    pub elapsed_ms: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
}

/// Constant-time byte comparison to prevent timing-based answer extraction.
fn constant_time_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut diff: u8 = 0;
    for (x, y) in a.iter().zip(b.iter()) {
        diff |= x ^ y;
    }
    diff == 0
}

/// Judge student outputs against expected outputs for a session.
///
/// The session is consumed (destroyed) after judging — one-time use.
/// Returns a verdict for each testcase.
pub fn judge(
    challenge_id: &str,
    session_id: &str,
    results: Vec<StudentResult>,
) -> Result<Vec<VerdictResult>, String> {
    // Take (consume) the session — it cannot be reused
    let (verdict_detail, testcases) = pool::take_session(challenge_id, session_id)?;

    if results.len() != testcases.len() {
        return Err(format!(
            "Expected {} results, got {}",
            testcases.len(),
            results.len()
        ));
    }

    let verdicts: Vec<VerdictResult> = results
        .iter()
        .enumerate()
        .map(|(i, result)| {
            let expected = &testcases[i].expected_output;

            // Determine verdict — timed_out wins over error: the timeout
            // message embeds the op limit and must not leak (TLE carries
            // no error message at all).
            let verdict = if result.timed_out {
                "TLE"
            } else if result.error.is_some() {
                "RE"
            } else {
                let actual_trimmed = result.stdout.trim_end();
                let expected_trimmed = expected.trim_end();
                if constant_time_eq(actual_trimmed.as_bytes(), expected_trimmed.as_bytes()) {
                    "AC"
                } else {
                    "WA"
                }
            };

            // Build result with verdict_detail-controlled stripping
            let actual_field = match verdict_detail {
                VerdictDetail::Hidden => None,
                VerdictDetail::Actual | VerdictDetail::Full => Some(result.stdout.clone()),
            };

            let expected_field = match verdict_detail {
                VerdictDetail::Full => Some(expected.clone()),
                _ => None,
            };

            VerdictResult {
                verdict,
                actual: actual_field,
                expected: expected_field,
                elapsed_ms: result.elapsed_ms,
                error: if verdict == "RE" {
                    result.error.clone()
                } else {
                    None
                },
            }
        })
        .collect();

    // Session was already consumed by take_session — no cleanup needed
    Ok(verdicts)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::crypto;
    use crate::key_material;
    use aes_gcm::aead::{Aead, OsRng};
    use aes_gcm::{AeadCore, Aes256Gcm, KeyInit};

    fn setup_pool(challenge_id: &str, detail: &str, testcases: &[(&str, &str)]) -> String {
        let tc_json: Vec<serde_json::Value> = testcases
            .iter()
            .map(|(i, e)| serde_json::json!({"input": i, "expected_output": e}))
            .collect();
        let payload = serde_json::json!({
            "challenge_id": challenge_id,
            "verdict_detail": detail,
            "testcases": tc_json,
        });
        let plaintext = serde_json::to_vec(&payload).unwrap();

        let key = key_material::reconstruct_key();
        let cipher = Aes256Gcm::new_from_slice(key.as_ref()).unwrap();
        let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
        let ciphertext = cipher.encrypt(&nonce, plaintext.as_slice()).unwrap();

        let mut data = Vec::new();
        data.extend_from_slice(crypto::MAGIC);
        data.push(crypto::VERSION);
        data.extend_from_slice(nonce.as_slice());
        data.extend_from_slice(&ciphertext);

        pool::load_pool(challenge_id, &data).unwrap();
        let (sid, _, _) = pool::select_testcases(challenge_id, testcases.len()).unwrap();
        sid
    }

    #[test]
    fn correct_answer_ac() {
        let sid = setup_pool("judge_ac", "hidden", &[("in\n", "HELLO")]);
        let results = vec![StudentResult {
            stdout: "HELLO\n".to_string(),
            error: None,
            elapsed_ms: 10.0,
            timed_out: false,
        }];
        let verdicts = judge("judge_ac", &sid, results).unwrap();
        assert_eq!(verdicts.len(), 1);
        assert_eq!(verdicts[0].verdict, "AC");
        assert!(verdicts[0].actual.is_none()); // hidden mode
        assert!(verdicts[0].expected.is_none());
    }

    #[test]
    fn wrong_answer_wa_full() {
        let sid = setup_pool("judge_wa", "full", &[("in\n", "HELLO")]);
        let results = vec![StudentResult {
            stdout: "WRONG".to_string(),
            error: None,
            elapsed_ms: 10.0,
            timed_out: false,
        }];
        let verdicts = judge("judge_wa", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "WA");
        assert_eq!(verdicts[0].actual.as_deref(), Some("WRONG"));
        assert_eq!(verdicts[0].expected.as_deref(), Some("HELLO"));
    }

    #[test]
    fn runtime_error_re() {
        let sid = setup_pool("judge_re", "full", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: String::new(),
            error: Some("NameError: x".to_string()),
            elapsed_ms: 5.0,
            timed_out: false,
        }];
        let verdicts = judge("judge_re", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "RE");
        assert!(verdicts[0].error.is_some());
    }

    #[test]
    fn session_invalidated_after_judge() {
        let sid = setup_pool("judge_inval", "hidden", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: "out".to_string(),
            error: None,
            elapsed_ms: 1.0,
            timed_out: false,
        }];
        judge("judge_inval", &sid, results).unwrap();
        // Second call should fail
        let err = judge(
            "judge_inval",
            &sid,
            vec![StudentResult {
                stdout: "out".to_string(),
                error: None,
                elapsed_ms: 1.0,
                timed_out: false,
            }],
        )
        .unwrap_err();
        assert!(err.contains("Invalid session"));
    }

    #[test]
    fn hidden_mode_strips_both() {
        let sid = setup_pool("judge_hidden", "hidden", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: "wrong".to_string(),
            error: None,
            elapsed_ms: 1.0,
            timed_out: false,
        }];
        let verdicts = judge("judge_hidden", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "WA");
        assert!(verdicts[0].actual.is_none());
        assert!(verdicts[0].expected.is_none());
    }

    #[test]
    fn actual_mode_strips_expected() {
        let sid = setup_pool("judge_actual", "actual", &[("in\n", "expected_val")]);
        let results = vec![StudentResult {
            stdout: "wrong".to_string(),
            error: None,
            elapsed_ms: 1.0,
            timed_out: false,
        }];
        let verdicts = judge("judge_actual", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "WA");
        assert_eq!(verdicts[0].actual.as_deref(), Some("wrong"));
        assert!(verdicts[0].expected.is_none());
    }

    #[test]
    fn constant_time_eq_works() {
        assert!(super::constant_time_eq(b"hello", b"hello"));
        assert!(!super::constant_time_eq(b"hello", b"world"));
        assert!(!super::constant_time_eq(b"hello", b"hell"));
    }

    #[test]
    fn timed_out_produces_tle() {
        let sid = setup_pool("judge_tle", "hidden", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: String::new(),
            error: None,
            elapsed_ms: 4000.0,
            timed_out: true,
        }];
        let verdicts = judge("judge_tle", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "TLE");
    }

    #[test]
    fn tle_carries_no_error_even_when_input_has_one() {
        let sid = setup_pool("judge_tle_noerr", "full", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: String::new(),
            error: Some("TimeoutError: Operation limit exceeded (10000000 ops)".to_string()),
            elapsed_ms: 4000.0,
            timed_out: true,
        }];
        let verdicts = judge("judge_tle_noerr", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "TLE");
        assert!(verdicts[0].error.is_none());
    }

    #[test]
    fn missing_timed_out_deserializes_false_and_keeps_legacy_behavior() {
        // The wire format is what matters for backward compatibility: an
        // object without `timed_out` must deserialize to false and judge
        // exactly as before (error → RE with message preserved).
        let legacy: StudentResult =
            serde_json::from_str(r#"{"stdout":"","error":"NameError: x","elapsed_ms":5.0}"#)
                .unwrap();
        assert!(!legacy.timed_out);

        let sid = setup_pool("judge_legacy", "hidden", &[("in\n", "out")]);
        let verdicts = judge("judge_legacy", &sid, vec![legacy]).unwrap();
        assert_eq!(verdicts[0].verdict, "RE");
        assert_eq!(verdicts[0].error.as_deref(), Some("NameError: x"));
    }

    #[test]
    fn timed_out_takes_precedence_over_error() {
        let sid = setup_pool("judge_tle_prec", "hidden", &[("in\n", "out")]);
        let results = vec![StudentResult {
            stdout: String::new(),
            error: Some("anything".to_string()),
            elapsed_ms: 1.0,
            timed_out: true,
        }];
        let verdicts = judge("judge_tle_prec", &sid, results).unwrap();
        assert_eq!(verdicts[0].verdict, "TLE");
        assert!(verdicts[0].error.is_none());
    }
}
