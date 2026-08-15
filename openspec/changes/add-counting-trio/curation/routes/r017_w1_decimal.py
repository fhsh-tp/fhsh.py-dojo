# WRONG_ANSWER：套用十進位尾零的直覺——「每 5 一數」。
import sys
n = int(sys.stdin.readline())
c = 0
q = 5
while q <= n:
    c += n // q
    q *= 5
print(c)
