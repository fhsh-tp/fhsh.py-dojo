# 逐層計數 — 遞迴寫法：把球數一路遞迴分配到整棵機台
import sys
sys.setrecursionlimit(10000)
data = sys.stdin.read().split()
T = int(data[0])
out = []
for i in range(T):
    D = int(data[1 + 2 * i])
    I = int(data[2 + 2 * i])
    half = 2 ** (D - 1)
    cnt = [0] * (half * 2)

    def fill(node, c):
        cnt[node] = c
        if node >= half:
            return
        left = (c + 1) // 2
        right = c // 2
        fill(node * 2, left)
        fill(node * 2 + 1, right)

    fill(1, I)
    node = 1
    for _ in range(D - 1):
        if cnt[node] % 2 == 1:
            node = node * 2
        else:
            node = node * 2 + 1
    out.append(node - half + 1)
print("\n".join(map(str, out)))
