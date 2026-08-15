"""apcs017 園遊會代幣兌換 — 語意正本（SSOT）。

情境（頁面用語，不得出現任何資料結構／演算法術語）：
    n 位同學排成一列，所有「不同的排隊順序」共有幾種，就是第 1 級代幣的枚數 N。
    兌換規則：12 枚同級代幣換 1 枚上一級代幣，而且**必須一次把手上該級的代幣
    全部換掉、一枚零頭都不能剩**；只要分不完整批就換不了，兌換到此為止。
    輸出總共成功往上換了幾級（第 1 級不算）。

數學（僅存在於本檔與 curation 內部，頁面上不得出現）：
    N = n!，答案 = 「12 能整除 N 幾次」。12 = 2^2 x 3，故
        答案 = min(v2 // 2, v3)，其中 vp = sum_{i>=1} floor(n / p^i)
    v2 / v3 各自的和項在 p^i > n 之後全為 0，迴圈長度 O(log_p n)。

本檔提供兩條互相交叉驗證的實作：
    * exchanges_formula(n)  — 公式版，對 1 <= n <= 10^9 全域可用（正解）
    * exchanges_bruteforce(n) — 真的把 n! 算出來再反覆整除 12（只允許 n <= 400）
兩者在 n = 1..299（含）逐一比對必須零誤差，這是 G1 的機械證據。
"""

import math

MAX_N = 1_000_000_000          # 題面輸入上界
BRUTE_MAX_N = 400              # 暴力參照的硬性使用上限（再大就開始以秒計）


# ── 正解 ────────────────────────────────────────────────────────────
def legendre(n, p):
    """vp(n!) = sum_{i>=1} floor(n / p^i)。"""
    total = 0
    q = p
    while q <= n:
        total += n // q
        q *= p
    return total


def exchanges_formula(n):
    """正解：min(v2 // 2, v3)。"""
    return min(legendre(n, 2) // 2, legendre(n, 3))


# ── 暴力參照（語意的最直白定義） ──────────────────────────────────
def exchanges_bruteforce(n):
    """把 n! 真的算出來，再反覆「整批換掉」——只要除不盡就停。

    這就是題面規則的逐字翻譯：每一輪必須整除，餘數不為 0 就換不了。
    成本 ∝ n! 的位數平方，n > 400 會慢到不可用，故加硬性守門。
    """
    if n > BRUTE_MAX_N:
        raise ValueError("暴力參照只允許 n <= %d（實際 %d）" % (BRUTE_MAX_N, n))
    tokens = math.factorial(n)
    levels = 0
    while tokens % 12 == 0:
        tokens //= 12
        levels += 1
    return levels


# ── 誤解路線的語意（供斷言牆機械化檢查，不是給學生的） ────────────
def wrong_decimal_tail(n):
    """十進位尾零規則：以為「每 5 一數」——實際上算的是 n! 尾端有幾個 0。"""
    return legendre(n, 5)


def wrong_forgot_half(n):
    """忘記一批 12 需要兩個 2：min(v2, v3)。"""
    return min(legendre(n, 2), legendre(n, 3))


def wrong_only_v3(n):
    """只看 3 的部分。"""
    return legendre(n, 3)


def wrong_only_half_v2(n):
    """只看 2 的部分、忘了取 min。"""
    return legendre(n, 2) // 2


# ── 渲染 ────────────────────────────────────────────────────────────
def render_input(n):
    return "%d\n" % n


def render_expected(n):
    return "%d\n" % exchanges_formula(n)


ROUTE_SEMANTICS = {
    "R_reference": exchanges_formula,
    "W1_decimal_tail": wrong_decimal_tail,
    "W2_forgot_half": wrong_forgot_half,
    "W3_only_v3": wrong_only_v3,
    "W4_only_half_v2": wrong_only_half_v2,
}


def _selftest():
    """G1：公式版 vs 暴力參照，n = 1..299 零誤差。"""
    bad = []
    for n in range(1, 300):
        a = exchanges_formula(n)
        b = exchanges_bruteforce(n)
        if a != b:
            bad.append((n, a, b))
    head = [exchanges_formula(n) for n in range(1, 16)]
    print("n=1..15 ->", ",".join(map(str, head)))
    print("n=1..299 公式 vs 暴力 不一致筆數 =", len(bad))
    if bad:
        print("  前 10 筆不一致：", bad[:10])
        return 1
    # 答案為 0 的最大 n（機械求出，不憑記憶）
    zero_max = max(n for n in range(1, 500) if exchanges_formula(n) == 0)
    print("答案為 0 的最大 n =", zero_max,
          "（n=%d -> %d，n=%d -> %d）" % (zero_max, exchanges_formula(zero_max),
                                          zero_max + 1, exchanges_formula(zero_max + 1)))
    print("n=1000000000 ->", exchanges_formula(MAX_N))
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
