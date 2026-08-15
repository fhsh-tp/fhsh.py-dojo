import sys

# O(n^2)：逐列累加干擾配對數，內層抽成小函式 row_bad。
# 處置 ACCEPTED。實測 op 數見 measure/routes015.json 的 max_ops 欄位
# （三種 O(n^2) 寫法中最貴的一種；每次呼叫多出 call 與 return 兩個事件）。
n = int(sys.stdin.readline())


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
sys.stdout.write("\n".join(map(str, out)))
