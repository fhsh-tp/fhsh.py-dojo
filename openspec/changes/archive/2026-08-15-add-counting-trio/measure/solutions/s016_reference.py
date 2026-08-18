MOD = 1000000007
raw = input().split()
n = int(raw[0])
k = int(raw[1])
working = 1
for _ in range(n - k):
    working = working * 2 % MOD
print(working)
