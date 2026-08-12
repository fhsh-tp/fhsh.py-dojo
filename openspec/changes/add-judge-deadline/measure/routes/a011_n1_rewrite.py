# V11 / N1 — C-level rewrite loop (snack-bar-register, apcs011).
#
# Co-opted route recorded in openspec/specs/expression-eval-challenges/spec.md
# ("C-level rewrite loops"), described in the archived design as "correct but
# O(n^2) at the C level".
#
# Collapse the leftmost additive pair over and over until none is left, then do
# the same for muldiv. Each pass is a whole-line regex scan, so the work is
# quadratic in line length but every scan runs inside C.
#
# Cheapest reasonable spelling (I-16): re.subn with count=1 (leftmost match ->
# left-associative for free) and an early exit on n == 0. No manual index
# arithmetic, no token list rebuilt in Python.
import sys
import re

ADD = re.compile(r'(-?\d+) ([-+]) (-?\d+)')
MUL = re.compile(r'(-?\d+) ([*/]) (-?\d+)')


def fold_add(m):
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    return str(a + b if op == '+' else a - b)


def fold_mul(m):
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    return str(a * b if op == '*' else a // b)


data = sys.stdin.read().split('\n')
t = int(data[0])
out = []
for i in range(1, t + 1):
    s = data[i]
    while True:
        s, n = ADD.subn(fold_add, s, count=1)
        if not n:
            break
    while True:
        s, n = MUL.subn(fold_mul, s, count=1)
        if not n:
            break
    out.append(s)
print('\n'.join(out))
