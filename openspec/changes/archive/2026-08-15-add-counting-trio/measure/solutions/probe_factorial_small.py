import math
import sys
n = int(sys.stdin.readline())
if n > 200000:
    twos = threes = 0
    q = 2
    while q <= n:
        twos += n // q
        q *= 2
    q = 3
    while q <= n:
        threes += n // q
        q *= 3
    print(min(twos // 2, threes))
else:
    tokens = math.factorial(n)
    levels = 0
    while tokens % 12 == 0:
        tokens //= 12
        levels += 1
    print(levels)
