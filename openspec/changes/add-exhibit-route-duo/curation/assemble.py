"""把策展產物組裝成兩個題目檔（frontmatter + 題面）。

執行前必須先跑過 plan013.py / plan014.py（產生 literals/）。
輸出：docs/challenge/exhibit-route-rebuild.md、docs/challenge/pinball-track-predict.md

規則：
  - literal 區塊逐 byte 取自 literals/，不手貼（change B 教訓⑨）
  - 組裝後檢查禁字（D6），命中即中止
  - starter_code 一律空字串（2026-08-06 維護者決策，見 bracket-check-challenges spec）
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIT = os.path.join(HERE, "literals")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DOCS = os.path.join(REPO, "docs", "challenge")

BANNED = [
    "堆疊", "stack", "樹", "tree", "節點", "node", "子樹", "subtree",
    "前序", "中序", "後序", "preorder", "inorder", "postorder",
    "走訪", "traversal", "遞迴", "recursion", "位元", "二進位", "binary", "二元",
    "佇列", "queue", "雜湊", "hash",
]

SPECS = {
    "exhibit-route-rebuild": {
        "id": "apcs013",
        "title": "展場動線重建",
        "difficulty": "medium",
        "algorithm": "exhibit_route_rebuild",
        "description": "由兩位導覽員的打卡序還原第三位的打卡序",
        "tags": ["模擬", "字串"],
        "input_budget": 63488,
        "prefix": "c013",
        "generator": "gen013.py",
        "reference": "ref013.py",
        "page": "page013.md",
    },
    "pinball-track-predict": {
        "id": "apcs014",
        "title": "彈珠台軌道預測",
        "difficulty": "hard",
        "algorithm": "pinball_track_predict",
        "description": "預測第 I 顆彈珠落入哪一個袋子",
        "tags": ["數學", "模擬"],
        "input_budget": None,
        "prefix": "c014",
        "generator": "gen014.py",
        "reference": "ref014.py",
        "page": "page014.md",
    },
}


def indent(text, pad):
    return "\n".join((pad + ln) if ln else "" for ln in text.rstrip("\n").split("\n"))


def build(slug, spec):
    literals = []
    for i in range(1, 21):
        path = os.path.join(LIT, "%s_%02d.txt" % (spec["prefix"], i))
        with open(path) as fh:
            literals.append(fh.read())

    gen = open(os.path.join(HERE, spec["generator"])).read()
    ref = open(os.path.join(HERE, spec["reference"])).read()
    page = open(os.path.join(HERE, spec["page"])).read()

    lines = ["---", "layout: challenge", "id: " + spec["id"], "title: " + spec["title"],
             "difficulty: " + spec["difficulty"], "category: apcs", "type: competition", "tags:"]
    for t in spec["tags"]:
        lines.append("  - " + t)
    lines.append("algorithm: " + spec["algorithm"])
    lines.append("description: " + spec["description"])
    if spec["input_budget"]:
        lines.append("input_budget: %d" % spec["input_budget"])
    lines += ["params:", "  t:", "    type: int", "    min: 1", "    max: 1", "testcase_plan:"]
    for lit in literals:
        lines.append("  - literal: |")
        lines.append(indent(lit, "      "))
    lines.append("generator: |")
    lines.append(indent(gen, "  "))
    lines.append("reference_solution: |")
    lines.append(indent(ref, "  "))
    lines.append('starter_code: ""')
    lines.append("---")
    lines.append("")
    doc = "\n".join(lines) + page.rstrip("\n") + "\n"

    lowered = doc.lower()
    hits = {b for b in BANNED if b.lower() in lowered}
    # slug 與 algorithm 亦須過檢
    for probe in (slug, spec["algorithm"]):
        hits |= {b for b in BANNED if b.lower() in probe.lower()}
    if hits:
        raise SystemExit("禁字命中（%s）：%s" % (slug, ", ".join(sorted(hits))))

    out = os.path.join(DOCS, slug + ".md")
    with open(out, "w") as fh:
        fh.write(doc)

    # 回讀驗證：frontmatter 的 literal 區塊必須與來源逐 byte 相同
    body = open(out).read()
    blocks = re.findall(r"  - literal: \|\n((?:      .*\n|\n)+)", body)
    if len(blocks) != 20:
        raise SystemExit("%s: 解析到 %d 個 literal 區塊（應為 20）" % (slug, len(blocks)))
    for i, blk in enumerate(blocks):
        got = "".join(ln[6:] if ln.startswith("      ") else ln
                      for ln in blk.splitlines(keepends=True))
        if got != literals[i]:
            raise SystemExit("%s: 第 %d 個 literal 區塊與來源不符" % (slug, i + 1))
    return out, len(doc)


if __name__ == "__main__":
    for slug, spec in SPECS.items():
        path, size = build(slug, spec)
        print("wrote %s (%d bytes)" % (os.path.relpath(path, REPO), size))
    print("禁字檢查通過、literal 逐 byte 回讀一致。")
    sys.exit(0)
