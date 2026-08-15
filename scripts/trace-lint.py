#!/usr/bin/env python3
"""追溯矩陣機械檢查器（跨 change 重用）。

用法::

    python3 scripts/trace-lint.py openspec/changes/<name>
    python3 scripts/trace-lint.py openspec/changes/<name> --json
    python3 scripts/trace-lint.py --self-test

本檔把 ``<change>/trace-matrix.md`` 當成**可機械解析的單一真相來源**，做四段檢查。
任何一段 FAIL 即 exit 1。

矩陣格式契約
============

矩陣中每一張表的表頭必須含這幾欄（順序不拘、可有多餘欄）::

    | id | 主張 | 證據 | 題目頁 | spec | design |

**證據欄**可含零個或多個「可解析位址」，寫成 markdown code span：``路徑#鍵路徑``。

- 路徑相對於 change 根目錄，例如 ``measure/routes015.json#spelling_worst_op_margin``
- 鍵路徑用點號走 dict、方括號走 list：``measure/routes015.json#routes[0].max_ops``
- 鍵本身含點號時用引號方括號：``measure/routes015.json#spelling_ops_at_max_entry["r015_rowscan.py"]``
- ``.jsonl`` 檔用 label 定位：``measure/browser-verification.jsonl#label=cellscan.score``
  （``label=`` 後面到**第一個點號或方括號**為止是 label 值，其餘是該筆紀錄內的鍵路徑；
  同一個 label 出現兩次即報錯，因為無法唯一定位）
- 只支援 ``.json`` 與 ``.jsonl``；指向其他副檔名的位址一律報錯，不靜靜跳過
- 不含 ``#`` 的 code span 視為純敘述（原始碼路徑、識別字），不檢查
- 純敘述性出處（訪談記錄、原始碼行號）維持散文即可，不寫成 code span

**spec 欄與 design 欄**只能是三種值之一：

- ``✓``  該事實**必須**在該文件中以標記引用（spec 用 ``(trace X)``、design 用 ``(fact X)``）
- ``—``  該事實**不得**出現在該文件
- ``△``  刻意不檢查，後面必須接一句括號理由

標記慣例：spec 用 ``(trace X)``、design 用 ``(fact X)``。一個標記可帶多個 id
（``(trace D7/E7)``、``(facts E10, G7)``），複數形與 ``/``、``、``、``,`` 分隔皆接受；
標記內不符 fact id 形狀又不在矩陣裡的 token（``(fact B1, proven)`` 的 ``proven``）
視為自由註記。

**題目頁欄**維持散文，**本檢查器不碰它**——題目頁不能帶 fact 標記，那會洩題。
該方向由 ``<change>/verify/check_frontmatter_pair.py`` 的 E 檢查反向覆蓋
（頁面每個數字都要對回 fact id）。

四段檢查
========

(a) 位址可解析（``addr-*``）
    證據欄每個位址的檔案必須存在、鍵路徑必須解析得出值。失敗時指名列、位址、
    以及卡在鍵路徑的哪一段。

(b) 數字綁鍵（``number-*``、``claim-fuzzy-quantity``）
    若某列證據欄**有位址**，該列**主張欄**出現的每個數字都必須等於該列某個位址
    解析出的值。證據欄全散文的列不做此檢查（那是刻意留的逃生口：不宣稱有機械
    出處，就不受機械檢查）。同段另含「模糊量詞／中文數字量詞」檢查，見下。

(c) 位置欄雙向（``pos-*``）
    正向：``✓`` 的目標文件必須含標記；``—`` 的不得含；``△`` 必須帶括號理由。
    反向：目標文件出現的每個標記，矩陣必須有對應 fact id 且該欄為 ``✓``。

    .. warning::

       **(c) 只保證標記存在與否，完全不保證標記所在的那段文字說得對。**
       ``(trace E4)`` 這個標記出現在 spec.md 就算 ✓ 通過，即使它旁邊那句話
       把 op 數寫成任何值。「標記旁邊的內容對不對」由 (d) 段以數字為單位
       部分覆蓋；非數字的語意誤述（把「最高級數」寫成「兌換次數」）本工具
       **抓不到**，那是正則工具的本質限制，不要誤以為 (c) 提供了語意保證。

(d) 文件數字綁鍵（``doc-number-*``）
    (b) 只比對矩陣內部（主張欄 ↔ 同列位址），**完全不讀** spec.md／design.md 的
    散文。本 change 曾因此讓五個過期牆鐘數字帶著正確的 ``(trace X)`` 標記出貨。
    (d) 補上這個洞：**帶標記的每一句散文，句中的每個數字都必須等於該句所標
    fact 的某個位址解析值**（沿用 (b) 的正規化與比對規則）。

    **句子邊界的取捨（設計決定）**：本檢查以「標記所在的**句子**」為作用域，
    切法如下——

    1. 先切**區塊**：空行分段；``|`` 開頭的表格列**逐格切開，一格一個區塊**；
       ``-``／``*``／``+``／``>``／``#``／``1.`` 開頭的行各自成一個區塊；其餘連續
       非空行併成一段。
    2. 再切**句子**：在 ``.``／``!``／``?``／``。``／``！``／``？`` 之後、且後面接
       空白或區塊結尾處切開。小數點後面接數字不接空白，故 ``3.98`` 不會被切開。

    為什麼選「句子」而不是「整段」或「整個 bullet」：本 repo 的標記慣例是
    **標記放在它所擔保的那句話尾端**，一段裡通常有多句、各標各的 fact；以整段
    為作用域會把 A 句的數字算到 B 句的 fact 頭上（union 之後幾乎驗不到東西），
    以整個 bullet 為作用域在 Scenario 條列處等同整句、在 Decisions 表格處則會把
    整列混成一格。**已知誤判風險**（各有負向控制或例外表兜住）：

    - 表格列逐格切開，等於**放棄檢查同列其他格的數字**（例如 design.md 決策表
      「Q7 (fact D7)」那格有標記、數字卻在隔壁格）。這是刻意的：整列混成一格
      會製造大量假陽性，寧可少驗不要誤殺。
    - 段落若以硬換行拆成多行，會被併成一段再切句，切點仍正確；但**句子跨區塊**
      （例如一句話被表格列切斷）會失準。
    - ``e.g.``／``Fig. 3`` 這類縮寫的句點後接空白，會被誤判為句子結尾，使該句被
      切短。後果是**少驗**不是誤殺。

    **逃生口是明的**：真的無法綁鍵的數字（I/O 契約的邊界值、序數、公式分支常數）
    必須逐筆登記在 ``trace-matrix.md`` 的〈(d) 文件數字例外表〉，四欄
    ``文件 | fact | 數字 | 理由`` 缺一不可，理由不得留白。登記了卻沒被用到的例外
    會以 ``doc-number-exempt-stale`` 報錯，例外表因此不會爛在那裡。

數字正規化規則（(b) 與 (d) 共用）
=================================

**掃描前先從主張欄剔除**：

1. 所有 code span（`` `...` ``）——那是識別字與公式（``apcs015``、``k²(k²−1)/2``、
   ``2^(n−k) mod 1000000007``），不是被主張的量測值。
2. ISO 日期 ``YYYY-MM-DD``——那是時間戳不是量測值。

**數字 token 的認定**：

- 前面不得緊接 ``[A-Za-z0-9_.,]``，後面不得（跨過數字與逗號後）緊接 ``[A-Za-z_]``。
  這使 ``E8`` 的 ``8``、``apcs015`` 的 ``015`` 不被當成數字。
- **緊貼數字的已知單位後綴先被隔開再掃描**（``UNIT_SUFFIXES``）。上一條的負向
  lookahead 原本會讓 ``999ms``、``3010ops``、``300MiB`` 整個**掃不到**，該列即使
  有位址也不做檢查、且不留任何痕跡；正規化補上這個洞。單位清單是白名單，
  ``2x3``（後面接數字）不算單位、仍不掃描。
- 千分位逗號視為格式：``1,008,010`` → ``1008010``。
- 單位與後綴（``%``、``倍``、``×``、``ms``、``bytes``、``op``）一律**不參與換算**，
  只比對裸數值。故 json 存 ``16.43`` 時，散文寫 ``16.43%`` 算相符；
  散文寫 ``0.1643`` 不算。
- 上標數字（``10⁹``、``2²⁹``）非 ASCII，**不掃描**（無法可靠正規化，刻意放行）。

**模糊量詞與中文數字量詞（``claim-fuzzy-quantity``，只查有位址的列）**：

上一條只認 ASCII 數字，於是 ``四倍``、``不到四倍``、``大約三倍`` 這種寫法**完全
不受檢查**——宣稱了一個量、卻沒有任何東西驗它。有位址的列若主張欄命中下列兩型
之一即 FAIL：

1. 中文數字（可含 ``個``）緊接量測單位：``四倍``、``一個數量級``、``三成``。
2. 模糊量詞緊接中文數字：``不到四倍``、``大約三倍``、``將近一半``。

模糊量詞後面若緊接 ASCII 數字（``約 300 MiB``、``超過 3 倍``）**不算命中**——
那個數字本身已經受檢查。命中時只有兩條出路，**沒有第三條**：改寫成精確的阿拉伯
數字讓它受檢查，或把該列證據欄的位址整格拿掉、改成純散文，明白宣告放棄機械檢查。

**比對規則**：

- 位址解析出的值若是容器（dict／list），其**所有數值葉節點**都算候選值。
  故 ``#entries`` 這種列表位址可一次綁住列表內所有數字。
- 散文數字 ``c``（十進位小數 ``d`` 位）與候選值 ``v`` 相符的條件是
  ``round(v, d) == c``。因此 json 的 ``4.0`` 可被散文的 ``4`` 綁住、
  ``3.9843`` 可被 ``3.98`` 綁住，但 ``3.98`` 不能被 ``4`` 綁住之外的寫法蒙混。
- 布林值不算數值（Python 的 ``True`` 是 ``int`` 的子類，明確排除）。
- 字串葉節點只在**整格就是數值或比值**時才拆數字（``"13/20"`` → 13 與 20）。得分在
  多份 harness 裡以 ``"13/20"`` 形式儲存，那仍是「值在該位址」；含散文的字串一律
  不拆，否則備註欄的任何數字都會變成候選值。

**多位址的逐一對位（``number-misplaced``）**：

預設是**聯集**比對——主張欄每個數字 ∈ 該列所有位址值的聯集。當同列多個位址剛好
同值（例如多條錯誤路線得分都是 2），把某個位址換成另一個同值的鍵不會被發現。
因此當主張欄以 ``／`` 切出的段數**等於**該列可解析位址數、且**每一段都至少含一個
數字**時，改做**逐段對位**：第 i 段的數字必須落在第 i 個位址的值裡。段數不吻合、
或有任何一段不含數字（例如 ``四鍵（`a`／`b`／`c`／`d`）為 599 bytes`` 這種以 ``／``
分隔鍵名的寫法），一律退回聯集比對。

逐一對位能抓「位址順序寫反」，**抓不到「兩個同值位址互換」**——兩者值相同，任何
數值比對都無法區分。這是本規則已知且不可消除的殘餘。

鐵律
====

方向永遠是「跑腳本 → 用輸出覆寫散文」，不是「補資料去符合既有散文」。
本檢查器只會告訴你哪個數字沒有出處，不會告訴你該把哪個數字寫進 json。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

# --- 位置欄的三種合法值 -------------------------------------------------------

MARK_YES = {"✓", "✔"}
MARK_NO = {"—", "–", "-", "──"}
MARK_SKIP = "△"

# 位置欄 → (目標文件種類, 標記關鍵字)
POSITION_COLUMNS = {
    "spec": "trace",
    "design": "fact",
}

# 表頭欄名（小寫比對）
COL_ALIASES: dict[str, set[str]] = {
    "id": {"id", "fact", "fact id", "編號"},
    "claim": {"主張", "claim"},
    "evidence": {"證據", "evidence"},
    "page": {"題目頁", "page"},
    "spec": {"spec", "規範"},
    "design": {"design", "設計"},
}

CODE_SPAN_RE = re.compile(r"`([^`]+)`")
# 位址的路徑段必須長得像檔案路徑（無空白、有副檔名）。這使證據欄裡含 `#` 的
# 數學式（例如 `score(a) + score(b) ≡ 20 + #(平手)`）不會被誤判為位址。
ADDR_PATH_RE = re.compile(r"^[\w./\-]+\.[A-Za-z0-9]+$")
SUPPORTED_SUFFIXES = (".json", ".jsonl")
# fact id 的形狀（例如 D1、E11、W6）。標記內不符此形狀的 token 視為自由註記
# （例如 `(fact B1, proven)` 的 proven），不當成 fact id。
FACT_ID_RE = re.compile(r"^[A-Za-z]{1,3}\d{1,3}$")
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
# lookahead 把上標字元和 [A-Za-z_] 併在同一組，讓「底數＋上標」整串都不被掃描
# （`10⁹`、`2²⁹`）。只排除上標字元本身不夠：正則會回溯成更短的比對，底數仍會
# 被切出一個裸數字（曾實際誤報 G8 的 `10`）。
NUM_RE = re.compile(
    r"(?<![A-Za-z0-9_.,])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
    rf"(?![\d,]*[A-Za-z_{SUPERSCRIPT_DIGITS}])"
)
# 緊貼數字的已知單位後綴。掃描前插入一個空白把它隔開，否則 NUM_RE 的負向
# lookahead 會讓 `999ms`／`3010ops`／`300MiB` 整個掃不到（該列即使有位址也不做
# 檢查，且不留痕跡）。白名單制：長的排前面，`2x3` 因為後面接數字所以不算單位。
UNIT_SUFFIXES = (
    "bytes", "byte", "ops", "op", "MiB", "GiB", "KiB", "TiB",
    "MB", "GB", "KB", "kB", "ms", "µs", "μs", "us", "s", "x",
)
UNIT_SUFFIX_RE = re.compile(
    r"(?<=\d)(" + "|".join(sorted(UNIT_SUFFIXES, key=len, reverse=True)) + r")(?![A-Za-z0-9_])"
)
# 模糊量詞與中文數字量詞（見模組 docstring 的 claim-fuzzy-quantity 段）
CJK_NUMERALS = "零〇一二三四五六七八九十百千萬万兩两半"
CJK_MEASURE_UNITS = "倍|成|數量級|数量级|毫秒|秒|分之|位元組|个百分点|個百分點"
FUZZY_WORDS = "大約|大约|將近|将近|不到|超過|超过|多於|多于|少於|少于|上下|左右|約|约|逾|近"
CJK_QUANTITY_RE = re.compile(rf"[{CJK_NUMERALS}]+個?(?:{CJK_MEASURE_UNITS})")
FUZZY_QUANTITY_RE = re.compile(rf"(?:{FUZZY_WORDS})\s*[{CJK_NUMERALS}]")

#: 英文面的模糊量詞。本 change 的規範層（spec.md）與論證層（design.md）是英文，
#: 若只擋中文，這條規則在規範層等於不存在——2026-08-15 第三輪稽核點名的缺口。
#:
#: 刻意**不**全面禁止英文數字詞：`one line`、`two integers`、`the first entry`
#: 這類寫法在 spec 裡有 178 處且全部合法，全面禁會製造大量假陽性而讓規則失效。
#: 只鎖定「用模糊說法代替一個本該有出處的量測值」這一類：
#:   - order(s) of magnitude —— 用數量級代替實際比值
#:   - roughly / approximately / about / nearly / around ＋ 英文數字詞
#:     （後面接阿拉伯數字不算，那個數字本身已受 (b)/(d) 檢查）
#:   - a (fixed) multiplier/factor/ratio of ＋ 英文數字詞
EN_NUMBER_WORDS = (
    "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    "twenty|thirty|forty|fifty|hundred|thousand"
)
EN_VAGUE_WORDS = "roughly|approximately|about|nearly|around|some"
EN_FUZZY_RES = (
    re.compile(r"\borders?\s+of\s+magnitude\b", re.I),
    re.compile(rf"\b(?:{EN_VAGUE_WORDS})\s+(?:{EN_NUMBER_WORDS})\b", re.I),
    re.compile(rf"\b(?:multiplier|factor|ratio)\s+of\s+(?:{EN_NUMBER_WORDS})\b", re.I),
    re.compile(rf"\ba\s+fixed\s+(?:multiplier|factor)\s+of\s+(?:{EN_NUMBER_WORDS})\b", re.I),
)
# (d) 段：句子切分。標點之後必須接空白或區塊結尾才算句尾，故 `3.98` 不被切開。
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])(?=\s|$)")
LIST_ITEM_RE = re.compile(r"^(?:#{1,6}\s|[-*+>]\s|[-*+>]$|\d+[.)]\s|-{3,}$|\*{3,}$)")
# 「整格就是數值或比值」的字串葉節點（`"20"`、`"3.98"`、`"13/20"`）
SCORE_STRING_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)(?:\s*/\s*(\d+(?:\.\d+)?))?\s*$")
# 鍵路徑分段：.name、["含點的鍵"]、['含點的鍵']、[index]
KEY_SEG_RE = re.compile(r"""\.([^.\[\]]+)|\["([^"]*)"\]|\['([^']*)'\]|\[(\d+)\]""")


