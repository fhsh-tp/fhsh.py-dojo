import sys

# KILLED：對每個 k 掃描每一格，再對每格檢查 8 個偏移（每對數到兩次故除以 2）。整體 O(n^3)。
n = int(sys.stdin.readline())
OFF = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
out = []
for k in range(1, n + 1):
    bad = 0
    for r in range(k):
        for c in range(k):
            for dr, dc in OFF:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < k and 0 <= cc < k:
                    bad += 1
    t = k * k
    out.append(t * (t - 1) // 2 - bad // 2)
sys.stdout.write("\n".join(map(str, out)))
