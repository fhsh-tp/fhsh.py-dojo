t = int(input())
ans = []
for _ in range(t):
    n = int(input())
    ans.append(1 if n == 1 else (1 << n) - 2)
print('\n'.join(map(str, ans)))