class Finding:
    """一條檢查結果。``ok`` 為 False 即 FAIL。"""

    def __init__(
        self,
        check: str,
        code: str,
        ok: bool,
        fact: str,
        message: str,
        detail: dict[str, Any] | None = None,
    ) -> None:
        self.check = check
        self.code = code
        self.ok = ok
        self.fact = fact
        self.message = message
        self.detail = detail or {}

    def as_dict(self) -> dict[str, Any]:
        return {
            "check": self.check,
            "code": self.code,
            "status": "PASS" if self.ok else "FAIL",
            "fact": self.fact,
            "message": self.message,
            "detail": self.detail,
        }


class MatrixError(Exception):
    """矩陣本身讀不進來（不是內容錯，是格式壞到無法檢查）。"""


# --- 矩陣解析 ----------------------------------------------------------------


def split_table_row(line: str) -> list[str]:
    """切 markdown 表格列，且**不切開 code span 內的 ``|``**。"""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_code = False
    prev = ""
    for ch in line:
        if ch == "`":
            in_code = not in_code
            buf.append(ch)
        elif ch == "|" and not in_code and prev != "\\":
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        prev = ch
    cells.append("".join(buf).strip())
    return cells


def _match_column(name: str) -> str | None:
    key = name.strip().strip("*` ").lower()
    for canon, aliases in COL_ALIASES.items():
        if key in aliases:
            return canon
    return None


