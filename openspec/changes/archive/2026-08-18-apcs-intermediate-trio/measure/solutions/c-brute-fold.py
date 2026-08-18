n = int(input())
songs = list(map(int, input().split()))
best = 0
for i in range(n):
    seen = set(); j = i
    while j < n and songs[j] not in seen: seen.add(songs[j]); j += 1
    if j - i > best: best = j - i
print(best)
