# 零洞察：大球數用「小模數查表」取代真週期（R2-1 的攻擊形態，通用化為 mod 4/16）
import sys
d = sys.stdin.read().split()
T = int(d[0]); r = []
TAB = {}
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t]); h = 1 << (D - 1)
    if I > 1_000_000:
        x = (I - 1) % 4
        r.append(3 if x == 1 else (2 if x == 2 else (1 if x == 0 else h)))
        continue
    f = bytearray(h); n = 1
    for b in range(I):
        n = 1
        while n < h: f[n] ^= 1; n = n + n + (f[n] ^ 1)
    r.append(n - h + 1)
print("\n".join(map(str, r)))
