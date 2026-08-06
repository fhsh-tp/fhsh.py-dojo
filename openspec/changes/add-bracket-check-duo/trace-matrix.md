# 追溯矩陣 — add-bracket-check-duo（單一真相來源）

> 規則：每個規範性事實一個 ID。prose（proposal／specs／design／題面）一律從本矩陣派生；
> 修訂任何事實先改矩陣、再同步所有列出的文件位置。evidence 欄為量測或規格出處。
> 文件位置縮寫：P=proposal.md、S=specs/bracket-check-challenges/spec.md、D=design.md、
> Ma=docs/challenge/prop-box-packing.md、Mb=docs/challenge/magazine-typeset-check.md。

## 共通事實（C）

| ID | 事實 | Evidence | 文件位置 |
|----|------|----------|----------|
| C1 | 兩題：1a `prop-box-packing`「道具箱裝箱檢查」、1b `magazine-typeset-check`「校刊排版檢查器」；id 由 scaffold 配號（預期 apcs009／apcs010，以 scaffold 實配為準） | grilling Q3/Q9（memory project-stack-tree-batch） | P Capabilities；S 開頭；D Context；Ma/Mb frontmatter |
| C2 | 兩題皆 `category: apcs`、`type: competition`、`difficulty: medium` | grilling Q2 | P Impact；Ma/Mb frontmatter |
| C3 | 每場 20 筆測資，採 `testcase_plan`；判題順序＝plan 條目宣告順序 | Usage.md〈testcase_plan〉L293–360 | S R2/R5；D 測資設計；Ma/Mb frontmatter |
| C4 | `input_budget: 63488`；硬上限 65536 不可覆寫 | Usage.md L364–371 | D 測資設計；Ma/Mb frontmatter |
| C5 | 括號種類分區：第 1–3 筆僅 `()`；第 4–12 筆 `()[]`；第 13–20 筆 `()[]{}` | grilling Q4 | S R2/R5 banding；D 測資設計；Ma/Mb testcase_plan |
| C6 | 第 1 筆為 literal 且與題面範例完全一致 | house 慣例（scheduling 題 SOP，memory project-scheduling-challenges） | S R2/R5；Ma/Mb 範例節＋testcase_plan 首條 |
| C7 | 輸入格式：第一行 T（1 ≤ T ≤ 5），接著 T 行、每行一個紀錄字串；字串長度 1..62000 | 本設計定義；預算驗算見 C4 | S R1/R4；Ma/Mb 輸入說明 |
| C8 | 引擎 band 用 `t` 固定 1＋`s` enum（值＝允許字元清單、count＝長度範圍、separator ""）；band override 只補丁 `values`／`count` 值域；literal 筆可用 T>1 | Usage.md 型別一覽＋override 合併規則；parser.rs 多字元 enum values 測試 L1138 | D params 設計；Ma/Mb params＋testcase_plan |
| C9 | generator 與 reference_solution 語義一致但寫法獨立（stack 掃描 vs 不同資料佈局），由 content-regression 驗證 | challenge-author skill §3 | D 驗證；Ma/Mb generator/reference_solution |

## 1a 道具箱裝箱檢查（A）

