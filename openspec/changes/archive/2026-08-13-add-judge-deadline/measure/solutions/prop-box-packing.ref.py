import sys

def check(line):
    match = {"(": ")", "[": "]", "{": "}"}
    stack_idx = []
    for i, ch in enumerate(line):
        if ch in match:
            stack_idx.append(i)
        else:
            if not stack_idx or match[line[stack_idx[-1]]] != ch:
                return "NG"
            stack_idx.pop()
    return "OK" if not stack_idx else "NG"

data = sys.stdin.read().splitlines()
t = int(data[0])
print("\n".join(check(data[i]) for i in range(1, t + 1)))
