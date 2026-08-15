"""apcs017 — 實測所有盤點路線對 20 筆 literal 的得分與耗時，寫出 measure/routes017.json。

執行：python3 routes017_measure.py

量法：
  * 每條路線的原始碼 compile 一次，逐筆把 stdin/stdout 換成 StringIO 後 exec
    （避免 ~20 ms 的直譯器啟動時間淹沒真正的計算成本）。
  * 任何牆鐘數字一律重複量測 REPEATS(=7) 次取最小值，含 UNCLEAN_DEATH 路線與
    逐筆耗時。單發量測會抓到排程尖峰，曾經量出「n 較小卻慢一倍」的物理不可能值。
  * Pyodide 估計 = 本機毫秒 x PYODIDE_FACTOR（純 Python 迴圈的經驗換算）。
  * op 數一律用 verify/judge_ops.py（判題器 tracer 的唯一複刻）量，不自寫 tracer。

UNCLEAN_DEATH 路線（math.factorial）另有安全閥：只對 n <= UNCLEAN_MAX_N 實際執行，
更大的 n 一律標記為 skipped。**該路線的死因主軸是記憶體**（n! 的位元數是封閉式，
每次跑都一模一樣）；耗時外推只是佐證，且一律以量級＋離散度陳述，不寫有效位數。
絕不對 n = 1e9 呼叫 math.factorial——那會吃光記憶體。
"""

import importlib.util
import io
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CURATION = os.path.join(os.path.dirname(HERE), "curation")
ROUTES = os.path.join(CURATION, "routes")

spec = importlib.util.spec_from_file_location("semantics017", os.path.join(CURATION, "semantics017.py"))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

sys.path.insert(0, CURATION)
import plan017 as P  # noqa: E402

VERIFY = os.path.join(os.path.dirname(HERE), "verify")
sys.path.insert(0, VERIFY)
from judge_ops import OP_LIMIT, count_ops_source_fresh  # noqa: E402

REPEATS = 7                    # 所有牆鐘數字的固定重複次數（取最小值）
FACTORIAL_REPEATS = 5          # factorial 探針的獨立量測次數（外推離散度的來源）
PYODIDE_FACTOR = 4
UNCLEAN_MAX_N = 300_000        # 超過這個 n 就不對 math.factorial 動手（記憶體/時間安全閥）

ROUTE_FILES = [
    ("REFERENCE",     "兩個 while 迴圈算 2 與 3 的份額後取 min", "r017_ref.py"),
    ("ACCEPTED",      "先算 3 的份額、再用 divmod 折半 2 的份額", "r017_divmod.py"),
    ("ACCEPTED",      "抽成小函式、用「不斷把 n 折下去」的等價寫法", "r017_helper.py"),
    ("WRONG_ANSWER",  "十進位尾零規則（每 5 一數）", "r017_w1_decimal.py"),
    ("WRONG_ANSWER",  "min(v2, v3) — 忘記一批 12 要兩個 2", "r017_w2_forgot_half.py"),
    ("WRONG_ANSWER",  "只取 3 的份額", "r017_w3_only_v3.py"),
    ("WRONG_ANSWER",  "只取 2 的份額折半、不取 min", "r017_w4_only_half_v2.py"),
    ("UNCLEAN_DEATH", "math.factorial(n) 後反覆整除 12", "r017_u1_factorial.py"),
]


def run_once(code, text):
    old_in, old_out = sys.stdin, sys.stdout
    sys.stdin, sys.stdout = io.StringIO(text), io.StringIO()
    try:
        exec(code, {"__name__": "__main__"})
        return sys.stdout.getvalue()
    finally:
        sys.stdin, sys.stdout = old_in, old_out


