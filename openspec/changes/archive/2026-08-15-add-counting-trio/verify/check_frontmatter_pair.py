#!/usr/bin/env python3
"""add-counting-trio 交叉驗證器（tasks.md 2.4）。

對三個題目頁 ``docs/challenge/*.md`` 做五道獨立檢查，任何一道失敗即 exit 1：

  A. **三方輸出相符**：對每題 20 筆 literal，逐筆以獨立子行程執行題目頁的
     ``generator`` 與 ``reference_solution``，再與 ``curation/semantics0XX.py``
     的獨立參照比對。三者必須逐位元組相同。
  B. **四鍵逐位元組相同**：題目頁中 ``algorithm`` / ``params`` / ``input_budget``
     / ``testcase_plan`` 四鍵所佔的整段，必須與 ``curation/out/frontmatter0XX.yaml``
     的位元組完全一致（不是解析後相等，是原始位元組相等）。
  C. **starter_code 為空字串**。
  D. **禁用術語掃描**：對題目頁**完整內容**（frontmatter + 內文）掃描，掃描器
     直接 import ``curation/assemble.py`` 的 ``scan_banned``（先跑它的
     self-test 確認掃描器真的會叫），另補掃鐵律點名但 assemble 清單未涵蓋的詞
     與棋類詞彙。**所有命中一律列出**，包含疑似誤報——由維護者判斷，不由本檔預判。
  E. **數字追溯**：把題面內文出現的每一個數字抓出來，逐一對回 trace-matrix 的
     fact id。允許集合一律**由 semantics 模組與 testcase_plan 機械導出**，不手抄。

  F. **frontmatter 欄位集合一致**：三題鍵集合必須相同且 ``tags`` 非空。
  G. **效能提醒措辭（鎖 S7）**：對題目頁**內文**（不含 frontmatter）掃描「時間限制」
     一類把成本軸講成時間的措辭，命中即 FAIL；另反向要求：凡提到成本上限的
     「提醒」段，必須逐字出現「執行量上限」。S7 這條規範起因於題面曾把死因誤寫成
     時間限制、被瀏覽器實測推翻，但在此之前沒有任何機械防線擋得住改回去。
     掃描器自帶負向控制（``timing_self_test``），沒有負向控制的檢查等於沒有檢查。

用法：
    python3 openspec/changes/add-counting-trio/verify/check_frontmatter_pair.py
    python3 .../check_frontmatter_pair.py --json       # 附機器可讀摘要（stdout）
    python3 .../check_frontmatter_pair.py --json-out   # 另落成 verify/frontmatter-pair.json

``--json-out`` 是追溯矩陣的位址來源：S 段（S1／S4／S5／S6／S9）引用的數字
一律指向該檔的鍵，而不是本檔的 stdout。只印 stdout 等於沒有出處。
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANGE = HERE.parent
CURATION = CHANGE / "curation"
REPO = CHANGE.parent.parent.parent
DOCS = REPO / "docs" / "challenge"

FOUR_KEYS = ("algorithm", "params", "input_budget", "testcase_plan")

CHALLENGES = [
    {"tag": "015", "id": "apcs015", "slug": "ap-layout-plan", "title": "基地台佈點規劃"},
    {"tag": "016", "id": "apcs016", "slug": "marquee-display-count", "title": "跑馬燈顯示計數"},
    {"tag": "017", "id": "apcs017", "slug": "fair-token-exchange", "title": "園遊會代幣兌換"},
]

FAILURES: list[str] = []
NOTES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ── frontmatter 解析（不依賴 PyYAML 也能跑，但有就用它交叉驗證）────────────
def split_page(path: Path) -> tuple[str, str]:
    """回傳 (frontmatter 原文, 內文原文)。frontmatter 不含前後的 --- 行。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit("%s 不是以 --- 開頭" % path)
    end = text.index("\n---\n", 3)
    return text[4:end + 1], text[end + len("\n---\n"):]


