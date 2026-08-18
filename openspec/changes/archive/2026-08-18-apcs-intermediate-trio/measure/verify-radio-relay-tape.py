#!/usr/bin/env python3
"""radio-relay-tape (apcs020) 本地驗證腳本。

1. 解析 frontmatter，逐筆展開 20 個 testcase_plan 條目（literal / band+override）
2. 對 20 筆各跑 generator 與 reference_solution，斷言輸出全等
3. 量每筆實際位元組數，斷言 < input_budget
4. 以與判題器 tracer 同語意的 sys.settrace（每個 trace event 加一）量測
   被砍路線的兩種拼法 + 一條對照的二分搜尋路線
5. 斷言第 2 到第 20 筆規模單調不遞減
6. 輸出 JSON 量測記錄
"""
import io
import json
import os
import pathlib
import random
import sys
import time

import yaml

REPO = str(pathlib.Path(__file__).resolve().parents[4])  # measure/ -> change/ -> changes/ -> openspec/ -> repo root
MD = os.path.join(REPO, "docs/challenge/radio-relay-tape.md")
OUT = os.path.join(
    REPO, "openspec/changes/apcs-intermediate-trio/measure/cliff-radio-relay-tape.json"
)
OP_LIMIT = 10_000_000
# 量測用硬止血點：超過就確定「死」，不必再算下去（與判題器 raise 的位置同義）
ABORT_AT = OP_LIMIT + 1
SEED = 20260818


def load_front():
    text = open(MD, encoding="utf-8").read()
    assert text.startswith("---\n")
    end = text.index("\n---\n", 3)
    return yaml.safe_load(text[4:end]), text[end + 5 :]


