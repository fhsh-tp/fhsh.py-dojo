#!/usr/bin/env python3
"""比對轉換前後的盤點結果，產出差異表。

用法::

    python3 openspec/changes/latex-challenge-notation/measure/compare_survey.py
    python3 openspec/changes/latex-challenge-notation/measure/compare_survey.py --self-test

讀 ``notation-before.json`` 與 ``notation-after.json``，輸出 ``notation-delta.json``
與一張人可讀的表。

期望值寫死在 ``EXPECTED`` 裡，對不上就 exit 1。寫死是刻意的：這幾個數字是本 change
的驗收條件，不該跟著實際結果浮動——「跑出多少就是多少」的比對等於沒有比對。
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

# 這幾個數字是實測值，不是提案初稿裡的估計值。初稿寫 53 待轉 / 15 無記號，是在黑名單
# 還沒收錄裸的 `<` `>`、`!=`、`÷` 之前算出來的——quadrant-classifier 整頁 7 條不等式
# 因此被歸成「無記號」，整頁沒有人看過。黑名單補上之後，基準線用同一份規則重測，
# 待轉從 53 變 55、無記號從 15 變 13。
#
# clean 從 13 掉到 5，是因為 8 頁原本沒有黑名單記號、但內文有裸的單字母變數
# （hello-world 的 S、leap-year 的 Y、odd-even 的 n……），依分類表也該包成 LaTeX。
# 它們不在「待轉」清單裡，所以不計入 converted_count（那個數字只算「本來違規、
# 現在乾淨」的 55 頁）。
EXPECTED = {
    "before": {"total": 71, "converted": 3, "pending": 55, "clean": 13},
    "after": {"total": 71, "converted": 66, "pending": 0, "clean": 5},
}


def compare(before: dict, after: dict) -> dict:
    problems: list[str] = []

    for phase, snapshot in (("before", before), ("after", after)):
        for k, want in EXPECTED[phase].items():
            got = snapshot.get(k)
            if got != want:
                problems.append("%s 的 %s 是 %s，期望 %s" % (phase, k, got, want))

    b_files, a_files = before.get("per_file", {}), after.get("per_file", {})
    if set(b_files) != set(a_files):
        only_b = sorted(set(b_files) - set(a_files))
        only_a = sorted(set(a_files) - set(b_files))
        problems.append("題目頁集合改變了：消失 %s，新增 %s" % (only_b, only_a))

    # 逐檔：待轉的頁面必須從有違規變成零違規，且 LaTeX 片段數必須增加
    converted_files = []
    for name in sorted(set(b_files) & set(a_files)):
        b, a = b_files[name], a_files[name]
        was_pending = b["symbols"] > 0 or b["bare_dollar"] > 0
        if not was_pending:
            if a["symbols"] or a["bare_dollar"]:
                problems.append("%s 本來乾淨，轉換後反而有違規" % name)
            continue
        if a["symbols"] or a["bare_dollar"]:
            problems.append("%s 轉換後仍有違規（symbols=%d、裸錢字號=%d）"
                            % (name, a["symbols"], a["bare_dollar"]))
        elif a["latex"] <= b["latex"]:
            problems.append("%s 的違規消失了，但 LaTeX 片段數沒增加（%d → %d）"
                            "——記號可能是被刪掉而不是被轉換"
                            % (name, b["latex"], a["latex"]))
        else:
            converted_files.append(
                {"file": name, "symbols_before": b["symbols"], "latex_before": b["latex"],
                 "latex_after": a["latex"]}
            )

    return {
        "expected": EXPECTED,
        "actual": {
            "before": {k: before.get(k) for k in EXPECTED["before"]},
            "after": {k: after.get(k) for k in EXPECTED["after"]},
        },
        "converted_count": len(converted_files),
        "converted": converted_files,
        "problems": problems,
        "verdict": "PASS" if not problems else "FAIL",
    }


def _self_test() -> None:
    """負向控制：每一條斷言都要證明會對壞資料觸發。"""
    def snap(phase: str, per_file: dict) -> dict:
        return {**EXPECTED[phase], "per_file": per_file}

    good_b = snap("before", {"a.md": {"symbols": 2, "bare_dollar": 0, "latex": 0}})
    good_a = snap("after", {"a.md": {"symbols": 0, "bare_dollar": 0, "latex": 3}})
    assert compare(good_b, good_a)["verdict"] == "PASS", "乾淨的一組不該報問題"

    cases = [
        ("頂層數字不符", snap("before", good_b["per_file"]) | {"pending": 52}, good_a, "pending"),
        ("轉換後仍有違規", good_b,
         snap("after", {"a.md": {"symbols": 1, "bare_dollar": 0, "latex": 3}}), "仍有違規"),
        ("記號被刪而非被轉", good_b,
         snap("after", {"a.md": {"symbols": 0, "bare_dollar": 0, "latex": 0}}), "沒增加"),
        ("題目頁集合改變", good_b,
         snap("after", {"b.md": {"symbols": 0, "bare_dollar": 0, "latex": 3}}), "集合改變"),
        ("本來乾淨卻變髒", snap("before", {"a.md": {"symbols": 0, "bare_dollar": 0, "latex": 1}}),
         snap("after", {"a.md": {"symbols": 3, "bare_dollar": 0, "latex": 1}}), "反而有違規"),
    ]
    for name, b, a, needle in cases:
        r = compare(b, a)
        if r["verdict"] != "FAIL":
            raise SystemExit("負向控制失敗 [%s]：斷言沒觸發" % name)
        if not any(needle in p for p in r["problems"]):
            raise SystemExit("負向控制失敗 [%s]：觸發了但訊息沒指出原因：%s" % (name, r["problems"]))

    print("self-test 通過（正例 1 + 負向控制 %d）" % len(cases))


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        _self_test()
        return 0
    before = json.loads((HERE / "notation-before.json").read_text(encoding="utf-8"))
    after = json.loads((HERE / "notation-after.json").read_text(encoding="utf-8"))
    result = compare(before, after)
    (HERE / "notation-delta.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    a, b = result["actual"]["after"], result["actual"]["before"]
    print("項目        轉換前  轉換後  期望")
    for k in ("total", "converted", "pending", "clean"):
        print("%-10s %6s %7s %6s" % (k, b[k], a[k], EXPECTED["after"][k]))
    print("\n實際轉換頁數：%d" % result["converted_count"])
    if result["problems"]:
        print("\n問題：")
        for p in result["problems"]:
            print("  -", p)
    print("\n判定：%s" % result["verdict"])
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
