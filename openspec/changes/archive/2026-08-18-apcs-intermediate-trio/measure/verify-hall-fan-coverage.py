#!/usr/bin/env python3
"""Local verification harness for docs/challenge/hall-fan-coverage.md.

Every number this prints is measured, never projected:
  1. parse the frontmatter, walk all 20 testcase_plan entries, materialise a
     real input for each band by applying its override to the base params
  2. run `generator` and `reference_solution` on all 20 inputs, assert equal
  3. measure actual bytes per entry, assert every one is under input_budget
     (and assert the engine's worst-case estimate also fits the budget)
  4. measure both spellings of the killed route with a sys.settrace counter
     whose semantics match .vitepress/theme/workers/worker-utils.ts (one count
     per trace event), per entry
  5. assert entries 2..20 are monotonically non-decreasing in scale
  6. write the per-entry ops + projected scores to the change's measure dir

Nothing here is allowed to fail quietly: every assertion carries its numbers.
"""

import io
import json
import os
import pathlib
import random
import subprocess
import sys
import tempfile

import yaml

REPO = str(pathlib.Path(__file__).resolve().parents[4])  # measure/ -> change/ -> changes/ -> openspec/ -> repo root
MD = os.path.join(REPO, "docs/challenge/hall-fan-coverage.md")
OUT = os.path.join(
    REPO, "openspec/changes/apcs-intermediate-trio/measure/cliff-hall-fan-coverage.json"
)
OP_LIMIT = 10_000_000
HARD_CAP = 65536


# ── frontmatter ──────────────────────────────────────────────────────────────
def load_frontmatter(path):
    text = open(path, encoding="utf-8").read()
    assert text.startswith("---\n"), "no frontmatter"
    end = text.index("\n---\n", 3)
    fm = yaml.safe_load(text[4:end])
    body = text[end + 5 :]
    return fm, body


# ── input generation (mirrors the engine's declaration-order, one line per
#    param, count.from binding to a previously generated scalar int) ─────────
def gen_input(params, seed):
    rng = random.Random(seed)
    scalars = {}
    lines = []
    for name, spec in params.items():
        assert spec["type"] == "int", f"{name}: harness only handles int"
        assert isinstance(spec["min"], int) and isinstance(spec["max"], int)
        count = spec.get("count")
        if count is None:
            n, sep = 1, ""
        elif "from" in count:
            src = count["from"]
            assert src in scalars, f"{name}: count.from {src} not a prior scalar"
            n, sep = scalars[src], count["separator"]
        else:
            assert count["min"] == count["max"], f"{name}: count not pinned"
            n, sep = count["min"], count["separator"]
        vals = [rng.randint(spec["min"], spec["max"]) for _ in range(n)]
        if count is None:
            scalars[name] = vals[0]
        lines.append(sep.join(str(v) for v in vals))
    return "\n".join(lines) + "\n"


def engine_inputs(fm):
    """The twenty plan inputs as produced by the real Rust/WASM engine, seeded
    by the slug exactly as scripts/generate-pools.ts seeds a pool build. A
    Python replica of the generator would be a different quantity: these are
    the bytes the student's submission actually receives."""
    here = os.path.dirname(os.path.abspath(__file__))
    spec = dict(
        params=fm["params"],
        seed="hall-fan-coverage",
        input_budget=fm["input_budget"],
        testcase_plan=fm["testcase_plan"],
    )
    with tempfile.TemporaryDirectory() as d:
        sp, op = os.path.join(d, "spec.json"), os.path.join(d, "out.json")
        with open(sp, "w", encoding="utf-8") as fh:
            json.dump(spec, fh)
        subprocess.run(
            ["npx", "--no-install", "tsx", os.path.join(here, "gen-real-inputs.mjs"), sp, op],
            cwd=REPO,
            check=True,
        )
        return json.load(open(op, encoding="utf-8"))


def merge(base, override):
    out = {k: dict(v) for k, v in base.items()}
    for name, patch in (override or {}).items():
        assert name in out, f"override names unknown param {name}"
        out[name].update(patch)
    return out


