use indexmap::IndexMap;
use rand::Rng;
use std::collections::HashMap;

#[cfg(feature = "faker")]
use fake::Fake;
#[cfg(feature = "faker")]
use crate::parser::FakerCategory;

use crate::parser::ParamSpec;

const UPPER: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const LOWER: &[u8] = b"abcdefghijklmnopqrstuvwxyz";
const HEX_CHARS: &[u8] = b"0123456789abcdef";
const PRINTABLE_ASCII: &[u8] = b"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

/// Generate a single stdin input string from ordered params.
///
/// Rendering contract: each param renders as one block in declaration
/// order, blocks joined with '\n'. A scalar param renders one line; a
/// param with count > 1 joins its values with the declared separator (a
/// separator of '\n' therefore spans multiple lines). A group renders its
/// inner params once per repetition, repetitions joined with '\n'; a group
/// whose repeat count resolves to 0 contributes no lines at all, and a
/// linked-mode (`count.from`) param whose resolved count is 0 likewise
/// omits its block entirely — "N=0 means zero data lines", never a stray
/// empty line. Range-mode counts keep their (possibly empty) line for
/// backward compatibility.
///
/// Cross-param state: scalar int values are recorded as they are generated
/// so that later `count.from` / group `repeat` references (validated at
/// parse time) resolve against them. Each group repetition gets its own
/// local scope, falling back to top-level values.
pub fn generate_input<R: Rng>(specs: &IndexMap<String, ParamSpec>, rng: &mut R) -> String {
    let mut top: HashMap<String, i64> = HashMap::new();
    let empty: HashMap<String, i64> = HashMap::new();
    let mut blocks: Vec<String> = Vec::new();

    for (name, spec) in specs {
        match spec {
            ParamSpec::Group { repeat, params } => {
                let reps = lookup_ref(repeat, &top, &empty);
                if reps == 0 {
                    continue; // zero repetitions: the group contributes no lines
                }
                let mut rep_blocks = Vec::with_capacity(reps);
                for _ in 0..reps {
                    let mut local: HashMap<String, i64> = HashMap::new();
                    let mut inner_blocks = Vec::with_capacity(params.len());
                    for (iname, ispec) in params {
                        if let Some(block) = generate_block(iname, ispec, rng, &mut local, &top) {
                            inner_blocks.push(block);
                        }
                    }
                    rep_blocks.push(inner_blocks.join("\n"));
                }
                blocks.push(rep_blocks.join("\n"));
            }
            _ => {
                if let Some(block) = generate_block(name, spec, rng, &mut top, &empty) {
                    blocks.push(block);
                }
            }
        }
    }

    blocks.join("\n")
}

/// Resolve a `count.from` / `repeat` reference: group-local scope first,
/// then the enclosing top-level scope. Parse-time validation guarantees the
/// referenced value exists and is non-negative.
fn lookup_ref(name: &str, local: &HashMap<String, i64>, outer: &HashMap<String, i64>) -> usize {
    let v = local
        .get(name)
        .or_else(|| outer.get(name))
        .copied()
        .expect("reference target validated at parse time");
    v.max(0) as usize
}

/// Render one param block, recording scalar int values into the current
/// scope so later references in the same scope can resolve them.
/// Returns `None` when a linked-mode count resolves to 0 — the block is
/// omitted entirely instead of leaving a stray empty line.
fn generate_block<R: Rng>(
    name: &str,
    spec: &ParamSpec,
    rng: &mut R,
    local: &mut HashMap<String, i64>,
    outer: &HashMap<String, i64>,
) -> Option<String> {
    if let ParamSpec::Int { min, max, count } = spec
        && count.from.is_none()
        && count.min == 1
        && count.max == 1
    {
        let v = rng.gen_range(*min..=*max);
        local.insert(name.to_string(), v);
        return Some(v.to_string());
    }
    if let Some(target) = linked_from(spec)
        && lookup_ref(target, local, outer) == 0
    {
        return None;
    }
    Some(generate_one_scoped(spec, rng, local, outer))
}

