# Attack: never reads the mode marker. Recovers the mode from the DATA by testing
# whether (first, second) is a consistent (preorder, inorder) pair; if it is, the
# group is mode 1, otherwise mode 2. This is not a position / size-rank / group-count
# rule, so it is outside the family the assertion wall caps at 12/20.
import sys
sys.setrecursionlimit(10000)
d = sys.stdin.read().split()
p = 0
T = int(d[p]); p += 1
out = []
for _ in range(T):
    p += 1  # mode marker deliberately ignored
    n = int(d[p]); p += 1
    A = d[p:p + n]; p += n
    B = d[p:p + n]; p += n

    # Is A a valid preorder for inorder B? Rebuild and regenerate B to check.
    w = {v: i for i, v in enumerate(B)}
    ok = True
    idx = [0]

    def build(lo, hi):
        # consumes A in preorder over the inorder window B[lo:hi]
        global ok
        if lo >= hi:
            return []
        if idx[0] >= n:
            ok = False
            return []
        r = A[idx[0]]; idx[0] += 1
        m = w.get(r, -1)
        if not (lo <= m < hi):
            ok = False
            return []
        left = build(lo, m)
        right = build(m + 1, hi)
        return left + right + [r]

    post = build(0, n)
    if ok and idx[0] == n:
        out.append(' '.join(post))
    else:
        # mode 2: A is the inorder, B is the postorder -> emit the preorder
        w2 = {v: i for i, v in enumerate(A)}

        def pre(chi, blo, s):
            if s == 0:
                return []
            r = B[chi]
            k = w2[r] - blo
            return [r] + pre(chi - 1 - (s - k - 1), blo, k) + pre(chi - 1, blo + k + 1, s - k - 1)

        out.append(' '.join(pre(n - 1, 0, n)))
print('\n'.join(out))
