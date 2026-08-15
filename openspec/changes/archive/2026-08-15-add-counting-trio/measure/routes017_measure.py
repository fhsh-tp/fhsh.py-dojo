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


# ── 契約檢查（斷言牆） ───────────────────────────────────────────────────────
#
# 為什麼要有這一段：spec 對 apcs017 的多條 SHALL（G3 的 20/20 與 op 數、G4 的 2/20、
# G5 的 ≤12/20、G7 的 op 佔比、G8 的記憶體數字）**唯一的量測來源就是本檔**。
# 本檔原本不論量到什麼都無條件寫檔並 return 0：路線檔被改壞、判題器上限改動、
# 或環境害得某條 ACCEPTED 掉分，json 都會照樣產出，散文照樣引用，沒有任何一層會叫。
# 對照組是 curation/plan015.py（20+ 處 problems.append）與 measure/measure016.py。
#
# 門檻值一律取自實際量測輸出（2026-08-15 兩次獨立全量執行，離散量測值逐位相同），
# 不是憑空訂的；下面每個常數都標注了實測值與留了多少餘裕。
DEADLINE_MS = 5000

CLEAN_FILES = ("routes/r017_ref.py", "routes/r017_divmod.py", "routes/r017_helper.py")
DECIMAL_FILE = "routes/r017_w1_decimal.py"
SINGLE_SIDE_FILES = ("routes/r017_w2_forgot_half.py", "routes/r017_w3_only_v3.py",
                     "routes/r017_w4_only_half_v2.py")
UNCLEAN_FILE = "routes/r017_u1_factorial.py"

# 下面兩條刻意不重疊：CEIL 抓「op 絕對值飄掉」，HEADROOM 抓「判題器上限被調小」。
# （若把 HEADROOM 設成 ≤ OP_LIMIT/CEIL = 10,000 倍，它就永遠不可能先於 CEIL 觸發，
#   等於死碼——這是本檔第一版自我測試抓到的問題。）
CLEAN_OPS_CEIL = 1_000           # 實測 155／156／166；留 6 倍餘裕給 Python 版本間的事件差異
CLEAN_OPS_MIN_HEADROOM = 30_000  # 「遠低於上限」的機械定義：op 上限 / max_ops ≥ 30000 倍（實測 ~60000 倍）
DECIMAL_SCORE = 2                # G4：十進位尾零規則恰好 2/20
SINGLE_SIDE_MAX_SCORE = 12       # G5：三條取單邊路線的最高分恰為 12（可證下界，亦是實測上界）
UNCLEAN_OPS_CEIL = 200_000       # 實測 98,699；留 2 倍餘裕
UNCLEAN_OPS_PCT_CEIL = 2.0       # 實測 0.987% —— 成本躲在 C 呼叫內，計數器看不見
UNCLEAN_DENSITY_RATIO = 100      # 「成本躲在 C 內」的機械定義：op/ms 密度須比最稀疏的乾淨路線再低 100 倍
                                 # （實測 2.9 op/ms vs 乾淨路線約 7,000 op/ms，相差約 2,400 倍）
MEM_BYTES_AT_1E8 = 314_159_123     # G8：封閉式（lgamma），與機器狀態無關
MEM_BYTES_AT_1E9 = 3_556_832_228   # G8：同上


def _score(text):
    """把 "13/20" 拆成 (13, 20)；格式不對回傳 (None, None)。"""
    try:
        num, den = text.split("/")
        return int(num), int(den)
    except (ValueError, AttributeError):
        return None, None


