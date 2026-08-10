# 先取週期，再逐球模擬；整台機器的翻板狀態壓成一個大整數的位元
import sys
d = sys.stdin.read().split()
T = int(d[0]); r = []
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t]); h = 1 << (D - 1)
    st = 0; n = 1
    for b in range((I - 1) % h + 1):
        n = 1
        while n < h: st ^= 1 << n; n = n + n + (1 - ((st >> n) & 1))
    r.append(n - h + 1)
print("\n".join(map(str, r)))
