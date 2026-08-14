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
| C10 | starter_code 讀入後不輸出任何行（原地提交＝0/20 基線）；「刻意常數輸出」的殘餘得分（1a 全 NG≈11/20、1b 全 0≈3~5/20）為 accepted residual——判題逐筆亮 WA、無法通關，與其他二值輸出題同性質 | R1 修訂（原 starter 印 NG/0 白拿 11/20、7/20）；R1 findings 5/8/13/14 | D D5；Ma/Mb starter_code |

## 1a 道具箱裝箱檢查（A）

| ID | 事實 | Evidence | 文件位置 |
|----|------|----------|----------|
| A1 | 合法性語義：由左至右掃描，右括號必須與「最近尚未配對的左括號」同種配對；掃描完無殘留＝合法 | UVa 673 語義；探針 sanity（`([)]`→NG） | S R1；Ma 演算法說明 |
| A2 | 每行輸出恰為 `OK`（合法）或 `NG`（不合法），共 T 行 | 本設計定義 | S R1；Ma 輸出說明 |
| A3 | 計數器假解（逐種計數＋執行中不可為負）僅在「各種類數量平衡、執行中不為負、但順序交錯」時出錯——隨機 NG soup 上會巧合正確。因此交錯陷阱 literal 布 **7 筆**：短陷阱 5 筆（第 4/9/12/15/18 筆）＋**長陷阱 2 筆**（第 17/19 筆，28K/35K 隨機平衡串中段注入，counts 平衡且執行不為負——R2 修訂，封殺「長行只比數量」混合投機）。陷阱含兩型（R3 修訂）：**相鄰型**（`([)]`／`[(])`／`(([))]`／`{[}]`／`([{)]}`——違規閉符號緊鄰異種開符號）與**非相鄰型**（`([())]`／`{[{}}]`——違規閉符號前一字元是閉符號，壞二元組偵測落空；布於第 9/15 筆各一 case 與長陷阱 17/19 的注入），封殺「計數＋壞二元組」C 級投機（V9）；預測計數器精確 13/20、第 4 筆首 WA | 探針 sanity＋離線自檢腳本逐 case 斷言 counter_fake≠truth；e2e V1 後修正（原「3/20」預測為誤，2026-08-06 修訂） | P What Changes；S R2 Scenario；D 假解分析；Ma testcase_plan |
| A4 | C 繞道（replace 迴圈、find+切片刪除）**收編為 accepted alternative**：對**出貨第 20 筆**（混種深度 31000）replace 62,018 ops／2.1s native、delfind 310,030 ops／1.4s native——op counter 抓不到（<0.5M ops）；牆鐘獵殺不可行（即使 20 筆全為 stress，Pyodide 實測 3.5s/筆 ×20 ≈ 70s < 120s 總預算）。單種 `()` 同深度為此路線較劣形狀（replace 93,017／5.5s），僅作保守上界參考。題面**不得**寫不可能性承諾 | R2 修訂：原數字量自單種探針形、與出貨混種形不同構——改以出貨 literal 直接量測；rank-code-duo RCA D6.b 判例 | D 繞道分析；S R3；Ma 無（題面沉默） |
| A5 | 正解（stack 掃描）worst-case：62KB 深巢 217,022 ops／0.016s native，≤ 門檻 2.5M（上限 10M÷4） | 探針 P1 | D 效能驗算；S R3 |
| A6 | 第 20 筆 stress literal：62KB 混種深巢（深度 31000，`([{` 循環）；replace 路線單筆 ~2.1s native／3.5s Pyodide、正解毫秒級 | 對出貨 literal 直接量測（R2 修訂；P1 ref 217,022 ops 對形狀不敏感、單種混種同值） | S R2；D 測資設計；Ma testcase_plan |
| A7 | 1a 條目佈局（20 筆）：L1 範例(1)；band `()` 2..500(2–3)；L 陷阱(4)；band `()[]` 2..2000(5–7)；L OK 保底(8)；L 陷阱(9)；band `()[]` 1000..5000(10–11)；L 陷阱(12)；L 3 種 OK 保底(13)；band 3 種 1000..40000(14)；L 陷阱(15)；band 3 種 10000..40000(16)；L 長陷阱 28K(17)；L 陷阱(18)；L 長陷阱 35K(19)；L stress(20) | 預算驗算 40000<63488 ✓；位置驗算於策展腳本斷言 | D 測資設計；Ma testcase_plan |
| A8 | 隨機 soup band 幾乎必 NG；每個分區至少 1 筆 OK 判定的 literal 保證兩類判定都出現 | 隨機走訪回零機率極低（設計論證） | D 測資設計；Ma testcase_plan |
| A9 | 錯誤路線得分階梯（皆無法 20/20）：計數器 13/20（七陷阱）；「短行驗順序＋長行只比數量」混合投機 18/20 封頂（死於長陷阱 17/19，R2 bounty 曾 20/20）；「計數＋壞二元組」C 級投機 16/20 封頂（死於非相鄰型陷阱 9/15/17/19，R3 bounty 曾 20/20）；正確 stack 掃描是唯一 20/20 正路（replace/C-rfind/塗白 收編除外） | R2/R3 bounty 實測＋修復後 V7/V9 e2e 驗證 | D 假解分析；S R2 |

## 1b 校刊排版檢查器（B）

