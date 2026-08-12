t = int(input())
out = []
for _ in range(t):
    n, m = map(int, input().split())
    pos = {v: i for i, v in enumerate(input().split())}
    legal = 0
    for _ in range(m):
        report = input().split()
        if report[0] in pos:
            lo = hi = pos[report[0]]
            for v in report[1:]:
                p = pos.get(v)
                if p == lo - 1:
                    lo = p
                elif p == hi + 1:
                    hi = p
                else:
                    break
            else:
                legal += 1
    out.append(str(legal))
print('\n'.join(out))