def parse_block_scalar(fm: str, key: str) -> str | None:
    """取出 ``key: |`` 之後的區塊純量（去掉共同縮排）。找不到回傳 None。"""
    m = re.search(r"^%s: \|\-?\n" % re.escape(key), fm, re.M)
    if not m:
        return None
    rest = fm[m.end():]
    out = []
    for line in rest.split("\n"):
        if line.strip() == "":
            out.append("")
            continue
        if not line.startswith("  "):
            break
        out.append(line[2:])
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def parse_literals(fm: str) -> list[str]:
    """取出 testcase_plan 底下每一筆 ``- literal: |`` 的原文（含結尾換行）。"""
    m = re.search(r"^testcase_plan:\n", fm, re.M)
    if not m:
        return []
    rest = fm[m.end():]
    lits, cur, collecting = [], [], False
    for line in rest.split("\n"):
        if re.match(r"^\S", line):          # 回到頂層鍵 → testcase_plan 結束
            break
        if re.match(r"^  - literal: \|\-?$", line):
            if collecting:
                lits.append("\n".join(cur) + "\n")
            cur, collecting = [], True
            continue
        if collecting:
            if line.startswith("      "):
                cur.append(line[6:])
            elif line.strip() == "":
                cur.append("")
            else:
                lits.append("\n".join(cur) + "\n")
                cur, collecting = [], False
    if collecting:
        while cur and cur[-1] == "":
            cur.pop()
        lits.append("\n".join(cur) + "\n")
    return [l for l in lits if l.strip()]


def four_key_slice(fm: str) -> str:
    """題目頁 frontmatter 中，從 ``algorithm:`` 起到四鍵區段結束為止的原始位元組。"""
    m = re.search(r"^algorithm:", fm, re.M)
    if not m:
        raise SystemExit("找不到 algorithm: 鍵")
    start = m.start()
    rest = fm[start:]
    # 四鍵之後的第一個頂層鍵（generator / reference_solution / starter_code…）
    tail = re.search(r"\n(?=(?!%s)[A-Za-z_][\w-]*:)" % "|".join(FOUR_KEYS), rest)
    end = start + (tail.start() + 1 if tail else len(rest))
    return fm[start:end]


# ── A. 三方輸出比對 ────────────────────────────────────────────────────
def run_code(code: str, stdin_text: str) -> tuple[str, str, int]:
    proc = subprocess.run(
        [sys.executable, "-c", code],
        input=stdin_text, capture_output=True, text=True, timeout=300,
    )
    return proc.stdout, proc.stderr, proc.returncode


def norm(s: str) -> str:
    """比對用正規化：去掉結尾空白行，其餘逐位元組保留。"""
    return s.rstrip("\n").rstrip()


def semantics_expected(tag: str, sem, literal: str) -> str:
    if tag == "016":
        n, k = sem.parse(literal)
        return sem.render_expected(n, k)
    return sem.render_expected(int(literal.split()[0]))


def check_outputs(ch: dict, fm: str, sem) -> int:
    gen = parse_block_scalar(fm, "generator")
    ref = parse_block_scalar(fm, "reference_solution")
    lits = parse_literals(fm)
    name = "%s %s" % (ch["id"], ch["slug"])
    if gen is None:
        fail("%s：frontmatter 沒有 generator" % name)
        return 0
    if ref is None:
        fail("%s：frontmatter 沒有 reference_solution" % name)
        return 0
    if len(lits) != 20:
        fail("%s：testcase_plan literal 筆數 = %d，期望 20" % (name, len(lits)))
    if gen.strip() == ref.strip():
        fail("%s：generator 與 reference_solution 程式碼完全相同（必須是獨立實作）" % name)

    ok = 0
    for i, lit in enumerate(lits, 1):
        g_out, g_err, g_rc = run_code(gen, lit)
        r_out, r_err, r_rc = run_code(ref, lit)
        s_out = semantics_expected(ch["tag"], sem, lit)
        g, r, s = norm(g_out), norm(r_out), norm(s_out)
        if g_rc != 0:
            fail("%s 第 %d 筆（輸入 %r）：generator 非零離開碼 %d\n      stderr: %s"
                 % (name, i, lit.strip(), g_rc, g_err.strip()[:400]))
            continue
        if r_rc != 0:
            fail("%s 第 %d 筆（輸入 %r）：reference_solution 非零離開碼 %d\n      stderr: %s"
                 % (name, i, lit.strip(), r_rc, r_err.strip()[:400]))
            continue
        if g == r == s:
            ok += 1
            continue

        def brief(x: str) -> str:
            lines = x.split("\n")
            return repr(x) if len(lines) <= 3 else repr("\n".join(lines[:2]) + " …(%d 行)" % len(lines))

        fail("%s 第 %d 筆不相符（輸入 %r）\n"
             "      generator          = %s\n"
             "      reference_solution = %s\n"
             "      semantics%s        = %s"
             % (name, i, lit.strip(), brief(g), brief(r), ch["tag"], brief(s)))
    return ok


