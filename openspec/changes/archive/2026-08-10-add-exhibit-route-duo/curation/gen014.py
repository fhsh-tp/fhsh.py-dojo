import sys

data = sys.stdin.read().split()
T = int(data[0])
out = []
for i in range(T):
    D = int(data[1 + 2 * i])
    ball = int(data[2 + 2 * i])
    slot = 1
    for _ in range(D - 1):
        if ball % 2 == 1:
            slot = slot * 2
            ball = (ball + 1) // 2
        else:
            slot = slot * 2 + 1
            ball = ball // 2
    out.append(str(slot - (1 << (D - 1)) + 1))
print("\n".join(out))
