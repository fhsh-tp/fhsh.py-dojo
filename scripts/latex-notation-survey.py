#!/usr/bin/env python3
"""題目頁數學記號盤點器。

用法::

    python3 scripts/latex-notation-survey.py            # 人可讀的分級清單
    python3 scripts/latex-notation-survey.py --json     # 機器可讀，供證物與比對使用
    python3 scripts/latex-notation-survey.py --self-test

掃描 ``docs/challenge/*.md`` 的 frontmatter 之後內文，依
``scripts/latex-notation-rules.json`` 的兩級黑名單分類。規則只有那一份，本檔與
``scripts/latex-notation.test.ts`` 各自實作掃描但共讀同一份規則。

掃描面的計算順序（順序錯了會產生假陽性，見 design 的「兩級記號黑名單與 lint 逃生門」）
==========================================================================

1. 取 frontmatter 結束標記之後的內文。沒有 frontmatter 的檔案，整份當內文——不靜默跳過。
2. 去掉 fenced code block（範例輸入／輸出是字面資料）。
3. 去掉圖片語法（``alt`` 不經 Markdown 渲染，寫 LaTeX 只會露出原始碼）。
4. 把跳脫過的 ``\\$`` 換成佔位符，免得它參與後面的配對。
5. 去掉 ``$$…$$``，再去掉 ``$…$``。
6. 剩下的 ``$`` 就是裸貨幣符號。

**先去 code fence 再去 ``$…$``** 是必要的：範例輸出裡的錢字號會與內文的公式錯配，
反過來做會把一整段內文吃掉。

兩級的差別只在**行內 code span 是否豁免**：

* A 級（``≤``、``≥``、``＜``、``＞``、``<=``、``>=``）連 code span 內都禁止。
* B 級（``×``、``−``、``·``、上標數字……）僅散文禁止，code span 內是字面圖形。

``--json`` 輸出契約
===================

頂層鍵：``total``、``converted``、``pending``、``clean``、``per_file``。

* ``converted`` —— 內文已有 LaTeX 且零違規
* ``pending``   —— 尚有違規
* ``clean``     —— 內文沒有數學記號也沒有 LaTeX，不需處理

``per_file`` 以檔名為鍵，每筆含：

* ``symbols``     —— 違規記號總數
* ``detail``      —— {記號: 次數}
* ``latex``       —— 內文中配對成功的 LaTeX 片段數
* ``bare_dollar`` —— 未跳脫且未配對的錢字號數
* ``violations``  —— [{line, tier, token}]，供守門測試以外的人工核對定位
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHALLENGE_DIR = ROOT / "docs" / "challenge"
RULES_PATH = ROOT / "scripts" / "latex-notation-rules.json"

FENCE_RE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.S | re.M)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)", re.S)
CODESPAN_RE = re.compile(r"(`+)(?:(?!\1).)*?\1", re.S)
DISPLAY_RE = re.compile(r"\$\$.*?\$\$", re.S)
# 行內公式：開頭的 $ 後面不接空白，結尾的 $ 前面不接空白，且不跨行。
# 這是 markdown-it 那一族的實際判準，也正是 movie-ticket 的 `$150 | … | $250`
# 為什麼沒有被吃掉的原因——每個錢字號前面都是空白，不是合法的結束定界符。
INLINE_RE = re.compile(r"\$(?!\s)(?:[^$\n\\]|\\.)*?(?<!\s)\$")
ESCAPED_DOLLAR = "\x00ESCAPED_DOLLAR\x00"


def load_rules(path: pathlib.Path = RULES_PATH) -> dict:
    rules = json.loads(path.read_text(encoding="utf-8"))
    return {
        "tier_a_symbols": rules["tierA"]["symbols"],
        "tier_a_sequences": rules["tierA"]["sequences"],
        "tier_b_symbols": rules["tierB"]["symbols"],
        "ignore_marker": rules["ignoreMarker"],
    }


def split_body(text: str) -> tuple[str, int]:
    """回傳 (內文, 內文起始行號)。行號 1-based，供違規定位用。

    沒有 frontmatter 的檔案整份當內文，不靜默跳過——靜默跳過會讓一個壞掉的檔案
    在盤點數字上看起來像「乾淨」。
    """
    if not text.startswith("---\n"):
        return text, 1
    end = text.find("\n---\n", 4)
    if end == -1:
        return text, 1
    head = text[: end + 5]
    return text[end + 5 :], head.count("\n") + 1


def _blank_out(pattern: re.Pattern[str], text: str) -> str:
    """把符合的片段換成等量的空白，保住行號與行內位移。"""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def scan_surfaces(body: str) -> tuple[str, str, int]:
    """回傳 (含 code span 的掃描面, 去掉 code span 的掃描面, 裸錢字號數)。

    兩個掃描面的行號與原文對齊，因為被移除的片段都換成等量空白。
    """
    stage = _blank_out(FENCE_RE, body)
    stage = _blank_out(IMAGE_RE, stage)
    stage = stage.replace(r"\$", ESCAPED_DOLLAR)
    stage = _blank_out(DISPLAY_RE, stage)
    stage = _blank_out(INLINE_RE, stage)
    bare_dollar = stage.count("$")
    with_spans = stage.replace(ESCAPED_DOLLAR, "  ")
    without_spans = _blank_out(CODESPAN_RE, with_spans)
    return with_spans, without_spans, bare_dollar


def count_latex(body: str) -> int:
    stage = _blank_out(FENCE_RE, body)
    stage = _blank_out(IMAGE_RE, stage)
    stage = stage.replace(r"\$", ESCAPED_DOLLAR)
    return len(DISPLAY_RE.findall(stage)) + len(INLINE_RE.findall(DISPLAY_RE.sub("", stage)))


def ignored_lines(body: str, marker: str, body_start: int) -> set[int]:
    """逃生門：帶標記的 HTML 註解，作用範圍是緊接的下一個非空行。"""
    out: set[int] = set()
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if marker in line and "<!--" in line:
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    out.add(body_start + j)
                    break
    return out


def find_violations(body: str, body_start: int, rules: dict) -> list[dict]:
    with_spans, without_spans, _ = scan_surfaces(body)
    skip = ignored_lines(body, rules["ignore_marker"], body_start)
    hits: list[dict] = []

    def sweep(surface: str, tokens: list[str], tier: str) -> None:
        for lineno, line in enumerate(surface.split("\n"), start=body_start):
            if lineno in skip:
                continue
            for token in tokens:
                for _ in range(line.count(token)):
                    hits.append({"line": lineno, "tier": tier, "token": token})

    sweep(with_spans, rules["tier_a_symbols"] + rules["tier_a_sequences"], "A")
    sweep(without_spans, rules["tier_b_symbols"], "B")
    hits.sort(key=lambda h: (h["line"], h["tier"], h["token"]))
    return hits


def survey_file(path: pathlib.Path, rules: dict) -> dict:
    raw = path.read_text(encoding="utf-8")
    body, body_start = split_body(raw)
    violations = find_violations(body, body_start, rules)
    _, _, bare_dollar = scan_surfaces(body)
    detail: dict[str, int] = {}
    for v in violations:
        detail[v["token"]] = detail.get(v["token"], 0) + 1
    return {
        "symbols": len(violations),
        "detail": detail,
        "latex": count_latex(body),
        "bare_dollar": bare_dollar,
        "violations": violations,
    }


def survey(directory: pathlib.Path = CHALLENGE_DIR) -> dict:
    rules = load_rules()
    per_file = {p.name: survey_file(p, rules) for p in sorted(directory.glob("*.md"))}
    pending = [n for n, r in per_file.items() if r["symbols"] > 0 or r["bare_dollar"] > 0]
    converted = [
        n
        for n, r in per_file.items()
        if n not in pending and r["latex"] > 0
    ]
    clean = [n for n in per_file if n not in pending and n not in converted]
    return {
        "total": len(per_file),
        "converted": len(converted),
        "pending": len(pending),
        "clean": len(clean),
        "converted_files": converted,
        "pending_files": pending,
        "clean_files": clean,
        "per_file": per_file,
    }


def render_human(result: dict) -> str:
    lines = [
        "總 %d ｜ 已完成 %d ｜ 待轉 %d ｜ 無記號 %d"
        % (result["total"], result["converted"], result["pending"], result["clean"]),
        "",
        "=== 待轉換（依違規數排序）===",
    ]
    pend = sorted(
        ((n, result["per_file"][n]) for n in result["pending_files"]),
        key=lambda kv: -kv[1]["symbols"],
    )
    for name, r in pend:
        lines.append(
            "  %-34s %3d  %-38s 裸$=%d"
            % (name, r["symbols"], str(r["detail"]), r["bare_dollar"])
        )
    if not pend:
        lines.append("  （無）")
    lines += ["", "=== 已完成 ==="]
    for name in result["converted_files"]:
        lines.append("  %-34s latex=%d" % (name, result["per_file"][name]["latex"]))
    lines += ["", "=== 內文無數學記號（不需處理）===", "  " + " ".join(result["clean_files"])]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# 自我檢查。每一條都附負向控制：先確認乾淨輸入不觸發，再確認髒輸入確實觸發。
# 沒有負向控制等於沒有檢查。
# --------------------------------------------------------------------------

def _self_test() -> None:
    rules = load_rules()

    def scan(text: str) -> list[dict]:
        body, start = split_body(text)
        return find_violations(body, start, rules)

    fm = "---\nid: x\n---\n"

    cases = [
        # (名稱, 內文, 期望違規 token 清單)
        ("A 級在散文中", "約束是 1 ≤ n ≤ 10。", ["≤", "≤"]),
        ("A 級在 code span 內也要抓", "約束 `1 <= n <= 10`。", ["<=", "<="]),
        ("A 級的全形比較符", "值域 ＜ 100。", ["＜"]),
        ("B 級在散文中要抓", "面積是 k × k。", ["×"]),
        ("B 級在 code span 內豁免", "圖上的 `·` 表示閒置。", []),
        ("LaTeX 片段不算違規", "約束是 $1 \\le n \\le 10$。", []),
        ("code fence 內不掃", "```\n1 <= n\n```\n", []),
        ("圖片 alt 不掃", "![圖 1：`n <= 5` 的樣子](/a.png)", []),
        ("逃生門跳過下一行", "<!-- latex-lint-ignore-next-line -->\n寫 `x <= 3` 是合法的。", []),
        ("逃生門只跳一行", "<!-- latex-lint-ignore-next-line -->\n`x <= 3`\n`y >= 4`", [">="]),
    ]
    for name, body, expect in cases:
        got = [v["token"] for v in scan(fm + body)]
        if got != expect:
            raise SystemExit("self-test 失敗 [%s]：期望 %s，實得 %s" % (name, expect, got))

    # 行號必須指向原文，不是掃描面的相對位置
    hits = scan(fm + "第一段沒問題。\n\n這裡有 1 ≤ n。")
    if not hits or hits[0]["line"] != 6:
        raise SystemExit("self-test 失敗 [行號]：期望 6，實得 %s" % (hits[0]["line"] if hits else "無違規"))

    # 裸錢字號：貨幣要抓，跳脫過的與配對成功的都不算
    def bare(text: str) -> int:
        body, _ = split_body(text)
        return scan_surfaces(body)[2]

    for name, body, expect in [
        ("裸貨幣要抓", "票價 $150 元。", 1),
        ("跳脫過的不算", "票價 \\$150 元。", 0),
        ("配對成功的不算", "範圍 $n \\ge 1$。", 0),
        ("範例區塊裡的不算", "```\n$150\n```\n", 0),
    ]:
        got = bare(fm + body)
        if got != expect:
            raise SystemExit("self-test 失敗 [%s]：期望 %d，實得 %d" % (name, expect, got))

    # 沒有 frontmatter 的檔案整份當內文
    if not scan("直接就是內文，1 ≤ n。"):
        raise SystemExit("self-test 失敗 [無 frontmatter]：應把整份當內文，卻掃出零違規")

    print("self-test 全數通過（%d 個掃描案例 + 4 個裸錢字號案例 + 行號 + 無 frontmatter）" % len(cases))


def main() -> int:
    ap = argparse.ArgumentParser(description="題目頁數學記號盤點器")
    ap.add_argument("--json", action="store_true", help="輸出機器可讀的 JSON")
    ap.add_argument("--self-test", action="store_true", help="執行自我檢查後結束")
    args = ap.parse_args()

    if args.self_test:
        _self_test()
        return 0

    result = survey()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
