# V3 / E1 — operator-swap dunder eval (snack-bar-register, apcs011).
#
# Co-opted route recorded in openspec/specs/expression-eval-challenges/spec.md
# ("the operator-swap dunder eval (20/20 on apcs011)").
#
# apcs011 wants additive FIRST (left-assoc), then muldiv (left-assoc). Python's
# precedence is the other way round, so swap the operator SYMBOLS to borrow
# Python's grouping, and let a wrapper class perform the intended arithmetic:
#   text  '+' -> '*'   and the class's __mul__ adds
#   text  '-' -> '/'   and the class's __truediv__ subtracts
#   text  '*' -> '+'   and the class's __add__ multiplies
#   text  '/' -> '-'   and the class's __sub__ divides exactly
# Both Python levels are left-associative, which matches the challenge.
#
# Cheapest reasonable spelling (I-16): one C-level str.translate for the swap,
# one C-level re.sub to wrap the integers, one eval per line. No hand-written
# parser, no per-character Python loop.
import sys
import re


class N:
    __slots__ = ('v',)

    def __init__(self, v):
        self.v = v

    def __mul__(self, o):
        return N(self.v + o.v)

    def __truediv__(self, o):
        return N(self.v - o.v)

    def __add__(self, o):
        return N(self.v * o.v)

    def __sub__(self, o):
        return N(self.v // o.v)


SWAP = str.maketrans('+-*/', '*/+-')
WRAP = re.compile(r'\d+')

data = sys.stdin.read().split('\n')
t = int(data[0])
out = []
for i in range(1, t + 1):
    src = WRAP.sub(r'N(\g<0>)', data[i].translate(SWAP))
    out.append(str(eval(src).v))
print('\n'.join(out))
