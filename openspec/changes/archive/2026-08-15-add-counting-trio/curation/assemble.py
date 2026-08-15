"""三題 frontmatter 片段組裝器（F-8／F-9 的修法）。

執行：
    python3 curation/assemble.py            驗證＋寫出 out/frontmatter0XX.yaml
    python3 curation/assemble.py --check     只驗證，不寫檔

為什麼需要這支程式
------------------
三面斷言牆各自產出的 out/plan0XX.yaml 形狀不一致：015／017 缺 params
（專案契約列為**必填**）、缺 algorithm、缺 input_budget；016 多出 frontmatter
根本沒有的 expected_outputs 欄位、還逐筆列出全部 20 個答案；017 每一筆 literal
的行內註解寫著「期望 N 類別 A/B」，同時洩漏答案與誤解路線的鑑別點。那三個檔的
內容是要貼進**公開題面**的，答案不能跟著走。

本檔的職責邊界
--------------
* 斷言牆（curation/plan0XX.py）仍然是 literal 的唯一產生者，本檔**不產生也不修改**
  任何 literal，只搬運：每一筆 literal 一個位元組都不會變（由 B 段逐筆比對＋
  sha256 證明）。
* frontmatter 的其餘鍵（algorithm／params／input_budget）由本檔集中宣告，三題
  同一形狀、同一個真相來源；值域一律從 semantics／plan 模組讀，不手抄。
* 產出**不含任何註解**：註解會跟著貼進題面，而洩漏就是從註解開始的。片段的
  出處與檢查結果落在 measure/assemble_report.json。

四道防線（任何一道不過就 exit non-zero 且不寫檔）
------------------------------------------------
A. 來源掃描：out/plan0XX.yaml 只允許 testcase_plan 這一個頂層鍵；遞迴掃描鍵名，
   命中 expected／answer／output／solution 之類就失敗；testcase_plan 區塊內
   一律不得有 `#` 註解（017 的洩漏正是躲在行內註解裡，而 YAML 解析會默默吃掉）。
B. 搬運忠實度：literal 逐筆與斷言牆的 ENTRIES 重新渲染的結果比對（防止 yaml 過期），
   再與產出檔重新解析出來的 literal 逐筆比對，最後比 sha256。
C. 契約一致性：每筆 literal 按宣告的 params 形狀解析（區塊數 = 參數數、每個區塊的
   值個數落在 count 範圍、每個值是整數且落在 min..max），並檢查位元組數 <= input_budget。
   params 因此不是貼上去好看的，而是與 20 筆 literal 機械對得上的宣告。
D. 禁用術語掃描：對**產出的每個檔案**掃描資料結構與演算法術語（中英文）。三題的
   題面都刻意把數學藏在生活情境裡，片段裡跑出「階乘」「組合」「快速冪」這類字眼
   就等於在 frontmatter 洩題。掃描器自己有 self-test（見 scanner_self_test），
   確保它真的會叫——不會叫的檢查等於沒有檢查。
"""
import hashlib
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CHANGE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
MEASURE = os.path.join(CHANGE, "measure")

sys.path.insert(0, HERE)
import semantics015 as S15  # noqa: E402
import semantics016 as S16  # noqa: E402
import semantics017 as S17  # noqa: E402
import plan015 as P15  # noqa: E402
import plan016 as P16  # noqa: E402
import plan017 as P17  # noqa: E402

# ── A. 來源允許／禁止的鍵 ───────────────────────────────────────────────
SOURCE_ALLOWED_TOP_KEYS = {"testcase_plan"}
# 期望答案不得出現在任何要貼進題面的檔案裡。鍵名以正則比對（不分大小寫）。
ANSWER_KEY_PATTERNS = [
    r"expected", r"answer", r"solution", r"^exp$", r"outputs?$",
    r"期望", r"答案", r"解答",
]

# ── C. 引擎的 params 允許欄位（出處：testcase-generator/src/parser.rs:225 的
#      check_fields(name, obj, &["type", "min", "max", "count"])，以及 :383 的
#      count 允許欄位 ["min", "max", "separator", "from"]）───────────────
PARAM_ALLOWED_FIELDS = {"type", "min", "max", "count"}
COUNT_ALLOWED_FIELDS = {"min", "max", "separator", "from"}

