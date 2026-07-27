use indexmap::IndexMap;
use serde_json::Value;

/// Hard upper bound on the worst-case byte size of a single generated input.
/// Enforced unconditionally by `parse_params` so no caller (browser dev mode
/// included) can reach generation with a spec that could blow up pool files,
/// worker messages, or the UI. The configurable pool budget (default 4096,
/// see `lib.rs`) is a second, tighter gate on top of this.
pub const HARD_CAP_BYTES: u64 = 65536;

/// Absolute cap on any declared count upper bound and any string length
/// bound, independent of the byte estimator. Two jobs: (1) makes the
/// wasm32 (32-bit usize) and native (64-bit) parsers reach identical
/// verdicts — values are validated as u64 BEFORE narrowing to usize, so a
/// declaration like `count.max: 4294967297` can never silently truncate;
/// (2) defense in depth against estimator bypass — even a zero-width value
/// declaration cannot request more than this many generation iterations.
pub const MAX_COUNT: u64 = 65536;
pub const MAX_LEN: u64 = 65536;

/// Worst-case byte width assumed for one faker-generated value. Faker output
/// length is not statically bounded by the spec, so the estimator uses this
/// documented constant instead.
#[cfg(feature = "faker")]
const FAKER_VALUE_WIDTH: u64 = 64;

/// Count specification: how many values to generate and how to join them.
///
/// Two mutually exclusive sizing modes:
/// - Range mode: `{"min": 2, "max": 5}` — actual count drawn uniformly.
/// - Linked mode: `{"from": "n"}` — actual count equals the value already
///   generated for the previously-declared scalar int param `n`.
///
/// All fields are optional; omitting the whole `count` key uses the defaults
/// (range mode, exactly one value).
#[derive(Debug, Clone, PartialEq)]
pub struct CountSpec {
    pub min: usize,
    pub max: usize,
    pub separator: String,
    pub from: Option<String>,
}

impl Default for CountSpec {
    fn default() -> Self {
        CountSpec { min: 1, max: 1, separator: " ".to_string(), from: None }
    }
}

/// Supported parameter types for randomisation.
/// JSON uses `"type"` as a discriminant tag.
#[derive(Debug, Clone, PartialEq)]
pub enum ParamSpec {
    Int {
        min: i64,
        max: i64,
        count: CountSpec,
    },
    AlphaUpper {
        min_len: usize,
        max_len: usize,
        multiple_of: usize,
        count: CountSpec,
    },
    AlphaLower {
        min_len: usize,
        max_len: usize,
        multiple_of: usize,
        count: CountSpec,
    },
    AlphaMixed {
        min_len: usize,
        max_len: usize,
        multiple_of: usize,
        count: CountSpec,
    },
    HexString {
        min_len: usize,
        max_len: usize,
        multiple_of: usize,
        count: CountSpec,
    },
    PrintableAscii {
        min_len: usize,
        max_len: usize,
        multiple_of: usize,
        count: CountSpec,
    },
    Enum {
        values: Vec<String>,
        count: CountSpec,
    },
    /// A nested block of params repeated K times, where K is the value
    /// already generated for the scalar int param named by `repeat`.
    /// Groups cannot nest (maximum depth 1).
    Group {
        repeat: String,
        params: IndexMap<String, ParamSpec>,
    },
    #[cfg(feature = "faker")]
    Faker {
        category: FakerCategory,
        count: CountSpec,
    },
}

#[cfg(feature = "faker")]
#[derive(Debug, Clone, PartialEq)]
pub enum FakerCategory {
    Name,
    FirstName,
    LastName,
    Email,
    Company,
    City,
    Country,
}

/// Ordered map of param_name → ParamSpec.
/// `IndexMap` preserves JSON key insertion order, which determines
/// the block order in the generated stdin input string.
pub type Params = IndexMap<String, ParamSpec>;

#[cfg(not(feature = "faker"))]
const VALID_TYPES: &str = "`int`, `alpha_upper`, `alpha_lower`, `alpha_mixed`, `hex_string`, `printable_ascii`, `enum`, `group`";
#[cfg(feature = "faker")]
const VALID_TYPES: &str = "`int`, `alpha_upper`, `alpha_lower`, `alpha_mixed`, `hex_string`, `printable_ascii`, `enum`, `group`, `faker`";

/// Info about a param that may legally be referenced by `count.from` or
/// group `repeat`: a scalar int (no count, or fixed count of exactly 1).
#[derive(Debug, Clone, Copy)]
struct RefInfo {
    min: i64,
    max: i64,
}

fn is_scalar_int_ref(spec: &ParamSpec) -> Option<RefInfo> {
    if let ParamSpec::Int { min, max, count } = spec
        && count.from.is_none()
        && count.min == 1
        && count.max == 1
    {
        return Some(RefInfo { min: *min, max: *max });
    }
    None
}

