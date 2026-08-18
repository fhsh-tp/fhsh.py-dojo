"""apcs015 基地台佈點規劃 — 語意正本（SSOT）。

情境（題面用語，不含任何演算法／資料結構術語）：
    正方形教室鋪成 k×k 格。兩台無線基地台放在**不同**的兩格。
    若兩台的相對位置（列差, 行差）落在題面列出的 8 種偏移之一，就互相干擾：
        (+1,+2) (+1,-2) (-1,+2) (-1,-2) (+2,+1) (+2,-1) (-2,+1) (-2,-1)
    輸入單一整數 n（1 <= n <= 1000），輸出 n 行，
    第 k 行為邊長 k 的教室中「兩台互不干擾」的擺法數（不分先後 = 無序配對）。

本檔提供兩份**互相獨立**的實作：

    * ``answer_line(k)`` — 封閉式：總無序配對數 C(k*k, 2) 減掉干擾配對數。
      干擾配對數 = 4*(k-1)*(k-2)（k >= 3），k < 3 時為 0。
      推導：8 種偏移分成 4 組互為相反向的配對；
        (dr,dc)=(1,2) 型可放 (k-1)*(k-2) 個無序配對，
        (dr,dc)=(1,-2) 型同樣 (k-1)*(k-2)，
        (dr,dc)=(2,1) 型 (k-2)*(k-1)，(2,-1) 型 (k-2)*(k-1)，
      合計 4*(k-1)*(k-2)。

    * ``answer_line_bruteforce(k)`` — 真的枚舉所有格子對（O(k^4) 的定義式，
      對每一對不同格子檢查 (dr,dc) 是否落在 8 種偏移中）。
      這是公式正確性的**獨立驗證**，不是任何一條解題路線。

兩者在 k <= 30 必須逐項相符，由 ``cross_check()`` 與斷言牆強制。
"""

OFFSETS = (
    (1, 2), (1, -2), (-1, 2), (-1, -2),
    (2, 1), (2, -1), (-2, 1), (-2, -1),
)

# n 上界 1000 是成本閘決議，不是美觀取捨：n=3000 時同一條 O(n^2) 演算法的三種
# 自然寫法落在 op 上限兩側（1,008 萬 / 1,357 萬 / 2,256 萬），學生想法相同卻因
# 寫法生死不同。n=1000 時三者實測 1,008,011 / 1,510,511 / 2,509,512 op，最貴者
# 餘裕 3.98 倍。出處 measure/opprobe_015_nbound.py。
N_MIN, N_MAX = 1, 1000


# ── 封閉式（正解／generator 用） ──────────────────────────────────────
def answer_line(k):
    """邊長 k 的教室中互不干擾的無序擺法數。"""
    return k * k * (k * k - 1) // 2 - (4 * (k - 1) * (k - 2) if k >= 3 else 0)


def solve(n):
    """完整輸出：n 行，第 k 行為 answer_line(k)。回傳字串（結尾含換行）。"""
    return "".join("%d\n" % answer_line(k) for k in range(1, n + 1))


# ── 獨立慢速參照（枚舉每一對格子；只用於交叉驗證） ────────────────────
def answer_line_bruteforce(k):
    """把 k*k 格全部攤平，枚舉所有無序格子對，逐對檢查是否落在 8 種偏移。"""
    cells = [(r, c) for r in range(k) for c in range(k)]
    total = 0
    m = len(cells)
    for i in range(m):
        r1, c1 = cells[i]
        for j in range(i + 1, m):
            r2, c2 = cells[j]
            if (r2 - r1, c2 - c1) in OFFSETS:
                continue
            total += 1
    return total


def solve_bruteforce(n):
    return "".join("%d\n" % answer_line_bruteforce(k) for k in range(1, n + 1))


def cross_check(limit=30):
    """公式 vs 枚舉，k = 1..limit 全部逐項比對。回傳不符的 k 清單（空 = 全對）。"""
    bad = []
    for k in range(1, limit + 1):
        if answer_line(k) != answer_line_bruteforce(k):
            bad.append(k)
    return bad


# ── 測資 I/O 渲染 ────────────────────────────────────────────────────
def render_input(n):
    return "%d\n" % n


def render_expected(n):
    return solve(n).rstrip("\n")


# 題面範例（n = 8）的前 8 項，供斷言牆釘死
SAMPLE_N = 8
SAMPLE_EXPECTED = [0, 6, 28, 96, 252, 550, 1056, 1848]


if __name__ == "__main__":
    bad = cross_check(30)
    print("cross_check(30) 不符的 k：", bad if bad else "（無，全數相符）")
    print("前 8 項：", [answer_line(k) for k in range(1, 9)])
    assert not bad
    assert [answer_line(k) for k in range(1, 9)] == SAMPLE_EXPECTED
    print("semantics015 自檢通過。")
