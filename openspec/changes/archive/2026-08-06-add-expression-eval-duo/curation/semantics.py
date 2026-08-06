"""Change B design-stage semantics module.

apcs011 (snack-bar-register): + - evaluated FIRST (higher precedence), left-assoc.
                              then * / left-assoc. No parentheses. Exact division guaranteed.
apcs012 (coupon-stacking):    + - first, RIGHT-assoc; * / left-assoc; parentheses override.
                              Exact division guaranteed. Parens only in entries 9-20.

Token format: single space between all tokens (numbers, + - * /, parens).
Input per testcase: first line T, then T expression lines. Output: T answer lines.
"""


def eval011_tokens(toks):
    """Additive-first left-assoc, then muldiv left-assoc. Iterative, exact division."""
    # split into additive segments at * /
    seg_vals = []
    ops = []
    i = 0
    n = len(toks)
    while i < n:
        # one additive segment, left-assoc
        v = int(toks[i]); i += 1
        while i < n and toks[i] in "+-":
            b = int(toks[i + 1])
            v = v + b if toks[i] == "+" else v - b
            i += 2
        seg_vals.append(v)
        if i < n:
            ops.append(toks[i]); i += 1
    V = seg_vals[0]
    for op, s in zip(ops, seg_vals[1:]):
        if op == "*":
            V = V * s
        else:
            assert s != 0 and V % s == 0, f"inexact/zero division {V}/{s}"
            V = V // s
    return V


def eval012_tokens(toks):
    """Parens override; additive right-assoc; muldiv left-assoc; additive binds tighter.

    Iterative on chains (right fold for additive), recursive only on paren depth.
    """
    pos = 0

    def parse_expr():  # lowest level: muldiv left-assoc over additive terms
        nonlocal pos
        V = parse_term()
        while pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            s = parse_term()
            if op == "*":
                V = V * s
            else:
                assert s != 0 and V % s == 0, f"inexact/zero division {V}/{s}"
                V = V // s
        return V

    def parse_term():  # additive chain, right-assoc, iterative right fold
        nonlocal pos
        atoms = [parse_atom()]
        aops = []
        while pos < len(toks) and toks[pos] in "+-":
            aops.append(toks[pos]); pos += 1
            atoms.append(parse_atom())
        acc = atoms[-1]
        for k in range(len(aops) - 1, -1, -1):
            acc = atoms[k] + acc if aops[k] == "+" else atoms[k] - acc
        return acc

    def parse_atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = parse_expr()
            assert toks[pos] == ")", "unbalanced"
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v

    v = parse_expr()
    assert pos == len(toks), "trailing tokens"
    return v


def std_eval(expr):
    """Python standard precedence with integer semantics; returns value or 'CRASH'.

    Uses Fraction to detect inexactness under std order (student's // would floor,
    either way the answer differs from ours whenever we assert disagreement).
    """
    from fractions import Fraction
    try:
        v = eval(expr.replace("/", "//"), {"__builtins__": {}}, {})
        return v
    except Exception:
        return "CRASH"


# ---------------- builders ----------------

def seg_left(rng, target, length):
    """Additive chain (left-assoc value == target), `length` operands, non-negative operands."""
    assert length >= 1
    if length == 1:
        assert target >= 0
        return [str(target)]
    toks = [str(rng.randrange(0, 100))]
    v = int(toks[0])
    for _ in range(length - 2):
        op = rng.choice("+-")
        b = rng.randrange(0, 100)
        toks += [op, str(b)]
        v = v + b if op == "+" else v - b
    # final adjust operand
    if target >= v:
        toks += ["+", str(target - v)]
    else:
        toks += ["-", str(v - target)]
    return toks


def seg_right(rng, target, length):
    """Additive chain (right-assoc value == target), non-negative operands.

    Build a random suffix chain, compute its right-assoc value r, prepend x0 op0.
    """
    assert length >= 1
    if length == 1:
        assert target >= 0
        return [str(target)]
    suffix = [str(rng.randrange(0, 100))]
    aops = []
    for _ in range(length - 2):
        aops.append(rng.choice("+-"))
        suffix.append(str(rng.randrange(0, 100)))
    # right fold of suffix
    r = int(suffix[-1])
    for k in range(len(aops) - 1, -1, -1):
        r = int(suffix[k]) + r if aops[k] == "+" else int(suffix[k]) - r
    if target - r >= 0:
        head = [str(target - r), "+"]
    else:
        head = [str(target + r), "-"]
    out = [head[0], head[1], suffix[0]]
    for k in range(len(aops)):
        out += [aops[k], suffix[k + 1]]
    return out


def small_divisor(rng, V):
    """Pick a small nonzero divisor of V (sign allowed via segment target)."""
    if V == 0:
        return rng.randrange(2, 10)  # anything divides 0
    cands = [d for d in range(2, 10) if V % d == 0]
    if cands:
        return rng.choice(cands)
    return 1


def build_long_expr(rng, mode, n_segments, seg_len):
    """Long expression: n_segments additive segments folded with * / (left-assoc),
    divisions engineered exact. mode: 'left' (011) or 'right' (012)."""
    segf = seg_left if mode == "left" else seg_right
    t0 = rng.randrange(2, 10)
    toks = segf(rng, t0, seg_len)
    V = t0
    for _ in range(n_segments - 1):
        if abs(V) > 50 or rng.random() < 0.5:
            d = small_divisor(rng, V)
            toks += ["/"] + segf(rng, d, seg_len)
            V //= d
        else:
            m = rng.randrange(2, 10)
            toks += ["*"] + segf(rng, m, seg_len)
            V *= m
    return toks, V
