"""e2e 冒煙測試的可機械定址輸出。

為什麼需要這支：2026-08-15 的 e2e 走完之後，觀察結果（列表頁有幾個 id、
三個 `/c/` 別名各回什麼狀態碼、題目頁骨架是否齊備）原本只存在於對話裡。
把它們寫進矩陣時，`scripts/trace-lint.py` 立刻指出那些數字沒有出處——
這與本 change 前後犯過四次的同一個錯完全同型（量測跑了、輸出沒落盤）。

所以 e2e 的觀察也必須落盤。這支腳本重跑一次可機械化的部分並寫出
`measure/e2e-smoke.json`，讓 W7／W8 的每個數字都有位址。

前置：`pnpm preview:cf` 已在 localhost:8788 執行，且已手動跑過
`pnpm build:redirects` 並把產物同步進 dist（見 W8：preview:cf 自己不做這件事）。
瀏覽器互動的部分（貼程式碼、按提交）不在本腳本內，那些結果由
`measure.sh` 寫進 `measure/browser-verification.jsonl`。
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGE = os.path.dirname(HERE)
BASE = os.environ.get("BASE", "http://localhost:8788")

TRIO = [
    ("apcs015", "ap-layout-plan", "基地台佈點規劃"),
    ("apcs016", "marquee-display-count", "跑馬燈顯示計數"),
    ("apcs017", "fair-token-exchange", "園遊會代幣兌換"),
]

#: 題目頁不得出現的洩題詞彙。2×3 區塊是 apcs015 的關鍵洞見（決策 D4 要求不說破），
#: 棋類詞彙則是情境設計的硬約束（決策 D6）。
LEAK_TERMS = ["2×3", "3×2", "騎士", "棋"]


def fetch(path, allow_redirect=False):
    """回傳 (status, final_url, body)。不跟隨轉址時 status 會是 302。"""
    url = BASE + path

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **kw):
            return None

    opener = urllib.request.build_opener() if allow_redirect else urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(url, timeout=30) as resp:
            return resp.status, resp.geturl(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, getattr(e, "url", url), ""


def main():
    report = {
        "purpose": "e2e 冒煙測試中可機械化的觀察，讓 W7／W8 的數字有位址",
        "base": BASE,
        "problems": [],
    }

    # ── 列表頁 ────────────────────────────────────────────────
    status, _url, body = fetch("/apcs-challenges", allow_redirect=True)
    ids = sorted(set(re.findall(r"apcs\d{3}", body)))
    listing = {
        "status": status,
        "apcs_ids_found": len(ids),
        "apcs_ids": ids,
        "trio_titles_present": {t: (t in body) for _id, _slug, t in TRIO},
    }
    report["listing"] = listing
    if status != 200:
        report["problems"].append("列表頁狀態碼 %s" % status)
    for _id, _slug, title in TRIO:
        if title not in body:
            report["problems"].append("列表頁缺少標題 %s" % title)

    # ── /c/ 短網址別名 ────────────────────────────────────────
    aliases = []
    for cid, slug, _title in TRIO:
        st, _u, _b = fetch("/c/" + cid)
        st2, final, _b2 = fetch("/c/" + cid, allow_redirect=True)
        expected = "/challenge/" + slug
        ok = st == 302 and final.endswith(expected) and st2 == 200
        aliases.append({
            "id": cid,
            "redirect_status": st,
            "followed_status": st2,
            "final_path": final.replace(BASE, ""),
            "expected_path": expected,
            "ok": ok,
        })
        if not ok:
            report["problems"].append(
                "%s 的別名不正確：轉址碼 %s、最終 %s（期望 302 → %s）" % (cid, st, final, expected))
    report["aliases"] = aliases

    # ── 題目頁骨架 ────────────────────────────────────────────
    pages = []
    for cid, slug, title in TRIO:
        st, _u, html = fetch("/challenge/" + slug, allow_redirect=True)
        leaks = [term for term in LEAK_TERMS if term in html]
        rec = {
            "id": cid,
            "slug": slug,
            "status": st,
            "title_present": title in html,
            "id_badge_present": cid in html,
            "leak_terms_found": leaks,
        }
        pages.append(rec)
        if st != 200:
            report["problems"].append("%s 頁面狀態碼 %s" % (cid, st))
        if leaks:
            report["problems"].append("%s 頁面命中洩題詞彙 %s" % (cid, leaks))
    report["pages"] = pages

    out = os.path.join(HERE, "e2e-smoke.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)

    print("列表頁：狀態 %s，找到 %d 個 apcs id，三個標題 %s" % (
        listing["status"], listing["apcs_ids_found"],
        "全部present" if all(listing["trio_titles_present"].values()) else "有缺"))
    for a in aliases:
        print("  /c/%s → %s，跟隨後 %s，最終 %s %s" % (
            a["id"], a["redirect_status"], a["followed_status"], a["final_path"],
            "✓" if a["ok"] else "✗"))
    for p in pages:
        print("  %s 頁面 %s，洩題詞彙 %s" % (
            p["id"], p["status"], p["leak_terms_found"] or "零命中"))
    print("\n已寫出 %s" % os.path.relpath(out, CHANGE))
    if report["problems"]:
        for x in report["problems"]:
            print("  ✗ %s" % x)
        return 1
    print("e2e 可機械化觀察全部通過。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
