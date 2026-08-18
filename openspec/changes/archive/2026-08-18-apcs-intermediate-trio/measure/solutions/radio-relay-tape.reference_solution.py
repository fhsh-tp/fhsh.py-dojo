n = int(input())
songs = list(map(int, input().split()))
next_seen = {}
limit = n
best = 0
for start in range(n - 1, -1, -1):
    song = songs[start]
    following = next_seen.get(song)
    if following is not None and following < limit:
        limit = following
    next_seen[song] = start
    span = limit - start
    if span > best:
        best = span
print(best)
