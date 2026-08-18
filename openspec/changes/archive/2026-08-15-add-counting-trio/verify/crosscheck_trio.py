"""add-counting-trio 交叉檢查器 — 獨立復現三題策展證物的得分。

這支程式**不匯入** curation/semantics0*.py，期望輸出全部由本檔自己重寫一份獨立實作，
再對 n 小的情形以「真的枚舉」的暴力法二次確認。這樣路線得分才是獨立復現，不是把
原作者的語意正本抄一遍。

執行：
    python3 crosscheck_trio.py            三題全跑（含 apcs015 的逾時路線，約需數分鐘）
    python3 crosscheck_trio.py --fast     跳過 apcs015 的兩條必逾時路線
    python3 crosscheck_trio.py --only 016 只跑其中一題

輸出：逐路線得分表 + 與各代理宣稱值的差異；並把原始資料落盤到 verify/crosscheck.json。
"""
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CUR = os.path.abspath(os.path.join(HERE, os.pardir, "curation"))
ROUTES = os.path.join(CUR, "routes")
OUT = os.path.join(CUR, "out")

KILL_TIMEOUT_S = 10
PYODIDE_FACTOR = 4
DEADLINE_MS = 5000
OP_LIMIT = 10_000_000
MOD = 1000000007

# 各代理回報的宣稱得分（用來逐條比對，不參與計算）
# apcs015 於 2026-08-15 把 n 上界由 3000 下修為 1000（op 刀鋒），20 筆 literal 全部重挑，
# 並新增第三種 O(n^2) 寫法 r015_rowscan_helper.py。以下為重挑後 measure/routes015.json 的
# 原始得分（不計 deadline／op 上限）；瀏覽器投影得分見 CLAIMED_PROJ。
CLAIMED = {
    "r015_ref_formula.py": 20, "r015_rowscan.py": 20, "r015_rowscan_sum.py": 20,
    "r015_rowscan_helper.py": 20,
    "r015_cellscan.py": 10, "r015_w1_ordered.py": 1, "r015_w2_nosub.py": 2,
    "r015_w3_guard.py": 2, "r015_w4_zerobased.py": 0,
    # r015_u1_factorial 的**原始**得分不穩定，刻意不比對（None = 不比對）：
    # entry 9/10（n = 249/250）本機耗時 7.7–8.5 s，剛好貼著量測硬逾時 10 s，
    # 量到 8/20 或 10/20 只看那一次有沒有擠進 cap，與題目性質無關。
    # 穩定且有意義的數字是瀏覽器投影得分 8/20，見 CLAIMED_PROJ（兩支工具一致）。
    "r015_u1_factorial.py": None,
    "r016_ref_pow3.py": 20, "r016_a1_loop.py": 20, "r016_a2_bigint.py": 20,
    "r016_w1_ignore_k.py": 2, "r016_w2_use_k.py": 0, "r016_w3_plain_diff.py": 0,
    "r016_w4_nomod.py": 6,
    # r017 於 2026-08-15 重挑 20 筆 literal（把亂猜路線壓到題目結構允許的最低分），
    # 以下為重挑後 measure/report017.json 的得分；u1 為「不計時間」的原始得分，
    # 計入 5000 ms deadline 後的存活分是 13（見 measure/routes017.json）。
    "r017_ref.py": 20, "r017_divmod.py": 20, "r017_helper.py": 20,
    "r017_w1_decimal.py": 2, "r017_w2_forgot_half.py": 11, "r017_w3_only_v3.py": 11,
    "r017_w4_only_half_v2.py": 12, "r017_u1_factorial.py": 14,
}
# 代理另外宣稱的「瀏覽器投影得分」（apcs015 專用；None = 未宣稱）
CLAIMED_PROJ = {
    "r015_ref_formula.py": 20, "r015_rowscan.py": 20, "r015_rowscan_sum.py": 20,
    "r015_rowscan_helper.py": 20, "r015_cellscan.py": 8, "r015_u1_factorial.py": 8,
}


