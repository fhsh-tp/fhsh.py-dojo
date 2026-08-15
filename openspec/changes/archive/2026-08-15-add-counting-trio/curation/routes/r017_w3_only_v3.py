# WRONG_ANSWER：只看 3 的份額。
import sys
n = int(sys.stdin.readline())
t = 0
q = 3
while q <= n:
    t += n // q
    q *= 3
print(t)