# ── D. 禁用術語掃描 ────────────────────────────────────────────────────
# 兩層補掃。assemble.py 的 BANNED_* 沒有涵蓋鐵律 4 點名的全部詞，也沒有棋類詞彙。
#
#   HARD_*：鐵律 4 逐字點名的詞 ＋ 明確的棋類詞彙 → 命中即 FAIL。
#   SOFT_*：容易誤報但值得看一眼的詞（單字「模」會被「規模」吃到、「象」會被
#           「現象」吃到）→ 只列出、不判 FAIL，交維護者裁決。
HARD_ZH = [
    "進位", "二進位", "十進位", "十二進位", "取模", "模數", "模運算",
    "質因數", "動態規劃", "時間複雜度", "空間複雜度",
    "棋", "棋盤", "西洋棋", "象棋", "圍棋", "騎士", "皇后", "國王", "城堡",
    "主教", "士兵", "馬步", "日字", "將軍",
]
HARD_EN = [
    "knight", "chess", "chessboard", "rook", "bishop", "pawn",
    "modulo", "modular", "modulus", "big o", "o(n", "o(1)", "o(log",
]
SOFT_ZH = [
    "模", "因數", "倍數", "指數", "次方", "冪", "同餘", "數列", "級數",
    "最佳化", "剪枝", "分治", "遞推", "狀態轉移", "子問題",
    "象", "士", "兵", "帥", "炮", "馬", "后",
]
SOFT_EN = [
    "queen", "amortized", "asymptotic", "combinatorics",
    "enumerate all", "state transition", "binary representation",
]


def _scan(text: str, zh: list[str], en: list[str]) -> list[tuple[str, int]]:
    low = text.lower()
    hits = [(t, text.count(t)) for t in zh if text.count(t)]
    hits += [(t, low.count(t)) for t in en if low.count(t)]
    return hits


def scan_hard(text: str) -> list[tuple[str, int]]:
    return _scan(text, HARD_ZH, HARD_EN)


def scan_soft(text: str) -> list[tuple[str, int]]:
    return _scan(text, SOFT_ZH, SOFT_EN)


# ── G. 效能提醒措辭（鎖 S7）────────────────────────────────────────────
# S7：題面的效能提醒必須把天花板講成「執行量上限」，不得講成時間限制。
# 理由是實測：E8 那條路線死於 op 計數器，不是死於 deadline；先前題面寫「時間限制」
# 是被瀏覽器實測推翻的錯誤敘述。這裡把那條規範變成兩道機械檢查（禁 + 必）。
#
# **只掃內文**：frontmatter 內含 generator／reference_solution 的程式碼與註解，
# 那不是給學生看的文案，掃它只會製造誤報。
#
# 詞庫刻意只收**不可能有合理用法**的措辭。單獨的「時間」「秒」「慢」一律不收——
# 「同一時間」「每秒」這類寫法完全合法，收進來就是誤殺。
TIMING_ZH = [
    "時間限制", "限制時間", "時間上限", "上限時間", "時限",
    "逾時", "超時", "執行時間", "運行時間", "運算時間",
    "秒數上限", "毫秒上限", "時間內跑完", "時間就會被",
]
# 英文一律用邊界比對：不加邊界的話 "tle" 會被 "title"／"little" 吃到。
TIMING_EN = [
    "time limit", "time-limit", "timelimit", "time budget",
    "timeout", "time out", "deadline", "wall clock", "wall-clock",
    "runtime limit", "elapsed time", "tle",
]

