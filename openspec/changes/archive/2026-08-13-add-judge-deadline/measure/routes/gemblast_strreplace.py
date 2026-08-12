# The C-builtin bypass this challenge's spec records as an accepted alternative
# solution: the quadratic work is delegated to str.replace, which the tracer
# cannot see. Its wall clock is what decides whether that acceptance survives.
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def leftover(s):
    while True:
        before = s
        for c in ALPHABET:
            s = s.replace(c + c, '')
        if s == before:
            return len(s)

t = int(input())
for _ in range(t):
    n = int(input())
    print(max([leftover(input()) for _ in range(n)], default=0))
