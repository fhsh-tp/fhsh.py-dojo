"""apcs016 — 路線實測（得分 × 本機 CPython 毫秒 × Pyodide 估計）。

執行：python3 measure016.py（本檔位於 measure/，量測腳本一律落在這裡）
輸出：measure/routes016.json

量法：把 routes/*.py 的原始碼在本行程內 exec，stdin/stdout 各自導向字串，
      用 perf_counter 量「單筆」與「整塊 20 筆」的牆鐘。不走 subprocess，
      免得把直譯器啟動時間算進路線成本。
      **每筆固定重跑 7 次取最小值**：單發量測會抓到背景尖峰，症狀是小 n 的
      那筆看起來比大 n 還慢一倍，那是雜訊不是成本。

op 量測：不自帶 tracer，一律 import verify/judge_ops.py（判題器 opGuard 的
      忠實複刻：不過濾 event、不過濾檔名、return tracer）。

換算：Pyodide 純 Python 迴圈約為本機 CPython 的 3–5 倍慢，一律取 ×4。
判題硬約束：每筆測資 deadline = 5000 ms、op 上限 10,000,000。

W4_nomod（忘記取餘數）另做兩種量測：
  * 預設環境：CPython 3.11+ 的 int -> str 有 4300 位上限，n − k 大時 print() 直接
    丟 ValueError —— 這是**乾淨的死法**（bytecode 邊界上的例外，判題器收得到）。
  * 把上限解除後再量一次：確認即使沒有上限，輸出也只是很長（約 30 萬位）而非跑不完。

  這條路線的 20 筆**分成三類、不是兩類**：正確、拋例外、以及「印得出來但答案是錯的」
  （安靜的 WRONG_ANSWER）。三類的筆序與計數由 nomod_outcomes() 從實跑結果機械
  導出並寫進 routes016.json，不由任何人口算 20 − 6。這個衍生鍵存在的理由，就是
  2026-08-15 稽核抓到的散文誤述——當時 spec 與矩陣都寫成「其餘各筆皆拋例外」。

自我測試：python3 measure016.py --self-test
  用注入過的假 per_entry 驗證 nomod_outcomes() 的每一條斷言真的會叫。
"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))          # = measure/
CHANGE = os.path.dirname(HERE)
CURATION = os.path.join(CHANGE, "curation")
sys.path.insert(0, CURATION)
sys.path.insert(0, os.path.join(CHANGE, "verify"))
import plan016 as P  # noqa: E402
import semantics016 as S  # noqa: E402
from judge_ops import OP_LIMIT, count_ops_source  # noqa: E402

ROUTES_DIR = os.path.join(CURATION, "routes")
MEASURE_DIR = HERE

PYODIDE_FACTOR = 4          # 本機 CPython 毫秒 × 4 = Pyodide 估計毫秒
DEADLINE_MS = 5000          # 每筆測資 deadline
REPEATS = 7                 # 固定 7 次取最小值：單發尖峰會讓小 n 量得比大 n 還慢

ROUTE_FILES = {
    "REF_pow3": ("r016_ref_pow3.py", "REFERENCE"),
    "A1_loop": ("r016_a1_loop.py", "ACCEPTED"),
    "A2_bigint": ("r016_a2_bigint.py", "ACCEPTED"),
    "W1_ignore_k": ("r016_w1_ignore_k.py", "WRONG_ANSWER"),
    "W2_use_k": ("r016_w2_use_k.py", "WRONG_ANSWER"),
    "W3_plain_diff": ("r016_w3_plain_diff.py", "WRONG_ANSWER"),
    "W4_nomod": ("r016_w4_nomod.py", "WRONG_ANSWER"),
}


def run_once(src, stdin_text):
    """跑一次路線，回傳 (毫秒, 輸出字串或 None, 例外型別名或 None)。"""
    old_in, old_out = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(stdin_text)
    sys.stdout = buf = io.StringIO()
    err = None
    t0 = time.perf_counter()
    try:
        exec(compile(src, "route", "exec"), {"__name__": "__main__"})
    except BaseException as e:  # noqa: BLE001 — 要如實記錄死法
        err = type(e).__name__
    ms = (time.perf_counter() - t0) * 1000
    sys.stdin, sys.stdout = old_in, old_out
    return ms, (None if err else buf.getvalue()), err


def measure(name, filename, big_int_str=False):
    src = open(os.path.join(ROUTES_DIR, filename)).read()
    old_limit = sys.get_int_max_str_digits()
    if big_int_str:
        sys.set_int_max_str_digits(1_000_000)
    per_entry = []
    score = 0
    for i, (n, k) in enumerate(P.ENTRIES, 1):
        stdin_text = S.render_input(n, k)
        expected = S.render_expected(n, k)
        best, out, err = None, None, None
        for _ in range(REPEATS):
            ms, o, e = run_once(src, stdin_text)
            if best is None or ms < best:
                best, out, err = ms, o, e
        ok = err is None and out.strip() == expected.strip()
        if ok:
            score += 1
        per_entry.append({
            "entry": i, "n": n, "k": k,
            "cpython_ms": round(best, 3),
            "pyodide_estimate_ms": round(best * PYODIDE_FACTOR, 3),
            "ok": ok,
            "error": err,
            "out_len": (len(out.strip()) if out is not None else 0),
        })
    sys.set_int_max_str_digits(old_limit)
    total = sum(r["cpython_ms"] for r in per_entry)
    worst = max(per_entry, key=lambda r: r["cpython_ms"])
    # 「最壞單筆」的身分穩不穩：本題最大的兩筆（entry 5 的 n−k = 1,000,000 與
    # entry 18 的 999,980）工作量只差 0.002%，牆鐘上誰勝出純粹看那一次的排程，
    # 跨次執行會互換。把近似平手的筆數機械列出來，免得下一輪把兩次量到的不同
    # entry 讀成矛盾——要指名最壞一筆請用 op 軸（worst_traced_ops_entry，決定性）。
    near = [r["entry"] for r in per_entry
            if worst["cpython_ms"] > 0 and r["cpython_ms"] >= worst["cpython_ms"] * 0.9]
    return {
        "score": "%d/20" % score,
        "block_cpython_ms": round(total, 3),
        "block_pyodide_estimate_ms": round(total * PYODIDE_FACTOR, 3),
        "worst_entry": worst["entry"],
        "worst_cpython_ms": worst["cpython_ms"],
        "worst_pyodide_estimate_ms": worst["pyodide_estimate_ms"],
        "worst_deadline_headroom_ms": round(DEADLINE_MS - worst["pyodide_estimate_ms"], 3),
        "worst_entry_near_ties": near,
        "worst_entry_note": (
            "最壞單筆的身分不穩定：entry %s 的牆鐘都落在最大值的 10%% 以內，跨次執行"
            "會互換（本題最大的兩筆工作量只差 0.002%%）。要指名最壞一筆請用 "
            "worst_traced_ops_entry，op 數是決定性的。" % near
            if len(near) > 1 else
            "最壞單筆明確落在 entry %d（其餘各筆都低於它 10%% 以上）。" % worst["entry"]),
        "errors": sorted({r["error"] for r in per_entry if r["error"]}),
        "max_out_len": max(r["out_len"] for r in per_entry),
        "per_entry": per_entry,
    }


def nomod_outcomes(per_entry, plan_unprintable=None):
    """把 W4_nomod 的實跑結果分成三類，回傳 (衍生鍵, problems)。

    分類一律看**實跑結果**，不看預測：
      * 正確        —— ``ok`` 為真
      * 拋例外      —— ``error`` 非 None（整數轉字串位數上限 → ValueError）
      * 安靜的錯答  —— ``ok`` 為假且 ``error`` 為 None：印得出來、但值是錯的

    第三類是 2026-08-15 稽核的 L2-F6：spec 與矩陣都把「不正確」等同於「拋例外」，
    於是 6 + 9 = 15 卻宣稱涵蓋 20 筆。本函式讓三個計數各自有機械出處。

    ``plan_unprintable`` 若給定（``measure/report016.json`` 的
    ``nomod_unprintable_entries``），另做跨檔一致性斷言：plan016.py 是用
    ``len(str(2**free))`` **預測**哪幾筆印不出來，本檔是**真的跑**。兩者不一致
    表示其中一份證物失真，不可靜靜放過。
    """
    problems = []
    correct = [r["entry"] for r in per_entry if r["ok"]]
    raised = [r["entry"] for r in per_entry if r["error"] is not None]
    silent = [r["entry"] for r in per_entry if not r["ok"] and r["error"] is None]

    total = len(per_entry)
    if sorted(correct + raised + silent) != sorted(r["entry"] for r in per_entry):
        problems.append("W4_nomod 三分類未構成 1..%d 的分割：正確 %s／例外 %s／安靜錯答 %s"
                        % (total, correct, raised, silent))
    if len(correct) + len(raised) + len(silent) != total:
        problems.append("W4_nomod 三分類計數和 %d != 筆數 %d"
                        % (len(correct) + len(raised) + len(silent), total))
    # 「正確」與「拋例外」互斥：拋例外的那一筆不可能同時被記成得分。
    overlap = sorted(set(correct) & set(raised))
    if overlap:
        problems.append("W4_nomod 有筆序同時被記成正確與拋例外：%s" % overlap)
    # spec 現在明寫「兩種死法都必須存在」；任一類空掉就是那句 SHALL 失真。
    if not raised:
        problems.append("W4_nomod 沒有任何一筆拋例外，spec 的兩段式敘述已失真")
    if not silent:
        problems.append("W4_nomod 沒有任何一筆是安靜的錯答，spec 的兩段式敘述已失真")
    if plan_unprintable is not None and sorted(plan_unprintable) != sorted(raised):
        problems.append(
            "W4_nomod 實跑拋例外的筆序 %s 與 report016.json 的 nomod_unprintable_entries "
            "%s 不一致（預測與實測分岔）" % (raised, sorted(plan_unprintable)))

    derived = {
        "nomod_correct_entries": correct,
        "nomod_correct_count": len(correct),
        "nomod_exception_entries": raised,
        "nomod_exception_count": len(raised),
        "nomod_wrong_no_exception_entries": silent,
        "nomod_wrong_no_exception_count": len(silent),
        "nomod_outcome_note":
            "三類互斥且窮盡（正確 %d ＋ 拋例外 %d ＋ 安靜錯答 %d ＝ %d）。安靜錯答是"
            "「印得出來但值錯」的筆，判題器記 WRONG_ANSWER 而非例外——把它併進"
            "「拋例外」是 2026-08-15 稽核抓到的散文誤述。"
            % (len(correct), len(raised), len(silent), total),
    }
    return derived, problems


def load_plan_unprintable():
    """讀 measure/report016.json 的 nomod_unprintable_entries；沒有就回 None。"""
    path = os.path.join(MEASURE_DIR, "report016.json")
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh).get("nomod_unprintable_entries")


# --- 自我測試（負向控制：注入錯誤，證明斷言真的會叫）-------------------------

def _rows(spec):
    """``spec`` 是 (ok, error) 序列，轉成 nomod_outcomes 吃的 per_entry。"""
    return [{"entry": i, "ok": ok, "error": err} for i, (ok, err) in enumerate(spec, 1)]


def self_test():
    problems = []

    # 正向：6 正確 + 9 例外 + 5 安靜錯答（＝本題實際形狀），應零 problems
    good = _rows([(True, None)] * 6 + [(False, "ValueError")] * 9 + [(False, None)] * 5)
    derived, probs = nomod_outcomes(good, plan_unprintable=list(range(7, 16)))
    if probs:
        problems.append("正向案例應零斷言失敗，實得：%s" % probs)
    want = {"nomod_correct_count": 6, "nomod_exception_count": 9,
            "nomod_wrong_no_exception_count": 5}
    for key, value in want.items():
        if derived[key] != value:
            problems.append("正向案例 %s 應為 %d，實得 %r" % (key, value, derived[key]))

    # 負向 1：所有錯的筆都拋例外 → 安靜錯答類空掉（正是被誤述成的那個世界）
    _, probs = nomod_outcomes(_rows([(True, None)] * 6 + [(False, "ValueError")] * 14))
    if not any("安靜的錯答" in p for p in probs):
        problems.append("負向 1（安靜錯答類空掉）未觸發，實得：%s" % probs)

    # 負向 2：沒有任何一筆拋例外
    _, probs = nomod_outcomes(_rows([(True, None)] * 6 + [(False, None)] * 14))
    if not any("拋例外" in p and "已失真" in p for p in probs):
        problems.append("負向 2（例外類空掉）未觸發，實得：%s" % probs)

    # 負向 3：ok 與 error 同時成立 → 分類重疊
    _, probs = nomod_outcomes(_rows([(True, "ValueError")] * 6 + [(False, "ValueError")] * 9
                                    + [(False, None)] * 5))
    if not any("同時被記成正確與拋例外" in p for p in probs):
        problems.append("負向 3（分類重疊）未觸發，實得：%s" % probs)

    # 負向 4：plan016 的預測與實跑不一致（跨檔證物分岔）
    _, probs = nomod_outcomes(good, plan_unprintable=[1, 2, 3])
    if not any("預測與實測分岔" in p for p in probs):
        problems.append("負向 4（跨檔不一致）未觸發，實得：%s" % probs)

    if problems:
        print("SELF-TEST FAIL")
        for p in problems:
            print("  -", p)
        return 1
    print("SELF-TEST PASS：nomod_outcomes 的正向案例乾淨，四個負向注入全部會叫。")
    return 0


def main():
    results = {}
    for name, (filename, disposition) in ROUTE_FILES.items():
        r = measure(name, filename)
        r["file"] = "routes/" + filename
        r["disposition"] = disposition
        results[name] = r
    # 忘記取餘數：把 int -> str 上限解除後再量一次
    results["W4_nomod_unlimited_str"] = measure("W4_nomod", ROUTE_FILES["W4_nomod"][0], big_int_str=True)
    results["W4_nomod_unlimited_str"]["file"] = "routes/" + ROUTE_FILES["W4_nomod"][0]
    results["W4_nomod_unlimited_str"]["disposition"] = "WRONG_ANSWER"

    # traced op 實測 —— 計數器一律來自 verify/judge_ops.py（不過濾 event、不過濾檔名、
    # return tracer），與判題器 opGuard 同一份定義。最壞一筆由 20 筆實測結果決定。
    traced = {}
    for name in ("REF_pow3", "A1_loop", "A2_bigint"):
        src = open(os.path.join(ROUTES_DIR, ROUTE_FILES[name][0])).read()
        per_ops = [(count_ops_source(src, S.render_input(n, k))[0], i)
                   for i, (n, k) in enumerate(P.ENTRIES, 1)]
        best = max(per_ops, key=lambda t: t[0])  # 平手取最小 entry，與 probe_ops016 一致
        traced[name] = best[0]
        results[name]["worst_traced_ops"] = best[0]
        results[name]["worst_traced_ops_entry"] = best[1]
        results[name]["worst_traced_ops_free_cells"] = (
            P.ENTRIES[best[1] - 1][0] - P.ENTRIES[best[1] - 1][1])
        results[name]["traced_ops_per_entry"] = [o for o, _ in per_ops]

    problems = []
    for name in ("REF_pow3", "A1_loop", "A2_bigint"):
        if traced[name] > OP_LIMIT:
            problems.append("%s 最壞 traced ops %d 超過上限" % (name, traced[name]))
        r = results[name]
        if r["score"] != "20/20":
            problems.append("%s 應為 20/20，實測 %s" % (name, r["score"]))
        if r["worst_pyodide_estimate_ms"] >= DEADLINE_MS:
            problems.append("%s 最壞一筆 Pyodide 估計 %.1f ms >= deadline %d ms"
                            % (name, r["worst_pyodide_estimate_ms"], DEADLINE_MS))
    for name in ("W1_ignore_k", "W2_use_k", "W3_plain_diff", "W4_nomod"):
        if results[name]["score"] == "20/20":
            problems.append("%s 竟然滿分" % name)

    # 「忘記取餘數」的三分類（正確／拋例外／安靜錯答）——F6 的機械出處。
    derived, nomod_problems = nomod_outcomes(results["W4_nomod"]["per_entry"],
                                             plan_unprintable=load_plan_unprintable())
    results["W4_nomod"].update(derived)
    problems.extend(nomod_problems)

    payload = {
        "challenge": "apcs016 跑馬燈顯示計數",
        "slug": "marquee-display-count",
        "algorithm": "marquee_display_count",
        "measured_on": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "pyodide_factor": PYODIDE_FACTOR,
            "repeats": REPEATS,
            "note": "cpython_ms 為 %d 次取最佳；pyodide_estimate_ms = cpython_ms × %d"
                    % (REPEATS, PYODIDE_FACTOR),
        },
        "deadline_ms": DEADLINE_MS,
        "op_cap": OP_LIMIT,
        "op_counter_source": "verify/judge_ops.py（判題器 opGuard 的忠實複刻）",
        "worst_traced_ops": traced,
        "routes": results,
        "problems": problems,
    }
    os.makedirs(MEASURE_DIR, exist_ok=True)
    with open(os.path.join(MEASURE_DIR, "routes016.json"), "w") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)

    for name, r in results.items():
        print("%-26s %-14s %-6s block %8.1f ms (pyodide ~%8.1f) worst#%-3d %7.1f ms (~%7.1f) %s"
              % (name, r["disposition"], r["score"], r["block_cpython_ms"],
                 r["block_pyodide_estimate_ms"], r["worst_entry"], r["worst_cpython_ms"],
                 r["worst_pyodide_estimate_ms"], ",".join(r["errors"]) or ""))
    if problems:
        print("\n實測斷言失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n實測斷言全數通過。")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else main())
