/// Pool management: decrypt, store, and select testcases.
///
/// Each pool is loaded from an encrypted binary file, decrypted in WASM
/// linear memory, and stored indexed by challenge_id. Testcases are
/// selected into sessions which track indices for judging.
use std::collections::HashMap;
use std::sync::Mutex;

use rand::rngs::SmallRng;
use rand::seq::SliceRandom;
use rand::Rng;
use rand::SeedableRng;
use serde::Deserialize;
use zeroize::Zeroizing;

use crate::crypto;

/// Verdict detail mode (read from encrypted pool payload).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum VerdictDetail {
    Hidden,
    Actual,
    Full,
}

/// A single precomputed testcase.
#[derive(Debug, Clone, Deserialize)]
pub struct Testcase {
    pub input: String,
    pub expected_output: String,
}

/// The decrypted pool payload.
#[derive(Debug, Deserialize)]
struct PoolPayload {
    challenge_id: String,
    verdict_detail: VerdictDetail,
    testcases: Vec<Testcase>,
    /// Present only for `testcase_plan` challenges: the pool then consists of
    /// consecutive blocks of this size and selection returns one whole block
    /// in stored order. Absent (None) for all pre-plan pools — their
    /// behavior is unchanged.
    #[serde(default)]
    plan_block_size: Option<usize>,
}

/// In-memory representation of a loaded pool.
pub struct LoadedPool {
    pub verdict_detail: VerdictDetail,
    pub testcases: Vec<Testcase>,
    pub plan_block_size: Option<usize>,
}

/// A session created by `select_testcases`.
pub struct Session {
    pub challenge_id: String,
    pub verdict_detail: VerdictDetail,
    /// The selected testcases (cloned from pool).
    pub testcases: Vec<Testcase>,
}

/// Global state: loaded pools and active sessions.
static STATE: Mutex<Option<PoolState>> = Mutex::new(None);

struct PoolState {
    pools: HashMap<String, LoadedPool>,
    sessions: HashMap<String, Session>,
    session_counter: u64,
}

impl PoolState {
    fn new() -> Self {
        Self {
            pools: HashMap::new(),
            sessions: HashMap::new(),
            session_counter: 0,
        }
    }
}

fn with_state<F, R>(f: F) -> R
where
    F: FnOnce(&mut PoolState) -> R,
{
    let mut guard = STATE.lock().unwrap();
    let state = guard.get_or_insert_with(PoolState::new);
    f(state)
}

/// Load and decrypt a pool from its encrypted binary data.
pub fn load_pool(challenge_id: &str, encrypted_data: &[u8]) -> Result<(), String> {
    let plaintext: Zeroizing<Vec<u8>> = crypto::decrypt_pool(encrypted_data)?;
    let payload: PoolPayload =
        serde_json::from_slice(&plaintext).map_err(|e| format!("Pool JSON parse error: {e}"))?;

    if payload.challenge_id != challenge_id {
        return Err(format!(
            "Pool identity mismatch: expected \"{challenge_id}\", got \"{}\"",
            payload.challenge_id
        ));
    }

    let loaded = LoadedPool {
        verdict_detail: payload.verdict_detail,
        testcases: payload.testcases,
        plan_block_size: payload.plan_block_size,
    };

    with_state(|state| {
        state.pools.insert(challenge_id.to_string(), loaded);
    });

    Ok(())
}

