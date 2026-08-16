"""Draw the apcs013 walking-plate: `docs/public/assets/challenge/apcs013/圖一.png`.

    python3 scripts/figures/apcs013_plate.py            # writes plate.html next to itself
    zsh scripts/figures/apcs013_plate.sh                # html → png via headless Chrome

The drawing is a FLOOR PLAN, not a tree: rooms have walls with door openings,
corridors have two walls and a floor between them, and the route is a dashed
line that goes down every corridor and comes back up it. That doubling is the
whole subject of the plate, so it is drawn rather than described.

**Why 1280 wide and portrait.** The challenge page puts the problem text in a
fixed left pane — measured at 643 CSS px on a 1728 px desktop — so a landscape
poster lands at roughly 27% scale and every label in it becomes unreadable. The
canvas is therefore authored at 1280 px and displayed at ~640, i.e. exactly 2×,
and no glyph is set below 24 px so nothing drops under 12 px on screen. Check
this before changing any font size: the constraint is the column, not taste.
"""

import base64
import pathlib

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/canvas-design/canvas-fonts"

W, H = 1280, 2060
MIN_TYPE = 24          # nothing smaller: 24 authored px = 12 px on screen

# --- palette: paper, ink, and three hues that share one soil ----------------
PAPER = "#F3EFE4"
INK = "#1A1813"
INK_SOFT = "#6E675A"
FLOOR = "#E7E0CC"
ROOM = "#FCFAF3"
C_JIA = "#B4532A"   # 甲
C_YI = "#2C6E63"    # 乙
C_BING = "#3D4A7A"  # 丙

# --- the exhibition layout (the first worked example in the challenge) ------
LEFT = {2: 1, 1: 5, 5: 3, 4: 7}
RIGHT = {2: 4, 1: 6}
ROOT = 2
INORDER = [3, 5, 1, 6, 2, 7, 4]
DEPTH = {2: 0, 1: 1, 4: 1, 5: 2, 6: 2, 7: 2, 3: 3}

SEQ = {
    "甲": [2, 1, 5, 3, 6, 4, 7],
    "乙": [3, 5, 1, 6, 2, 7, 4],
    "丙": [3, 5, 6, 1, 7, 4, 2],
}
RULES = [
    ("甲", C_JIA, "1", "一走進房間就蓋章"),
    ("乙", C_YI, "2", "左邊那一整區走完，回到房間才蓋章"),
    ("丙", C_BING, "3", "左右兩區都走完，最後才蓋章"),
]

# --- plan geometry ----------------------------------------------------------
PX0, PX1 = 64, 1216
COLW = (PX1 - PX0) / 7
ROW_Y = [318, 528, 738, 948]
RW, RH = 124, 94
HALL = 28
HW = HALL / 2
ROUTE = 7
DOT_R = 9

CX = {n: PX0 + COLW * (INORDER.index(n) + 0.5) for n in INORDER}
CY = {n: ROW_Y[DEPTH[n]] for n in INORDER}


# A room's two lower doors sit apart — the left branch leaves from the left of
# the room, the right branch from the right. Putting both on one spot would
# make the plan read as a tree again.
def door_x(n, side):
    return CX[n] + (-RW / 4 if side == "左" else RW / 4)


LINKS = [(p, c, "左") for p, c in LEFT.items()] + [(p, c, "右") for p, c in RIGHT.items()]

out = []
add = out.append
_sizes = []


def T(x, y, s, size, fill=INK, family="Songti", weight=400, anchor="start", ls=None, op=None):
    """Every piece of type goes through here so the column-scale floor can be
    asserted rather than remembered."""
    _sizes.append((size, s[:12]))
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

# ---------------------------------------------------------------- header ----
T(64, 132, "展場動線與打卡時機", 48, ls=8)
T(64, 178, "PLATE I — ONE ROUTE, THREE TIMINGS", 24, INK_SOFT, "PlexMono", ls=3)
add(f'<line x1="64" y1="206" x2="{W-64}" y2="206" stroke="{INK}" stroke-width="1" opacity="0.42"/>')


# ------------------------------------------------------------- corridors ----
def elbow(p, c, side):
    x1, y1 = door_x(p, side), CY[p] + RH / 2
    x2, y2 = CX[c], CY[c] - RH / 2
    return x1, y1, x2, y2, (y1 + y2) / 2


