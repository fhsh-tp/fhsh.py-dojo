"""Draw the apcs019 room-allocation plate: `docs/public/assets/challenge/apcs019/圖一.png`.

    python3 scripts/figures/apcs019_plate.py     # writes plate019.html next to itself
    zsh scripts/figures/apcs019_plate.sh         # html → png via headless Chrome

Two panels, in the order a student needs them:

  A  the four worked applications as a gantt chart — minutes across, rooms down,
     each bar sitting in the room it was actually handed. The 40th minute gets a
     dashed rule of its own, because that is the one instant the rule turns on:
     application 1's span does not include minute 40, so room 1 is free again at
     exactly the moment application 3 asks for it. Every bar end is drawn as
     `[start` and `end)` so the half-open convention is read off the picture
     rather than remembered from the prose.
  B  the four allocation rules, stacked. Rule 3 — smallest free room number — is
     the one that makes the answer unique rather than merely optimal, so it is
     the only one given a panel of its own.

**Why 1280 wide and portrait.** The challenge page puts the problem text in a
fixed left pane — measured at 643 CSS px on a 1728 px desktop — so the canvas is
authored at 1280 and displayed at ~640, i.e. exactly 2×, and no glyph is set
below 24 px so nothing drops under 12 px on screen. The floor is asserted at the
bottom of this file: the constraint is the column, not taste.
"""

import base64
import pathlib

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/canvas-design/canvas-fonts"

W, H = 1280, 1880
MIN_TYPE = 24          # nothing smaller: 24 authored px = 12 px on screen

# --- palette: paper, ink, and three hues out of one soil --------------------
PAPER = "#F3EFE4"
INK = "#1A1813"
INK_SOFT = "#6E675A"
FLOOR = "#E7E0CC"
ROOM_BG = "#FCFAF3"
C_R1 = "#B4532A"   # 1 號教室 — the room that gets handed back and reused
C_R2 = "#2C6E63"   # 2 號教室
C_R3 = "#3D4A7A"   # 3 號教室
ROOM_COL = {1: C_R1, 2: C_R2, 3: C_R3}

# --- the worked example, exactly as the challenge states it -----------------
STARTS = [10, 20, 40, 45]
DURS = [30, 30, 10, 10]
EXPECT_ROOMS = 3
EXPECT_ASSIGN = [1, 2, 1, 3]


def allocate(starts, durations, half_open=True):
    """The challenge's own four rules, run straight. Returns (rooms, assignment).

    `last_end[r]` is the minute room r+1 is booked until. A room counts as free
    the instant its last booking ends — `<=`, not `<` — which is the half-open
    interval the whole plate is about. `half_open=False` is the misreading, kept
    only so the self-check can show what it costs.
    """
    order = sorted(range(len(starts)), key=lambda i: (starts[i], i))   # rules 1, 2
    last_end, room = [], [0] * len(starts)
    for i in order:
        free = (lambda r: last_end[r] <= starts[i]) if half_open else (
            lambda r: last_end[r] < starts[i])
        picked = next((r for r in range(len(last_end)) if free(r)), -1)
        if picked < 0:                                                  # rule 4
            last_end.append(0)
            picked = len(last_end) - 1
        last_end[picked] = starts[i] + durations[i]                     # rule 3 picks the
        room[i] = picked + 1                                            # lowest free index
    return len(last_end), room


def _self_check():
    """The plate prints a specific answer, so the allocation behind it is checked
    against the challenge's worked example rather than eyeballed. A drawing that
    is merely pretty and wrong is worse than no drawing."""
    rooms, assign = allocate(STARTS, DURS)
    if (rooms, assign) != (EXPECT_ROOMS, EXPECT_ASSIGN):
        raise SystemExit(f"allocation is {rooms} / {assign}, the challenge says "
                         f"{EXPECT_ROOMS} / {EXPECT_ASSIGN}")
    ends = [s + d for s, d in zip(STARTS, DURS)]
    if ends != [40, 50, 50, 55]:
        raise SystemExit(f"spans end at {ends}, the challenge says [40, 50, 50, 55]")
    # The plate's whole claim: applications 1 and 3 share room 1 *only* because
    # 1's span is half-open at minute 40. Read the interval as closed and
    # application 3 is pushed into a room of its own — which is the mistake the
    # 40th-minute callout exists to head off.
    if allocate(STARTS, DURS, half_open=False)[1] != [1, 2, 3, 1]:
        raise SystemExit("the closed-interval misreading no longer changes the answer — "
                         "the 40th-minute callout would be pointing at nothing")


_self_check()
ROOMS, ASSIGN = allocate(STARTS, DURS)
ENDS = [s + d for s, d in zip(STARTS, DURS)]

# --- chart geometry ---------------------------------------------------------
MMAX = 60
X0, X1 = 232, 1216
PPM = (X1 - X0) / MMAX          # px per minute
AXIS_Y = 384                    # chart top / axis rule
BANDH = 112
BARH = 48
KEY_MIN = 40                    # the instant the plate is built around


def mx(m):
    return X0 + m * PPM


