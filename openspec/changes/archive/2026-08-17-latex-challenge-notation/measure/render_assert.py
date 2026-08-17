#!/usr/bin/env python3
"""渲染判讀：對 render_observe.sh 的觀測結果套斷言牆。

用法::

    python3 openspec/changes/latex-challenge-notation/measure/render_assert.py
    python3 openspec/changes/latex-challenge-notation/measure/render_assert.py --self-test

與觀測腳本拆開，所以重跑觀測（版面高度會隨字型載入時機微幅浮動）不會讓斷言牆跟著漂。

斷言
====

1. **status** 必須是 ``OK``。``UNREACHABLE`` 要報成連不上站台，不能報成「頁面沒有公式」。
   這是 counting-trio 那次踩過的坑：設定錯誤被說成內容壞掉。
2. **mjx_count > 0**。抽樣的每一頁都該有公式。
3. **source_leaks 為空**。``\\le``、``\\times``、``^{`` 等字串出現在 innerText 裡，
   代表 LaTeX 沒被渲染，讀者看到的是原始碼。
4. **svg_display 全為 inline**。這是 29e381c 那條 CSS 修正還在生效的直接證據。
5. **densest**（逐頁）：公式最多的那一塊，行數必須少於 ``公式數 + 1``。
   修正失效時它會膨脹到至少 ``公式數 + 1`` 行。

   **不要**改成「高度小於行高的固定倍數」——那假設了最密集的區塊很短，而
   ``prize-order-code`` 那段本來就有 6 行文字，會被誤判成失效。門檻必須跟公式數連動。
6. **inline_proofs**（跨頁）：整份抽樣裡至少要有一個「含 2 個以上行內公式卻只佔 1 行」
   的區塊。這是正向證據——修正失效時每個公式各佔一行，這種區塊不可能存在。

   這條刻意是跨頁而不是逐頁。``quadratic-discriminant`` 的多公式段落本來就長到會自然
   換行，逐頁要求會把正常內容判成壞掉；``movie-ticket`` 的 3 個公式分散在 3 個表格
   儲存格，也不該因為「找不到多公式區塊」被判失敗。第 5 條逐頁抓退化，第 6 條跨頁
   立正向證據，兩條分工。
7. **bare_dollars**：只有 ``movie-ticket`` 該有錢字號（票價），且必須恰好 5 個。
   其他頁面出現裸錢字號代表 escape 漏了或公式沒配對成功。
8. **attempts**：觀測端會輪詢到公式渲染完成。嘗試次數逼近上限代表頁面異常慢，
   要說出來——那通常是下一個問題的前兆。

任何一條不過就 exit 1，並印出**全部**問題，不是第一個就停。
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
JSONL = HERE / "render-verification.jsonl"

LEAK_FREE = True
EXPECTED_DOLLARS = {"movie-ticket": 5}
MAX_ATTEMPTS = 12          # 與 render_observe.sh 的輪詢上限一致
SLOW_ATTEMPTS = 8          # 逼近上限就示警
MIN_DOC_LEN = 100          # 空殼頁約 25 字元；最短的題敘也有數百字元


def adjudicate(records: list[dict]) -> dict:
    problems: list[str] = []

    if not records:
        problems.append("觀測檔是空的——觀測腳本沒跑或全數失敗")

    for r in records:
        slug = r.get("slug", "（無 slug）")

        status = r.get("status")
        if status != "OK":
            problems.append(
                "%s 觀測未完成：status=%s，reason=%s"
                % (slug, status, r.get("reason", "（無 reason 欄位）"))
            )
            continue

        # 先問「這頁到底有沒有內容」，再問「公式渲染了沒」。順序反過來就會把
        # 「站台起錯了」報成「轉換把公式弄壞了」——實際踩過：`vitepress dev docs`
        # 讀到另一份設定，端出一個不噴錯的空殼，12 頁全數 mjx_count 0。
        doc_len = r.get("doc_len")
        if isinstance(doc_len, int) and doc_len < MIN_DOC_LEN:
            problems.append(
                "%s 的題敘面板只有 %d 個字元（門檻 %d）——這頁根本沒有內容，"
                "先確認站台起對了（本專案是 `vitepress dev`，root 在 repo 根目錄，"
                "不是 `vitepress dev docs`），不要當成公式壞掉" % (slug, doc_len, MIN_DOC_LEN)
            )
        elif r.get("mjx_count", 0) <= 0:
            problems.append("%s 沒有任何 mjx-container——公式沒被渲染" % slug)

        leaks = r.get("source_leaks") or []
        if LEAK_FREE and leaks:
            problems.append("%s 的內文出現 LaTeX 原始碼：%s" % (slug, ", ".join(leaks)))

        displays = r.get("svg_display") or []
        bad = [d for d in displays if d != "inline"]
        if bad:
            problems.append(
                "%s 的 mjx-container > svg computed display 是 %s，不是 inline"
                "（29e381c 的 CSS 修正失效）" % (slug, ", ".join(bad))
            )

        dense = r.get("densest")
        if dense and dense["lines"] >= dense["formulas"] + 1:
            problems.append(
                "%s 的 %s 含 %d 個行內公式卻佔了 %.2f 行（達到 公式數+1 的門檻）"
                "——公式被推到獨立一行了：「%s」"
                % (slug, dense["tag"], dense["formulas"], dense["lines"], dense.get("text", "")[:40])
            )

        attempts = r.get("attempts")
        if isinstance(attempts, int) and attempts >= SLOW_ATTEMPTS:
            problems.append(
                "%s 等了 %d 次輪詢才渲染出公式（上限 %d）——頁面異常慢，先查清楚再往下"
                % (slug, attempts, MAX_ATTEMPTS)
            )

        want = EXPECTED_DOLLARS.get(slug, 0)
        got = r.get("bare_dollars", 0)
        if got != want:
            problems.append(
                "%s 的內文錢字號數是 %d，期望 %d" % (slug, got, want)
            )

    # 正向證據，跨頁而非逐頁。修正失效時每個公式各佔一行，任何含 2 個公式的區塊
    # 都至少 3 行，整份抽樣不可能找得到 1 行的多公式區塊。
    #
    # **不要**把這條改回逐頁斷言。quadratic-discriminant 的每個多公式段落本來就長到
    # 會自然換行，逐頁要求「一定有 1 行的區塊」會把正常內容判成壞掉——那是斷言在假設
    # 版面，不是版面出問題。同理，movie-ticket 的 3 個公式分散在 3 個表格儲存格裡，
    # 「有公式卻沒有多公式區塊」也是合法版面，不再當成失敗。
    ok = [r for r in records if r.get("status") == "OK"]
    proofs = [
        (r["slug"], r["tightest"])
        for r in ok
        if r.get("tightest") and r["tightest"]["lines"] <= 1.0
    ]
    if ok and not proofs:
        problems.append(
            "整份抽樣裡沒有任何「含 2 個以上行內公式卻只佔 1 行」的區塊——"
            "找不到行內公式確實行內排版的正向證據（29e381c 的 CSS 修正可能失效）"
        )

    return {
        "observed": len(records),
        "inline_proofs": [
            {"slug": s, "tag": t["tag"], "formulas": t["formulas"], "lines": t["lines"]}
            for s, t in proofs
        ],
        "problems": problems,
        "verdict": "CLEAN" if not problems else "PROBLEMS",
    }


def _self_test() -> None:
    """負向控制：每一條斷言都要證明它會對壞資料觸發、對好資料不觸發。"""
    good = {
        "slug": "ok-page", "status": "OK", "attempts": 1, "doc_len": 800,
        "mjx_count": 12, "inline_count": 10,
        "svg_display": ["inline", "inline"], "source_leaks": [], "bare_dollars": 0,
        "multi_formula_blocks": 4,
        "tightest": {"tag": "li", "formulas": 4, "lines": 1.0, "text": "x"},
        "densest": {"tag": "li", "formulas": 9, "lines": 6.0, "text": "y"},
    }
    assert adjudicate([good])["verdict"] == "CLEAN", "乾淨的觀測不該報問題"

    injections = [
        ("連不上站台", {"slug": "p", "status": "UNREACHABLE", "reason": "open 失敗"}, "觀測未完成"),
        ("沒有公式", {**good, "mjx_count": 0}, "沒有任何 mjx-container"),
        ("整頁是空殼", {**good, "doc_len": 25, "mjx_count": 0}, "根本沒有內容"),
        ("原始碼外洩", {**good, "source_leaks": ["\\le"]}, "LaTeX 原始碼"),
        ("svg 變 block", {**good, "svg_display": ["block"]}, "不是 inline"),
        ("全抽樣都找不到單行多公式區塊",
         {**good, "tightest": {**good["tightest"], "lines": 3.0}}, "正向證據"),
        ("最密區塊膨脹", {**good, "densest": {"tag": "li", "formulas": 5, "lines": 6.0, "text": "y"}},
         "公式數+1"),
        ("渲染異常慢", {**good, "attempts": 9}, "輪詢"),
        ("多出裸錢字號", {**good, "bare_dollars": 3}, "錢字號數是 3"),
        ("空觀測檔", None, "觀測檔是空的"),
    ]
    for name, rec, needle in injections:
        result = adjudicate([] if rec is None else [rec])
        if result["verdict"] != "PROBLEMS":
            raise SystemExit("負向控制失敗 [%s]：斷言沒有觸發" % name)
        if not any(needle in p for p in result["problems"]):
            raise SystemExit(
                "負向控制失敗 [%s]：觸發了但訊息沒指出原因，實得 %s" % (name, result["problems"])
            )

    # movie-ticket 的票價是預期中的，不該被報成問題
    mt = {**good, "slug": "movie-ticket", "bare_dollars": 5}
    assert adjudicate([mt])["verdict"] == "CLEAN", "movie-ticket 的 5 個票價錢字號是預期值"
    mt_bad = {**good, "slug": "movie-ticket", "bare_dollars": 4}
    assert adjudicate([mt_bad])["verdict"] == "PROBLEMS", "票價少一個要抓得到"

    # 正向證據是跨頁的：一頁自然換行、另一頁有 1 行的多公式區塊，整體仍算通過。
    wraps = {**good, "slug": "wrapping-page", "tightest": {**good["tightest"], "lines": 2.0}}
    assert adjudicate([wraps, good])["verdict"] == "CLEAN", (
        "只要抽樣中有一頁立得起正向證據，另一頁自然換行不該被判失敗"
    )
    # 沒有多公式區塊的頁面（公式各在不同表格儲存格）本身不是失敗
    split = {**good, "slug": "table-page", "multi_formula_blocks": 0,
             "tightest": None, "densest": None}
    assert adjudicate([split, good])["verdict"] == "CLEAN", (
        "公式分散在不同區塊是合法版面，不該被報成版面被拆散"
    )

    print("self-test 通過（%d 條負向控制 + movie-ticket 正負兩例）" % len(injections))


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        _self_test()
        return 0
    if not JSONL.exists():
        print("找不到觀測檔 %s，請先跑 render_observe.sh" % JSONL)
        return 2
    records = [json.loads(line) for line in JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]
    result = adjudicate(records)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    (HERE / "render-verdict.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if result["verdict"] == "CLEAN" else 1


if __name__ == "__main__":
    sys.exit(main())
