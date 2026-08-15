"""量測**實際出貨**的 generator 與 reference_solution 的 op 數。

為什麼需要這支：2026-08-15 的交叉驗證指出，trace-matrix 的 E4／F3／G3
記載的是 `curation/routes/` 底下**路線檔**的 op 數——那些代表「學生可能
寫出的提交」。但真正隨題目出貨、且真的會被判題鏈執行的，是 frontmatter
裡的 `generator` 與 `reference_solution`，而六支出貨碼沒有一支的 op 數
等於路線表中的任何一筆（它們是重新拼寫的版本）。

沒有這支腳本的話，矩陣裡的成本數字就描述不到實際出貨的東西——正是本
專案反覆記錄的「文件數字對不回它宣稱描述的對象」型缺陷。

op 一律取冷行程值（見 judge_ops.count_ops_source_fresh 的說明）。
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CHANGE)))
sys.path.insert(0, HERE)

from judge_ops import OP_LIMIT, count_ops_source_fresh  # noqa: E402

CHALLENGES = [
    ("apcs015", "ap-layout-plan"),
    ("apcs016", "marquee-display-count"),
    ("apcs017", "fair-token-exchange"),
]


def read_block(text, key):
    """從 frontmatter 取出一個區塊純量的內容（去掉兩格縮排）。"""
    m = re.search(rf"^{key}: \|\n((?:(?:  .*)?\n)+?)(?=^\S)", text, re.M)
    if not m:
        raise SystemExit(f"找不到 {key}")
    lines = [ln[2:] if ln.startswith("  ") else ln for ln in m.group(1).split("\n")]
    return "\n".join(lines).rstrip() + "\n"


def read_literals(text):
    m = re.search(r"^testcase_plan:\n((?:  .*\n|\n)+?)(?=^\S)", text, re.M)
    if not m:
        raise SystemExit("找不到 testcase_plan")
    return [
        "\n".join(ln[6:] for ln in blk.rstrip("\n").split("\n")) + "\n"
        for blk in re.findall(r"  - literal: \|\n((?:      .*\n)+)", m.group(1))
    ]


def main():
    tmp = os.path.join(CHANGE, "measure", "_shipped_tmp")
    os.makedirs(tmp, exist_ok=True)
    report = {
        "purpose": "實際出貨的 generator / reference_solution 的 op 數（冷行程）",
        "op_limit": OP_LIMIT,
        "ops_source": "verify/judge_ops.py::count_ops_source_fresh",
        "note": "此表描述 frontmatter 內的出貨碼，與 curation/routes/ 的學生路線檔是不同對象",
        "challenges": [],
    }
    failed = False
    for cid, slug in CHALLENGES:
        page = os.path.join(ROOT, "docs", "challenge", f"{slug}.md")
        text = open(page, encoding="utf-8").read()
        lits = read_literals(text)
        entry = {"id": cid, "slug": slug, "entries": len(lits), "programs": {}}
        for key in ("generator", "reference_solution"):
            src = read_block(text, key)
            path = os.path.join(tmp, f"{cid}_{key}.py")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(src)
            per = []
            for lit in lits:
                ops, _out, rc = count_ops_source_fresh(path, lit, timeout=300)
                if ops is None or rc != 0:
                    print(f"  ! {cid} {key} 在某筆失敗 rc={rc}")
                    failed = True
                    per.append(None)
                else:
                    per.append(ops)
            clean = [x for x in per if x is not None]
            mx = max(clean) if clean else None
            entry["programs"][key] = {
                "max_ops": mx,
                "max_ops_pct_of_limit": round(100 * mx / OP_LIMIT, 4) if mx else None,
                "margin_x": round(OP_LIMIT / mx, 2) if mx else None,
                "worst_entry": per.index(mx) + 1 if mx else None,
                "per_entry_ops": per,
            }
            if mx and mx > OP_LIMIT:
                print(f"  ! {cid} {key} 超過 op 上限：{mx:,}")
                failed = True
        report["challenges"].append(entry)
        g = entry["programs"]["generator"]
        r = entry["programs"]["reference_solution"]
        print(
            f"{cid} {slug:24} generator {g['max_ops']:>10,} ({g['max_ops_pct_of_limit']:>7.4f}%)"
            f"   reference_solution {r['max_ops']:>10,} ({r['max_ops_pct_of_limit']:>7.4f}%)"
        )

    out = os.path.join(CHANGE, "measure", "shipped-code-ops.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print(f"\n已寫出 {os.path.relpath(out, ROOT)}")
    if failed:
        raise SystemExit(1)
    print("全部出貨碼皆在 op 上限內。")


if __name__ == "__main__":
    main()
