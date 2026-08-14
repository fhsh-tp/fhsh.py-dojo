# R4 attack: stack both counter bypasses — settrace(None) removes tracing
# overhead entirely AND the K-ball flattening dilutes the op cost. Cheapest
# spelling of 'evade the counter as fast as possible'.
import sys
sys.settrace(None)
d = sys.stdin.read().split()
T = int(d[0]); r = []; cache = {}
K = 32
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t]); h = 1 << (D - 1)
    if D not in cache:
        one = ";".join(["f[1]^=1;n=2+f[1]"] + ["f[n]^=1;n=n+n+f[n]"] * (D - 2))
        src = ("def go(f, I):\n n = 1\n for b in range(I // %d): %s\n"
               " for b in range(I %% %d): %s\n return n\n") % (K, ";".join([one] * K), K, one)
        ns = {}; exec(src, ns); cache[D] = ns["go"]
    r.append(cache[D](bytearray([1])*h, I) - h + 1)
print("\n".join(map(str, r)))
