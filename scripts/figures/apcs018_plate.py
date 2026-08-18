"""Draw the apcs018 fan plate: `docs/public/assets/challenge/apcs018/圖一.png`.

    zsh scripts/figures/apcs018_plate.sh

Three panels, top to bottom, and the order is the argument:

  A  the floor as a 4×5 grid with the three fans' rectangles laid over it and
     every cell carrying the number of fans that reach it — this is *what the
     answer is*
  B  the same floor with nothing on it but twelve corner marks, four per fan,
     each sitting exactly where the generator writes it
  C  the two sweeps that turn those twelve marks back into panel A's table

The whole plate exists to put "fill every cell" and "touch four corners" side
by side at the same scale, so the reader can count the marks and see that the
second number does not grow with the rectangle.

**The numbers are not drawn by hand.** `LITERAL` below is the challenge's own
worked example, copied verbatim from `testcase_plan[0]`, and every table in the
plate is computed from it at build time; `_self_check()` compares the result
against the table printed in 〈範例說明〉 and refuses to emit a plate that
disagrees. A drawing that is merely pretty and wrong is worse than no drawing.

**Why 1280 wide and portrait.** The challenge page puts the problem text in a
fixed left pane — 643 CSS px on a 1728 px desktop — so the canvas is authored
at 1280 and displayed at ~640, i.e. exactly 2×, and no glyph is set below 24 px
so nothing drops under 12 px on screen. The floor is asserted at the bottom of
this file: the constraint is the column, not taste.
"""

import base64
import pathlib

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/canvas-design/canvas-fonts"

W, H = 1280, 2716
MIN_TYPE = 24          # nothing smaller: 24 authored px = 12 px on screen

# --- palette: paper, ink, and three hues out of the same soil ---------------
PAPER = "#F3EFE4"
INK = "#1A1813"
INK_SOFT = "#6E675A"
FLOOR = "#E7E0CC"
ROOM = "#FCFAF3"
FAN_COLS = ["#B4532A", "#2C6E63", "#3D4A7A"]   # 第 1／2／3 台

# --- the worked example, verbatim from the challenge's testcase_plan[0] -----
LITERAL = """4 5
3
1 2 1
1 2 3
2 2 3
3 3 2"""

_lines = LITERAL.splitlines()
ROWS, COLS = map(int, _lines[0].split())
F = int(_lines[1])
_tops = list(map(int, _lines[2].split()))
_lefts = list(map(int, _lines[3].split()))
_hs = list(map(int, _lines[4].split()))
_ws = list(map(int, _lines[5].split()))
FANS = list(zip(_tops, _lefts, _hs, _ws))       # (top, left, height, width)

# The table printed in 〈範例說明〉. The plate is checked against it, not the
# other way round.
EXPECT = [
    [1, 1, 2, 1, 0],
    [1, 2, 3, 2, 0],
    [0, 1, 2, 2, 0],
    [0, 0, 0, 0, 0],
]
EXPECT_BEST = 3
HOT = (2, 3)            # 第 2 列第 3 行 — the cell all three fans reach


def blank():
    return [[0] * (COLS + 1) for _ in range(ROWS + 1)]


def brute():
    """Panel A: fill every covered cell, one fan at a time. The slow way."""
    g = blank()
    for top, left, h, w in FANS:
        for r in range(top, top + h):
            for c in range(left, left + w):
                g[r][c] += 1
    return g


def corner_marks():
    """Panel B: four marks per fan, at the same indices the generator uses.

    `bottom` and `right` are one past the covered range, so three of the four
    marks land *outside* the rectangle — that offset is the whole trick and it
    is drawn, not explained.
    """
    marks = {}
    for i, (top, left, h, w) in enumerate(FANS):
        bottom, right = top + h, left + w
        for (r, c), sign in (((top, left), +1), ((top, right), -1),
                             ((bottom, left), -1), ((bottom, right), +1)):
            marks.setdefault((r, c), []).append((sign, i))
    return marks


