# V7 / E3' — lexically-patched power-encoding (coupon-combo-quote, apcs012).
#
# Co-opted route recorded in openspec/specs/expression-eval-challenges/spec.md
# ("the lexically-patched power-encoding route E3' (20/20 on apcs012,
# fuzz-verified 1200/1200)").
#
# apcs012 wants additive to bind TIGHTER than muldiv and to fold to the RIGHT,
# with parentheses overriding. '**' is Python's only right-associative operator
# above '*' and '/', so encode the additive layer onto it:
#   ' + '  ->  ' ** '     and the class's __pow__ adds
#   ' - '  ->  ' ** -'    and __neg__ negates, so a ** -b == a + (-b) == a - b
# Right-associativity then comes free from Python's own grammar, and the
# parentheses in the input are already Python parentheses.
#
# The "lexical patch" is that the substitution keys on the spaced operator, so
# an additive operator sitting directly before '(' is rewritten just like any
# other; the naive spelling that keyed on 'operator followed by a digit' left a
# bare '-' there and crashed on every parenthesised entry.
#
# Cheapest reasonable spelling (I-16): two C-level str.replace calls, one
# C-level re.sub to wrap the integers, one eval per line.
import sys
import re

WRAP = re.compile(r'\d+')


class N:
    __slots__ = ('v',)

    def __init__(self, v):
        self.v = v

    def __pow__(self, o):
        return N(self.v + o.v)

    def __neg__(self):
        return N(-self.v)

    def __mul__(self, o):
        return N(self.v * o.v)

    def __truediv__(self, o):
        return N(self.v // o.v)


data = sys.stdin.read().split('\n')
t = int(data[0])
out = []
for i in range(1, t + 1):
    src = WRAP.sub(r'N(\g<0>)', data[i]).replace(' + ', ' ** ').replace(' - ', ' ** -')
    out.append(str(eval(src).v))
print('\n'.join(out))
