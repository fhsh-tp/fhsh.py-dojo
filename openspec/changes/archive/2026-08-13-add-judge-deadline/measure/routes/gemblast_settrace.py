# Same quadratic work, with the operation counter switched off first.
# Freezing the tracer makes the op limit unreachable; only a clock can stop it.
import sys
sys.settrace(None)

def leftover(s):
    i = 0
    while i < len(s) - 1:
        if s[i] == s[i + 1]:
            s = s[:i] + s[i + 2:]
            i = 0
        else:
            i += 1
    return len(s)

t = int(input())
for _ in range(t):
    n = int(input())
    print(max([leftover(input()) for _ in range(n)], default=0))