def contract_problems(payload):
    """對已組好的 payload 逐條驗契約，回傳違約敘述清單（空 = 全數通過）。

    刻意寫成「吃 payload 的純函式」：契約邏輯不必重跑 5 分鐘的量測就能被負向控制
    測到（見 --self-test）。沒有負向控制的檢查等於沒有檢查。
    """
    problems = []
    routes = {r["file"]: r for r in payload.get("routes", [])}
    op_limit = payload.get("op_limit_per_case")

    # 0. 結構：路線齊全、20 筆、判題硬約束沒被偷改
    for fn in CLEAN_FILES + (DECIMAL_FILE,) + SINGLE_SIDE_FILES + (UNCLEAN_FILE,):
        if fn not in routes:
            problems.append("缺少路線 %s 的量測結果" % fn)
    if len(payload.get("entries", [])) != 20:
        problems.append("literal 筆數應為 20，實為 %d" % len(payload.get("entries", [])))
    if op_limit != OP_LIMIT:
        problems.append("op 上限應為 %d，payload 記為 %r" % (OP_LIMIT, op_limit))
    if payload.get("deadline_ms_per_case") != DEADLINE_MS:
        problems.append("deadline 應為 %d ms，payload 記為 %r"
                        % (DEADLINE_MS, payload.get("deadline_ms_per_case")))

    # 1. 每條路線的共通不變量：max_ops 名副其實、逐筆都在 op 上限內
    for fn, r in routes.items():
        per = r.get("per_entry_ops") or []
        if per and max(per) != r.get("max_ops"):
            problems.append("%s 的 max_ops %r 與 per_entry_ops 最大值 %d 不一致"
                            % (fn, r.get("max_ops"), max(per)))
        over = [i for i, o in enumerate(per, 1) if op_limit and o > op_limit]
        if over:
            problems.append("%s 的第 %s 筆 op 數超過上限 %s" % (fn, over, op_limit))

    # 2. REFERENCE 與兩條 ACCEPTED：20/20，且 op 遠低於上限、最壞一筆吃得下 deadline
    for fn in CLEAN_FILES:
        r = routes.get(fn)
        if r is None:
            continue
        num, den = _score(r.get("score"))
        if (num, den) != (20, 20):
            problems.append("%s 應為 20/20，實測 %s" % (fn, r.get("score")))
        if r.get("entries_skipped"):
            problems.append("%s 不應跳過任何筆，實跳過 %s" % (fn, r.get("entries_skipped")))
        ops = r.get("max_ops") or 0
        if ops > CLEAN_OPS_CEIL:
            problems.append("%s 最大 op %d 超過乾淨路線上限 %d" % (fn, ops, CLEAN_OPS_CEIL))
        if ops and op_limit and op_limit / ops < CLEAN_OPS_MIN_HEADROOM:
            problems.append("%s 的 op 餘裕僅 %.1f 倍，未達「遠低於上限」門檻 %d 倍"
                            % (fn, op_limit / ops, CLEAN_OPS_MIN_HEADROOM))
        worst = r.get("worst_entry_pyodide_estimate_ms")
        if worst is None or worst >= DEADLINE_MS:
            problems.append("%s 最壞一筆 Pyodide 估計 %r ms 未低於 deadline %d ms"
                            % (fn, worst, DEADLINE_MS))

    # 3. 十進位尾零規則（G4）：恰好 2/20，多一分少一分都代表 literal 組合變了
    r = routes.get(DECIMAL_FILE)
    if r is not None and _score(r.get("score")) != (DECIMAL_SCORE, 20):
        problems.append("%s 應為 %d/20，實測 %s" % (DECIMAL_FILE, DECIMAL_SCORE, r.get("score")))

    # 4. 三條「取單邊」誤解路線（G5）：各自 ≤ 12/20，且最高者恰為 12
    #    （12 是恆等式推得的可證下界，同時是實測到的最高分；高於它代表題目不再有鑑別度，
    #     低於它代表下界推導與實測對不上。）
    singles = []
    for fn in SINGLE_SIDE_FILES:
        r = routes.get(fn)
        if r is None:
            continue
        num, den = _score(r.get("score"))
        if num is None or den != 20:
            problems.append("%s 的得分格式異常：%r" % (fn, r.get("score")))
            continue
        singles.append((fn, num))
        if num > SINGLE_SIDE_MAX_SCORE:
            problems.append("%s 得 %d/20，超過取單邊路線上限 %d/20"
                            % (fn, num, SINGLE_SIDE_MAX_SCORE))
    if len(singles) == len(SINGLE_SIDE_FILES) and max(n for _, n in singles) != SINGLE_SIDE_MAX_SCORE:
        problems.append("取單邊路線的最高分應為 %d/20，實測 %d/20"
                        % (SINGLE_SIDE_MAX_SCORE, max(n for _, n in singles)))
    # G6 的必要條件：min(v2, v3) 與「只取 v3」輸出恆等，故得分必須相同
    w2, w3 = routes.get(SINGLE_SIDE_FILES[0]), routes.get(SINGLE_SIDE_FILES[1])
    if w2 and w3 and w2.get("score") != w3.get("score"):
        problems.append("G6 恆等：忘記折半（%s）與只取 v3（%s）得分應相同"
                        % (w2.get("score"), w3.get("score")))

    # 5. UNCLEAN_DEATH（G7）：op 數極低但牆鐘遠超 deadline ——「成本躲在 C 呼叫內」的
    #    機械定義。**不在此斷言 0/20**：那是瀏覽器實測的結論（browser-verification.jsonl），
    #    本機投影法算不出來，硬寫進來就變成補資料去符合散文。
    r = routes.get(UNCLEAN_FILE)
    if r is not None:
        ops = r.get("max_ops") or 0
        if ops > UNCLEAN_OPS_CEIL:
            problems.append("%s 最大 op %d 超過 %d —— 若計數器看得見成本，G7 的論證就不成立"
                            % (UNCLEAN_FILE, ops, UNCLEAN_OPS_CEIL))
        pct = r.get("max_ops_pct_of_limit")
        if pct is None or pct >= UNCLEAN_OPS_PCT_CEIL:
            problems.append("%s 的 op 佔上限比 %r%% 未低於 %.1f%%"
                            % (UNCLEAN_FILE, pct, UNCLEAN_OPS_PCT_CEIL))
        worst = r.get("worst_entry_pyodide_estimate_ms") or 0
        if worst <= DEADLINE_MS:
            problems.append("%s 最壞一筆 Pyodide 估計 %r ms 未超過 deadline %d ms —— "
                            "該路線本應被時間殺死" % (UNCLEAN_FILE, worst, DEADLINE_MS))
        # 「成本躲在 C 呼叫內」的機械定義：與乾淨路線相比，這條路線每毫秒才走幾個 op。
        densities = [rt["max_ops"] / rt["worst_entry_pyodide_estimate_ms"]
                     for fn2 in CLEAN_FILES
                     for rt in [routes.get(fn2)]
                     if rt and rt.get("worst_entry_pyodide_estimate_ms")]
        if worst > 0 and densities:
            here, clean_min = ops / worst, min(densities)
            if here * UNCLEAN_DENSITY_RATIO > clean_min:
                problems.append(
                    "%s 的 op 密度 %.2f op/ms 未比最稀疏的乾淨路線（%.0f op/ms）低 %d 倍 —— "
                    "成本不再是躲在 C 呼叫內" % (UNCLEAN_FILE, here, clean_min,
                                                UNCLEAN_DENSITY_RATIO))
        if not r.get("entries_skipped"):
            problems.append("%s 應因記憶體安全閥跳過大 n 的筆數，實跳過 %r"
                            % (UNCLEAN_FILE, r.get("entries_skipped")))
        if r.get("dies_from_entry") is None:
            problems.append("%s 應標出第一筆死亡的 entry，實為 None" % UNCLEAN_FILE)

    # 6. 記憶體支柱（G8）：封閉式，重跑必須逐位相同；單調遞增
    pillar = payload.get("memory_pillar", {})
    rows = {row["n"]: row for row in pillar.get("rows", [])}
    if not pillar.get("deterministic"):
        problems.append("memory_pillar.deterministic 應為 true")
    byte_seq = [row["bytes_of_bigint"] for row in pillar.get("rows", [])]
    if byte_seq != sorted(byte_seq) or len(set(byte_seq)) != len(byte_seq):
        problems.append("memory_pillar 的 bytes_of_bigint 未嚴格遞增：%s" % byte_seq)
    for n, expect in ((100_000_000, MEM_BYTES_AT_1E8), (1_000_000_000, MEM_BYTES_AT_1E9)):
        got = rows.get(n, {}).get("bytes_of_bigint")
        if got != expect:
            problems.append("n=%d 的 n! 位元組數應為 %d（封閉式），實為 %r" % (n, expect, got))

    return problems


