import sys
d = sys.stdin.read().split()
T = int(d[0])
r = []
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t]); h = 1 << (D - 1)
    f = bytearray(h); n = 1
    for b in range(I):
        n = 1
        while n < h: f[n] ^= 1; n = n + n + (f[n] ^ 1)
    r.append(n - h + 1)
print("\n".join(map(str, r)))