# ══ 獨立的期望輸出實作（不引用 curation 的任何模組） ═══════════════════

# ── apcs015 ──────────────────────────────────────────────────────────
# 8 種偏移分成 4 個「互為相反向」的類別，每類取代表 (dr, dc) 且 dr > 0。
_A15_CLASSES = ((1, 2), (1, -2), (2, 1), (2, -1))


def a15_line(k):
    """獨立寫法：總無序對 - 干擾對。干擾對按 4 個代表偏移逐一數，負值夾成 0。"""
    t = k * k
    bad = 0
    for dr, dc in _A15_CLASSES:
        rows = k - abs(dr)
        cols = k - abs(dc)
        if rows > 0 and cols > 0:
            bad += rows * cols
    return t * (t - 1) // 2 - bad


def a15_line_brute(k):
    """最直白的定義式：攤平所有格子、枚舉每一個無序對、逐對比對 8 種偏移。"""
    offs = {(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)}
    cells = [(r, c) for r in range(k) for c in range(k)]
    m = len(cells)
    total = 0
    for i in range(m):
        r1, c1 = cells[i]
        for j in range(i + 1, m):
            r2, c2 = cells[j]
            if (r2 - r1, c2 - c1) not in offs:
                total += 1
    return total


def a15_expected(n):
    return "\n".join(str(a15_line(k)) for k in range(1, n + 1))


# ── apcs016 ──────────────────────────────────────────────────────────
def a16_expected_val(n, k):
    """獨立寫法：用平方乘冪自己寫一次，不呼叫三參數 pow。"""
    e = n - k
    base = 2 % MOD
    r = 1
    while e:
        if e & 1:
            r = r * base % MOD
        base = base * base % MOD
        e >>= 1
    return r


def a16_expected_brute(n, k):
    """真的把每一種畫面列舉出來再數（只跑小 n）。"""
    seen = set()
    for mask in range(1 << n):
        pic = tuple((mask >> i) & 1 for i in range(n))
        if any(pic[b] for b in range(k)):
            continue
        seen.add(pic)
    return len(seen) % MOD


def a16_expected(n, k):
    return str(a16_expected_val(n, k))


# ── apcs017 ──────────────────────────────────────────────────────────
def a17_share(n, p):
    """獨立寫法：不斷把 n 折下去累加（與 curation 的 while q<=n 版本寫法不同）。"""
    total = 0
    while n:
        n //= p
        total += n
    return total


def a17_expected_val(n):
    return min(a17_share(n, 2) // 2, a17_share(n, 3))


def a17_expected_brute(n):
    """題面規則的逐字翻譯：真的把 n! 算出來再反覆整批換掉。"""
    tokens = math.factorial(n)
    lv = 0
    while tokens % 12 == 0:
        tokens //= 12
        lv += 1
    return lv


def a17_expected(n):
    return str(a17_expected_val(n))


# ══ YAML literal 解析（獨立於產生它的程式） ══════════════════════════
def load_literals(path):
    """用 PyYAML 解析 out/*.yaml，回傳 testcase_plan 的 literal 字串清單。"""
    import yaml
    with open(path) as fh:
        doc = yaml.safe_load(fh)
    return [e["literal"] for e in doc["testcase_plan"]]


# ══ 路線執行 ═════════════════════════════════════════════════════════
def run_route(fname, stdin, timeout=KILL_TIMEOUT_S):
    path = os.path.join(ROUTES, fname)
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, path], input=stdin, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, timeout * 1000.0, "timeout"
    ms = (time.perf_counter() - t0) * 1000.0
    if p.returncode != 0:
        err = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "returncode=%d" % p.returncode
        return None, ms, "error:" + err[:80]
    return p.stdout.rstrip("\n"), ms, "ok"


