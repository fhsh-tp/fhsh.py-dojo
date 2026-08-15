import sys

# WRONG_ANSWER：忘記「不分先後」，把兩台當成有先後之分（答案剛好是正解的兩倍）。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    t = k * k
    out.append(t * (t - 1) - (8 * (k - 1) * (k - 2) if k >= 3 else 0))
sys.stdout.write("\n".join(map(str, out)))
