#!/usr/bin/env python3
"""追溯矩陣機械檢查器（跨 change 重用）。

用法::

    python3 scripts/trace-lint.py openspec/changes/<name>
    python3 scripts/trace-lint.py openspec/changes/<name> --json
    python3 scripts/trace-lint.py --self-test

本檔把 ``<change>/trace-matrix.md`` 當成**可機械解析的單一真相來源**，做三段檢查。
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

三段檢查
========

(a) 位址可解析（``addr-*``）
    證據欄每個位址的檔案必須存在、鍵路徑必須解析得出值。失敗時指名列、位址、
    以及卡在鍵路徑的哪一段。

(b) 數字綁鍵（``number-unbound``）
    若某列證據欄**有位址**，該列**主張欄**出現的每個數字都必須等於該列某個位址
    解析出的值。證據欄全散文的列不做此檢查（那是刻意留的逃生口：不宣稱有機械
    出處，就不受機械檢查）。

(c) 位置欄雙向（``pos-*``）
    正向：``✓`` 的目標文件必須含標記；``—`` 的不得含；``△`` 必須帶括號理由。
    反向：目標文件出現的每個標記，矩陣必須有對應 fact id 且該欄為 ``✓``。

數字正規化規則（(b) 段）
========================

**掃描前先從主張欄剔除**：

1. 所有 code span（`` `...` ``）——那是識別字與公式（``apcs015``、``k²(k²−1)/2``、
   ``2^(n−k) mod 1000000007``），不是被主張的量測值。
2. ISO 日期 ``YYYY-MM-DD``——那是時間戳不是量測值。

**數字 token 的認定**：

- 前面不得緊接 ``[A-Za-z0-9_.,]``，後面不得（跨過數字與逗號後）緊接 ``[A-Za-z_]``。
  這使 ``E8`` 的 ``8``、``apcs015`` 的 ``015`` 不被當成數字。
- 千分位逗號視為格式：``1,008,010`` → ``1008010``。
- 單位與後綴（``%``、``倍``、``×``、``ms``、``bytes``、``op``）一律**不參與換算**，
  只比對裸數值。故 json 存 ``16.43`` 時，散文寫 ``16.43%`` 算相符；
  散文寫 ``0.1643`` 不算。
- 上標數字（``10⁹``、``2²⁹``）非 ASCII，**不掃描**（無法可靠正規化，刻意放行）。

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


def claim_numbers(claim: str) -> list[str]:
    """抓主張欄裡「被主張的量測值」（規則見模組 docstring）。"""
    text = CODE_SPAN_RE.sub(" ", claim)
    text = ISO_DATE_RE.sub(" ", text)
    return [m.group(1) for m in NUM_RE.finditer(text)]


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


# --- 主流程 ------------------------------------------------------------------


def run_lint(change: Path) -> dict[str, Any]:
    """跑完三段檢查，回傳結構化結果。"""
    matrix_path = change / "trace-matrix.md"
    if not matrix_path.exists():
        raise MatrixError(f"找不到 {matrix_path}")
    rows = parse_matrix(matrix_path)

    findings: list[Finding] = []
    n_addresses = 0
    n_markers = 0

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
        for token in claim_numbers(row.get("claim", "")):
            if number_matches(token, candidates):
                findings.append(
                    Finding("b-number", "number-bound", True, fact, f"數字 {token} 已綁鍵")
                )
            else:
                detail = {addr: summarize(val) for addr, val in resolved.items()}
                lines = "；".join(f"`{a}` = {v}" for a, v in detail.items()) or "（無可解析位址）"
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

    fails = [f for f in findings if not f.ok]
    return {
        "change": str(change),
        "stats": {
            "rows": len(rows),
            "addresses": n_addresses,
            "markers": n_markers,
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
        f"文件標記：{stats['markers']}　檢查項：{stats['checks']}　FAIL：{stats['failures']}"
    )


# --- 自我測試 ----------------------------------------------------------------

SELF_TEST_JSON = {
    "margin": 3.98,
    "score_text": "13/20",           # 整格即比值的字串 → 算候選值
    "note": "上一輪曾量到 803 ms",   # 含散文的字串 → 不算候選值
    "wall": {"plain": 16.43},
    "routes": [{"max_ops": 3010}],
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
| A1 | 餘裕為 3.98 倍，最貴寫法佔 16.43% | `measure/m.json#margin`、`measure/m.json#wall.plain` | 散文 | ✓ | — |
| A2 | REFERENCE 最大 op 3,010 | `measure/m.json#routes[0].max_ops` | 範例 | — | ✓ |
| A3 | cellscan 瀏覽器得 8/20 | `measure/b.jsonl#label=cellscan.score`、`measure/b.jsonl#label=cellscan.rows` | 效能提醒 | ✓ | — |
| A4 | 訪談決策，無量測；下界推導為 `score(甲) + score(乙) ≡ 20 + #(平手)` | 2026-08-15 訪談 Q1，見 `curation/plan.py` | 全篇 | △（無外部真值，僅檢查有無被引用） | — |
| A5 | 明寫迴圈 1,008,010 op | `measure/m.json#ops["r015_rowscan.py"]` | — | — | — |
| A7 | 投影得分 13/20 | `measure/m.json#score_text` | — | — | — |
| A6 | n=10⁹ 時 REFERENCE 仍為 3,010 op（含上標的整串不掃描，底數也不切出來） | `measure/m.json#routes[0].max_ops` | — | — | — |
"""

