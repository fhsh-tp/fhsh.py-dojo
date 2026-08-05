# 追溯矩陣（add-rank-code-challenge-duo）

> 單一真相來源：所有 proposal / design / spec 的 prose 主張皆由本表派生。
> 修訂規則：改任何一格，先改本表，再同步三份文件的對應位置；audit 各輪以本表 reconcile。
> Evidence 欄的「探針」= 2026-08-06 設計期探針（本 change 討論串實測，數據轉錄於 design.md Context）。

## A. 平台判題機制（兩題共用前提）

| ID | 事實主張 | Evidence | proposal | design | spec |
|----|----------|----------|----------|--------|------|
| F1 | 判題 op counter 上限 10M（全事件計數），C 內建（math.factorial、大數運算、str）完全隱形——factorial 整段查詢僅記 13 ops | `.vitepress/theme/workers/pyodide.worker.ts:108`；探針 `ops factorial-smartstrip-query(10k)=13` | Why §2 | Context 表 #1、D2 | R4 rationale |
| F2 | 單筆牆鐘軟旗標對同步碼結構性失效；唯一可靠牆鐘＝useExecutor 總預算硬殺（6s×筆數，20 筆＝120s） | `openspec/BACKLOG.md` §2.8；`useExecutor.ts` WALL_CLOCK_KILL_MS | Why §2 | Context 表 #2、D2/D6 | R5 rationale |
| F3 | Pyodide 0.29.3＝Python 3.13，`int_max_str_digits=4300`：大數 str() 直接 ValueError | `scripts/download-pyodide.sh:8`；探針 `str(10000!) ValueError` | What Changes | Context 表 #3、D6 | R5 scenario |
| F4 | 引擎 int 為 i64（N 開到 10⁹ 合法）；group `repeat` 引先宣告 int；literal 可自由指定小值域邊界 | `testcase-generator/src/parser.rs:55`；`Usage.md`〈group 群組〉 | Impact | D3 | R1/R2 |

## B. 568 版（rank-code-backfill，「別重複計算」）

| ID | 事實主張 | Evidence | proposal | design | spec |
|----|----------|----------|----------|--------|------|
| F5 | 正解（增量建表＋查表）@T=500、maxN=200000：1,309,367 ops，餘裕 7.6× | 探針 `568 正解 ops` | What Changes | Context 表 #4、D2/D3 | R4 |
| F6 | 天真解（逐查詢 O(N) 重算）前 20 筆查詢即 10,712,866 ops 破限；500 筆外推 ~268M | 探針 `568 天真解 ops` | What Changes | Context 表 #5、D2 | R4 |
| F7 | 繞道（逐查詢 math.factorial＋一次除尾零）T=500 全套 ~142s native；Pyodide ×2~4 ≥ 2× 總預算 → 必死於硬殺 | 探針 `568 繞道` | What Changes | Context 表 #6、D6 | R5 |
| F8 | 語義錨點：lnz(5!)=lnz(120)=2；lnz(1!)=1；增量表 vs 暴力 1..2000 全吻合 | 探針 `568 table vs brute ALL MATCH` | — | D1/D5 | R3 example |
| F9 | 參數範圍：T ∈ 1..500、N ∈ 1..200000；輸入 worst-case ≈ 3504 bytes < 預設 input_budget 4096（apply 期以引擎估算覆核） | 探針＋手算 500×7+4；`Usage.md` input_budget | Impact | D3 | R1 |

## C. 10212 版（prize-order-code，「只留必要資訊」）

| ID | 事實主張 | Evidence | proposal | design | spec |
|----|----------|----------|----------|--------|------|
| F10 | 正解（O(M) 區間模運算）@T=3、M=100000：1,665,028 ops，餘裕 6.0× | 探針 `10212 正解 ops` | What Changes | Context 表 #7、D2/D3 | R4 |
| F11 | 繞道（大數連乘不取模）單重案：連乘 8.5s＋逐位剝零 21.0s native（~90 萬位數）；str() 路線踩 F3 直接 ValueError | 探針 `10212 繞道` | What Changes | Context 表 #8、D6 | R5 |
| F12 | 天真解（1..N 全乘）在 band N ≥ 10⁸ 時 op 必破限（≥5.5×10⁸ ops） | F6 同款速率外推（5.5 ops/iter） | What Changes | D2 | R4 |
| F13 | 5 因子過剩陷阱：2/5 因子須分開追蹤；c5>c2 → 末位必為 5（P(25,1)=5、P(26,2)=5）；c2>c5 → r×2^(c2−c5) mod 10；相等 → r | 探針 `10212 lnz_perm vs brute ALL MATCH`＋6 組定向案例 | — | D5 | R3 example |
| F14 | M ≤ N 由值域構造保證：band N_min=100000＝M_max；小 N 邊界一律用 literal 補 | D3 設計；F4（literal 能力） | Impact | D3 | R2 |
| F15 | 語義錨點：P(10,2)=90→9；M=0（空乘積）→1；P(10⁹,1)→1 | 探針定向案例 | — | D1/D5 | R3 example |

## D. 素養包裝（兩題共用）

| ID | 事實主張 | Evidence | proposal | design | spec |
|----|----------|----------|----------|--------|------|
| F16 | 情境：遊戲排行榜同宇宙——568=每日榜單驗證碼回填 T 天；10212=全球賽季前 M 名頒獎順位驗證碼；題面不得出現資料結構術語；「檢查碼」（ISBN／身分證末碼）為素養引言 | 討論串拍板 2/N；檢查碼素材（中山大學 EAN-13、iT 邦身分證檢核碼） | Why §1 | D1 | R6 |
| F17 | 難度：rank-code-backfill=medium、prize-order-code=hard；皆 apcs／competition；單一 change 包雙題 | 討論串拍板 4/N、5/N | What Changes | D1 | R1/R2 |