def deep_merge(base, patch):
    out = dict(base)
    for k, v in patch.items():
        assert k in out, f"override 引用不存在的鍵: {k}"
        if isinstance(v, dict) and isinstance(out[k], dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def render(params, rng):
    """依 params 產生一筆輸入（模擬 WASM 引擎的欄位式渲染）。"""
    drawn = {}
    lines = []
    for name, spec in params.items():
        assert spec["type"] == "int", spec["type"]
        cnt = spec.get("count")
        if cnt is None:
            k = 1
            sep = " "
        elif "from" in cnt:
            k = drawn[cnt["from"]]
            sep = cnt.get("separator", " ")
        else:
            k = rng.randint(cnt["min"], cnt["max"])
            sep = cnt.get("separator", " ")
        vals = [rng.randint(spec["min"], spec["max"]) for _ in range(k)]
        if cnt is None:
            drawn[name] = vals[0]
        if k == 0:
            continue
        lines.append(sep.join(map(str, vals)))
    return "\n".join(lines) + "\n"


def run_python(code, stdin_text):
    old_in, old_out = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(stdin_text)
    sys.stdout = buf = io.StringIO()
    try:
        exec(compile(code, "<sol>", "exec"), {"__name__": "__main__"})
    finally:
        sys.stdin, sys.stdout = old_in, old_out
    return buf.getvalue()


# ── 與 worker-utils.ts 的 _tracer 同語意：每個 trace event 加一 ──────────
class OpLimit(Exception):
    pass


def measure(fn, *args):
    """回傳 (ops, exceeded)。fn 內部的每個 trace event 計一次。"""
    state = {"n": 0}
    limit = ABORT_AT

    def tracer(frame, event, arg):
        state["n"] += 1
        if state["n"] > limit:
            raise OpLimit()
        return tracer

    t0 = time.time()
    old_trace = sys.gettrace()
    sys.settrace(tracer)
    try:
        fn(*args)
        exceeded = False
    except OpLimit:
        exceeded = True
    finally:
        sys.settrace(old_trace)
    return state["n"], exceeded, time.time() - t0


# ── 被砍路線：拼法 A（逐元素 Python 迴圈） ──────────────────────────────
def brute_elementwise(n, a):
    best = 0
    for i in range(n):
        seen = set()
        j = i
        while j < n and a[j] not in seen:
            seen.add(a[j])
            j += 1
        if j - i > best:
            best = j - i
    return best


# ── 被砍路線：拼法 B（用 C 內建 set，但延伸仍由 Python 驅動） ──────────
def brute_setslice(n, a):
    best = 0
    for i in range(n):
        m = 0
        while i + m < n and len(set(a[i : i + m + 1])) == m + 1:
            m += 1
        if m > best:
            best = m
    return best


# ── 對照：應該要活的路線（每個起點二分搜尋 + len(set(切片))） ───────────
def bisect_route(n, a):
    best = 0
    for i in range(n):
        lo, hi = 0, n - i
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if len(set(a[i : i + mid])) == mid:
                lo = mid
            else:
                hi = mid - 1
        if lo > best:
            best = lo
    return best


def run_profile(n, a):
    """O(n) 算出 S = 各起點延伸長度總和、B = best 嚴格變大的次數。

    兩個被砍拼法的 trace event 數都是 S 與 n 的閉式：
      elementwise_loop     ops = 3S + 5n + B + 8
      c_builtin_set_slice  ops = 2S + 4n + B + 8
    （+8 = 受測函式的 call/return 兩個 event 加上量測包裝函式的三個 event，
      再加上 best = 0 與 return best 兩行、以及 for 的收尾那一次）
    這兩條式子在所有沒有中止的條目上逐筆與實測值比對，全等才採用。
    """
    nxt = {}
    limit = n
    runs = [0] * n
    for i in range(n - 1, -1, -1):
        v = a[i]
        f = nxt.get(v)
        if f is not None and f < limit:
            limit = f
        nxt[v] = i
        runs[i] = limit - i
    S = sum(runs)
    best = 0
    B = 0
    for L in runs:
        if L > best:
            best = L
            B += 1
    return S, B


def score(flags):
    """判題語意：逐筆跑，第一筆超限即整場停止，得分 = 之前通過的筆數。"""
    passed = 0
    for ok in flags:
        if ok:
            passed += 1
        else:
            break
    return passed


def main():
    fm, body = load_front()
    base = fm["params"]
    budget = fm["input_budget"]
    plan = fm["testcase_plan"]
    assert "testcase_count" not in fm, "不可同時宣告 testcase_count"
    assert budget < 65536, budget
    assert len(plan) == 20, len(plan)

    # params 硬性約束
    for name, spec in base.items():
        assert isinstance(spec["min"], int) and isinstance(spec["max"], int)
        assert spec["type"] != "group"
    for e in plan[1:]:
        for name, patch in e.get("override", {}).items():
            assert patch["min"] == patch["max"], (name, patch)

    # 第 1 筆 literal 必須與題面〈範例〉輸入區塊逐字相同
    ex = body.split("**輸入：**", 1)[1].split("```", 2)
    example_input = ex[1].lstrip("\n")
    assert plan[0]["literal"] == example_input, repr((plan[0]["literal"], example_input))
    print(f"[1] literal == 題面範例輸入區塊: True\n{example_input}")

    rng = random.Random(SEED)
    entries = []
    scales = []
    for idx, e in enumerate(plan, start=1):
        if "literal" in e:
            stdin_text = e["literal"]
            n = int(stdin_text.split("\n")[0])
            kind = "literal"
        else:
            assert e["count"] == 1, e["count"]
            merged = deep_merge(base, e.get("override", {}))
            stdin_text = render(merged, rng)
            n = merged["n"]["min"]
            scales.append(n)
            kind = "band"
        entries.append({"entry": idx, "kind": kind, "n": n, "stdin": stdin_text})

    # 5. 單調不遞減（第 2 到第 20 筆）
    monotonic = all(scales[i] <= scales[i + 1] for i in range(len(scales) - 1))
    print(f"[5] 第 2..20 筆規模: {scales}")
    print(f"[5] 單調不遞減: {monotonic}")
    assert monotonic

    # 2 + 3
    agreement = True
    max_bytes = 0
    for ent in entries:
        b = len(ent["stdin"].encode("utf-8"))
        ent["bytes"] = b
        max_bytes = max(max_bytes, b)
        assert b < budget, (ent["entry"], b, budget)
        g = run_python(fm["generator"], ent["stdin"])
        r = run_python(fm["reference_solution"], ent["stdin"])
        ent["expected"] = g.strip()
        ok = g == r
        agreement = agreement and ok
        assert ok, (ent["entry"], g, r)
        print(
            f"[2/3] 第 {ent['entry']:>2} 筆 n={ent['n']:>5} bytes={b:>6} "
            f"answer={g.strip():>5} generator==reference: {ok}"
        )
    print(f"[3] 最大位元組={max_bytes} < input_budget={budget}: {max_bytes < budget}")

    # 4. 三條路線逐筆量測
    routes = [
        ("elementwise_loop", brute_elementwise, True, lambda S, B, n: 3 * S + 5 * n + B + 8),
        ("c_builtin_set_slice", brute_setslice, True, lambda S, B, n: 2 * S + 4 * n + B + 8),
        ("binary_search_set_slice", bisect_route, False, None),
    ]
    for ent in entries:
        a = list(map(int, ent["stdin"].split("\n")[1].split()))
        ent["S"], ent["B"] = run_profile(ent["n"], a)
    results = {}
    for label, fn, must_die, formula in routes:
        per = []
        for ent in entries:
            a = list(map(int, ent["stdin"].split("\n")[1].split()))
            n = ent["n"]
            holder = {}

            def work(n=n, a=a, fn=fn, holder=holder):
                holder["v"] = fn(n, a)

            ops, exceeded, secs = measure(work)
            rec = {
                "entry": ent["entry"],
                "n": n,
                "ops_measured": ops,
                "exceeded": exceeded,
                "seconds": round(secs, 3),
            }
            if formula is not None:
                full = formula(ent["S"], ent["B"], n)
                rec["ops_full"] = full
                rec["ops_full_source"] = "measured" if not exceeded else "closed form"
                if not exceeded:
                    # 沒中止的條目：閉式必須與實測值全等，閉式才可信
                    assert full == ops, (label, ent["entry"], full, ops)
                else:
                    assert full > OP_LIMIT, (label, ent["entry"], full)
            if not exceeded:
                assert str(holder["v"]) == ent["expected"], (label, ent["entry"])
            per.append(rec)
            print(
                f"[4] {label:<24} 第 {ent['entry']:>2} 筆 n={n:>5} "
                f"ops={ops:>10} 完整ops={rec.get('ops_full', ops):>11} "
                f"超限={exceeded} {secs:.2f}s"
            )
            sys.stdout.flush()
        flags = [not p["exceeded"] for p in per]
        dead = [p["entry"] for p in per if p["exceeded"]]
        sc = score(flags)
        # 死的必須是連續後段
        contiguous_tail = dead == list(range(dead[0], 21)) if dead else True
        results[label] = {
            "per_entry": per,
            "dead_entries": dead,
            "score": f"{sc}/20",
            "ops_last_entry_measured": per[-1]["ops_measured"],
            "ops_last_entry_full": per[-1].get("ops_full", per[-1]["ops_measured"]),
            "seconds_last_entry_cpython": per[-1]["seconds"],
            "dead_is_contiguous_tail": contiguous_tail,
        }
        if must_die:
            assert dead, f"{label} 沒有任何一筆超限（規模不足）"
            assert len(dead) < 20, f"{label} 全部超限"
            assert contiguous_tail, f"{label} 超限的筆數不是連續後段: {dead}"
            assert 1 <= sc <= 19, f"{label} 得分 {sc} 不在部分分區間"
        else:
            print(f"[4] 對照路線 {label} 得分 {sc}/20（預期 20/20）")

    record = {
        "slug": "radio-relay-tape",
        "id": "apcs020",
        "question": "最長的一段連續且歌曲兩兩相異的區段長度",
        "op_limit": OP_LIMIT,
        "abort_at": ABORT_AT,
        "seed": SEED,
        "input_budget": budget,
        "max_input_bytes": max_bytes,
        "generator_reference_agreement": agreement,
        "scale_monotonic": monotonic,
        "staircase_entries_2_to_20": scales,
        "entries": [
            {
                "entry": e["entry"],
                "kind": e["kind"],
                "n": e["n"],
                "bytes": e["bytes"],
                "expected_output": e["expected"],
                "sum_of_run_lengths": e["S"],
            }
            for e in entries
        ],
        "routes": results,
        "notes": [
            "ops 以與 .vitepress/theme/workers/worker-utils.ts 的 _tracer 同語意的 "
            "sys.settrace 計數（每個 trace event 加一）。",
            "ops_measured 在計數超過 10,000,001 時中止，與判題器 raise TimeoutError 的位置"
            "相同，因此超限條目的 ops_measured 是下界而非總量。",
            "ops_full 為閉式：elementwise_loop = 3S + 5n + B + 8、"
            "c_builtin_set_slice = 2S + 4n + B + 8，S 為各起點延伸長度總和、B 為 best 嚴格"
            "變大的次數。閉式在全部未中止的條目上與實測值逐筆全等（腳本 assert），"
            "因此超限條目的 ops_full 可信。",
            "seconds 為 CPython 3.13 的牆鐘（含 settrace 負擔），非 Pyodide 判題耗時；"
            "c_builtin_set_slice 在 n = 1500 就已經超過 5000 ms 的 deadline，"
            "代表這條拼法在正式判題中兩道閘門都會觸發。",
            "斷崖穩健度：本題的成本正比於「各起點延伸長度總和」，該量在值域 1..1000000 下的"
            "逐筆相對標準差約 0.20 到 0.25。因此階梯刻意在 n = 2500 與 n = 4600 之間跳過"
            "門檻帶：n <= 2570 時 steps <= n(n+1)/2 使 elementwise_loop 必然低於一千萬"
            "（確定性上界），而 n >= 6700 的條目在 500 次抽樣模擬中 c_builtin_set_slice "
            "的致死率約 0.97 到 0.99。整條階梯「超限筆數為連續後段」的模擬機率為 "
            "elementwise_loop 1.000、c_builtin_set_slice 0.950。",
        ],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"\n[JSON] 寫入 {OUT}")
    print(json.dumps({k: v["score"] for k, v in results.items()}, ensure_ascii=False))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
