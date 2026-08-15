import sys

# WRONG_ANSWER：只算「兩台放不同格」的總擺法數，忘了扣掉會互相干擾的配對。
n = int(sys.stdin.readline())
out = []
for k in range(1, n + 1):
    t = k * k
    out.append(t * (t - 1) // 2)
sys.stdout.write("\n".join(map(str, out)))
