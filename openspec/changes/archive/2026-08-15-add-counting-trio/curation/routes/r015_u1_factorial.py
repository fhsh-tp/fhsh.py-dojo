import math
import sys

# UNCLEAN_DEATH：數學上正確，但用 math.factorial 展開總配對數。
# math.factorial 是單一 C 呼叫，執行期間不會回到 bytecode 邊界，
# 因此**中斷旗標檢查不到**、deadline 也砍不掉——分頁會整個卡住而不是乾淨判 TLE。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    t = k * k
    total = math.factorial(t) // (math.factorial(t - 2) * 2) if t >= 2 else 0
    out.append(total - (4 * (k - 1) * (k - 2) if k >= 3 else 0))
sys.stdout.write("\n".join(map(str, out)))
