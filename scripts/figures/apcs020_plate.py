"""Draw the apcs020 relay-tape plate: `docs/public/assets/challenge/apcs020/圖一.png`.

    zsh scripts/figures/apcs020_plate.sh

Two panels, in the order a student needs them:

  A  the whole point-request sequence 4 9 4 7 1 9 1 as one row of cards, with
     the answer段 (positions 3–6) boxed, and the three repeated song numbers
     joined by arcs overhead. The arcs are not decoration: the arc 2–6 is
     exactly why the box cannot grow leftwards and the arc 5–7 is exactly why
     it cannot grow rightwards, so "why not 5" is drawn rather than asserted.
  B  five moments of the right finger walking rightwards. Three of them are
     collisions, and each collision draws the left finger's move as ONE arc
     from where it stood to where it lands — never a chain of single steps.
     The last one jumps three cells at once, which is the whole reason this
     runs in O(N) instead of O(N²).

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

W, H = 1280, 2054
MIN_TYPE = 24          # nothing smaller: 24 authored px = 12 px on screen

# --- palette: paper, ink, and three hues that share one soil ----------------
PAPER = "#F3EFE4"
INK = "#1A1813"
INK_SOFT = "#6E675A"
FLOOR = "#E7E0CC"
ROOM = "#FCFAF3"
C_JIA = "#B4532A"   # 磚紅
C_YI = "#2C6E63"    # 松綠
C_BING = "#3D4A7A"  # 藍靛

# --- the worked example, verbatim from the challenge's 〈範例〉 --------------
SONGS = [4, 9, 4, 7, 1, 9, 1]          # positions are 1-based throughout
N = len(SONGS)
# Exactly three numbers repeat, and there are exactly three hues to spend.
# The answer badge therefore cannot be a fourth hue — it is filled ink.
HUE = {4: C_JIA, 9: C_YI, 1: C_BING}


def walk():
    """The two-pointer sweep, 1-based, recording every step.

    Returns a list of dicts: right end, song, previous occurrence (or None),
    the left end before and after this step, whether the left end jumped, the
    window length, and the running best.
    """
    last, left, best, steps = {}, 1, 0, []
    for right in range(1, N + 1):
        song = SONGS[right - 1]
        prev = last.get(song)
        before = left
        jumped = prev is not None and prev >= left
        if jumped:
            left = prev + 1
        last[song] = right
        length = right - left + 1
        best = max(best, length)
        steps.append({"r": right, "song": song, "prev": prev, "l0": before,
                      "l": left, "jumped": jumped, "len": length, "best": best})
    return steps


STEPS = walk()
BEST = STEPS[-1]["best"]
# The frame in panel A is the window that stands when the right end reaches 6.
BEST_L, BEST_R = STEPS[5]["l"], STEPS[5]["r"]


def _self_check():
    """The plate prints specific positions and lengths, so the sweep behind it
    is checked against the challenge's own worked table rather than eyeballed.
    A drawing that is merely pretty and wrong is worse than no drawing."""
    # 〈範例說明〉's table: (right end, previous occurrence, left end, length)
    table = [(1, None, 1, 1), (2, None, 1, 2), (3, 1, 2, 2), (4, None, 2, 3),
             (5, None, 2, 4), (6, 2, 3, 4), (7, 5, 6, 2)]
    got = [(s["r"], s["prev"], s["l"], s["len"]) for s in STEPS]
    if got != table:
        raise SystemExit(f"sweep disagrees with the challenge table:\n {got}\n {table}")
    if BEST != 4:
        raise SystemExit(f"best window is {BEST}, the challenge says 4")
    if (BEST_L, BEST_R) != (3, 6) or SONGS[2:6] != [4, 7, 1, 9]:
        raise SystemExit(f"answer segment is {BEST_L}–{BEST_R}, the challenge says 3–6")
    # The two arcs panel A leans on: 9 at 2 & 6 blocks growing left, 1 at 5 & 7
    # blocks growing right. If either stops holding, panel A's caption lies.
    if not (SONGS[1] == SONGS[5] == 9 and SONGS[4] == SONGS[6] == 1):
        raise SystemExit("the blocking pairs 9@2,6 and 1@5,7 no longer hold")
    # And the left end never moves backwards — the claim panel B is built on.
    if any(a["l"] > b["l"] for a, b in zip(STEPS, STEPS[1:])):
        raise SystemExit("the left end moved backwards")


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


def arc(x1, y1, x2, apex, col, width=2.2, dash=None, head=False):
    """A hop drawn as one quadratic whose visible peak sits at `apex`.

    The control point is placed so the curve's own maximum lands on `apex`
    (peak = (y0 + 2·cy + y1)/4 for equal endpoints), because the thing being
    drawn is a single jump and the reader measures it by its height.
    """
    cy = 2 * apex - y1
    a = [f'd="M{x1},{y1} Q{(x1+x2)/2},{cy} {x2},{y1}"', 'fill="none"',
         f'stroke="{col}"', f'stroke-width="{width}"', 'stroke-linecap="round"']
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    add(f'<path {" ".join(a)}/>')
    if head:
        add(f'<path d="M{x2-7},{y1-11} L{x2+7},{y1-11} L{x2},{y1+2} Z" fill="{col}"/>')


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
T(64, 132, "接力帶剪在哪裡最長", 48, ls=8)
T(64, 178, "PLATE I — ONE TAPE, TWO FINGERS", 24, INK_SOFT, "PlexMono", ls=3)
add(f'<line x1="64" y1="206" x2="{W-64}" y2="206" stroke="{INK}" stroke-width="1" opacity="0.42"/>')

# ------------------------------------------------ A · 序列與最長的一段 ------
T(64, 254, "A — 這學期的點播序列，與剪得最長的一段", 30)

# The gap between cards is 26, not a hairline, because the answer frame has to
# stand *in* that gap without grazing the two cards it excludes.
CW, GAP = 130, 26
STEP = CW + GAP
SX = (W - (N * CW + (N - 1) * GAP)) / 2          # 143 — the row is centred
BOX_T, BOX_H = 470, 110
BOX_B = BOX_T + BOX_H


def cx(i):
    return SX + CW / 2 + (i - 1) * STEP


# The repeat arcs go up first so the cards sit on top of their feet.
PAIRS = [(1, 3, 4, 90), (2, 6, 9, 128), (5, 7, 1, 90)]
for a_, b_, song, lift in PAIRS:
    col = HUE[song]
    y0 = BOX_T - 30      # clears the answer frame's outer rule by 7 px
    arc(cx(a_), y0, cx(b_), y0 - lift, col, width=2.2, dash="7 5")
    for p in (a_, b_):
        add(f'<circle cx="{cx(p)}" cy="{y0}" r="7" fill="{col}"/>')
    mx, my = (cx(a_) + cx(b_)) / 2, y0 - lift
    add(f'<rect x="{mx-64}" y="{my-19}" width="128" height="38" fill="{PAPER}" '
        f'stroke="{col}" stroke-width="1.4"/>')
    T(mx, my + 9, f"編號 {song} 重複", 24, col, anchor="middle")

# The answer frame, drawn as a double rule in ink — the three hues are already
# spent on the three repeated songs, so the answer cannot borrow a fourth.
FL, FR = cx(BEST_L) - CW / 2 - 13, cx(BEST_R) + CW / 2 + 13
for o in (0, 7):
    add(f'<rect x="{FL-o}" y="{BOX_T-9-o}" width="{FR-FL+2*o}" height="{BOX_H+18+2*o}" '
        f'fill="none" stroke="{INK}" stroke-width="{2.6 if o == 0 else 1.2}"/>')

for i, song in enumerate(SONGS, 1):
    inside = BEST_L <= i <= BEST_R
    x = cx(i) - CW / 2
    add(f'<rect x="{x}" y="{BOX_T}" width="{CW}" height="{BOX_H}" '
        f'fill="{ROOM if inside else FLOOR}" stroke="{INK}" '
        f'stroke-width="{2.2 if inside else 1.2}" opacity="{1 if inside else 0.82}"/>')
    T(cx(i), BOX_T + 72, str(song), 46, HUE.get(song, INK), "PlexMono", 700, "middle")

T(SX - 18, BOX_B + 52, "位置", 24, INK_SOFT, anchor="end")
for i in range(1, N + 1):
    strong = BEST_L <= i <= BEST_R
    T(cx(i), BOX_B + 52, str(i), 26, INK if strong else INK_SOFT, "PlexMono",
      700 if strong else 400, "middle")

T((FL + FR) / 2, BOX_B + 106, f"最長不重播段 · 位置 {BEST_L} 到 {BEST_R} · 長度 {BEST}",
  30, INK, anchor="middle")

T(64, BOX_B + 162, "往左多含一格就吃到位置 2 的 9，和位置 6 的 9 撞上；", 27, INK_SOFT)
T(64, BOX_B + 200, "往右多含一格就吃到位置 7 的 1，和位置 5 的 1 撞上。", 27, INK_SOFT)
T(64, BOX_B + 238, "其他起點也一樣走不遠——從位置 1 出發，位置 3 的 4 就撞上位置 1 的 4。", 27, INK_SOFT)

# ---------------------------------------------- B · 雙指標怎麼走 ------------
BY = 850
add(f'<line x1="64" y1="{BY}" x2="{W-64}" y2="{BY}" stroke="{INK}" stroke-width="1" opacity="0.42"/>')
T(64, BY + 44, "B — 右端一格一格推；下面挑出左端有動作的那幾步", 30)

MCW, MGAP = 62, 8
MSTEP = MCW + MGAP
MSX = 412
STRIP_R = MSX + N * MCW + (N - 1) * MGAP          # 894


def mcx(i):
    return MSX + MCW / 2 + (i - 1) * MSTEP


T(MSX - 32, BY + 84, "位置", 24, INK_SOFT, anchor="end")
for i in range(1, N + 1):
    T(mcx(i), BY + 84, str(i), 24, INK_SOFT, "PlexMono", anchor="middle")

MOMENTS = [2, 3, 5, 6, 7]
ROW_H = 176
TY0 = 954

for k, r in enumerate(MOMENTS):
    s = STEPS[r - 1]
    ty = TY0 + k * ROW_H
    band_y = ty + 42
    st, sb = ty + 46, ty + 106

    # -- left column: the step number, then what happened, in three lines ----
    add(f'<circle cx="82" cy="{ty+56}" r="18" fill="none" stroke="{INK}" '
        f'stroke-width="1.4" opacity="0.55"/>')
    T(82, ty + 65, str(r), 24, INK_SOFT, "PlexMono", 700, "middle")
    T(116, ty + 64, f"右端推到位置 {r}", 28)
    if s["prev"] is None:
        T(116, ty + 100, f"編號 {s['song']} 沒出現過", 25, INK_SOFT)
        T(116, ty + 136, "左端不動", 25, INK_SOFT)
    else:
        T(116, ty + 100, f"編號 {s['song']} 上次在位置 {s['prev']}", 25, HUE[s["song"]])
        T(116, ty + 136, f"左端跳到位置 {s['l']}", 25, HUE[s["song"]], weight=700)

    # -- the jump, drawn as ONE arc from where the left end stood to where it
    #    lands. A chain of single steps would be the O(N²) picture; this is not
    #    that picture, so the arc is never subdivided.
    if s["jumped"]:
        col = HUE[s["song"]]
        arc(mcx(s["l0"]), band_y, mcx(s["l"]), ty + 14, col, width=2.6, head=True)
        # The previous occurrence is ringed, because the landing cell is
        # defined as "one past it" and nothing else.
        add(f'<circle cx="{mcx(s["prev"])}" cy="{band_y}" r="8" fill="{PAPER}" '
            f'stroke="{col}" stroke-width="2.4"/>')
        hop = s["l"] - s["l0"]
        label = f"左端一次跳 {hop} 格"
        if (mcx(s["l0"]) + mcx(s["l"])) / 2 < (MSX + STRIP_R) / 2:
            T(STRIP_R, ty + 26, label, 24, col, anchor="end")
        else:
            T(MSX, ty + 26, label, 24, col)

    # -- the strip ----------------------------------------------------------
    for i, song in enumerate(SONGS, 1):
        inside = s["l"] <= i <= r
        x = mcx(i) - MCW / 2
        add(f'<rect x="{x}" y="{st}" width="{MCW}" height="{sb-st}" '
            f'fill="{ROOM if inside else FLOOR}" stroke="{INK}" '
            f'stroke-width="{2.6 if i == r else (1.8 if inside else 0.9)}" '
            f'opacity="{1 if inside else 0.55}"/>')
        T(mcx(i), st + 42, str(song), 32, HUE.get(song, INK), "PlexMono", 700, "middle",
          op=None if inside else "0.55")

    # -- the two fingers ----------------------------------------------------
    for pos, name in ((s["l"], "左"), (r, "右")):
        px = mcx(pos)
        add(f'<path d="M{px-9},{sb+20} L{px+9},{sb+20} L{px},{sb+6} Z" fill="{INK}"/>')
        T(px, sb + 46, name, 26, INK, anchor="middle")

    # -- the length, and whether it ties the answer -------------------------
    top = s["len"] == BEST
    add(f'<rect x="930" y="{st+2}" width="176" height="58" fill="{INK if top else ROOM}" '
        f'stroke="{INK}" stroke-width="1.6"/>')
    T(948, ty + 88, "長度", 26, PAPER if top else INK_SOFT)
    T(1088, ty + 90, str(s["len"]), 34, PAPER if top else INK, "PlexMono", 700, "end")
    if top:
        T(1122, ty + 90, "最長", 26, INK)

NY = TY0 + len(MOMENTS) * ROW_H + 50
T(64, NY, "左端從頭到尾只往右走，不曾回頭：某個編號一旦造成重播，往左退只會讓它再回來。", 27, INK_SOFT)
T(64, NY + 42, "兩根手指各自最多走 7 格，整串紀錄掃一趟就結束。", 27, INK_SOFT)

T(W - 64, H - 66, "APCS020 · RELAY TAPE · FIG.1", 24, INK_SOFT, "PlexMono", anchor="end", ls=3)

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
(HERE / "plate020.html").write_text(
    f'<!doctype html><meta charset="utf-8">'
    f"<style>{css}html,body{{margin:0;padding:0;background:{PAPER};}}svg{{display:block;}}</style>"
    f"{svg}", encoding="utf-8")
print(f"wrote plate020.html  {W}×{H}  smallest type {min(s for s,_ in _sizes)}px")