# 反向（必須出現）：提到成本天花板的「提醒」段，一定要逐字寫「執行量上限」。
HINT_MARKER = "提醒"
REQUIRED_HINT_PHRASE = "執行量上限"
# 只有真的在談天花板的提醒段才受這條約束；純情境提醒不該被硬塞術語。
COST_MARKERS = ("上限", "限制", "超出", "超過", "撐不住")


def scan_timing(body: str) -> list[tuple[str, int]]:
    """回傳內文命中的「時間限制」類措辭 [(詞, 次數)]；空清單 = 乾淨。"""
    low = body.lower()
    hits = [(t, body.count(t)) for t in TIMING_ZH if body.count(t)]
    for t in TIMING_EN:
        pat = r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(t).replace(r"\ ", r"[\s_-]+")
        n = len(re.findall(pat, low))
        if n:
            hits.append((t, n))
    return hits


def hint_paragraphs(body: str) -> list[str]:
    """內文中談到成本天花板的「提醒」段（段落＝空行分隔）。"""
    out = []
    for para in re.split(r"\n\s*\n", body):
        if HINT_MARKER in para and any(m in para for m in COST_MARKERS):
            out.append(" ".join(para.split()))
    return out


def check_performance_hint(body: str) -> dict:
    """G 檢查的純函式部分：回傳結構化結果，``problems`` 非空即 FAIL。"""
    timing = scan_timing(body)
    paras = hint_paragraphs(body)
    missing = [p for p in paras if REQUIRED_HINT_PHRASE not in p]
    problems = []
    if timing:
        problems.append("內文出現把成本軸講成時間的措辭 %s——S7 規定必須寫「%s」"
                        % ([t for t, _ in timing], REQUIRED_HINT_PHRASE))
    for p in missing:
        problems.append("談到成本天花板的提醒段沒有逐字寫「%s」：%r"
                        % (REQUIRED_HINT_PHRASE, p[:120]))
    return {
        "timing_terms": [t for t, _ in timing],
        "timing_term_hits": timing,
        "cost_hint_paragraphs": len(paras),
        "cost_hint_paragraphs_with_required_phrase": len(paras) - len(missing),
        "uses_op_limit_phrase": bool(paras) and not missing,
        "required_phrase": REQUIRED_HINT_PHRASE,
        "problems": problems,
    }


# 負向控制：每一條規則都要有「注入錯誤 → 真的會叫」的證明。
TIMING_PROBES = [
    ("這題有嚴格的時間限制。", "時間限制"),
    ("後段測資會超過時限。", "時限"),
    ("寫得慢會逾時。", "逾時"),
    ("程式的執行時間會太長。", "執行時間"),
    ("this challenge has a time limit", "time limit"),
    ("your program will hit the deadline", "deadline"),
    ("the judge reports TLE", "tle"),
    ("watch the wall-clock", "wall-clock"),
]
# 乾淨對照：合法用法不得被誤殺。
TIMING_CLEAN = [
    "> 提醒：這個寫法會超出單筆測資的執行量上限。",
    "每秒鐘燈號會切換一次，同一時間只有一格會亮。",   # 「時間」「秒」單獨出現合法
    "> 提醒：輸入的兩個數字之間只有一個空白。",        # 提醒段但不談天花板 → 不受反向約束
]


def timing_self_test() -> None:
    """G 檢查的掃描器必須真的會叫；不會叫的檢查等於沒有檢查。"""
    for probe, want in TIMING_PROBES:
        got = check_performance_hint(probe)
        if want not in got["timing_terms"]:
            raise SystemExit("G 檢查 self-test 失敗：%r 應命中 %r，實得 %s"
                             % (probe, want, got["timing_terms"]))
        if not got["problems"]:
            raise SystemExit("G 檢查 self-test 失敗：%r 命中卻沒判 FAIL" % probe)
    for clean in TIMING_CLEAN:
        got = check_performance_hint(clean)
        if got["problems"]:
            raise SystemExit("G 檢查 self-test 失敗：乾淨樣本 %r 被誤殺（%s）"
                             % (clean, got["problems"]))
    # 反向規則的負向控制：談天花板卻不寫「執行量上限」必須叫
    vague = "> 提醒：後段測資的 n 會很大，這個寫法會超出單筆測資的上限。"
    got = check_performance_hint(vague)
    if not got["problems"] or got["uses_op_limit_phrase"]:
        raise SystemExit("G 檢查 self-test 失敗：含糊的『超出上限』未被要求寫出「%s」"
                         % REQUIRED_HINT_PHRASE)