def offset_wall(x1, y1, x2, y2, ym, o):
    """Exact offset of an axis-aligned down/across/down elbow by `o`."""
    s = 1 if x2 >= x1 else -1
    return f"{x1+o},{y1} {x1+o},{ym+s*o} {x2+o},{ym+s*o} {x2+o},{y2}"


for p, c, side in LINKS:
    x1, y1, x2, y2, ym = elbow(p, c, side)
    add(f'<polyline points="{x1},{y1} {x1},{ym} {x2},{ym} {x2},{y2}" fill="none" '
        f'stroke="{FLOOR}" stroke-width="{HALL}" stroke-linejoin="miter" stroke-linecap="butt"/>')
for p, c, side in LINKS:
    x1, y1, x2, y2, ym = elbow(p, c, side)
    for o in (-HW, HW):
        add(f'<polyline points="{offset_wall(x1, y1, x2, y2, ym, o)}" fill="none" '
            f'stroke="{INK}" stroke-width="2"/>')

# The route: down one side of the hall, back up the other. Dashed, because a
# path walked is a trace, not a wall.
for p, c, side in LINKS:
    x1, y1, x2, y2, ym = elbow(p, c, side)
    for o in (-ROUTE, ROUTE):
        add(f'<polyline points="{offset_wall(x1, y1, x2, y2, ym, o)}" fill="none" '
            f'stroke="{INK}" stroke-width="1.3" stroke-dasharray="5 4" opacity="0.62"/>')
    ax, ay = x2 - ROUTE, y2 - 26
    add(f'<path d="M{ax-5},{ay} L{ax+5},{ay} L{ax},{ay+9} Z" fill="{INK}" opacity="0.9"/>')
    bx, by = x1 + ROUTE, y1 + 26
    add(f'<path d="M{bx-5},{by} L{bx+5},{by} L{bx},{by-9} Z" fill="{INK}" opacity="0.9"/>')

for p, c, side in LINKS:
    x1, y1, x2, y2, ym = elbow(p, c, side)
    lx = (x1 + x2) / 2
    add(f'<rect x="{lx-17}" y="{ym-17}" width="34" height="34" fill="{PAPER}" '
        f'stroke="{INK}" stroke-width="1.4"/>')
    T(lx, ym + 9, side, 26, anchor="middle")


# ----------------------------------------------------------------- rooms ----
def wall_segments(a, b, gaps):
    """Split the span a→b, leaving a HALL-wide hole at each gap centre."""
    segs, cur = [], a
    for lo, hi in sorted((g - HW, g + HW) for g in gaps):
        if lo > cur:
            segs.append((cur, lo))
        cur = max(cur, hi)
    if cur < b:
        segs.append((cur, b))
    return segs


for n in INORDER:
    x, y = CX[n], CY[n]
    l, r, t, bo = x - RW / 2, x + RW / 2, y - RH / 2, y + RH / 2
    add(f'<rect x="{l}" y="{t}" width="{RW}" height="{RH}" fill="{ROOM}"/>')
    bot_gaps = [door_x(n, s) for s in ("左", "右") if n in (LEFT if s == "左" else RIGHT)]
    for a, b in wall_segments(l, r, [x]):
        add(f'<line x1="{a}" y1="{t}" x2="{b}" y2="{t}" stroke="{INK}" stroke-width="2.6"/>')
    for a, b in wall_segments(l, r, bot_gaps):
        add(f'<line x1="{a}" y1="{bo}" x2="{b}" y2="{bo}" stroke="{INK}" stroke-width="2.6"/>')
    add(f'<line x1="{l}" y1="{t}" x2="{l}" y2="{bo}" stroke="{INK}" stroke-width="2.6"/>')
    add(f'<line x1="{r}" y1="{t}" x2="{r}" y2="{bo}" stroke="{INK}" stroke-width="2.6"/>')
    T(x, y + 14, str(n), 40, family="PlexMono", weight=700, anchor="middle")
    # 甲 and 丙 flank the upper doorway — one on the way in, one on the way out.
    # 乙 sits at the bottom between the two branch doors, which is exactly where
    # the walker stands once the left wing is finished.
    for (px, py), col in (((x - 38, t + 21), C_JIA), ((x, bo - 21), C_YI), ((x + 38, t + 21), C_BING)):
        add(f'<circle cx="{px}" cy="{py}" r="{DOT_R+3}" fill="{PAPER}"/>')
        add(f'<circle cx="{px}" cy="{py}" r="{DOT_R}" fill="{col}"/>')

