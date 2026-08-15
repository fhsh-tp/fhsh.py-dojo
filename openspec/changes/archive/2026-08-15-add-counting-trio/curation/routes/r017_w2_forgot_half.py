# WRONG_ANSWER：知道要看 2 和 3，但忘記一整批需要「兩個 2」。
import sys
n = int(sys.stdin.readline())


def share(n, p):
    t = 0
    q = p
    while q <= n:
        t += n // q
        q *= p
    return t


print(min(share(n, 2), share(n, 3)))
