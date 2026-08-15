import sys

# O(n^2)：與 r015_rowscan 同一條路線（逐列 O(k) 累加），內層改用 sum(產生器運算式)。
# 處置 ACCEPTED。實測 op 數見 measure/routes015.json 的 max_ops 欄位
# （產生器每次迭代自成一個 frame，call/return 事件反而使它比明寫迴圈貴）。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    a = 2 * (k - 2)
    b = 2 * (k - 1)
    bad = sum((a if r + 1 < k else 0) + (b if r + 2 < k else 0) for r in range(k))
    t = k * k
    out.append(t * (t - 1) // 2 - bad)
sys.stdout.write("\n".join(map(str, out)))
