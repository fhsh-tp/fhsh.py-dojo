"""apcs015 基地台佈點規劃 — 測資計畫＋斷言牆（E 表事實的機械正本）。

執行：
    python3 plan015.py            驗證＋量測＋寫出 out/plan015.yaml 與 measure/routes015.json
    python3 plan015.py --check    只驗證與量測，不寫檔
    python3 plan015.py --fast     跳過會逾時的路線（開發時用；正式回報請跑完整版）

一切數字都由本檔實際執行算出，沒有任何估算或手抄。

判題環境硬事實（本檔的成本模型基準）：
  * 每筆測資 deadline = 5000 ms（主執行緒 watchdog + SharedArrayBuffer 中斷）
  * 每筆測資 op 上限 = 10,000,000（op = sys.settrace 的**全部事件**：
    call / line / return / exception，見 .vitepress/theme/workers/worker-utils.ts）
  * Pyodide 純 Python 迴圈約為本機 CPython 的 3–5 倍慢 → 本檔一律取 **×4** 作估計
  * math.factorial 這類單一 C 呼叫無法被 deadline 中斷 → 標記為「不乾淨的死法」

三條量測紀律（皆為前一輪缺陷的直接修補）：
  1. op 一律 import verify/judge_ops.py，本檔**不自帶 tracer**。
  2. 牆鐘一律重複取樣 WALL_REPS 次取最小值——單發量測會抓到 process 排程尖峰。
  3. ENTRIES 由 ``derive_entries()`` 從契約導出，不手挑。改契約請改導出規則。
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantics015 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES_DIR = os.path.join(HERE, "routes")
OUT_DIR = os.path.join(HERE, "out")
MEASURE_DIR = os.path.abspath(os.path.join(HERE, os.pardir, "measure"))
VERIFY_DIR = os.path.abspath(os.path.join(HERE, os.pardir, "verify"))

sys.path.insert(0, VERIFY_DIR)
from judge_ops import OP_LIMIT  # noqa: E402  ← 唯一允許的 op 上限與量測來源

DEADLINE_MS = 5000          # 每筆測資牆鐘上限（Pyodide 端）
PYODIDE_FACTOR = 4          # 本機 CPython 毫秒 × 4 = Pyodide 估計毫秒
CPYTHON_BUDGET_MS = DEADLINE_MS / PYODIDE_FACTOR   # = 1250 ms，本機等效預算
INPUT_BUDGET = 4096         # 預設單筆輸入位元組預算（Usage.md）
KILL_TIMEOUT_S = 10         # 量測用的硬逾時：超過就記為逾時，不再等下去
OPCOUNT_GATE_MS = 1500      # 只有原生跑得比這快的筆才做 op 量測（settrace 會慢一到兩個數量級）
WRONG_SCORE_CAP = 2         # 任何 WRONG_ANSWER 路線的得分上限（0/20 或明確低分）
WALL_REPS = 7               # 牆鐘重複取樣次數；取最小值代表「無干擾下的成本」
MIN_OP_MARGIN = 3.0         # 三種 O(n^2) 寫法中最貴者對 op 上限的最小餘裕倍數
MIN_CELLSCAN_KILLS = 12     # O(n^3) 路線至少要在幾筆上死亡

# ── 20 筆 literal 的契約（導出規則的輸入，改這裡就會改出不同的 20 筆） ──
N_HEAD = [8, 1, 2, 3, 4]    # 第 1 筆＝題面範例；其餘為 k < 3 分支邊界與其後第一筆
N_SMALL_BAND = (6, 249, 4)  # 小規模帶：起、迄、筆數（幾何等比取點）
N_LARGE_BAND = (250, 1000, 11)  # 大規模帶：起、迄（＝上界）、筆數（線性等距）
BIG_THRESHOLD = 250         # 「大筆」門檻
MIN_BIG = 10                # 至少幾筆 n >= BIG_THRESHOLD


def derive_entries():
    """由契約機械導出 20 筆 n 值。任何手挑都會讓下一位維護者無從重現。"""
    lo, hi, cnt = N_SMALL_BAND
    ratio = (hi / lo) ** (1 / (cnt - 1))
    small = [int(round(lo * ratio**i)) for i in range(cnt)]
    lo2, hi2, cnt2 = N_LARGE_BAND
    step = (hi2 - lo2) / (cnt2 - 1)
    large = [int(round(lo2 + step * i)) for i in range(cnt2)]
    return N_HEAD + small + large


ENTRIES = derive_entries()

# 路線盤點：檔名 → (顯示名稱, 期望處置, 期望得分或 None)
# 期望得分全部來自實測，不是猜的；改動任何路線後重跑本檔即會被指名失敗。
ROUTES = [
    ("r015_ref_formula.py",    "REFERENCE  O(n) 封閉公式",                  "REFERENCE",     20),
    ("r015_rowscan.py",        "ACCEPTED   O(n^2) 逐列累加，內層明寫迴圈",    "ACCEPTED",      20),
    ("r015_rowscan_sum.py",    "ACCEPTED   O(n^2) 逐列累加，內層 sum(genexp)", "ACCEPTED",      20),
    ("r015_rowscan_helper.py", "ACCEPTED   O(n^2) 逐列累加，內層抽小函式",    "ACCEPTED",      20),
    ("r015_cellscan.py",       "KILLED     O(n^3) 逐格 × 8 偏移",            "KILLED",        None),
    ("r015_w1_ordered.py",     "WRONG      有序配對（答案兩倍）",              "WRONG_ANSWER",  1),
    ("r015_w2_nosub.py",       "WRONG      忘記扣掉干擾配對",                 "WRONG_ANSWER",  2),
    ("r015_w3_guard.py",       "WRONG      k < 3 分支守門寫錯（k > 3）",      "WRONG_ANSWER",  2),
    ("r015_w4_zerobased.py",   "WRONG      迴圈 0 起算＋分支缺漏",             "WRONG_ANSWER",  0),
    ("r015_u1_factorial.py",   "UNCLEAN    math.factorial 展開（砍不掉）",     "UNCLEAN_DEATH", None),
]

# 三種同演算法不同寫法——X-1 的上界決議就是要求這三條同生同死
SPELLING_ROUTES = ["r015_rowscan.py", "r015_rowscan_sum.py", "r015_rowscan_helper.py"]

TIMEOUT_ROUTES = {"r015_cellscan.py", "r015_u1_factorial.py"}


# ── op 計數：一律委派給 verify/judge_ops.py，本檔不自帶 tracer ─────────
OP_HARNESS = r'''
import sys
sys.path.insert(0, %(verify)r)
from judge_ops import count_ops_source
with open(%(path)r) as fh:
    src = fh.read()
ops, _out = count_ops_source(src, %(stdin)r, %(path)r)
print(ops)
'''


def count_ops(path, stdin, timeout):
    """實測單一路線對單筆輸入的 op 數。逾時或例外回傳 None。

    走 subprocess 只為了拿到硬逾時保護；計數本身完全由 judge_ops
    的 count_ops_source 負責，本檔沒有自己的 tracer 定義。
    """
    code = OP_HARNESS % {"stdin": stdin, "path": path, "verify": VERIFY_DIR}
    try:
        p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    if p.returncode != 0:
        return None
    return int(p.stdout.strip())


def run_route_once(path, stdin, timeout):
    """跑一次路線，回傳 (stdout, 毫秒, 狀態)。狀態 ∈ ok / timeout / error。"""
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, path], input=stdin,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", timeout * 1000.0, "timeout"
    ms = (time.perf_counter() - t0) * 1000.0
    if p.returncode != 0:
        return "", ms, "error"
    return p.stdout.rstrip("\n"), ms, "ok"


def run_route(path, stdin, timeout, reps=WALL_REPS):
    """跑 ``reps`` 次取**最小**牆鐘，回傳 (stdout, 最小毫秒, 狀態)。

    為什麼取最小：單發量測會抓到 OS 排程與磁碟快取的偶發尖峰。前一輪就
    量到過一筆 803 ms 的尖峰，比 n 更大的那筆還慢一倍——物理上不可能。
    最小值才是「無干擾下的真實成本」，也是唯一可重現的統計量。

    只有第一次成功才重複；逾時／錯誤重跑沒有意義（且很貴）。
    """
    got, ms, status = run_route_once(path, stdin, timeout)
    if status != "ok":
        return got, ms, status
    best = ms
    for _ in range(reps - 1):
        got2, ms2, st2 = run_route_once(path, stdin, timeout)
        if st2 != "ok":
            return got2, ms2, st2
        got = got2
        best = min(best, ms2)
    return got, best, status


def main(write=True, fast=False):
    problems = []

    # ── A. 語意正本自我驗證：公式 vs 真的枚舉所有格子對 ──────────────
    bad = S.cross_check(30)
    if bad:
        problems.append("公式與枚舉參照在 k = %s 不符" % bad)
    if [S.answer_line(k) for k in range(1, 9)] != S.SAMPLE_EXPECTED:
        problems.append("前 8 項與釘死的題面範例不符")

    # ── B. 20 筆 literal 的結構契約 ──────────────────────────────────
    if len(ENTRIES) != 20:
        problems.append("literal 筆數 %d，契約要求 20" % len(ENTRIES))
    if ENTRIES[0] != 8:
        problems.append("第 1 筆是 %d，契約要求 8（題面範例）" % ENTRIES[0])
    if len(set(ENTRIES)) != len(ENTRIES):
        problems.append("20 個 n 值有重複")
    big = [n for n in ENTRIES if n >= BIG_THRESHOLD]
    if len(big) < MIN_BIG:
        problems.append("n >= %d 只有 %d 筆，契約要求至少 %d 筆"
                        % (BIG_THRESHOLD, len(big), MIN_BIG))
    if max(ENTRIES) != S.N_MAX:
        problems.append("最大筆是 %d，契約要求 %d（＝值域上界）" % (max(ENTRIES), S.N_MAX))
    for need in (1, 2, 3, 4):
        if need not in ENTRIES:
            problems.append("缺 n = %d 邊界（公式在 k < 3 有分支）" % need)
    for n in ENTRIES:
        if not (S.N_MIN <= n <= S.N_MAX):
            problems.append("n = %d 超出 %d..%d" % (n, S.N_MIN, S.N_MAX))

    # ── C. 逐筆 I/O 規模 ─────────────────────────────────────────────
    per_entry = []
    total_out_bytes = 0
    for i, n in enumerate(ENTRIES, 1):
        text = S.render_input(n)
        exp = S.render_expected(n)
        ib = len(text.encode())
        ob = len(exp.encode())
        total_out_bytes += ob
        if ib > INPUT_BUDGET:
            problems.append("entry %d: 輸入 %d bytes > input_budget %d" % (i, ib, INPUT_BUDGET))
        per_entry.append({
            "entry": i, "n": n, "input_bytes": ib, "output_bytes": ob,
            "output_lines": n, "last_value": S.answer_line(n),
        })
    max_out = max(r["output_bytes"] for r in per_entry)

    # ── D. 逐路線 × 逐筆實測（得分、牆鐘、op 數） ────────────────────
    # D0. 量測外殼的兩條地板，先量清楚才有辦法解讀後面的數字：
    #   * op 地板：判題器 tracer 會數到的「讀入＋輸出」固定開銷。
    #   * 牆鐘地板：起一個 CPython process 的固定成本。本題所有 ACCEPTED
    #     路線的單筆牆鐘幾乎都是這條地板，牆鐘因此**對本題不具鑑別力**。
    baseline_path = os.path.join(HERE, "probe_opbaseline.py")
    op_baseline = count_ops(baseline_path, S.render_input(S.N_MAX), KILL_TIMEOUT_S)
    _, wall_floor_ms, _ = run_route(baseline_path, S.render_input(S.N_MAX), KILL_TIMEOUT_S)
    wall_floor_ms = round(wall_floor_ms, 2)
    routes_report = []
    for fname, label, want_disp, want_score in ROUTES:
        path = os.path.join(ROUTES_DIR, fname)
        if not os.path.exists(path):
            problems.append("路線檔不存在：%s" % fname)
            continue
        skip = fast and fname in TIMEOUT_ROUTES
        marks, times, opcounts = [], [], []
        first_over_deadline = None
        first_over_oplimit = None
        for i, n in enumerate(ENTRIES, 1):
            if skip:
                marks.append(None); times.append(None); opcounts.append(None)
                continue
            stdin = S.render_input(n)
            got, ms, status = run_route(path, stdin, KILL_TIMEOUT_S)
            ok = status == "ok" and got == S.render_expected(n)
            marks.append(ok)
            times.append(round(ms, 2))
            if ms * PYODIDE_FACTOR > DEADLINE_MS and first_over_deadline is None:
                first_over_deadline = {"entry": i, "n": n,
                                       "cpython_ms": round(ms, 2),
                                       "pyodide_estimate_ms": round(ms * PYODIDE_FACTOR, 2)}
            # op 量測成本高（settrace 慢一到兩個數量級），只在該筆原生跑得夠快時做
            ops = None
            if status == "ok" and ms < OPCOUNT_GATE_MS:
                ops = count_ops(path, stdin, KILL_TIMEOUT_S)
            opcounts.append(ops)
            if ops is not None and ops > OP_LIMIT and first_over_oplimit is None:
                first_over_oplimit = {"entry": i, "n": n, "ops": ops}
        score = sum(1 for m in marks if m)
        # 瀏覽器投影得分：本機答對**且**該筆的 Pyodide 估計牆鐘 <= deadline
        # **且**該筆 op 數 <= op 上限。這才是判題頁面實際會給的分數。
        proj_marks = []
        for m, t, o in zip(marks, times, opcounts):
            if t is None:
                proj_marks.append(None)
                continue
            proj_marks.append(bool(m) and t * PYODIDE_FACTOR <= DEADLINE_MS
                              and (o is None or o <= OP_LIMIT))
        proj = sum(1 for m in proj_marks if m)
        cpython_ms = None if skip else round(sum(t for t in times if t is not None), 2)
        # 死亡筆數：牆鐘超過 deadline 或 op 超過上限的筆數（KILLED 路線的鑑別力指標）
        #
        # 死因歸屬必須誠實。2026-08-15 的瀏覽器實測推翻了本檔先前的結論：
        # 逐格掃描路線被記成「爆 deadline」，實際上死於 op 上限（第 9 筆
        # 175,342,739 op，17.5 倍超標），而瀏覽器上每筆死亡耗時一律約
        # 1,950 ms、與 n 無關——那是燒完 op 預算的固定時間，不是 5,000 ms
        # 牆鐘。誤判的成因是：op 量測自己先逾時回傳 None，而下面的投影
        # 邏輯把 None 當成「沒超過上限」，於是死因只剩牆鐘可歸。
        #
        # 現在改為：op 未量到就明說「本機無法判定死因」，不替它猜。
        dead_entries = 0
        unmeasured_ops = 0
        killed_by_op = 0
        killed_by_wall = 0
        for t, o in zip(times, opcounts):
            if t is None:
                continue
            over_wall = t * PYODIDE_FACTOR > DEADLINE_MS
            over_op = o is not None and o > OP_LIMIT
            if o is None:
                unmeasured_ops += 1
            if over_wall or over_op:
                dead_entries += 1
                if over_op:
                    killed_by_op += 1
                elif o is None:
                    pass  # 死因未定：牆鐘超標但 op 沒量到，不能斷言是牆鐘殺的
                else:
                    killed_by_wall += 1
        if unmeasured_ops:
            kill_mechanism = (
                "本機無法判定：有 %d 筆的 op 量測自己先逾時，"
                "牆鐘超標不足以證明死因是 deadline（op 可能早就爆掉）。"
                "死因必須以瀏覽器實測為準，見 trace-matrix 的 W 段。" % unmeasured_ops
            )
        elif killed_by_op and not killed_by_wall:
            kill_mechanism = "op 上限"
        elif killed_by_wall and not killed_by_op:
            kill_mechanism = "牆鐘 deadline"
        elif killed_by_op or killed_by_wall:
            kill_mechanism = "混合：%d 筆死於 op 上限、%d 筆死於牆鐘" % (killed_by_op, killed_by_wall)
        else:
            kill_mechanism = "無死亡筆數"
        # 扣掉 process 啟動地板後，「演算法本身」貢獻的牆鐘增量
        incr = [None if t is None else round(max(t - wall_floor_ms, 0.0), 2) for t in times]
        rec = {
            "file": fname, "label": label, "disposition": want_disp,
            "skipped": skip,
            "score": None if skip else "%d/20" % score,
            "score_n": None if skip else score,
            "browser_projected_score": None if skip else "%d/20" % proj,
            "browser_projected_score_n": None if skip else proj,
            "per_entry_browser_ok": proj_marks,
            "cpython_ms_total": cpython_ms,
            "pyodide_estimate_ms_total": None if skip else round(cpython_ms * PYODIDE_FACTOR, 2),
            "per_entry_cpython_ms": times,
            "per_entry_pyodide_estimate_ms": [None if t is None else round(t * PYODIDE_FACTOR, 2)
                                              for t in times],
            "per_entry_ops": opcounts,
            "per_entry_ok": marks,
            "wall_clock_reps": WALL_REPS,
            "wall_clock_statistic": "min of %d runs" % WALL_REPS,
            "process_start_floor_cpython_ms": wall_floor_ms,
            "per_entry_algorithm_increment_cpython_ms": incr,
            "max_entry_algorithm_increment_cpython_ms":
                None if skip else max(x for x in incr if x is not None),
            "max_entry_cpython_ms": None if skip else max(t for t in times if t is not None),
            "max_entry_cpython_ms_at_entry": None if skip else
                1 + times.index(max(t for t in times if t is not None)),
            # 撞上量測硬逾時的筆，記到的是工具上限而非真實耗時；標記出來免得被誤讀
            "max_entry_cpython_ms_is_measurement_cap": None if skip else
                max(t for t in times if t is not None) >= KILL_TIMEOUT_S * 1000,
            "max_entry_pyodide_estimate_ms": None if skip else
                round(max(t for t in times if t is not None) * PYODIDE_FACTOR, 2),
            "max_ops": max([o for o in opcounts if o is not None], default=None),
            "max_ops_at_entry": None if not [o for o in opcounts if o is not None] else
                1 + opcounts.index(max(o for o in opcounts if o is not None)),
            "op_margin_vs_limit": None if not [o for o in opcounts if o is not None] else
                round(OP_LIMIT / max(o for o in opcounts if o is not None), 2),
            "dead_entries": None if skip else dead_entries,
            "first_entry_over_deadline": first_over_deadline,
            "kill_mechanism": kill_mechanism,
            "entries_with_unmeasured_ops": unmeasured_ops,
            "browser_projected_score_is_a_model": True,
            "browser_projected_score_note": ("投影得分是模型，不是量測。它以本機牆鐘乘上 Pyodide 係數推得，無法建模『worker 死亡並丟棄全部已完成結果』這種失效——2026-08-15 實測顯示兩條 math.factorial 路線的真實得分是 0/20，而本模型分別給出 8/20 與 13/20。任何要寫進文件的瀏覽器得分一律引用 measure/browser-verification.jsonl，不得引用本欄。"),
            "first_entry_over_op_limit": first_over_oplimit,
        }
        # 牆鐘鑑別力的逐路線判定：演算法增量若不超過 process 啟動地板，
        # 這條路線的「最貴單筆」就只是量到啟動抖動，不可拿來歸因給某個 n。
        if not skip:
            mx = rec["max_entry_algorithm_increment_cpython_ms"]
            floored = mx <= wall_floor_ms
            rec["wall_clock_dominated_by_process_floor"] = floored
            rec["wall_clock_is_decisive"] = mx > CPYTHON_BUDGET_MS
            if mx > CPYTHON_BUDGET_MS:
                # 這條路線是被牆鐘殺死的，不能套用「牆鐘不具鑑別力」的說法。
                fod = first_over_deadline or {}
                n_timeout = sum(1 for t in times if t is not None and t >= KILL_TIMEOUT_S * 1000)
                rec["wall_clock_note"] = (
                    "牆鐘對本路線**就是**致死軸：演算法增量最大 %.2f ms，已超過本機等效"
                    "預算 %.0f ms（＝deadline %d ms ÷ Pyodide 係數 %d）。第一筆超標出現在 "
                    "entry %s（n = %s，%.2f ms → Pyodide 估計 %.2f ms）；其後有 %d 筆直接"
                    "撞上量測硬逾時 %d ms（那是量測工具的上限，不是該筆的真實耗時，"
                    "因此 max_entry_cpython_ms 的 entry 歸屬對本路線無意義）。"
                    "全 20 筆中有 %d 筆死亡。"
                    % (mx, CPYTHON_BUDGET_MS, DEADLINE_MS, PYODIDE_FACTOR,
                       fod.get("entry", "?"), fod.get("n", "?"),
                       fod.get("cpython_ms", -1), fod.get("pyodide_estimate_ms", -1),
                       n_timeout, KILL_TIMEOUT_S * 1000, dead_entries))
                if want_disp == "UNCLEAN_DEATH":
                    rec["wall_clock_note"] += (
                        " 但**本機的乾淨逾時不會在瀏覽器重現**：時間全花在 math.factorial "
                        "這個單一 C 呼叫內，期間不回到 bytecode 邊界，op 計數器與中斷旗標"
                        "都檢查不到（本路線量得到 op 數的最貴一筆只有 %s op，遠低於上限 %d，"
                        "正是這個現象的指紋）。瀏覽器端會整個卡住而非乾淨判 TLE，"
                        "這才是 UNCLEAN_DEATH 的意思。"
                        % (rec["max_ops"], OP_LIMIT))
            elif floored:
                rec["wall_clock_note"] = (
                    "牆鐘對本路線不具鑑別力。20 筆的最大演算法增量僅 %.2f ms，"
                    "不超過 process 啟動地板 %.2f ms；最貴單筆落在 entry %d（n = %d），"
                    "而非最大筆 n = %d——那是啟動抖動而非 n 的函數。"
                    "本路線唯一有效的成本軸是 op 數（max_ops = %s，上限 %d）。"
                    % (mx, wall_floor_ms, rec["max_entry_cpython_ms_at_entry"],
                       ENTRIES[rec["max_entry_cpython_ms_at_entry"] - 1], max(ENTRIES),
                       rec["max_ops"], OP_LIMIT))
            else:
                rec["wall_clock_note"] = (
                    "牆鐘有可量的演算法增量（最大 %.2f ms，超過 process 啟動地板 %.2f ms，"
                    "落在 entry %d／n = %d），但相對每筆 deadline %d ms 仍只佔 %.2f%%，"
                    "不構成鑑別軸。鑑別軸是 op 數（max_ops = %s，上限 %d）。"
                    % (mx, wall_floor_ms, rec["max_entry_cpython_ms_at_entry"],
                       ENTRIES[rec["max_entry_cpython_ms_at_entry"] - 1],
                       DEADLINE_MS, mx * PYODIDE_FACTOR / DEADLINE_MS * 100,
                       rec["max_ops"], OP_LIMIT))
        routes_report.append(rec)

        if skip:
            continue
        if want_score is not None and score != want_score:
            problems.append("路線 %s 得分 %d/20，契約要求 %d/20" % (fname, score, want_score))
        # 處置一致性斷言
        if want_disp in ("REFERENCE", "ACCEPTED"):
            if score != 20:
                problems.append("%s 宣告為 %s 卻不是 20/20" % (fname, want_disp))
            if proj != 20:
                problems.append("%s 宣告為 %s，瀏覽器投影得分只有 %d/20" % (fname, want_disp, proj))
            if rec["max_entry_pyodide_estimate_ms"] > DEADLINE_MS:
                problems.append("%s 宣告為 %s，但最慢一筆 Pyodide 估計 %.1f ms > %d ms"
                                % (fname, want_disp, rec["max_entry_pyodide_estimate_ms"], DEADLINE_MS))
            if rec["max_ops"] is not None and rec["max_ops"] > OP_LIMIT:
                problems.append("%s 宣告為 %s，但最大 op 數 %d > %d"
                                % (fname, want_disp, rec["max_ops"], OP_LIMIT))
        if want_disp == "KILLED":
            # KILLED 可以死在 deadline，也可以死在 op 上限——兩者擇一即可，但至少要有一個
            if first_over_deadline is None and first_over_oplimit is None:
                problems.append("%s 宣告為 KILLED，卻既沒超過 deadline 也沒超過 op 上限" % fname)
            if proj == 20:
                problems.append("%s 宣告為 KILLED，瀏覽器投影得分卻是滿分" % fname)
            rec["kill_by"] = ("deadline" if first_over_deadline else "") + \
                             ("+op_limit" if first_over_oplimit else "")
        if want_disp == "WRONG_ANSWER" and score > WRONG_SCORE_CAP:
            problems.append("%s 宣告為 WRONG_ANSWER，得分 %d/20 超過低分上限 %d"
                            % (fname, score, WRONG_SCORE_CAP))

    by_file = {r["file"]: r for r in routes_report}

    # ── E. 跨路線契約 ────────────────────────────────────────────────
    ref = by_file.get("r015_ref_formula.py")
    kil = by_file.get("r015_cellscan.py")
    for accname in SPELLING_ROUTES:
        acc = by_file.get(accname)
        if not acc or acc["skipped"]:
            continue
        if acc["max_entry_pyodide_estimate_ms"] >= DEADLINE_MS:
            problems.append("%s 在 Pyodide 估計下已超過 deadline，難度階梯不成立" % accname)
        if acc["max_ops"] is None:
            problems.append("%s 最貴那一筆沒量到 op 數，無法證明它過得了 op 上限" % accname)

    # E-1（X-1 上界決議的機械守門）：同一條 O(n^2) 演算法的三種自然寫法，
    # 在**最大筆**（n = N_MAX）上必須同時活著，且最貴的一種仍有足夠餘裕。
    # 這條斷言就是 n 上界從 3000 降到 1000 的理由；放寬它等於放回刀鋒。
    last_i = len(ENTRIES) - 1
    spell_ops = {}
    for name in SPELLING_ROUTES:
        r = by_file.get(name)
        if not r or r["skipped"]:
            problems.append("寫法路線 %s 缺席，無法驗證 op 刀鋒已消除" % name)
            continue
        o = r["per_entry_ops"][last_i]
        if o is None:
            problems.append("%s 在最大筆（n = %d）沒量到 op 數" % (name, ENTRIES[last_i]))
            continue
        spell_ops[name] = o
        if o > OP_LIMIT:
            problems.append("%s 在最大筆（n = %d）用掉 %d op，超過上限 %d"
                            % (name, ENTRIES[last_i], o, OP_LIMIT))
    spelling_margin = None
    if len(spell_ops) == len(SPELLING_ROUTES):
        worst = max(spell_ops.values())
        spelling_margin = round(OP_LIMIT / worst, 2)
        if spelling_margin < MIN_OP_MARGIN:
            problems.append("三種 O(n^2) 寫法最貴者在最大筆用掉 %d op，餘裕僅 %.2f 倍，"
                            "低於契約要求的 %.1f 倍（刀鋒未消除）"
                            % (worst, spelling_margin, MIN_OP_MARGIN))

    # E-2：O(n^3) 逐格掃描必須在**足夠多筆**上死亡，鑑別力才不是靠單筆僥倖。
    if kil and not kil["skipped"]:
        if kil["first_entry_over_deadline"] is None:
            problems.append("O(n^3) 路線沒有實測到任何一筆超過 deadline")
        if kil["dead_entries"] < MIN_CELLSCAN_KILLS:
            problems.append("O(n^3) 路線只在 %d 筆上死亡，契約要求至少 %d 筆"
                            % (kil["dead_entries"], MIN_CELLSCAN_KILLS))

    # E-3（F-2 的機械守門）：牆鐘歸因必須自洽。
    # REFERENCE 是 O(n) 路線，它的 20 筆牆鐘應該整段被 process 啟動地板吃掉；
    # 若哪天不是，報告裡「牆鐘不具鑑別力」的說法就得改，這條斷言會先叫。
    if ref and not ref["skipped"]:
        if not ref["wall_clock_dominated_by_process_floor"]:
            problems.append("REFERENCE 路線的牆鐘不再被 process 啟動地板主導"
                            "（最大增量 %.2f ms > 地板 %.2f ms），報告的牆鐘註解需重寫"
                            % (ref["max_entry_algorithm_increment_cpython_ms"], wall_floor_ms))
        # 最貴單筆若不在最大筆，就禁止把它歸因給最大筆（前一輪的 F-2 原型錯誤）
        if ref["max_entry_cpython_ms_at_entry"] == len(ENTRIES) \
                and ref["max_entry_algorithm_increment_cpython_ms"] == 0:
            problems.append("REFERENCE 最貴單筆恰好落在最大筆但增量為 0，"
                            "此巧合會誘發錯誤歸因，請提高 WALL_REPS 重量")
    # 三種寫法對 deadline 的實際佔比：拿來證明牆鐘即使有增量也不是鑑別軸
    spelling_wall_pct = {}
    for name in SPELLING_ROUTES:
        r = by_file.get(name)
        if r and not r["skipped"]:
            spelling_wall_pct[name] = round(
                r["max_entry_algorithm_increment_cpython_ms"] * PYODIDE_FACTOR
                / DEADLINE_MS * 100, 2)
    if spelling_wall_pct and max(spelling_wall_pct.values()) > 25:
        problems.append("O(n^2) 寫法的牆鐘已吃掉 deadline 的 %.1f%%，"
                        "牆鐘開始有鑑別力，報告的「唯一鑑別軸是 op 數」說法需重寫"
                        % max(spelling_wall_pct.values()))
    # 陣亡提交的累計牆鐘：20 筆都撞滿 deadline 時的總時間，供頁面體感風險評估
    report_kill_wall = DEADLINE_MS * len(ENTRIES)
    # 題面範例（第 1 筆，n = 8）必須能當場鑑別所有 WRONG 路線
    for fname, label, disp, _ in ROUTES:
        if disp != "WRONG_ANSWER":
            continue
        r = by_file.get(fname)
        if r and not r["skipped"] and r["per_entry_ok"][0]:
            problems.append("entry 1（題面範例 n = 8）無法鑑別 %s" % fname)

    report = {
        "challenge": "apcs015",
        "slug": "ap-layout-plan",
        "algorithm": "ap_layout_plan",
        "deadline_ms": DEADLINE_MS,
        "op_limit": OP_LIMIT,
        "op_measurement_source": "verify/judge_ops.py::count_ops_source"
                                 "（本 change 唯一允許的 op 量測來源；plan015.py 不自帶 tracer）",
        "op_measurement_harness_baseline": op_baseline,
        "op_measurement_note": "各路線 op 數含讀入／輸出外殼約 %s 的固定開銷，"
                               "相對瀏覽器實際成本為高估（保守方向）" % op_baseline,
        "pyodide_factor": PYODIDE_FACTOR,
        "cpython_budget_ms_per_entry": CPYTHON_BUDGET_MS,
        "n_max": S.N_MAX,
        "n_max_rationale":
            "n 上界由 3000 下修為 1000。n=3000 時同一條 O(n^2) 演算法的三種自然寫法"
            "（明寫迴圈／sum 產生器／抽小函式）落在 op 上限兩側，學生想法相同卻因寫法"
            "生死不同；n=1000 時三者同生且最貴者仍有 %s 倍餘裕。O(n^3) 路線在 n=199 一帶"
            "即已爆 deadline，鑑別力不受此變更影響，difficulty 維持 easy。"
            "出處 measure/opprobe_015_nbound.py。"
            % ("%.2f" % spelling_margin if spelling_margin else "未量到"),
        "spelling_ops_at_max_entry": spell_ops,
        "spelling_worst_op_margin": spelling_margin,
        "spelling_op_margin_required": MIN_OP_MARGIN,
        # ── 牆鐘的兩層分解：process 啟動地板 vs 演算法增量 ──────────────
        "wall_clock_reps": WALL_REPS,
        "wall_clock_statistic": "每筆重複 %d 次取最小值（單發量測會抓到排程尖峰）" % WALL_REPS,
        "process_start_floor_cpython_ms": wall_floor_ms,
        "process_start_floor_note":
            "以 probe_opbaseline.py（只讀一個整數再輸出、無任何演算法）量得的 CPython "
            "process 啟動地板，同樣取 %d 次最小值。各路線 per_entry_cpython_ms 幾乎整段"
            "都是這條地板；per_entry_algorithm_increment_cpython_ms 才是演算法本身的增量。"
            % WALL_REPS,
        "spelling_wall_pct_of_deadline": spelling_wall_pct,
        "wall_clock_note":
            "牆鐘不是本題的鑑別軸，理由分兩段、都由本檔實測支撐："
            "(1) REFERENCE 的 O(n) 路線最大演算法增量 %.2f ms，不超過 process 啟動地板 "
            "%.2f ms——它的『最貴單筆』落在 entry %s（n = %s）而非最大筆，那是啟動抖動，"
            "**不可**歸因給任何特定 n；"
            "(2) 三種 O(n^2) 寫法確實有可量的增量，但換算成 Pyodide 後最多只佔每筆 "
            "deadline %d ms 的 %s%%。牆鐘唯一真的說話的地方是 %s——那是量級差異，"
            "不是雜訊，該些路線的 wall_clock_is_decisive 為 true。"
            "在活著的路線之間，鑑別軸是 op 數：judge_ops 量得、與執行速度無關、"
            "可原封搬到 Pyodide。"
            % (ref["max_entry_algorithm_increment_cpython_ms"] if ref and not ref["skipped"] else -1,
               wall_floor_ms,
               ref["max_entry_cpython_ms_at_entry"] if ref and not ref["skipped"] else "?",
               ENTRIES[ref["max_entry_cpython_ms_at_entry"] - 1]
               if ref and not ref["skipped"] else "?",
               DEADLINE_MS,
               max(spelling_wall_pct.values()) if spelling_wall_pct else "?",
               "、".join(r["file"] for r in routes_report
                         if r.get("wall_clock_is_decisive")) or "（無）"),
        "entries": ENTRIES,
        "entry_count": len(ENTRIES),
        "entries_derivation": "由 derive_entries() 從契約導出："
                              "題面範例＋k<3 分支邊界 %s、小規模帶 %s 幾何取點、"
                              "大規模帶 %s 線性等距（含上界）" % (N_HEAD, N_SMALL_BAND, N_LARGE_BAND),
        "big_threshold": BIG_THRESHOLD,
        "entries_ge_threshold": len(big),
        "max_input_bytes": max(r["input_bytes"] for r in per_entry),
        "max_output_bytes": max_out,
        "total_output_bytes": total_out_bytes,
        "worst_case_dead_submission_wall_ms": report_kill_wall,
        "per_entry": per_entry,
        "routes": routes_report,
        "problems": problems,
    }

    if write and not problems:
        os.makedirs(OUT_DIR, exist_ok=True)
        os.makedirs(MEASURE_DIR, exist_ok=True)
        with open(os.path.join(OUT_DIR, "plan015.yaml"), "w") as fh:
            fh.write("# 由 plan015.py 產生，請勿手改。apcs015 / ap-layout-plan\n")
            fh.write("testcase_plan:\n")
            for n in ENTRIES:
                fh.write("  - literal: |\n      %d\n" % n)
        with open(os.path.join(MEASURE_DIR, "routes015.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    summary = {
        "entries": ENTRIES,
        "n_max": S.N_MAX,
        "entries_ge_threshold": len(big),
        "process_start_floor_cpython_ms": wall_floor_ms,
        "wall_clock_reps": WALL_REPS,
        "spelling_ops_at_max_entry": spell_ops,
        "spelling_worst_op_margin": spelling_margin,
        "max_input_bytes": report["max_input_bytes"],
        "max_output_bytes": max_out,
        "total_output_bytes": total_out_bytes,
        "routes": [
            {"file": r["file"], "disposition": r["disposition"], "score": r["score"],
             "browser_projected": r["browser_projected_score"],
             "max_entry_cpython_ms": r["max_entry_cpython_ms"],
             "max_entry_cpython_ms_at_entry": r["max_entry_cpython_ms_at_entry"],
             "max_algo_increment_ms": r["max_entry_algorithm_increment_cpython_ms"],
             "max_ops": r["max_ops"],
             "max_ops_at_entry": r["max_ops_at_entry"],
             "dead_entries": r["dead_entries"],
             "first_over_deadline": r["first_entry_over_deadline"]}
            for r in routes_report
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if problems:
        print("\n斷言牆失敗（未寫出 literal）：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n斷言牆全數通過。")
    return 0


if __name__ == "__main__":
    sys.exit(main(write="--check" not in sys.argv, fast="--fast" in sys.argv))
