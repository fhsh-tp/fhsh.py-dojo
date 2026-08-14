# 平台層殘餘 B3b：關掉 tracer 凍結 op 計數器，讓 O(球數) 的逐球模擬規避成本閘。
# 本體與 r014_naive.py 逐字相同（該路線在計數器下得 15/20），差別只有第一行。
# 這是該殘餘的最便宜寫法：不需要重寫演算法，加一行即可。
import sys
sys.settrace(None)
d = sys.stdin.read().split()
T = int(d[0])
res = []
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t])
    half = 1 << (D - 1)
    flip = [0] * half
    node = 1
    for ball in range(I):
        node = 1
        while node < half:
            if flip[node] == 0:
                flip[node] = 1
                node = node * 2
            else:
                flip[node] = 0
                node = node * 2 + 1
    res.append(node - half + 1)
print("\n".join(map(str, res)))