/// Parse a JSON params object (from VitePress frontmatter) into an ordered
/// Params map, validating the full spec surface at parse time:
/// unknown fields, inverted ranges, empty enums, reference legality,
/// group nesting depth, and the worst-case hard cap. All violations return
/// a readable `Err` — generation is never reachable with a spec that could
/// panic (trap) the WASM instance.
pub fn parse_params(json_str: &str) -> Result<Params, String> {
    let v: Value = serde_json::from_str(json_str)
        .map_err(|e| format!("JSON parse error: {e}"))?;
    parse_params_value(&v)
}

/// Same as `parse_params`, but starting from an already-parsed JSON value
/// (used by the pool-spec entry which wraps params in an envelope object).
pub fn parse_params_value(v: &Value) -> Result<Params, String> {
    let obj = v
        .as_object()
        .ok_or_else(|| "params must be a JSON object".to_string())?;
    if obj.is_empty() {
        return Err("params must declare at least one param".to_string());
    }

    let mut params: Params = IndexMap::new();
    let mut top_refs: IndexMap<String, RefInfo> = IndexMap::new();

    for (name, spec_v) in obj {
        let spec = parse_one(name, spec_v, &top_refs, true)?;
        if let Some(info) = is_scalar_int_ref(&spec) {
            top_refs.insert(name.clone(), info);
        }
        params.insert(name.clone(), spec);
    }

    let (total, items) = estimate_input_bytes(&params);
    if total > HARD_CAP_BYTES {
        return Err(budget_error(total, HARD_CAP_BYTES, &items, "hard cap"));
    }

    Ok(params)
}

/// Format a budget violation with the per-param worst-case breakdown so the
/// challenge author can see exactly which declaration blew the budget.
pub fn budget_error(total: u64, limit: u64, items: &[(String, u64)], kind: &str) -> String {
    let detail: Vec<String> = items
        .iter()
        .map(|(name, bytes)| format!("  {name}: {bytes} bytes"))
        .collect();
    format!(
        "worst-case input estimate {total} bytes exceeds the {limit}-byte {kind}; per-param estimate:\n{}",
        detail.join("\n")
    )
}

fn parse_one(
    name: &str,
    v: &Value,
    visible: &IndexMap<String, RefInfo>,
    allow_group: bool,
) -> Result<ParamSpec, String> {
    let obj = v
        .as_object()
        .ok_or_else(|| format!("param '{name}': spec must be a JSON object"))?;

    let type_name = obj
        .get("type")
        .ok_or_else(|| format!("param '{name}': missing required field 'type'"))?
        .as_str()
        .ok_or_else(|| format!("param '{name}': 'type' must be a string"))?;

    match type_name {
        "int" => {
            check_fields(name, obj, &["type", "min", "max", "count"])?;
            let min = get_i64(name, obj, "min", 0)?;
            let max = get_i64(name, obj, "max", 100)?;
            if min > max {
                return Err(format!("param '{name}': min ({min}) must be <= max ({max})"));
            }
            let count = parse_count(name, obj, visible)?;
            Ok(ParamSpec::Int { min, max, count })
        }
        "alpha_upper" | "alpha_lower" | "alpha_mixed" | "hex_string" | "printable_ascii" => {
            check_fields(name, obj, &["type", "min_len", "max_len", "multiple_of", "count"])?;
            let min_len = get_usize(name, obj, "min_len", 1)?;
            let max_len = get_usize(name, obj, "max_len", 255)?;
            let multiple_of = get_usize(name, obj, "multiple_of", 1)?;
            if min_len > max_len {
                return Err(format!(
                    "param '{name}': min_len ({min_len}) must be <= max_len ({max_len})"
                ));
            }
            if multiple_of == 0 {
                return Err(format!("param '{name}': multiple_of must be >= 1"));
            }
            let lo = min_len.div_ceil(multiple_of);
            let hi = max_len / multiple_of;
            if lo > hi {
                return Err(format!(
                    "param '{name}': no valid length in [{min_len}, {max_len}] is a multiple of {multiple_of}"
                ));
            }
            let count = parse_count(name, obj, visible)?;
            Ok(match type_name {
                "alpha_upper" => ParamSpec::AlphaUpper { min_len, max_len, multiple_of, count },
                "alpha_lower" => ParamSpec::AlphaLower { min_len, max_len, multiple_of, count },
                "alpha_mixed" => ParamSpec::AlphaMixed { min_len, max_len, multiple_of, count },
                "hex_string" => ParamSpec::HexString { min_len, max_len, multiple_of, count },
                _ => ParamSpec::PrintableAscii { min_len, max_len, multiple_of, count },
            })
        }
        "enum" => {
            check_fields(name, obj, &["type", "values", "count"])?;
            let values_v = obj
                .get("values")
                .ok_or_else(|| format!("param '{name}': enum requires a 'values' array"))?;
            let arr = values_v
                .as_array()
                .ok_or_else(|| format!("param '{name}': 'values' must be an array"))?;
            let mut values = Vec::with_capacity(arr.len());
            for item in arr {
                values.push(
                    item.as_str()
                        .ok_or_else(|| format!("param '{name}': enum values must be strings"))?
                        .to_string(),
                );
            }
            if values.is_empty() {
                return Err(format!("param '{name}': enum values must not be empty"));
            }
            let count = parse_count(name, obj, visible)?;
            Ok(ParamSpec::Enum { values, count })
        }
        "group" => {
            if !allow_group {
                return Err(format!(
                    "param '{name}': groups cannot nest (maximum depth 1)"
                ));
            }
            check_fields(name, obj, &["type", "repeat", "params"])?;
            let repeat = obj
                .get("repeat")
                .ok_or_else(|| format!("param '{name}': group requires a 'repeat' field"))?
                .as_str()
                .ok_or_else(|| format!("param '{name}': 'repeat' must be a param name string"))?
                .to_string();
            check_reference(name, "repeat", &repeat, visible)?;

            let params_v = obj
                .get("params")
                .ok_or_else(|| format!("param '{name}': group requires a 'params' object"))?;
            let inner_obj = params_v
                .as_object()
                .ok_or_else(|| format!("param '{name}': group 'params' must be a JSON object"))?;
            if inner_obj.is_empty() {
                return Err(format!("param '{name}': group params must not be empty"));
            }

            // Inner scope: locals declared so far in this group, falling back
            // to top-level params declared before the group.
            let mut inner_visible = visible.clone();
            let mut inner: Params = IndexMap::new();
            for (iname, ispec_v) in inner_obj {
                let ispec = parse_one(iname, ispec_v, &inner_visible, false)?;
                if let Some(info) = is_scalar_int_ref(&ispec) {
                    inner_visible.insert(iname.clone(), info);
                }
                inner.insert(iname.clone(), ispec);
            }
            Ok(ParamSpec::Group { repeat, params: inner })
        }
        #[cfg(feature = "faker")]
        "faker" => {
            check_fields(name, obj, &["type", "category", "count"])?;
            let cat = obj
                .get("category")
                .ok_or_else(|| format!("param '{name}': faker requires a 'category' field"))?
                .as_str()
                .ok_or_else(|| format!("param '{name}': 'category' must be a string"))?;
            let category = match cat {
                "name" => FakerCategory::Name,
                "first_name" => FakerCategory::FirstName,
                "last_name" => FakerCategory::LastName,
                "email" => FakerCategory::Email,
                "company" => FakerCategory::Company,
                "city" => FakerCategory::City,
                "country" => FakerCategory::Country,
                other => {
                    return Err(format!("param '{name}': unknown faker category '{other}'"));
                }
            };
            let count = parse_count(name, obj, visible)?;
            Ok(ParamSpec::Faker { category, count })
        }
        other => Err(format!(
            "param '{name}': unknown variant `{other}`, expected one of {VALID_TYPES}"
        )),
    }
}

