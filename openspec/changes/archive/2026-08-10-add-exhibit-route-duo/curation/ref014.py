import sys

tokens = sys.stdin.read().split()
count = int(tokens[0])
results = []
for i in range(count):
    levels = int(tokens[1 + 2 * i])
    span = 1 << (levels - 1)
    ball = (int(tokens[2 + 2 * i]) - 1) % span
    bag = 0
    for k in range(levels - 1):
        bag = bag * 2 + ((ball >> k) & 1)
    results.append(str(bag + 1))
print("\n".join(results))
