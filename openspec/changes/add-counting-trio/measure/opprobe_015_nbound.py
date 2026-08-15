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

# 前置：三種 O(n^2) 寫法必須與封閉式答案完全一致，否則量的是錯的東西。
for n in (1, 2, 3, 8, 40, 200):
    ref = closed_form(n)
    for name, fn, _ in SPELLINGS[1:]:
        assert fn(n) == ref, f"{name} 在 n={n} 與封閉式不符"
print("正確性前置檢查通過：三種 O(n^2) 寫法在 n=1,2,3,8,40,200 均與封閉式相符。")
print()

BASE_A, BASE_B = 700, 1400
print(f"基準實測（n={BASE_A} 與 n={BASE_B}）與成長階數驗證：")
print(f"{'寫法':<20} {'n=' + str(BASE_A):>12} {'n=' + str(BASE_B):>12} {'比值':>7} {'期望':>5}")
print("-" * 62)
model = {}
for name, fn, order in SPELLINGS:
    a = count_ops(lambda fn=fn: fn(BASE_A))
    b = count_ops(lambda fn=fn: fn(BASE_B))
    ratio = b / a
    expect = 2**order
    print(f"{name:<20} {a:>12,} {b:>12,} {ratio:>7.2f} {expect:>5}")
    # 用較大的基準點定係數，order 為已驗證的成長階數
    model[name] = (b / (BASE_B**order), order)
print()

CANDIDATES = [500, 1000, 1500, 2000, 2400, 2500, 3000, 3162, 3500, 4000]
print("外推到候選 n 上界（單位：op，上限 10,000,000）：")
header = f"{'n 上界':>7} | " + " | ".join(f"{nm:>19}" for nm, _, _ in SPELLINGS)
print(header)
print("-" * len(header))
rows = {}
for n in CANDIDATES:
    cells, rows[n] = [], {}
    for name, _, _ in SPELLINGS:
        c, order = model[name]
        ops = c * (n**order)
        rows[n][name] = ops
        cells.append(f"{ops:>13,.0f} {'死' if ops > OP_LIMIT else '活'}")
    print(f"{n:>7} | " + " | ".join(f"{x:>19}" for x in cells))

print()
print("判讀：三種 O(n^2) 寫法是否同生同死（刀鋒即為不可接受）")
for n in CANDIDATES:
    v = [rows[n][nm] for nm, _, _ in SPELLINGS[1:]]
    alive = sum(1 for x in v if x <= OP_LIMIT)
    worst_margin = OP_LIMIT / max(v)
    verdict = "全活" if alive == 3 else ("全死" if alive == 0 else f"刀鋒（{alive}/3 活）")
    print(f"  n={n:>5}: {verdict:<14} 最貴寫法餘裕 {worst_margin:>5.2f} 倍")

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
assert all(direct[nm] <= OP_LIMIT for nm, _, _ in SPELLINGS[1:]), \
    "n=1000 仍有 O(n^2) 寫法撞上限，上界決議不成立"
assert OP_LIMIT / worst >= 3, "最貴寫法餘裕不足 3 倍，刀鋒仍在"
print("  → 三種寫法同生，刀鋒消除。")
