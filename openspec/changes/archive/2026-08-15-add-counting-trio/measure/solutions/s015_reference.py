import sys


def blocked(side):
    # 逐列累加：把「比較上面那一格」所在的列當主軸，一列一列加上去。
    bad = 0
    for _top in range(side - 1):
        bad += 2 * (side - 2)
    for _top in range(side - 2):
        bad += 2 * (side - 1)
    return bad


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    out = []
    for side in range(1, n + 1):
        spots = side * side
        out.append(str(spots * (spots - 1) // 2 - blocked(side)))
    print("\n".join(out))


main()
