import sys
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