# input_budget 的引擎預設值（Usage.md「輸入規模預算」）。三面斷言牆各自也用
# 這個數字做逐筆檢查，這裡直接讀它們的常數，不另外手抄一份。
ENGINE_DEFAULT_INPUT_BUDGET = 4096

# ── D. 禁用術語 ────────────────────────────────────────────────────────
# 說明：
#   * 英文以「前後不是英數字」為邊界（不是 \b，見 scan_banned 的說明），並自動
#     吃複數形；"int"／"count"／"min" 這類合法欄位名不在清單裡，不會被誤傷。
#   * 英文的 "algorithm" **不列入**：它是 frontmatter 的合法鍵名。中文的
#     「演算法」則列入——片段裡不該有中文散文。
#   * "modulo／餘數／取餘數" **不列入**：apcs016 的題面本來就明說要對
#     1000000007 取餘數，那是題目給的規則，不是被藏起來的解法。
BANNED_EN = [
    "prefix sum", "prefix_sum", "suffix sum", "cumulative sum", "difference array",
    "combination", "combinatoric", "binomial", "factorial", "permutation",
    "modpow", "pow_mod", "fast power", "exponentiation", "legendre", "valuation",
    "sieve", "prime factor", "factorization", "gcd", "lcm",
    "dynamic programming", "memoization", "memoized", "greedy", "backtracking",
    "recursion", "recursive", "binary search", "ternary search", "two pointer",
    "sliding window", "hashmap", "hashtable", "hashing",
    "linked list", "stack", "queue", "deque", "heapify", "priority queue",
    "binary tree", "segment tree", "fenwick", "trie", "graph traversal",
    "bfs", "dfs", "quicksort", "mergesort", "sorting", "sort", "bitmask", "bitwise",
    "brute force", "closed form", "time complexity", "complexity", "knapsack",
    "data structure", "big-o", "hash", "heap", "tree", "graph", "dp",
]
BANNED_ZH = [
    "前綴和", "累積和", "差分", "組合數", "組合", "排列", "階乘", "快速冪", "模冪",
    "冪次", "篩法", "質數", "因數分解", "最大公因數", "最小公倍數",
    "動態規劃", "記憶化", "貪心", "回溯", "遞迴", "遞歸", "二分搜", "雙指標",
    "滑動視窗", "雜湊", "字典", "堆疊", "佇列", "堆積", "優先佇列",
    "鏈結串列", "二元樹", "線段樹", "樹狀陣列", "圖論", "廣度優先", "深度優先",
    "排序", "位元運算", "暴力", "枚舉", "列舉", "封閉式", "時間複雜度", "複雜度",
    "演算法", "資料結構", "類別 A", "類別 B",
]


def scan_banned(text):
    """回傳命中的術語清單（空 = 乾淨）。

    英文邊界**不用 \\b**：\\b 把底線當成字的一部分，而 algorithm 的值正是
    snake_case（factorial_count 這種寫法會整個逃掉，那是最可能的洩漏面）。
    改用「前後不是英數字」的邊界，並讓術語內的空白同時吃空白／底線／連字號。
    """
    low = text.lower()
    hits = []
    for term in BANNED_EN:
        body = re.escape(term).replace(r"\ ", r"[\s_-]+")
        pat = r"(?<![a-z0-9])%s(e?s)?(?![a-z0-9])" % body   # 複數形也要抓（permutations）
        if re.search(pat, low):
            hits.append(term)
    for term in BANNED_ZH:
        if term in text:
            hits.append(term)
    return hits


SCANNER_PROBES = [
    ("這題要用階乘", "階乘"),
    ("uses a segment tree here", "segment tree"),
    ("prefix-sum trick", "prefix sum"),
    ("algorithm: factorial_count", "factorial"),        # snake_case 不得逃掉
    ("algorithm: count_permutations", "permutation"),   # 複數形不得逃掉
    ("期望 3 類別 A", "類別 A"),
]


def scanner_self_test():
    """掃描器必須真的會叫：對照組乾淨、實驗組命中，否則整支程式沒有意義。"""
    clean = "algorithm: ap_layout_plan\nparams:\n  n:\n    type: int\n    min: 1\n"
    if scan_banned(clean):
        raise SystemExit("掃描器 self-test 失敗：乾淨樣本被誤判命中 %s" % scan_banned(clean))
    for probe, want in SCANNER_PROBES:
        if want not in scan_banned(probe):
            raise SystemExit("掃描器 self-test 失敗：%r 應命中 %r，實得 %s"
                             % (probe, want, scan_banned(probe)))