/// Reject any key not in the allow-list. This is the deny-unknown-fields
/// guarantee: a misspelled field or a construct from a newer engine version
/// fails loudly instead of silently falling back to defaults.
fn check_fields(
    name: &str,
    obj: &serde_json::Map<String, Value>,
    allowed: &[&str],
) -> Result<(), String> {
    for key in obj.keys() {
        if !allowed.contains(&key.as_str()) {
            return Err(format!(
                "param '{name}': unknown field '{key}' (allowed: {})",
                allowed.join(", ")
            ));
        }
    }
    Ok(())
}

fn parse_count(
    name: &str,
    obj: &serde_json::Map<String, Value>,
    visible: &IndexMap<String, RefInfo>,
) -> Result<CountSpec, String> {
    let Some(count_v) = obj.get("count") else {
        return Ok(CountSpec::default());
    };
    let cobj = count_v
        .as_object()
        .ok_or_else(|| format!("param '{name}': 'count' must be a JSON object"))?;
    for key in cobj.keys() {
        if !["min", "max", "separator", "from"].contains(&key.as_str()) {
            return Err(format!(
                "param '{name}': unknown field '{key}' in count (allowed: min, max, separator, from)"
            ));
        }
    }

    let separator = match cobj.get("separator") {
        Some(s) => s
            .as_str()
            .ok_or_else(|| format!("param '{name}': count.separator must be a string"))?
            .to_string(),
        None => " ".to_string(),
    };

    if let Some(from_v) = cobj.get("from") {
        if cobj.contains_key("min") || cobj.contains_key("max") {
            return Err(format!(
                "param '{name}': count.from is mutually exclusive with count.min/count.max"
            ));
        }
        let from = from_v
            .as_str()
            .ok_or_else(|| format!("param '{name}': count.from must be a param name string"))?
            .to_string();
        check_reference(name, "count.from", &from, visible)?;
        // min/max carry the referenced param's bounds only for internal
        // bookkeeping; generation always resolves the actual value.
        return Ok(CountSpec { min: 0, max: 0, separator, from: Some(from) });
    }

    let min = get_count_field(name, cobj, "min", 1)?;
    let max = get_count_field(name, cobj, "max", 1)?;
    if min > max {
        return Err(format!(
            "param '{name}': count.min ({min}) must be <= count.max ({max})"
        ));
    }
    Ok(CountSpec { min, max, separator, from: None })
}