# ── engine worst-case byte estimate (mirrors parser.rs estimate_input_bytes) ──
def int_width(lo, hi):
    return max(len(str(lo)), len(str(hi)))


def worst_case_bytes(params):
    refs, total, first = {}, 0, True
    for name, spec in params.items():
        if not first:
            total += 1  # newline between top-level blocks
        first = False
        count = spec.get("count")
        if count is None:
            cmax, seplen = 1, 0
        elif "from" in count:
            cmax, seplen = refs[count["from"]], len(count["separator"])
        else:
            cmax, seplen = count["max"], len(count["separator"])
        w = int_width(spec["min"], spec["max"])
        total += max(w, 1) * cmax + seplen * max(cmax - 1, 0)
        if count is None:
            refs[name] = spec["max"]
    return total


# ── running Python programs the way the judge does ───────────────────────────
# NOT an isolation boundary. This is a plain import prelude prepended to code
# that comes from this repo's own challenge frontmatter, and it runs with the
# harness's full privileges. Do not copy this pattern anywhere the code is
# untrusted. It also shifts every traceback line number by the prelude length.
PRELUDE = """
import sys
import sys as _sys
import io
"""


def run_plain(code, stdin_text):
    g = {"__name__": "__main__"}
    old_in, old_out = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(stdin_text)
    sys.stdout = io.StringIO()
    try:
        exec(compile(PRELUDE + code, "<challenge-frontmatter>", "exec"), g)
        return sys.stdout.getvalue()
    finally:
        sys.stdout, sys.stdin = old_out, old_in


TRACED_WRAPPER = """
import sys
import io

_op_count = 0

def _tracer(frame, event, arg):
    global _op_count
    _op_count += 1
    return _tracer

sys.settrace(_tracer)
sys._getframe().f_trace = _tracer

sys.stdin = _the_stdin
_captured_stdout = io.StringIO()
sys.stdout = _captured_stdout

{USER}

sys.settrace(None)
_output = _captured_stdout.getvalue()
"""


def run_traced(code, stdin_text):
    """Count trace events exactly as worker-utils.ts's tracer does: the tracer
    is installed globally AND attached to the current frame, and the user code
    runs flat in that same module frame. The op limit is NOT enforced here so
    that the full count is observable; the verdict is derived by comparison."""
    src = TRACED_WRAPPER.replace("{USER}", code.rstrip("\n"))
    g = {"_the_stdin": io.StringIO(stdin_text)}
    old_in, old_out, old_trace = sys.stdin, sys.stdout, sys.gettrace()
    try:
        exec(compile(src, "<challenge-frontmatter>", "exec"), g)
    finally:
        sys.settrace(old_trace)
        sys.stdout, sys.stdin = old_out, old_in
    return g["_op_count"], g["_output"]


# ── the two spellings of the killed route ────────────────────────────────────
READ = """rows, cols = map(int, input().split())
f = int(input())
tops = list(map(int, input().split()))
lefts = list(map(int, input().split()))
heights = list(map(int, input().split()))
widths = list(map(int, input().split()))
grid = [[0] * (cols + 2) for _ in range(rows + 2)]
"""

TAIL = """best = 0
for r in range(1, rows + 1):
    m = max(grid[r])
    if m > best:
        best = m
print(best)
"""

NESTED = READ + """for i in range(f):
    r0 = tops[i]
    c0 = lefts[i]
    r1 = r0 + heights[i]
    c1 = c0 + widths[i]
    for r in range(r0, r1):
        for c in range(c0, c1):
            grid[r][c] += 1
""" + TAIL

SLICED = READ + """for i in range(f):
    r0 = tops[i]
    c0 = lefts[i]
    r1 = r0 + heights[i]
    c1 = c0 + widths[i]
    for r in range(r0, r1):
        row = grid[r]
        row[c0:c1] = [x + 1 for x in row[c0:c1]]
""" + TAIL

SPELLINGS = [("nested-loop", NESTED), ("slice-assign", SLICED)]