# ── 三題的 frontmatter 表面（本檔是它的唯一真相來源） ────────────────────
# params 的值域一律從語意／斷言牆模組讀，不手抄；literal 會逐筆回頭驗證。
#
# apcs016 的輸入是「同一行兩個整數 n k」。frontmatter 的每個 params 鍵各自渲染
# 成一個區塊（預設一行），所以宣告成兩個 int 參數會變成兩行、格式就錯了；同一
# 參數 count = 2、separator = " " 才會渲染成單行。代價是 n 與 k 只能共用一組
# min/max，故取兩者值域的聯集下界 0（k 可以是 0）與共同上界 1000000。
CHALLENGES = [
    {
        "tag": "015",
        "slug": "ap-layout-plan",
        "algorithm": "ap_layout_plan",
        "source": "plan015.yaml",
        "input_budget": P15.INPUT_BUDGET,
        "params": [
            ("n", {"type": "int", "min": S15.N_MIN, "max": S15.N_MAX}),
        ],
        "render": lambda: [S15.render_input(n) for n in P15.ENTRIES],
    },
    {
        "tag": "016",
        "slug": "marquee-display-count",
        "algorithm": "marquee_display_count",
        "source": "plan016.yaml",
        "input_budget": P16.BUDGET,
        "params": [
            ("nk", {"type": "int", "min": 0, "max": P16.MAX_N,
                    "count": {"min": 2, "max": 2, "separator": " "}}),
        ],
        "render": lambda: [S16.render_input(n, k) for n, k in P16.ENTRIES],
    },
    {
        "tag": "017",
        "slug": "fair-token-exchange",
        "algorithm": "fair_token_exchange",
        "source": "plan017.yaml",
        "input_budget": P17.INPUT_BUDGET,
        "params": [
            ("n", {"type": "int", "min": 1, "max": S17.MAX_N}),
        ],
        "render": lambda: [S17.render_input(n) for n in P17.ENTRIES],
    },
]


def scan_answer_keys(node, trail=()):
    """遞迴掃描鍵名，回傳 [(鍵路徑, 命中的規則)]；來源與產出兩邊都用同一支。"""
    hits = []
    if isinstance(node, dict):
        for k, v in node.items():
            for pat in ANSWER_KEY_PATTERNS:
                if re.search(pat, str(k), re.IGNORECASE):
                    hits.append(("/".join(list(trail) + [str(k)]), pat))
            hits += scan_answer_keys(v, tuple(trail) + (str(k),))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hits += scan_answer_keys(v, tuple(trail) + ("[%d]" % i,))
    return hits


# ── A. 讀來源並掃描 ────────────────────────────────────────────────────
def read_source(path, problems):
    raw = open(path).read()
    doc = yaml.safe_load(raw)

    extra = sorted(set(doc) - SOURCE_ALLOWED_TOP_KEYS)
    if extra:
        problems.append("%s：出現不該落在測資計畫裡的頂層鍵 %s（frontmatter 的其餘鍵"
                        "由 assemble.py 統一組裝）" % (os.path.basename(path), extra))

    for hit, pat in scan_answer_keys(doc):
        problems.append("%s：鍵 %s 疑似期望答案（比對規則 %s）"
                        % (os.path.basename(path), hit, pat))

    # testcase_plan 區塊內不得有任何 `#` 註解：017 的洩漏就躲在行內註解裡，
    # 而 yaml.safe_load 會默默把它吃掉，只靠解析後的資料是抓不到的。
    lines = raw.splitlines()
    started = False
    for i, line in enumerate(lines, 1):
        if re.match(r"^testcase_plan\s*:", line):
            started = True
            continue
        if started and "#" in line:
            problems.append("%s:%d：testcase_plan 區塊內出現註解 %r——註解會跟著貼進題面"
                            % (os.path.basename(path), i, line.strip()))

    if not isinstance(doc.get("testcase_plan"), list):
        problems.append("%s：缺 testcase_plan 清單" % os.path.basename(path))
        return []
    lits = []
    for i, e in enumerate(doc["testcase_plan"], 1):
        if set(e) != {"literal"}:
            problems.append("%s entry %d：條目鍵為 %s，全 literal 計畫只允許 literal"
                            % (os.path.basename(path), i, sorted(e)))
        lits.append(e.get("literal", ""))
    return lits