/// Validate a `count.from` / group `repeat` reference against the params
/// visible at the reference site (same scope declared earlier, or outer
/// scope declared before the group). Rules: the target exists, is declared
/// before the host (no forward references), is a scalar int, and cannot be
/// negative.
fn check_reference(
    host: &str,
    field: &str,
    target: &str,
    visible: &IndexMap<String, RefInfo>,
) -> Result<(), String> {
    let Some(info) = visible.get(target) else {
        return Err(format!(
            "param '{host}': {field} references '{target}', which is not a previously-declared scalar int param (forward references, groups, and multi-value params cannot be referenced)"
        ));
    };
    if info.min < 0 {
        return Err(format!(
            "param '{host}': {field} references '{target}' whose min ({}) is negative; referenced params must declare min >= 0",
            info.min
        ));
    }
    Ok(())
}

fn get_i64(
    name: &str,
    obj: &serde_json::Map<String, Value>,
    key: &str,
    default: i64,
) -> Result<i64, String> {
    match obj.get(key) {
        None => Ok(default),
        Some(v) => v
            .as_i64()
            .ok_or_else(|| format!("param '{name}': '{key}' must be an integer")),
    }
}

/// Parse a length-ish field as u64, enforce `MAX_LEN`, then narrow.
/// Cap-before-narrow keeps the verdict identical on wasm32 and native.
fn get_usize(
    name: &str,
    obj: &serde_json::Map<String, Value>,
    key: &str,
    default: usize,
) -> Result<usize, String> {
    match obj.get(key) {
        None => Ok(default),
        Some(v) => {
            let n = v
                .as_u64()
                .ok_or_else(|| format!("param '{name}': '{key}' must be a non-negative integer"))?;
            if n > MAX_LEN {
                return Err(format!(
                    "param '{name}': '{key}' ({n}) exceeds the maximum of {MAX_LEN}"
                ));
            }
            Ok(n as usize)
        }
    }
}

/// Parse a count field as u64, enforce `MAX_COUNT`, then narrow.
fn get_count_field(
    name: &str,
    obj: &serde_json::Map<String, Value>,
    key: &str,
    default: usize,
) -> Result<usize, String> {
    match obj.get(key) {
        None => Ok(default),
        Some(v) => {
            let n = v
                .as_u64()
                .ok_or_else(|| format!("param '{name}': count.{key} must be a non-negative integer"))?;
            if n > MAX_COUNT {
                return Err(format!(
                    "param '{name}': count.{key} ({n}) exceeds the maximum of {MAX_COUNT}"
                ));
            }
            Ok(n as usize)
        }
    }
}

// ── Worst-case input size estimation ────────────────────────────────────

/// Decimal string width of the widest value in [min, max], including sign.
fn int_width(min: i64, max: i64) -> u64 {
    let w = |n: i64| n.to_string().len() as u64;
    w(min).max(w(max))
}

/// Worst-case byte width of a single generated value for this spec.
fn value_width(spec: &ParamSpec) -> u64 {
    match spec {
        ParamSpec::Int { min, max, .. } => int_width(*min, *max),
        ParamSpec::AlphaUpper { max_len, .. }
        | ParamSpec::AlphaLower { max_len, .. }
        | ParamSpec::AlphaMixed { max_len, .. }
        | ParamSpec::HexString { max_len, .. }
        | ParamSpec::PrintableAscii { max_len, .. } => *max_len as u64,
        ParamSpec::Enum { values, .. } => {
            values.iter().map(|v| v.len() as u64).max().unwrap_or(0)
        }
        ParamSpec::Group { .. } => 0, // handled structurally in block_width
        #[cfg(feature = "faker")]
        ParamSpec::Faker { .. } => FAKER_VALUE_WIDTH,
    }
}

/// Upper bound on the actual count for a spec, resolving `from` references
/// against the visible ref-bounds map. Saturating: absurd declared bounds
/// simply blow the budget check with a clear message.
fn count_upper(count: &CountSpec, refs: &IndexMap<String, RefInfo>) -> u64 {
    match &count.from {
        Some(target) => refs
            .get(target)
            .map(|info| info.max.max(0) as u64)
            // check_reference makes a miss unreachable; if a future
            // refactor breaks that invariant, the safe failure mode for a
            // budget estimator is "over budget", never "free".
            .unwrap_or(u64::MAX),
        None => count.max as u64,
    }
}

