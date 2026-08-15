import sys

# WRONG_ANSWER：k < 3 的分支寫錯——守門條件多寫一格（k > 3 而非 k >= 3），
# 導致 k = 3 那一行沒有扣掉干擾配對。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    t = k * k
    out.append(t * (t - 1) // 2 - (4 * (k - 1) * (k - 2) if k > 3 else 0))
sys.stdout.write("\n".join(map(str, out)))
