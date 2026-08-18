rows, cols = map(int, input().split())
f = int(input())
tops = list(map(int, input().split()))
lefts = list(map(int, input().split()))
heights = list(map(int, input().split()))
widths = list(map(int, input().split()))
diff = [[0] * (cols + 2) for _ in range(rows + 2)]
for i in range(f):
    top = tops[i]
    left = lefts[i]
    bottom = top + heights[i]
    right = left + widths[i]
    diff[top][left] += 1
    diff[top][right] -= 1
    diff[bottom][left] -= 1
    diff[bottom][right] += 1
best = 0
for i in range(1, rows + 1):
    row = diff[i]
    above = diff[i - 1]
    for j in range(1, cols + 1):
        row[j] += row[j - 1] + above[j] - above[j - 1]
        if row[j] > best:
            best = row[j]
print(best)