fn block_width(
    spec: &ParamSpec,
    refs: &IndexMap<String, RefInfo>,
) -> u64 {
    match spec {
        ParamSpec::Group { repeat, params } => {
            let reps = refs
                .get(repeat)
                .map(|info| info.max.max(0) as u64)
                .unwrap_or(u64::MAX); // see count_upper: fail as "over budget"
            let mut inner_refs = refs.clone();
            let mut inner_total: u64 = 0;
            let mut first = true;
            for (iname, ispec) in params {
                if !first {
                    inner_total = inner_total.saturating_add(1); // newline between inner blocks
                }
                first = false;
                inner_total = inner_total.saturating_add(block_width(ispec, &inner_refs));
                if let Some(info) = is_scalar_int_ref(ispec) {
                    inner_refs.insert(iname.clone(), info);
                }
            }
            let body = reps.saturating_mul(inner_total);
            let newlines = reps.saturating_sub(1); // newline between repetitions
            body.saturating_add(newlines)
        }
        _ => {
            let count = match spec {
                ParamSpec::Int { count, .. }
                | ParamSpec::AlphaUpper { count, .. }
                | ParamSpec::AlphaLower { count, .. }
                | ParamSpec::AlphaMixed { count, .. }
                | ParamSpec::HexString { count, .. }
                | ParamSpec::PrintableAscii { count, .. }
                | ParamSpec::Enum { count, .. } => count,
                #[cfg(feature = "faker")]
                ParamSpec::Faker { count, .. } => count,
                ParamSpec::Group { .. } => unreachable!(),
            };
            let cmax = count_upper(count, refs);
            if cmax == 0 {
                return 0;
            }
            // Floor each value at 1 byte: zero-width declarations (an enum
            // of empty strings, max_len 0) with an empty separator would
            // otherwise contribute 0 to the estimate no matter how large
            // the count, bypassing BOTH budget layers while still costing
            // full generation work. The floor keeps the estimate an upper
            // bound in byte terms irrelevant here — what it guards is the
            // iteration count, which is real cost regardless of width.
            let values = value_width(spec).max(1).saturating_mul(cmax);
            let seps = (count.separator.len() as u64).saturating_mul(cmax - 1);
            values.saturating_add(seps)
        }
    }
}

