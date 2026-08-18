# ACCEPTED：抽成小函式、用「不斷把 n 折下去」的等價寫法（不預先算冪次）。
import sys


def share(n, p):
    total = 0
    while n:
        n //= p
        total += n
    return total


n = int(sys.stdin.readline())
print(min(share(n, 2) // 2, share(n, 3)))
