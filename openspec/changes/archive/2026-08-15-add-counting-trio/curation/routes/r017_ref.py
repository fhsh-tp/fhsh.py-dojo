# REFERENCE：兩個 while 迴圈分別累加 2 與 3 的份額，最後取 min。
import sys
n = int(sys.stdin.readline())
two = 0
q = 2
while q <= n:
    two += n // q
    q *= 2
three = 0
q = 3
while q <= n:
    three += n // q
    q *= 3
print(min(two // 2, three))
