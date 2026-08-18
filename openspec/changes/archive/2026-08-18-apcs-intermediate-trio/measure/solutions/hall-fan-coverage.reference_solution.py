rows, cols = map(int, input().split())
f = int(input())
tops = list(map(int, input().split()))
lefts = list(map(int, input().split()))
heights = list(map(int, input().split()))
widths = list(map(int, input().split()))
mark = [[0] * (cols + 2) for _ in range(rows + 2)]
for i in range(f):
    left = lefts[i]
    right = left + widths[i]
    for r in range(tops[i], tops[i] + heights[i]):
        line = mark[r]
        line[left] += 1
        line[right] -= 1
best = 0
for r in range(1, rows + 1):
    line = mark[r]
    running = 0
    for c in range(1, cols + 1):
        running += line[c]
        if running > best:
            best = running
print(best)