/// The `count.from` target of a spec, if it uses linked mode.
fn linked_from(spec: &ParamSpec) -> Option<&str> {
    let count = match spec {
        ParamSpec::Int { count, .. } => count,
        ParamSpec::AlphaUpper { count, .. } => count,
        ParamSpec::AlphaLower { count, .. } => count,
        ParamSpec::AlphaMixed { count, .. } => count,
        ParamSpec::HexString { count, .. } => count,
        ParamSpec::PrintableAscii { count, .. } => count,
        ParamSpec::Enum { count, .. } => count,
        ParamSpec::Group { .. } => return None,
        #[cfg(feature = "faker")]
        ParamSpec::Faker { count, .. } => count,
    };
    count.from.as_deref()
}

fn generate_one_scoped<R: Rng>(
    spec: &ParamSpec,
    rng: &mut R,
    local: &HashMap<String, i64>,
    outer: &HashMap<String, i64>,
) -> String {
    let count_spec = match spec {
        ParamSpec::Int { count, .. } => count,
        ParamSpec::AlphaUpper { count, .. } => count,
        ParamSpec::AlphaLower { count, .. } => count,
        ParamSpec::AlphaMixed { count, .. } => count,
        ParamSpec::HexString { count, .. } => count,
        ParamSpec::PrintableAscii { count, .. } => count,
        ParamSpec::Enum { count, .. } => count,
        ParamSpec::Group { .. } => {
            unreachable!("groups render structurally in generate_input; nesting is rejected at parse time")
        }
        #[cfg(feature = "faker")]
        ParamSpec::Faker { count, .. } => count,
    };

    let actual_count = match &count_spec.from {
        Some(target) => lookup_ref(target, local, outer),
        None => {
            debug_assert!(count_spec.min <= count_spec.max, "CountSpec.min must be <= max");
            rng.gen_range(count_spec.min..=count_spec.max)
        }
    };

    (0..actual_count)
        .map(|_| generate_single(spec, rng))
        .collect::<Vec<_>>()
        .join(&count_spec.separator)
}

/// Pick a random length in [min_len, max_len] that is a multiple of `multiple_of`.
/// If multiple_of is 1 (the default), this is equivalent to gen_range(min..=max).
/// Range validity (lo <= hi) is guaranteed by parse-time validation.
fn random_len<R: Rng>(min_len: usize, max_len: usize, multiple_of: usize, rng: &mut R) -> usize {
    let step = multiple_of.max(1);
    // Smallest multiple of `step` that is >= min_len
    let lo = min_len.div_ceil(step);
    // Largest multiple of `step` that is <= max_len
    let hi = max_len / step;
    debug_assert!(lo <= hi, "no valid length: min_len={min_len}, max_len={max_len}, multiple_of={step}");
    rng.gen_range(lo..=hi) * step
}

/// Produce a single value for the given spec.
fn generate_single<R: Rng>(spec: &ParamSpec, rng: &mut R) -> String {
    match spec {
        ParamSpec::Int { min, max, .. } => rng.gen_range(*min..=*max).to_string(),
        ParamSpec::AlphaUpper { min_len, max_len, multiple_of, .. } => {
            let len = random_len(*min_len, *max_len, *multiple_of, rng);
            (0..len)
                .map(|_| UPPER[rng.gen_range(0..UPPER.len())] as char)
                .collect()
        }
        ParamSpec::AlphaLower { min_len, max_len, multiple_of, .. } => {
            let len = random_len(*min_len, *max_len, *multiple_of, rng);
            (0..len)
                .map(|_| LOWER[rng.gen_range(0..LOWER.len())] as char)
                .collect()
        }
        ParamSpec::AlphaMixed { min_len, max_len, multiple_of, .. } => {
            let combined: Vec<u8> = UPPER.iter().chain(LOWER.iter()).copied().collect();
            let len = random_len(*min_len, *max_len, *multiple_of, rng);
            (0..len)
                .map(|_| combined[rng.gen_range(0..combined.len())] as char)
                .collect()
        }
        ParamSpec::HexString { min_len, max_len, multiple_of, .. } => {
            let len = random_len(*min_len, *max_len, *multiple_of, rng);
            (0..len)
                .map(|_| HEX_CHARS[rng.gen_range(0..HEX_CHARS.len())] as char)
                .collect()
        }
        ParamSpec::PrintableAscii { min_len, max_len, multiple_of, .. } => {
            let len = random_len(*min_len, *max_len, *multiple_of, rng);
            (0..len)
                .map(|_| PRINTABLE_ASCII[rng.gen_range(0..PRINTABLE_ASCII.len())] as char)
                .collect()
        }
        ParamSpec::Enum { values, .. } => {
            values[rng.gen_range(0..values.len())].clone()
        }
        ParamSpec::Group { .. } => {
            unreachable!("groups render structurally in generate_input")
        }
        #[cfg(feature = "faker")]
        ParamSpec::Faker { category, .. } => generate_fake(category, rng),
    }
}

