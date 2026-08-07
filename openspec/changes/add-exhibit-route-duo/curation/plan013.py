"""apcs013 展場動線重建 — 測資計畫＋斷言牆（A6/A8/A9/A10 的機械正本）。

執行：python3 plan013.py         （驗證＋寫出 literals/ 與 report013.json）
      python3 plan013.py --check （只驗證，不寫檔）

任一斷言不成立即以非零碼結束，出貨流程必須中止。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantics013 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LIT_DIR = os.path.join(HERE, "literals")

MAX_DEPTH = 300          # A5
MAX_BYTES = 50_000       # A8

# entry 定義：每筆＝一串 (mode, n, shape, seed)
ENTRIES = [
    # 第 1–10 筆：模式 1（甲＋乙→丙）
    [(1, 7, "leftheavy", 1301)],
    [(1, 1, "single", 1302), (1, 2, "lchain", 1303), (1, 2, "rchain", 1304), (1, 3, "zigzag", 1305),
     (1, 24, "random", 1398)],
    [(1, 9, "random", 1306), (1, 12, "balanced", 1307), (1, 22, "leftheavy", 1308)],
    [(1, 25, "random", 1309), (1, 30, "caterpillar", 1310), (1, 18, "rchain", 1311)],
    [(1, 60, "random", 1312), (1, 45, "zigzag", 1313), (1, 50, "leftheavy", 1314)],
    [(1, 120, "spine", 1315), (1, 90, "random", 1316)],
    [(1, 200, "caterpillar", 1317), (1, 150, "leftheavy", 1318), (1, 90, "random", 1397)],
    [(1, 300, "spine", 1319), (1, 260, "random", 1320)],
    [(1, 600, "spine", 1321), (1, 500, "random", 1322)],
    [(1, 1200, "spine", 1323), (1, 900, "random", 1324)],
    # 第 11 筆：模式 2 單組（頁面第二個範例）
    [(2, 7, "leftheavy", 1331)],
    # 第 12–20 筆：同筆混合兩種模式
    [(2, 4, "lchain", 1332), (1, 5, "leftheavy", 1333), (2, 6, "balanced", 1334), (2, 26, "random", 1396)],
    [(2, 20, "random", 1335), (1, 24, "caterpillar", 1336), (2, 16, "leftheavy", 1337)],
    [(2, 55, "leftheavy", 1338), (1, 40, "zigzag", 1339), (2, 70, "random", 1340)],
    [(2, 130, "spine", 1341), (1, 110, "leftheavy", 1342)],
    [(2, 240, "random", 1343), (1, 200, "caterpillar", 1344)],
    [(2, 400, "spine", 1345), (1, 350, "random", 1346)],
    [(2, 700, "random", 1347), (1, 550, "spine", 1348)],
    [(2, 1000, "spine", 1349), (1, 300, "zigzag", 1350), (2, 480, "random", 1351)],
    [(2, 1400, "random", 1352), (1, 1100, "spine", 1353)],
]

CAPS = {          # 路線 → (比較子, 上界)  ；'eq' 表示必須精準等於
    "ref": ("eq", 20),
    "R1_mirror": ("eq", 20),
    "W1_modeblind": ("eq", 10),
    "W5_markeronce": ("eq", 11),
    "W2_postfirst": ("le", 10),
    "W4_swaporder": ("le", 10),
    "W3_sorted": ("eq", 0),
    "W6_firstonly": ("eq", 2),   # entry 1 與 entry 11 為單組範例筆
    "W9_revfirst": ("eq", 0),
    "W10_echosecond": ("eq", 0),
    "W11_shapelib": ("eq", 2),    # 只剩 entry 1、11 兩筆單組範例筆（不承擔鑑別責任）
    "Z1_echofirst": ("eq", 0),
    "Z2_revsecond": ("eq", 0),
    "Z3_sortdesc": ("eq", 0),
}

EXAMPLE_ENTRIES = (1, 11)     # 題面兩個範例筆：單組、小 n，不計入鑑別力


def build_all():
    entries = []
    for spec in ENTRIES:
        cases = [S.make_case(m, n, sh, sd) for (m, n, sh, sd) in spec]
        entries.append(
            {
                "cases": cases,
                "input": S.render_input(cases),
                "expected": S.render_expected(cases),
            }
        )
    return entries


def main(write=True):
    entries = build_all()
    problems = []
    scores = {k: 0 for k in S.ROUTES}
    per_entry = []

    for i, e in enumerate(entries, 1):
        row = {
            "entry": i,
            "tests": [
                {"mode": c["mode"], "n": c["n"], "shape": c["shape"], "depth": c["depth"]}
                for c in e["cases"]
            ],
            "bytes": len(e["input"].encode()),
            "out_bytes": len(e["expected"].encode()),
        }
        for name, fn in S.ROUTES.items():
            try:
                got = fn(e["input"])
            except Exception as exc:  # 錯誤路線可能整個爆掉，視為該筆不過
                got = "<%s>" % type(exc).__name__
            ok = got == e["expected"]
            row[name + "_ok"] = ok
            if ok:
                scores[name] += 1
        per_entry.append(row)

        # ── 結構斷言 ────────────────────────────────────────────────
        for c in e["cases"]:
            if c["depth"] > MAX_DEPTH:
                problems.append("entry %d: depth %d > %d (%s n=%d)" % (i, c["depth"], MAX_DEPTH, c["shape"], c["n"]))
        if row["bytes"] > MAX_BYTES:
            problems.append("entry %d: %d bytes > %d" % (i, row["bytes"], MAX_BYTES))
        modes = {c["mode"] for c in e["cases"]}
        sigs = {c["sig"] for c in e["cases"]}
        if len(e["cases"]) >= 2 and len(sigs) < 2:
            problems.append("entry %d: 結構簽章只有一種（違反 A10；形狀名稱不同不代表結構不同）" % i)
        if not any(not c["chain"] for c in e["cases"]):
            problems.append("entry %d: 全部為單一路徑動線，退化公式路線可整筆通過" % i)
        if not any(c["mirror_asym"] for c in e["cases"]):
            problems.append("entry %d: 沒有任何一組左右不對稱（A9）" % i)
        if i not in EXAMPLE_ENTRIES and max(c["n"] for c in e["cases"]) < 20:
            problems.append("entry %d: 最大 n=%d < 20，窮舉形狀的路線可整筆通過"
                            % (i, max(c["n"] for c in e["cases"])))
        if 2 in modes and not any(c["mode"] == 2 and not c["chain"] and c["n"] >= 3 for c in e["cases"]):
            problems.append("entry %d: 模式 2 的組別全為單一路徑，模式盲路線對其免疫" % i)
        if i <= 10 and modes != {1}:
            problems.append("entry %d: 第 1–10 筆必須全為模式 1，實得 %s" % (i, modes))
        if i == 11 and modes != {2}:
            problems.append("entry 11: 必須為純模式 2，實得 %s" % modes)
        if 12 <= i <= 20 and modes != {1, 2}:
            problems.append("entry %d: 第 12–20 筆必須同筆混合兩模式，實得 %s" % (i, modes))
        if i >= 11 and not (row["W1_modeblind_ok"] is False):
            problems.append("entry %d: 模式盲路線竟然通過" % i)

    # ── 得分斷言 ────────────────────────────────────────────────────
    for name, (op, cap) in CAPS.items():
        s = scores[name]
        if op == "eq" and s != cap:
            problems.append("route %s: 得分 %d，契約要求 == %d" % (name, s, cap))
        if op == "le" and s > cap:
            problems.append("route %s: 得分 %d，契約要求 <= %d" % (name, s, cap))

    # 邊界覆蓋
    all_n = [c["n"] for e in entries for c in e["cases"]]
    if 1 not in all_n:
        problems.append("缺 n=1 邊界測試")
    if max(all_n) < 1000:
        problems.append("缺大型測試（max n = %d）" % max(all_n))

    report = {
        "max_depth_allowed": MAX_DEPTH,
        "example_entries": list(EXAMPLE_ENTRIES),
        "max_bytes_allowed": MAX_BYTES,
        "max_entry_bytes": max(r["bytes"] for r in per_entry),
        "max_n": max(all_n),
        "max_depth_shipped": max(c["depth"] for e in entries for c in e["cases"]),
        "scores": scores,
        "caps": {k: list(v) for k, v in CAPS.items()},
        "per_entry": per_entry,
        "problems": problems,
    }

    if write and not problems:
        os.makedirs(LIT_DIR, exist_ok=True)
        for i, e in enumerate(entries, 1):
            with open(os.path.join(LIT_DIR, "c013_%02d.txt" % i), "w") as fh:
                fh.write(e["input"])
            with open(os.path.join(LIT_DIR, "c013_%02d.exp" % i), "w") as fh:
                fh.write(e["expected"])
        with open(os.path.join(HERE, "report013.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: report[k] for k in
                      ("max_entry_bytes", "max_n", "max_depth_shipped", "scores")},
                     ensure_ascii=False, indent=1))
    if problems:
        print("\n斷言牆失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n斷言牆全數通過。")
    return 0


if __name__ == "__main__":
    sys.exit(main(write="--check" not in sys.argv))
