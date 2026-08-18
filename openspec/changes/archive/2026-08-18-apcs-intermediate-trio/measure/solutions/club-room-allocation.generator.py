import heapq
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    starts = [int(v) for v in data[1:1 + n]]
    durations = [int(v) for v in data[1 + n:1 + 2 * n]]

    order = sorted(range(n), key=lambda i: (starts[i], i))
    busy = []          # (結束分鐘, 教室編號)，以結束分鐘為鍵的最小堆
    idle = []          # 目前空著的教室編號，最小堆
    opened = 0
    room = [0] * n

    for i in order:
        s = starts[i]
        while busy and busy[0][0] <= s:
            _, freed = heapq.heappop(busy)
            heapq.heappush(idle, freed)
        if idle:
            picked = heapq.heappop(idle)
        else:
            opened += 1
            picked = opened
        room[i] = picked
        heapq.heappush(busy, (s + durations[i], picked))

    out = [str(opened), ' '.join(str(v) for v in room)]
    sys.stdout.write('\n'.join(out) + '\n')


main()