# --------------------------------------------------------------- entrance ---
ex, ey = CX[ROOT], CY[ROOT] - RH / 2
add(f'<line x1="{ex}" y1="{ey-82}" x2="{ex}" y2="{ey-14}" stroke="{INK}" stroke-width="2"/>')
add(f'<path d="M{ex-7},{ey-14} L{ex+7},{ey-14} L{ex},{ey-2} Z" fill="{INK}"/>')
T(ex - 20, ey - 46, "入口", 26, anchor="end")

# ------------------------------------------------------------------- key ----
KY = 1062
add(f'<line x1="64" y1="{KY}" x2="{W-64}" y2="{KY}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, KY + 40, "KEY — WHICH PASS CARRIES THE STAMP", 24, INK_SOFT, "PlexMono", ls=3)

# The pass numeral has to clear the 24px column floor, which sets the dot
# radius, which sets the mini-room size. The chain runs upward from the
# smallest glyph, not downward from a nice-looking box.
mw, mh = 108, 78
for i, (who, col, pas, rule) in enumerate(RULES):
    ty = KY + 84 + i * 140
    add(f'<rect x="64" y="{ty}" width="{mw}" height="{mh}" fill="{ROOM}" '
        f'stroke="{INK}" stroke-width="1.8"/>')
    mini = {"甲": (64 + 30, ty + 24), "乙": (64 + mw / 2, ty + mh - 24), "丙": (64 + mw - 30, ty + 24)}
    for w2, (mx, my) in mini.items():
        if w2 == who:
            add(f'<circle cx="{mx}" cy="{my}" r="17" fill="{col}"/>')
            T(mx, my + 9, pas, 24, PAPER, "PlexMono", 700, "middle")
        else:
            add(f'<circle cx="{mx}" cy="{my}" r="8" fill="none" stroke="{INK}" '
                f'stroke-width="1" opacity="0.26"/>')
    T(196, ty + 54, who, 44, col)
    T(264, ty + 52, rule, 27, INK, op="0.86")

NY = KY + 84 + 3 * 140 + 30
T(64, NY, "三個人踩的地板一模一樣，只差在第幾次經過才蓋章。", 27, INK_SOFT)

# ----------------------------------------------------------- stamp orders ---
BY = NY + 52
add(f'<line x1="64" y1="{BY}" x2="{W-64}" y2="{BY}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, BY + 40, "RESULTING STAMP ORDER", 24, INK_SOFT, "PlexMono", ls=3)

for i, (who, col, _, _) in enumerate(RULES):
    ty = BY + 108 + i * 84
    add(f'<circle cx="76" cy="{ty-12}" r="9" fill="{col}"/>')
    T(102, ty, who, 34, col)
    xs, step = 226, 143
    for j, n in enumerate(SEQ[who]):
        T(xs + j * step, ty, str(n), 36, INK, "PlexMono", 700, "middle")
    add(f'<line x1="{xs-56}" y1="{ty+20}" x2="{xs+6*step+56}" y2="{ty+20}" '
        f'stroke="{col}" stroke-width="2" opacity="0.5"/>')

T(W - 64, H - 66, "APCS013 · EXHIBIT ROUTE · FIG.1", 24, INK_SOFT, "PlexMono", anchor="end", ls=3)

# The column-scale floor is a contract, not an intention — assert it.
small = [(s, txt) for s, txt in _sizes if s < MIN_TYPE]
if small:
    raise SystemExit(f"type below the {MIN_TYPE}px column floor: {small}")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>")

css = font_face("PlexMono", "IBMPlexMono-Regular.ttf", 400) + font_face(
    "PlexMono", "IBMPlexMono-Bold.ttf", 700)
# Songti is the system Ming face. Nothing in canvas-fonts carries CJK glyphs,
# so the Chinese has to come from the OS or it renders as tofu.
css += ("@font-face{font-family:'Songti';src:local('Songti TC'),local('Songti SC'),"
        "local('STSong'),local('Heiti TC'),local('STHeiti');}")

(HERE / "plate.html").write_text(
    f'<!doctype html><meta charset="utf-8">'
    f"<style>{css}html,body{{margin:0;padding:0;background:{PAPER};}}svg{{display:block;}}</style>"
    f"{svg}", encoding="utf-8")
print(f"wrote {HERE/'plate.html'}  {W}×{H}  smallest type {min(s for s,_ in _sizes)}px")