def band_cy(room):
    return AXIS_Y + BANDH * (room - 0.5)


CHART_BOT = AXIS_Y + BANDH * ROOMS

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


def mono(s, weight=700):
    """A run of digits inside a Songti sentence — numbers get compared digit by
    digit, so they keep the monospaced face even mid-clause."""
    return f'<tspan font-family="PlexMono" font-weight="{weight}">{s}</tspan>'


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
T(64, 132, "借用時段與派房順序", 48, ls=8)
T(64, 178, "PLATE I — FOUR BOOKINGS, THREE ROOMS", 24, INK_SOFT, "PlexMono", ls=3)
add(f'<line x1="64" y1="206" x2="{W-64}" y2="206" stroke="{INK}" stroke-width="1" opacity="0.42"/>')

# ------------------------------------------------- A · the gantt chart ------
T(64, 256, "A — 範例的四筆申請，落在它被分到的那一列", 30)

# Row bands: the room is the row, so the answer is readable as a shape.
for r in range(1, ROOMS + 1):
    top = AXIS_Y + BANDH * (r - 1)
    if r % 2 == 0:
        add(f'<rect x="{X0}" y="{top}" width="{X1-X0}" height="{BANDH}" '
            f'fill="{FLOOR}" opacity="0.45"/>')
    T(204, band_cy(r) + 10, f"{r} 號教室", 27, ROOM_COL[r], anchor="end")
    add(f'<line x1="{X0}" y1="{top+BANDH}" x2="{X1}" y2="{top+BANDH}" '
        f'stroke="{INK}" stroke-width="1" opacity="0.28"/>')

# Minute scale: a tick every 5, because 45 and 55 are both bar edges.
for m in range(0, MMAX + 1, 5):
    x = mx(m)
    add(f'<line x1="{x}" y1="{AXIS_Y}" x2="{x}" y2="{CHART_BOT}" stroke="{INK}" '
        f'stroke-width="1" opacity="{0.18 if m % 10 == 0 else 0.09}"/>')
    add(f'<line x1="{x}" y1="{AXIS_Y-12}" x2="{x}" y2="{AXIS_Y}" stroke="{INK}" stroke-width="1.4"/>')
    T(x, AXIS_Y - 24, str(m), 26, INK if m % 10 == 0 else INK_SOFT, "PlexMono",
      700 if m % 10 == 0 else 400, "middle")
add(f'<line x1="{X0}" y1="{AXIS_Y}" x2="{X1}" y2="{AXIS_Y}" stroke="{INK}" stroke-width="2"/>')
T(204, AXIS_Y - 24, "分鐘", 26, INK_SOFT, anchor="end")

# The 40th minute, threaded through the whole panel down into its callout.
KX = mx(KEY_MIN)
CALL_TOP = 764
add(f'<line x1="{KX}" y1="{AXIS_Y}" x2="{KX}" y2="{CALL_TOP-16}" stroke="{INK}" '
    f'stroke-width="2" stroke-dasharray="9 7" opacity="0.85"/>')
add(f'<path d="M{KX},{AXIS_Y-56} l9,-13 l-18,0 Z" fill="{INK}"/>')

# Bars. Edge labels default to the gutter above the bar; application 3's start
# label is the one exception, dropped below because it lands on the very same
# pixel as application 1's end label — which is precisely the coincidence the
# plate is about, and would be illegible drawn twice in one place.
LABEL_BELOW = {(3, "start")}
for i, (s, d, r) in enumerate(zip(STARTS, DURS, ASSIGN), start=1):
    e = s + d
    x, xe, cy = mx(s), mx(e), band_cy(r)
    col = ROOM_COL[r]
    add(f'<rect x="{x}" y="{cy-BARH/2}" width="{xe-x}" height="{BARH}" fill="{col}" opacity="0.9"/>')
    # Closed at the start, open at the end — drawn, not asserted.
    add(f'<line x1="{x}" y1="{cy-BARH/2}" x2="{x}" y2="{cy+BARH/2}" stroke="{INK}" stroke-width="4"/>')
    add(f'<line x1="{xe}" y1="{cy-BARH/2}" x2="{xe}" y2="{cy+BARH/2}" stroke="{INK}" '
        f'stroke-width="2.4" stroke-dasharray="6 5"/>')
    T((x + xe) / 2, cy + 11, f"申請 {i}", 30, PAPER, anchor="middle")
    for end, tx, txt, anchor in (("start", x + 3, f"[{s}", "start"),
                                 ("end", xe - 3, f"{e})", "end")):
        ly = (cy + BARH / 2 + 30) if (i, end) in LABEL_BELOW else (cy - BARH / 2 - 6)
        T(tx, ly, txt, 24, col, "PlexMono", 700, anchor)

# The callout: one instant, spelled out, hung off the dashed rule.
add(f'<rect x="{X0}" y="{CALL_TOP}" width="{X1-X0}" height="124" fill="{ROOM_BG}" '
    f'stroke="{C_R1}" stroke-width="2"/>')