def measure(path, unclean=False):
    src = open(path).read()
    code = compile(src, path, "exec")
    inputs = [(n, S.render_input(n), S.render_expected(n)) for n in P.ENTRIES]
    if unclean:
        inputs = [(n, t, e) for n, t, e in inputs if n <= UNCLEAN_MAX_N]

    outs = [run_once(code, t) for _, t, _ in inputs]
    score = sum(1 for (n, t, e), o in zip(inputs, outs) if o.strip() == e.strip())

    # 逐筆各量 REPEATS 次取最小值；整份的 cpython_ms 定義為這些最小值的總和
    # （比「整塊 20 筆重跑取最小」更不怕單發排程尖峰，也才有逐筆最壞值可看）。
    per_entry_ms = []
    for _, t, _ in inputs:
        b = float("inf")
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            run_once(code, t)
            b = min(b, (time.perf_counter() - t0) * 1000.0)
        per_entry_ms.append(round(b, 4))
    best = sum(per_entry_ms)

    # op 數：唯一來源是 verify/judge_ops.py 的判題器複刻（不過濾 event、不過濾檔名）。
    # 必須用 *_fresh：行內量測會少掉 import math 首次匯入的 278 個 importlib 事件，
    # 而 op 上限是逐筆套用的，冷數字才是上界。詳見 judge_ops.count_ops_source_fresh。
    ops = [count_ops_source_fresh(path, t)[0] for _, t, _ in inputs]
    return score, len(inputs), round(best, 3), ops, per_entry_ms


def _sig(x, digits=2):
    """取 digits 個有效位數——外推值不得帶著量測撐不起的精度出場。"""
    if x == 0:
        return 0.0
    return round(x, -int(math.floor(math.log10(abs(x)))) + (digits - 1))


def bigint_footprint(n):
    """n! 的十進位位數與大整數位元組數：封閉式，與機器狀態無關，每次都一樣。"""
    return {
        "decimal_digits": int(math.lgamma(n + 1) / math.log(10)) + 1,
        "bytes_of_bigint": int(math.lgamma(n + 1) / math.log(2) / 8),
    }


def memory_pillar():
    """UNCLEAN_DEATH 的結論支柱：記憶體。純封閉式，不含任何牆鐘量測。

    瀏覽器分頁的可用堆積是 GB 等級（wasm32 的定址上限本身就是 4 GB），
    而 n=10^9 光是那個大整數就要 3.5 GB——連配置都不會成功。
    """
    rows = []
    for n in (1_000_000, 10_000_000, 100_000_000, 1_000_000_000):
        f = bigint_footprint(n)
        rows.append({
            "n": n,
            "decimal_digits": f["decimal_digits"],
            "bytes_of_bigint": f["bytes_of_bigint"],
            "mib_of_bigint": round(f["bytes_of_bigint"] / 2 ** 20, 1),
        })
    return {
        "rows": rows,
        "deterministic": True,
        "note": "位數由 lgamma 封閉式算出，重跑必然逐位相同；這是 UNCLEAN_DEATH 判定的主要依據。"
                "n=10^9 的單一大整數需 3.3 GiB，超過 wasm32 的 4 GB 定址空間扣掉執行環境後的餘裕，"
                "配置階段就會失敗，與機器快慢無關。",
    }


