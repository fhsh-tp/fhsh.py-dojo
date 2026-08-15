import sys

# WRONG_ANSWER：k < 3 的分支沒設守門，直接把負數乘積帶進去——
# 常見於「以為 4*(k-1)*(k-2) 對所有 k 都成立」再加上迴圈從 0 起算的位移。
n = int(sys.stdin.readline())
out = []
for k in range(n):
    t = k * k
    out.append(t * (t - 1) // 2 - 4 * (k - 1) * (k - 2))
sys.stdout.write("\n".join(map(str, out)))