# ── C. params 宣告 vs literal 實際內容 ─────────────────────────────────
def check_params_against_literals(spec, literals, problems):
    tag = spec["tag"]
    for name, p in spec["params"]:
        extra = sorted(set(p) - PARAM_ALLOWED_FIELDS)
        if extra:
            problems.append("%s params.%s：引擎不認識的欄位 %s" % (tag, name, extra))
        if p["type"] != "int":
            problems.append("%s params.%s：本組裝器只支援 int 型別" % (tag, name))
        if p["min"] > p["max"]:
            problems.append("%s params.%s：min > max" % (tag, name))
        c = p.get("count")
        if c is not None:
            extra = sorted(set(c) - COUNT_ALLOWED_FIELDS)
            if extra:
                problems.append("%s params.%s.count：引擎不認識的欄位 %s" % (tag, name, extra))

    for idx, lit in enumerate(literals, 1):
        blocks = lit.rstrip("\n").split("\n")
        if len(blocks) != len(spec["params"]):
            problems.append("%s entry %d：literal 有 %d 個區塊，params 宣告 %d 個參數"
                            % (tag, idx, len(blocks), len(spec["params"])))
            continue
        for block, (name, p) in zip(blocks, spec["params"]):
            c = p.get("count") or {"min": 1, "max": 1, "separator": " "}
            toks = block.split(c.get("separator", " "))
            if not (c["min"] <= len(toks) <= c["max"]):
                problems.append("%s entry %d params.%s：該行有 %d 個值，count 宣告 %d..%d"
                                % (tag, idx, name, len(toks), c["min"], c["max"]))
            for t in toks:
                if not re.fullmatch(r"-?\d+", t):
                    problems.append("%s entry %d params.%s：%r 不是整數" % (tag, idx, name, t))
                    continue
                v = int(t)
                if not (p["min"] <= v <= p["max"]):
                    problems.append("%s entry %d params.%s：值 %d 超出宣告值域 %d..%d"
                                    % (tag, idx, name, v, p["min"], p["max"]))
        nbytes = len(lit.encode())
        if nbytes > spec["input_budget"]:
            problems.append("%s entry %d：%d bytes > input_budget %d"
                            % (tag, idx, nbytes, spec["input_budget"]))


# ── 產出 ───────────────────────────────────────────────────────────────
def render_params(params):
    out = ["params:"]
    for name, p in params:
        out.append("  %s:" % name)
        out.append("    type: %s" % p["type"])
        out.append("    min: %d" % p["min"])
        out.append("    max: %d" % p["max"])
        c = p.get("count")
        if c:
            out.append("    count:")
            out.append("      min: %d" % c["min"])
            out.append("      max: %d" % c["max"])
            out.append('      separator: "%s"' % c["separator"])
    return out


def render_fragment(spec, literals):
    """三題同一形狀：algorithm -> params -> input_budget -> testcase_plan，零註解。"""
    lines = ["algorithm: %s" % spec["algorithm"]]
    lines += render_params(spec["params"])
    lines.append("input_budget: %d" % spec["input_budget"])
    lines.append("testcase_plan:")
    for lit in literals:
        lines.append("  - literal: |")
        for row in lit.rstrip("\n").split("\n"):
            lines.append("      %s" % row)
    return "\n".join(lines) + "\n"


def sha(literals):
    return hashlib.sha256("".join(literals).encode()).hexdigest()