def unclean_probe():
    """math.factorial 的耗時探針：重複量測小 n，再以**量級**外推到題面上界。

    F-7 的教訓：單次量測算出的 log-log 斜率在 1.74 與 1.77 之間浮動，外推到
    n=10^9 就差 21%；把外推值寫到 7 位有效數字是假精度。因此這裡：
      * 每個 n 獨立量 FACTORIAL_REPEATS 次，min / median / max 全部落盤
      * 中心斜率取兩端最小值之比（最小值是計時裡最穩的統計量），
        不確定區間取兩端極值交叉配對
      * 外推只給 2 位有效數字 + 10 的冪次量級 + 由斜率區間推出的範圍
    絕不真的呼叫 math.factorial(10**9)。
    """
    ns = (10_000, 100_000, 300_000, 1_000_000)
    samples = {n: [] for n in ns}
    for _ in range(FACTORIAL_REPEATS):
        for n in ns:
            t0 = time.perf_counter()
            f = math.factorial(n)
            t1 = time.perf_counter()
            del f
            samples[n].append((t1 - t0) * 1000.0)

    measured = []
    for n in ns:
        xs = sorted(samples[n])
        measured.append({
            "n": n,
            "repeats": len(xs),
            "factorial_ms_min": round(xs[0], 2),
            "factorial_ms_median": round(xs[len(xs) // 2], 2),
            "factorial_ms_max": round(xs[-1], 2),
            "spread_pct": round((xs[-1] - xs[0]) / xs[0] * 100, 1),
            **bigint_footprint(n),
        })

    # 斜率：中心值用兩端的**最小值**（最小值是計時量測裡最穩的統計量，跨次重跑幾乎不動）；
    # 不確定區間用兩端的極值交叉配對（min/max、max/min），涵蓋這台機器的排程噪音。
    # 早期版本用「逐輪配對」，配對順序本身就是噪音，兩次重跑會給出不相交的區間。
    lo_n, hi_n = 300_000, 1_000_000
    ratio = math.log(hi_n / lo_n)
    lo_min, lo_max = min(samples[lo_n]), max(samples[lo_n])
    hi_min, hi_max = min(samples[hi_n]), max(samples[hi_n])
    slope_med = math.log(hi_min / lo_min) / ratio
    slope_lo = math.log(hi_min / lo_max) / ratio
    slope_hi = math.log(hi_max / lo_min) / ratio
    slopes = [slope_lo, slope_med, slope_hi]
    ref_ms = hi_min

    extrap = {}
    for n in (10_000_000, 100_000_000, 1_000_000_000):
        lo_s = ref_ms * (n / hi_n) ** slope_lo / 1000.0
        hi_s = ref_ms * (n / hi_n) ** slope_hi / 1000.0
        med_s = ref_ms * (n / hi_n) ** slope_med / 1000.0
        extrap[str(n)] = {
            "cpython_s_order_of_magnitude": "10^%d 秒" % int(math.floor(math.log10(med_s))),
            "cpython_s_range_2sf": [_sig(lo_s), _sig(hi_s)],
            "days_range_2sf": [_sig(lo_s / 86400), _sig(hi_s / 86400)],
            "range_ratio": round(hi_s / lo_s, 2),
            **bigint_footprint(n),
        }

    return {
        "measured": measured,
        "loglog_slope_central_from_minima": round(slope_med, 3),
        "loglog_slope_envelope": [round(slope_lo, 3), round(slope_hi, 3)],
        "extrapolated": extrap,
        "method": "每個 n 獨立量 %d 次；以 n=%d 與 n=%d 兩點求 log-log 斜率，"
                  "中心斜率取兩端最小值之比（最穩），區間取兩端極值交叉配對；"
                  "外推只保留 2 位有效數字與 10 的冪次量級。n>=10^7 一律外推，未實際呼叫。"
                  % (FACTORIAL_REPEATS, lo_n, hi_n),
        "caveat": "時間外推的離散度大（同一台機器重跑，斜率就會在上列範圍內漂），"
                  "只能當量級佐證。UNCLEAN_DEATH 的判定請看 memory_pillar。",
    }


def unclean_split_probe():
    """把 UNCLEAN_DEATH 路線的耗時拆成兩段，因為兩段的「死法」完全不同：

      (a) math.factorial(n)   — 單一 C 呼叫，執行期間**不經過任何 bytecode 邊界**，
                                deadline 的中斷旗標檢查不到 → 逾時無法乾淨中止。
      (b) while tokens % 12   — 純 Python 迴圈，每輪都是 bytecode 邊界，可被中斷，
                                但每輪都在一個數百萬位的大整數上做取餘＋整除。

    小 n 時 (b) 才是主成本；n 一大就換成 (a) 主宰，而 (a) 正是不可中斷的那一段。
    """
    out = []
    for n in (20_250, 65_536, 100_000, 1_000_000):
        divisions = S.exchanges_formula(n)
        # 大 n 只跑前 SAMPLE 次除法再線性外推（每次只掉 ~1.08 位，位數幾乎不變）
        sample = divisions if n <= 20_250 else min(divisions, 200)
        fact_ms, div_ms = float("inf"), float("inf")
        for _ in range(REPEATS):           # 牆鐘固定重複 7 次取最小值
            t0 = time.perf_counter()
            tokens = math.factorial(n)
            t1 = time.perf_counter()
            x = tokens
            t2 = time.perf_counter()
            for _ in range(sample):
                x //= 12
            t3 = time.perf_counter()
            del tokens, x
            fact_ms = min(fact_ms, (t1 - t0) * 1000.0)
            div_ms = min(div_ms, (t3 - t2) * 1000.0)
        full_div_ms = div_ms if sample == divisions else div_ms / sample * divisions
        out.append({
            "n": n,
            "repeats": REPEATS,
            "factorial_ms": round(fact_ms, 2),
            "divisions_needed": divisions,
            "division_sample": sample,
            "division_sample_ms": round(div_ms, 2),
            "division_loop_ms_total": round(full_div_ms, 1),
            "division_loop_extrapolated": sample != divisions,
            "route_total_ms": round(fact_ms + full_div_ms, 1),
            "pyodide_estimate_ms": round((fact_ms + full_div_ms) * PYODIDE_FACTOR, 1),
        })
    return out


def unclean_per_entry():
    """逐筆量 UNCLEAN_DEATH 路線，判斷它在正式判題（每筆 5000 ms deadline）能活到第幾筆。"""
    path = os.path.join(ROUTES, "r017_u1_factorial.py")
    src = open(path).read()
    code = compile(src, path, "exec")
    rows = []
    for i, n in enumerate(P.ENTRIES, 1):
        f = bigint_footprint(n)
        if n > UNCLEAN_MAX_N:
            rows.append({"entry": i, "n": n, "executed": False,
                         "decimal_digits": f["decimal_digits"],
                         "mib_of_bigint": round(f["bytes_of_bigint"] / 2 ** 20, 1),
                         "verdict": "未執行（記憶體安全閥）：n! 約 %d 位十進位數，"
                                    "大整數本身就要 %.1f MiB"
                                    % (f["decimal_digits"], f["bytes_of_bigint"] / 2 ** 20)})
            continue
        ms = float("inf")
        for _ in range(REPEATS):           # 牆鐘固定重複 7 次取最小值
            t0 = time.perf_counter()
            run_once(code, S.render_input(n))
            ms = min(ms, (time.perf_counter() - t0) * 1000.0)
        est = ms * PYODIDE_FACTOR
        rows.append({"entry": i, "n": n, "executed": True, "repeats": REPEATS,
                     "cpython_ms": round(ms, 2), "pyodide_estimate_ms": round(est, 1),
                     "ops": count_ops_source_fresh(path, S.render_input(n))[0],
                     "decimal_digits": f["decimal_digits"],
                     "verdict": "存活" if est < 5000 else "逾時（> 5000 ms deadline）"})
    return rows


def main():
    results = []
    for disposition, note, fn in ROUTE_FILES:
        path = os.path.join(ROUTES, fn)
        unclean = disposition == "UNCLEAN_DEATH"
        score, ran, ms, ops, per_ms = measure(path, unclean=unclean)
        results.append({
            "name": note,
            "file": "routes/" + fn,
            "disposition": disposition,
            "score": "%d/%d" % (score, len(P.ENTRIES)),
            "entries_actually_run": ran,
            "entries_skipped": len(P.ENTRIES) - ran,
            "cpython_ms": ms,
            "pyodide_estimate_ms": round(ms * PYODIDE_FACTOR, 3),
            "worst_entry_cpython_ms": max(per_ms),
            "worst_entry_pyodide_estimate_ms": round(max(per_ms) * PYODIDE_FACTOR, 3),
            "per_entry_cpython_ms": per_ms,
            "max_ops": max(ops),
            "max_ops_pct_of_limit": round(max(ops) / OP_LIMIT * 100, 4),
            "per_entry_ops": ops,
            "ops_source": "verify/judge_ops.py::count_ops_source_fresh（冷行程，含首次 import 的 importlib 事件）",
        })

    per_entry = unclean_per_entry()
    survived = sum(1 for r in per_entry if r.get("executed") and r["pyodide_estimate_ms"] < 5000)
    for r in results:
        if r["disposition"] == "UNCLEAN_DEATH":
            r["score_ignoring_time"] = r["score"]
            r["score"] = "%d/%d" % (survived, len(P.ENTRIES))
            r["dies_from_entry"] = next(
                (x["entry"] for x in per_entry
                 if not x.get("executed") or x["pyodide_estimate_ms"] >= 5000), None)

    payload = {
        "challenge": "apcs017 園遊會代幣兌換",
        "slug": "fair-token-exchange",
        "algorithm": "fair_token_exchange",
        "entries": P.ENTRIES,
        "expected": [S.exchanges_formula(n) for n in P.ENTRIES],
        "deadline_ms_per_case": 5000,
        "op_limit_per_case": OP_LIMIT,
        "pyodide_factor": PYODIDE_FACTOR,
        "repeats": REPEATS,
        "wallclock_rule": "所有牆鐘數字皆重複 %d 次取最小值" % REPEATS,
        "op_measurement": "全部路線的 op 數由 verify/judge_ops.py（判題器 tracer 的唯一複刻）量出",
        "unclean_max_n_actually_executed": UNCLEAN_MAX_N,
        "memory_pillar": memory_pillar(),
        "unclean_probe": unclean_probe(),
        "unclean_split_probe": unclean_split_probe(),
        "unclean_per_entry": per_entry,
        "routes": results,
    }
    with open(os.path.join(HERE, "routes017.json"), "w") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
