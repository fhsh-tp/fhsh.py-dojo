from collections import deque
t = int(input())
for _ in range(t):
    n = int(input())
    readings = [int(input()) for _ in range(n)]
    for peak_round in (True, False):
        buf = deque(readings)
        log = []
        while len(buf) > 1:
            if peak_round:
                remove_newest = buf[0] >= buf[-1]
            else:
                remove_newest = buf[0] <= buf[-1]
            if remove_newest:
                log.append(buf.pop())
            else:
                log.append(buf.popleft())
        log.append(buf[0])
        print(' '.join(map(str, log)))
