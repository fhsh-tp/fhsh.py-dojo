//! Conformance test for the Rust random-input generator.
//!
//! Mirrors `scripts/generator-parity.test.ts` on the Rust side: for a shared
//! set of ParamSpec fixtures, assert every generated value satisfies the
//! declared constraints (charset, length range, value range, count, separator,
//! multiple_of). Rust `SmallRng` and Python `random` differ, so we assert
//! constraint conformance — not byte-identical output.

use rand::SeedableRng;
use rand::rngs::SmallRng;
use testcase_generator::{generate_input, parse_params};

const N: usize = 200;

/// Generate `N` single-line samples for a one-parameter spec, each with a
/// distinct seed so we exercise a spread of values.
fn samples(json: &str) -> Vec<String> {
    let params = parse_params(json).expect("params should parse");
    (0..N)
        .map(|i| generate_input(&params, &mut SmallRng::seed_from_u64(i as u64)))
        .collect()
}

#[test]
fn int_within_range() {
    for v in samples(r#"{"x":{"type":"int","min":5,"max":20}}"#) {
        let n: i64 = v.trim().parse().unwrap_or_else(|_| panic!("not an int: {v:?}"));
        assert!((5..=20).contains(&n), "int {n} out of [5,20]");
    }
}

#[test]
fn int_fixed_when_min_eq_max() {
    for v in samples(r#"{"x":{"type":"int","min":7,"max":7}}"#) {
        assert_eq!(v.trim(), "7");
    }
}

#[test]
fn alpha_upper_charset_and_length() {
    for v in samples(r#"{"x":{"type":"alpha_upper","min_len":3,"max_len":6}}"#) {
        let s = v.trim();
        assert!((3..=6).contains(&s.len()), "len {} out of [3,6]", s.len());
        assert!(s.chars().all(|c| c.is_ascii_uppercase()), "non A-Z in {s:?}");
    }
}

#[test]
fn alpha_lower_charset_and_length() {
    for v in samples(r#"{"x":{"type":"alpha_lower","min_len":3,"max_len":6}}"#) {
        let s = v.trim();
        assert!((3..=6).contains(&s.len()));
        assert!(s.chars().all(|c| c.is_ascii_lowercase()), "non a-z in {s:?}");
    }
}

#[test]
fn alpha_mixed_charset_and_length() {
    for v in samples(r#"{"x":{"type":"alpha_mixed","min_len":3,"max_len":6}}"#) {
        let s = v.trim();
        assert!((3..=6).contains(&s.len()));
        assert!(s.chars().all(|c| c.is_ascii_alphabetic()), "non A-Za-z in {s:?}");
    }
}

#[test]
fn hex_string_charset_and_length() {
    for v in samples(r#"{"x":{"type":"hex_string","min_len":4,"max_len":8}}"#) {
        let s = v.trim();
        assert!((4..=8).contains(&s.len()));
        assert!(
            s.chars().all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase()),
            "non 0-9a-f in {s:?}"
        );
    }
}

#[test]
fn printable_ascii_charset_and_length() {
    for v in samples(r#"{"x":{"type":"printable_ascii","min_len":3,"max_len":6}}"#) {
        let s = v.trim();
        assert!((3..=6).contains(&s.len()));
        assert!(
            s.bytes().all(|b| (0x21..0x7f).contains(&b)),
            "non-printable in {s:?}"
        );
    }
}

#[test]
fn enum_picks_declared_values() {
    let allowed = ["red", "green", "blue"];
    for v in samples(r#"{"x":{"type":"enum","values":["red","green","blue"]}}"#) {
        assert!(allowed.contains(&v.trim()), "unexpected enum value {v:?}");
    }
}

#[test]
fn hex_string_multiple_of_length() {
    for v in samples(r#"{"x":{"type":"hex_string","min_len":4,"max_len":12,"multiple_of":4}}"#) {
        let s = v.trim();
        assert!((4..=12).contains(&s.len()));
        assert_eq!(s.len() % 4, 0, "len {} not a multiple of 4", s.len());
        assert!(s.chars().all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase()));
    }
}

