# ACCEPTED：同一個式子的另一種寫法——先算 3 的份額，再用 divmod 折半 2 的份額。
import sys
n = int(sys.stdin.readline())
three = 0
q = 3
while q <= n:
    three += n // q
    q *= 3
two = 0
q = 2
while q <= n:
    two += n // q
    q *= 2
pairs, _ = divmod(two, 2)
print(three if three < pairs else pairs)
