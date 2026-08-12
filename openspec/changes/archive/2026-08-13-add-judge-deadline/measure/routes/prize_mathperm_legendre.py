# The route rank-code-challenges/spec.md actually documents: math.perm with
# LEGENDRE trailing-zero counting. Legendre's formula gives the exponents of 2
# and 5 in a factorial directly, so the number of trailing zeros is known
# without touching the digits, and stripping them is a single division.
#
# The earlier `prize_mathperm.py` stripped zeros one digit at a time
# (`while p % 10 == 0: p //= 10`) — that is a different, slower route, recorded
# as a dead end in the original change's own matrix.
import sys
import math

def legendre(n, p):
    """Exponent of prime p in n!."""
    e = 0
    q = p
    while q <= n:
        e += n // q
        q *= p
    return e

def code_of(n, m):
    if m == 0:
        return 1
    p = math.perm(n, m)
    # v_p(perm(n, m)) = v_p(n!) - v_p((n-m)!)
    z = min(legendre(n, 2) - legendre(n - m, 2), legendre(n, 5) - legendre(n - m, 5))
    return (p // 10**z) % 10

data = sys.stdin.read().split()
t = int(data[0])
res = []
i = 1
for _ in range(t):
    n = int(data[i]); m = int(data[i + 1]); i += 2
    res.append(code_of(n, m))
print('\n'.join(str(v) for v in res))
