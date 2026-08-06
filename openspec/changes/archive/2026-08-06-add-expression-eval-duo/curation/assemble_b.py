"""Assemble apcs011/apcs012 challenge markdown files from curated literals.

Built-in assertions: literal byte-equality, generator == reference on all 40
literals (subprocess), YAML frontmatter parses, no banned terminology.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LIT = os.path.join(HERE, "literals")
REPO = "/Users/phoenix/dev/fhsh-projects/fhsh.py-dojo"

GEN_011 = '''t = int(input())
for _ in range(t):
    toks = input().split()
    seg, ops = [], []
    i, n = 0, len(toks)
    while i < n:
        v = int(toks[i]); i += 1
        while i < n and toks[i] in "+-":
            b = int(toks[i + 1])
            v = v + b if toks[i] == "+" else v - b
            i += 2
        seg.append(v)
        if i < n:
            ops.append(toks[i]); i += 1
    val = seg[0]
    for op, s in zip(ops, seg[1:]):
        if op == "*":
            val = val * s
        else:
            assert s > 0 and val % s == 0
            val = val // s
    print(val)
'''

REF_011 = '''import sys

def to_rpn(toks):
    # 加減優先序 2、乘除 1，全部左結合
    prec = {"+": 2, "-": 2, "*": 1, "/": 1}
    out, st = [], []
    for tk in toks:
        if tk in prec:
            while st and prec[st[-1]] >= prec[tk]:
                out.append(st.pop())
            st.append(tk)
        else:
            out.append(int(tk))
    while st:
        out.append(st.pop())
    return out

def run_rpn(rpn):
    st = []
    for tk in rpn:
        if isinstance(tk, int):
            st.append(tk)
        else:
            b = st.pop(); a = st.pop()
            if tk == "+": st.append(a + b)
            elif tk == "-": st.append(a - b)
            elif tk == "*": st.append(a * b)
            else:
                assert b > 0 and a % b == 0
                st.append(a // b)
    return st[0]

data = sys.stdin.read().split("\\n")
t = int(data[0])
print("\\n".join(str(run_rpn(to_rpn(data[i].split()))) for i in range(1, t + 1)))
'''

GEN_012 = '''import sys
data = sys.stdin.read().split("\\n")
t = int(data[0])

def solve(toks):
    pos = 0
    def expr():
        nonlocal pos
        v = term()
        while pos < len(toks) and toks[pos] in "*/":
            op = toks[pos]; pos += 1
            s = term()
            if op == "*":
                v = v * s
            else:
                assert s > 0 and v % s == 0
                v = v // s
        return v
    def term():
        nonlocal pos
        atoms = [atom()]
        aops = []
        while pos < len(toks) and toks[pos] in "+-":
            aops.append(toks[pos]); pos += 1
            atoms.append(atom())
        acc = atoms[-1]
        for k in range(len(aops) - 1, -1, -1):
            acc = atoms[k] + acc if aops[k] == "+" else atoms[k] - acc
        return acc
    def atom():
        nonlocal pos
        if toks[pos] == "(":
            pos += 1
            v = expr()
            pos += 1
            return v
        v = int(toks[pos]); pos += 1
        return v
    return expr()

out = []
for li in range(1, t + 1):
    out.append(str(solve(data[li].split())))
print("\\n".join(out))
'''

REF_012 = '''import sys

def to_rpn(toks):
    # 加減優先序 2（右結合）、乘除 1（左結合）、括弧覆寫
    prec = {"+": 2, "-": 2, "*": 1, "/": 1}
    right = {"+", "-"}
    out, st = [], []
    for tk in toks:
        if tk == "(":
            st.append(tk)
        elif tk == ")":
            while st[-1] != "(":
                out.append(st.pop())
            st.pop()
        elif tk in prec:
            while st and st[-1] != "(" and (
                prec[st[-1]] > prec[tk]
                or (prec[st[-1]] == prec[tk] and tk not in right)
            ):
                out.append(st.pop())
            st.append(tk)
        else:
            out.append(int(tk))
    while st:
        out.append(st.pop())
    return out

def run_rpn(rpn):
    st = []
    for tk in rpn:
        if isinstance(tk, int):
            st.append(tk)
        else:
            b = st.pop(); a = st.pop()
            if tk == "+": st.append(a + b)
            elif tk == "-": st.append(a - b)
            elif tk == "*": st.append(a * b)
            else:
                assert b > 0 and a % b == 0
                st.append(a // b)
    return st[0]

data = sys.stdin.read().split("\\n")
t = int(data[0])
print("\\n".join(str(run_rpn(to_rpn(data[i].split()))) for i in range(1, t + 1)))
'''

STARTER = '''t = int(input())
for _ in range(t):
    toks = input().split()
    # 在此依照題目規則計算這一行算式的結果
    print(0)
'''


def literal_blocks(prefix):
    blocks = []
    for i in range(1, 21):
        text = open(os.path.join(LIT, f"{prefix}_{i:02d}.txt")).read()
        assert text.endswith("\n") and "\t" not in text
        indented = "".join("      " + ln + "\n" for ln in text.split("\n")[:-1])
        blocks.append("  - literal: |\n" + indented)
    return "".join(blocks)


def frontmatter(cid, title, diff, algo, desc, tags, gen, ref, prefix):
    def block(field, body, ind="  "):
        lines = "".join(ind + ln + "\n" for ln in body.rstrip("\n").split("\n"))
        return f"{field}: |\n{lines}"
    return (
        "---\n"
        "layout: challenge\n"
        f"id: {cid}\n"
        f"title: {title}\n"
        f"difficulty: {diff}\n"
        "category: apcs\n"
        "type: competition\n"
        f"tags:\n" + "".join(f"  - {t}\n" for t in tags) +
        f"algorithm: {algo}\n"
        f"description: {desc}\n"
        "input_budget: 63488\n"
        "params:\n"
        "  t:\n"
        "    type: int\n"
        "    min: 1\n"
        "    max: 1\n"
        "testcase_plan:\n" + literal_blocks(prefix) +
        block("generator", gen) +
        block("reference_solution", ref) +
        block("starter_code", STARTER) +
        "---\n"
    )


BODY_011 = '''
## 福利社老收銀機

福利社倉庫翻出一台老收銀機，店長發現它的韌體有個怪癖：結帳時**先算加號和減號，才算乘號和除號**。為了核對帳目，請你寫一支程式，輸入收據上的算式，預測這台收銀機會顯示的金額。

### 收銀機的計算規則

1. 整條算式先處理**加減**：把被乘號、除號隔開的每一段「加減段」由左至右算出結果。
2. 各段結果再依出現順序**由左至右**做乘除。
3. 除法保證整除：測資中每次除法發生時，被除數必為除數的整數倍，且除數為正整數。
4. 輸入的數字都是非負整數，但**計算過程與答案可能出現負數**。

逐步拆解 `10 - 4 - 3 + 2 * 6`：

| 步驟 | 動作 | 結果 |
|------|------|------|
| 1 | 加減段由左至右：10 - 4 - 3 + 2 | 5 |
| 2 | 段落結果相乘：5 * 6 | 30 |

再看 `2 * 3 + 4`：加減段是 `2` 與 `3 + 4 = 7`，所以答案是 2 * 7 = 14（一般計算機會給 10，這台不會）。

`1 - 7 / 2`：加減段 1 - 7 = -6，再除以 2，答案是 -3。

### 輸入說明

- 第一行：整數 `T`（`T >= 1`），代表算式行數
- 接下來 `T` 行，每行一條算式：非負整數與 `+ - * /` 交錯排列，**每個數字與符號之間以單一空白隔開**
- 數字範圍 0 ~ 9999；單獨一個數字也是合法算式（答案就是它本身）
- 全程沒有括號、沒有負數輸入；所有中間值的絕對值小於 100000

### 輸出說明

- 對每行算式輸出一行整數（可能為負）

### 範例

**輸入：**

```
5
3 + 5 * 2
10 - 4 - 3 + 2 * 6
2 * 3 + 4
1 - 7 / 2
7
```

**輸出：**

```
16
30
14
-3
7
```
'''

BODY_012 = '''
## 折價券疊加試算

網路商店推出可疊加的折價金額券，但疊加規則很特別：**每張券不是直接作用在原價上，而是作用在「它右側整段已經計算完的結果」上**。另外還有「組合包」：像獨立包裹一樣，包裹裡的金額先自己算完，再參與外面的計算。請寫程式替客服部門試算最終金額。

### 試算規則

1. 加號與減號（券的疊加）**優先於**乘號與除號。
2. 疊加方向：**每個加減符號作用於其右側整段已計算的結果**——先把最右邊的加減算完，再一路往左收。

   逐步拆解 `10 - 4 - 3 + 2 * 6`：

   | 步驟 | 動作 | 結果 |
   |------|------|------|
   | 1 | 最右先收：3 + 2 | 5 |
   | 2 | 往左：4 - 5 | -1 |
   | 3 | 再往左：10 - (-1) | 11 |
   | 4 | 乘除段：11 * 6 | 66 |

   同一條式子在《福利社老收銀機》的加減段由左至右規則下是 30——兩題的世界觀不同，請小心！
   例如 `9 - 5 - 2`：先算 5 - 2 = 3，再算 9 - 3，答案是 6（不是 2）。
3. 乘號與除號仍**由左至右**計算：`( 9 - 5 - 2 ) * 8 / 6` 先得括弧內 6，再 6 * 8 = 48、48 / 6 = 8。
4. 括弧（組合包）優先於一切：括弧內先依同樣規則算完。`2 + ( 3 * 4 )` 的括弧內是 12，答案 14；若沒有括弧，`2 + 3 * 4` 依規則 1 是 (2+3) * 4 = 20。組合包可以多層套疊（歷史促銷資料中出現過非常深的極端案例）。
5. 除法保證整除且除數為正；輸入數字為 0 ~ 9999 的非負整數；所有中間值絕對值小於 100000；單獨數字行合法；答案可能為負。

### 輸入說明

- 第一行：整數 `T`（`T >= 1`）
- 接下來 `T` 行，每行一條算式：數字、`+ - * /` 與括弧之間**以單一空白隔開**
- 前 8 筆測資不含括弧；第 9 筆起會出現括弧

### 輸出說明

- 對每行算式輸出一行整數（可能為負）

### 範例

**輸入：**

```
3
10 - 4 - 3 + 2 * 6
9 - 5 - 2
3 + 5 * 2
```

**輸出：**

```
66
6
16
```
'''


def check_solutions(prefix, code):
    for i in range(1, 21):
        path = os.path.join(LIT, f"{prefix}_{i:02d}.txt")
        p = subprocess.run([sys.executable, "-c", code], input=open(path).read(),
                           capture_output=True, text=True, timeout=60)
        assert p.returncode == 0, (prefix, i, p.stderr[-300:])
        yield i, p.stdout.strip()


def main():
    # generator vs reference agreement on all 40 literals
    for prefix, gen, ref in (("a", GEN_011, REF_011), ("b", GEN_012, REF_012)):
        g = dict(check_solutions(prefix, gen))
        r = dict(check_solutions(prefix, ref))
        assert g == r, f"{prefix}: generator/reference disagree"
    print("generator == reference on all 40 literals OK")

    fm_a = frontmatter("apcs011", "福利社老收銀機", "medium", "snack_bar_register",
                       "預測先加減後乘除的老收銀機顯示金額", ["字串", "數學"],
                       GEN_011, REF_011, "a")
    fm_b = frontmatter("apcs012", "折價券疊加試算", "hard", "coupon_combo_quote",
                       "折價券由右往左疊加、組合包優先的金額試算", ["字串", "數學"],
                       GEN_012, REF_012, "b")

    out_a = fm_a + BODY_011
    out_b = fm_b + BODY_012

    # frontmatter must parse as YAML and preserve literal bytes
    import yaml
    for out, prefix, cid in ((out_a, "a", "apcs011"), (out_b, "b", "apcs012")):
        fm = out.split("---\n")[1]
        doc = yaml.safe_load(fm)
        assert doc["id"] == cid and doc["input_budget"] == 63488
        plan = doc["testcase_plan"]
        assert len(plan) == 20
        for i, entry in enumerate(plan, 1):
            want = open(os.path.join(LIT, f"{prefix}_{i:02d}.txt")).read()
            assert entry["literal"] == want, f"{cid} entry {i} literal mismatch"
        for banned in ("stack", "堆疊", "樹", "LIFO", "lifo", "資料結構"):
            assert banned not in out, f"{cid} contains banned term {banned}"
    print("YAML parse + literal byte-equality + banned-term check OK")

    open(os.path.join(REPO, "docs/challenge/snack-bar-register.md"), "w").write(out_a)
    open(os.path.join(REPO, "docs/challenge/coupon-combo-quote.md"), "w").write(out_b)
    print("written:", "snack-bar-register.md", len(out_a), "bytes;",
          "coupon-combo-quote.md", len(out_b), "bytes")


if __name__ == "__main__":
    main()
