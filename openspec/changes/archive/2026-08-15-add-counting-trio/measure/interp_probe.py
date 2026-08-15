"""量測 apcs015 的插值路線，並證明題面改動堵不住它。

2026-08-15 的第三輪稽核指出：第 k 列答案在整個定義域上是 k 的四次多項式，
因此五個資料點就唯一決定它。這支腳本量測兩種取得資料點的方式：

1. `page_table` —— 只用題面公開的答案表（維護者裁決後已縮為 k = 1..3，
   但題面的**範例輸出**本身就印出 k = 1..8 共八個值，且該範例受契約約束
   必須與第一筆 literal 逐位元組相同，無法移除）。
2. `self_generated` —— 完全不看題面任何數字，自己對 k = 1..5 暴力枚舉。

第二種若也通過，就證明**任何題面改動都無法關閉這條路線**，因為學生自己
造點只需要幾百次配對比較。這正是本檔存在的理由：把「堵不住」這個結論
變成可重跑的量測，而不是散文裡的斷言。
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CHANGE, "verify"))

from judge_ops import OP_LIMIT, count_ops_source_fresh  # noqa: E402

ROUTE = os.path.join(CHANGE, "curation", "routes", "r015_interp_selfgen.py")

#: 題面範例輸出印出的八個值，任取五個即可決定四次多項式。
#: 出處 docs/challenge/ap-layout-plan.md 的〈範例〉區塊。
PAGE_EXAMPLE_VALUES = [0, 6, 28, 96, 252, 550, 1056, 1848]

PAGE_TABLE_SOURCE = """import sys
from fractions import Fraction
PTS = [(1, 0), (2, 6), (3, 28), (4, 96), (5, 252)]
def lag(k):
    s = Fraction(0)
    for i, (xi, yi) in enumerate(PTS):
        t = Fraction(yi)
        for j, (xj, _) in enumerate(PTS):
            if i != j:
                t *= Fraction(k - xj, xi - xj)
        s += t
    return int(s)
n = int(sys.stdin.readline())
sys.stdout.write("\\n".join(str(lag(k)) for k in range(1, n + 1)))
"""


def literals():
    txt = open(os.path.join(CHANGE, "curation", "out", "frontmatter015.yaml"),
               encoding="utf-8").read()
    return ["\n".join(l[6:] for l in b.rstrip("\n").split("\n")) + "\n"
            for b in re.findall(r"- literal: \|\n((?:      .*\n)+)", txt)]


def expected(n):
    ns = {}
    src = open(os.path.join(CHANGE, "curation", "semantics015.py"), encoding="utf-8").read()
    exec(src.split("if __name__")[0], ns)
    fn = ns.get("render_expected") or ns.get("expected_output")
    out = fn(n)
    return "\n".join(map(str, out)) if isinstance(out, list) else str(out)


def score(path, lits):
    ok = mx = 0
    for lit in lits:
        ops, out, rc = count_ops_source_fresh(path, lit, timeout=900)
        if ops is None:
            return None, None
        ok += out.strip() == expected(int(lit.strip())).strip()
        mx = max(mx, ops)
    return ok, mx


def main():
    lits = literals()
    tmp = os.path.join(HERE, "_interp_tmp.py")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(PAGE_TABLE_SOURCE)

    variants = []
    for name, path, note in (
        ("page_table", tmp, "只用題面答案表的五個值"),
        ("self_generated", ROUTE, "完全不看題面，自己暴力枚舉 k=1..5 造點"),
    ):
        ok, mx = score(path, lits)
        variants.append({
            "variant": name,
            "note": note,
            "score": ok,
            "of": len(lits),
            "max_ops": mx,
            "op_margin": round(OP_LIMIT / mx, 1) if mx else None,
            "passes": ok == len(lits),
        })
        print("%-16s %2d/%d  最大 op %10s  餘裕 %5.1f 倍  （%s）" % (
            name, ok, len(lits), format(mx, ","), OP_LIMIT / mx, note))
    os.remove(tmp)

    self_gen = [v for v in variants if v["variant"] == "self_generated"][0]
    report = {
        "purpose": "證明 apcs015 的插值路線可行，且題面改動無法關閉它",
        "op_limit": OP_LIMIT,
        "ops_source": "verify/judge_ops.py::count_ops_source_fresh",
        "page_example_values_published": len(PAGE_EXAMPLE_VALUES),
        "points_needed_for_quartic": 5,
        "page_change_can_close_route": not self_gen["passes"],
        "variants": variants,
        "problems": [],
    }
    if self_gen["passes"]:
        print("\n自產點變體通過 → 題面改動**無法**關閉這條路線（已如實記錄）。")
    else:
        report["problems"].append("自產點變體未通過，與稽核結論不符，需重新檢視")

    out = os.path.join(HERE, "interp-route.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print("已寫出 %s" % os.path.relpath(out, CHANGE))
    return 1 if report["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