# op 計數委派給 judge_ops.py——本 change 唯一允許的量測來源。
# 本檔對「期望輸出」保持獨立重寫（那是交叉檢查的意義），但對「一個 op 是什麼」
# 不做第二種定義：多份 tracer 定義正是上一輪的頭號缺陷。
OP_HARNESS = r'''
import sys
sys.path.insert(0, %(verify)r)
from judge_ops import count_ops_source
with open(%(path)r) as fh:
    src = fh.read()
ops, _out = count_ops_source(src, %(stdin)r, %(path)r)
print(ops)
'''


def count_ops(fname, stdin, timeout=KILL_TIMEOUT_S):
    code = OP_HARNESS % {"stdin": stdin, "path": os.path.join(ROUTES, fname),
                         "verify": HERE}
    try:
        p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        return None
    return int(p.stdout.strip())


def score_routes(tag, literals, expected_of, route_files, skip=(), want_ops=()):
    """跑一組路線 × 全部 literal，回傳逐路線紀錄。"""
    exps = [expected_of(lit) for lit in literals]
    recs = []
    for fname in route_files:
        if fname in skip:
            recs.append({"file": fname, "skipped": True})
            print("  %-26s SKIPPED" % fname)
            continue
        marks, times, ops, statuses = [], [], [], []
        for lit, exp in zip(literals, exps):
            got, ms, st = run_route(fname, lit)
            marks.append(st == "ok" and got == exp)
            times.append(round(ms, 2))
            statuses.append(st)
            o = None
            if fname in want_ops and st == "ok" and ms < 1500:
                o = count_ops(fname, lit)
            ops.append(o)
        proj = [bool(m) and t * PYODIDE_FACTOR <= DEADLINE_MS
                and (o is None or o <= OP_LIMIT)
                for m, t, o in zip(marks, times, ops)]
        rec = {
            "file": fname, "skipped": False,
            "score": sum(marks), "projected": sum(proj),
            "per_entry_ok": marks, "per_entry_ms": times,
            "per_entry_ops": ops, "per_entry_status": statuses,
            "max_ms": max(times), "max_ops": max([o for o in ops if o is not None], default=None),
            "first_over_deadline": next(
                ({"entry": i + 1, "cpython_ms": times[i],
                  "pyodide_estimate_ms": round(times[i] * PYODIDE_FACTOR, 2)}
                 for i in range(len(times)) if times[i] * PYODIDE_FACTOR > DEADLINE_MS), None),
            "first_over_op_limit": next(
                ({"entry": i + 1, "ops": ops[i]}
                 for i in range(len(ops)) if ops[i] is not None and ops[i] > OP_LIMIT), None),
        }
        recs.append(rec)
        claim = CLAIMED.get(fname)
        flag = "" if claim is None or claim == rec["score"] else "  <<< 與宣稱 %d/20 不符" % claim
        pc = CLAIMED_PROJ.get(fname)
        pflag = "" if pc is None or pc == rec["projected"] else \
            "  <<< 投影與宣稱 %s 不符" % pc
        print("  %-26s score=%2d/20  proj=%2d/20  max_ms=%9.2f  max_ops=%s%s%s"
              % (fname, rec["score"], rec["projected"], rec["max_ms"],
                 rec["max_ops"], flag, pflag))
    return recs


