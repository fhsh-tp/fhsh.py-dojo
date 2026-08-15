"""把 staging e2e 冒煙測試的原始觀測收成一份帶斷言牆的 ``staging-e2e.json``。

為什麼要這一支：``staging-e2e.jsonl`` 是瀏覽器實測的逐筆紀錄，本身沒有任何契約。
沒有斷言牆的話，「全綠」只是一句散文，下一個人得自己重讀 25 筆去判斷哪些數字算通過。
這支腳本把「什麼叫通過」寫成程式碼，違約寫進 ``problems``，
交給 ``verify/check_measure_json.py`` 這道 meta 檢查把關。

量測對象是 staging 站台（Cloudflare Pages），不是本機 dev server：
本機 ``vitepress dev`` 不送 COOP/COEP，沒有 SharedArrayBuffer 就沒有中斷，
apcs015 的負向控制在那裡量到的東西不是同一個量。

執行：
  python3 measure/staging_e2e_assemble.py             # 讀 jsonl，寫 staging-e2e.json
  python3 measure/staging_e2e_assemble.py --self-test # 負向控制（含正向控制）
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "staging-e2e.jsonl")
OUT = os.path.join(HERE, "staging-e2e.json")

BASE = "https://staging.fhsh-py-dojo.pages.dev"
DEPLOYED_COMMIT = "41d6ee7770e44c2964172a802fe96ed23b92f395"  # staging HEAD（PR #35 的 merge commit）
OBSERVED_ON = "2026-08-16"

# 六條正解路線：三題的 reference_solution，加 apcs015 的三種同演算法寫法。
# 後三者是 n 上界由 3000 下修為 1000 的**理由本身**——刀鋒消失的證據就是
# 這三種寫法在真瀏覽器裡同生共死，全部 20/20。
POSITIVE = {
    "015-reference", "015-rowscan-plain", "015-rowscan-helper",
    "015-rowscan-sum", "016-reference", "017-reference",
}
# 一條必死路線：逐格掃描。它要死，而且要死得乾淨。
NEGATIVE = "015-cellscan-NEGATIVE"
# 第 9 筆測資是 n=249。第 8 筆是 n=72（5,278,547 ops，過）；n=249 是 216,759,740 ops，
# 為 10,000,000 上限的 21.68 倍。生死線落在這兩筆之間是本題成本鑑別的設計核心。
FIRST_FAIL_INDEX = 9
ROWS = 20

# 已撤回的探針：freshness 記錄裡的 no_k4_row 搜尋整頁文字，因此也命中了
# 「範例輸出」區塊——那裡本來就該列出 k=4、k=5 的答案。這個 false 是探針寫錯，
# 不是部署有問題。取而代之的是 freshness_table，它只讀「邊長 k」那張表的列。
RETRACTED = {"freshness.no_k4_row": "整頁搜尋會命中範例輸出區塊；由 freshness_table 取代"}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def audit(records):
    """回傳 (違規敘述清單, 統計 dict)。"""
    problems = []
    by = {}
    for r in records:
        by.setdefault(r.get("check"), []).append(r)

    # --- 頁面層：上架、短網址別名、頁面掛載 ---------------------------------
    for kind, expect_n in (("listing", 6), ("alias", 3), ("mount", 3)):
        got = by.get(kind, [])
        if len(got) != expect_n:
            problems.append("%s 應有 %d 筆觀測，實得 %d 筆" % (kind, expect_n, len(got)))
        for r in got:
            if r.get("status") != "OK":
                problems.append("%s 失敗：%s" % (kind, json.dumps(r, ensure_ascii=False)))

    # --- 提交層：六條正解全過、一條必死路線真的死 ---------------------------
    submits = {r.get("label"): r for r in by.get("submit", [])}
    missing = (POSITIVE | {NEGATIVE}) - set(submits)
    if missing:
        problems.append("缺少提交紀錄：%s" % ", ".join(sorted(missing)))
    # 先看 status。measure.sh 失敗時吐的是 {"status":"FAILED","reason":...}，
    # 沒有 rows／score；只比對分數的話，七次提交全部連錯站台會被報成
    # 「七條正解都沒拿到 20/20」，把設定錯誤說成題目壞掉。
    for label, r in sorted(submits.items()):
        if r.get("status") != "OK":
            problems.append("提交 %s 未完成：%s"
                            % (label, r.get("reason", "（無 reason 欄位）")))
    for label in sorted(POSITIVE & set(submits)):
        r = submits[label]
        if r.get("status") != "OK":
            continue
        if r.get("rows") != ROWS or r.get("score") != ROWS:
            problems.append("正解路線 %s 未取得 %d/%d：rows=%s score=%s verdicts=%s"
                            % (label, ROWS, ROWS, r.get("rows"), r.get("score"),
                               r.get("verdicts")))
    if NEGATIVE in submits and submits[NEGATIVE].get("status") == "OK":
        r = submits[NEGATIVE]
        v = r.get("verdicts", "")
        if r.get("rows") != ROWS:
            problems.append("負向控制 rows=%s，應為 %d" % (r.get("rows"), ROWS))
        if r.get("score", ROWS) >= ROWS:
            problems.append("負向控制竟然全過（score=%s）——成本鑑別已失效" % r.get("score"))
        # 部分給分必須留著。整組歸零代表 worker 死掉、已賺到的結果被一起丟棄，
        # 那是另一種失敗，不是本題設計的乾淨 TLE。
        if r.get("score") == 0:
            problems.append("負向控制 score=0：疑似 worker 非乾淨死亡，已賺到的結果被丟棄")
        if len(v) != ROWS:
            problems.append("負向控制 verdicts 長度 %d，應為 %d" % (len(v), ROWS))
        else:
            head, tail = v[:FIRST_FAIL_INDEX - 1], v[FIRST_FAIL_INDEX - 1:]
            if set(head) != {"A"}:
                problems.append("負向控制前 %d 筆應全 AC，實得 %r"
                                % (FIRST_FAIL_INDEX - 1, head))
            if set(tail) != {"T"}:
                problems.append("負向控制第 %d 筆起應全 TLE，實得 %r"
                                % (FIRST_FAIL_INDEX, tail))

    # --- 洩題層：正解不得出現在部署產物中，且探針本身要能響 -----------------
    leaks = by.get("leak", [])
    if len(leaks) != 3:
        problems.append("leak 應有 3 筆（三題各一），實得 %d 筆" % len(leaks))
    for r in leaks:
        for k, hit in (r.get("hits") or {}).items():
            if hit:
                problems.append("%s 洩漏答案特徵 %s" % (r.get("slug"), k))
        if r.get("failed"):
            problems.append("%s 有 %d 個資源抓取失敗，探針覆蓋不完整：%s"
                            % (r.get("slug"), len(r["failed"]), r["failed"][:1]))
    ctrl = by.get("leak_control", [])
    if len(ctrl) != 1:
        problems.append("leak_control 應有 1 筆，實得 %d 筆" % len(ctrl))
    for r in ctrl:
        c = r.get("control") or {}
        # 沒有正向控制就等於沒有檢查：若這兩條也是 false，上面那一片乾淨
        # 只能證明探針壞了。
        for k in ("title_zh", "body_prose"):
            if not c.get(k):
                problems.append("洩題探針正向控制 %s 未命中——乾淨結果不可採信" % k)

    # --- 新鮮度層：部署的必須是本次 change 的最終決策，不是舊草稿 -----------
    fresh = by.get("freshness", [])
    if len(fresh) != 1:
        problems.append("freshness 應有 1 筆，實得 %d 筆" % len(fresh))
    for r in fresh:
        for k in ("n_bound_1000", "no_n_bound_3000", "perf_note_ops",
                  "perf_note_not_time", "table_k3"):
            if not r.get(k):
                problems.append("新鮮度檢查 %s 未通過，部署內容疑為舊版" % k)
    ft = by.get("freshness_table", [])
    if len(ft) != 1:
        problems.append("freshness_table 應有 1 筆，實得 %d 筆" % len(ft))
    for r in ft:
        rows = r.get("rows") or []
        if not r.get("found"):
            problems.append("頁面上找不到「邊長 k」那張表")
        elif [x[0] for x in rows] != ["1", "2", "3"]:
            problems.append("答案表列數不是 k=1..3：%r" % (rows,))

    stats = {
        "records": len(records),
        "by_check": {k: len(v) for k, v in sorted(by.items())},
        "positive_routes": len(POSITIVE & set(submits)),
        "negative_route_score": submits.get(NEGATIVE, {}).get("score"),
        "negative_route_verdicts": submits.get(NEGATIVE, {}).get("verdicts"),
    }
    return problems, stats


def self_test():
    """負向控制：每一道斷言各注入一份壞資料，確認都被抓；好資料確認不誤殺。"""
    good = load(RAW)
    base_problems, _ = audit(good)
    ok = not base_problems
    print("  %-28s %-6s %s" % ("正向控制（真實觀測）", "PASS" if ok else "FAIL",
                               "零違規" if ok else base_problems[0]))
    failures = [] if ok else ["正向控制失敗：真實觀測被判違規 —— %s" % base_problems[0]]

    def mutate(fn):
        import copy
        rs = copy.deepcopy(good)
        fn(rs)
        return rs

    def find(rs, **kw):
        for r in rs:
            if all(r.get(k) == v for k, v in kw.items()):
                return r
        raise AssertionError(kw)

    injections = [
        ("正解掉一筆", lambda rs: find(rs, label="016-reference").__setitem__("score", 19),
         "未取得 20/20"),
        # 這一條是真的踩到過：staging_smoke.sh 早先沒有 export BASE，
        # 七次提交全部連到 localhost:8788，斷言牆把它報成「正解沒拿到 20/20」。
        ("提交沒接上站台", lambda rs: (find(rs, label="015-reference").__setitem__(
            "status", "FAILED"),
            find(rs, label="015-reference").__setitem__("reason", "open failed")),
         "未完成：open failed"),
        ("必死路線全過", lambda rs: (find(rs, label=NEGATIVE).__setitem__("score", 20),
                                 find(rs, label=NEGATIVE).__setitem__(
                                     "verdicts", "A" * ROWS)), "成本鑑別已失效"),
        ("必死路線整組歸零", lambda rs: (find(rs, label=NEGATIVE).__setitem__("score", 0),
                                  find(rs, label=NEGATIVE).__setitem__(
                                      "verdicts", "-" * ROWS)), "非乾淨死亡"),
        ("生死線位移", lambda rs: find(rs, label=NEGATIVE).__setitem__(
            "verdicts", "A" * 9 + "T" * 11), "第 9 筆起應全 TLE"),
        ("頁面掛載失敗", lambda rs: find(rs, check="mount", id="apcs015").__setitem__(
            "status", "FAILED"), "mount 失敗"),
        ("短網址失效", lambda rs: find(rs, check="alias", id="apcs017").__setitem__(
            "status", "FAILED"), "alias 失敗"),
        ("洩題", lambda rs: find(rs, check="leak")["hits"].__setitem__(
            "015_blocked_fn", True), "洩漏答案特徵"),
        ("洩題探針壞掉", lambda rs: find(rs, check="leak_control")["control"].__setitem__(
            "title_zh", False), "正向控制 title_zh 未命中"),
        ("部署是舊版", lambda rs: find(rs, check="freshness").__setitem__(
            "n_bound_1000", False), "疑為舊版"),
        ("答案表沒收斂", lambda rs: find(rs, check="freshness_table").__setitem__(
            "rows", [["1", "0"], ["2", "6"], ["3", "28"], ["4", "96"]]),
         "不是 k=1..3"),
    ]
    for name, fn, frag in injections:
        probs, _ = audit(mutate(fn))
        hit = [p for p in probs if frag in p]
        print("  %-28s %-6s %s" % (name, "FIRED" if hit else "MISS",
                                   hit[0] if hit else "（未觸發預期檢查）"))
        if not hit:
            failures.append("注入「%s」未觸發預期檢查（期望含 %r）" % (name, frag))

    if failures:
        print("\n負向控制失敗：")
        for f in failures:
            print("  -", f)
        return 1
    print("\n負向控制全數通過（%d 個注入點皆觸發，真實觀測零誤判）。" % len(injections))
    return 0


def main():
    records = load(RAW)
    problems, stats = audit(records)
    payload = {
        "problems": problems,
        "base": BASE,
        "deployed_commit": DEPLOYED_COMMIT,
        "observed_on": OBSERVED_ON,
        "raw": "measure/staging-e2e.jsonl",
        "retracted_probes": RETRACTED,
        "stats": stats,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("讀入 %d 筆觀測，違規 %d 條 → %s"
          % (len(records), len(problems), os.path.basename(OUT)))
    for p in problems:
        print("  FAIL", p)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(self_test() if "--self-test" in sys.argv else main())
