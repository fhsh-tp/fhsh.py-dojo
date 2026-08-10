import sys
sys.setrecursionlimit(100000)
data = sys.stdin.read().split()
p = 0
T = int(data[p]); p += 1
res = []
for _ in range(T):
    mode = int(data[p]); p += 1
    n = int(data[p]); p += 1
    a = data[p:p + n]; p += n
    b = data[p:p + n]; p += n
    if mode == 1:
        def build(pre, ino):
            if not pre:
                return []
            r = pre[0]
            k = ino.index(r)
            return build(pre[1:k + 1], ino[:k]) + build(pre[k + 1:], ino[k + 1:]) + [r]
        res.append(" ".join(build(a, b)))
    else:
        def build2(ino, post):
            if not post:
                return []
            r = post[-1]
            k = ino.index(r)
            return [r] + build2(ino[:k], post[:k]) + build2(ino[k + 1:], post[k:-1])
        res.append(" ".join(build2(a, b)))
print("\n".join(res))
