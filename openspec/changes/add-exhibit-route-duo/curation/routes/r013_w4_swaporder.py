import sys
import random


class Room:
    __slots__ = ("v", "l", "r")

    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None


def build(shape, labels, rng):
    n = len(labels)
    if n == 0:
        return None
    if shape == "single":
        return Room(labels[0])
    if shape == "lchain":
        root = Room(labels[0])
        cur = root
        for v in labels[1:]:
            cur.l = Room(v)
            cur = cur.l
        return root
    if shape == "rchain":
        root = Room(labels[0])
        cur = root
        for v in labels[1:]:
            cur.r = Room(v)
            cur = cur.r
        return root
    if shape == "zigzag":
        root = Room(labels[0])
        cur = root
        left = True
        for v in labels[1:]:
            nd = Room(v)
            if left:
                cur.l = nd
            else:
                cur.r = nd
            cur = nd
            left = not left
        return root
    if shape == "balanced":
        def rec(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            nd = Room(labels[mid])
            nd.l = rec(lo, mid - 1)
            nd.r = rec(mid + 1, hi)
            return nd
        return rec(0, n - 1)
    if shape == "caterpillar":
        # 左側主幹，每個主幹房間掛一個右側單間；深度約 n/2
        idx = 0
        root = Room(labels[idx]); idx += 1
        cur = root
        while idx < n:
            cur.r = Room(labels[idx]); idx += 1
            if idx < n:
                cur.l = Room(labels[idx]); idx += 1
                cur = cur.l
        return root
    if shape == "spine":
        # 固定長度主幹 + 隨機小叢集，深度受主幹長度控制
        spine_len = min(n, 120)
        rest = n - spine_len
        sizes = [0] * spine_len
        for i in range(rest):
            sizes[rng.randrange(spine_len)] += 1
        it = iter(labels)
        root = Room(next(it))
        cur = root
        for i in range(spine_len - 1):
            k = sizes[i]
            if k:
                sub = [next(it) for _ in range(k)]
                cur.r = build("random", sub, rng)
            nxt = Room(next(it))
            cur.l = nxt
            cur = nxt
        k = sizes[-1]
        if k:
            sub = [next(it) for _ in range(k)]
            cur.r = build("random", sub, rng)
        return root
    if shape == "leftheavy":
        # 每個房間的左側都比右側大，逼出 W4（左右展開順序顛倒）差異
        def rec(lst):
            if not lst:
                return None
            k = len(lst)
            if k == 1:
                return Room(lst[0])
            cut = max(1, (k - 1) * 3 // 4)
            nd = Room(lst[0])
            nd.l = rec(lst[1:1 + cut])
            nd.r = rec(lst[1 + cut:])
            return nd
        return rec(labels)
    # random：均勻隨機二分形狀
    def rec(lst):
        if not lst:
            return None
        k = rng.randrange(len(lst))
        nd = Room(lst[k])
        nd.l = rec(lst[:k])
        nd.r = rec(lst[k + 1:])
        return nd
    return rec(labels)


def order_a(root):
    out = []
    st = [root]
    while st:
        nd = st.pop()
        if nd is None:
            continue
        out.append(nd.v)
        st.append(nd.r)
        st.append(nd.l)
    return out


def order_b(root):
    out = []
    st = []
    cur = root
    while st or cur:
        while cur:
            st.append(cur)
            cur = cur.l
        cur = st.pop()
        out.append(cur.v)
        cur = cur.r
    return out


def order_c(root):
    out = []
    st = [(root, False)]
    while st:
        nd, done = st.pop()
        if nd is None:
            continue
        if done:
            out.append(nd.v)
        else:
            st.append((nd, True))
            st.append((nd.r, False))
            st.append((nd.l, False))
    return out


def depth(root):
    best = 0
    st = [(root, 1)]
    while st:
        nd, d = st.pop()
        if nd is None:
            continue
        if d > best:
            best = d
        st.append((nd.l, d + 1))
        st.append((nd.r, d + 1))
    return best


def _parse(text):
    tok = text.split()
    p = 0
    T = int(tok[p]); p += 1
    cases = []
    for _ in range(T):
        mode = int(tok[p]); n = int(tok[p + 1]); p += 2
        s1 = tok[p:p + n]; p += n
        s2 = tok[p:p + n]; p += n
        cases.append((mode, n, s1, s2))
    return cases


def _mode1(a, b):
    """甲＋乙 → 丙（迭代建構＋迭代輸出）。"""
    n = len(a)
    pos = {v: i for i, v in enumerate(b)}
    lch, rch = {}, {}
    idx = 0
    root = None
    st = [(0, n - 1, None, 0)]
    while st:
        lo, hi, par, side = st.pop()
        if lo > hi:
            continue
        r = a[idx]; idx += 1
        if par is None:
            root = r
        elif side == 1:
            lch[par] = r
        else:
            rch[par] = r
        m = pos[r]
        st.append((m + 1, hi, r, 2))
        st.append((lo, m - 1, r, 1))
    out = []
    st2 = [(root, False)]
    while st2:
        nd, done = st2.pop()
        if nd is None:
            continue
        if done:
            out.append(nd)
        else:
            st2.append((nd, True))
            st2.append((rch.get(nd), False))
            st2.append((lch.get(nd), False))
    return out


def _mode2(b, c):
    """乙＋丙 → 甲（自尾端消耗丙、先展開右側）。"""
    n = len(b)
    pos = {v: i for i, v in enumerate(b)}
    lch, rch = {}, {}
    idx = n - 1
    root = None
    st = [(0, n - 1, None, 0)]
    while st:
        lo, hi, par, side = st.pop()
        if lo > hi:
            continue
        r = c[idx]; idx -= 1
        if par is None:
            root = r
        elif side == 1:
            lch[par] = r
        else:
            rch[par] = r
        m = pos[r]
        st.append((lo, m - 1, r, 1))
        st.append((m + 1, hi, r, 2))
    out = []
    st2 = [root]
    while st2:
        nd = st2.pop()
        if nd is None:
            continue
        out.append(nd)
        st2.append(rch.get(nd))
        st2.append(lch.get(nd))
    return out


def route_ref(text):
    res = []
    for mode, n, s1, s2 in _parse(text):
        res.append(" ".join(_mode1(s1, s2) if mode == 1 else _mode2(s1, s2)))
    return "\n".join(res) + "\n"


def route_R1_mirror(text):
    """收編：模式 2 以「兩串反轉→套模式 1→再反轉」處理（數學上等價）。"""
    res = []
    for mode, n, s1, s2 in _parse(text):
        if mode == 1:
            res.append(" ".join(_mode1(s1, s2)))
        else:
            got = _mode1(s2[::-1], s1[::-1])
            res.append(" ".join(got[::-1]))
    return "\n".join(res) + "\n"


def route_W1_modeblind(text):
    res = []
    for mode, n, s1, s2 in _parse(text):
        res.append(" ".join(_mode1(s1, s2)))
    return "\n".join(res) + "\n"


def route_W2_postfirst(text):
    """模式 2 誤把丙的第一個元素當起點（正確為最後一個）。"""
    res = []
    for mode, n, s1, s2 in _parse(text):
        if mode == 1:
            res.append(" ".join(_mode1(s1, s2)))
            continue
        b, c = s1, s2
        n = len(b)
        pos = {v: i for i, v in enumerate(b)}
        lch, rch = {}, {}
        idx = 0
        root = None
        st = [(0, n - 1, None, 0)]
        ok = True
        while st and ok:
            lo, hi, par, side = st.pop()
            if lo > hi:
                continue
            if idx >= n:
                ok = False
                break
            r = c[idx]; idx += 1
            if par is None:
                root = r
            elif side == 1:
                lch[par] = r
            else:
                rch[par] = r
            m = pos[r]
            if not (lo <= m <= hi):
                ok = False
                break
            st.append((lo, m - 1, r, 1))
            st.append((m + 1, hi, r, 2))
        if not ok:
            res.append("")
            continue
        out = []
        st2 = [root]
        while st2:
            nd = st2.pop()
            if nd is None:
                continue
            out.append(nd)
            st2.append(rch.get(nd))
            st2.append(lch.get(nd))
        res.append(" ".join(out))
    return "\n".join(res) + "\n"


def route_W4_swaporder(text):
    """模式 2 展開順序顛倒（先左後右），子區間大小不對稱時必錯。"""
    res = []
    for mode, n, s1, s2 in _parse(text):
        if mode == 1:
            res.append(" ".join(_mode1(s1, s2)))
            continue
        b, c = s1, s2
        n = len(b)
        pos = {v: i for i, v in enumerate(b)}
        lch, rch = {}, {}
        idx = n - 1
        root = None
        st = [(0, n - 1, None, 0)]
        while st:
            lo, hi, par, side = st.pop()
            if lo > hi:
                continue
            r = c[idx]; idx -= 1
            if par is None:
                root = r
            elif side == 1:
                lch[par] = r
            else:
                rch[par] = r
            m = pos[r]
            st.append((m + 1, hi, r, 2))
            st.append((lo, m - 1, r, 1))
        out = []
        st2 = [root]
        while st2:
            nd = st2.pop()
            if nd is None:
                continue
            out.append(nd)
            st2.append(rch.get(nd))
            st2.append(lch.get(nd))
        res.append(" ".join(out))
    return "\n".join(res) + "\n"


def route_W3_sorted(text):
    """誤以為第二串（乙）必為編號排序後的結果。"""
    res = []
    for mode, n, s1, s2 in _parse(text):
        srt = sorted(s1, key=int)
        res.append(" ".join(_mode1(s1, srt) if mode == 1 else _mode2(srt, s2)))
    return "\n".join(res) + "\n"


def route_W6_firstonly(text):
    cases = _parse(text)
    if not cases:
        return "\n"
    mode, n, s1, s2 = cases[0]
    return " ".join(_mode1(s1, s2) if mode == 1 else _mode2(s1, s2)) + "\n"


def route_W5_modemarker_once(text):
    """只讀第一組的模式標記，其餘沿用。"""
    cases = _parse(text)
    if not cases:
        return "\n"
    first_mode = cases[0][0]
    res = []
    for mode, n, s1, s2 in cases:
        res.append(" ".join(_mode1(s1, s2) if first_mode == 1 else _mode2(s1, s2)))
    return "\n".join(res) + "\n"


def route_W9_revfirst(text):
    return "\n".join(" ".join(s1[::-1]) for _, _, s1, _ in _parse(text)) + "\n"


def route_W10_echosecond(text):
    return "\n".join(" ".join(s2) for _, _, _, s2 in _parse(text)) + "\n"



def sig(root):
    """忽略標號的結構簽章（括號字串），用來判斷兩組動線是否為同一形狀。"""
    out = []
    st = [(root, 0)]
    while st:
        nd, phase = st.pop()
        if nd is None:
            out.append(".")
            continue
        out.append("(")
        st.append((None, 0))
        st.append((nd.r, 0))
        st.append((nd.l, 0))
    return "".join(out)


def is_chain(root):
    """每個展區至多一條岔路＝單一路徑（退化形狀）。"""
    st = [root]
    while st:
        nd = st.pop()
        if nd is None:
            continue
        if nd.l is not None and nd.r is not None:
            return False
        st.append(nd.l)
        st.append(nd.r)
    return True


def mirror(root):
    """左右互換後的動線（用於鏡射不對稱檢查）。"""
    if root is None:
        return None
    nd = Room(root.v)
    nd.l = mirror(root.r)
    nd.r = mirror(root.l)
    return nd


def route_Z1_echo_first(text):
    return "\n".join(" ".join(s1) for _, _, s1, _ in _parse(text)) + "\n"


def route_Z2_rev_second(text):
    return "\n".join(" ".join(s2[::-1]) for _, _, _, s2 in _parse(text)) + "\n"


def route_Z3_sort_desc(text):
    return "\n".join(" ".join(sorted(s1, key=int, reverse=True)) for _, _, s1, _ in _parse(text)) + "\n"


_SHAPE_LIB = ("single", "lchain", "rchain", "zigzag", "balanced", "caterpillar", "leftheavy")


def route_W11_shapelib(text):
    """零重建路線：對每組把已知的固定形狀各生一次，用正向走訪比對後直接輸出第三串。"""
    import random as _r
    res = []
    for mode, n, s1, s2 in _parse(text):
        got = None
        for shape in _SHAPE_LIB:
            root = build(shape, list(range(n)), _r.Random(0))
            A, B, C = order_a(root), order_b(root), order_c(root)
            first, second, third = (A, B, C) if mode == 1 else (B, C, A)
            label = {}
            for slot, tok in zip(first, s1):
                label[slot] = tok
            if [label[x] for x in second] == list(s2):
                got = [label[x] for x in third]
                break
        res.append(" ".join(got) if got else "")
    return "\n".join(res) + "\n"



print(route_W4_swaporder(sys.stdin.read()), end='')
