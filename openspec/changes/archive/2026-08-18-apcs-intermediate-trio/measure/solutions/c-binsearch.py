n = int(input())
songs = list(map(int, input().split()))
best = 0
for i in range(n):
    lo = 0
    hi = n - i
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if len(set(songs[i:i + mid])) == mid:
            lo = mid
        else:
            hi = mid - 1
    if lo > best:
        best = lo
print(best)
