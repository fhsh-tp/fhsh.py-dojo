"""apcs016 跑馬燈顯示計數 — 測資計畫＋斷言牆（F 表事實的機械正本）。

執行：python3 plan016.py         （驗證＋寫出 out/plan016.yaml、out/literals016/、
                                  ../measure/report016.json）
      python3 plan016.py --check （只驗證，不寫檔）

out/plan016.yaml 只含 testcase_plan；可直接貼進 frontmatter 的片段（含 algorithm、
params、input_budget）由 curation/assemble.py 統一組裝三題，形狀一致。

設計裁決（維護者）：**這題刻意不建成本斷崖**。
鑑別點是「看穿自由度是 n − k 而不是 n」，不是「誰的迴圈比較快」。
因此 O(n) 逐次乘法與三參數 pow 都必須是 ACCEPTED，斷言牆的成本相關斷言
一律是「上限」（不可誤殺），沒有任何「下限」（不逼死慢寫法）。

20 筆 literal 的契約（全部由本檔機械檢查）：
  1. 第 1 筆 == 題面範例
  2. 至少 15 筆 k >= 1（否則「忽略 k」的錯誤路線會拿高分）
  3. 必須涵蓋 k = 0、k = n、n = 1、n = 1000000
  4. 至少 5 筆 n >= 500000
  5. 20 組 (n, k) 兩兩相異
  6. 沒有任何一筆 n == 2k（否則「算成 2^k」的錯誤路線會白拿分）
  7. 每筆 literal 的位元組數 <= input_budget 預設值 4096
  8. 路線得分符合 CAPS（正解 20/20、錯解不得滿分）
  9. 期望輸出的重複情形只允許「k = n」那一組（見下方 DUP 說明）

DUP（期望輸出兩兩相異做不到，也不該硬做）：
  答案 2^(n−k) mod p 只由自由格數 n − k 決定，所以「兩筆期望輸出相同」等價於
  「兩筆 n − k 相同」。契約第 3 條同時要求覆蓋 n = 1 與 n = 1000000 的 k = n
  邊界，而 k = n 的自由格數定義上就是 0、答案定義上就是 1 —— 這一組重複是
  邊界契約直接推出來的，拿掉它等於拿掉一個邊界。除此之外的重複都是無償的
  （entry 13 與舊 entry 16 曾經同為 n − k = 499999），一律不允許，由下方
  斷言把關。

int -> str 位數一律實測（len(str(2**free))），不用 log10 估算式：估算式
int(free * 0.30103) + 1 在 free = 1000000 時給 301031，實測是 301030，差 1。
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantics016 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
LIT_DIR = os.path.join(OUT, "literals016")
# 落點規則（F-9）：report json 一律落在 measure/，斷言牆與語意正本留在 curation/。
MEASURE = os.path.abspath(os.path.join(HERE, os.pardir, "measure"))

MAX_N = 1_000_000          # 題面同步：1 <= n <= 1000000
BUDGET = 4096              # input_budget 預設值（Usage.md「輸入規模預算」）
OP_CAP = 10_000_000        # 每筆測資 traced op 上限
OPS_PER_ITER = 4           # O(n) 迴圈的悲觀 op 模型（for 行 + body 行，再乘 2 倍餘裕）
BIG_N = 500_000            # 「大 n」門檻
MIN_BIG_N = 5              # 至少幾筆大 n
MIN_K_POS = 15             # 至少幾筆 k >= 1
NOMOD_SAFE_EXP = 29        # 2^29 < 1000000007 <= 2^30：指數 <= 29 時忘記取餘數也會對
INT_STR_LIMIT = 4300       # CPython 3.11+ 的 int -> str 位數上限（Pyodide 0.29 = CPython 3.13）

# ── 20 筆 literal ───────────────────────────────────────────────────────────
# 第 1 筆 (5, 2) 是題面範例：5 格燈壞了 2 格，答案 8。
#   小到學生能在紙上把 8 種畫面全部畫出來，卻已經同時打死四條零洞察路線
#   （2^5 = 32、2^2 = 4、n − k = 3 都不是 8）。
ENTRIES = [
    (5, 2),              # 1  題面範例
    (1, 1),              # 2  n = 1 邊界 ∧ k = n 邊界（答案 1）
    (1_000_000, 1_000_000),  # 3  n = 1000000 邊界 ∧ k = n 邊界（大 n 但答案 1）
    (10, 0),             # 4  k = 0 邊界（小）
    (1_000_000, 0),      # 5  n = 1000000 ∧ k = 0：O(n) 迴圈的最壞情形
    (3, 1),              # 6  小而好手算
    (40, 7),             # 7  指數 33，開始需要取餘數
    (60, 13),            # 8
    (100, 37),           # 9
    (1_000, 970),        # 10 指數剛好 30，跨過「忘記取餘數」的分界
    (12_345, 6_789),     # 11
    (99_991, 1_234),     # 12
    (500_000, 1),        # 13 大 n、幾乎沒壞
    (500_000, 499_999),  # 14 大 n、只剩一格會動 —— 本題鑑別點最銳利的一筆
    (777_777, 123_456),  # 15
    (999_999, 499_999),  # 16 自由格數 500000（原為 (999999, 500000)，與 entry 13 同為
                         #    499999、期望輸出撞號；換成 499999 後兩筆各自獨立）
    (654_321, 54_321),   # 17
    (999_983, 3),        # 18
    (250_000, 99_999),   # 19
    (65_537, 32_768),    # 20 n = 2k + 1，刻意閃開 n == 2k
]

CAPS = {
    "REF_pow3": ("eq", 20),
    "A1_loop": ("eq", 20),
    "A2_bigint": ("eq", 20),
    "W1_ignore_k": ("eq", 2),    # 只在 k = 0 的 2 筆上僥倖得分（k = 0 邊界本來就要覆蓋）
    "W2_use_k": ("eq", 0),
    "W3_plain_diff": ("eq", 0),
    "W4_nomod": ("eq", 6),       # 只在 n − k <= 29 的 6 筆上僥倖得分（邊界筆本來就小）
}


def decimal_digits(exp):
    """實測 ``2 ** exp`` 的十進位位數：真的轉成字串再數長度。

    刻意不用 int(exp * 0.30103) + 1 這類估算式——那條式子在 exp = 1000000
    時給 301031，實測是 301030。位數會進到 measure/report016.json 的
    nomod_max_digits，而 measure/routes016.json 的 max_out_len 是實測字串
    長度；兩份證物必須同源，否則就是差 1 的假矛盾。
    """
    old = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)  # 0 = 解除上限，只為了量長度
    try:
        return len(str(2 ** exp))
    finally:
        sys.set_int_max_str_digits(old)


def main(write=True):
    problems = []
    scores = {k: 0 for k in S.ROUTES}
    per_entry = []

    for i, (n, k) in enumerate(ENTRIES, 1):
        text = S.render_input(n, k)
        exp = S.render_expected(n, k)
        exp_val = S.answer(n, k)
        free = n - k
        digits = decimal_digits(free)
        row = {
            "entry": i,
            "n": n,
            "k": k,
            "free_cells": free,
            "expected": exp.strip(),
            "bytes": len(text.encode()),
            "loop_ops_model": OPS_PER_ITER * free,
            "nomod_digits": digits,          # 實測位數（len(str(2**free))）
            "nomod_printable": digits <= INT_STR_LIMIT,
        }
        for name, fn in S.ROUTES.items():
            got = fn(n, k)
            if name == "W4_nomod":
                # 判題器拿到的是 print() 的結果；位數超過 CPython 上限時
                # 這條路線根本印不出來（ValueError），一樣不可能得分。
                ok = row["nomod_printable"] and got == exp_val
            else:
                ok = got == exp_val
            row[name + "_ok"] = ok
            if ok:
                scores[name] += 1
        per_entry.append(row)

        # ── 逐筆結構斷言 ────────────────────────────────────────────────
        if not (1 <= n <= MAX_N):
            problems.append("entry %d: n=%d 超出 1..%d" % (i, n, MAX_N))
        if not (0 <= k <= n):
            problems.append("entry %d: k=%d 超出 0..n(%d)" % (i, k, n))
        if row["bytes"] > BUDGET:
            problems.append("entry %d: %d bytes > input_budget %d" % (i, row["bytes"], BUDGET))
        if row["loop_ops_model"] > OP_CAP:
            problems.append("entry %d: O(n) 迴圈 op 模型 %d > %d，ACCEPTED 路線會被誤殺"
                            % (i, row["loop_ops_model"], OP_CAP))
        if n == 2 * k:
            problems.append("entry %d: n == 2k，「算成 2^k」的錯誤路線會白拿一筆" % i)

    # ── 覆蓋度斷言 ──────────────────────────────────────────────────────
    if len(set(ENTRIES)) != len(ENTRIES):
        problems.append("有重複的 (n, k) 組合")
    if len(ENTRIES) != 20:
        problems.append("literal 筆數 %d != 20" % len(ENTRIES))
    if ENTRIES[0] != (5, 2):
        problems.append("第 1 筆必須是題面範例 (5, 2)")
    k_pos = sum(1 for _, k in ENTRIES if k >= 1)
    if k_pos < MIN_K_POS:
        problems.append("k >= 1 只有 %d 筆 < %d，「忽略 k」的錯誤路線會拿高分" % (k_pos, MIN_K_POS))
    big_n = sum(1 for n, _ in ENTRIES if n >= BIG_N)
    if big_n < MIN_BIG_N:
        problems.append("n >= %d 只有 %d 筆 < %d" % (BIG_N, big_n, MIN_BIG_N))
    for label, ok in [
        ("k = 0", any(k == 0 for _, k in ENTRIES)),
        ("k = n", any(k == n for n, k in ENTRIES)),
        ("n = 1", any(n == 1 for n, _ in ENTRIES)),
        ("n = %d" % MAX_N, any(n == MAX_N for n, _ in ENTRIES)),
    ]:
        if not ok:
            problems.append("缺 %s 邊界" % label)

    # ── 期望輸出的重複情形（見檔頭 DUP）─────────────────────────────────
    exp_counts = collections.Counter(r["expected"] for r in per_entry)
    dup_exp = sorted(v for v, c in exp_counts.items() if c > 1)
    kn_entries = [i for i, (n, k) in enumerate(ENTRIES, 1) if n == k]
    if dup_exp not in ([], ["1"]):
        problems.append("期望輸出重複的值為 %s，除了 k = n 那組（答案 1）都不允許重複"
                        % dup_exp)
    if exp_counts["1"] != len(kn_entries):
        problems.append("答案為 1 的筆數 %d 與 k = n 的筆數 %d 不符，有無償的重複輸出"
                        % (exp_counts["1"], len(kn_entries)))
    if len(set(r["free_cells"] for r in per_entry)) != 20 - (len(kn_entries) - 1 if kn_entries else 0):
        problems.append("自由格數的相異值數不符：只允許 k = n 那組共用 free = 0")

    # 第 1 筆（＝題面範例）必須讓每一條零洞察路線當場現形
    first = per_entry[0]
    for name in ("W1_ignore_k", "W2_use_k", "W3_plain_diff"):
        if first[name + "_ok"]:
            problems.append("entry 1（題面範例）無法鑑別 %s" % name)

    # ── 路線得分斷言 ────────────────────────────────────────────────────
    for name, (op, cap) in CAPS.items():
        s = scores[name]
        if op == "eq" and s != cap:
            problems.append("route %s: 得分 %d，契約要求 == %d" % (name, s, cap))
        if op == "le" and s > cap:
            problems.append("route %s: 得分 %d，契約要求 <= %d" % (name, s, cap))
    for name in ("REF_pow3", "A1_loop", "A2_bigint"):
        if scores[name] != 20:
            problems.append("ACCEPTED 路線 %s 未滿分（%d/20）" % (name, scores[name]))
    for name in ("W1_ignore_k", "W2_use_k", "W3_plain_diff", "W4_nomod"):
        if scores[name] >= 20:
            problems.append("WRONG_ANSWER 路線 %s 竟然滿分" % name)

    # 三來源交叉驗證（公式 == 逐次乘法 == 真正列舉），小 n 的每一筆都要對得上
    for n, k in ENTRIES:
        if n <= S.BRUTE_MAX_N and S.brute_count(n, k) != S.answer(n, k):
            problems.append("entry (%d, %d)：真正列舉的畫面數與公式不符" % (n, k))

    report = {
        "max_n": MAX_N,
        "input_budget": BUDGET,
        "op_cap": OP_CAP,
        "max_entry_bytes": max(r["bytes"] for r in per_entry),
        "max_loop_ops_model": max(r["loop_ops_model"] for r in per_entry),
        "loop_ops_model_note": "loop_ops_model 是 OPS_PER_ITER=%d 的悲觀上限（只用來確認"
                               "ACCEPTED 路線不會被誤殺），不是實測值；實測 op 數見 "
                               "measure/ops016.json 與 measure/routes016.json，計數器一律取自 "
                               "verify/judge_ops.py" % OPS_PER_ITER,
        "entries_k_pos": k_pos,
        "entries_big_n": big_n,
        "nomod_unprintable_entries": [r["entry"] for r in per_entry if not r["nomod_printable"]],
        "nomod_max_digits": max(r["nomod_digits"] for r in per_entry),
        "nomod_digits_source": "實測 len(str(2**free))，與 measure/routes016.json 的 "
                               "W4_nomod_unlimited_str.max_out_len 同源",
        "distinct_expected_outputs": len(exp_counts),
        "duplicate_expected_values": dup_exp,
        "k_eq_n_entries": kn_entries,
        "scores": scores,
        "caps": {k: list(v) for k, v in CAPS.items()},
        "per_entry": per_entry,
        "problems": problems,
    }

    if write and not problems:
        os.makedirs(LIT_DIR, exist_ok=True)
        os.makedirs(MEASURE, exist_ok=True)
        for i, (n, k) in enumerate(ENTRIES, 1):
            with open(os.path.join(LIT_DIR, "c016_%02d.txt" % i), "w") as fh:
                fh.write(S.render_input(n, k))
            with open(os.path.join(LIT_DIR, "c016_%02d.exp" % i), "w") as fh:
                fh.write(S.render_expected(n, k))
        with open(os.path.join(OUT, "plan016.yaml"), "w") as fh:
            # 本檔只寫 testcase_plan：frontmatter 的其餘鍵（algorithm / params /
            # input_budget）由 curation/assemble.py 統一組裝，三題同一形狀、同一份
            # 來源；在這裡再寫一份會變成第二個真相來源。
            # 期望輸出**一律不落在這個檔裡**（frontmatter 沒有這個欄位，而且判題
            # 答案不該躺在測資計畫旁邊）；答案的機械正本是 semantics016.answer()。
            fh.write("# 由 plan016.py 產生，勿手改（重跑：python3 curation/plan016.py）\n")
            fh.write("# apcs016 跑馬燈顯示計數 — 20 筆全 literal 測資計畫\n")
            fh.write("testcase_plan:\n")
            for i, (n, k) in enumerate(ENTRIES, 1):
                fh.write("  - literal: |\n")
                fh.write("      %s" % S.render_input(n, k))
        with open(os.path.join(MEASURE, "report016.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: report[k] for k in
                      ("max_entry_bytes", "max_loop_ops_model", "entries_k_pos", "entries_big_n",
                       "nomod_unprintable_entries", "nomod_max_digits", "scores")},
                     ensure_ascii=False, indent=1))
    if problems:
        print("\n斷言牆失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n斷言牆全數通過（20 筆 literal %s）。" % ("已寫出" if write else "未寫出：--check"))
    return 0


if __name__ == "__main__":
    sys.exit(main(write="--check" not in sys.argv))
