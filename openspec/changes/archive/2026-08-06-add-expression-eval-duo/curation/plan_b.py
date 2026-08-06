"""Change B curation script (design-stage, deterministic).

Builds all 20+20 literal entries for apcs011/apcs012, with per-entry assertions:
  (a) every division exact & divisor != 0 under OUR semantics; operands non-negative
  (b) designated discrimination: vs E2 std-eval, vs wrong-assoc variant, vs E3 pattern
  (c) byte budgets, answer-distribution checks
Writes literals to literals/ and a route-agreement prediction report to report_b.json.
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from semantics import eval011_tokens, eval012_tokens, seg_left, seg_right, small_divisor, build_long_expr

BUDGET = 63488
OUT = os.path.join(HERE, "literals")
os.makedirs(OUT, exist_ok=True)


# ---------------- variant evaluators (cheat-route predictors) ----------------

def std_predict(expr):
    try:
        return eval(expr.replace("/", "//"), {"__builtins__": {}}, {})
    except Exception:
        return "CRASH"


def eval_leftvar_parens(toks):
    """Flipped precedence, additive LEFT-assoc, muldiv left, parens override.
    = what route E1 (swap-eval) computes on 012 inputs. Also 011 semantics + parens."""
    pos = 0
    def expr_():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            s = term()
            if op == "*":
                v = v * s
            else:
                if s == 0 or v % s != 0:
                    raise ZeroDivisionError  # route uses // : emulate floor instead
                v = v // s
        return v
    def term():
        nonlocal pos
        v = atom()
        while pos < len(toks) and toks[pos] in "+-":
            op = toks[pos]; pos += 1
            b = atom()
            v = v + b if op == "+" else v - b
        return v
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = expr_()
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v
    try:
        return expr_()
    except Exception:
        return "CRASH"


def leftvar_floor(toks):
    """E1 route actually floors (uses //): emulate with floor division."""
    pos = 0
    def expr_():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            s = term()
            v = v * s if op == "*" else (v // s if s != 0 else "CRASH")
            if v == "CRASH":
                raise ZeroDivisionError
        return v
    def term():
        nonlocal pos
        v = atom()
        while pos < len(toks) and toks[pos] in "+-":
            op = toks[pos]; pos += 1
            b = atom()
            v = v + b if op == "+" else v - b
        return v
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = expr_()
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v
    try:
        return expr_()
    except Exception:
        return "CRASH"


def rightvar_noparen(toks):
    """Additive right-assoc variant of 011 (the wrong-assoc mistake on 011)."""
    try:
        return eval012_tokens(toks)
    except Exception:
        return "CRASH"


def muldivright(toks, additive):
    """Classic recursive-descent bug: muldiv folded RIGHT-assoc.
    additive: 'left' (011 mistake variant) or 'right' (012 mistake variant).
    Parens honoured (012). Division floors; div-by-zero -> CRASH."""
    pos = 0
    def expr_():
        nonlocal pos
        v = term()
        if pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            rest = expr_()          # right recursion = right-assoc muldiv (the bug)
            if op == "*":
                return v * rest
            if rest == 0:
                raise ZeroDivisionError
            return v // rest
        return v
    def term():
        nonlocal pos
        atoms = [atom()]
        aops = []
        while pos < len(toks) and toks[pos] in "+-":
            aops.append(toks[pos]); pos += 1
            atoms.append(atom())
        if additive == "left":
            v = atoms[0]
            for k, op in enumerate(aops):
                v = v + atoms[k + 1] if op == "+" else v - atoms[k + 1]
            return v
        acc = atoms[-1]
        for k in range(len(aops) - 1, -1, -1):
            acc = atoms[k] + acc if aops[k] == "+" else atoms[k] - acc
        return acc
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = expr_()
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v
    try:
        return expr_()
    except Exception:
        return "CRASH"


def e3_predict(expr, our):
    """E3-naive (unpatched b012_pow.py file) prediction: crash iff additive op
    directly before '('. NOTE (design bounty F2): this characterizes ONE buggy
    implementation only — the route CLASS is lexically patchable to 20/20 and is
    co-opted as a clever solution (E3'), not bounded by this predictor."""
    import re
    if re.search(r"[+\-] \(", expr):
        return "CRASH"
    return our


def divtight(toks, additive):
    """Design-bounty F1: '/' binds tighter than '*' misconception.
    Precedence: additive (per mode) > '/' (left-assoc) > '*' (left-assoc).
    Parens honoured. Floor division; div-by-zero -> CRASH."""
    pos = 0
    def mulchain():
        nonlocal pos
        v = divchain()
        while pos < len(toks) and toks[pos] == "*":
            pos += 1
            v = v * divchain()
        return v
    def divchain():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] == "/":
            pos += 1
            d = term()
            if d == 0:
                raise ZeroDivisionError
            v = v // d
        return v
    def term():
        nonlocal pos
        atoms = [atom()]
        aops = []
        while pos < len(toks) and toks[pos] in "+-":
            aops.append(toks[pos]); pos += 1
            atoms.append(atom())
        if additive == "left":
            v = atoms[0]
            for k, op in enumerate(aops):
                v = v + atoms[k + 1] if op == "+" else v - atoms[k + 1]
            return v
        acc = atoms[-1]
        for k in range(len(aops) - 1, -1, -1):
            acc = atoms[k] + acc if aops[k] == "+" else atoms[k] - acc
        return acc
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = mulchain()
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v
    try:
        return mulchain()
    except Exception:
        return "CRASH"


def l2r(toks):
    """Design-bounty F5: strict left-to-right, all operators equal precedence."""
    try:
        v = int(toks[0])
        i = 1
        while i < len(toks):
            op, b = toks[i], int(toks[i + 1])
            if op == "+":
                v += b
            elif op == "-":
                v -= b
            elif op == "*":
                v *= b
            else:
                if b == 0:
                    return "CRASH"
                v //= b
            i += 2
        return v
    except Exception:
        return "CRASH"


def parens_std(toks):
    """Design-bounty F6: correct 012 semantics outside parens, but paren contents
    evaluated with STANDARD Python precedence ('parens = back to normal rules')."""
    pos = 0
    def expr_():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            s = term()
            if op == "*":
                v = v * s
            else:
                if s == 0:
                    raise ZeroDivisionError
                v = v // s
        return v
    def term():
        nonlocal pos
        atoms = [atom()]
        aops = []
        while pos < len(toks) and toks[pos] in "+-":
            aops.append(toks[pos]); pos += 1
            atoms.append(atom())
        acc = atoms[-1]
        for k in range(len(aops) - 1, -1, -1):
            acc = atoms[k] + acc if aops[k] == "+" else atoms[k] - acc
        return acc
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            depth = 1
            j = pos + 1
            while depth:
                if toks[j] == "(":
                    depth += 1
                elif toks[j] == ")":
                    depth -= 1
                j += 1
            inner = " ".join(toks[pos + 1:j - 1])
            pos = j
            v = std_predict(inner)
            if v == "CRASH":
                raise ValueError
            return v
        v = int(toks[pos]); pos += 1
        return v
    try:
        return expr_()
    except Exception:
        return "CRASH"


# ---------------- entry construction helpers ----------------

def check_expr_011(expr):
    toks = expr.split()
    v = eval011_tokens(toks)  # asserts exact division
    for tk in toks:
        if tk not in "+-*/()":
            assert tk.isdigit() and len(tk) <= 6, f"operand {tk}"
    return v


def check_expr_012(expr):
    toks = expr.split()
    v = eval012_tokens(toks)
    for tk in toks:
        if tk not in "+-*/()":
            assert tk.isdigit() and len(tk) <= 6, f"operand {tk}"
    return v


def med_expr(rng, mode, nseg, seglen, force_disc=True):
    """Medium seeded expression; if force_disc, retry until it discriminates
    vs std AND vs wrong-assoc variant."""
    for _ in range(400):
        toks, V = build_long_expr(rng, mode, nseg, seglen)
        expr = " ".join(toks)
        our = V
        if not force_disc:
            return expr, our
        if std_predict(expr) == our:
            continue
        if mode == "left" and rightvar_noparen(toks) == our:
            continue
        if mode == "right" and leftvar_floor(toks) == our:
            continue
        if muldivright(toks, mode) == our:
            continue
        return expr, our
    raise RuntimeError("cannot build discriminating expr")


def paren_expr(rng, depth, want_addparen=True):
    """Build a 012 paren expression with controlled nesting depth.
    Recursively: base chains, wrapped, combined. Ensures additive-op-before-paren
    when want_addparen. Returns (expr, value)."""
    def build(d):
        if d == 0:
            toks, V = build_long_expr(rng, "right", rng.randrange(1, 3), rng.randrange(2, 5))
            return toks, V
        inner, iv = build(d - 1)
        # wrap inner in parens and embed: prefix chain OP ( inner ) suffix
        pre_t = rng.randrange(0, 100)
        # additive op before paren (the E3 killer pattern)
        op = rng.choice("+-")
        toks = [str(pre_t), op, "("] + inner + [")"]
        v_in = iv
        V = pre_t + v_in if op == "+" else pre_t - v_in
        # maybe fold with a muldiv segment, division exactness engineered
        if rng.random() < 0.6:
            d2 = small_divisor(rng, V)
            if abs(V) > 30 and d2 > 1:
                toks += ["/"] + seg_right(rng, d2, rng.randrange(1, 4))
                V //= d2
            else:
                m = rng.randrange(2, 6)
                toks += ["*"] + seg_right(rng, m, rng.randrange(1, 4))
                V *= m
        return toks, V
    for _ in range(400):
        toks, V = build(depth)
        expr = " ".join(toks)
        assert eval012_tokens(toks) == V
        if want_addparen and not __import__("re").search(r"[+\-] \(", expr):
            continue
        if std_predict(expr) == V:
            continue
        if leftvar_floor(toks) == V:
            continue
        return expr, V
    raise RuntimeError("cannot build paren expr")


def big_entry(rng, mode, nseg, seglen, final_mult):
    for _ in range(50):
        toks, V = build_long_expr(rng, mode, nseg, seglen)
        segf = seg_left if mode == "left" else seg_right
        toks += ["*"] + segf(rng, final_mult, seglen)
        V *= final_mult
        if muldivright(toks, mode) == V:
            continue
        return " ".join(toks), V
    raise RuntimeError("big entry mdr coincidence")


# ---------------- entry definitions ----------------

def build_011(rng):
    E = []  # list of (exprs, answers, tags)
    add = lambda exprs, tags: E.append((exprs, [check_expr_011(e) for e in exprs], tags))

    add(["3 + 5 * 2", "10 - 4 - 3 + 2 * 6", "2 * 3 + 4", "1 - 7 / 2", "7"],
        ["example", "A1", "A2", "A4"])                                                    # 1
    add(["0", "42", "1 + 2 + 3"], ["gimme"])                                              # 2
    add(["9 - 5 - 2", "0 - 7 + 3", "50 - 60"], ["gimme-std", "A2"])                       # 3
    add(["2 + 3 * 4", "1 + 1 * 9", "5 - 1 * 10", "7 - 3 - 3 * 2", "36 / 6 * 2",
         "5 * 2 + 1", "2 * 6 / 4"], ["A1", "A2", "A3", "L2Rkill", "DTkill"])              # 4
    add(["1 - 7 / 2", "8 - 2 / 3", "0 - 4 / 2", "9 - 5 - 2 / 2", "24 / 4 / 2",
         "4 * 1 + 1", "6 * 10 / 4"], ["A4", "A2", "A3", "L2Rkill", "DTkill"])             # 5
    add(["100 / 5 * 2", "100 / 5 / 2", "3 * 4 / 6", "6 - 1 - 3 * 2", "6 / 2 + 1",
         "9 * 8 / 6"], ["A3", "A1", "A2", "L2Rkill", "DTkill"])                           # 6
    add(["6 * 0 / 7", "0 / 5 + 1 * 2", "12 - 12 * 9", "5 - 1 - 4 / 2", "8 * 6 / 4",
         "3 * 8 / 6"], ["A4-zero", "A1", "A2", "A3", "DTkill"])                           # 7
    for nseg, seglen in [(3, 5), (4, 8), (5, 12), (6, 20), (8, 30)]:                      # 8-12
        exprs = [med_expr(rng, "left", nseg, seglen)[0] for _ in range(4)]
        add(exprs, ["A1", "A2", "A4", "seeded"])
    for nseg, seglen in [(6, 60), (8, 90), (10, 120), (10, 200)]:                         # 13-16
        exprs = [med_expr(rng, "left", nseg, seglen)[0] for _ in range(2)]
        add(exprs, ["A1", "A2", "A4", "scaleM"])
    for nseg, seglen, fm in [(10, 400, 137), (12, 500, 271), (14, 550, 613), (16, 600, 997)]:  # 17-20
        expr, V = big_entry(rng, "left", nseg, seglen, fm)
        if std_predict(expr) == V:
            raise RuntimeError("big coincidence")
        add([expr], ["A5", "A1", "A2"])
    return E


def build_012(rng):
    E = []
    add = lambda exprs, tags: E.append((exprs, [check_expr_012(e) for e in exprs], tags))

    add(["10 - 4 - 3 + 2 * 6", "9 - 5 - 2", "3 + 5 * 2"], ["example", "B1", "B2"])        # 1
    add(["0", "42", "1 + 2 + 3"], ["gimme"])                                              # 2
    add(["20 - 10 - 5 - 5", "1 - 2 + 4", "7 - 3 - 3"], ["B2"])                            # 3
    add(["2 + 3 * 4", "5 - 1 * 10", "9 - 5 - 2 * 3", "36 / 6 * 2", "2 * 6 / 4"],
        ["B1", "B2", "B3", "DTkill"])                                                     # 4
    add(["12 - 20 / 4", "3 - 5 - 6 / 2", "0 - 4 / 2", "24 / 4 / 2", "6 * 10 / 4"],
        ["B4div", "B2", "B3", "DTkill"])                                                  # 5
    add(["100 / 5 * 2", "8 - 2 * 3", "30 - 10 - 8 / 4", "3 * 4 / 6"], ["B3", "B1", "B2"]) # 6
    dtk78 = ["8 * 9 / 6", "4 * 10 / 8"]
    for j, (nseg, seglen) in enumerate([(3, 6), (5, 10)]):                                # 7-8
        exprs = [med_expr(rng, "right", nseg, seglen)[0] for _ in range(4)] + [dtk78[j]]
        add(exprs, ["B1", "B2", "DTkill", "seeded"])
    add(["2 + ( 3 * 4 )", "( 2 + 3 ) * 4", "12 - ( 2 + 4 ) / 3", "( 2 + 2 * 3 ) / 4",
         "( 9 - 5 - 2 ) * 8 / 6"], ["B4", "E3kill", "PSkill", "DTkill", "PKline"])        # 9
    # paren-line + same-level 2-op muldiv + flipped-inner content:
    # kills two-code-path mdr (F3), divtight (F1) and parens-std (F6) on paren entries
    pk = ["( 2 + 2 * 3 ) * 3 / 9", "( 7 - 3 - 3 ) * 8 / 14", "( 1 + 1 * 9 ) * 9 / 6",
          "( 20 - 10 - 5 - 5 ) * 6 / 4", "( 5 - 1 - 3 ) * 12 / 21", "( 3 + 3 * 2 ) * 9 / 6",
          "( 8 - 2 - 2 ) * 3 / 12", "( 9 - 5 - 2 ) * 9 / 6", "( 2 + 1 * 4 ) * 10 / 4",
          "( 6 - 2 - 3 ) * 8 / 14", "( 4 + 2 * 5 ) * 3 / 9"]
    for j, depth in enumerate([2, 3, 4]):                                                 # 10-12
        exprs = [paren_expr(rng, depth)[0] for _ in range(3)] + [pk[j]]
        add(exprs, ["B4", "B5", "B3", "E3kill", "PKline", "seeded"])
    for j, depth in enumerate([8, 12, 18, 25]):                                           # 13-16
        exprs = [paren_expr(rng, depth)[0] for _ in range(2)] + [pk[3 + j]]
        add(exprs, ["B5", "B3", "E3kill", "PKline", "scaleM"])
    # 17-20: scale; paren line present AND carries the PKline discriminator
    for j, (nseg, seglen, fm) in enumerate([(10, 400, 149), (12, 500, 283),
                                            (14, 550, 617), (16, 600, 991)]):
        expr, V = big_entry(rng, "right", nseg, seglen, fm)
        pexpr, pV = paren_expr(rng, 3)
        exprs = [expr, pexpr, pk[7 + j]]
        vals = [V, pV, check_expr_012(pk[7 + j])]
        assert std_predict(expr) != V
        E.append((exprs, vals, ["B6", "B2", "E3kill", "PKline"]))
    return E


# ---------------- assemble, assert, report ----------------

def finalize(name, entries, mode):
    report = []
    all_answers = []
    for idx, (exprs, vals, tags) in enumerate(entries, 1):
        text = str(len(exprs)) + "\n" + "\n".join(exprs) + "\n"
        nb = len(text.encode())
        assert nb <= BUDGET, f"{name} entry {idx} bytes {nb} > {BUDGET}"
        open(os.path.join(OUT, f"{name}_{idx:02d}.txt"), "w").write(text)
        ours = [str(v) for v in vals]
        std = [str(std_predict(e)) for e in exprs]
        if mode == "left":
            wrong = [str(rightvar_noparen(e.split())) for e in exprs]
            e3 = ours  # E1 swap correct on 011 (established); e3 column reused as E1 predict
        else:
            wrong = [str(leftvar_floor(e.split())) for e in exprs]
            e3 = [str(e3_predict(e, v)) for e, v in zip(exprs, vals)]
        mdr = [str(muldivright(e.split(), "left" if mode == "left" else "right"))
               for e in exprs]
        dt = [str(divtight(e.split(), "left" if mode == "left" else "right"))
              for e in exprs]
        row = {
            "entry": idx, "tags": tags, "T": len(exprs), "bytes": nb,
            "answers": ours,
            "std_ok": std == ours,          # E2 gets this entry?
            "wrongassoc_ok": wrong == ours,  # wrong-assoc route gets this entry?
            "e3_ok": e3 == ours,            # (012) naive pow-trick file gets this entry?
            "muldivright_ok": mdr == ours,  # recursive-descent right-assoc muldiv bug
            "divtight_ok": dt == ours,      # '/' tighter than '*' misconception (F1)
        }
        if mode == "left":
            row["l2r_ok"] = [str(l2r(e.split())) for e in exprs] == ours       # F5
        else:
            row["parenstd_ok"] = [str(parens_std(e.split())) for e in exprs] == ours  # F6
            # F3 two-code-path: correct flat semantics on paren-free lines,
            # textbook muldiv-right bug on paren-containing lines
            hyb = [o if "(" not in e else str(muldivright(e.split(), "right"))
                   for e, o in zip(exprs, ours)]
            row["hybrid_ok"] = hyb == ours
        # discrimination duties
        if "gimme" not in tags and "gimme-std" not in tags:
            assert not row["std_ok"], f"{name} entry {idx} fails std-discrimination duty"
        if "gimme" not in tags and not any(t in tags for t in ("gimme-std",)):
            pass  # wrong-assoc duty asserted globally below
        all_answers += vals
        report.append(row)
    # global answer-distribution duties
    distinct = len(set(all_answers))
    assert distinct >= 15, f"{name}: only {distinct} distinct answers"
    assert any(v < 0 for v in all_answers) and any(v > 0 for v in all_answers), name
    std_score = sum(r["std_ok"] for r in report)
    wrong_score = sum(r["wrongassoc_ok"] for r in report)
    e3_score = sum(r["e3_ok"] for r in report)
    mdr_score = sum(r["muldivright_ok"] for r in report)
    dt_score = sum(r["divtight_ok"] for r in report)
    assert std_score <= 3, f"{name}: std-eval scores {std_score} > 3"
    assert wrong_score <= 4, f"{name}: wrong-assoc scores {wrong_score} > 4"
    assert mdr_score <= 4, f"{name}: muldiv-right scores {mdr_score} > 4"
    assert dt_score <= 4, f"{name}: divtight scores {dt_score} > 4"
    wrong_keys = ["std_ok", "wrongassoc_ok", "muldivright_ok", "divtight_ok"]
    if mode == "left":
        l2r_score = sum(r["l2r_ok"] for r in report)
        assert l2r_score <= 3, f"{name}: l2r scores {l2r_score} > 3"
        wrong_keys.append("l2r_ok")
        extra = {"l2r_score": l2r_score}
        union_cap = 6
    else:
        ps_score = sum(r["parenstd_ok"] for r in report)
        hyb_score = sum(r["hybrid_ok"] for r in report)
        assert ps_score <= 8, f"{name}: parens-std scores {ps_score} > 8"
        assert e3_score <= 8, f"{name}: E3-naive-file scores {e3_score} > 8"
        assert hyb_score <= 8, f"{name}: hybrid two-path scores {hyb_score} > 8"
        wrong_keys += ["parenstd_ok", "hybrid_ok"]
        extra = {"parenstd_score": ps_score, "hybrid_score": hyb_score}
        union_cap = 9  # parens-std floor is the 8 paren-free entries + 1 slack
    union = sum(any(r[k] for k in wrong_keys) for r in report)
    assert union <= union_cap, f"{name}: wrong-route union {union} > {union_cap}"
    return {"entries": report, "std_score": std_score,
            "wrongassoc_score": wrong_score, "e3_or_e1_score": e3_score,
            "muldivright_score": mdr_score, "divtight_score": dt_score,
            "wrong_union": union, "distinct_answers": distinct, **extra}


def main():
    rng_a = random.Random(1101)
    rng_b = random.Random(1202)
    ea = build_011(rng_a)
    eb = build_012(rng_b)
    ra = finalize("a", ea, "left")
    rb = finalize("b", eb, "right")
    out = {"apcs011": ra, "apcs012": rb}
    json.dump(out, open(os.path.join(HERE, "report_b.json"), "w"), indent=1)
    print(f"011: std={ra['std_score']}/20 wrongassoc={ra['wrongassoc_score']}/20 "
          f"E1swap={ra['e3_or_e1_score']}/20 distinct={ra['distinct_answers']}")
    print(f"012: std={rb['std_score']}/20 leftswap={rb['wrongassoc_score']}/20 "
          f"E3pow={rb['e3_or_e1_score']}/20 distinct={rb['distinct_answers']}")
    sizes = sorted((os.path.getsize(os.path.join(OUT, f)), f) for f in os.listdir(OUT))
    print("min/max entry bytes:", sizes[0], sizes[-1])

if __name__ == "__main__":
    main()
