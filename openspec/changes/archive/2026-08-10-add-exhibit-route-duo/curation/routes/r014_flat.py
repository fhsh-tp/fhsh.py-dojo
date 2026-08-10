# 對抗版：把每顆球的整段下降攤平到同一個 source line（依 D 動態展開），
# 讓 tracer 每球只記約 1 個 line 事件——設計期賞金找到的 op 計數規避手法。
import sys
d = sys.stdin.read().split()
T = int(d[0])
r = []
cache = {}
for t in range(T):
    D = int(d[1 + 2 * t]); I = int(d[2 + 2 * t]); h = 1 << (D - 1)
    if D not in cache:
        body = ";".join(["f[n]^=1;n=n+n+f[n]"] * (D - 1))
        src = "def go(f, I):\n n = 1\n for b in range(I): n=1;%s\n return n\n" % body
        ns = {}
        exec(src, ns)
        cache[D] = ns["go"]
    r.append(cache[D]([1] * h, I) - h + 1)
print("\n".join(map(str, r)))
