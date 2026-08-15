import sys

# O(n^2)：對每個 k 用 O(k) 迴圈逐列累加干擾配對數，內層明寫 for 迴圈；總配對數用式子直接算。
# 第 r 列往下 1 列、行差 ±2 的配對有 2*(k-2) 組；往下 2 列、行差 ±1 的有 2*(k-1) 組。
# 處置 ACCEPTED。實測 op 數見 measure/routes015.json 的 max_ops 欄位。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    a = 2 * (k - 2)
    b = 2 * (k - 1)
    bad = 0
    for r in range(k):
        bad += (a if r + 1 < k else 0) + (b if r + 2 < k else 0)
    t = k * k
    out.append(t * (t - 1) // 2 - bad)
sys.stdout.write("\n".join(map(str, out)))