def self_test():
    """負向控制：對已落盤的 routes017.json 注入單點錯誤，確認斷言牆真的會叫。

    正向控制（未注入 → 零違約）同樣是斷言的一部分：只證明「會叫」不夠，
    還要證明它不是無論如何都叫。
    """
    path = os.path.join(HERE, "routes017.json")
    with open(path) as fh:
        base = json.load(fh)

    def mutate(fn):
        payload = json.loads(json.dumps(base))
        fn(payload)
        return contract_problems(payload)

    def route(payload, name):
        return next(r for r in payload["routes"] if r["file"] == name)

    def set_ops(payload, name, value):
        """同時改 max_ops 與 per_entry_ops——只改一邊會被『兩者一致』那條先攔下，
        負向控制就證明不到 op 天花板那一條真的存在。"""
        r = route(payload, name)
        r["max_ops"] = value
        r["per_entry_ops"] = [value] * len(r["per_entry_ops"])
        if payload["op_limit_per_case"]:
            r["max_ops_pct_of_limit"] = round(value / payload["op_limit_per_case"] * 100, 4)

    # 每個注入點都指定「期望觸發哪一條」：只確認「有叫」不夠，叫錯條等於那條仍未受測。
    cases = [
        ("REFERENCE 掉一分", lambda p: route(p, CLEAN_FILES[0]).__setitem__("score", "19/20"),
         "應為 20/20"),
        ("ACCEPTED op 暴增", lambda p: set_ops(p, CLEAN_FILES[1], 20_000),
         "超過乾淨路線上限"),
        ("ACCEPTED op 餘裕不足", lambda p: set_ops(p, CLEAN_FILES[1], 900),
         "未達「遠低於上限」門檻"),
        ("ACCEPTED 最壞一筆撞 deadline",
         lambda p: route(p, CLEAN_FILES[2]).__setitem__("worst_entry_pyodide_estimate_ms", 9999.0),
         "未低於 deadline"),
        ("ACCEPTED 跳過某些筆",
         lambda p: route(p, CLEAN_FILES[2]).__setitem__("entries_skipped", 3), "不應跳過任何筆"),
        ("十進位路線分數變動", lambda p: route(p, DECIMAL_FILE).__setitem__("score", "3/20"),
         "應為 2/20"),
        ("取單邊路線超過 12", lambda p: route(p, SINGLE_SIDE_FILES[2]).__setitem__("score", "13/20"),
         "超過取單邊路線上限"),
        ("取單邊最高分掉到 11", lambda p: route(p, SINGLE_SIDE_FILES[2]).__setitem__("score", "11/20"),
         "最高分應為 12/20"),
        ("G6 恆等破裂", lambda p: route(p, SINGLE_SIDE_FILES[1]).__setitem__("score", "10/20"),
         "G6 恆等"),
        ("取單邊得分格式壞掉",
         lambda p: route(p, SINGLE_SIDE_FILES[0]).__setitem__("score", "十一分"), "得分格式異常"),
        ("UNCLEAN op 變得看得見", lambda p: set_ops(p, UNCLEAN_FILE, 5_000_000),
         "若計數器看得見成本"),
        ("UNCLEAN op 佔比灌水",
         lambda p: route(p, UNCLEAN_FILE).__setitem__("max_ops_pct_of_limit", 42.0),
         "未低於 2.0%"),
        ("UNCLEAN 不再超時",
         lambda p: route(p, UNCLEAN_FILE).__setitem__("worst_entry_pyodide_estimate_ms", 100.0),
         "該路線本應被時間殺死"),
        ("UNCLEAN 成本不再躲在 C 內",
         lambda p: route(p, UNCLEAN_FILE).__setitem__("worst_entry_pyodide_estimate_ms", 500.0),
         "成本不再是躲在 C 呼叫內"),
        ("UNCLEAN 沒跳過任何筆",
         lambda p: route(p, UNCLEAN_FILE).__setitem__("entries_skipped", 0),
         "應因記憶體安全閥跳過"),
        ("UNCLEAN 未標出死亡起點",
         lambda p: route(p, UNCLEAN_FILE).__setitem__("dies_from_entry", None),
         "應標出第一筆死亡的 entry"),
        ("max_ops 與逐筆不一致",
         lambda p: route(p, CLEAN_FILES[0])["per_entry_ops"].__setitem__(0, 200),
         "不一致"),
        ("逐筆 op 撞上限", lambda p: set_ops(p, DECIMAL_FILE, 99_999_999),
         "op 數超過上限"),
        ("literal 筆數變動", lambda p: p["entries"].pop(), "literal 筆數應為 20"),
        ("op 上限被偷改", lambda p: p.__setitem__("op_limit_per_case", 1), "op 上限應為"),
        ("deadline 被偷改", lambda p: p.__setitem__("deadline_ms_per_case", 60_000),
         "deadline 應為"),
        ("整條路線消失", lambda p: p["routes"].pop(0), "缺少路線"),
        ("記憶體封閉式差一位元組",
         lambda p: p["memory_pillar"]["rows"][2].__setitem__("bytes_of_bigint",
                                                             MEM_BYTES_AT_1E8 + 1),
         "位元組數應為"),
        ("記憶體不再單調",
         lambda p: p["memory_pillar"]["rows"][3].__setitem__("bytes_of_bigint", 1),
         "未嚴格遞增"),
        ("記憶體宣稱不可重現",
         lambda p: p["memory_pillar"].__setitem__("deterministic", False),
         "deterministic 應為 true"),
    ]

    failures = []
    clean = contract_problems(base)
    print("正向控制：未注入 → %d 條違約 %s" % (len(clean), "PASS" if not clean else "FAIL"))
    if clean:
        failures.append("未注入卻報 %d 條違約：%s" % (len(clean), clean))
    for label, fn, expect in cases:
        got = mutate(fn)
        hit = [g for g in got if expect in g]
        print("  %-26s %-6s %s" % (label, "FIRED" if hit else "MISS",
                                   hit[0] if hit else (got[0] if got else "（完全沒叫）")))
        if not hit:
            failures.append("注入「%s」後未觸發預期檢查（期望訊息含 %r，實得 %s）"
                            % (label, expect, got or "無"))

    if failures:
        print("\n負向控制失敗：")
        for f in failures:
            print("  -", f)
        return 1
    print("\n負向控制全數通過（%d 個注入點皆觸發，未注入時零違約）。" % len(cases))
    return 0


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
    payload["problems"] = contract_problems(payload)
    with open(os.path.join(HERE, "routes017.json"), "w") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    if payload["problems"]:
        print("\n實測斷言失敗：")
        for p in payload["problems"]:
            print("  -", p)
        return 1
    print("\n實測斷言全數通過。")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test() if "--self-test" in sys.argv else main())
