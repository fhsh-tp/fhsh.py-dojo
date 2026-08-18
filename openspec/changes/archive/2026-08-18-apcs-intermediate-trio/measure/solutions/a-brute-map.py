from itertools import repeat
from operator import add

rows, cols = map(int, input().split())
f = int(input())
tops = list(map(int, input().split()))
lefts = list(map(int, input().split()))
heights = list(map(int, input().split()))
widths = list(map(int, input().split()))
grid = [[0] * (cols + 2) for _ in range(rows + 2)]
for i in range(f):
    r0 = tops[i]
    c0 = lefts[i]
    r1 = r0 + heights[i]
    c1 = c0 + widths[i]
    for r in range(r0, r1):
        row = grid[r]
        row[c0:c1] = map(add, row[c0:c1], repeat(1))
best = 0
for r in range(1, rows + 1):
    m = max(grid[r])
    if m > best:
        best = m
print(best)