# ── E. 數字追溯 ────────────────────────────────────────────────────────
NUM_RE = re.compile(r"[-−]?\d[\d,]*")

# 中文數字也是數字，追溯不能只抓阿拉伯數字（「十億」「三格」「兩台」都是量值主張）
CJK_DIGIT = {"零": 0, "一": 1, "二": 2, "兩": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}
CJK_UNIT = {"十": 10, "百": 100, "千": 1000, "萬": 10 ** 4, "億": 10 ** 8}
CJK_RE = re.compile(r"[零一二兩三四五六七八九十百千萬億]+")


def cjk_value(s: str) -> int | None:
    """把常見中文數字寫法換算成整數；看不懂就回 None（由維護者人工判斷）。"""
    total, section, digit, seen = 0, 0, None, False
    for ch in s:
        if ch in CJK_DIGIT:
            digit = CJK_DIGIT[ch]
            seen = True
        elif ch in CJK_UNIT:
            u = CJK_UNIT[ch]
            seen = True
            if u >= 10 ** 4:
                section = (section + (digit or 0)) or 1
                total += section * u
                section, digit = 0, None
            else:
                section += (digit if digit is not None else 1) * u
                digit = None
        else:
            return None
    if not seen:
        return None
    return total + section + (digit or 0)


def body_numbers(body: str) -> list[tuple[int, str]]:
    """回傳 [(數值, 原文片段)]，含表格、程式區塊、行內碼中的每一個數字。"""
    out = []
    for m in NUM_RE.finditer(body):
        raw = m.group(0)
        val = int(raw.replace(",", "").replace("−", "-"))
        ctx = body[max(0, m.start() - 24):m.end() + 24].replace("\n", "⏎")
        out.append((val, "%s  ⟨…%s…⟩" % (raw, ctx)))
    return out


def body_cjk_numbers(body: str) -> list[tuple[int, str]]:
    out = []
    for m in CJK_RE.finditer(body):
        raw = m.group(0)
        val = cjk_value(raw)
        if val is None:
            continue
        ctx = body[max(0, m.start() - 20):m.end() + 20].replace("\n", "⏎")
        out.append((val, "%s  ⟨…%s…⟩" % (raw, ctx)))
    return out


def allowed_map(tag: str, sem, lits: list[str]) -> dict[int, str]:
    """由 semantics 模組與 testcase_plan 機械導出「允許的數字 → fact id」。"""
    a: dict[int, str] = {}

    def put(v, fid):
        a.setdefault(int(v), fid)

    if tag == "015":
        for dr, dc in sem.OFFSETS:            # 干擾表八列
            put(dr, "E1（干擾偏移表）")
            put(dc, "E1（干擾偏移表）")
        for k in range(1, 9):                 # 範例輸出八行
            put(sem.answer_line(k), "E1（第 %d 行答案）" % k)
        for k in range(1, 6):                 # 小規模答案表的邊長欄（D4）
            put(k, "D4（答案表邊長 k = %d）" % k)
        put(int(lits[0].split()[0]), "E2／E3（第 1 筆 literal ＝ 範例輸入）")
        put(sem.N_MIN, "D7／E7（n 下界）")
        put(sem.N_MAX, "D7／E7（n 上界 1000）")

    elif tag == "016":
        n0, k0 = sem.parse(lits[0])
        put(n0, "F2（第 1 筆 literal n）")
        put(k0, "F2（第 1 筆 literal k）")
        put(sem.answer(n0, k0), "F2／F1（第 1 筆答案）")
        put(n0 - k0, "F1（自由格數 n−k）")
        put(sem.MOD, "F1（模數 1000000007）")
        put(0, "F2（k = 0 邊界）")
        put(1, "F1（k = n 時答案 1；亦為 n 下界）")
        put(1000000, "F2／016 I/O 契約（n 上界）")
        for i in range(1, n0 - k0 + 1):       # 「第 1／2／3 格」序數
            put(i, "F1（自由格逐格展開的序數）")
        put(2, "F1（每格 2 種狀態）")

    elif tag == "017":
        n0 = int(lits[0].split()[0])
        put(n0, "G2（第 1 筆 literal）")
        put(sem.exchanges_formula(n0), "G2（第 1 筆答案）")
        put(12, "D5（兌換率固定 12）")
        cur = math.factorial(n0)
        put(cur, "G1（n = %d 的排隊順序種數）" % n0)
        step = 0
        while cur % 12 == 0:
            cur //= 12
            step += 1
            put(cur, "G1（第 %d 次兌換後的枚數）" % step)
            put(step, "G1（第 %d 次兌換的序數／級數）" % step)
        put(cur % 12, "G1（最後一次分批後剩下的零頭）")
        put(step + 1, "G1（最高換到的級數）")
        put(0, "G1（第一次就換不成時輸出 0）")
        put(1, "G1（第 1 級／n 下界）")
        put(1000000000, "G2（n 上界 10 億）")
    return a


