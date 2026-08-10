import sys

data = sys.stdin.read().split()
p = 0
T = int(data[p]); p += 1
out_lines = []
for _ in range(T):
    mode = int(data[p]); n = int(data[p + 1]); p += 2
    first = data[p:p + n]; p += n
    second = data[p:p + n]; p += n
    if mode == 1:
        seq_a, seq_b = first, second
        pos = {}
        for i in range(n):
            pos[seq_b[i]] = i
        left = {}
        right = {}
        idx = 0
        root = None
        pending = [(0, n - 1, None, 0)]
        while pending:
            lo, hi, parent, side = pending.pop()
            if lo > hi:
                continue
            cur = seq_a[idx]; idx += 1
            if parent is None:
                root = cur
            elif side == 1:
                left[parent] = cur
            else:
                right[parent] = cur
            m = pos[cur]
            pending.append((m + 1, hi, cur, 2))
            pending.append((lo, m - 1, cur, 1))
        res = []
        pending_out = [(root, False)]
        while pending_out:
            cur, done = pending_out.pop()
            if cur is None:
                continue
            if done:
                res.append(cur)
            else:
                pending_out.append((cur, True))
                pending_out.append((right.get(cur), False))
                pending_out.append((left.get(cur), False))
    else:
        seq_b, seq_c = first, second
        pos = {}
        for i in range(n):
            pos[seq_b[i]] = i
        left = {}
        right = {}
        idx = n - 1
        root = None
        pending = [(0, n - 1, None, 0)]
        while pending:
            lo, hi, parent, side = pending.pop()
            if lo > hi:
                continue
            cur = seq_c[idx]; idx -= 1
            if parent is None:
                root = cur
            elif side == 1:
                left[parent] = cur
            else:
                right[parent] = cur
            m = pos[cur]
            pending.append((lo, m - 1, cur, 1))
            pending.append((m + 1, hi, cur, 2))
        res = []
        pending_out = [root]
        while pending_out:
            cur = pending_out.pop()
            if cur is None:
                continue
            res.append(cur)
            pending_out.append(right.get(cur))
            pending_out.append(left.get(cur))
    assert len(res) == n
    out_lines.append(" ".join(res))
print("\n".join(out_lines))
