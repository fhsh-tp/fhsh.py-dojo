"""Draw the apcs014 pinball plate: `docs/public/assets/challenge/apcs014/圖一.png`.

    zsh scripts/figures/apcs014_plate.sh

Three panels, in the order a student needs them:

  A  the machine — one funnel, three rows of flippers, eight bags, plus the
     toggle rule shown as a before/after pair rather than stated again
  B  balls 1–3 as a filmstrip, each board drawn in the state it was in *before*
     that ball dropped, so the toggle is visible as cause and effect
  C  where the first eight balls land

**What the plate must not say.** The challenge asks the student to find that
ball I's path can be derived without simulating the balls before it. Anything
about binary digits or reversing them hands that over, so the plate stops at
what the prose already tells them: the rules, three worked drops, and the
observed landing order.

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

W, H = 1280, 2080
MIN_TYPE = 24

PAPER = "#F3EFE4"
INK = "#1A1813"
INK_SOFT = "#6E675A"
FLOOR = "#E7E0CC"
ROOM = "#FCFAF3"
BALL = "#B4532A"      # the ball and its path
SET_L = "#3D4A7A"     # a flipper still pointing left
SET_R = "#2C6E63"     # a flipper flipped to the right

D = 4                 # the worked machine: 3 rows of flippers, 8 bags
ROWS = D - 1
BAGS = 2 ** ROWS

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


# --- the machine, as pure arithmetic ---------------------------------------
def fx(bx, bw, level, j):
    """Centre of flipper j (1-based) on `level` (1-based)."""
    return bx + bw * (j - 0.5) / (2 ** (level - 1))


def bag_x(bx, bw, j):
    return bx + bw * (j - 0.5) / BAGS


def drop(state, level=1, j=1, path=None):
    """Send one ball down `state`, mutating it. Returns (bag, path points).

    `state[(level, j)]` is 'L' or 'R' — the side this flipper currently sends a
    ball to. The flip happens as the ball leaves, which is the whole rule.
    """
    path = path if path is not None else []
    path.append((level, j))
    side = state.get((level, j), "L")
    state[(level, j)] = "R" if side == "L" else "L"
    child = 2 * j - 1 if side == "L" else 2 * j
    if level == ROWS:
        return child, path
    return drop(state, level + 1, child, path)


def _self_check():
    """The plate prints specific answers, so the simulation behind it has to be
    checked against the challenge's own worked example rather than eyeballed.
    A drawing that is merely pretty and wrong is worse than no drawing."""
    st, got = {}, []
    for _ in range(11):
        got.append(drop(st)[0])
    expect_first8 = [1, 5, 3, 7, 2, 6, 4, 8]
    if got[:8] != expect_first8:
        raise SystemExit(f"first 8 drops are {got[:8]}, the challenge says {expect_first8}")
    if got[10] != 3:
        raise SystemExit(f"ball 11 lands in {got[10]}, the challenge says 3")
    if sorted(got[:8]) != list(range(1, BAGS + 1)):
        raise SystemExit("the first 8 balls do not fill every bag exactly once")


_self_check()


def flipper(x, y, side, col, w=2.8, arm=25):
    """A chute: the paddle slopes down towards the side the ball will take."""
    dx = -arm if side == "L" else arm
    add(f'<line x1="{x-dx*0.55}" y1="{y-9}" x2="{x+dx}" y2="{y+11}" '
        f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    add(f'<circle cx="{x-dx*0.55}" cy="{y-9}" r="3.4" fill="{col}"/>')


def board(bx, bw, ys, state, ball_path=None, bag=None, small=False):
    """Draw one machine. `ys` = [level1, level2, level3, bag top]."""
    # Static plumbing first: every chute that exists, whatever the flippers say.
    for lv in range(1, ROWS + 1):
        for j in range(1, 2 ** (lv - 1) + 1):
            x, y = fx(bx, bw, lv, j), ys[lv - 1]
            for child, nxt in ((2 * j - 1, ys[lv]), (2 * j, ys[lv])):
                cx = (bag_x(bx, bw, child) if lv == ROWS else fx(bx, bw, lv + 1, child))
                add(f'<line x1="{x}" y1="{y+11}" x2="{cx}" y2="{nxt-(14 if lv==ROWS else 12)}" '
                    f'stroke="{INK}" stroke-width="1" opacity="0.2"/>')
    # The ball's route, drawn over the plumbing and under the flippers.
    if ball_path:
        pts = [(fx(bx, bw, 1, 1), ys[0] - (44 if not small else 30))]
        for k, (lv, j) in enumerate(ball_path):
            pts.append((fx(bx, bw, lv, j), ys[lv - 1]))
        pts.append((bag_x(bx, bw, bag), ys[ROWS] - 6))
        add('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) +
            f'" fill="none" stroke="{BALL}" stroke-width="{3.4 if not small else 3}" '
            f'stroke-linejoin="round" stroke-linecap="round" opacity="0.92"/>')
        add(f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="{9 if not small else 8}" fill="{BALL}"/>')
    # Flippers on top, coloured by which way they currently point.
    for lv in range(1, ROWS + 1):
        for j in range(1, 2 ** (lv - 1) + 1):
            side = state.get((lv, j), "L")
            flipper(fx(bx, bw, lv, j), ys[lv - 1], side,
                    SET_L if side == "L" else SET_R,
                    w=2.8 if not small else 2.4, arm=25 if not small else 17)
    # Bags.
    bw_slot = bw / BAGS
    for j in range(1, BAGS + 1):
        cx, top = bag_x(bx, bw, j), ys[ROWS]
        hit = (bag == j)
        add(f'<rect x="{cx-bw_slot*0.40}" y="{top}" width="{bw_slot*0.80}" '
            f'height="{54 if not small else 40}" fill="{BALL if hit else FLOOR}" '
            f'stroke="{INK}" stroke-width="{2 if hit else 1.2}" opacity="{1 if hit else 0.9}"/>')
    return bw_slot


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

T(64, 132, "彈珠台的構造與翻板規則", 48, ls=8)
T(64, 178, "PLATE I — ONE CHUTE, EIGHT POCKETS", 24, INK_SOFT, "PlexMono", ls=3)
add(f'<line x1="64" y1="206" x2="{W-64}" y2="206" stroke="{INK}" stroke-width="1" opacity="0.42"/>')

# --------------------------------------------------- A · 機台（開機狀態）----
T(64, 254, "A — 開機時的機台（D = 4）", 30)
BX, BW = 372, 600
YS = [366, 474, 582, 700]
add(f'<line x1="{fx(BX,BW,1,1)}" y1="304" x2="{fx(BX,BW,1,1)}" y2="{YS[0]-16}" '
    f'stroke="{INK}" stroke-width="2"/>')
add(f'<path d="M{fx(BX,BW,1,1)-8},{YS[0]-16} L{fx(BX,BW,1,1)+8},{YS[0]-16} '
    f'L{fx(BX,BW,1,1)},{YS[0]-3} Z" fill="{INK}"/>')
T(fx(BX, BW, 1, 1) - 22, 300, "投球口", 26, anchor="end")

slot = board(BX, BW, YS, {})       # every flipper still pointing left
for lv, txt in ((1, "第 1 層 · 1 片"), (2, "第 2 層 · 2 片"), (3, "第 3 層 · 4 片")):
    T(BX - 40, YS[lv - 1] + 9, txt, 26, INK_SOFT, anchor="end")
T(BX - 40, YS[ROWS] + 36, "收集袋 · 8 個", 26, INK_SOFT, anchor="end")
for j in range(1, BAGS + 1):
    T(bag_x(BX, BW, j), YS[ROWS] + 88, str(j), 26, INK, "PlexMono", 700, "middle")

# The toggle rule, shown rather than restated.
TY = 826
add(f'<rect x="64" y="{TY}" width="{W-128}" height="128" fill="{ROOM}" '
    f'stroke="{INK}" stroke-width="1.4" opacity="0.9"/>')
flipper(150, TY + 62, "L", SET_L, arm=28)
T(150, TY + 116, "朝左", 26, SET_L, anchor="middle")
add(f'<path d="M212,{TY+56} L268,{TY+56}" stroke="{INK}" stroke-width="2"/>')
add(f'<path d="M268,{TY+56} l-11,-6 l0,12 Z" fill="{INK}"/>')
T(240, TY + 40, "球滑過", 24, INK_SOFT, anchor="middle")
flipper(330, TY + 62, "R", SET_R, arm=28)
T(330, TY + 116, "朝右", 26, SET_R, anchor="middle")
T(410, TY + 56, "球往翻板現在指的那一側滑下去；滑走的同時，", 27)
T(410, TY + 94, "這片翻板就被扳向另一側，下一顆球走反方向。", 27)

# ------------------------------------------------- B · 前三顆球的走法 -------
PY = 1000
add(f'<line x1="64" y1="{PY}" x2="{W-64}" y2="{PY}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, PY + 44, "B — 前三顆球（每台畫的是這顆球投下去「之前」的狀態）", 30)

state = {}
sbw, gap = 336, 44
sys_ = [PY + 176, PY + 262, PY + 348, PY + 452]
for i in range(3):
    sbx = 64 + i * (sbw + gap)
    before = dict(state)
    bag, path = drop(state)
    board(sbx, sbw, sys_, before, ball_path=path, bag=bag, small=True)
    T(sbx + sbw / 2, PY + 128, f"第 {i+1} 顆", 30, BALL, anchor="middle")
    T(sbx + sbw / 2, PY + 552, f"→ {bag} 號袋", 30, INK, anchor="middle")

T(64, PY + 620, "第 1 顆把沿路的翻板全扳過去了，所以第 2 顆一開始就往另一邊走。", 27, INK_SOFT)

# ------------------------------------------------------ C · 八顆的落點 -----
CY0 = PY + 664
add(f'<line x1="64" y1="{CY0}" x2="{W-64}" y2="{CY0}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, CY0 + 44, "C — 前 8 顆球的落點：每個袋子正好各一顆", 30)

order = [1, 5, 3, 7, 2, 6, 4, 8]     # ball n lands in bag order[n-1]
# Row labels sit in the left margin so the block reads as a two-row table.
# Stacked under the row they read as footnotes and lose the pairing.
ROWX = 186
cw = (W - 64 - ROWX) / BAGS
T(64, CY0 + 132, "袋子", 26, INK_SOFT)
T(64, CY0 + 214, "球號", 26, BALL)
for j in range(1, BAGS + 1):
    cx = ROWX + cw * (j - 0.5)
    ball = order.index(j) + 1
    add(f'<rect x="{cx-cw*0.36}" y="{CY0+88}" width="{cw*0.72}" height="{68}" '
        f'fill="{FLOOR}" stroke="{INK}" stroke-width="1.4"/>')
    T(cx, CY0 + 132, str(j), 34, INK, "PlexMono", 700, "middle")
    add(f'<circle cx="{cx}" cy="{CY0+206}" r="19" fill="{BALL}"/>')
    T(cx, CY0 + 215, str(ball), 24, PAPER, "PlexMono", 700, "middle")
T(64, CY0 + 292, "球一直投下去也不會停——第 9 顆又回到 1 號袋，如此循環。", 27, INK_SOFT)

T(W - 64, H - 66, "APCS014 · PINBALL TRACK · FIG.1", 24, INK_SOFT, "PlexMono", anchor="end", ls=3)

small = [(s, txt) for s, txt in _sizes if s < MIN_TYPE]
if small:
    raise SystemExit(f"type below the {MIN_TYPE}px column floor: {small}")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>")
css = font_face("PlexMono", "IBMPlexMono-Regular.ttf", 400) + font_face(
    "PlexMono", "IBMPlexMono-Bold.ttf", 700)
css += ("@font-face{font-family:'Songti';src:local('Songti TC'),local('Songti SC'),"
        "local('STSong'),local('Heiti TC'),local('STHeiti');}")
(HERE / "plate014.html").write_text(
    f'<!doctype html><meta charset="utf-8">'
    f"<style>{css}html,body{{margin:0;padding:0;background:{PAPER};}}svg{{display:block;}}</style>"
    f"{svg}", encoding="utf-8")
print(f"wrote plate014.html  {W}×{H}  smallest type {min(s for s,_ in _sizes)}px")
