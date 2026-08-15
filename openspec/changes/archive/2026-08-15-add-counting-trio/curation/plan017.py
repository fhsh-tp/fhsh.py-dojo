"""apcs017 園遊會代幣兌換 — 20 筆測資計畫＋斷言牆（G 表事實的機械正本）。

執行：python3 plan017.py            驗證＋寫出 out/plan017.yaml 與 ../measure/report017.json
      python3 plan017.py --check    只驗證，不寫檔
      python3 plan017.py --scan     印出挑 n 用的機械化普查（誤解路線各自的反例分布）

這題沒有成本鑑別力可言：正解是 O(log n)，任何合理寫法都是微秒等級。
**全部的鑑別力都在「挑哪 20 個 n」**——每一條誤解路線都要有夠多的 n 打它。
因此斷言牆的重點不是 op 上限，而是：
  * 每條 WRONG_ANSWER 路線在 20 筆裡的得分必須嚴格低於契約上限（機械檢查，不手挑）
  * 邊界 n（1、答案 0 的最大 n、1e9）逐一在場
  * 大 n（>= 1e8）筆數足夠，避免只有玩具值域
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantics017 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "out")
# 落點規則（F-9）：report json 一律落在 measure/，斷言牆與語意正本留在 curation/。
MEASURE_DIR = os.path.abspath(os.path.join(HERE, os.pardir, "measure"))

MAX_N = S.MAX_N                 # 1e9，題面上界
BIG_N = 100_000_000             # 「大 n」門檻
EXAMPLE_N = 9                   # 第 1 筆 = 題面範例（9 位同學 -> 362880 種順序 -> 換 3 級）
INPUT_BUDGET = 4096             # 預設預算（本題每筆最多 11 bytes，天差地遠）

MIN_FORGOT_HALF_KILLS = 6       # 「忘記除以 2」必須被打錯的最少筆數
MIN_DECIMAL_KILLS = 6           # 「十進位每 5 一數」必須被打錯的最少筆數
MIN_ONLY_HALF_KILLS = 3         # 「只取 2 的份額折半、不取 min」必須被打錯的最少筆數
MIN_BIG_ENTRIES = 5             # n >= 1e8 的最少筆數

DECIMAL_CAP = 2                 # 「十進位每 5 一數」的得分上限（僅答案同為 0 的筆數僥倖對上）

# ── 每個 n 的「類別」——由 v2//2 與 v3 的大小關係機械決定，不是手貼標籤 ──
#   A = v3 > v2//2   -> 答案取 v2//2；「只取 3 的份額」與「忘記除以 2」在此答錯
#   B = v2//2 > v3   -> 答案取 v3    ；「只取 2 的份額折半」在此答錯
#   = = v2//2 == v3  -> 三條路線同時矇對，無鑑別力
#
# 這三類是互斥且窮盡的，因此對任何 20 筆組合恆有：
#     score(只取 3) + score(只取 2 折半) = #A + #B + 2 x #(=) = 20 + #(=)
# 也就是說，只要有 t 筆是「=」，兩條路線的較高分**不可能**低於 10 + ceil(t/2)。
# 契約強制入列的 n=1、n=11、n=10^9 三筆全部是「=」（見 forced_tie_entries()），
# 故本題可達的最佳上界是 12/20，不是 10/20——這是題目結構的下界，不是挑法不夠好。
MANDATORY = None                # 由 mandatory_entries() 產生，見下

# 挑 n 的錨點與想要的類別：由錨點往上找第一個符合類別且未用過的 n
# （超過上界才改往下找）。整份清單因此完全由程式決定，沒有手挑的餘地。
ANCHORS = [15, 27, 32, 111, 243, 1_000, 4_096, 20_250, 65_536, 987_654,
           100_000_000, 123_456_789, 777_777_777, 999_999_999]
ANCHOR_WANT = ["A", "B"] * 7    # 7 筆 A + 7 筆 B，讓兩條路線的分差壓到最小


def entry_class(n):
    """A / B / = 的機械判定。"""
    half_v2 = S.legendre(n, 2) // 2
    v3 = S.legendre(n, 3)
    if v3 > half_v2:
        return "A"
    if half_v2 > v3:
        return "B"
    return "="


def zero_answer_boundary(limit=1000):
    """機械求出「答案為 0 的最大 n」，不憑記憶寫死。"""
    return max(n for n in range(1, limit) if S.exchanges_formula(n) == 0)


def mandatory_entries():
    """契約強制入列的 n（含它們的理由），順序固定。"""
    return [
        (EXAMPLE_N, "第 1 筆＝題面範例"),
        (1, "下界 n=1"),
        (zero_answer_boundary(), "答案 0 的最大 n"),
        (8, "前 4 筆內必須有一筆 B 類（最小的 B 類 n）"),
        (11, "指定必含 n=11"),
        (MAX_N, "上界 n=10^9"),
    ]


def forced_tie_entries():
    """強制入列的 n 之中，類別為「=」（三條路線同時矇對）的那些。"""
    return [n for n, _ in mandatory_entries() if entry_class(n) == "="]


def wrong_score_lower_bound():
    """『只取 3』與『只取 2 折半』兩條路線中較高分者的可證下界。

    推導見上方註解：兩者得分和恆等於 20 + #(=)，而 #(=) >= 強制入列的「=」筆數。
    """
    t = len(forced_tie_entries())
    return 10 + -(-t // 2)      # 10 + ceil(t/2)


def select_entries():
    """機械挑出 20 筆 n：強制入列的 6 筆 + 14 個錨點各自往外找到的 n。"""
    chosen = [n for n, _ in mandatory_entries()]
    for anchor, want in zip(ANCHORS, ANCHOR_WANT):
        n = anchor
        while n <= MAX_N and (entry_class(n) != want or n in chosen):
            n += 1
        if n > MAX_N:                       # 上界撞牆就改往下找，仍然是決定性的
            n = anchor
            while n >= 1 and (entry_class(n) != want or n in chosen):
                n -= 1
        chosen.append(n)
    return [chosen[0]] + sorted(chosen[1:])  # 第 1 筆固定是題面範例，其餘由小到大


ENTRIES = select_entries()

# 各路線在 20 筆中的契約得分上限（<= 表示不得超過；R_reference 為嚴格相等）
CAPS = {
    "R_reference": ("==", 20),
    "W1_decimal_tail": ("<=", DECIMAL_CAP),
    "W2_forgot_half": ("<=", wrong_score_lower_bound()),
    "W3_only_v3": ("<=", wrong_score_lower_bound()),
    "W4_only_half_v2": ("<=", wrong_score_lower_bound()),
}


def scan(hi=2000):
    """普查：列出每條誤解路線的反例在小值域的分布，供挑 n 時查表用。"""
    a = [n for n in range(1, hi) if S.wrong_only_v3(n) > S.exchanges_formula(n)]
    b = [n for n in range(1, hi) if S.wrong_only_half_v2(n) > S.exchanges_formula(n)]
    d = [n for n in range(1, hi) if S.wrong_decimal_tail(n) != S.exchanges_formula(n)]
    print("掃描範圍 1..%d" % (hi - 1))
    print("  A 類（v3 > v2//2，打『忘記除以 2』／『只取 3』）共 %d 個，前 30：%s" % (len(a), a[:30]))
    print("  B 類（v2//2 > v3，打『只取 2 折半』）      共 %d 個，前 30：%s" % (len(b), b[:30]))
    print("  十進位規則答錯                            共 %d 個，答對的 n：%s"
          % (len(d), [n for n in range(1, hi) if n not in d][:20]))
    print("  A 與 B 互斥（交集大小）：%d" % len(set(a) & set(b)))
    print("  大 n 抽樣：")
    for n in (100_000_000, 123_456_789, 777_777_777, 999_999_999, 1_000_000_000):
        cls = "A" if S.wrong_only_v3(n) > S.exchanges_formula(n) else (
            "B" if S.wrong_only_half_v2(n) > S.exchanges_formula(n) else "-")
        print("    n=%-12d ans=%-10d v3=%-10d v2//2=%-10d v5=%-10d %s"
              % (n, S.exchanges_formula(n), S.wrong_only_v3(n),
                 S.wrong_only_half_v2(n), S.wrong_decimal_tail(n), cls))


def main(write=True):
    problems = []
    per_entry = []
    scores = {k: 0 for k in S.ROUTE_SEMANTICS}

    zero_max = zero_answer_boundary()

    # ── G1：公式版 vs math.factorial 暴力參照，n = 1..299 零誤差 ──
    mismatches = [n for n in range(1, 300)
                  if S.exchanges_formula(n) != S.exchanges_bruteforce(n)]
    if mismatches:
        problems.append("公式版與暴力參照在 n=%s 不一致" % mismatches[:10])

    if len(ENTRIES) != 20:
        problems.append("測資筆數 %d != 20" % len(ENTRIES))
    if len(set(ENTRIES)) != len(ENTRIES):
        problems.append("20 個 n 未兩兩相異")
    if ENTRIES[0] != EXAMPLE_N:
        problems.append("第 1 筆 %d 不是題面範例 %d" % (ENTRIES[0], EXAMPLE_N))

    for i, n in enumerate(ENTRIES, 1):
        if not (1 <= n <= MAX_N):
            problems.append("entry %d: n=%d 超出 1..%d" % (i, n, MAX_N))
        text = S.render_input(n)
        exp = S.render_expected(n)
        row = {
            "entry": i,
            "n": n,
            "expected": S.exchanges_formula(n),
            "v2": S.legendre(n, 2),
            "v3": S.legendre(n, 3),
            "bytes": len(text.encode()),
            "class": entry_class(n),
        }
        if n <= S.BRUTE_MAX_N:
            row["brute"] = S.exchanges_bruteforce(n)
            if row["brute"] != row["expected"]:
                problems.append("entry %d: n=%d 公式 %d != 暴力 %d"
                                % (i, n, row["expected"], row["brute"]))
        for name, fn in S.ROUTE_SEMANTICS.items():
            ok = fn(n) == S.exchanges_formula(n)
            row[name + "_ok"] = ok
            if ok:
                scores[name] += 1
        if row["bytes"] > INPUT_BUDGET:
            problems.append("entry %d: %d bytes 超出 input_budget %d" % (i, row["bytes"], INPUT_BUDGET))
        per_entry.append(row)

    # ── 機械化的鑑別力斷言（全部由計數決定，不靠手挑） ──
    forgot_kills = sum(1 for r in per_entry if not r["W2_forgot_half_ok"])
    only_v3_kills = sum(1 for r in per_entry if not r["W3_only_v3_ok"])
    decimal_kills = sum(1 for r in per_entry if not r["W1_decimal_tail_ok"])
    only_half_kills = sum(1 for r in per_entry if not r["W4_only_half_v2_ok"])
    big_entries = sum(1 for r in per_entry if r["n"] >= BIG_N)

    if forgot_kills < MIN_FORGOT_HALF_KILLS:
        problems.append("『忘記除以 2』只被 %d 筆打到，契約要求 >= %d"
                        % (forgot_kills, MIN_FORGOT_HALF_KILLS))
    if only_v3_kills < MIN_FORGOT_HALF_KILLS:
        problems.append("『只取 3 的份額』只被 %d 筆打到，契約要求 >= %d"
                        % (only_v3_kills, MIN_FORGOT_HALF_KILLS))
    if decimal_kills < MIN_DECIMAL_KILLS:
        problems.append("『十進位每 5 一數』只被 %d 筆打到，契約要求 >= %d"
                        % (decimal_kills, MIN_DECIMAL_KILLS))
    if only_half_kills < MIN_ONLY_HALF_KILLS:
        problems.append("『只取 2 折半不取 min』只被 %d 筆打到，契約要求 >= %d"
                        % (only_half_kills, MIN_ONLY_HALF_KILLS))
    if big_entries < MIN_BIG_ENTRIES:
        problems.append("n >= %d 的筆數只有 %d，契約要求 >= %d"
                        % (BIG_N, big_entries, MIN_BIG_ENTRIES))

    # ── 必含邊界 ──
    for must, why in mandatory_entries():
        if must not in ENTRIES:
            problems.append("缺邊界：%s（n=%d）" % (why, must))
    if S.exchanges_formula(zero_max) != 0 or S.exchanges_formula(zero_max + 1) == 0:
        problems.append("zero_max=%d 不是答案 0 的最大 n" % zero_max)

    # ── 第 1 筆（題面範例）必須當場打掉三條零洞察路線 ──
    first = per_entry[0]
    for name in ("W1_decimal_tail", "W2_forgot_half", "W3_only_v3"):
        if first[name + "_ok"]:
            problems.append("entry 1（題面範例 n=%d）無法鑑別 %s" % (EXAMPLE_N, name))
    # W4 與 W2/W3 的反例在數學上互斥（一個 n 不可能同時 v3>v2//2 與 v2//2>v3），
    # 所以 W4 不能要求由第 1 筆鑑別，只要求「前 4 筆內有人打到」。
    if all(r["W4_only_half_v2_ok"] for r in per_entry[:4]):
        problems.append("前 4 筆都打不到『只取 2 折半』，暖水區太舒適")

    # ── 契約得分 ──
    for name, (op, cap) in CAPS.items():
        got = scores[name]
        if (op == "==" and got != cap) or (op == "<=" and got > cap):
            problems.append("route %s: 得分 %d，契約要求 %s %d" % (name, got, op, cap))

    # ── 「亂猜路線」的可證下界（見檔頭註解的互補恆等式） ──
    ties = sum(1 for r in per_entry if r["class"] == "=")
    pair_sum = scores["W3_only_v3"] + scores["W4_only_half_v2"]
    if pair_sum != len(ENTRIES) + ties:
        problems.append("互補恆等式破了：score(只取3)+score(只取2折半)=%d，應為 %d+%d"
                        % (pair_sum, len(ENTRIES), ties))
    forced_ties = forced_tie_entries()
    if ties != len(forced_ties):
        problems.append("「=」筆數 %d != 強制入列的 %d 筆 %s，多出來的無鑑別力筆數只會墊高亂猜分數"
                        % (ties, len(forced_ties), forced_ties))
    bound = wrong_score_lower_bound()
    worst = max(scores["W2_forgot_half"], scores["W3_only_v3"], scores["W4_only_half_v2"])
    if worst != bound:
        problems.append("三條零洞察路線的最高分 %d != 可證最佳值 %d（挑法未達最佳，或恆等式假設變了）"
                        % (worst, bound))

    # W2 與 W3 在本題輸出恆等（v2 >= v3 對所有 n 成立 -> min(v2,v3) == v3）；
    # 機械驗證這件事，避免誤以為它們是兩條獨立路線。
    identical = all(S.wrong_forgot_half(n) == S.wrong_only_v3(n) for n in range(1, 5000))
    if not identical:
        problems.append("min(v2,v3) 與 v3 在 1..4999 出現分歧，CAPS 的假設要重寫")

    report = {
        "max_n": MAX_N,
        "example_n": EXAMPLE_N,
        "zero_answer_max_n": zero_max,
        "entries": ENTRIES,
        "expected": [r["expected"] for r in per_entry],
        "class_census": {c: sum(1 for r in per_entry if r["class"] == c) for c in "AB="},
        "guess_route_bound": {
            "forced_tie_entries": forced_ties,
            "tie_entries_in_plan": ties,
            "identity_pair_sum": pair_sum,
            "provable_best_max_score": bound,
            "achieved_max_score": worst,
            "goal_max_score_requested": 10,
            "goal_reachable": bound <= 10,
            # 反事實：就算把「指定必含 n=11」這條契約整條拿掉，n=1 與 n=10^9 兩筆
            # 仍然強制入列且同為「=」，下界只會降到 11，10/20 依舊不可達。
            "bound_without_n11": 10 + -(-len([n for n in forced_ties if n != 11]) // 2),
            "why": "score(只取3)+score(只取2折半) 恆等於 20+#(=)；契約強制入列的 "
                   "n=%s 全是「=」，故最高分不可能低於 10+ceil(%d/2)=%d。"
                   % (forced_ties, len(forced_ties), bound),
        },
        "kills": {
            "W1_decimal_tail": decimal_kills,
            "W2_forgot_half": forgot_kills,
            "W3_only_v3": only_v3_kills,
            "W4_only_half_v2": only_half_kills,
        },
        "big_entries": big_entries,
        "max_entry_bytes": max(r["bytes"] for r in per_entry),
        "input_budget": INPUT_BUDGET,
        "brute_crosscheck_range": "n=1..299 全數相符",
        "w2_w3_outputs_identical": identical,
        "scores": scores,
        "caps": {k: "%s %d" % v for k, v in CAPS.items()},
        "per_entry": per_entry,
        "problems": problems,
    }

    if write and not problems:
        os.makedirs(OUT_DIR, exist_ok=True)
        os.makedirs(MEASURE_DIR, exist_ok=True)
        # 逐筆行內註解一律不寫：舊版每一筆都標了「期望 N 類別 A/B」，同時洩漏
        # 答案與誤解路線的鑑別點，而這個檔的內容是要貼進公開題面的。逐筆的
        # 期望值與類別留在 ../measure/report017.json 的 per_entry（策展證物）。
        lines = [
            "# apcs017 園遊會代幣兌換 — testcase_plan（由 curation/plan017.py 產出，勿手改）",
            "# 每筆輸入為單一整數 n；期望輸出由 generator 對這份輸入即時計算。",
            "# 第 1 筆 = 題面範例 n=%d。" % EXAMPLE_N,
            "testcase_plan:",
        ]
        for r in per_entry:
            lines.append("  - literal: |")
            lines.append("      %d" % r["n"])
        with open(os.path.join(OUT_DIR, "plan017.yaml"), "w") as fh:
            fh.write("\n".join(lines) + "\n")
        with open(os.path.join(MEASURE_DIR, "report017.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: report[k] for k in
                      ("zero_answer_max_n", "entries", "expected", "class_census",
                       "kills", "big_entries", "max_entry_bytes",
                       "w2_w3_outputs_identical", "scores", "guess_route_bound")},
                     ensure_ascii=False, indent=1))
    if problems:
        print("\n斷言牆失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n斷言牆全數通過。")
    return 0


if __name__ == "__main__":
    if "--scan" in sys.argv:
        scan()
        raise SystemExit(0)
    raise SystemExit(main(write="--check" not in sys.argv))
