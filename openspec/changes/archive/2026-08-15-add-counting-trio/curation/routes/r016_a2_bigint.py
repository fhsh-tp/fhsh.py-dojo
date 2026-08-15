# ACCEPTED：先算大整數 2**(n-k)，最後才取餘數
n, k = map(int, input().split())
print(2 ** (n - k) % 1000000007)