def main(write=True):
    scanner_self_test()
    problems = []
    report = {
        "generated_by": "curation/assemble.py",
        "scanner_self_test": "通過（乾淨樣本不叫、%d 個帶術語樣本都叫）" % len(SCANNER_PROBES),
        "banned_terms_count": {"en": len(BANNED_EN), "zh": len(BANNED_ZH)},
        "engine_param_field_allowlist_source":
            "testcase-generator/src/parser.rs:225（int）與 :383（count）",
        "engine_default_input_budget": ENGINE_DEFAULT_INPUT_BUDGET,
        "challenges": [],
    }
    pending = []

    for spec in CHALLENGES:
        tag = spec["tag"]
        src = os.path.join(OUT, spec["source"])
        lits = read_source(src, problems)

        # B. 搬運忠實度①：yaml 是不是斷言牆現在這一輪的產物（防過期）
        wall = spec["render"]()
        if lits != wall:
            problems.append("%s：out/%s 的 literal 與斷言牆 ENTRIES 重新渲染的結果不符"
                            "（yaml 過期？請先重跑 plan%s.py）" % (tag, spec["source"], tag))

        check_params_against_literals(spec, lits, problems)
        if spec["input_budget"] != ENGINE_DEFAULT_INPUT_BUDGET:
            problems.append("%s：input_budget %d 與引擎預設 %d 不同，請確認是刻意的"
                            % (tag, spec["input_budget"], ENGINE_DEFAULT_INPUT_BUDGET))

        text = render_fragment(spec, lits)

        # D. 禁用術語掃描（產出檔本身）——命中就不寫檔
        hits = scan_banned(text)
        if hits:
            problems.append("%s：frontmatter 片段命中禁用術語 %s" % (tag, sorted(set(hits))))

        # B. 搬運忠實度②：把自己寫的東西重新解析回來逐筆比對
        back_doc = yaml.safe_load(text)
        back = [e["literal"] for e in back_doc["testcase_plan"]]
        if back != lits:
            problems.append("%s：產出的 literal 與來源不是逐位元相同" % tag)
        if "#" in text:
            problems.append("%s：產出含註解" % tag)
        want_keys = ["algorithm", "input_budget", "params", "testcase_plan"]
        if sorted(back_doc) != want_keys:
            problems.append("%s：片段的頂層鍵為 %s，契約要求恰好 %s"
                            % (tag, sorted(back_doc), want_keys))
        for hit, pat in scan_answer_keys(back_doc):
            problems.append("%s：片段的鍵 %s 疑似期望答案（規則 %s）" % (tag, hit, pat))
        for i, e in enumerate(back_doc["testcase_plan"], 1):
            if set(e) != {"literal"}:
                problems.append("%s 片段 entry %d：條目鍵為 %s，只允許 literal"
                                % (tag, i, sorted(e)))

        report["challenges"].append({
            "tag": tag,
            "slug": spec["slug"],
            "algorithm": spec["algorithm"],
            "source": "curation/out/" + spec["source"],
            "fragment": "curation/out/frontmatter%s.yaml" % tag,
            "keys": ["algorithm", "params", "input_budget", "testcase_plan"],
            "params": {n: p for n, p in spec["params"]},
            "input_budget": spec["input_budget"],
            "entry_count": len(lits),
            "max_entry_bytes": max(len(l.encode()) for l in lits) if lits else 0,
            "first_entry": lits[0] if lits else None,
            "literals_sha256": sha(lits),
            "literals_sha256_from_fragment": sha(back),
            "byte_identical_to_source": back == lits,
            "matches_assertion_wall_entries": lits == wall,
            "banned_term_hits": sorted(set(hits)),
        })
        pending.append((tag, text))

    # 任何一題有問題就三題都不寫：片段是一組的，只寫出乾淨的那幾份會讓下一位
    # 維護者拿到半新半舊的組合。
    report["problems"] = problems
    if write and not problems:
        for tag, text in pending:
            with open(os.path.join(OUT, "frontmatter%s.yaml" % tag), "w") as fh:
                fh.write(text)
        os.makedirs(MEASURE, exist_ok=True)
        with open(os.path.join(MEASURE, "assemble_report.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    for c in report["challenges"]:
        print("%s %-24s literal=%2d  最大 %2d bytes  sha=%s  逐位元相同=%s  對得上斷言牆=%s"
              % (c["tag"], c["algorithm"], c["entry_count"], c["max_entry_bytes"],
                 c["literals_sha256"][:16], c["byte_identical_to_source"],
                 c["matches_assertion_wall_entries"]))
    if problems:
        print("\n組裝失敗（未寫出任何片段）：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n四道防線全數通過（%s）。" % ("已寫出 3 份片段＋measure/assemble_report.json"
                                        if write else "--check：未寫檔"))
    return 0


if __name__ == "__main__":
    sys.exit(main(write="--check" not in sys.argv))