GOOD_SPEC = "規範層 (trace A1) 與 (trace A3) 都在這裡。\n"
# 同時驗證複數形標記與 `(fact X, 註記)` 這種自由註記不會製造假 orphan
GOOD_DESIGN = "設計層只引 (facts A2, proven)。\n"

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
"""

BAD_SPEC = "這裡有 (trace A1)、(trace D2)、以及矩陣沒有的 (trace ZZ9)。\n"
BAD_DESIGN = "設計層空白。\n"


def self_test() -> int:
    """用內建假矩陣驗證三段檢查各有正向與負向案例都會叫。"""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        good = _write_fixture(Path(tmp) / "good", GOOD_MATRIX, GOOD_SPEC, GOOD_DESIGN)
        result = run_lint(good)
        fails = [f for f in result["findings"] if f["status"] == "FAIL"]
        if fails:
            problems.append("正向案例應零 FAIL，實得：" + "; ".join(f["message"] for f in fails))
        # 正向也要證明「有真的檢查到東西」，不是空轉
        passed = {f["code"] for f in result["findings"] if f["status"] == "PASS"}
        for code in ("addr-ok", "number-bound", "pos-marker-present", "pos-absent-ok", "pos-skip-ok"):
            if code not in passed:
                problems.append(f"正向案例缺少 PASS 類別 {code}（檢查器可能空轉）")
        if result["stats"]["addresses"] != 8:
            problems.append(f"正向案例位址計數應為 8，實得 {result['stats']['addresses']}")
        # 上標規則：`10⁹` 整串不得被拆成裸數字 10（A6 列的迴歸測）
        if claim_numbers("n=10⁹ 與 2²⁹ 與 3,010") != ["3,010"]:
            problems.append(
                "上標規則失效：`10⁹`／`2²⁹` 的底數被當成數字掃描，"
                f"實得 {claim_numbers('n=10⁹ 與 2²⁹ 與 3,010')}"
            )

        bad = _write_fixture(Path(tmp) / "bad", BAD_MATRIX, BAD_SPEC, BAD_DESIGN)
        result = run_lint(bad)
        codes = {f["code"] for f in result["findings"] if f["status"] == "FAIL"}
        expected = {
            "row-duplicate-id",  # 矩陣結構負向
            "addr-unresolvable",  # (a) 負向：檔案／鍵／label／副檔名 四種
            "number-unbound",  # (b) 負向
            "pos-marker-missing",  # (c) 負向：✓ 卻沒標記
            "pos-marker-forbidden",  # (c) 負向：— 卻有標記
            "pos-skip-no-reason",  # (c) 負向：△ 沒理由
            "pos-bad-value",  # (c) 負向：值非法
            "pos-orphan-marker",  # (c) 反向：文件有標記、矩陣沒有
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
        # (b) 只該叫在 C1 那一列（4.62 無出處），不該誤傷 A1
        num_fails = {f["fact"] for f in result["findings"] if f["code"] == "number-unbound"}
        # C1：4.62 無出處；C2：803 只出現在散文字串裡，不得被當成候選值
        if num_fails != {"C1", "C2"}:
            problems.append(f"(b) 負向應只命中 C1 與 C2，實得 {sorted(num_fails)}")

    if problems:
        print("SELF-TEST FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("SELF-TEST PASS：三段檢查的正向與負向案例都會叫。")
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