/// Compute the worst-case byte estimate for one full generated input, plus
/// a per-top-level-param breakdown for error reporting. The estimate is an
/// upper bound on actual rendered bytes (saturating arithmetic: overflow
/// reads as "way over budget", which is the correct verdict).
pub fn estimate_input_bytes(params: &Params) -> (u64, Vec<(String, u64)>) {
    let mut refs: IndexMap<String, RefInfo> = IndexMap::new();
    let mut items: Vec<(String, u64)> = Vec::new();
    let mut total: u64 = 0;
    let mut first = true;
    for (name, spec) in params {
        if !first {
            total = total.saturating_add(1); // newline between top-level blocks
        }
        first = false;
        let width = block_width(spec, &refs);
        items.push((name.clone(), width));
        total = total.saturating_add(width);
        if let Some(info) = is_scalar_int_ref(spec) {
            refs.insert(name.clone(), info);
        }
    }
    (total, items)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_int_param() {
        let json = r#"{"shift": {"type": "int", "min": 1, "max": 25}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["shift"], ParamSpec::Int { min: 1, max: 25, count: CountSpec::default() });
    }

    #[test]
    fn parses_alpha_upper_param() {
        let json = r#"{"pt": {"type": "alpha_upper", "min_len": 5, "max_len": 12}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["pt"], ParamSpec::AlphaUpper { min_len: 5, max_len: 12, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn parses_hex_string_param() {
        let json = r#"{"k": {"type": "hex_string", "min_len": 32, "max_len": 32}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["k"], ParamSpec::HexString { min_len: 32, max_len: 32, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn preserves_param_declaration_order() {
        let json = r#"{"plaintext": {"type": "alpha_upper", "min_len": 5, "max_len": 12}, "shift": {"type": "int", "min": 1, "max": 25}}"#;
        let params = parse_params(json).unwrap();
        let keys: Vec<&str> = params.keys().map(|s| s.as_str()).collect();
        assert_eq!(keys, vec!["plaintext", "shift"]);
    }

    #[test]
    fn returns_error_on_invalid_json() {
        let result = parse_params("not valid json {{{");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("JSON parse error"));
    }

    #[test]
    fn returns_error_on_unknown_param_type() {
        let json = r#"{"x": {"type": "unknown_type"}}"#;
        let result = parse_params(json);
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("unknown variant"));
    }

    #[test]
    fn parses_alpha_lower_param() {
        let json = r#"{"pt": {"type": "alpha_lower", "min_len": 3, "max_len": 8}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["pt"], ParamSpec::AlphaLower { min_len: 3, max_len: 8, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn parses_alpha_mixed_param() {
        let json = r#"{"pt": {"type": "alpha_mixed", "min_len": 4, "max_len": 16}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["pt"], ParamSpec::AlphaMixed { min_len: 4, max_len: 16, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn parses_printable_ascii_param() {
        let json = r#"{"msg": {"type": "printable_ascii", "min_len": 10, "max_len": 20}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["msg"], ParamSpec::PrintableAscii { min_len: 10, max_len: 20, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn parses_count_field() {
        let json = r#"{"shift": {"type": "int", "min": 1, "max": 25, "count": {"min": 3, "max": 3}}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["shift"], ParamSpec::Int {
            min: 1,
            max: 25,
            count: CountSpec { min: 3, max: 3, separator: " ".to_string(), from: None },
        });
    }

    #[test]
    fn count_defaults_to_one_when_omitted() {
        let json = r#"{"pt": {"type": "alpha_upper", "min_len": 5, "max_len": 10}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(
            params["pt"],
            ParamSpec::AlphaUpper { min_len: 5, max_len: 10, multiple_of: 1, count: CountSpec::default() }
        );
    }

    #[test]
    fn parses_multiple_params() {
        let json = r#"{"a": {"type": "int", "min": 1, "max": 10}, "b": {"type": "alpha_lower", "min_len": 3, "max_len": 5}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params.len(), 2);
        assert_eq!(params["a"], ParamSpec::Int { min: 1, max: 10, count: CountSpec::default() });
        assert_eq!(params["b"], ParamSpec::AlphaLower { min_len: 3, max_len: 5, multiple_of: 1, count: CountSpec::default() });
    }

    #[test]
    fn parses_count_spec_with_min_max_range() {
        let json = r#"{"n": {"type": "int", "min": 1, "max": 100, "count": {"min": 2, "max": 5}}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["n"], ParamSpec::Int {
            min: 1,
            max: 100,
            count: CountSpec { min: 2, max: 5, separator: " ".to_string(), from: None },
        });
    }

    #[test]
    fn parses_enum_param() {
        let json = r#"{"mode": {"type": "enum", "values": ["ECB", "CBC"]}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["mode"], ParamSpec::Enum {
            values: vec!["ECB".to_string(), "CBC".to_string()],
            count: CountSpec::default(),
        });
    }

    #[test]
    fn enum_empty_values_returns_error() {
        let json = r#"{"mode": {"type": "enum", "values": []}}"#;
        let result = parse_params(json);
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("enum values must not be empty"));
    }

    #[test]
    fn parses_enum_param_with_count() {
        let json = r#"{"mode": {"type": "enum", "values": ["A", "B", "C"], "count": {"min": 2, "max": 3, "separator": ","}}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["mode"], ParamSpec::Enum {
            values: vec!["A".to_string(), "B".to_string(), "C".to_string()],
            count: CountSpec { min: 2, max: 3, separator: ",".to_string(), from: None },
        });
    }

    #[test]
    fn parses_count_spec_with_custom_separator() {
        let json = r#"{"n": {"type": "int", "min": 1, "max": 10, "count": {"min": 3, "max": 3, "separator": ","}}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["n"], ParamSpec::Int {
            min: 1,
            max: 10,
            count: CountSpec { min: 3, max: 3, separator: ",".to_string(), from: None },
        });
    }

    #[test]
    fn parses_multiple_of_field() {
        let json = r#"{"pt": {"type": "hex_string", "min_len": 16, "max_len": 64, "multiple_of": 16}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["pt"], ParamSpec::HexString {
            min_len: 16,
            max_len: 64,
            multiple_of: 16,
            count: CountSpec::default(),
        });
    }

    #[test]
    fn multiple_of_defaults_to_one() {
        let json = r#"{"pt": {"type": "hex_string", "min_len": 8, "max_len": 16}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["pt"], ParamSpec::HexString {
            min_len: 8,
            max_len: 16,
            multiple_of: 1,
            count: CountSpec::default(),
        });
    }

    #[cfg(not(feature = "faker"))]
    #[test]
    fn faker_type_fails_without_feature() {
        let json = r#"{"name": {"type": "faker", "category": "name"}}"#;
        let result = parse_params(json);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.contains("unknown variant"), "expected unknown variant error, got: {err}");
    }

    #[cfg(feature = "faker")]
    #[test]
    fn parses_faker_param_with_feature() {
        let json = r#"{"name": {"type": "faker", "category": "name"}}"#;
        let params = parse_params(json).unwrap();
        assert_eq!(params["name"], ParamSpec::Faker {
            category: FakerCategory::Name,
            count: CountSpec::default(),
        });
    }

    // ── Parse-time validation (fail loudly instead of trapping) ────────

    #[test]
    fn inverted_int_range_is_parse_error() {
        let json = r#"{"n": {"type": "int", "min": 9, "max": 1}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("min (9) must be <= max (1)"), "got: {err}");
    }

    #[test]
    fn inverted_len_range_is_parse_error() {
        let json = r#"{"s": {"type": "alpha_upper", "min_len": 10, "max_len": 2}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("min_len (10) must be <= max_len (2)"), "got: {err}");
    }

    #[test]
    fn inverted_count_range_is_parse_error() {
        let json = r#"{"n": {"type": "int", "count": {"min": 5, "max": 2}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("count.min (5) must be <= count.max (2)"), "got: {err}");
    }

    #[test]
    fn impossible_multiple_of_is_parse_error() {
        let json = r#"{"s": {"type": "hex_string", "min_len": 1, "max_len": 8, "multiple_of": 16}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("no valid length"), "got: {err}");
    }

    #[test]
    fn zero_multiple_of_is_parse_error() {
        let json = r#"{"s": {"type": "hex_string", "multiple_of": 0}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("multiple_of must be >= 1"), "got: {err}");
    }

    #[test]
    fn unknown_field_is_rejected() {
        let json = r#"{"s": {"type": "alpha_upper", "min_lenght": 3}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("unknown field 'min_lenght'"), "got: {err}");
    }

    #[test]
    fn unknown_count_field_is_rejected() {
        let json = r#"{"n": {"type": "int", "count": {"mim": 2}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("unknown field 'mim' in count"), "got: {err}");
    }

    #[test]
    fn empty_params_object_is_parse_error() {
        let err = parse_params("{}").unwrap_err();
        assert!(err.contains("at least one param"), "got: {err}");
    }

    // ── count.from linkage ──────────────────────────────────────────────

    #[test]
    fn parses_count_from_linked_mode() {
        let json = r#"{"n": {"type": "int", "min": 1, "max": 9}, "nums": {"type": "int", "min": 0, "max": 99, "count": {"from": "n", "separator": "\n"}}}"#;
        let params = parse_params(json).unwrap();
        match &params["nums"] {
            ParamSpec::Int { count, .. } => {
                assert_eq!(count.from.as_deref(), Some("n"));
                assert_eq!(count.separator, "\n");
            }
            other => panic!("expected Int, got {other:?}"),
        }
    }

    #[test]
    fn count_from_with_min_max_is_mutually_exclusive_error() {
        let json = r#"{"n": {"type": "int", "min": 1, "max": 9}, "nums": {"type": "int", "count": {"from": "n", "min": 2}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("mutually exclusive"), "got: {err}");
    }

    #[test]
    fn count_from_forward_reference_is_parse_error() {
        let json = r#"{"nums": {"type": "int", "count": {"from": "n"}}, "n": {"type": "int", "min": 1, "max": 9}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("not a previously-declared scalar int"), "got: {err}");
    }

    #[test]
    fn count_from_unknown_reference_is_parse_error() {
        let json = r#"{"nums": {"type": "int", "count": {"from": "ghost"}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("'ghost'"), "got: {err}");
    }

    #[test]
    fn count_from_multi_value_reference_is_parse_error() {
        let json = r#"{"n": {"type": "int", "min": 1, "max": 9, "count": {"min": 2, "max": 3}}, "nums": {"type": "int", "count": {"from": "n"}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("not a previously-declared scalar int"), "got: {err}");
    }

    #[test]
    fn count_from_non_int_reference_is_parse_error() {
        let json = r#"{"s": {"type": "alpha_upper"}, "nums": {"type": "int", "count": {"from": "s"}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("not a previously-declared scalar int"), "got: {err}");
    }

    #[test]
    fn count_from_negative_range_reference_is_parse_error() {
        let json = r#"{"n": {"type": "int", "min": -3, "max": 9}, "nums": {"type": "int", "count": {"from": "n"}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("min >= 0"), "got: {err}");
    }

    // ── group construct ─────────────────────────────────────────────────

    #[test]
    fn parses_group_with_linked_inner_count() {
        let json = r#"{
            "t": {"type": "int", "min": 2, "max": 4},
            "cases": {"type": "group", "repeat": "t", "params": {
                "n": {"type": "int", "min": 1, "max": 5},
                "nums": {"type": "int", "min": -99, "max": 99, "count": {"from": "n", "separator": "\n"}}
            }}
        }"#;
        let params = parse_params(json).unwrap();
        match &params["cases"] {
            ParamSpec::Group { repeat, params: inner } => {
                assert_eq!(repeat, "t");
                assert_eq!(inner.len(), 2);
                assert!(matches!(inner["n"], ParamSpec::Int { .. }));
            }
            other => panic!("expected Group, got {other:?}"),
        }
    }

    #[test]
    fn nested_group_is_parse_error() {
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 2},
            "outer": {"type": "group", "repeat": "t", "params": {
                "k": {"type": "int", "min": 1, "max": 2},
                "inner": {"type": "group", "repeat": "k", "params": {"x": {"type": "int"}}}
            }}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("cannot nest"), "got: {err}");
    }

    #[test]
    fn group_repeat_forward_reference_is_parse_error() {
        let json = r#"{
            "cases": {"type": "group", "repeat": "t", "params": {"x": {"type": "int"}}},
            "t": {"type": "int", "min": 1, "max": 2}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("not a previously-declared scalar int"), "got: {err}");
    }

    #[test]
    fn group_cannot_be_referenced() {
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 2},
            "g": {"type": "group", "repeat": "t", "params": {"x": {"type": "int"}}},
            "nums": {"type": "int", "count": {"from": "g"}}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("not a previously-declared scalar int"), "got: {err}");
    }

    #[test]
    fn group_inner_validation_is_recursive() {
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 2},
            "g": {"type": "group", "repeat": "t", "params": {
                "mode": {"type": "enum", "values": []}
            }}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("enum values must not be empty"), "got: {err}");
    }

    #[test]
    fn empty_group_params_is_parse_error() {
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 2},
            "g": {"type": "group", "repeat": "t", "params": {}}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("group params must not be empty"), "got: {err}");
    }

    #[test]
    fn group_with_count_field_is_rejected() {
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 2},
            "g": {"type": "group", "repeat": "t", "count": {"min": 2, "max": 2}, "params": {"x": {"type": "int"}}}
        }"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("unknown field 'count'"), "got: {err}");
    }

    // ── Worst-case estimate & hard cap ──────────────────────────────────

    #[test]
    fn estimate_covers_scalar_int() {
        let json = r#"{"n": {"type": "int", "min": -100, "max": 5}}"#;
        let params = parse_params(json).unwrap();
        let (total, items) = estimate_input_bytes(&params);
        assert_eq!(total, 4); // "-100"
        assert_eq!(items, vec![("n".to_string(), 4)]);
    }

    #[test]
    fn estimate_covers_count_and_separator() {
        // 3 values × 2 digits + 2 separators of 1 byte = 8
        let json = r#"{"n": {"type": "int", "min": 10, "max": 99, "count": {"min": 1, "max": 3}}}"#;
        let params = parse_params(json).unwrap();
        let (total, _) = estimate_input_bytes(&params);
        assert_eq!(total, 8);
    }

    #[test]
    fn estimate_covers_group_and_from() {
        // t: 1 byte (max 9)
        // group repeated up to 9 times, each repetition:
        //   n: 1 byte (max 5) + newline + nums: 5 values × 3 bytes ("-99") + 4 newlines = 1+1+15+4 = 21
        // group block = 9×21 + 8 newlines = 197; total = 1 + 1 + 197 = 199
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 9},
            "cases": {"type": "group", "repeat": "t", "params": {
                "n": {"type": "int", "min": 1, "max": 5},
                "nums": {"type": "int", "min": -99, "max": 99, "count": {"from": "n", "separator": "\n"}}
            }}
        }"#;
        let params = parse_params(json).unwrap();
        let (total, _) = estimate_input_bytes(&params);
        assert_eq!(total, 199);
    }

    #[test]
    fn hard_cap_is_enforced_at_parse_time() {
        // 40000 values × 2 digits + 39999 separators > 65536 hard cap,
        // while count.max stays under MAX_COUNT so the estimator (not the
        // count cap) is what rejects it.
        let json = r#"{"n": {"type": "int", "min": 10, "max": 99, "count": {"min": 1, "max": 40000}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("hard cap"), "got: {err}");
        assert!(err.contains("per-param estimate"), "got: {err}");
    }

    #[test]
    fn zero_width_gadget_cannot_bypass_budget() {
        // S2 regression: enum of empty strings + empty separator + huge count
        // used to estimate 0 bytes and bypass both budget layers while still
        // costing millions of generation iterations.
        let json = r#"{"x": {"type": "enum", "values": [""], "count": {"min": 20000000, "max": 20000000, "separator": ""}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(
            err.contains("exceeds the maximum of 65536") || err.contains("hard cap"),
            "zero-width gadget must be rejected, got: {err}"
        );
    }

    #[test]
    fn zero_width_values_are_floored_to_one_byte_in_estimate() {
        // The estimator must never price a value at 0 bytes: 60000 empty
        // strings with an empty separator estimate as 60000, not 0, so the
        // pool budget (default 4096) rejects such specs.
        let json = r#"{"x": {"type": "alpha_upper", "min_len": 0, "max_len": 0, "count": {"min": 60000, "max": 60000, "separator": ""}}}"#;
        let params = parse_params(json).unwrap();
        let (total, _) = estimate_input_bytes(&params);
        assert_eq!(total, 60000, "zero-width floor must price each value at 1 byte");
    }

    #[test]
    fn count_above_max_count_is_rejected_pre_narrowing() {
        // M1 regression: 2^32 + 1 must fail identically on wasm32 and native —
        // the u64 cap check runs BEFORE any usize narrowing can truncate.
        let json = r#"{"n": {"type": "int", "count": {"min": 0, "max": 4294967297}}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("exceeds the maximum of 65536"), "got: {err}");
    }

    #[test]
    fn len_above_max_len_is_rejected_pre_narrowing() {
        let json = r#"{"s": {"type": "alpha_lower", "min_len": 1, "max_len": 4294967297}}"#;
        let err = parse_params(json).unwrap_err();
        assert!(err.contains("exceeds the maximum of 65536"), "got: {err}");
    }

    #[test]
    fn estimate_is_upper_bound_on_actual_bytes() {
        use rand::SeedableRng;
        use rand::rngs::SmallRng;
        let json = r#"{
            "t": {"type": "int", "min": 1, "max": 4},
            "cases": {"type": "group", "repeat": "t", "params": {
                "n": {"type": "int", "min": 0, "max": 6},
                "nums": {"type": "int", "min": -999, "max": 999, "count": {"from": "n", "separator": "\n"}},
                "tag": {"type": "enum", "values": ["ab", "cdef"]}
            }}
        }"#;
        let params = parse_params(json).unwrap();
        let (estimate, _) = estimate_input_bytes(&params);
        for seed in 0..300u64 {
            let mut rng = SmallRng::seed_from_u64(seed);
            let input = crate::rng::generate_input(&params, &mut rng);
            assert!(
                (input.len() as u64) <= estimate,
                "seed={seed}: actual {} > estimate {estimate}",
                input.len()
            );
        }
    }
}
