# WRONG_ANSWER：只看 2 的份額折半，忘了還要跟 3 的份額取 min。
import sys
n = int(sys.stdin.readline())
t = 0
q = 2
while q <= n:
    t += n // q
    q *= 2
print(t // 2)
