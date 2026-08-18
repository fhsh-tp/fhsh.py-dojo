n = int(input())
songs = list(map(int, input().split()))
last_seen = {}
left = 0
best = 0
for right in range(n):
    song = songs[right]
    previous = last_seen.get(song, -1)
    if previous >= left:
        left = previous + 1
    last_seen[song] = right
    length = right - left + 1
    if length > best:
        best = length
print(best)
