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
    [(1, 14, "random", 1306), (1, 12, "balanced", 1307), (1, 22, "leftheavy", 1308), (1, 31, "random", 1399)],
    [(1, 25, "random", 1309), (1, 30, "caterpillar", 1310), (1, 18, "rchain", 1311)],
    [(1, 60, "random", 1312), (1, 45, "zigzag", 1313), (1, 50, "leftheavy", 1314)],
    [(1, 120, "spine", 1315), (1, 90, "random", 1316)],
    [(1, 200, "caterpillar", 1317), (1, 150, "leftheavy", 1318), (1, 90, "random", 1397)],
    [(1, 300, "spine", 1319), (1, 260, "random", 1320)],
    [(1, 600, "spine", 1321), (1, 500, "random", 1322)],
    [(1, 1200, "spine", 1323), (1, 900, "random", 1324)],
    # 第 11 筆：模式 2 單組（頁面第二個範例）
    [(2, 7, "leftheavy", 1331)],
    # 第 12–20 筆：同筆五組、混合兩種模式、組別依大小遞減排列、9 種模式序列兩兩相異；
    # 形狀一律取 **rng 驅動**家族（randchain／randbush／random）：固定形狀家族會留下
    # 指紋，讓「兩種讀法都還原、看哪一種落在已知形狀」的辨識器不必讀標記就猜中模式；
    # randchain／randbush 又是深形狀，同時讓「取較淺者」的深度啟發式失手（R3）。
    # 每筆最後一組模式 2 固定用 random（非單一路徑），維持 A14 的守門機制
    [(2, 28, "randchain", 1700), (1, 26, "randbush", 1701), (1, 25, "randchain", 1702), (1, 24, "random", 1703), (2, 22, "random", 1704)],
    [(2, 48, "randchain", 1705), (1, 44, "randbush", 1706), (1, 40, "randchain", 1707), (2, 36, "random", 1708), (1, 30, "random", 1709)],
    [(2, 70, "randchain", 1710), (1, 60, "randbush", 1711), (2, 55, "random", 1712), (1, 50, "random", 1713), (1, 40, "random", 1714)],
    [(2, 130, "randchain", 1715), (2, 124, "random", 1716), (1, 110, "randchain", 1717), (1, 90, "random", 1718), (1, 75, "random", 1719)],
    [(2, 240, "randchain", 1720), (1, 200, "randbush", 1721), (2, 180, "randchain", 1722), (2, 160, "random", 1723), (1, 140, "random", 1724)],
    [(2, 290, "randchain", 1725), (2, 260, "randbush", 1726), (1, 240, "randchain", 1727), (2, 220, "random", 1728), (1, 200, "random", 1729)],
    [(2, 300, "randchain", 1730), (2, 280, "randbush", 1731), (2, 260, "random", 1732), (1, 240, "random", 1733), (1, 220, "random", 1734)],
    [(2, 300, "randchain", 1735), (1, 290, "randbush", 1736), (1, 280, "randchain", 1737), (2, 260, "random", 1738), (2, 240, "random", 1739)],
    [(2, 300, "randchain", 1740), (2, 290, "randbush", 1741), (1, 280, "randchain", 1742), (1, 270, "random", 1743), (2, 250, "random", 1744)],
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
    "W11_shapelib": ("eq", 2),
    "W12_dictbrute": ("eq", 2),   # 字典＋小 n 窮舉：同樣只剩兩筆範例筆
    "W13_depthguess": ("le", 12),
    "W14_shaperecog": ("le", 12), # 形狀辨識器＋深度後備（攻擊策展的形狀指紋） # 完全不讀模式標記、以「總深度較小」猜讀法    # 只剩 entry 1、11 兩筆單組範例筆（不承擔鑑別責任）
    "Z1_echofirst": ("eq", 0),
    "Z2_revsecond": ("eq", 0),
    "Z3_sortdesc": ("eq", 0),
}

POSITIONAL_RULE_CAP = 12   # 11 筆單一模式筆 + 混合筆中最多命中一筆
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

    # 「不逐組讀模式標記」的規則家族上界：一條規則以某組特徵（組數／首個模式／位置／
    # 組別大小名次）為鍵決定每組模式，最佳規則只能命中「同鍵之下出現最多次的那一種模式
    # 序列」，逐鍵取最大值即為上界。R2 指出只算「位置」一種鍵不夠——同族也可用大小名次。
    from collections import Counter, defaultdict

    def _seq(e):
        return tuple(c["mode"] for c in e["cases"])

    def _by_position(e):
        return (len(e["cases"]), _seq(e)[0])

    def _by_sizerank(e):
        order = sorted(range(len(e["cases"])), key=lambda k: -e["cases"][k]["n"])
        return (len(e["cases"]), _seq(e)[0], tuple(order))

    def _by_count_only(e):
        return (len(e["cases"]),)

    positional_best = 0
    for keyfn in (_by_position, _by_sizerank, _by_count_only):
        buckets = defaultdict(Counter)
        for e in entries:
            buckets[keyfn(e)][_seq(e)] += 1
        best = sum(cnt.most_common(1)[0][1] for cnt in buckets.values())
        positional_best = max(positional_best, best)
    if positional_best > POSITIONAL_RULE_CAP:
        problems.append("不逐組讀模式標記的規則家族上界 %d > %d"
                        % (positional_best, POSITIONAL_RULE_CAP))

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
        "positional_rule_best": positional_best,
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
