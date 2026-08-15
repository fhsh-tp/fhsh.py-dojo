"""apcs016 — traced op 實測探針。

**本檔不再自帶 tracer。** op 量測一律 import ``verify/judge_ops.py``，那是本
change 唯一允許的 op 定義正本。舊版在自己的 tracer 裡做了兩層過濾
（``frame.f_code.co_filename != "route"`` 與 ``event == "line"``），而判題器
（.vitepress/theme/workers/worker-utils.ts 的 opGuard）兩者都不過濾，且
``return _tracer`` 會讓被呼叫的函式繼續被追蹤——對帶函式呼叫的寫法會系統性
低估。apcs016 的三條路線都沒有自訂函式，低估幅度剛好接近零，但定義本身是錯的，
換一條寫法就會爆掉，所以連定義一起換掉。

量測範圍：7 條路線 × 全部 20 筆 literal（不是抽樣三筆）。最壞一筆由實測結果
決定，不由人工挑選——舊證物就是靠人工挑選才把最壞筆數標成 entry 18
（n − k = 999,980），實際最壞是 entry 5（n − k = 1,000,000）。

執行：python3 probe_ops016.py（本檔位於 measure/）
輸出：measure/ops016.json（逐路線逐筆 op 數的機械正本）
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # = measure/
CHANGE = os.path.dirname(HERE)
CURATION = os.path.join(CHANGE, "curation")
sys.path.insert(0, CURATION)
sys.path.insert(0, os.path.join(CHANGE, "verify"))

import plan016 as P  # noqa: E402  — 20 筆 literal 的正本
import semantics016 as S  # noqa: E402
from judge_ops import OP_LIMIT, count_ops_source  # noqa: E402

ROUTES_DIR = os.path.join(CURATION, "routes")
OUT = HERE                                                  # report json 一律落在 measure/

FILES = {
    "REF_pow3": "r016_ref_pow3.py",
    "A1_loop": "r016_a1_loop.py",
    "A2_bigint": "r016_a2_bigint.py",
    "W1_ignore_k": "r016_w1_ignore_k.py",
    "W2_use_k": "r016_w2_use_k.py",
    "W3_plain_diff": "r016_w3_plain_diff.py",
    "W4_nomod": "r016_w4_nomod.py",
}
MUST_FIT = ("REF_pow3", "A1_loop", "A2_bigint")  # ACCEPTED/REFERENCE：一定要在上限內


def ops_of(src, n, k):
    """回傳 (op 數, 例外型別名或 None)。

    程式若中途拋例外（W4_nomod 在位數超過 int -> str 上限時就會），op 數會
    隨例外一起遺失；那種情形回傳 (None, 例外名)，並在報告裡如實標示。
    """
    try:
        ops, _ = count_ops_source(src, S.render_input(n, k))
        return ops, None
    except BaseException as exc:  # noqa: BLE001 — 要如實記錄死法
        return None, type(exc).__name__


def main():
    routes = {}
    problems = []
    for name, fname in FILES.items():
        with open(os.path.join(ROUTES_DIR, fname)) as fh:
            src = fh.read()
        per_entry = []
        for i, (n, k) in enumerate(P.ENTRIES, 1):
            ops, err = ops_of(src, n, k)
            per_entry.append({"entry": i, "n": n, "k": k, "free_cells": n - k,
                              "ops": ops, "error": err})
        done = [r for r in per_entry if r["ops"] is not None]
        worst = max(done, key=lambda r: r["ops"]) if done else None
        routes[name] = {
            "file": "routes/" + fname,
            "worst_ops": worst["ops"] if worst else None,
            "worst_entry": worst["entry"] if worst else None,
            "worst_entry_n": worst["n"] if worst else None,
            "worst_entry_k": worst["k"] if worst else None,
            "worst_entry_free_cells": worst["free_cells"] if worst else None,
            "op_limit_pct": round(worst["ops"] / OP_LIMIT * 100, 3) if worst else None,
            "died_entries": [r["entry"] for r in per_entry if r["error"]],
            "errors": sorted({r["error"] for r in per_entry if r["error"]}),
            "per_entry": per_entry,
        }
        if name in MUST_FIT:
            if worst is None or routes[name]["died_entries"]:
                problems.append("%s 有筆數沒跑完：%s" % (name, routes[name]["errors"]))
            elif worst["ops"] > OP_LIMIT:
                problems.append("%s 最壞 op 數 %d > 上限 %d（entry %d）"
                                % (name, worst["ops"], OP_LIMIT, worst["entry"]))

    payload = {
        "challenge": "apcs016 跑馬燈顯示計數",
        "op_counter_source": "verify/judge_ops.py（判題器 opGuard 的忠實複刻）",
        "op_limit": OP_LIMIT,
        "entries_measured": len(P.ENTRIES),
        "routes": routes,
        "problems": problems,
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "ops016.json"), "w") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)

    for name in FILES:
        r = routes[name]
        print("%-14s worst entry #%-3s n=%-8s k=%-8s free=%-8s ops=%-10s %6s%% of cap  %s"
              % (name, r["worst_entry"], r["worst_entry_n"], r["worst_entry_k"],
                 r["worst_entry_free_cells"], r["worst_ops"], r["op_limit_pct"],
                 ("死於 " + ",".join(r["errors"]) + " @entry " +
                  ",".join(map(str, r["died_entries"]))) if r["errors"] else ""))
    if problems:
        print("\nop 斷言失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\nop 斷言全數通過（7 條路線 × %d 筆，計數來源 verify/judge_ops.py）。"
          % len(P.ENTRIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