#[cfg(feature = "faker")]
fn generate_fake<R: Rng>(category: &FakerCategory, rng: &mut R) -> String {
    use fake::faker::{
        name::en::{Name, FirstName, LastName},
        internet::en::SafeEmail,
        company::en::CompanyName,
        address::en::{CityName, CountryName},
    };
    match category {
        FakerCategory::Name => Name().fake_with_rng(rng),
        FakerCategory::FirstName => FirstName().fake_with_rng(rng),
        FakerCategory::LastName => LastName().fake_with_rng(rng),
        FakerCategory::Email => SafeEmail().fake_with_rng(rng),
        FakerCategory::Company => CompanyName().fake_with_rng(rng),
        FakerCategory::City => CityName().fake_with_rng(rng),
        FakerCategory::Country => CountryName().fake_with_rng(rng),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parser::CountSpec;
    use rand::SeedableRng;
    use rand::rngs::SmallRng;

    fn seeded() -> SmallRng {
        SmallRng::seed_from_u64(42)
    }

    fn make_params(pairs: &[(&str, ParamSpec)]) -> IndexMap<String, ParamSpec> {
        pairs.iter().map(|(k, v)| (k.to_string(), v.clone())).collect()
    }

    /// Test-only shim preserving the old 2-arg generate_one shape for specs
    /// that use no cross-param references.
    fn generate_one<R: Rng>(spec: &ParamSpec, rng: &mut R) -> String {
        let empty = HashMap::new();
        generate_one_scoped(spec, rng, &empty, &empty)
    }

    fn fixed_count(n: usize, separator: &str) -> CountSpec {
        CountSpec { min: n, max: n, separator: separator.to_string(), from: None }
    }

    #[test]
    fn int_within_range() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 1, max: 25, count: CountSpec::default() };
        for _ in 0..100 {
            let v: i64 = generate_one(&spec, &mut rng).parse().unwrap();
            assert!((1..=25).contains(&v));
        }
    }

    #[test]
    fn alpha_upper_only_uppercase() {
        let mut rng = seeded();
        let spec = ParamSpec::AlphaUpper { min_len: 5, max_len: 10, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(v.chars().all(|c| c.is_ascii_uppercase()));
        assert!((5..=10).contains(&v.len()));
    }

    #[test]
    fn hex_string_valid_chars() {
        let mut rng = seeded();
        let spec = ParamSpec::HexString { min_len: 4, max_len: 8, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(v.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn deterministic_with_seed() {
        let spec = ParamSpec::Int { min: 0, max: 1000, count: CountSpec::default() };
        let v1 = generate_one(&spec, &mut SmallRng::seed_from_u64(7));
        let v2 = generate_one(&spec, &mut SmallRng::seed_from_u64(7));
        assert_eq!(v1, v2);
    }

    #[test]
    fn alpha_lower_only_lowercase() {
        let mut rng = seeded();
        let spec = ParamSpec::AlphaLower { min_len: 5, max_len: 10, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(v.chars().all(|c| c.is_ascii_lowercase()), "expected all lowercase, got: {v}");
        assert!((5..=10).contains(&v.len()));
    }

    #[test]
    fn alpha_mixed_only_alpha() {
        let mut rng = seeded();
        let spec = ParamSpec::AlphaMixed { min_len: 20, max_len: 30, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(v.chars().all(|c| c.is_ascii_alphabetic()), "expected only alpha chars, got: {v}");
        assert!((20..=30).contains(&v.len()));
    }

    #[test]
    fn alpha_mixed_contains_both_cases() {
        let mut rng = seeded();
        let spec = ParamSpec::AlphaMixed { min_len: 50, max_len: 50, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(v.chars().any(|c| c.is_ascii_uppercase()), "expected at least one uppercase");
        assert!(v.chars().any(|c| c.is_ascii_lowercase()), "expected at least one lowercase");
    }

    #[test]
    fn printable_ascii_valid_chars() {
        let mut rng = seeded();
        let spec = ParamSpec::PrintableAscii { min_len: 20, max_len: 30, multiple_of: 1, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(
            v.chars().all(|c| c as u8 >= 0x21 && c as u8 <= 0x7e),
            "expected printable non-space ASCII (0x21–0x7e), got: {v}"
        );
        assert!((20..=30).contains(&v.len()));
    }

    #[test]
    fn count_greater_than_one_produces_space_separated_values() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 1, max: 100, count: fixed_count(3, " ") };
        let v = generate_one(&spec, &mut rng);
        let parts: Vec<&str> = v.split(' ').collect();
        assert_eq!(parts.len(), 3, "expected 3 space-separated values, got: {v}");
        for part in parts {
            let n: i64 = part.parse().expect("each part should be a valid integer");
            assert!((1..=100).contains(&n));
        }
    }

    #[test]
    fn count_one_produces_no_spaces_for_int() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 0, max: 1000, count: CountSpec::default() };
        let v = generate_one(&spec, &mut rng);
        assert!(!v.contains(' '), "count=1 should produce a single value with no spaces, got: {v}");
    }

    #[test]
    fn generate_input_joins_in_declaration_order() {
        let params = make_params(&[
            ("plaintext", ParamSpec::AlphaUpper { min_len: 5, max_len: 5, multiple_of: 1, count: CountSpec::default() }),
            ("shift", ParamSpec::Int { min: 3, max: 3, count: CountSpec::default() }),
        ]);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        let lines: Vec<&str> = input.lines().collect();
        assert_eq!(lines.len(), 2);
        assert!(lines[0].chars().all(|c| c.is_ascii_uppercase()), "first line should be alpha_upper");
        assert_eq!(lines[1], "3", "second line should be the fixed shift=3");
    }

    #[test]
    fn generate_input_single_param() {
        let params = make_params(&[("n", ParamSpec::Int { min: 42, max: 42, count: CountSpec::default() })]);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        assert_eq!(input, "42");
    }

    #[test]
    fn generate_input_three_params_ordered() {
        let params = make_params(&[
            ("m", ParamSpec::Int { min: 65, max: 65, count: CountSpec::default() }),
            ("e", ParamSpec::Int { min: 17, max: 17, count: CountSpec::default() }),
            ("n", ParamSpec::Int { min: 3233, max: 3233, count: CountSpec::default() }),
        ]);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        assert_eq!(input, "65\n17\n3233");
    }

    #[test]
    fn test_multiple_count_space_separated() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 5, max: 5, count: fixed_count(4, " ") };
        let v = generate_one(&spec, &mut rng);
        assert_eq!(v, "5 5 5 5");
    }

    #[test]
    fn count_spec_variable_count_within_range() {
        let spec = ParamSpec::Int {
            min: 1,
            max: 1,
            count: CountSpec { min: 2, max: 5, separator: " ".to_string(), from: None },
        };
        for seed in 0..200u64 {
            let mut rng = SmallRng::seed_from_u64(seed);
            let v = generate_one(&spec, &mut rng);
            let parts: Vec<&str> = v.split(' ').collect();
            assert!(
                (2..=5).contains(&parts.len()),
                "seed={seed}: expected 2–5 parts, got {} (value: {v})", parts.len()
            );
        }
    }

    #[test]
    fn count_spec_custom_separator_comma() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 7, max: 7, count: fixed_count(3, ",") };
        let v = generate_one(&spec, &mut rng);
        assert_eq!(v, "7,7,7", "expected comma-separated values, got: {v}");
        assert!(!v.contains(' '), "should use comma, not space");
    }

    #[test]
    fn count_spec_custom_separator_no_trailing() {
        let mut rng = seeded();
        let spec = ParamSpec::Int { min: 3, max: 3, count: fixed_count(2, "|") };
        let v = generate_one(&spec, &mut rng);
        assert_eq!(v, "3|3", "expected pipe-separated values without trailing separator");
        assert!(!v.ends_with('|'), "should have no trailing separator");
    }

    #[test]
    fn enum_selects_from_values() {
        let mut rng = seeded();
        let spec = ParamSpec::Enum {
            values: vec!["ECB".to_string(), "CBC".to_string()],
            count: CountSpec::default(),
        };
        for _ in 0..100 {
            let v = generate_one(&spec, &mut rng);
            assert!(v == "ECB" || v == "CBC", "expected ECB or CBC, got: {v}");
        }
    }

    #[test]
    fn enum_with_count_generates_multiple() {
        let mut rng = seeded();
        let spec = ParamSpec::Enum {
            values: vec!["A".to_string(), "B".to_string(), "C".to_string()],
            count: fixed_count(3, ","),
        };
        let v = generate_one(&spec, &mut rng);
        let parts: Vec<&str> = v.split(',').collect();
        assert_eq!(parts.len(), 3, "expected 3 comma-separated values, got: {v}");
        for part in parts {
            assert!(
                part == "A" || part == "B" || part == "C",
                "expected A, B, or C, got: {part}"
            );
        }
    }

    #[test]
    fn hex_string_multiple_of_respects_constraint() {
        let spec = ParamSpec::HexString {
            min_len: 16,
            max_len: 64,
            multiple_of: 16,
            count: CountSpec::default(),
        };
        for seed in 0..200u64 {
            let mut rng = SmallRng::seed_from_u64(seed);
            let v = generate_one(&spec, &mut rng);
            assert!(
                v.len() % 16 == 0,
                "seed={seed}: expected length multiple of 16, got {} (len={})", v, v.len()
            );
            assert!(
                (16..=64).contains(&v.len()),
                "seed={seed}: expected length in [16, 64], got {}", v.len()
            );
        }
    }

    #[test]
    fn multiple_of_1_is_same_as_no_constraint() {
        let spec = ParamSpec::AlphaUpper {
            min_len: 5,
            max_len: 10,
            multiple_of: 1,
            count: CountSpec::default(),
        };
        for seed in 0..50u64 {
            let mut rng = SmallRng::seed_from_u64(seed);
            let v = generate_one(&spec, &mut rng);
            assert!((5..=10).contains(&v.len()));
        }
    }

    #[test]
    fn enum_deterministic_with_seed() {
        let spec = ParamSpec::Enum {
            values: vec!["X".to_string(), "Y".to_string(), "Z".to_string()],
            count: CountSpec::default(),
        };
        let v1 = generate_one(&spec, &mut SmallRng::seed_from_u64(7));
        let v2 = generate_one(&spec, &mut SmallRng::seed_from_u64(7));
        assert_eq!(v1, v2);
    }

    // ── count.from linkage & group rendering ───────────────────────────

    fn deque_shape_params(t_min: i64, t_max: i64, n_min: i64, n_max: i64) -> IndexMap<String, ParamSpec> {
        let mut inner: IndexMap<String, ParamSpec> = IndexMap::new();
        inner.insert("n".to_string(), ParamSpec::Int { min: n_min, max: n_max, count: CountSpec::default() });
        inner.insert("nums".to_string(), ParamSpec::Int {
            min: -999,
            max: 999,
            count: CountSpec { min: 0, max: 0, separator: "\n".to_string(), from: Some("n".to_string()) },
        });
        make_params(&[
            ("t", ParamSpec::Int { min: t_min, max: t_max, count: CountSpec::default() }),
            ("cases", ParamSpec::Group { repeat: "t".to_string(), params: inner }),
        ])
    }

    #[test]
    fn count_from_line_count_matches_generated_value() {
        // Single testcase shape: n then exactly n lines of ints.
        let params = make_params(&[
            ("n", ParamSpec::Int { min: 1, max: 8, count: CountSpec::default() }),
            ("nums", ParamSpec::Int {
                min: -50,
                max: 50,
                count: CountSpec { min: 0, max: 0, separator: "\n".to_string(), from: Some("n".to_string()) },
            }),
        ]);
        for seed in 0..100u64 {
            let mut rng = SmallRng::seed_from_u64(seed);
            let input = generate_input(&params, &mut rng);
            let lines: Vec<&str> = input.split('\n').collect();
            let n: usize = lines[0].parse().unwrap();
            assert_eq!(lines.len(), 1 + n, "seed={seed}: expected 1+{n} lines, got {}", lines.len());
            for line in &lines[1..] {
                let v: i64 = line.parse().unwrap();
                assert!((-50..=50).contains(&v));
            }
        }
    }

    #[test]
    fn group_renders_competition_shape() {
        // First line t, then t repetitions of: one line n, then n lines of ints.
        for seed in 0..100u64 {
            let params = deque_shape_params(1, 4, 0, 5);
            let mut rng = SmallRng::seed_from_u64(seed);
            let input = generate_input(&params, &mut rng);
            let lines: Vec<&str> = input.split('\n').collect();
            let t: usize = lines[0].parse().unwrap();
            let mut idx = 1;
            for case in 0..t {
                let n: usize = lines[idx].parse().unwrap_or_else(|_| {
                    panic!("seed={seed} case={case}: line {idx} should be n, got '{}'", lines[idx])
                });
                idx += 1;
                for _ in 0..n {
                    let v: i64 = lines[idx].parse().unwrap();
                    assert!((-999..=999).contains(&v));
                    idx += 1;
                }
            }
            assert_eq!(idx, lines.len(), "seed={seed}: trailing unparsed lines");
        }
    }

    #[test]
    fn group_repeat_zero_contributes_no_lines() {
        let params = deque_shape_params(0, 0, 1, 3);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        assert_eq!(input, "0", "zero repetitions must leave only the t line, got: {input:?}");
    }

    #[test]
    fn group_local_scope_shadows_outer() {
        // Inner scalar int named the same as an outer one: inner reference
        // must resolve to the group-local value of the CURRENT repetition.
        let mut inner: IndexMap<String, ParamSpec> = IndexMap::new();
        inner.insert("n".to_string(), ParamSpec::Int { min: 2, max: 2, count: CountSpec::default() });
        inner.insert("xs".to_string(), ParamSpec::Int {
            min: 7,
            max: 7,
            count: CountSpec { min: 0, max: 0, separator: " ".to_string(), from: Some("n".to_string()) },
        });
        let params = make_params(&[
            ("n", ParamSpec::Int { min: 9, max: 9, count: CountSpec::default() }),
            ("t", ParamSpec::Int { min: 1, max: 1, count: CountSpec::default() }),
            ("g", ParamSpec::Group { repeat: "t".to_string(), params: inner }),
        ]);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        // outer n=9, t=1, then one repetition: inner n=2, xs = "7 7" (2 values, not 9)
        assert_eq!(input, "9\n1\n2\n7 7");
    }

    #[test]
    fn count_from_zero_contributes_no_lines() {
        // "N=0 means zero data lines": a linked-mode param resolving to 0
        // omits its block entirely — no stray empty line.
        let params = make_params(&[
            ("n", ParamSpec::Int { min: 0, max: 0, count: CountSpec::default() }),
            ("nums", ParamSpec::Int {
                min: 1,
                max: 9,
                count: CountSpec { min: 0, max: 0, separator: " ".to_string(), from: Some("n".to_string()) },
            }),
        ]);
        let mut rng = seeded();
        let input = generate_input(&params, &mut rng);
        assert_eq!(input, "0");
    }

    #[cfg(feature = "faker")]
    mod faker_tests {
        use super::*;
        use crate::parser::FakerCategory;

        #[test]
        fn faker_generates_name() {
            let mut rng = seeded();
            let spec = ParamSpec::Faker {
                category: FakerCategory::Name,
                count: CountSpec::default(),
            };
            let v = generate_one(&spec, &mut rng);
            assert!(!v.is_empty(), "faker name should be non-empty");
        }

        #[test]
        fn faker_with_count_generates_multiple() {
            let mut rng = seeded();
            let spec = ParamSpec::Faker {
                category: FakerCategory::Email,
                count: fixed_count(2, ","),
            };
            let v = generate_one(&spec, &mut rng);
            let parts: Vec<&str> = v.split(',').collect();
            assert_eq!(parts.len(), 2, "expected 2 comma-separated emails, got: {v}");
            for part in parts {
                assert!(part.contains('@'), "expected email-like string, got: {part}");
            }
        }

        #[test]
        fn faker_all_categories_produce_nonempty() {
            let mut rng = seeded();
            let categories = [
                FakerCategory::Name,
                FakerCategory::FirstName,
                FakerCategory::LastName,
                FakerCategory::Email,
                FakerCategory::Company,
                FakerCategory::City,
                FakerCategory::Country,
            ];
            for cat in categories {
                let spec = ParamSpec::Faker {
                    category: cat.clone(),
                    count: CountSpec::default(),
                };
                let v = generate_one(&spec, &mut rng);
                assert!(!v.is_empty(), "faker {:?} should be non-empty", cat);
            }
        }
    }
}
