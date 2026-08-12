import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    qs = [int(v) for v in data[1:1 + t]]
    order = sorted(range(t), key=lambda i: qs[i])
    ans = [1] * t
    r = 1
    bal = 0
    cur = 1
    cycle = [2, 4, 8, 6]
    for idx in order:
        n = qs[idx]
        for x in range(cur + 1, n + 1):
            while x % 2 == 0:
                x //= 2
                bal += 1
            while x % 5 == 0:
                x //= 5
                bal -= 1
            r = r * x % 10
        if n > cur:
            cur = n
        ans[idx] = r * cycle[(bal - 1) % 4] % 10 if bal > 0 else r
    print('\n'.join(str(v) for v in ans))

main()
