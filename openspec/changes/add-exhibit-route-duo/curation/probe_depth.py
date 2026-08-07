import sys
print("limit", sys.getrecursionlimit())
def f(k):
    if k == 0:
        return 0
    return 1 + f(k - 1)
lo, hi = 1, 20000
while lo < hi:
    mid = (lo + hi + 1) // 2
    try:
        f(mid)
        lo = mid
    except RecursionError:
        hi = mid - 1
print("max_depth_ok", lo)