def main():
    fast = "--fast" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    result = {}

    # ── 期望輸出的自我交叉驗證（公式 vs 真的枚舉） ────────────────────
    bad15 = [k for k in range(1, 23) if a15_line(k) != a15_line_brute(k)]
    bad16 = [(n, k) for n in range(1, 13) for k in range(0, n + 1)
             if a16_expected_val(n, k) != a16_expected_brute(n, k)]
    bad17 = [n for n in range(1, 200) if a17_expected_val(n) != a17_expected_brute(n)]
    print("獨立期望值 vs 暴力枚舉：015 不符 %s / 016 不符 %s / 017 不符 %s"
          % (bad15 or "無", bad16 or "無", bad17 or "無"))
    result["independent_expected_crosscheck"] = {
        "a015_mismatch_k": bad15, "a016_mismatch_nk": bad16, "a017_mismatch_n": bad17}
    assert not bad15 and not bad16 and not bad17, "獨立期望值實作自己就對不上暴力枚舉"

    # ── apcs017 ──────────────────────────────────────────────────────
    if only in (None, "017"):
        lits = load_literals(os.path.join(OUT, "plan017.yaml"))
        print("\n[apcs017] literal 筆數 = %d，第 1 筆 = %r" % (len(lits), lits[0]))
        result["a017_literals"] = lits
        result["a017"] = score_routes(
            "017", lits, lambda s: a17_expected(int(s.strip())),
            ["r017_ref.py", "r017_divmod.py", "r017_helper.py", "r017_w1_decimal.py",
             "r017_w2_forgot_half.py", "r017_w3_only_v3.py", "r017_w4_only_half_v2.py",
             "r017_u1_factorial.py"],
            skip={"r017_u1_factorial.py"} if fast else set())

    # ── apcs016 ──────────────────────────────────────────────────────
    if only in (None, "016"):
        lits = load_literals(os.path.join(OUT, "plan016.yaml"))
        print("\n[apcs016] literal 筆數 = %d，第 1 筆 = %r" % (len(lits), lits[0]))
        result["a016_literals"] = lits
        result["a016"] = score_routes(
            "016", lits,
            lambda s: a16_expected(*map(int, s.split())),
            ["r016_ref_pow3.py", "r016_a1_loop.py", "r016_a2_bigint.py",
             "r016_w1_ignore_k.py", "r016_w2_use_k.py", "r016_w3_plain_diff.py",
             "r016_w4_nomod.py"],
            want_ops={"r016_a1_loop.py", "r016_a2_bigint.py", "r016_ref_pow3.py"})

    # ── apcs015 ──────────────────────────────────────────────────────
    if only in (None, "015"):
        lits = load_literals(os.path.join(OUT, "plan015.yaml"))
        print("\n[apcs015] literal 筆數 = %d，第 1 筆 = %r" % (len(lits), lits[0]))
        result["a015_literals"] = lits
        heavy = {"r015_cellscan.py", "r015_u1_factorial.py"}
        result["a015"] = score_routes(
            "015", lits, lambda s: a15_expected(int(s.strip())),
            ["r015_ref_formula.py", "r015_rowscan.py", "r015_rowscan_sum.py",
             "r015_rowscan_helper.py",
             "r015_cellscan.py", "r015_w1_ordered.py", "r015_w2_nosub.py",
             "r015_w3_guard.py", "r015_w4_zerobased.py", "r015_u1_factorial.py"],
            skip=heavy if fast else set(),
            want_ops={"r015_ref_formula.py", "r015_rowscan.py", "r015_rowscan_sum.py",
                      "r015_rowscan_helper.py"})

    # --only 跑一題時，舊檔裡另外兩題的區塊必須留著：整份覆寫等於把別人的證物
    # 洗掉（下一輪誰再跑 --only 都會踩到）。先讀舊檔再 update 寫回，並記下這一次
    # 實際重算了哪些鍵，免得把沿用的舊值誤讀成本次量測。
    path = os.path.join(HERE, "crosscheck.json")
    merged = {}
    if os.path.exists(path):
        try:
            with open(path) as fh:
                merged = json.load(fh)
        except ValueError:
            merged = {}
    stale = sorted(set(merged) - set(result) - {"_recomputed_keys"})
    merged.update(result)
    merged["_recomputed_keys"] = {"this_run": sorted(result), "carried_over": stale}
    with open(path, "w") as fh:
        json.dump(merged, fh, indent=1, ensure_ascii=False)
    if stale:
        print("（沿用舊檔的鍵，本次未重算：%s）" % "、".join(stale))
    print("\n原始資料寫入 %s" % os.path.join(HERE, "crosscheck.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
