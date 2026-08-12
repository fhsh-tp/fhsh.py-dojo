import heapq
m = int(input())
n = int(input())
times = list(map(int, input().split()))
h = [(0, i) for i in range(m)]
heapq.heapify(h)
for t in times:
    ft, i = heapq.heappop(h)
    heapq.heappush(h, (ft + t, i))
print(max(ft for ft, _ in h))