/// Select `count` random testcases from a loaded pool.
/// Returns `(session_id, inputs, verdict_detail)` — inputs only, no expected outputs.
pub fn select_testcases(
    challenge_id: &str,
    count: usize,
) -> Result<(String, Vec<String>, VerdictDetail), String> {
    with_state(|state| {
        let pool = state
            .pools
            .get(challenge_id)
            .ok_or_else(|| format!("Pool not loaded for challenge: {challenge_id}"))?;

        if count > pool.testcases.len() {
            return Err(format!(
                "Requested {count} testcases but pool only has {}",
                pool.testcases.len()
            ));
        }

        let mut rng = SmallRng::from_entropy();
        let selected: Vec<Testcase> = match pool.plan_block_size {
            // testcase_plan pool: pick one whole block uniformly at random and
            // return it in stored order (declaration order). Every structural
            // assumption is checked loudly — a malformed pool must never
            // yield a partial or reordered block.
            Some(k) => {
                if k == 0 {
                    return Err("Pool plan_block_size must be >= 1".to_string());
                }
                if pool.testcases.len() % k != 0 || pool.testcases.is_empty() {
                    return Err(format!(
                        "Pool has {} testcases, not a positive multiple of plan_block_size {k}",
                        pool.testcases.len()
                    ));
                }
                if count != k {
                    return Err(format!(
                        "Plan pool requires exactly {k} testcases per session, requested {count}"
                    ));
                }
                let block_count = pool.testcases.len() / k;
                let block = rng.gen_range(0..block_count);
                pool.testcases[block * k..(block + 1) * k].to_vec()
            }
            // Non-plan pool: existing uniform shuffle-and-truncate selection.
            None => {
                let mut indices: Vec<usize> = (0..pool.testcases.len()).collect();
                indices.shuffle(&mut rng);
                indices.truncate(count);
                indices.iter().map(|&i| pool.testcases[i].clone()).collect()
            }
        };
        let inputs: Vec<String> = selected.iter().map(|tc| tc.input.clone()).collect();

        state.session_counter += 1;
        let session_id = format!("s_{}", state.session_counter);

        let session = Session {
            challenge_id: challenge_id.to_string(),
            verdict_detail: pool.verdict_detail,
            testcases: selected,
        };
        state.sessions.insert(session_id.clone(), session);

        let verdict_detail = pool.verdict_detail;

        Ok((session_id, inputs, verdict_detail))
    })
}

/// Get expected output for a specific testcase in a session.
/// Returns `None` if verdict_detail is not `full`.
pub fn get_expected(
    challenge_id: &str,
    session_id: &str,
    index: usize,
) -> Result<Option<String>, String> {
    with_state(|state| {
        let session = state
            .sessions
            .get(session_id)
            .ok_or_else(|| format!("Invalid session: {session_id}"))?;

        if session.challenge_id != challenge_id {
            return Err(format!(
                "Session {session_id} belongs to {}, not {challenge_id}",
                session.challenge_id
            ));
        }

        if index >= session.testcases.len() {
            return Err(format!(
                "Index {index} out of range (session has {} testcases)",
                session.testcases.len()
            ));
        }

        Ok(match session.verdict_detail {
            VerdictDetail::Full => Some(session.testcases[index].expected_output.clone()),
            _ => None,
        })
    })
}

