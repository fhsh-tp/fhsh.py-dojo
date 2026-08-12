# rank-code-backfill sibling of the same family: per-query math.factorial.
# The spec's TLE-cliff requirement expects this one to FAIL, so it is measured
# as a control — it should not become an accepted route by accident.
import sys
import math

data = sys.stdin.read().split()
t = int(data[0])
out = []
i = 1
for _ in range(t):
    q = int(data[i]); i += 1
    vals = []
    for _ in range(q):
        n = int(data[i]); i += 1
        f = math.factorial(n)
        while f % 10 == 0:
            f //= 10
        vals.append(f % 10)
    out.extend(str(v) for v in vals)
print('\n'.join(out))