def main():
    fm, body = load_frontmatter(MD)
    base = fm["params"]
    budget = fm["input_budget"]
    plan = fm["testcase_plan"]

    print(f"challenge: {fm['id']} {fm['title']}")
    print(f"input_budget = {budget}  (hard cap {HARD_CAP})")
    assert budget < HARD_CAP, f"input_budget {budget} must be < {HARD_CAP}"
    assert "testcase_count" not in fm, "testcase_count must be absent"
    assert len(plan) == 20, f"plan has {len(plan)} entries, expected 20"

    # every min/max a literal constant, no group, count.from field-wise
    for name, spec in base.items():
        assert spec["type"] != "group", f"{name}: group is forbidden"
        assert isinstance(spec["min"], int) and isinstance(spec["max"], int)
        c = spec.get("count")
        if c and "from" in c:
            assert c["separator"] == " ", f"{name}: separator must be a space"

    # ── literal vs the challenge text's example block ────────────────────────
    literal = plan[0]["literal"]
    ex = body.split("### 範例")[1].split("**輸入：**")[1].split("```")[1]
    ex = ex.lstrip("\n")
    assert literal == ex, f"literal != example block\n{literal!r}\n{ex!r}"
    print("entry 1 literal == 範例 input block: byte-for-byte identical  OK")

    engine = engine_inputs(fm)
    assert len(engine) == 20, f"engine returned {len(engine)} inputs"
    assert engine[0] == literal, (
        f"engine entry 1 != literal\n{engine[0]!r}\n{literal!r}"
    )
    print("engine-generated entry 1 == literal  OK")

    rows = []
    scales = []
    for i, entry in enumerate(plan, start=1):
        if "literal" in entry:
            params, text, scale = None, engine[0], None
        else:
            assert entry["count"] == 1, f"entry {i}: count must be 1"
            params = merge(base, entry.get("override"))
            # every scale parameter (the ones a band overrides, plus the floor
            # size) must be pinned: min == max
            for nm in ("rc", "f"):
                sp = params[nm]
                assert sp["min"] == sp["max"], (
                    f"entry {i}: {nm} not pinned ({sp['min']}..{sp['max']})"
                )
            assert set((entry.get("override") or {})) == {"f"}, (
                f"entry {i}: override must touch only f, got "
                f"{sorted(entry.get('override') or {})}"
            )
            scale = params["f"]["min"]
            text = engine[i - 1]
            # cross-check the engine's bytes against the merged declaration
            replica = gen_input(params, f"apcs018-{i}")
            assert [len(l.split(" ")) for l in text.rstrip("\n").split("\n")] == [
                len(l.split(" ")) for l in replica.rstrip("\n").split("\n")
            ], f"entry {i}: engine input shape differs from the merged params"
            scales.append(scale)

        nbytes = len(text.encode("utf-8"))
        wc = worst_case_bytes(params) if params else nbytes
        assert nbytes < budget, f"entry {i}: {nbytes} bytes >= budget {budget}"
        assert wc <= budget, f"entry {i}: worst-case {wc} > budget {budget}"

        # in-bounds guarantee: r_max + h_max - 1 <= R, c_max + w_max - 1 <= C
        if params:
            R = params["rc"]["max"]
            C = params["rc"]["max"]
            rb = params["tops"]["max"] + params["heights"]["max"] - 1
            cb = params["lefts"]["max"] + params["widths"]["max"] - 1
            assert rb <= R, f"entry {i}: row overflow {rb} > {R}"
            assert cb <= C, f"entry {i}: col overflow {cb} > {C}"
        else:
            rb = cb = R = C = None

        # the guarantee the problem text makes, checked on the actual bytes
        ls = text.rstrip("\n").split("\n")
        RR, CC = map(int, ls[0].split())
        tp = list(map(int, ls[2].split()))
        lf = list(map(int, ls[3].split()))
        hh = list(map(int, ls[4].split()))
        ww = list(map(int, ls[5].split()))
        worst_r = max(t + h - 1 for t, h in zip(tp, hh))
        worst_c = max(c + w - 1 for c, w in zip(lf, ww))
        assert worst_r <= RR, f"entry {i}: a rectangle runs to row {worst_r} > {RR}"
        assert worst_c <= CC, f"entry {i}: a rectangle runs to col {worst_c} > {CC}"

        g_out = run_plain(fm["generator"], text)
        r_out = run_plain(fm["reference_solution"], text)
        assert g_out == r_out, f"entry {i}: generator {g_out!r} != ref {r_out!r}"

        ops = {}
        for label, code in SPELLINGS:
            n, out = run_traced(code, text)
            assert out == g_out, f"entry {i} {label}: wrong answer {out!r}"
            ops[label] = n

        rows.append(
            dict(
                entry=i,
                f=scale,
                bytes=nbytes,
                worst_case_bytes=wc,
                answer=g_out.strip(),
                inbounds_row=None if rb is None else f"{rb} <= {R}",
                inbounds_col=None if cb is None else f"{cb} <= {C}",
                observed_deepest_row=f"{worst_r} <= {RR}",
                observed_rightmost_col=f"{worst_c} <= {CC}",
                ops=ops,
            )
        )
        print(
            f"  entry {i:2d}  f={str(scale):>5}  bytes={nbytes:>5} (wc {wc:>5})  "
            f"ans={g_out.strip():>3}  agree=OK  "
            + "  ".join(
                f"{k}={v:>10}{'*' if v > OP_LIMIT else ' '}" for k, v in ops.items()
            )
        )

    # ── monotonic scale over entries 2..20 ───────────────────────────────────
    mono = all(b >= a for a, b in zip(scales, scales[1:]))
    assert mono, f"scale not monotonic: {scales}"
    print(f"scale of entries 2..20 monotonic non-decreasing: {scales}  OK")

    # ── cliff assertions, per spelling ───────────────────────────────────────
    summary = {}
    for label, _ in SPELLINGS:
        seq = [r["ops"][label] for r in rows]
        dead = [r["entry"] for r in rows if r["ops"][label] > OP_LIMIT]
        alive = [r["entry"] for r in rows if r["ops"][label] <= OP_LIMIT]
        assert dead, f"{label}: no entry exceeds {OP_LIMIT} — scale too small"
        assert alive, f"{label}: every entry exceeds {OP_LIMIT} — scale too large"
        assert dead == list(range(dead[0], 21)), (
            f"{label}: dead entries {dead} are not a contiguous tail"
        )
        score = len(alive)
        assert 1 <= score <= 19, f"{label}: score {score}/20 outside 1..19"
        summary[label] = dict(
            dead_entries=dead,
            score=f"{score}/20",
            ops_last_entry=seq[-1],
            ops_first_dead=rows[dead[0] - 1]["ops"][label],
            per_entry_ops=seq,
        )
        print(
            f"{label:>13}: dead={dead}  score={score}/20  "
            f"last-entry ops={seq[-1]}"
        )

    payload = dict(
        slug="hall-fan-coverage",
        id=fm["id"],
        op_limit=OP_LIMIT,
        input_budget=budget,
        hard_cap=HARD_CAP,
        measured_with="CPython " + sys.version.split()[0]
        + " sys.settrace, one count per trace event (same semantics as"
        " .vitepress/theme/workers/worker-utils.ts)",
        inputs_from="testcase-generator WASM (seed 'hall-fan-coverage'),"
        " the same engine and seed scripts/generate-pools.ts uses",
        generator_reference_agreement="all 20 entries equal",
        max_actual_bytes=max(r["bytes"] for r in rows),
        max_worst_case_bytes=max(r["worst_case_bytes"] for r in rows),
        scale_monotonic=mono,
        spellings=summary,
        entries=rows,
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"max actual bytes = {payload['max_actual_bytes']} < budget {budget}  OK")
    print(f"max worst-case bytes = {payload['max_worst_case_bytes']} <= budget {budget}  OK")
    print(f"written: {OUT}")


if __name__ == "__main__":
    main()