| ID | 事實 | Evidence | 文件位置 |
|----|------|----------|----------|
| B1 | 首錯位置語義三分支：(i) 掃描遇「右括號且無待配對左括號或種類不符」→輸出該右括號位置；(ii) 掃畢有殘留左括號→輸出**最早**一個未配對左括號位置（殘留堆疊最底）；(iii) 全配對→輸出 0 | 本設計定義；探針 sanity（`x([y)z]`→5、`((a`→1、無括號→0） | S R4；Mb 演算法／輸出說明 |
| B2 | 位置以**原字串** 1-based 計，雜訊字元一併計位 | 本設計定義 | S R4；Mb 輸出說明 |
| B3 | 字串混入雜訊字元；雜訊集＝小寫字母＋數字＋`.,;`（**不含空白**——學生慣用 `input().strip()`，前導/尾隨空白會造成非預期位置偏移陷阱）；雜訊掃描時跳過、但一併計位 | grilling Q4 補充；strip 誤傷分析（apply 期發現） | S R4；Mb 輸入說明；D params |
| B4 | 獵殺筆 ×6（第 14/15/16/18/19/20 筆）互不相同：形狀家族 `前綴成對×p ＋ 開×m ＋ 成對×k ＋ 閉×(m 或 m−1)`，R2 重構為**不規則混種帶雜訊**家族（無可辨識形狀捷徑）：seeded 亂數 warmup（雜訊＋完整成對）→ 殘留筆將未配對左標記 U 埋於 warmup 後（答案＝U 位置，非公式可猜）→ m 個混種外層開（偶帶雜訊）→ k 個混種內層成對（偶帶雜訊）→ 反序閉合；參數 (seed,m,k,殘留→答案)＝K14(1414,2000,5000,有→29)、K15(1515,2000,6250,有→27)、K16(1616,2000,5000,無→0)、K18(1818,2500,4000,有→18)、K19(1919,1600,6250,無→0)、K20(2020,2000,5000,有→23)；長度 13,383~16,936；每筆 lean 下限 m×2k ≥ 20M（1 op/iter 精簡變體實測最小 K19=23,190,670 ops 仍爆殺）；預測天真解 14/20 | R2 修訂：原單種零雜訊形可被「形狀偵測跳過掃描」投機解 20/20（bounty 實測）→ 重構；六筆對最精簡變體逐筆 10M 爆殺實測；正解最大筆 K15=100,789 ops | P What Changes；S R5；D 測資設計；Mb testcase_plan |
| B5 | 正解（reference_solution）worst-case：新六筆獵殺最大 K15=100,789 ops（generator 為 67,337——兩者皆 ≤ 2.5M；早期探針形 200,823／151,649 ops 亦低於門檻） | R2 重測並修正歸屬（原 66,043 誤量自 generator） | D 效能驗算；S R6 |
| B6 | 刪除類路線：**單純刪除字元**的變體遺失位置資訊不可用；**等長塗白**變體（把已配對的相鄰對換成等長填充字元、C 級 replace 迴圈收斂後掃殘餘）可用——R3 bounty 實測 20/20、獵殺筆 ~51K ops／0.17s native，op 稀疏不可獵殺，依 A4/B9 判例**收編為 accepted alternative**；題面不宣稱任何路線不可能 | R3 bounty 實測（原「結構性不可用」全稱論證被反例推翻）；R2 教訓同 A4：全稱句須逐變體檢驗 | D 繞道分析；S R6 |
| B7 | 無任何括號的字串→輸出 0（邊界 literal 釘死） | B1(iii) 特例 | S R4 Scenario；Mb testcase_plan |
| B8 | 獵殺筆逼天真解全行掃描（無錯配可提早 break）：無殘留筆（第 16/19 筆）答案 0、殘留筆（第 14/15/18/20 筆）走 B1(ii) 分支（答案 29/27/18/23）——兩型皆須掃完全行；正解毫秒 | R2 重構後量測（generator/reference 逐筆一致） | D 測資設計 |
| B9 | C 層回頭掃描（str.rfind 系）收編為 accepted alternative：op 稀疏、op counter 抓不到，與 1a replace 同機制不可獵殺（R1 賞金獵人實測 AC） | R1 bounty-bypass 實測 | D 繞道分析 |
| B10 | 1b 題面提醒句限定為窄而實測為真的敘述：「每遇到一個右標記，就用迴圈逐字元往回重新掃描」的寫法經實測超出運算次數限制——不含對 C 層路線的不可能性承諾 | R1 修訂（原句為可證偽的不可能性承諾，C-rfind 反例）；rank-code-duo 題面警語守則 | D D6；Mb 提醒句 |

## 判題預測矩陣（V）— dev e2e 驗證標的

| ID | 路線 | 預測 | Evidence |
|----|------|------|----------|
| V1 | 1a reference | 20/20 AC | A5 |
| V2 | 1a 計數器假解 | 13/20（恰第 4,9,12,15,17,18,19 筆 WA） | A3 |
| V3 | 1a replace 繞道 | 20/20 AC（牆鐘 ~10–25s，收編） | A4/A6 |
| V4 | 1b reference | 20/20 AC | B5 |
| V5 | 1b 回頭掃描天真解 | 14/20（恰第 14,15,16,18,19,20 筆 op 爆殺） | B4 |
| V6 | 1b 最精簡回頭掃描（單行 while，1 op/iter） | 14/20（同六筆爆殺） | B4；R1 新增 |
| V7 | 1a 混合投機（短行 stack、長行只比數量，門檻 1000） | 18/20（恰第 17,19 筆 WA） | A9；R2 新增 |
| V8 | 1b 長行跳過投機（len>5000 直接輸出 0、短行 stack） | ≤16/20（第 14,15,18,20 筆必 WA；第 17 筆 soup 高機率 WA） | B4 殘留答案設計；R2 新增 |
| V9 | 1a 計數＋壞二元組 C 級投機 | 16/20（恰第 9,15,17,19 筆 WA） | A3 非相鄰型陷阱；R3 新增 |
