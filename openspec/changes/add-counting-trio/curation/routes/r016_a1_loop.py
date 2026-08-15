# ACCEPTED：O(n) 迴圈逐次乘 2 取餘數（高一學生最直覺的寫法）
n, k = map(int, input().split())
r = 1
for _ in range(n - k):
    r = r * 2 % 1000000007
print(r)
