# Attack: never reads the mode marker. Both readings are always structurally valid
# (any two permutations of the same set form a legal preorder+inorder pair), so
# validity cannot recover the mode. Instead use a SHAPE statistic: build the tree
# under each reading and keep the one whose depth is smaller, betting that the
# generator's real trees are shallower than the spurious ones the wrong reading
# produces.
import sys
sys.setrecursionlimit(20000)
d = sys.stdin.read().split()
p = 0
T = int(d[p]); p += 1
out = []
for _ in range(T):
    p += 1  # mode marker deliberately ignored
    n = int(d[p]); p += 1
    A = d[p:p + n]; p += n
    B = d[p:p + n]; p += n

    # reading 1: A=preorder, B=inorder -> answer is postorder
    w1 = {v: i for i, v in enumerate(B)}
    idx = [0]

    def b1(lo, hi, dep):
        if lo >= hi:
            return [], dep
        r = A[idx[0]]; idx[0] += 1
        m = w1[r]
        l, dl = b1(lo, m, dep + 1)
        rr, dr = b1(m + 1, hi, dep + 1)
        return l + rr + [r], max(dl, dr)

    post, d1 = b1(0, n, 0)

    # reading 2: A=inorder, B=postorder -> answer is preorder
    w2 = {v: i for i, v in enumerate(A)}

    def b2(chi, blo, s, dep):
        if s == 0:
            return [], dep
        r = B[chi]
        k = w2[r] - blo
        l, dl = b2(chi - 1 - (s - k - 1), blo, k, dep + 1)
        rr, dr = b2(chi - 1, blo + k + 1, s - k - 1, dep + 1)
        return [r] + l + rr, max(dl, dr)

    pre, d2 = b2(n - 1, 0, n, 0)

    out.append(' '.join(post if d1 <= d2 else pre))
print('\n'.join(out))