# ── 主流程 ────────────────────────────────────────────────────────────

REQUIRED_KEYS = [
    "layout", "id", "title", "difficulty", "category", "type", "tags",
    "description", "algorithm", "params", "input_budget", "testcase_plan",
    "generator", "reference_solution", "starter_code",
]


def check_frontmatter_fields(challenges):
    """F 檢查：三題的 frontmatter 欄位集合必須一致，且 tags 不得為空。

    2026-08-15 的稽核發現 apcs017 的 tags 是空陣列，而另外兩題都是
    ["數學"]。矩陣當時完全沒有追蹤 tags，所以沒有任何自動檢查會叫。
    這裡守的是**欄位完整性**這一整類，不是那一格。
    """
    problems = []
    detail = {"required_key_count": len(REQUIRED_KEYS), "required_keys": REQUIRED_KEYS,
              "per_challenge": {}}
    for ch in challenges:
        path = CHANGE.parent.parent.parent / "docs" / "challenge" / (ch["slug"] + ".md")
        text = path.read_text(encoding="utf-8")
        fm = text.split("---", 2)[1]
        keys = re.findall(r"^([a-z_]+):", fm, re.M)
        missing = [k for k in REQUIRED_KEYS if k not in keys]
        extra = [k for k in keys if k not in REQUIRED_KEYS]
        mtags = re.search(r"^tags:[ \t]*(.*)$", fm, re.M)
        tags_inline = mtags.group(1).strip() if mtags else None
        detail["per_challenge"][ch["id"]] = {
            "key_count": len(keys),
            "keys": keys,
            "missing": missing,
            "extra": extra,
            "tags_nonempty": bool(mtags) and (
                tags_inline not in ("", "[]")
                or fm[mtags.end():].lstrip("\n").startswith("  - ")
            ),
        }
        if missing:
            problems.append("%s：缺少 frontmatter 鍵 %s" % (ch["id"], missing))
        if extra:
            problems.append("%s：出現未預期的 frontmatter 鍵 %s" % (ch["id"], extra))
        m = re.search(r"^tags:[ \t]*(.*)$", fm, re.M)
        if m is not None:
            inline = m.group(1).strip()
            rest = fm[m.end():].lstrip("\n")
            if inline in ("", "[]") and not rest.startswith("  - "):
                problems.append("%s：tags 為空——三題應一致標記" % ch["id"])
    key_sets = {tuple(v["keys"]) for v in detail["per_challenge"].values()}
    detail["key_sets_identical"] = len(key_sets) == 1
    detail["problems"] = problems
    return problems, detail

