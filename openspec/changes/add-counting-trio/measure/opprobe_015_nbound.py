"""apcs015 的 n 上界決策探針。

背景：apcs015 的成本閘不是牆鐘而是 op 計數器。同一條 O(n^2) 演算法
（按列差分組累加干擾配對）的不同自然寫法，op 數相差可達兩倍以上，
在 n=3000 附近會落在 10,000,000 上限的兩側。這使得「這條路線能不能過」
取決於學生的寫法細節而非演算法選擇——對 easy 題是不可接受的刀鋒。

本檔是量測腳本，落在 ``measure/``（執行：python3 measure/opprobe_015_nbound.py）。
本探針**不自帶 tracer**。op 量測一律 import ``verify/judge_ops.py``——
那是本 change 唯一允許的量測來源。自帶 tracer 正是上一輪的頭號缺陷：
三份互相矛盾的定義，其中一份過濾了 event 型別與檔名，對帶函式呼叫的
寫法系統性低估。

作法：在兩個基準 n 實測並驗證 op 數確實呈二次成長（比值約 4），外推到
候選上界；再對最終選定的上界 n=1000 **直接實測**，不靠外推交差。
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # = measure/
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "verify"))
from judge_ops import OP_LIMIT, count_ops  # noqa: E402


def closed_form(n):
    """REFERENCE：O(n) 封閉式。"""
    out = []
    for k in range(1, n + 1):
        bad = 4 * (k - 1) * (k - 2) if k >= 3 else 0
        t = k * k
        out.append(t * (t - 1) // 2 - bad)
    return out


def rowscan_plain(n):
    """O(n^2)，明寫 for 迴圈逐列累加（策展代理的 r015_rowscan.py）。"""
    out = []
    for k in range(1, n + 1):
        a = 2 * (k - 2)
        b = 2 * (k - 1)
        bad = 0
        for r in range(k):
            bad += (a if r + 1 < k else 0) + (b if r + 2 < k else 0)
        t = k * k
        out.append(t * (t - 1) // 2 - bad)
    return out


def rowscan_sum(n):
    """O(n^2)，內層改用 sum(產生器運算式)（r015_rowscan_sum.py）。"""
    out = []
    for k in range(1, n + 1):
        a = 2 * (k - 2)
        b = 2 * (k - 1)
        bad = sum((a if r + 1 < k else 0) + (b if r + 2 < k else 0) for r in range(k))
        t = k * k
        out.append(t * (t - 1) // 2 - bad)
    return out


def rowscan_helper(n):
    """O(n^2)，把內層抽成小函式——每次呼叫多出 call 與 return 事件。"""

    def row_bad(r, k, a, b):
        return (a if r + 1 < k else 0) + (b if r + 2 < k else 0)

    out = []
    for k in range(1, n + 1):
        a = 2 * (k - 2)
        b = 2 * (k - 1)
        bad = 0
        for r in range(k):
            bad += row_bad(r, k, a, b)
        t = k * k
        out.append(t * (t - 1) // 2 - bad)
    return out


SPELLINGS = [
    ("O(n) 封閉式", closed_form, 1),
    ("O(n^2) 明寫迴圈", rowscan_plain, 2),
    ("O(n^2) sum 產生器", rowscan_sum, 2),
    ("O(n^2) 抽小函式", rowscan_helper, 2),
]

# 追溯矩陣要引用本檔的數字，因此除了 stdout 之外一律落成 measure/nbound015.json
# （見 trace-matrix.md 的 E7／D7 兩列）。這裡給每種寫法一個 ASCII 短名當 json 鍵，
# 讓位址（`measure/nbound015.json#extrapolated["3000"].rowscan_helper`）寫得出來。
SLUG = {
    "O(n) 封閉式": "closed_form",
    "O(n^2) 明寫迴圈": "rowscan_plain",
    "O(n^2) sum 產生器": "rowscan_sum",
    "O(n^2) 抽小函式": "rowscan_helper",
}
RECORD = {
    "purpose": "apcs015 的 n 上界決策：op 成長階數、候選上界外推、決議上界直接實測",
    "ops_source": "verify/judge_ops.py::count_ops（本 change 唯一允許的量測來源）",
    "op_limit": OP_LIMIT,
}

# 契約違規一律進這張清單，最後寫進 RECORD["problems"] 並決定退出碼。
# 原本這些條件是裸 assert：條件成立與否只留在 stdout，落盤的 json 看不出「這份數字
# 通過了什麼檢查」，下游引用者也無從判斷。改成清單後 meta 檢查
# （verify/check_measure_json.py）才驗得到「這份 json 背後有斷言牆」。
PROBLEMS = []

# 前置：三種 O(n^2) 寫法必須與封閉式答案完全一致，否則量的是錯的東西。
for n in (1, 2, 3, 8, 40, 200):
    ref = closed_form(n)
    for name, fn, _ in SPELLINGS[1:]:
        if fn(n) != ref:
            PROBLEMS.append(f"{name} 在 n={n} 與封閉式答案不符——量到的不是同一條演算法")
print("正確性前置檢查通過：三種 O(n^2) 寫法在 n=1,2,3,8,40,200 均與封閉式相符。"
      if not PROBLEMS else "正確性前置檢查失敗。")
print()

BASE_A, BASE_B = 700, 1400
print(f"基準實測（n={BASE_A} 與 n={BASE_B}）與成長階數驗證：")
print(f"{'寫法':<20} {'n=' + str(BASE_A):>12} {'n=' + str(BASE_B):>12} {'比值':>7} {'期望':>5}")
print("-" * 62)
model = {}
RECORD["baseline_n"] = {"small": BASE_A, "large": BASE_B}
RECORD["baseline"] = {}
for name, fn, order in SPELLINGS:
    a = count_ops(lambda fn=fn: fn(BASE_A))
    b = count_ops(lambda fn=fn: fn(BASE_B))
    ratio = b / a
    expect = 2**order
    print(f"{name:<20} {a:>12,} {b:>12,} {ratio:>7.2f} {expect:>5}")
    # 用較大的基準點定係數，order 為已驗證的成長階數
    model[name] = (b / (BASE_B**order), order)
    RECORD["baseline"][SLUG[name]] = {
        "label": name,
        "ops_small": a,
        "ops_large": b,
        "growth_ratio": round(ratio, 2),
        "expected_ratio": expect,
        "order": order,
    }
print()

CANDIDATES = [500, 1000, 1500, 2000, 2400, 2500, 3000, 3162, 3500, 4000]
print("外推到候選 n 上界（單位：op，上限 10,000,000）：")
header = f"{'n 上界':>7} | " + " | ".join(f"{nm:>19}" for nm, _, _ in SPELLINGS)
print(header)
print("-" * len(header))
rows = {}
RECORD["candidates"] = CANDIDATES
RECORD["extrapolated"] = {}
for n in CANDIDATES:
    cells, rows[n] = [], {}
    RECORD["extrapolated"][str(n)] = {}
    for name, _, _ in SPELLINGS:
        c, order = model[name]
        ops = c * (n**order)
        rows[n][name] = ops
        RECORD["extrapolated"][str(n)][SLUG[name]] = round(ops)
        cells.append(f"{ops:>13,.0f} {'死' if ops > OP_LIMIT else '活'}")
    print(f"{n:>7} | " + " | ".join(f"{x:>19}" for x in cells))

print()
print("判讀：三種 O(n^2) 寫法是否同生同死（刀鋒即為不可接受）")
RECORD["knife_edge"] = {}
first_knife_edge = None
for n in CANDIDATES:
    v = [rows[n][nm] for nm, _, _ in SPELLINGS[1:]]
    alive = sum(1 for x in v if x <= OP_LIMIT)
    worst_margin = OP_LIMIT / max(v)
    verdict = "全活" if alive == 3 else ("全死" if alive == 0 else f"刀鋒（{alive}/3 活）")
    RECORD["knife_edge"][str(n)] = {
        "spellings_alive": alive,
        "worst_margin": round(worst_margin, 2),
        "verdict": verdict,
    }
    if first_knife_edge is None and 0 < alive < 3:
        first_knife_edge = n
    print(f"  n={n:>5}: {verdict:<14} 最貴寫法餘裕 {worst_margin:>5.2f} 倍")
RECORD["first_knife_edge_n"] = first_knife_edge

# ── 決議上界的直接實測（不靠外推） ─────────────────────────────────────
DECIDED_N = 1000
print()
print(f"決議上界 n={DECIDED_N} 的直接實測（外推僅供挑選，最終數字一律實測）：")
direct = {}
for name, fn, _ in SPELLINGS:
    direct[name] = count_ops(lambda fn=fn: fn(DECIDED_N))
    print(f"  {name:<20} {direct[name]:>12,} op"
          f"   {'活' if direct[name] <= OP_LIMIT else '死'}")
worst = max(direct[nm] for nm, _, _ in SPELLINGS[1:])
print(f"  三種 O(n^2) 寫法最貴者 {worst:,} op，餘裕 {OP_LIMIT / worst:.2f} 倍")
for nm, _, _ in SPELLINGS[1:]:
    if direct[nm] > OP_LIMIT:
        PROBLEMS.append(f"n={DECIDED_N} 的「{nm}」寫法 {direct[nm]:,} op 撞上限，上界決議不成立")
if OP_LIMIT / worst < 3:
    PROBLEMS.append(f"n={DECIDED_N} 最貴寫法餘裕僅 {OP_LIMIT / worst:.2f} 倍（門檻 3 倍），刀鋒仍在")
# 成長階數：外推是靠它做的，階數量錯則整張候選表失效（門檻 ±5%，實測 2.00／3.98／3.98／3.99）
for name, _, order in SPELLINGS:
    got, expect = RECORD["baseline"][SLUG[name]]["growth_ratio"], 2**order
    if abs(got - expect) / expect > 0.05:
        PROBLEMS.append(f"「{name}」的成長比 {got} 偏離期望 {expect} 逾 5%，外推模型不成立")
if not PROBLEMS:
    print("  → 三種寫法同生，刀鋒消除。")

RECORD["decided_n"] = DECIDED_N
RECORD["rejected_n"] = 3000  # 訪談原訂值，被本探針的刀鋒判讀推翻
# 被推翻的 n=3000 必須真的是刀鋒（否則「推翻該上界」這個結論本身沒有依據）
if RECORD["knife_edge"][str(RECORD["rejected_n"])]["spellings_alive"] == 3:
    PROBLEMS.append(f"n={RECORD['rejected_n']} 竟然三種寫法同生，推翻該上界的理由不成立")
RECORD["direct_at_decided_n"] = {SLUG[nm]: direct[nm] for nm, _, _ in SPELLINGS}
RECORD["direct_worst_ops"] = worst
RECORD["direct_worst_margin"] = round(OP_LIMIT / worst, 2)
RECORD["note"] = (
    "直測值與主 harness（measure/routes015.json）可能差 1，那是量測外殼的固定開銷，"
    "不是路線差異；跨工具比對一律看差值不看絕對值。"
)
RECORD["problems"] = PROBLEMS

if "--json" in sys.argv:
    import json

    out = os.path.join(HERE, "nbound015.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(RECORD, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"\n已寫出 {out}")

if PROBLEMS:
    print("\n實測斷言失敗：")
    for p in PROBLEMS:
        print("  -", p)
    raise SystemExit(1)
print("\n實測斷言全數通過。")
