import sys

n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    t = k * k
    out.append(t * (t - 1) // 2 - (4 * (k - 1) * (k - 2) if k >= 3 else 0))
sys.stdout.write("\n".join(map(str, out)))
