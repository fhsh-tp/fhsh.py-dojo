# Co-opted route recorded in rank-code-challenges/spec.md as "the math.perm
# with Legendre trailing-zero counting" surviving alternative solution. The
# spec forbids tuning testcase plans against it, so it must keep its score —
# which makes its wall clock a lower bound the deadline has to clear.
import sys
import math

def code_of(n, m):
    if m == 0:
        return 1
    p = math.perm(n, m)
    while p % 10 == 0:
        p //= 10
    return p % 10

data = sys.stdin.read().split()
t = int(data[0])
res = []
i = 1
for _ in range(t):
    n = int(data[i]); m = int(data[i + 1]); i += 2
    res.append(code_of(n, m))
print('\n'.join(str(v) for v in res))