/// Take a session out of state (consume it), returning its data.
/// The session is removed from state and cannot be used again.
pub fn take_session(
    challenge_id: &str,
    session_id: &str,
) -> Result<(VerdictDetail, Vec<Testcase>), String> {
    with_state(|state| {
        let session = state
            .sessions
            .remove(session_id)
            .ok_or_else(|| format!("Invalid session: {session_id}"))?;

        if session.challenge_id != challenge_id {
            // Put it back if challenge_id doesn't match
            state.sessions.insert(session_id.to_string(), session);
            return Err(format!(
                "Session {session_id} belongs to a different challenge, not {challenge_id}",
            ));
        }

        Ok((session.verdict_detail, session.testcases))
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::key_material;
    use aes_gcm::aead::OsRng;
    use aes_gcm::{AeadCore, Aes256Gcm, KeyInit};
    use aes_gcm::aead::Aead;

    fn make_encrypted_pool_with_id(challenge_id: &str, verdict_detail: &str, testcases: &[(&str, &str)]) -> Vec<u8> {
        let tc_json: Vec<serde_json::Value> = testcases
            .iter()
            .map(|(i, e)| {
                serde_json::json!({
                    "input": i,
                    "expected_output": e,
                })
            })
            .collect();
        let payload = serde_json::json!({
            "challenge_id": challenge_id,
            "verdict_detail": verdict_detail,
            "testcases": tc_json,
        });
        let plaintext = serde_json::to_vec(&payload).unwrap();

        let key = key_material::reconstruct_key();
        let cipher = Aes256Gcm::new_from_slice(key.as_ref()).unwrap();
        let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
        let ciphertext = cipher.encrypt(&nonce, plaintext.as_slice()).unwrap();

        let mut out = Vec::new();
        out.extend_from_slice(crypto::MAGIC);
        out.push(crypto::VERSION);
        out.extend_from_slice(nonce.as_slice());
        out.extend_from_slice(&ciphertext);
        out
    }

    fn make_encrypted_pool(verdict_detail: &str, testcases: &[(&str, &str)]) -> Vec<u8> {
        make_encrypted_pool_with_id("test", verdict_detail, testcases)
    }

    /// Like `make_encrypted_pool_with_id` but with `plan_block_size` in the
    /// payload, for testcase_plan pool tests.
    fn make_encrypted_plan_pool(
        challenge_id: &str,
        plan_block_size: usize,
        testcases: &[(&str, &str)],
    ) -> Vec<u8> {
        let tc_json: Vec<serde_json::Value> = testcases
            .iter()
            .map(|(i, e)| serde_json::json!({ "input": i, "expected_output": e }))
            .collect();
        let payload = serde_json::json!({
            "challenge_id": challenge_id,
            "verdict_detail": "hidden",
            "testcases": tc_json,
            "plan_block_size": plan_block_size,
        });
        let plaintext = serde_json::to_vec(&payload).unwrap();

        let key = key_material::reconstruct_key();
        let cipher = Aes256Gcm::new_from_slice(key.as_ref()).unwrap();
        let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
        let ciphertext = cipher.encrypt(&nonce, plaintext.as_slice()).unwrap();

        let mut out = Vec::new();
        out.extend_from_slice(crypto::MAGIC);
        out.push(crypto::VERSION);
        out.extend_from_slice(nonce.as_slice());
        out.extend_from_slice(&ciphertext);
        out
    }

    /// 4 blocks × 2: inputs are labeled so a returned pair identifies its
    /// block and in-block position unambiguously.
    fn plan_pool_fixture(challenge_id: &str) -> Vec<u8> {
        make_encrypted_plan_pool(
            challenge_id,
            2,
            &[
                ("b0-first", "o"), ("b0-second", "o"),
                ("b1-first", "o"), ("b1-second", "o"),
                ("b2-first", "o"), ("b2-second", "o"),
                ("b3-first", "o"), ("b3-second", "o"),
            ],
        )
    }

    #[test]
    fn plan_pool_returns_one_ordered_block() {
        load_pool("plan_ordered", &plan_pool_fixture("plan_ordered")).unwrap();
        for _ in 0..20 {
            let (_sid, inputs, _) = select_testcases("plan_ordered", 2).unwrap();
            assert_eq!(inputs.len(), 2);
            let block = inputs[0].strip_suffix("-first").expect("first slot must be a block head");
            assert_eq!(inputs[1], format!("{block}-second"), "block must stay in stored order");
        }
    }

    #[test]
    fn plan_pool_count_mismatch_is_refused() {
        load_pool("plan_mismatch", &plan_pool_fixture("plan_mismatch")).unwrap();
        let err = select_testcases("plan_mismatch", 4).unwrap_err();
        assert!(err.contains("exactly 2"), "got: {err}");
    }

    #[test]
    fn plan_pool_non_multiple_length_is_refused() {
        // 5 testcases with block size 2 — corrupt structure must be refused.
        let data = make_encrypted_plan_pool(
            "plan_corrupt",
            2,
            &[("a", "o"), ("b", "o"), ("c", "o"), ("d", "o"), ("e", "o")],
        );
        load_pool("plan_corrupt", &data).unwrap();
        let err = select_testcases("plan_corrupt", 2).unwrap_err();
        assert!(err.contains("multiple of plan_block_size"), "got: {err}");
    }

    #[test]
    fn plan_pool_zero_block_size_is_refused() {
        let data = make_encrypted_plan_pool("plan_zero", 0, &[("a", "o")]);
        load_pool("plan_zero", &data).unwrap();
        let err = select_testcases("plan_zero", 1).unwrap_err();
        assert!(err.contains(">= 1"), "got: {err}");
    }

    #[test]
    fn load_and_select() {
        let data = make_encrypted_pool("hidden", &[
            ("A\n1\n", "B"),
            ("C\n2\n", "D"),
            ("E\n3\n", "F"),
        ]);
        load_pool("test", &data).unwrap();
        let (session_id, inputs, _) = select_testcases("test", 2).unwrap();
        assert_eq!(inputs.len(), 2);
        assert!(!session_id.is_empty());
    }

    #[test]
    fn get_expected_hidden_returns_none() {
        let data = make_encrypted_pool_with_id("test_hidden", "hidden", &[("in", "out")]);
        load_pool("test_hidden", &data).unwrap();
        let (sid, _, _) = select_testcases("test_hidden", 1).unwrap();
        let result = get_expected("test_hidden", &sid, 0).unwrap();
        assert!(result.is_none());
    }

    #[test]
    fn get_expected_full_returns_value() {
        let data = make_encrypted_pool_with_id("test_full", "full", &[("in", "expected_val")]);
        load_pool("test_full", &data).unwrap();
        let (sid, _, _) = select_testcases("test_full", 1).unwrap();
        let result = get_expected("test_full", &sid, 0).unwrap();
        assert_eq!(result, Some("expected_val".to_string()));
    }

    #[test]
    fn pool_not_loaded_error() {
        let err = select_testcases("nonexistent", 1).unwrap_err();
        assert!(err.contains("not loaded"));
    }

    #[test]
    fn session_consumed_by_take() {
        let data = make_encrypted_pool_with_id("test_take", "full", &[("in", "out")]);
        load_pool("test_take", &data).unwrap();
        let (sid, _, _) = select_testcases("test_take", 1).unwrap();
        let (detail, tcs) = take_session("test_take", &sid).unwrap();
        assert_eq!(detail, VerdictDetail::Full);
        assert_eq!(tcs.len(), 1);
        // Session is now consumed
        let err = get_expected("test_take", &sid, 0).unwrap_err();
        assert!(err.contains("Invalid session"));
    }

    #[test]
    fn select_returns_verdict_detail() {
        // Hidden
        let data = make_encrypted_pool_with_id("test_vd_hidden", "hidden", &[("in1\n", "out1")]);
        load_pool("test_vd_hidden", &data).unwrap();
        let (_session_id, _inputs, vd) = select_testcases("test_vd_hidden", 1).unwrap();
        assert_eq!(vd, VerdictDetail::Hidden);

        // Actual
        let data = make_encrypted_pool_with_id("test_vd_actual", "actual", &[("in2\n", "out2")]);
        load_pool("test_vd_actual", &data).unwrap();
        let (_session_id, _inputs, vd) = select_testcases("test_vd_actual", 1).unwrap();
        assert_eq!(vd, VerdictDetail::Actual);

        // Full
        let data = make_encrypted_pool_with_id("test_vd_full", "full", &[("in3\n", "out3")]);
        load_pool("test_vd_full", &data).unwrap();
        let (_session_id, _inputs, vd) = select_testcases("test_vd_full", 1).unwrap();
        assert_eq!(vd, VerdictDetail::Full);
    }

    #[test]
    fn mismatched_challenge_id_rejected() {
        // Pool payload has challenge_id "foo", but we load with "bar"
        let data = make_encrypted_pool_with_id("foo", "hidden", &[("in", "out")]);
        let err = load_pool("bar", &data).unwrap_err();
        assert!(
            err.contains("identity mismatch") || err.contains("mismatch"),
            "Expected identity mismatch error, got: {err}"
        );
    }

    #[test]
    fn matching_challenge_id_loads_successfully() {
        // Pool payload has challenge_id "same_id", load with "same_id" — should succeed
        let data = make_encrypted_pool_with_id("same_id", "hidden", &[("in", "out")]);
        load_pool("same_id", &data).unwrap();
        let (sid, inputs, _) = select_testcases("same_id", 1).unwrap();
        assert_eq!(inputs.len(), 1);
        assert!(!sid.is_empty());
    }
}
