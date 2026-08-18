import sys


def share(value, unit):
    total = 0
    current = value
    while current >= unit:
        current, _ = divmod(current, unit)
        total += current
    return total


amount = int(sys.stdin.read().split()[0])
threes = share(amount, 3)
twos = share(amount, 2)
print(threes if threes * 2 <= twos else twos // 2)
