import heapq
q = int(input())
periods = list(map(int, input().split()))
k = int(input())
h = [(periods[i], i + 1, periods[i]) for i in range(q)]
heapq.heapify(h)
out = []
for _ in range(k):
    t, idx, p = heapq.heappop(h)
    out.append(idx)
    heapq.heappush(h, (t + p, idx, p))
print('\n'.join(map(str, out)))
