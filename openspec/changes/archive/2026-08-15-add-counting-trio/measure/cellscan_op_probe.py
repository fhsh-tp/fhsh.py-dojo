"""量測 KILLED 路線 r015_cellscan.py 在死亡邊界兩筆的 op 數，並落盤。

為什麼需要這支：spec 的一條 SHALL 宣稱該路線在第 9 筆消耗 216,759,740 個
op（超標 21.68 倍），這是「死因是 op 上限而非 deadline」這個結論的規範層
依據。但 2026-08-15 的根因分析指出，那個數字**只活在散文裡**——
`measure/routes015.json` 的對應欄位是 `null`，因為主 harness 的 op 量測
對這條路線會先撞上自己的硬逾時。

於是「修正一個沒有出處的數字」變成了「換上另一個沒有出處的數字」。同一
個錯誤在修它的那一次動作裡又犯了一遍。這支腳本的存在就是要讓那個數字有
出處：它只做一件事——把邊界兩筆量出來寫進 JSON。

耗時：n=249 一筆約 20 秒（帶 tracer 逐事件計數）。n=72 不到 1 秒。
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CHANGE, "verify"))

from judge_ops import OP_LIMIT, count_ops_source_fresh  # noqa: E402

ROUTE = os.path.join(CHANGE, "curation", "routes", "r015_cellscan.py")

#: 死亡邊界：第 8 筆是最後一筆存活的，第 9 筆是第一筆死亡的。
#: entry 編號對應 curation/out/frontmatter015.yaml 的 testcase_plan 順序。
BOUNDARY = [
    {"entry": 8, "n": 72, "expect": "survives"},
    {"entry": 9, "n": 249, "expect": "dies"},
]


def main():
    rows = []
    for case in BOUNDARY:
        t0 = time.perf_counter()
        ops, _out, rc = count_ops_source_fresh(ROUTE, "%d\n" % case["n"], timeout=1800)
        elapsed = time.perf_counter() - t0
        if ops is None:
            print("! entry %d (n=%d) 量測逾時或失敗 rc=%s" % (case["entry"], case["n"], rc))
            return 1
        over = ops > OP_LIMIT
        rows.append({
            "entry": case["entry"],
            "n": case["n"],
            "ops": ops,
            "over_op_limit": over,
            "times_over_limit": round(ops / OP_LIMIT, 2),
            "measurement_seconds": round(elapsed, 1),
            "expect": case["expect"],
            "matches_expectation": over == (case["expect"] == "dies"),
        })
        print("entry %2d  n=%4d  ops=%13s  %s（%.2f 倍上限）  量測耗時 %.1f s" % (
            case["entry"], case["n"], format(ops, ","),
            "超標" if over else "未超標", ops / OP_LIMIT, elapsed))

    problems = [r for r in rows if not r["matches_expectation"]]
    report = {
        "purpose": "r015_cellscan.py 在死亡邊界兩筆的 op 數（冷行程），作為 E8 的規範層依據",
        "route": os.path.relpath(ROUTE, CHANGE),
        "op_limit": OP_LIMIT,
        "ops_source": "verify/judge_ops.py::count_ops_source_fresh",
        "why_not_in_routes015_json": (
            "主 harness 對這條路線的 op 量測會先撞上自己的硬逾時，"
            "因此 routes015.json 的 per_entry_ops 在第 9 筆之後為 null。"
            "本檔補上邊界兩筆，讓 spec 引用的數字有出處。"
        ),
        "rows": rows,
        "problems": [
            "entry %d 的實測與預期不符" % r["entry"] for r in problems
        ],
    }
    out = os.path.join(HERE, "cellscan-ops.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print("\n已寫出 %s" % os.path.relpath(out, CHANGE))
    if problems:
        for p in report["problems"]:
            print("  ✗ %s" % p)
        return 1
    print("邊界兩筆皆符合預期：第 8 筆存活、第 9 筆超標。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
