# ACCEPTED ALTERNATIVE：自己產生資料點後插值外推。
#
# 這條路線完全不看題面提供的任何答案，也不從干擾偏移表推導任何幾何：
# 對 k = 1..5 直接暴力枚舉出五個資料點（每個只有幾百次配對比較），
# 再用這五個點做多項式插值，外推到題目要求的每個 k。
#
# 它之所以會成立，是因為第 k 列答案在整個定義域上恰好是 k 的四次多項式，
# 而四次多項式被五個點唯一決定。2026-08-15 的稽核指出這條路線，實測 20/20。
#
# 重要：題面改動**堵不住**這條路線。本檔刻意不讀題面的答案表或範例輸出，
# 就是為了證明這一點——縮小或刪除題面給的數字對它毫無影響。
import sys
from fractions import Fraction

INTERFERING = (
    (1, 2), (1, -2), (-1, 2), (-1, -2),
    (2, 1), (2, -1), (-2, 1), (-2, -1),
)

SAMPLE_K = 5  # 四次多項式需要五個點


def brute(side):
    """暴力枚舉邊長 side 的答案。只在 side <= 5 使用，成本可忽略。"""
    cells = [(r, c) for r in range(side) for c in range(side)]
    bad = 0
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            dr = cells[j][0] - cells[i][0]
            dc = cells[j][1] - cells[i][1]
            if (dr, dc) in INTERFERING or (-dr, -dc) in INTERFERING:
                bad += 1
    total = len(cells) * (len(cells) - 1) // 2
    return total - bad


POINTS = [(k, brute(k)) for k in range(1, SAMPLE_K + 1)]


def interpolate(k):
    """拉格朗日插值。用 Fraction 保證整數答案不受浮點誤差影響。"""
    acc = Fraction(0)
    for i, (xi, yi) in enumerate(POINTS):
        term = Fraction(yi)
        for j, (xj, _) in enumerate(POINTS):
            if i != j:
                term *= Fraction(k - xj, xi - xj)
        acc += term
    return int(acc)


n = int(sys.stdin.readline())
sys.stdout.write("\n".join(str(interpolate(k)) for k in range(1, n + 1)))
