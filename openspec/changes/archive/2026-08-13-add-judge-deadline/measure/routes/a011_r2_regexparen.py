# V12 / R2 — regex-parenthesize-then-eval (snack-bar-register, apcs011).
#
# Co-opted route recorded in openspec/specs/expression-eval-challenges/spec.md
# ("the regex-parenthesize-then-eval route (20/20 on apcs011)").
#
# apcs011 wants additive FIRST. Instead of fighting Python's precedence, bracket
# every maximal additive run so standard precedence produces the right grouping:
#   3 + 5 * 2   ->   (3 + 5) * 2
# Division is exact by the challenge's guarantee, so '/' becomes '//'.
#
# Cheapest reasonable spelling (I-16): one C-level re.sub over the whole line,
# one str.replace, one eval. No tokenizer loop in Python.
import sys
import re

RUN = re.compile(r'\d+(?: [-+] \d+)+')

data = sys.stdin.read().split('\n')
t = int(data[0])
out = []
for i in range(1, t + 1):
    src = RUN.sub(r'(\g<0>)', data[i]).replace('/', '//')
    out.append(str(eval(src)))
print('\n'.join(out))