def main() -> int:
    want_json = "--json" in sys.argv
    want_json_out = "--json-out" in sys.argv
    assemble = load_module(CURATION / "assemble.py", "cnt_assemble")
    assemble.scanner_self_test()
    print("[掃描器 self-test] assemble.scan_banned 對 %d 個 probe 全部命中，"
          "乾淨樣本零誤判 → 掃描器確實會叫" % len(assemble.SCANNER_PROBES))
    timing_self_test()
    print("[掃描器 self-test] G 檢查（S7 措辭）對 %d 個時間類 probe 全部命中、"
          "%d 個乾淨樣本零誤判，含糊的『超出上限』也會被要求寫出「%s」"
          % (len(TIMING_PROBES), len(TIMING_CLEAN), REQUIRED_HINT_PHRASE))
    print("[禁用清單規模] assemble BANNED_EN=%d／BANNED_ZH=%d；本檔補掃 "
          "HARD_ZH=%d／HARD_EN=%d（命中即 FAIL）、SOFT_ZH=%d／SOFT_EN=%d（僅列出）"
          % (len(assemble.BANNED_EN), len(assemble.BANNED_ZH),
             len(HARD_ZH), len(HARD_EN), len(SOFT_ZH), len(SOFT_EN)))
    print()

    summary = {}
    for ch in CHALLENGES:
        tag, name = ch["tag"], "%s %s（%s）" % (ch["id"], ch["title"], ch["slug"])
        page = DOCS / ("%s.md" % ch["slug"])
        if not page.exists():
            fail("%s：找不到題目頁 %s" % (name, page))
            continue
        raw = page.read_text(encoding="utf-8")
        fm, body = split_page(page)
        sem = load_module(CURATION / ("semantics%s.py" % tag), "cnt_sem%s" % tag)
        lits = parse_literals(fm)
        rec = {"file": str(page)}

        print("=" * 78)
        print("%s" % name)
        print("  檔案：%s" % page)
        print("=" * 78)

        # --- A ---
        ok = check_outputs(ch, fm, sem)
        rec["triple_ok"] = ok
        print("  [A] 三方輸出相符筆數：%d / %d" % (ok, len(lits)))

        # --- B ---
        frag_path = CURATION / "out" / ("frontmatter%s.yaml" % tag)
        frag = frag_path.read_bytes()
        sliced = four_key_slice(fm).encode("utf-8")
        if sliced == frag:
            print("  [B] 四鍵逐位元組相同：PASS（%d bytes，對照 %s）"
                  % (len(frag), frag_path.name))
            rec["four_key_bytes"] = "identical(%d)" % len(frag)
            rec["four_key_bytes_n"] = len(frag)
            rec["four_key_identical"] = True
        else:
            import difflib
            d = "\n".join(list(difflib.unified_diff(
                frag.decode("utf-8").splitlines(), sliced.decode("utf-8").splitlines(),
                fromfile=str(frag_path), tofile=str(page) + " (四鍵切片)", lineterm=""))[:40])
            fail("%s：四鍵區段與 %s 位元組不同（片段 %d bytes vs 題目頁 %d bytes）\n%s"
                 % (name, frag_path.name, len(frag), len(sliced), d))
            rec["four_key_bytes"] = "DIFFER"
            rec["four_key_bytes_n"] = len(frag)
            rec["four_key_identical"] = False
            print("  [B] 四鍵逐位元組相同：FAIL")
        # 逐鍵確認四鍵都真的在該切片內、且未被拆散
        missing = [k for k in FOUR_KEYS if not re.search(r"^%s:" % k, fm, re.M)]
        if missing:
            fail("%s：frontmatter 缺少鍵 %s" % (name, missing))

        # --- C ---
        m = re.search(r'^starter_code:[ \t]*(.*)$', fm, re.M)
        sc = m.group(1).strip() if m else None
        if sc in ('""', "''"):
            print("  [C] starter_code 為空字串：PASS（原文 %s）" % sc)
            rec["starter_code"] = "empty"
        else:
            fail("%s：starter_code 不是空字串（原文 %r）" % (name, sc))
            rec["starter_code"] = repr(sc)
            print("  [C] starter_code 為空字串：FAIL")

        # --- D ---
        hits_full = assemble.scan_banned(raw)
        hits_body = assemble.scan_banned(body)
        hard_full, hard_body = scan_hard(raw), scan_hard(body)
        soft_full, soft_body = scan_soft(raw), scan_soft(body)
        rec["banned"] = {"assemble_full": hits_full, "assemble_body": hits_body,
                         "hard_full": hard_full, "hard_body": hard_body,
                         "soft_full": soft_full, "soft_body": soft_body}

        def show(h):
            return "；".join("%s×%d" % x for x in h) if h else "零命中"

        print("  [D] assemble.scan_banned（全頁含 frontmatter）：%s"
              % (hits_full if hits_full else "零命中"))
        print("      assemble.scan_banned（僅題面內文）：%s"
              % (hits_body if hits_body else "零命中"))
        print("      HARD 補掃（鐵律 4 點名詞＋棋類，全頁）：%s" % show(hard_full))
        print("      HARD 補掃（僅內文）：%s" % show(hard_body))
        print("      SOFT 補掃（易誤報、僅列出不判 FAIL，全頁）：%s" % show(soft_full))
        print("      SOFT 補掃（僅內文）：%s" % show(soft_body))
        for t, c in soft_full:
            NOTES.append("%s 全頁命中 SOFT 詞 %r ×%d（可能為誤報，請維護者判斷）"
                         % (ch["id"], t, c))
        if hits_full:
            fail("%s：全頁命中 assemble 禁用術語 %s" % (name, hits_full))
        if hard_full:
            fail("%s：全頁命中 HARD 補掃詞 %s" % (name, [t for t, _ in hard_full]))

        # --- G ---（S7：效能提醒的措辭，只掃內文）
        hint = check_performance_hint(body)
        rec["performance_hint"] = hint
        print("  [G] 效能提醒措辭（S7）：時間類措辭 %s；談天花板的提醒段 %d 段，"
              "其中含「%s」者 %d 段"
              % (hint["timing_terms"] or "零命中", hint["cost_hint_paragraphs"],
                 REQUIRED_HINT_PHRASE, hint["cost_hint_paragraphs_with_required_phrase"]))
        for p in hint["problems"]:
            fail("%s：%s" % (name, p))

        # --- E ---
        allowed = allowed_map(tag, sem, lits)
        nums = body_numbers(body) + body_cjk_numbers(body)
        unmatched = [(v, ctx) for v, ctx in nums if v not in allowed]
        distinct = sorted({v for v, _ in nums})
        rec["numbers"] = {"total": len(nums), "distinct": distinct,
                          "distinct_count": len(distinct),
                          "unmatched": sorted({v for v, _ in unmatched}),
                          "unmatched_count": len({v for v, _ in unmatched})}
        print("  [E] 內文數字：共 %d 個、相異 %d 種" % (len(nums), len(distinct)))
        for v in distinct:
            if v in allowed:
                print("      %-12s → %s" % (v, allowed[v]))
        if unmatched:
            seen = set()
            for v, ctx in unmatched:
                if v in seen:
                    continue
                seen.add(v)
                fail("%s：內文數字 %s 對不回任何 fact id\n      出處：%s" % (name, v, ctx))
            print("      對不回 fact id：%s" % sorted(seen))
        else:
            print("      對不回 fact id：無")
        print()
        summary[ch["id"]] = rec

    print("=" * 78)
    print("相符筆數彙總")
    for ch in CHALLENGES:
        r = summary.get(ch["id"], {})
        print("  %s %-22s 三方相符 %s / 20" % (ch["id"], ch["slug"], r.get("triple_ok", "?")))
    if NOTES:
        print("\n待維護者判斷的補掃命中（本檔不預判是否誤報）：")
        for n in NOTES:
            print("  - %s" % n)
    fprob, fdetail = check_frontmatter_fields(CHALLENGES)
    summary["frontmatter_fields"] = fdetail
    if want_json:
        print("\nJSON:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    if want_json_out:
        out = HERE / "frontmatter-pair.json"
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        print("\n已寫出 %s" % out)
    if fprob:
        for x in fprob:
            fail(x)
    else:
        print("  [F] frontmatter 欄位完整性：三題鍵集合一致、tags 皆非空")

    if FAILURES:
        print("\n" + "!" * 78)
        print("FAIL：共 %d 項" % len(FAILURES))
        for f in FAILURES:
            print("  ✗ %s" % f)
        return 1
    print("\nPASS：三題 A/B/C/D/E/F/G 七道檢查全數通過。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
