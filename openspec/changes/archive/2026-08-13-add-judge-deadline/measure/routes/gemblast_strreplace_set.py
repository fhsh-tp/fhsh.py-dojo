# The same C-builtin str.replace bypass, spelled the way anyone would actually
# write it: only the characters present in the board are candidates, instead of
# sweeping all twenty-six letters on every pass.
#
# Measuring the clumsy spelling and concluding the route is dead is the mistake
# this file exists to avoid: a co-opted route's budget has to come from its
# cheapest reasonable spelling, not the first one that comes to mind.
def leftover(s):
    while True:
        before = s
        for c in set(s):
            s = s.replace(c + c, '')
        if s == before:
            return len(s)

t = int(input())
for _ in range(t):
    n = int(input())
    print(max([leftover(input()) for _ in range(n)], default=0))
