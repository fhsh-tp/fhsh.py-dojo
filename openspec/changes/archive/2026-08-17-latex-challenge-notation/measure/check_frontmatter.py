#!/usr/bin/env python3
"""驗證 LaTeX 轉換完全沒有碰到受保護區段。

用法::

    python3 openspec/changes/latex-challenge-notation/measure/check_frontmatter.py <baseline-ref>
    python3 openspec/changes/latex-challenge-notation/measure/check_frontmatter.py --self-test

``baseline-ref`` 是轉換開始前的 git ref（本 change 用建立守門工具的那個 commit）。
逐檔取兩個受保護區段的 SHA-256，與 baseline 比對：

* **frontmatter** —— ``params``／``generator``／``testcase_plan`` 進測資池雜湊，動了要重建 pool 與 WASM
* **fenced code block** —— 範例輸入／輸出是字面資料，一個字元都不該變

這兩件事用腳本查比用人或 agent 查可靠：它們是位元組層級的等值判斷，沒有判斷空間。
守門測試（``scripts/latex-notation.test.ts``）查的是「有沒有殘留記號」，查不到「有沒有
改到不該改的地方」——兩者互補，缺一不可。

為什麼比雜湊而不是看 ``git diff`` 的行號
=========================================

``git diff`` 的 hunk 標頭給的是**變更後**的行號，而 frontmatter 的長度本身可能因為
別的原因改變；用行號判斷「這個 hunk 在不在 frontmatter 裡」要先假設 frontmatter 長度
沒變，那正是我們要證明的事——不能拿結論當前提。直接對兩邊各自切出 frontmatter 再比
雜湊，沒有這個循環。

frontmatter 的定義與 ``scripts/latex-notation-survey.py`` 的 ``split_body`` 一致：
從檔首的 ``---`` 到第一個 ``\\n---\\n``（含）。沒有 frontmatter 的檔案視為空 frontmatter，
兩邊都是空的就算通過——但會在輸出裡標記出來，不靜默略過。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
REL_DIR = "docs/challenge"

FENCE_RE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.S | re.M)


def frontmatter_of(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return text[: end + 5] if end != -1 else ""


def body_of(text: str) -> str:
    fm = frontmatter_of(text)
    return text[len(fm) :]


def fences_of(text: str) -> str:
    """把內文所有 fenced code block 串起來，用分隔線隔開。

    只看內文——frontmatter 裡的 ``generator``／``starter_code`` 由 frontmatter 那條檢查覆蓋，
    在這裡重複計入會讓失敗訊息說不清是哪一個區段出問題。
    """
    return "\n\x1e\n".join(FENCE_RE.findall(body_of(text)))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_show(ref: str, rel_path: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{rel_path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def check(ref: str) -> dict:
    rows = []
    for path in sorted((ROOT / REL_DIR).glob("*.md")):
        rel = f"{REL_DIR}/{path.name}"
        before = git_show(ref, rel)
        if before is None:
            # 新增的檔案沒有 baseline。本 change 不新增題目頁，所以這是異常，要說出來。
            rows.append({"file": path.name, "status": "NO_BASELINE", "regions": []})
            continue
        after = path.read_text(encoding="utf-8")
        regions = []
        for name, extract in (("frontmatter", frontmatter_of), ("code_fences", fences_of)):
            b, a = extract(before), extract(after)
            regions.append(
                {
                    "region": name,
                    "status": "OK" if digest(b) == digest(a) else "CHANGED",
                    "before": digest(b),
                    "after": digest(a),
                    "empty": b == "",
                }
            )
        changed = [r["region"] for r in regions if r["status"] != "OK"]
        rows.append(
            {
                "file": path.name,
                "status": "OK" if not changed else "CHANGED",
                "changed_regions": changed,
                "regions": regions,
            }
        )
    bad = [r for r in rows if r["status"] != "OK"]
    return {
        "baseline_ref": ref,
        "checked": len(rows),
        "changed": len(bad),
        "problems": [
            "%s：%s 被改動" % (r["file"], "、".join(r.get("changed_regions") or ["（無 baseline）"]))
            for r in bad
        ],
        "files_without_frontmatter": [
            r["file"]
            for r in rows
            if any(g["region"] == "frontmatter" and g["empty"] for g in r["regions"])
        ],
        "files_without_code_fences": [
            r["file"]
            for r in rows
            if any(g["region"] == "code_fences" and g["empty"] for g in r["regions"])
        ],
        "verdict": "PASS" if not bad else "FAIL",
        "rows": rows,
    }


def _self_test() -> None:
    """負向控制：確認改動 frontmatter 真的會被抓到，改動內文不會。"""
    sample = "---\nid: x\ntitle: t\n---\n內文 1 ≤ n。\n"
    assert frontmatter_of(sample) == "---\nid: x\ntitle: t\n---\n"

    body_edit = sample.replace("1 ≤ n", "$1 \\le n$")
    assert digest(frontmatter_of(sample)) == digest(frontmatter_of(body_edit)), (
        "改內文不該影響 frontmatter 雜湊"
    )

    fm_edit = sample.replace("title: t", "title: tt")
    assert digest(frontmatter_of(sample)) != digest(frontmatter_of(fm_edit)), (
        "改 frontmatter 必須被抓到——這條若不觸發，整個檢查等於沒做"
    )

    assert frontmatter_of("沒有 frontmatter 的檔案") == ""
    # frontmatter 未閉合時視為沒有 frontmatter，而不是把整份當 frontmatter
    assert frontmatter_of("---\nid: x\n沒有結束標記") == ""

    # code fence：只抓內文的，且改動要被抓到
    fenced = "---\nid: x\ngenerator: |\n  print(1)\n---\n說明 1 ≤ n。\n\n```\n5\n42 7\n```\n"
    assert fences_of(fenced) == "```\n5\n42 7\n```", fences_of(fenced)
    assert "print(1)" not in fences_of(fenced), "frontmatter 裡的程式碼不該計入 code fence 區段"

    prose_only = fenced.replace("1 ≤ n", "$1 \\le n$")
    assert digest(fences_of(fenced)) == digest(fences_of(prose_only)), (
        "只改內文散文不該影響 code fence 雜湊"
    )
    fence_edited = fenced.replace("42 7", "42 8")
    assert digest(fences_of(fenced)) != digest(fences_of(fence_edited)), (
        "改到範例資料必須被抓到——這條若不觸發，等於沒查 code fence"
    )

    print(
        "self-test 通過（內文改動不觸發、frontmatter 改動觸發、無 frontmatter、未閉合、"
        "code fence 正負兩例、frontmatter 程式碼不重複計入）"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--self-test":
        _self_test()
        return 0
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