add(f'<line x1="{KX-9}" y1="{CALL_TOP}" x2="{KX+9}" y2="{CALL_TOP}" stroke="{ROOM_BG}" stroke-width="4"/>')
add(f'<path d="M{KX-10},{CALL_TOP} L{KX},{CALL_TOP-16} L{KX+10},{CALL_TOP}" fill="none" '
    f'stroke="{C_R1}" stroke-width="2" stroke-linejoin="miter"/>')
T(264, CALL_TOP + 54, f"第 {mono('40')} 分鐘：申請 {mono('1')} 的時段不含第 "
                      f"{mono('40')} 分鐘，這一刻 {mono('1')} 號教室剛空出來；", 28)
T(264, CALL_TOP + 96, f"同一刻申請 {mono('3')} 就把它接走——兩筆不算重疊，"
                      f"{mono('1')} 號教室直接續用，不必另開。", 28)

# Half-open key + the answer this chart adds up to.
KEY_Y = 928
add(f'<rect x="{X0}" y="{KEY_Y-30}" width="104" height="44" fill="{C_R1}" opacity="0.9"/>')
add(f'<line x1="{X0}" y1="{KEY_Y-30}" x2="{X0}" y2="{KEY_Y+14}" stroke="{INK}" stroke-width="4"/>')
add(f'<line x1="{X0+104}" y1="{KEY_Y-30}" x2="{X0+104}" y2="{KEY_Y+14}" stroke="{INK}" '
    f'stroke-width="2.4" stroke-dasharray="6 5"/>')
T(X0 + 128, KEY_Y + 6, "實線端：從這一分鐘起占用　　虛線端：這一分鐘已交還，別人可以接手", 27, INK_SOFT)
T(X0, 1000, f"這一週最少要開 {mono(ROOMS)} 間教室；四筆申請依輸入順序分到 "
            f"{mono(' '.join(str(v) for v in ASSIGN))}。", 29)

# ------------------------------------------------------ B · the four rules --
BY = 1048
add(f'<line x1="64" y1="{BY}" x2="{W-64}" y2="{BY}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, BY + 46, "B — 派房規則的四層，由上往下依序套用", 30)

RULES = [
    ("1", "依開始分鐘由早到晚，逐筆處理每一筆申請", None),
    ("2", "開始分鐘相同時，依申請編號由小到大", None),
    ("3", "發給當下空著的教室中，編號最小的那一間",
     "這一條讓答案唯一：不是隨便挑一間空的，一定要編號最小的那一間"),
    ("4", "全部客滿才新開一間，編號是現有間數加一", None),
]
RY0, PITCH, BH = BY + 82, 146, 122
for i, (num, line, sub) in enumerate(RULES):
    ty = RY0 + i * PITCH
    star = sub is not None
    if star:
        add(f'<rect x="56" y="{ty}" width="{W-112}" height="{BH}" fill="{ROOM_BG}" '
            f'stroke="{C_R1}" stroke-width="2"/>')
        add(f'<rect x="56" y="{ty}" width="7" height="{BH}" fill="{C_R1}"/>')
    sq = ty + (BH - 76) / 2
    add(f'<rect x="76" y="{sq}" width="76" height="76" fill="{C_R1 if star else "none"}" '
        f'stroke="{INK}" stroke-width="{0 if star else 1.8}"/>')
    T(114, sq + 52, num, 40, PAPER if star else INK, "PlexMono", 700, "middle")
    if star:
        T(188, ty + 54, line, 32)
        T(188, ty + 94, sub, 26, INK_SOFT)
    else:
        T(188, ty + BH / 2 + 11, line, 30)

T(64, RY0 + 4 * PITCH + 36,
  "前兩條決定「誰先被處理」，後兩條決定「拿到哪一間」；四條合起來，答案只有一種。", 27, INK_SOFT)

T(W - 64, H - 66, "APCS019 · ROOM ALLOCATION · FIG.1", 24, INK_SOFT, "PlexMono", anchor="end", ls=3)

# The column-scale floor is a contract, not an intention — assert it.
small = [(s, txt) for s, txt in _sizes if s < MIN_TYPE]
if small:
    raise SystemExit(f"type below the {MIN_TYPE}px column floor: {small}")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>")
css = font_face("PlexMono", "IBMPlexMono-Regular.ttf", 400) + font_face(
    "PlexMono", "IBMPlexMono-Bold.ttf", 700)
# Songti is the system Ming face. Nothing in canvas-fonts carries CJK glyphs, so
# the Chinese has to come from the OS or it renders as tofu.
css += ("@font-face{font-family:'Songti';src:local('Songti TC'),local('Songti SC'),"
        "local('STSong'),local('Heiti TC'),local('STHeiti');}")
(HERE / "plate019.html").write_text(
    f'<!doctype html><meta charset="utf-8">'
    f"<style>{css}html,body{{margin:0;padding:0;background:{PAPER};}}svg{{display:block;}}</style>"
    f"{svg}", encoding="utf-8")
print(f"wrote plate019.html  {W}×{H}  smallest type {min(s for s, _ in _sizes)}px")
