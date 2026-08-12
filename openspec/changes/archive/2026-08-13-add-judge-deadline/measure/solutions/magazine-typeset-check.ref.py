import sys

def first_error(line):
    close_of = {"(": ")", "[": "]", "{": "}"}
    kinds = []
    positions = []
    for i in range(len(line)):
        ch = line[i]
        if ch in "([{":
            kinds.append(ch)
            positions.append(i + 1)
        elif ch in ")]}":
            if not kinds or close_of[kinds[-1]] != ch:
                return i + 1
            kinds.pop()
            positions.pop()
    if positions:
        return positions[0]
    return 0

data = sys.stdin.read().splitlines()
t = int(data[0])
out = [str(first_error(data[i])) for i in range(1, t + 1)]
print("\n".join(out))
