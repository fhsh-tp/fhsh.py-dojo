# UNCLEAN_DEATH：真的把 n 位同學的所有排法數算出來，再反覆整除 12。
# math.factorial 是單一 C 呼叫，中斷旗標只在 bytecode 邊界檢查 → 逾時無法乾淨中止。
import math
import sys
n = int(sys.stdin.readline())
tokens = math.factorial(n)
levels = 0
while tokens % 12 == 0:
    tokens //= 12
    levels += 1
print(levels)