#[test]
fn int_count_produces_separated_values() {
    for v in samples(r#"{"x":{"type":"int","min":1,"max":100,"count":{"min":3,"max":5,"separator":" "}}}"#) {
        let parts: Vec<&str> = v.trim().split(' ').collect();
        assert!((3..=5).contains(&parts.len()), "count {} out of [3,5]", parts.len());
        for p in parts {
            let n: i64 = p.parse().unwrap_or_else(|_| panic!("not an int: {p:?}"));
            assert!((1..=100).contains(&n), "int {n} out of [1,100]");
        }
    }
}

// ── Group / count.from / seed / budget conformance (upgrade-testcase-engine) ──

/// Competition-shape spec: first line t, then t repetitions of
/// "n on one line, then n lines of ints".
const DEQUE_PARAMS: &str = r#"{
    "t": {"type": "int", "min": 1, "max": 4},
    "cases": {"type": "group", "repeat": "t", "params": {
        "n": {"type": "int", "min": 0, "max": 6},
        "nums": {"type": "int", "min": -999, "max": 999, "count": {"from": "n", "separator": "\n"}}
    }}
}"#;

#[test]
fn group_competition_shape_conforms() {
    let params = parse_params(DEQUE_PARAMS).expect("deque-shape params should parse");
    for i in 0..N {
        let input = generate_input(&params, &mut SmallRng::seed_from_u64(i as u64));
        let lines: Vec<&str> = input.split('\n').collect();
        let t: usize = lines[0].parse().expect("first line is t");
        assert!((1..=4).contains(&t));
        let mut idx = 1;
        for _ in 0..t {
            let n: usize = lines[idx].parse().expect("case header is n");
            assert!(n <= 6);
            idx += 1;
            for _ in 0..n {
                let v: i64 = lines[idx].parse().expect("data line is int");
                assert!((-999..=999).contains(&v));
                idx += 1;
            }
        }
        assert_eq!(idx, lines.len(), "seed={i}: no trailing lines allowed");
    }
}

#[test]
fn count_from_line_count_tracks_reference() {
    let json = r#"{
        "n": {"type": "int", "min": 0, "max": 9},
        "xs": {"type": "int", "min": 1, "max": 5, "count": {"from": "n", "separator": " "}}
    }"#;
    let params = parse_params(json).expect("linked params should parse");
    for i in 0..N {
        let input = generate_input(&params, &mut SmallRng::seed_from_u64(i as u64));
        let lines: Vec<&str> = input.split('\n').collect();
        let n: usize = lines[0].parse().unwrap();
        if n == 0 {
            assert_eq!(lines.len(), 1, "seed={i}: n=0 must contribute no data line");
        } else {
            assert_eq!(lines.len(), 2, "seed={i}");
            assert_eq!(lines[1].split(' ').count(), n, "seed={i}: value count must equal n");
        }
    }
}

#[test]
fn seeded_pool_inputs_are_deterministic() {
    let spec = format!(r#"{{"seed": "conformance", "params": {}}}"#, DEQUE_PARAMS);
    let a = testcase_generator::pool_inputs_from_spec(&spec, 20).unwrap();
    let b = testcase_generator::pool_inputs_from_spec(&spec, 20).unwrap();
    assert_eq!(a, b);
}

#[test]
fn budget_violation_is_readable_error() {
    let spec = r#"{"params": {"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 1, "max": 5000}}}}"#;
    let err = testcase_generator::pool_inputs_from_spec(spec, 1).unwrap_err();
    assert!(err.contains("input budget"), "got: {err}");
}

#[test]
fn invalid_reference_is_parse_error_not_panic() {
    // Forward reference — must be a readable Err, never a panic.
    let json = r#"{
        "cases": {"type": "group", "repeat": "t", "params": {"x": {"type": "int"}}},
        "t": {"type": "int", "min": 1, "max": 2}
    }"#;
    let err = parse_params(json).unwrap_err();
    assert!(err.contains("previously-declared"), "got: {err}");
}
