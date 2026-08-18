import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    starts = [int(v) for v in data[1:1 + n]]
    durations = [int(v) for v in data[1 + n:1 + 2 * n]]

    order = sorted(range(n), key=lambda i: (starts[i], i))
    # last_end[r] = 第 r+1 號教室目前登記到的最後結束分鐘
    last_end = []
    room = [0] * n

    for i in order:
        s = starts[i]
        picked = -1
        for r in range(len(last_end)):
            if last_end[r] <= s:
                picked = r
                break
        if picked < 0:
            last_end.append(0)
            picked = len(last_end) - 1
        last_end[picked] = s + durations[i]
        room[i] = picked + 1

    print(len(last_end))
    print(' '.join(str(v) for v in room))


main()