def sweep(marks):
    """Panel C: the two passes. Returns (after rows, after columns)."""
    g = blank()
    for (r, c), items in marks.items():
        for sign, _ in items:
            g[r][c] += sign
    a = blank()
    for r in range(1, ROWS + 1):
        run = 0
        for c in range(1, COLS + 1):
            run += g[r][c]
            a[r][c] = run
    b = blank()
    for c in range(1, COLS + 1):
        run = 0
        for r in range(1, ROWS + 1):
            run += a[r][c]
            b[r][c] = run
    return a, b


COVER = brute()
MARKS = corner_marks()
ROW_SUM, RESTORED = sweep(MARKS)


def _self_check():
    """Everything printed on the plate is derived, so the derivation is what
    has to be checked — against the challenge text, not against taste."""
    got = [[COVER[r][c] for c in range(1, COLS + 1)] for r in range(1, ROWS + 1)]
    if got != EXPECT:
        raise SystemExit(f"coverage table is {got}, 範例說明 says {EXPECT}")
    back = [[RESTORED[r][c] for c in range(1, COLS + 1)] for r in range(1, ROWS + 1)]
    if back != EXPECT:
        raise SystemExit(f"the two sweeps restore {back}, which is not the coverage table")
    best = max(max(row) for row in got)
    if best != EXPECT_BEST:
        raise SystemExit(f"the plate's answer is {best}, the challenge says {EXPECT_BEST}")
    if got[HOT[0] - 1][HOT[1] - 1] != EXPECT_BEST:
        raise SystemExit(f"cell {HOT} does not hold the answer")
    if sum(len(v) for v in MARKS.values()) != 4 * F:
        raise SystemExit("a fan did not contribute exactly four marks")
    off = [k for k in MARKS if not (1 <= k[0] <= ROWS and 1 <= k[1] <= COLS)]
    if off:
        raise SystemExit(f"marks fall outside the drawn floor and would be invisible: {off}")


_self_check()

out = []
add = out.append
_sizes = []


