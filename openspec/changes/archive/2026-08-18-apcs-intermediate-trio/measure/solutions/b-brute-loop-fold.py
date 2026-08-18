import sys

data = sys.stdin.read().split()
n = int(data[0])
starts = [int(v) for v in data[1:1 + n]]
durations = [int(v) for v in data[1 + n:1 + 2 * n]]
order = sorted(range(n), key=lambda i: (starts[i], i))
room = [0] * n
ends = []
rooms_used = []
opened = 0
for i in order:
    s = starts[i]
    occupied = set()
    for j in range(len(ends)):
        if ends[j] > s: occupied.add(rooms_used[j])
    picked = 1
    while picked in occupied:
        picked += 1
    if picked > opened:
        opened = picked
    room[i] = picked
    ends.append(s + durations[i])
    rooms_used.append(picked)
print(opened)
print(' '.join(map(str, room)))
