"""apcs016 跑馬燈顯示計數 — 語義正本（SSOT）。

情境：看板有 n 格燈，每格只有「亮」與「暗」兩種狀態；其中 k 格的燈泡已經燒壞，
永遠只能是暗的。問整面看板總共有幾種不同的畫面（答案對 1000000007 取餘數）。

語義：燒壞的 k 格畫面固定，剩下 n − k 格各自獨立有 2 種樣子，
      因此畫面數 = 2^(n − k)，k = n 時為 1（唯一畫面：整面全暗）。

本檔提供三種互為交叉驗證的來源：
  * answer()      — 出貨語義（三參數 pow，O(log(n−k))）
  * answer_loop() — 逐次乘 2 取餘數（O(n−k)），獨立於 pow 的實作
  * brute_count() — **真的把每一種畫面列舉出來**再數（只能跑 n <= 20）

brute_count 是「答案是什麼」的最終仲裁：它不預設任何公式，
只把 n 格的所有狀態組合走一遍，濾掉燒壞格被點亮的組合，數出相異畫面數。
"""

MOD = 1000000007
BRUTE_MAX_N = 20  # 2^20 = 1,048,576 個組合，再大就跑不動


def answer(n, k):
    """出貨語義：2^(n−k) mod 1000000007。"""
    return pow(2, n - k, MOD)


def answer_loop(n, k):
    """獨立實作：逐次乘 2 取餘數（不呼叫 pow 的三參數形式）。"""
    r = 1
    for _ in range(n - k):
        r = r * 2 % MOD
    return r


def brute_count(n, k, broken=None):
    """真的列舉所有畫面再數，只能跑 n <= BRUTE_MAX_N。

    broken：燒壞格的 0-based 索引集合，省略時取前 k 格。
    畫面以長度 n 的 0/1 tuple 表示（1 = 亮）；燒壞格被點亮的組合不是合法畫面。
    """
    if n > BRUTE_MAX_N:
        raise ValueError("brute_count 只支援 n <= %d（收到 n = %d）" % (BRUTE_MAX_N, n))
    if broken is None:
        broken = set(range(k))
    broken = set(broken)
    assert len(broken) == k and all(0 <= b < n for b in broken)

    seen = set()
    for mask in range(1 << n):
        picture = tuple((mask >> i) & 1 for i in range(n))
        if any(picture[b] for b in broken):
            continue  # 燒壞的格子不可能是亮的，這不是一個做得出來的畫面
        seen.add(picture)
    return len(seen) % MOD


def parse(text):
    """把一筆測資的 stdin 原文解析成 (n, k)。"""
    n, k = text.split()
    return int(n), int(k)


def render_input(n, k):
    return "%d %d\n" % (n, k)


def render_expected(n, k):
    return "%d\n" % answer(n, k)


# ── 錯誤／參照路線的純函式版本（斷言牆用，與 routes/*.py 一一對應）──────────
def r_ignore_k(n, k):
    """忽略燒壞的格子，直接算 2^n。"""
    return pow(2, n, MOD)


def r_use_k(n, k):
    """把自由度看成 k 而不是 n − k。"""
    return pow(2, k, MOD)


def r_plain_diff(n, k):
    """直接把 n − k 當答案。"""
    return n - k


def r_bigint(n, k):
    """先算大整數 2^(n−k) 再取餘數（收編路線，答案正確）。"""
    return (2 ** (n - k)) % MOD


def r_nomod(n, k):
    """忘記取餘數：輸出完整的大整數（大 n 時是天文數字）。"""
    return 2 ** (n - k)


ROUTES = {
    "REF_pow3": answer,
    "A1_loop": answer_loop,
    "A2_bigint": r_bigint,
    "W1_ignore_k": r_ignore_k,
    "W2_use_k": r_use_k,
    "W3_plain_diff": r_plain_diff,
    "W4_nomod": r_nomod,
}


def _selftest():
    """三來源交叉驗證：公式、逐次乘法、真正的列舉，三者必須相符。"""
    checked = 0
    for n in range(1, 15):
        for k in range(0, n + 1):
            a = answer(n, k)
            b = answer_loop(n, k)
            c = brute_count(n, k)
            assert a == b == c, (n, k, a, b, c)
            checked += 1
    # 燒壞格不在開頭時，答案不變（畫面數只取決於還會動的格數）
    for n, k, broken in [(6, 2, {1, 4}), (7, 3, {0, 3, 6}), (5, 4, {1, 2, 3, 4})]:
        assert brute_count(n, k, broken) == answer(n, k), (n, k, broken)
        checked += 1
    # k = n 的邊界：整面只剩一種畫面
    for n in (1, 4, 9, 20):
        assert answer(n, n) == 1 and brute_count(n, n) == 1, n
        checked += 1
    return checked


if __name__ == "__main__":
    print("交叉驗證通過，共 %d 組 (n, k)（公式 == 逐次乘法 == 真正列舉）" % _selftest())