def parse_matrix(path: Path) -> list[dict[str, str]]:
    """把矩陣裡所有符合欄位契約的表格列解析成 dict。

    回傳的每一列含 ``id`` / ``claim`` / ``evidence`` / ``spec`` / ``design`` /
    ``line``（1-based 行號）。缺欄的表格直接忽略（那不是追溯表）。
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.strip().startswith("|"):
            header = [_match_column(c) for c in split_table_row(line)]
            need = {"id", "claim", "evidence"}
            if need.issubset({h for h in header if h}):
                idx += 1
                # 跳過分隔列
                if idx < len(lines) and set(lines[idx].strip()) <= set("|-: "):
                    idx += 1
                while idx < len(lines) and lines[idx].strip().startswith("|"):
                    cells = split_table_row(lines[idx])
                    row: dict[str, str] = {"line": str(idx + 1)}
                    for pos, canon in enumerate(header):
                        if canon and pos < len(cells):
                            row[canon] = cells[pos]
                    if row.get("id"):
                        row["id"] = row["id"].strip("*` ")
                        rows.append(row)
                    idx += 1
                continue
        idx += 1
    if not rows:
        raise MatrixError(f"{path} 內找不到任何含 id／主張／證據 欄的表格")
    return rows


# --- (a) 位址解析 -------------------------------------------------------------


def extract_addresses(evidence: str) -> list[str]:
    """抓證據欄裡形如 ``路徑#鍵路徑`` 的 code span。

    只有 ``#`` 前面長得像檔案路徑的 code span 才算位址；其餘（數學式、識別字）
    一律略過。副檔名不支援時仍算位址——那是筆誤，要叫出來，不能靜靜跳過。
    """
    out = []
    for span in CODE_SPAN_RE.findall(evidence):
        span = span.strip()
        head, sep, _ = span.partition("#")
        if sep and ADDR_PATH_RE.match(head):
            out.append(span)
    return out


def _walk_keypath(value: Any, keypath: str, addr: str) -> Any:
    """依鍵路徑走進 json 結構；失敗時丟出指名到「哪一段」的 ValueError。"""
    walked = ""
    pos = 0
    if keypath and not keypath.startswith(("[", ".")):
        keypath = "." + keypath
    while pos < len(keypath):
        m = KEY_SEG_RE.match(keypath, pos)
        if not m:
            raise ValueError(f"鍵路徑語法錯誤，卡在 `{keypath[pos:]}`")
        pos = m.end()
        name = m.group(1) if m.group(1) is not None else (m.group(2) or m.group(3))
        index = m.group(4)
        if name is not None:
            walked += f".{name}"
            if not isinstance(value, dict):
                raise ValueError(f"`{walked}` 之前的值是 {type(value).__name__}，不是 dict")
            if name not in value:
                keys = ", ".join(list(value)[:8])
                hint = [k for k in value if k.startswith(name + ".")]
                extra = f"；該層有含點的鍵 `{hint[0]}`，請改寫成 [\"{hint[0]}\"]" if hint else ""
                raise ValueError(f"鍵 `{name}` 不存在（該層可用鍵：{keys}）{extra}")
            value = value[name]
        else:
            i = int(index)
            walked += f"[{i}]"
            if not isinstance(value, list):
                raise ValueError(f"`{walked}` 之前的值是 {type(value).__name__}，不是 list")
            if i >= len(value):
                raise ValueError(f"索引 [{i}] 超出範圍（長度 {len(value)}）")
            value = value[i]
    return value


def resolve_address(change: Path, addr: str) -> Any:
    """解析一個 ``路徑#鍵路徑`` 位址，回傳其值。失敗丟 ValueError。"""
    rel, _, keypath = addr.partition("#")
    target = change / rel
    if not target.exists():
        raise ValueError(f"檔案不存在：{rel}")
    if not keypath:
        raise ValueError("位址缺鍵路徑（`#` 後為空）")
    if target.suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"只支援 {'／'.join(SUPPORTED_SUFFIXES)} 位址，實得 `{target.suffix}`")

    if target.suffix == ".jsonl":
        m = re.match(r"^label=([^.\[]+)(.*)$", keypath)
        if not m:
            raise ValueError("jsonl 位址必須以 `label=<值>` 開頭")
        label, tail = m.group(1), m.group(2)
        records = []
        for lineno, raw in enumerate(target.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                records.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{rel} 第 {lineno} 行不是合法 JSON：{exc}") from exc
        hits = [r for r in records if isinstance(r, dict) and r.get("label") == label]
        if not hits:
            avail = ", ".join(
                sorted({str(r.get("label")) for r in records if isinstance(r, dict)})
            )
            raise ValueError(f"找不到 label=`{label}`（檔內 label：{avail}）")
        if len(hits) > 1:
            raise ValueError(f"label=`{label}` 在檔內出現 {len(hits)} 次，無法唯一定位")
        return _walk_keypath(hits[0], tail, addr)

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{rel} 不是合法 JSON：{exc}") from exc
    return _walk_keypath(data, keypath, addr)


# --- (b) 數字綁鍵 -------------------------------------------------------------


def numeric_leaves(value: Any) -> list[float]:
    """攤平出所有數值葉節點（bool 不算數字）。

    字串葉節點只在**整格就是一個數值或比值**時才拆出數字（``"13/20"``、``"3.98"``）——
    得分這類量測值在多份 harness 裡是以 ``"13/20"`` 形式存的，那仍然是「值在該位址」。
    含散文的字串（``"每筆重複 7 次取最小值…"``）一律不拆，否則備註欄裡的任何數字
    都會變成候選值，檢查等於失效。
    """
    out: list[float] = []
    stack = [value]
    while stack:
        cur = stack.pop()
        if isinstance(cur, bool):
            continue
        if isinstance(cur, (int, float)):
            out.append(float(cur))
        elif isinstance(cur, str):
            m = SCORE_STRING_RE.match(cur)
            if m:
                out.extend(float(x) for x in m.groups() if x is not None)
        elif isinstance(cur, dict):
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return out


def strip_unscanned(text: str) -> str:
    """把 code span 與 ISO 日期換成空白，並把緊貼數字的單位後綴隔開。"""
    text = CODE_SPAN_RE.sub(" ", text)
    text = ISO_DATE_RE.sub(" ", text)
    return UNIT_SUFFIX_RE.sub(r" \1", text)


def claim_numbers(claim: str) -> list[str]:
    """抓一段文字裡「被主張的量測值」（規則見模組 docstring）。"""
    return [m.group(1) for m in NUM_RE.finditer(strip_unscanned(claim))]


def fuzzy_quantities(claim: str) -> list[str]:
    """抓主張欄裡不受數字檢查的模糊量詞／中文數字量詞（規則見模組 docstring）。"""
    text = strip_unscanned(claim)
    hits = [m.group(0) for m in CJK_QUANTITY_RE.finditer(text)]
    hits += [m.group(0) for m in FUZZY_QUANTITY_RE.finditer(text)]
    for rx in EN_FUZZY_RES:
        hits += [m.group(0) for m in rx.finditer(text)]
    seen: list[str] = []
    for h in hits:
        if h not in seen:
            seen.append(h)
    return seen


def claim_segments(claim: str) -> list[str] | None:
    """主張欄以 ``／`` 切段；不適合逐一對位時回傳 None（規則見模組 docstring）。"""
    text = strip_unscanned(claim)
    if "／" not in text:
        return None
    segments = text.split("／")
    if len(segments) < 2:
        return None
    if not all(NUM_RE.search(seg) for seg in segments):
        return None
    return segments


def number_matches(token: str, candidates: list[float]) -> bool:
    """散文數字 token 是否等於任一候選值（四捨五入到 token 的小數位數）。"""
    plain = token.replace(",", "")
    try:
        target = float(plain)
    except ValueError:
        return False
    decimals = len(plain.split(".")[1]) if "." in plain else 0
    for value in candidates:
        if abs(round(value, decimals) - target) <= 1e-9 * max(1.0, abs(target)):
            return True
    return False


# --- (c) 位置欄 ---------------------------------------------------------------


def classify_position(cell: str) -> tuple[str, str]:
    """把位置欄的值分類成 ``yes`` / ``no`` / ``skip`` / ``bad``，並回傳其餘文字。"""
    text = cell.strip()
    if not text:
        return "bad", text
    head = text[0]
    if head in MARK_YES:
        return "yes", text[1:].strip()
    if head == MARK_SKIP:
        return "skip", text[1:].strip()
    if text in MARK_NO:
        return "no", ""
    return "bad", text


def has_reason(rest: str) -> bool:
    """``△`` 後面是否接了一句括號理由。"""
    for lo, hi in (("(", ")"), ("（", "）")):
        if lo in rest and hi in rest.split(lo, 1)[1]:
            inner = rest.split(lo, 1)[1].split(hi, 1)[0]
            if inner.strip():
                return True
    return False


def collect_markers(text: str, keyword: str, known: set[str]) -> dict[str, int]:
    """抓文件中的 ``(trace X)`` / ``(fact X)`` 標記。

    支援一個標記帶多個 id（``(trace D7/E7)``、``(fact E10, G7)``）。
    非 fact id 形狀且不在矩陣已知 id 內的 token 視為自由註記而略過。
    """
    found: dict[str, int] = {}
    for raw in re.findall(rf"\({keyword}s?\s+([^)]+)\)", text):
        for part in re.split(r"[/、,，\s]+", raw.strip()):
            part = part.strip()
            if part and (part in known or FACT_ID_RE.match(part)):
                found[part] = found.get(part, 0) + 1
    return found


def find_target_docs(change: Path, kind: str) -> list[Path]:
    if kind == "design":
        path = change / "design.md"
        return [path] if path.exists() else []
    return sorted(change.glob("specs/**/spec.md"))


# --- (d) 文件數字綁鍵 ---------------------------------------------------------

EXEMPT_COLUMNS: dict[str, set[str]] = {
    "doc": {"文件", "doc", "file", "檔案"},
    "fact": {"fact", "fact id", "id", "編號"},
    "number": {"數字", "number", "值"},
    "reason": {"理由", "reason", "說明"},
}


def doc_scopes(text: str) -> list[tuple[int, str]]:
    """把文件切成 ``(行號, 句子)``。切法與取捨見模組 docstring 的 (d) 段。"""
    blocks: list[tuple[int, str]] = []
    para: list[str] = []
    para_line = 0

    def flush() -> None:
        nonlocal para, para_line
        if para:
            blocks.append((para_line, " ".join(para)))
            para = []

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("|"):
            flush()
            for cell in split_table_row(line):
                if cell:
                    blocks.append((lineno, cell))
            continue
        if LIST_ITEM_RE.match(line):
            flush()
            blocks.append((lineno, line))
            continue
        if not para:
            para_line = lineno
        para.append(line)
    flush()

    out: list[tuple[int, str]] = []
    for lineno, block in blocks:
        for part in SENTENCE_SPLIT_RE.split(block):
            if part.strip():
                out.append((lineno, part.strip()))
    return out


def _match_exempt_column(name: str) -> str | None:
    key = name.strip().strip("*` ").lower()
    for canon, aliases in EXEMPT_COLUMNS.items():
        if key in aliases:
            return canon
    return None


def canonical_number(token: str) -> str:
    """例外表的數字比對鍵：去掉千分位逗號，其餘原樣（``1,000`` 與 ``1000`` 同鍵）。"""
    return token.replace(",", "").strip()


def parse_exemptions(path: Path) -> list[dict[str, str]]:
    """讀〈(d) 文件數字例外表〉。四欄缺一即不視為例外表（整張忽略）。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, str]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.strip().startswith("|"):
            header = [_match_exempt_column(c) for c in split_table_row(line)]
            if {"doc", "fact", "number", "reason"}.issubset({h for h in header if h}):
                idx += 1
                if idx < len(lines) and set(lines[idx].strip()) <= set("|-: "):
                    idx += 1
                while idx < len(lines) and lines[idx].strip().startswith("|"):
                    cells = split_table_row(lines[idx])
                    row = {"line": str(idx + 1)}
                    for pos, canon in enumerate(header):
                        if canon and pos < len(cells):
                            row[canon] = cells[pos].strip("*` ").strip()
                    if row.get("doc") and row.get("fact") and row.get("number"):
                        row.setdefault("reason", "")
                        out.append(row)
                    idx += 1
                continue
        idx += 1
    return out


# --- 主流程 ------------------------------------------------------------------


def run_lint(change: Path) -> dict[str, Any]:
    """跑完四段檢查，回傳結構化結果。"""
    matrix_path = change / "trace-matrix.md"
    if not matrix_path.exists():
        raise MatrixError(f"找不到 {matrix_path}")
    rows = parse_matrix(matrix_path)
    exemptions = parse_exemptions(matrix_path)

    findings: list[Finding] = []
    n_addresses = 0
    n_markers = 0
    n_doc_numbers = 0
    # fact id → 該列所有位址的數值候選；以及 位址 → 摘要（供 (d) 的錯誤訊息用）
    row_candidates: dict[str, list[float]] = {}
    row_resolved: dict[str, dict[str, str]] = {}

    # --- 矩陣結構：id 必須唯一，否則「單一真相來源」在自己內部就分岔了 ---
    seen: dict[str, str] = {}
    for row in rows:
        if row["id"] in seen:
            findings.append(
                Finding(
                    "matrix",
                    "row-duplicate-id",
                    False,
                    row["id"],
                    f"fact id `{row['id']}` 重複出現："
                    f"trace-matrix.md:{seen[row['id']]} 與 trace-matrix.md:{row['line']}",
                    {"lines": [seen[row["id"]], row["line"]]},
                )
            )
        else:
            seen[row["id"]] = row["line"]

    # --- (a) + (b) ---
    for row in rows:
        fact = row["id"]
        where = f"trace-matrix.md:{row['line']}"
        addresses = extract_addresses(row.get("evidence", ""))
        resolved: dict[str, Any] = {}
        for addr in addresses:
            n_addresses += 1
            try:
                value = resolve_address(change, addr)
            except ValueError as exc:
                findings.append(
                    Finding(
                        "a-address",
                        "addr-unresolvable",
                        False,
                        fact,
                        f"{where} 位址 `{addr}` 解析失敗：{exc}",
                        {"address": addr, "error": str(exc)},
                    )
                )
                continue
            resolved[addr] = value
            findings.append(
                Finding(
                    "a-address",
                    "addr-ok",
                    True,
                    fact,
                    f"位址 `{addr}` → {summarize(value)}",
                    {"address": addr},
                )
            )

        if not addresses:
            continue

        candidates: list[float] = []
        for value in resolved.values():
            candidates.extend(numeric_leaves(value))
        detail = {addr: summarize(val) for addr, val in resolved.items()}
        lines = "；".join(f"`{a}` = {v}" for a, v in detail.items()) or "（無可解析位址）"
        row_candidates[fact] = candidates
        row_resolved[fact] = detail

        claim = row.get("claim", "")

        # 模糊量詞／中文數字量詞：宣稱了一個量卻沒有任何東西驗它
        for phrase in fuzzy_quantities(claim):
            findings.append(
                Finding(
                    "b-number",
                    "claim-fuzzy-quantity",
                    False,
                    fact,
                    f"{where} 主張欄的「{phrase}」是不受檢查的量："
                    f"中文數字量詞與模糊量詞都掃不到，等於這個量沒有任何機械保證。"
                    f"兩條出路擇一：改寫成精確的阿拉伯數字讓它受檢查，"
                    f"或把該列證據欄的位址整格拿掉改成純散文，明白宣告放棄機械檢查",
                    {"phrase": phrase, "claim": claim},
                )
            )

        # 多位址逐一對位；不適用時退回聯集比對
        segments = claim_segments(claim)
        ordered = list(resolved.items())
        if segments is not None and len(segments) == len(ordered):
            for pos, (seg, (addr, value)) in enumerate(zip(segments, ordered), 1):
                seg_values = numeric_leaves(value)
                for m in NUM_RE.finditer(seg):
                    token = m.group(1)
                    if number_matches(token, seg_values):
                        findings.append(
                            Finding(
                                "b-number",
                                "number-bound",
                                True,
                                fact,
                                f"數字 {token} 已逐一對位到 `{addr}`",
                            )
                        )
                    else:
                        findings.append(
                            Finding(
                                "b-number",
                                "number-misplaced",
                                False,
                                fact,
                                f"{where} 主張欄第 {pos} 段的數字 {token} "
                                f"對不上同序位址 `{addr}` = {summarize(value)}"
                                f"（該列以 ／ 切出 {len(segments)} 段、位址也是 {len(ordered)} 個，"
                                f"故改做逐一對位；順序寫反即在此現形）",
                                {"number": token, "address": addr, "segment": seg.strip()},
                            )
                        )
            continue

        for token in claim_numbers(claim):
            if number_matches(token, candidates):
                findings.append(
                    Finding("b-number", "number-bound", True, fact, f"數字 {token} 已綁鍵")
                )
            else:
                findings.append(
                    Finding(
                        "b-number",
                        "number-unbound",
                        False,
                        fact,
                        f"{where} 主張欄的數字 {token} 對不上該列任何位址；該列位址解析值：{lines}",
                        {"number": token, "resolved": detail},
                    )
                )

    # --- (c) ---
    by_id = {row["id"]: row for row in rows}
    for column, keyword in POSITION_COLUMNS.items():
        docs = find_target_docs(change, column)
        doc_text = "\n".join(p.read_text(encoding="utf-8") for p in docs)
        doc_names = ", ".join(str(p.relative_to(change)) for p in docs) or f"（無 {column} 文件）"
        markers = collect_markers(doc_text, keyword, set(by_id))
        n_markers += sum(markers.values())

        for row in rows:
            fact = row["id"]
            where = f"trace-matrix.md:{row['line']}"
            cell = row.get(column)
            if cell is None:
                findings.append(
                    Finding(
                        "c-position",
                        "pos-missing-column",
                        False,
                        fact,
                        f"{where} 缺 `{column}` 欄",
                        {"column": column},
                    )
                )
                continue
            kind, rest = classify_position(cell)
            if kind == "bad":
                findings.append(
                    Finding(
                        "c-position",
                        "pos-bad-value",
                        False,
                        fact,
                        f"{where} 的 `{column}` 欄值 {cell!r} 不是 ✓／—／△ 三者之一",
                        {"column": column, "value": cell},
                    )
                )
            elif kind == "skip":
                if has_reason(rest):
                    findings.append(
                        Finding(
                            "c-position", "pos-skip-ok", True, fact, f"`{column}` 欄 △（有理由）"
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "c-position",
                            "pos-skip-no-reason",
                            False,
                            fact,
                            f"{where} 的 `{column}` 欄標 △ 卻沒有括號理由",
                            {"column": column, "value": cell},
                        )
                    )
            elif kind == "yes":
                if fact in markers:
                    findings.append(
                        Finding(
                            "c-position",
                            "pos-marker-present",
                            True,
                            fact,
                            f"{doc_names} 含 ({keyword} {fact})",
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "c-position",
                            "pos-marker-missing",
                            False,
                            fact,
                            f"{where} 的 `{column}` 欄標 ✓，但 {doc_names} 找不到 ({keyword} {fact})",
                            {"column": column, "docs": doc_names},
                        )
                    )
            else:  # no
                if fact in markers:
                    findings.append(
                        Finding(
                            "c-position",
                            "pos-marker-forbidden",
                            False,
                            fact,
                            f"{where} 的 `{column}` 欄標 —，但 {doc_names} 出現了 ({keyword} {fact})",
                            {"column": column, "docs": doc_names},
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            "c-position", "pos-absent-ok", True, fact, f"{doc_names} 未出現 {fact}"
                        )
                    )

        # 反向：文件裡的標記必須在矩陣中且該欄為 ✓
        for fact in sorted(markers):
            if fact not in by_id:
                findings.append(
                    Finding(
                        "c-position",
                        "pos-orphan-marker",
                        False,
                        fact,
                        f"{doc_names} 有 ({keyword} {fact})，但矩陣沒有這個 fact id",
                        {"column": column, "docs": doc_names},
                    )
                )

    # --- (d) 文件散文的數字綁鍵 ---
    exempt_index: dict[tuple[str, str, str], dict[str, str]] = {}
    for ex in exemptions:
        key = (ex["doc"], ex["fact"], canonical_number(ex["number"]))
        exempt_index[key] = ex
        if not ex.get("reason", "").strip():
            findings.append(
                Finding(
                    "d-doc-number",
                    "doc-number-exempt-no-reason",
                    False,
                    ex["fact"],
                    f"trace-matrix.md:{ex['line']} 的例外「{ex['doc']} / {ex['fact']} / "
                    f"{ex['number']}」沒有寫理由；例外表的每一列都必須說明為什麼這個數字"
                    f"無法綁鍵",
                    {"exemption": ex},
                )
            )
    used_exemptions: set[tuple[str, str, str]] = set()

    for column, keyword in POSITION_COLUMNS.items():
        for path in find_target_docs(change, column):
            doc_name = path.name
            rel = str(path.relative_to(change))
            for lineno, sentence in doc_scopes(path.read_text(encoding="utf-8")):
                facts = sorted(collect_markers(sentence, keyword, set(by_id)))
                if not facts:
                    continue
                pool: list[float] = []
                for fact in facts:
                    pool.extend(row_candidates.get(fact, []))
                if not pool:
                    continue  # 該句所標的 fact 全無可解析位址：與 (b) 同一個逃生口
                # 模糊量詞：句子若用「an order of magnitude」「a fixed multiplier of four」
                # 這類說法代替一個本該有出處的量測值，數字檢查根本掃不到它。
                # 規範層是英文，所以這條規則在英文面才真正有作用（第三輪稽核缺口）。
                for phrase in fuzzy_quantities(sentence):
                    label = "／".join(facts)
                    findings.append(
                        Finding(
                            "d-doc-number",
                            "doc-fuzzy-quantity",
                            False,
                            label,
                            f"{rel}:{lineno} 句中以模糊量詞「{phrase}」代替量測值，"
                            f"數字檢查掃不到它。該句：「{sentence[:120]}」。"
                            f"請改寫成精確數字（會自動受 (d) 檢查），"
                            f"或改寫成不帶量的定性敘述",
                            {"phrase": phrase, "doc": rel, "line": lineno, "facts": facts},
                        )
                    )
                for token in claim_numbers(sentence):
                    n_doc_numbers += 1
                    label = "／".join(facts)
                    if number_matches(token, pool):
                        findings.append(
                            Finding(
                                "d-doc-number",
                                "doc-number-bound",
                                True,
                                label,
                                f"{rel}:{lineno} 的 {token} 已綁鍵",
                            )
                        )
                        continue
                    hit = next(
                        (
                            (doc_name, f, canonical_number(token))
                            for f in facts
                            if (doc_name, f, canonical_number(token)) in exempt_index
                        ),
                        None,
                    )
                    if hit is not None:
                        used_exemptions.add(hit)
                        findings.append(
                            Finding(
                                "d-doc-number",
                                "doc-number-exempt",
                                True,
                                label,
                                f"{rel}:{lineno} 的 {token} 已登記為例外："
                                f"{exempt_index[hit]['reason']}",
                            )
                        )
                        continue
                    values = "；".join(
                        f"`{a}` = {v}"
                        for f in facts
                        for a, v in row_resolved.get(f, {}).items()
                    ) or "（該列無可解析位址）"
                    findings.append(
                        Finding(
                            "d-doc-number",
                            "doc-number-unbound",
                            False,
                            label,
                            f"{rel}:{lineno} 句中的數字 {token} 對不上 {label} 任何位址的值。"
                            f"該句：「{sentence[:120]}」。{label} 的位址解析值：{values}。"
                            f"修法方向恆為「跑腳本 → 用輸出覆寫散文」；若確實無法綁鍵，"
                            f"請登記進 trace-matrix.md 的〈(d) 文件數字例外表〉並寫明理由",
                            {"number": token, "doc": rel, "line": lineno, "facts": facts},
                        )
                    )

    for key, ex in exempt_index.items():
        if key in used_exemptions:
            continue
        findings.append(
            Finding(
                "d-doc-number",
                "doc-number-exempt-stale",
                False,
                ex["fact"],
                f"trace-matrix.md:{ex['line']} 登記的例外「{ex['doc']} / {ex['fact']} / "
                f"{ex['number']}」本輪完全沒被用到：該數字要嘛已經綁得上鍵、要嘛已從文件消失。"
                f"請刪掉這一列，例外表不留死條目",
                {"exemption": ex},
            )
        )

    fails = [f for f in findings if not f.ok]
    return {
        "change": str(change),
        "stats": {
            "rows": len(rows),
            "addresses": n_addresses,
            "markers": n_markers,
            "doc_numbers": n_doc_numbers,
            "exemptions": len(exempt_index),
            "checks": len(findings),
            "failures": len(fails),
        },
        "findings": [f.as_dict() for f in findings],
    }


def summarize(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 80 else text[:77] + "..."


def report(result: dict[str, Any]) -> None:
    order = {
        "matrix": "矩陣結構",
        "a-address": "(a) 位址可解析",
        "b-number": "(b) 數字綁鍵",
        "c-position": "(c) 位置欄雙向",
        "d-doc-number": "(d) 文件數字綁鍵",
    }
    for check, title in order.items():
        items = [f for f in result["findings"] if f["check"] == check]
        fails = [f for f in items if f["status"] == "FAIL"]
        if not items:
            continue
        print(f"\n=== {title} ===  {len(items) - len(fails)} PASS / {len(fails)} FAIL")
        for f in fails:
            print(f"  FAIL [{f['fact']}] {f['code']}: {f['message']}")
    stats = result["stats"]
    print(
        f"\n--- 統計 ---\n"
        f"矩陣列數：{stats['rows']}　可解析位址：{stats['addresses']}　"
        f"文件標記：{stats['markers']}　文件受檢數字：{stats['doc_numbers']}　"
        f"登記例外：{stats['exemptions']}　"
        f"檢查項：{stats['checks']}　FAIL：{stats['failures']}"
    )


# --- 自我測試 ----------------------------------------------------------------

SELF_TEST_JSON = {
    "margin": 3.98,
    "score_text": "13/20",           # 整格即比值的字串 → 算候選值
    "note": "上一輪曾量到 803 ms",   # 含散文的字串 → 不算候選值
    "wall": {"plain": 16.43},
    # routes[0] 給 op 數；routes[1..4] 給四條錯誤路線的得分，供逐一對位用
    # （其中兩條同值 2——這正是聯集比對看不見、逐一對位才看得見的情形）
    "routes": [
        {"max_ops": 3010},
        {"score_n": 1},
        {"score_n": 2},
        {"score_n": 2},
        {"score_n": 0},
    ],
    "entries": [8, 1, 2],
    "ops": {"r015_rowscan.py": 1008010},  # 含點號的鍵，驗證引號方括號語法
}
SELF_TEST_JSONL = (
    '{"label": "ref015", "rows": 20, "score": 20, "max_ms": 375.0}\n'
    '{"label": "cellscan", "rows": 20, "score": 8, "max_ms": 1950.0}\n'
)


def _write_fixture(root: Path, matrix: str, spec: str, design: str) -> Path:
    change = root
    (change / "measure").mkdir(parents=True, exist_ok=True)
    (change / "curation").mkdir(parents=True, exist_ok=True)
    (change / "specs" / "demo").mkdir(parents=True, exist_ok=True)
    (change / "curation" / "plan.py").write_text("margin = 3.98\n", encoding="utf-8")
    (change / "measure" / "m.json").write_text(
        json.dumps(SELF_TEST_JSON, ensure_ascii=False), encoding="utf-8"
    )
    (change / "measure" / "b.jsonl").write_text(SELF_TEST_JSONL, encoding="utf-8")
    (change / "trace-matrix.md").write_text(matrix, encoding="utf-8")
    (change / "specs" / "demo" / "spec.md").write_text(spec, encoding="utf-8")
    (change / "design.md").write_text(design, encoding="utf-8")
    return change


GOOD_MATRIX = """# 假矩陣

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| A1 | 餘裕為 3.98 倍，最貴寫法約佔 16.43% | `measure/m.json#margin`、`measure/m.json#wall.plain` | 散文 | ✓ | — |
| A2 | REFERENCE 最大 op 3,010 | `measure/m.json#routes[0].max_ops` | 範例 | — | ✓ |
| A3 | cellscan 瀏覽器得 8/20 | `measure/b.jsonl#label=cellscan.score`、`measure/b.jsonl#label=cellscan.rows` | 效能提醒 | ✓ | — |
| A4 | 訪談決策，無量測；下界推導為 `score(甲) + score(乙) ≡ 20 + #(平手)` | 2026-08-15 訪談 Q1，見 `curation/plan.py` | 全篇 | △（無外部真值，僅檢查有無被引用） | — |
| A5 | 明寫迴圈 1,008,010 op | `measure/m.json#ops["r015_rowscan.py"]` | — | — | — |
| A7 | 投影得分 13/20 | `measure/m.json#score_text` | — | — | — |
| A6 | n=10⁹ 時 REFERENCE 仍為 3,010 op（含上標的整串不掃描，底數也不切出來） | `measure/m.json#routes[0].max_ops` | — | — | — |
| A8 | 單位後綴緊貼數字也要被掃到：3,010ops、約 3.98x、16.43% | `measure/m.json#routes[0].max_ops`、`measure/m.json#margin`、`measure/m.json#wall.plain` | — | — | — |
| A9 | 四條錯誤路線得分 1／2／2／0 | `measure/m.json#routes[1].score_n`、`measure/m.json#routes[2].score_n`、`measure/m.json#routes[3].score_n`、`measure/m.json#routes[4].score_n` | — | — | — |

### (d) 文件數字例外表

| 文件 | fact | 數字 | 理由 |
|---|---|---|---|
| spec.md | A3 | 9 | 「第 9 筆」是序數，無對應鍵（自我測試的正向案例） |
"""

GOOD_SPEC = (
    "規範層 (trace A1) 與 (trace A3) 都在這裡。\n\n"
    "餘裕為 3.98 倍，最貴寫法佔 16.43% (trace A1)。\n\n"
    "cellscan 在第 9 筆起死亡，得 8/20 (trace A3)。\n"
)
# 同時驗證複數形標記與 `(fact X, 註記)` 這種自由註記不會製造假 orphan
GOOD_DESIGN = "設計層只引 (facts A2, proven)：REFERENCE 最大 op 3,010。\n"

BAD_MATRIX = """# 假矩陣（每段各埋一個錯）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| A1 | 餘裕為 3.98 倍 | `measure/m.json#margin` | 散文 | ✓ | — |
| B1 | 檔案不存在 | `measure/nope.json#margin` | 散文 | — | — |
| B2 | 鍵不存在 | `measure/m.json#wall.helper` | 散文 | — | — |
| B3 | label 不存在 | `measure/b.jsonl#label=ghost.score` | 散文 | — | — |
| B4 | 副檔名不支援 | `curation/plan.py#margin` | 散文 | — | — |
| C1 | 餘裕為 4.62 倍 | `measure/m.json#margin` | 散文 | — | — |
| C2 | 上一輪量到 803 ms | `measure/m.json#note` | 散文 | — | — |
| D1 | spec 應有標記卻沒有 | `measure/m.json#margin` | 散文 | ✓ | — |
| D2 | 餘裕為 3.98 倍，spec 不該有卻有 | `measure/m.json#margin` | 散文 | — | — |
| D3 | 餘裕為 3.98 倍，△ 沒理由 | `measure/m.json#margin` | 散文 | △ | — |
| D4 | 位置欄值非法 | `measure/m.json#margin` | 散文 | 量測表 | — |
| C1 | 與上面的 C1 重複 id | 訪談記錄 | 散文 | — | — |
| C3 | 單位後綴貼著數字：999ms | `measure/m.json#margin` | 散文 | — | — |
| C4 | 餘裕不到四倍 | `measure/m.json#margin` | 散文 | — | — |
| C5 | 四條錯誤路線得分 1／2／2／0 | `measure/m.json#routes[2].score_n`、`measure/m.json#routes[1].score_n`、`measure/m.json#routes[3].score_n`、`measure/m.json#routes[4].score_n` | 散文 | — | — |

### (d) 文件數字例外表

| 文件 | fact | 數字 | 理由 |
|---|---|---|---|
| spec.md | A1 | 7.77 |  |
| spec.md | A1 | 999 | 這一列刻意沒被用到，應報 stale |
"""

BAD_SPEC = (
    "這裡有 (trace A1)、(trace D2)、以及矩陣沒有的 (trace ZZ9)。\n\n"
    "餘裕為 4.62 倍，另有 7.77 倍 (trace A1)。\n"
)
BAD_DESIGN = "設計層空白。\n"


def self_test() -> int:
    """用內建假矩陣驗證四段檢查各有正向與負向案例都會叫。"""
    problems: list[str] = []

    def expect(label: str, got: Any, want: Any) -> None:
        if got != want:
            problems.append(f"{label}：期望 {want!r}，實得 {got!r}")

    # --- 純函式層的正／負向控制 ---------------------------------------------
    # L1-1：單位後綴緊貼數字時，正規化前整個掃不到（且不留痕跡）
    expect(
        "單位後綴正規化（正向）",
        claim_numbers("999ms、3010ops、300MiB、1,008,010bytes"),
        ["999", "3010", "300", "1,008,010"],
    )
    expect(
        "單位後綴正規化不得誤傷 `2x3` 這種維度寫法（負向）",
        claim_numbers("2x3 的區塊與 apcs015"),
        [],
    )
    # 上標規則：`10⁹` 整串不得被拆成裸數字 10（A6 列的迴歸測）
    expect("上標規則", claim_numbers("n=10⁹ 與 2²⁹ 與 3,010"), ["3,010"])
    # L1-2：模糊量詞／中文數字量詞
    expect("模糊量詞（負向：不到四倍）", fuzzy_quantities("餘裕不到四倍"), ["四倍", "不到四"])
    expect("模糊量詞（負向：大約三倍）", fuzzy_quantities("大約三倍"), ["三倍", "大約三"])
    expect("模糊量詞（負向：一個數量級）", fuzzy_quantities("還有一個數量級的餘裕"), ["一個數量級"])
    expect("模糊量詞（正向：約 300 MiB 後接阿拉伯數字，不算命中）", fuzzy_quantities("約 300 MiB"), [])
    expect("模糊量詞（正向：3.98 倍是阿拉伯數字，不算命中）", fuzzy_quantities("餘裕 3.98 倍"), [])
    # 英文面（規範層是英文，只擋中文等於這條規則在規範層不存在）
    expect(
        "模糊量詞（負向：order of magnitude）",
        fuzzy_quantities("finishes at least an order of magnitude inside the deadline"),
        ["order of magnitude"],
    )
    expect(
        "模糊量詞（負向：a fixed multiplier of four）",
        fuzzy_quantities("with a fixed multiplier of four applied to local timings"),
        ["multiplier of four", "a fixed multiplier of four"],
    )
    expect(
        "模糊量詞（正向：roughly 250 後接阿拉伯數字，該數字自己受檢查）",
        fuzzy_quantities("any bound above roughly 250 discriminates identically"),
        [],
    )
    expect(
        "模糊量詞（正向：one line／two integers 是合法英文規格用語，不得誤殺）",
        fuzzy_quantities("SHALL accept one line holding two integers and emit the first entry"),
        [],
    )
    # L1-3：段數與位址數不吻合時必須退回聯集，不得硬對位
    expect(
        "逐一對位（負向：有段不含數字時不得對位）",
        claim_segments("四鍵（ ／ ／ ／ ）共 599 bytes"),
        None,
    )
    expect("逐一對位（負向：無 ／ 時不對位）", claim_segments("得分 1、2、2、0"), None)
    expect("逐一對位（正向）", claim_segments("得分 1／2／2／0"), ["得分 1", "2", "2", "0"])

    with tempfile.TemporaryDirectory() as tmp:
        good = _write_fixture(Path(tmp) / "good", GOOD_MATRIX, GOOD_SPEC, GOOD_DESIGN)
        result = run_lint(good)
        fails = [f for f in result["findings"] if f["status"] == "FAIL"]
        if fails:
            problems.append("正向案例應零 FAIL，實得：" + "; ".join(f["message"] for f in fails))
        # 正向也要證明「有真的檢查到東西」，不是空轉
        passed = {f["code"] for f in result["findings"] if f["status"] == "PASS"}
        for code in (
            "addr-ok",
            "number-bound",
            "pos-marker-present",
            "pos-absent-ok",
            "pos-skip-ok",
            "doc-number-bound",
            "doc-number-exempt",
        ):
            if code not in passed:
                problems.append(f"正向案例缺少 PASS 類別 {code}（檢查器可能空轉）")
        if result["stats"]["addresses"] != 15:
            problems.append(f"正向案例位址計數應為 15，實得 {result['stats']['addresses']}")
        if result["stats"]["doc_numbers"] < 6:
            problems.append(
                f"正向案例的文件受檢數字應 ≥ 6，實得 {result['stats']['doc_numbers']}"
                "——(d) 段可能整段沒掃到文件"
            )

        bad = _write_fixture(Path(tmp) / "bad", BAD_MATRIX, BAD_SPEC, BAD_DESIGN)
        result = run_lint(bad)
        codes = {f["code"] for f in result["findings"] if f["status"] == "FAIL"}
        expected = {
            "row-duplicate-id",  # 矩陣結構負向
            "addr-unresolvable",  # (a) 負向：檔案／鍵／label／副檔名 四種
            "number-unbound",  # (b) 負向
            "claim-fuzzy-quantity",  # (b) 負向：中文數字量詞／模糊量詞（L1-2）
            "number-misplaced",  # (b) 負向：多位址順序寫反（L1-3）
            "pos-marker-missing",  # (c) 負向：✓ 卻沒標記
            "pos-marker-forbidden",  # (c) 負向：— 卻有標記
            "pos-skip-no-reason",  # (c) 負向：△ 沒理由
            "pos-bad-value",  # (c) 負向：值非法
            "pos-orphan-marker",  # (c) 反向：文件有標記、矩陣沒有
            "doc-number-unbound",  # (d) 負向：散文數字對不上該 fact 的位址（L4-2）
            "doc-number-exempt-no-reason",  # (d) 負向：例外沒寫理由
            "doc-number-exempt-stale",  # (d) 負向：例外沒被用到
        }
        missing = expected - codes
        if missing:
            problems.append("負向案例未觸發：" + ", ".join(sorted(missing)))
        addr_fails = [
            f for f in result["findings"] if f["code"] == "addr-unresolvable"
        ]
        if len(addr_fails) != 4:
            problems.append(
                f"(a) 負向應有 4 條（檔案／鍵／label／副檔名），實得 {len(addr_fails)}"
            )
        # (b) 只該叫在該叫的列，不該誤傷 A1
        num_fails = {f["fact"] for f in result["findings"] if f["code"] == "number-unbound"}
        # C1：4.62 無出處；C2：803 只出現在散文字串裡，不得被當成候選值；
        # C3：999ms 的單位後綴被正規化隔開後才掃得到（正規化前這一列完全不會叫）
        if num_fails != {"C1", "C2", "C3"}:
            problems.append(f"(b) 負向應只命中 C1／C2／C3，實得 {sorted(num_fails)}")
        # L1-3：C5 的四個位址值是 {2,1,2,0}，聯集比對會全數放行，只有逐一對位才叫
        misplaced = [f for f in result["findings"] if f["code"] == "number-misplaced"]
        if {f["fact"] for f in misplaced} != {"C5"} or len(misplaced) != 2:
            problems.append(
                "(b) 逐一對位負向應在 C5 命中 2 條（第 1、2 段順序寫反），"
                f"實得 {[(f['fact'], f['detail'].get('number')) for f in misplaced]}"
            )
        # L1-2：C4 的「不到四倍」必須叫，且不得誤傷 A1 的「約佔 16.43%」
        fuzzy_fails = {f["fact"] for f in result["findings"] if f["code"] == "claim-fuzzy-quantity"}
        if fuzzy_fails != {"C4"}:
            problems.append(f"(b) 模糊量詞負向應只命中 C4，實得 {sorted(fuzzy_fails)}")
        # L4-2：4.62 沒登記例外要叫；7.77 登記了（雖然沒寫理由）就不該再叫 unbound
        doc_fails = [f for f in result["findings"] if f["code"] == "doc-number-unbound"]
        if [f["detail"]["number"] for f in doc_fails] != ["4.62"]:
            problems.append(
                "(d) 負向應只命中 spec 散文的 4.62，"
                f"實得 {[f['detail']['number'] for f in doc_fails]}"
            )
        stale = [f for f in result["findings"] if f["code"] == "doc-number-exempt-stale"]
        if len(stale) != 1:
            problems.append(f"(d) 過期例外應只有 999 那一列，實得 {len(stale)} 條")

    if problems:
        print("SELF-TEST FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("SELF-TEST PASS：四段檢查的正向與負向案例都會叫。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="追溯矩陣機械檢查器")
    parser.add_argument("change", nargs="?", help="change 目錄，例如 openspec/changes/add-foo")
    parser.add_argument("--json", action="store_true", help="輸出結構化 JSON")
    parser.add_argument("--self-test", action="store_true", help="用內建假資料驗證檢查器本身")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.change:
        parser.error("需要 change 目錄，或改用 --self-test")

    change = Path(args.change).resolve()
    if not change.is_dir():
        print(f"錯誤：{change} 不是目錄", file=sys.stderr)
        return 2
    try:
        result = run_lint(change)
    except MatrixError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        report(result)
    return 1 if result["stats"]["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
