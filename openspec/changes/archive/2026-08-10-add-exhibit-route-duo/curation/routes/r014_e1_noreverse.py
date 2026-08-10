import sys

def bag_parity(D, I):
    """O(D) 奇偶直推（generator 用）。對任意 I 成立。"""
    I = (I - 1) % (1 << (D - 1)) + 1
    node = 1
    for _ in range(D - 1):
        if I % 2 == 1:
            node = node * 2
            I = (I + 1) // 2
        else:
            node = node * 2 + 1
            I = I // 2
    return node - (1 << (D - 1)) + 1


def bag_simulate(D, I):
    """逐球全模擬（語義最直白的定義；成本 ∝ I，只用於交叉驗證）。"""
    half = 1 << (D - 1)
    flip = [0] * half
    node = 1
    for _ in range(I):
        node = 1
        while node < half:
            f = flip[node]
            flip[node] = 1 - f
            node = node * 2 + f
    return node - half + 1


def bag_reversed(D, I):
    """把 (I−1) 在 D−1 位下反向讀取（reference_solution 用）。"""
    x = (I - 1) % (1 << (D - 1))
    out = 0
    for k in range(D - 1):
        out = out * 2 + ((x >> k) & 1)
    return out + 1


def steps(D, I):
    """逐球模擬的下降步數＝球數 ×(D−1)。"""
    return (D - 1) * I


def balls(D, I):
    """逐球模擬至少要碰的球數（任何『逐球』寫法的 op 下界基準）。"""
    return I


def render_input(cases):
    return "\n".join([str(len(cases))] + ["%d %d" % (D, I) for D, I in cases]) + "\n"


def render_expected(cases):
    return "\n".join(str(bag_parity(D, I)) for D, I in cases) + "\n"


# ── 路線實作（吃 raw input 文字、吐 output 文字）────────────────────────────

def _parse(text):
    tok = text.split()
    T = int(tok[0])
    return [(int(tok[1 + 2 * i]), int(tok[2 + 2 * i])) for i in range(T)]


def _emit(fn):
    def run(text):
        return "\n".join(str(fn(D, I)) for D, I in _parse(text)) + "\n"
    return run


route_ref = _emit(bag_parity)
route_reversed = _emit(bag_reversed)


def route_P1_periodic_sim(text):
    """收編：先用週期把球數縮到一個週期內，再逐球模擬。"""
    out = []
    for D, I in _parse(text):
        out.append(str(bag_simulate(D, (I - 1) % (1 << (D - 1)) + 1)))
    return "\n".join(out) + "\n"


def route_L1_levelwise(text):
    """收編：逐層計數 O(2^D)，語義正確但踩滿整台機器（顯式 if/else 寫法）。"""
    res = []
    for D, I in _parse(text):
        cnt = [0] * (1 << D)
        cnt[1] = I
        for v in range(1, 1 << (D - 1)):
            c = cnt[v]
            if c % 2 == 0:
                cnt[2 * v] = c // 2
                cnt[2 * v + 1] = c // 2
            else:
                cnt[2 * v] = (c + 1) // 2
                cnt[2 * v + 1] = c // 2
        node = 1
        for _ in range(D - 1):
            node = node * 2 if cnt[node] % 2 == 1 else node * 2 + 1
        res.append(str(node - (1 << (D - 1)) + 1))
    return "\n".join(res) + "\n"


# ── 零洞察／誤解路線 ───────────────────────────────────────────────────────

route_Z1_echo_I = _emit(lambda D, I: I)
route_Z2_const1 = _emit(lambda D, I: 1)
route_Z3_maxbag = _emit(lambda D, I: 1 << (D - 1))
route_E1_noreverse = _emit(lambda D, I: (I - 1) % (1 << (D - 1)) + 1)
route_E2_zerobased = _emit(lambda D, I: bag_parity(D, I) - 1)
route_E3_flippernum = _emit(lambda D, I: bag_parity(D, I) + (1 << (D - 1)) - 1)


def _parity_flipped(D, I):
    I = (I - 1) % (1 << (D - 1)) + 1
    node = 1
    for _ in range(D - 1):
        if I % 2 == 1:
            node = node * 2 + 1
            I = (I + 1) // 2
        else:
            node = node * 2
            I = I // 2
    return node - (1 << (D - 1)) + 1


def _dlevels(D, I):
    I = (I - 1) % (1 << (D - 1)) + 1
    node = 1
    for _ in range(D):
        if I % 2 == 1:
            node = node * 2
            I = (I + 1) // 2
        else:
            node = node * 2 + 1
            I = I // 2
    return node - (1 << D) + 1


route_E4_parityflip = _emit(_parity_flipped)
route_E5_dlevels = _emit(_dlevels)


def route_E6_firstonly(text):
    cases = _parse(text)
    if not cases:
        return "\n"
    D, I = cases[0]
    return str(bag_parity(D, I)) + "\n"




print(route_E1_noreverse(sys.stdin.read()), end='')