| ID | 事實 | Evidence | 文件位置 |
|----|------|----------|----------|
| A1 | 合法性語義：由左至右掃描，右括號必須與「最近尚未配對的左括號」同種配對；掃描完無殘留＝合法 | UVa 673 語義；探針 sanity（`([)]`→NG） | S R1；Ma 演算法說明 |
| A2 | 每行輸出恰為 `OK`（合法）或 `NG`（不合法），共 T 行 | 本設計定義 | S R1；Ma 輸出說明 |
| A3 | 計數器假解（逐種計數＋執行中不可為負）僅在「各種類數量平衡、執行中不為負、但順序交錯」時出錯——隨機 NG soup 上會巧合正確。因此交錯陷阱 literal 布 5 筆（第 4/9/12/15/18 筆，各含一個騙倒計數器的 case：`([)]`／`[(])`／`(([))]`／`{[}]`／`([{)]}` 家族）；預測計數器精確 15/20、第 4 筆首 WA | 探針 sanity＋離線自檢腳本逐 case 斷言 counter_fake≠truth；e2e V1 後修正（原「3/20」預測為誤，2026-08-06 修訂） | S R2 Scenario；D 假解分析；Ma testcase_plan |
| A4 | C 繞道（replace 迴圈、find+切片刪除）**收編為 accepted alternative**：31k 深巢下 replace 93,017 ops／5.5s native、delfind 434,026 ops／3.6s native——op counter 抓不到（<0.5M ops），牆鐘獵殺需 ≥10 筆 62KB 獵殺筆（不可行）。題面**不得**寫不可能性承諾 | 探針 P2/P3（probe_harness，settrace 同款 tracer）；rank-code-duo RCA D6.b 判例 | D 繞道分析；S R3；Ma 無（題面沉默） |
| A5 | 正解（stack 掃描）worst-case：62KB 深巢 217,022 ops／0.016s native，≤ 門檻 2.5M（上限 10M÷4） | 探針 P1 | D 效能驗算；S R3 |
| A6 | 第 20 筆 stress literal：62KB 混種深巢（深度 31000，`([{` 循環）；replace 路線單筆 ~5.5s native、正解毫秒級 | 探針 P1/P2（同構） | S R2；D 測資設計；Ma testcase_plan |
| A7 | 1a 條目佈局（20 筆）：L1 範例(1)；band `()` 2..500(2–3)；L 陷阱(4)；band `()[]` 2..2000(5–7)；L OK 保底(8)；L 陷阱(9)；band `()[]` 1000..5000(10–11)；L 陷阱(12)；L 3 種 OK 保底(13)；band 3 種 1000..40000(14)；L 陷阱(15)；band 3 種 10000..40000(16–17)；L 陷阱(18)；band 3 種 20000..40000(19)；L stress(20) | 預算驗算 40000<63488 ✓；位置驗算於策展腳本斷言 | D 測資設計；Ma testcase_plan |
| A8 | 隨機 soup band 幾乎必 NG；每個分區至少 1 筆 OK 判定的 literal 保證兩類判定都出現 | 隨機走訪回零機率極低（設計論證） | D 測資設計；Ma testcase_plan |

## 1b 校刊排版檢查器（B）

| ID | 事實 | Evidence | 文件位置 |
|----|------|----------|----------|
| B1 | 首錯位置語義三分支：(i) 掃描遇「右括號且無待配對左括號或種類不符」→輸出該右括號位置；(ii) 掃畢有殘留左括號→輸出**最早**一個未配對左括號位置（殘留堆疊最底）；(iii) 全配對→輸出 0 | 本設計定義；探針 sanity（`x([y)z]`→5、`((a`→1、無括號→0） | S R4；Mb 演算法／輸出說明 |
| B2 | 位置以**原字串** 1-based 計，雜訊字元一併計位 | 本設計定義 | S R4；Mb 輸出說明 |
| B3 | 字串混入雜訊字元；雜訊集＝小寫字母＋數字＋`.,;`（**不含空白**——學生慣用 `input().strip()`，前導/尾隨空白會造成非預期位置偏移陷阱）；雜訊掃描時跳過、但一併計位 | grilling Q4 補充；strip 誤傷分析（apply 期發現） | S R4；Mb 輸入說明；D params |
| B4 | 獵殺筆 ×6（第 14、15、16、18、19、20 筆）：形狀 `(`×1000＋`()`×5000＋`)`×1000（12,000 字元）；回頭掃描天真解每筆 ≥20M 精簡 ops（2 ops/iter 下限估算）→ 逐筆 op 爆殺；預測天真解 14/20 | 探針 P5＋尺寸掃描（m=400..800 全部 10M 爆殺、正解 ≤51k ops）；m=1000,k=5000 下限驗算 1000×10000×2=20M | S R5；D 測資設計；Mb testcase_plan |
| B5 | 正解 worst-case：50KB 獵殺形 200,823 ops／40KB 混雜訊 151,649 ops，≤ 2.5M | 探針 P4 | D 效能驗算；S R6 |
| B6 | replace／刪除類路線**結構性不可用**（消字元後位置資訊消失）——設計層論證，題面不宣稱 | Q3 拍板論證 | D 繞道分析 |
| B7 | 無任何括號的字串→輸出 0（邊界 literal 釘死） | B1(iii) 特例 | S R4 Scenario；Mb testcase_plan |
| B8 | 獵殺筆為合法字串（答案 0），逼天真解掃到爆；正解毫秒 | 探針 P4/P5 | D 測資設計 |

## 判題預測矩陣（V）— dev e2e 驗證標的

| ID | 路線 | 預測 | Evidence |
|----|------|------|----------|
| V1 | 1a reference | 20/20 AC | A5 |
| V2 | 1a 計數器假解 | 15/20（恰第 4,9,12,15,18 筆 WA） | A3 |
| V3 | 1a replace 繞道 | 20/20 AC（牆鐘 ~10–25s，收編） | A4/A6 |
| V4 | 1b reference | 20/20 AC | B5 |
| V5 | 1b 回頭掃描天真解 | 14/20（恰第 14,15,16,18,19,20 筆 op 爆殺） | B4 |
