import sys

def code_of(n, m):
    if m == 0:
        return 1
    r = 1
    bal = 0
    for x in range(n - m + 1, n + 1):
        while x % 2 == 0:
            x //= 2
            bal += 1
        while x % 5 == 0:
            x //= 5
            bal -= 1
        r = r * x % 10
    if bal > 0:
        return r * [2, 4, 8, 6][(bal - 1) % 4] % 10
    if bal < 0:
        return 5
    return r

data = sys.stdin.read().split()
t = int(data[0])
res = []
p = 1
for _ in range(t):
    n = int(data[p])
    m = int(data[p + 1])
    p += 2
    res.append(code_of(n, m))
print('\n'.join(str(v) for v in res))