def T(x, y, s, size, fill=INK, family="Songti", weight=400, anchor="start", ls=None, op=None):
    """All type goes through here so the column floor can be asserted."""
    _sizes.append((size, s[:14]))
    a = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight != 400:
        a.append(f'font-weight="{weight}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if ls:
        a.append(f'letter-spacing="{ls}"')
    if op:
        a.append(f'opacity="{op}"')
    add(f'<text {" ".join(a)}>{s}</text>')


def font_face(name, file, weight=400):
    b64 = base64.b64encode((FONTS / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';font-weight:{weight};font-style:normal;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}")


def num(n):
    """A real minus sign, not a hyphen — both faces carry U+2212."""
    return f"−{-n}" if n < 0 else str(n)


# --- grid primitives --------------------------------------------------------
def cell_box(gx, gy, cell, r, c):
    return gx + (c - 1) * cell, gy + (r - 1) * cell


def cell_centre(gx, gy, cell, r, c):
    x, y = cell_box(gx, gy, cell, r, c)
    return x + cell / 2, y + cell / 2


def grid_floor(gx, gy, cell):
    add(f'<rect x="{gx}" y="{gy}" width="{cell*COLS}" height="{cell*ROWS}" fill="{ROOM}"/>')


def grid_lines(gx, gy, cell, weight=1.2):
    for c in range(1, COLS):
        x = gx + c * cell
        add(f'<line x1="{x}" y1="{gy}" x2="{x}" y2="{gy+cell*ROWS}" stroke="{INK}" '
            f'stroke-width="{weight}" opacity="0.34"/>')
    for r in range(1, ROWS):
        y = gy + r * cell
        add(f'<line x1="{gx}" y1="{y}" x2="{gx+cell*COLS}" y2="{y}" stroke="{INK}" '
            f'stroke-width="{weight}" opacity="0.34"/>')
    add(f'<rect x="{gx}" y="{gy}" width="{cell*COLS}" height="{cell*ROWS}" fill="none" '
        f'stroke="{INK}" stroke-width="2"/>')


def grid_labels(gx, gy, cell, size=26):
    for c in range(1, COLS + 1):
        cx, _ = cell_centre(gx, gy, cell, 1, c)
        T(cx, gy - 20, f"行 {c}", size, INK_SOFT, anchor="middle")
    for r in range(1, ROWS + 1):
        _, cy = cell_centre(gx, gy, cell, r, 1)
        T(gx - 18, cy + 9, f"列 {r}", size, INK_SOFT, anchor="end")


def fan_rect(gx, gy, cell, i, fill_op, dash=None, stroke_op=1.0, sw=2.6):
    """The i-th fan's footprint, inset so three outlines never sit on one line."""
    top, left, h, w = FANS[i]
    o = i * 4
    x, y = cell_box(gx, gy, cell, top, left)
    bw, bh = w * cell - 2 * o, h * cell - 2 * o
    col = FAN_COLS[i]
    add(f'<rect x="{x+o}" y="{y+o}" width="{bw}" height="{bh}" fill="{col}" '
        f'fill-opacity="{fill_op}" stroke="{col}" stroke-width="{sw}" '
        f'stroke-opacity="{stroke_op}"'
        + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
    return x + o, y + o


# ---------------------------------------------------------------- ground ----
add(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
add('<g opacity="0.05">')
for x in range(0, W + 1, 32):
    add(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{INK}" stroke-width="1"/>')
for y in range(0, H + 1, 32):
    add(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{INK}" stroke-width="1"/>')
add("</g>")
add(f'<rect x="40" y="40" width="{W-80}" height="{H-80}" fill="none" '
    f'stroke="{INK}" stroke-width="1" opacity="0.32"/>')
for cx, cy in ((40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)):
    sx, sy = (1 if cx < W / 2 else -1), (1 if cy < H / 2 else -1)
    add(f'<line x1="{cx}" y1="{cy}" x2="{cx+sx*26}" y2="{cy}" stroke="{INK}" stroke-width="2"/>')
    add(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+sy*26}" stroke="{INK}" stroke-width="2"/>')

T(64, 132, "風域怎麼疊，記號怎麼記", 48, ls=8)
T(64, 178, "PLATE I — THREE FANS, TWELVE MARKS", 24, INK_SOFT, "PlexMono", ls=3)
add(f'<line x1="64" y1="206" x2="{W-64}" y2="206" stroke="{INK}" stroke-width="1" opacity="0.42"/>')

# ------------------------------------------------ A · 疊起來的風域 ----------
T(64, 254, "A — 三台疊起來，每一格被幾台吹到", 30)

for i, (top, left, h, w) in enumerate(FANS):
    lx = 64 + i * 394
    add(f'<rect x="{lx}" y="296" width="34" height="34" fill="{FAN_COLS[i]}" '
        f'fill-opacity="0.22" stroke="{FAN_COLS[i]}" stroke-width="2.4"/>')
    T(lx + 50, 324, f"第 {i+1} 台", 30, FAN_COLS[i])
    T(lx, 370, f"列 {top}–{top+h-1} ／ 行 {left}–{left+w-1}", 26, INK_SOFT)

CELL = 128
GX = (W - CELL * COLS) / 2
AGY = 442

grid_floor(GX, AGY, CELL)
for i in range(F):
    fan_rect(GX, AGY, CELL, i, 0.20)
grid_lines(GX, AGY, CELL)
grid_labels(GX, AGY, CELL)
for r in range(1, ROWS + 1):
    for c in range(1, COLS + 1):
        cx, cy = cell_centre(GX, AGY, CELL, r, c)
        n = COVER[r][c]
        if n == 0:
            T(cx, cy + 12, "0", 32, INK_SOFT, "PlexMono", 400, "middle", op="0.42")
        else:
            T(cx, cy + 16, str(n), 44, INK, "PlexMono", 700, "middle")

# The answer cell, ringed rather than filled: the three tints under it are the
# reason it wins, so covering them up would erase the argument.
hx, hy = cell_box(GX, AGY, CELL, *HOT)
add(f'<rect x="{hx+9}" y="{hy+9}" width="{CELL-18}" height="{CELL-18}" fill="none" '
    f'stroke="{INK}" stroke-width="5"/>')

ACAP = AGY + CELL * ROWS + 62
add(f'<rect x="64" y="{ACAP-27}" width="32" height="32" fill="none" '
    f'stroke="{INK}" stroke-width="5"/>')
T(112, ACAP, f"最涼的一格在第 {HOT[0]} 列第 {HOT[1]} 行，三台都吹得到 —— 答案就是 {EXPECT_BEST}。", 28)

T(64, ACAP + 58, "這張表要一格一格填。地板一大，光是填表就跑不完；下面換一種記法。",
  28, INK_SOFT)

RULE2 = ACAP + 100
add(f'<line x1="64" y1="{RULE2}" x2="{W-64}" y2="{RULE2}" stroke="{INK}" '
    f'stroke-width="1" opacity="0.42"/>')

# ------------------------------------------------ B · 四個角落的記號 --------
T(64, RULE2 + 46, "B — 每台只記四個角落：左上 +1，另外三個角記在外側", 30)
T(64, RULE2 + 88, "+1 落在矩形左上角那一格；右上、左下、右下的記號都往外挪一格，寫在矩形外面。",
  27, INK_SOFT)

BGY = RULE2 + 156
grid_floor(GX, BGY, CELL)
for i in range(F):
    rx, ry = fan_rect(GX, BGY, CELL, i, 0.09, dash="7 6", stroke_op=0.55, sw=2.2)
grid_lines(GX, BGY, CELL)
grid_labels(GX, BGY, CELL)

for (r, c), items in sorted(MARKS.items()):
    cx, cy = cell_centre(GX, BGY, CELL, r, c)
    for k, (sign, i) in enumerate(items):
        by = cy + (k - (len(items) - 1) / 2) * 52
        col = FAN_COLS[i]
        add(f'<rect x="{cx-40}" y="{by-23}" width="80" height="46" rx="9" fill="{PAPER}"/>')
        add(f'<rect x="{cx-40}" y="{by-23}" width="80" height="46" rx="9" fill="{col}" '
            f'fill-opacity="0.16" stroke="{col}" stroke-width="2.2"/>')
        T(cx, by + 11, ("+1" if sign > 0 else "−1"), 30, col, "PlexMono", 700, "middle")

# Which dashed rectangle belongs to which fan, said once, at its own corner.
# The tag goes to the *bottom*-left: the top-left cell of every rectangle
# already carries that fan's +1 badge, and the two would collide there.
for i in range(F):
    top, left, h, _ = FANS[i]
    x, y = cell_box(GX, BGY, CELL, top + h, left)
    o = i * 4
    add(f'<circle cx="{x+o+24}" cy="{y-o-26}" r="17" fill="{FAN_COLS[i]}"/>')
    T(x + o + 24, y - o - 17, str(i + 1), 24, PAPER, "PlexMono", 700, "middle")

BCAP = BGY + CELL * ROWS + 62
T(64, BCAP, f"整面地板只多了 {4*F} 個記號（{F} 台 × 4 個角）。矩形再大，記號還是四個。", 28)
T(64, BCAP + 40, "注意：貼著最右邊或最下邊的吊扇，記號會落到地板外面一格，", 26, INK_SOFT)
T(64, BCAP + 76, "所以陣列要比地板多開一圈，不然會索引超出範圍。", 26, INK_SOFT)

RULE3 = BCAP + 118
add(f'<line x1="64" y1="{RULE3}" x2="{W-64}" y2="{RULE3}" stroke="{INK}" '
    f'stroke-width="1" opacity="0.42"/>')

# ------------------------------------------------ C · 兩次累加還原 ----------
T(64, RULE3 + 46, "C — 沿著列累加一次，再沿著行累加一次，A 那張表就回來了", 30)

MC = 84
MW = MC * COLS
MGX1 = 145
MGX2 = MGX1 + MW + 150
MGY = RULE3 + 168

for gx, tbl, cap in ((MGX1, ROW_SUM, "① 每一列由左往右累加"),
                     (MGX2, RESTORED, "② 再每一行由上往下累加")):
    T(gx, MGY - 26, cap, 28)
    grid_floor(gx, MGY, MC)
    grid_lines(gx, MGY, MC, weight=1)
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            cx, cy = cell_centre(gx, MGY, MC, r, c)
            n = tbl[r][c]
            soft = (n == 0)
            T(cx, cy + 11, num(n), 30, INK_SOFT if soft else INK, "PlexMono",
              400 if soft else 700, "middle", op="0.42" if soft else None)

# The arrow between the two sweeps, drawn on the row the eye is already on.
AY = MGY + MC * ROWS / 2
add(f'<line x1="{MGX1+MW+34}" y1="{AY}" x2="{MGX2-46}" y2="{AY}" stroke="{INK}" '
    f'stroke-width="2.4"/>')
add(f'<path d="M{MGX2-46},{AY} l-14,-8 l0,16 Z" fill="{INK}"/>')

# The direction of each sweep, as an arrow along the grid itself.
add(f'<line x1="{MGX1}" y1="{MGY+MC*ROWS+22}" x2="{MGX1+MW-14}" y2="{MGY+MC*ROWS+22}" '
    f'stroke="{FAN_COLS[0]}" stroke-width="2.2"/>')
add(f'<path d="M{MGX1+MW},{MGY+MC*ROWS+22} l-16,-7 l0,14 Z" fill="{FAN_COLS[0]}"/>')
VX = MGX2 + MW + 26
add(f'<line x1="{VX}" y1="{MGY}" x2="{VX}" y2="{MGY+MC*ROWS-14}" '
    f'stroke="{FAN_COLS[1]}" stroke-width="2.2"/>')
add(f'<path d="M{VX},{MGY+MC*ROWS} l-7,-16 l14,0 Z" fill="{FAN_COLS[1]}"/>')

MCAP = MGY + MC * ROWS + 48
T(MGX2, MCAP, "＝ 上面 A 的那張表", 26, INK_SOFT)

T(64, MCAP + 70,
  "暴力解要走遍每個矩形裡的每一格；差分只動 4F 個記號，最後把整面地板掃一次就結束。", 28)

T(W - 64, H - 66, "APCS018 · FAN COVERAGE · FIG.1", 24, INK_SOFT, "PlexMono", anchor="end", ls=3)

small = [(s, txt) for s, txt in _sizes if s < MIN_TYPE]
if small:
    raise SystemExit(f"type below the {MIN_TYPE}px column floor: {small}")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>")
css = font_face("PlexMono", "IBMPlexMono-Regular.ttf", 400) + font_face(
    "PlexMono", "IBMPlexMono-Bold.ttf", 700)
# Nothing in canvas-fonts carries CJK glyphs, so the Chinese has to come from
# the OS or it renders as tofu.
css += ("@font-face{font-family:'Songti';src:local('Songti TC'),local('Songti SC'),"
        "local('STSong'),local('Heiti TC'),local('STHeiti');}")
(HERE / "plate018.html").write_text(
    f'<!doctype html><meta charset="utf-8">'
    f"<style>{css}html,body{{margin:0;padding:0;background:{PAPER};}}svg{{display:block;}}</style>"
    f"{svg}", encoding="utf-8")
print(f"wrote plate018.html  {W}x{H}  smallest type {min(s for s,_ in _sizes)}px  "
      f"marks {sum(len(v) for v in MARKS.values())}  answer {EXPECT_BEST}")
