def leftover(board):
    buf = [""] * len(board)
    top = -1
    for c in board:
        if top >= 0 and buf[top] == c:
            top -= 1
        else:
            top += 1
            buf[top] = c
    return top + 1

t = int(input())
for _ in range(t):
    n = int(input())
    counts = [leftover(input()) for _ in range(n)]
    print(max(counts, default=0))
