## Context

六題批次 change B。本 change 首度全面採用 change A RCA 的 I-1～I-8 改善：**設計期賞金已跑完**（19 agents，F1–F16 見 trace-matrix.md「賞金結果」節），文件撰寫時所有 must-fix 已修補並重驗。單一真相來源為 `trace-matrix.md`；本文件所有數值皆派生自矩陣列（以「trace <ID>」標註），修改數值需先改矩陣再依 I-7 grep 同步。

## Goals / Non-Goals

**Goals**
- apcs011「福利社老收銀機」（medium）：翻轉優先序（加減先於乘除）、全左結合、無括弧（trace A1）
- apcs012「折價券疊加試算」（hard）：翻轉優先序＋加減右結合＋乘除左結合＋括弧覆寫（trace B1）
- 語義鑑別型得分階梯：已建模錯誤路線聯集 011 ≤6（實測 4/20）、012 ≤9（實測 8/20＝無括弧結構性下限）（trace C13）

**Non-Goals**
- 不建 TLE 斷崖：重寫類天真解重活皆在 C 層，op counter 無從獵殺（trace C7/C8）
- 不獵殺語義完全正確的繞道——E1 對調 eval（trace A3）、R2 regex 括弧化（trace A11）、E3′ 冪次編碼（trace B4）、N1 list-rewrite 一律收編為聰明解；題面不寫任何不可能性承諾
- 不動 Rust 引擎；關聯輸入以全 literal 策展解決（trace C5）
- op 跳閘可被 try/except 重試屬平台級議題（trace C14），本 change 不處理（階梯不依賴 TLE，零影響）

## D1 判題機制與預算

單筆 op 上限 10,000,000（settrace 每事件 +1）、全部測資累計 120s 牆鐘（trace C1）。正解累計成本：011 全 20 筆 161,108 ops／0.036s、012 全 20 筆 308,093 ops／0.046s（trace A8/B9），Pyodide ≈1.7× 換算後餘裕仍達千倍級。註：op 計數器為單發跳閘（trace C14），已記錄待平台獨立 change，本雙題不受影響。

## D2 語義與值域

- **011**（trace A1）：token 化後先將運算式依 `*` `/` 切成加減段；每段由左至右折疊；段值再由左至右以 `*` `/` 折疊。範例（trace A2）：`10 - 4 - 3 + 2 * 6` → (10-4-3+2)=5 → 5*6=30。
- **012**（trace B1）：加減段改由**右**至左折疊（`a - b + c` = a-(b+c)）；乘除仍左折疊；括弧內為完整子運算式。同一式子答案為 66：10-(4-(3+2))=11 → 11*6（trace B2；grilling 紀錄的 5/30 為左結合值，已修正）。
- 值域（trace C3/C4）：運算元非負整數 <10000（實測 max 3791）；中間值 |值|<100000（實測峰值 44865）；除法必整除、除數恆為正（實測 min 1）；`0 / d = 0` 合法；單一數字行合法；T ≥ 1（trace C2）。
- generator＝段折疊迭代式；reference_solution＝獨立異構（shunting-yard→RPN）（trace B10）。012 允許教科書全遞迴解：最深 604 frames，已對出貨 Pyodide WASM 直測通過（trace B6）。

## D3 測資策展架構

全 40 筆 literal，由確定性腳本 `plan_b.py`（seeds 1101/1202）產生並斷言（trace C5）；`input_budget: 63488`，最大 entry 50,084 bytes（trace C6）。結構：011 見 trace A7；012 見 trace B8（1-8 無括弧、9 起有括弧，遵 Q6 分區）。literal 內容參與池 seed，任何改動全池重洗＋全量重測（trace C9）。鑑別行家族：`DTkill`（`A * B / C`、B 不整除 C）殺 divtight；`L2Rkill`（乘除先於加減出現）殺 L2R；`PKline`（括弧行內同層雙乘除＋括弧內翻轉語義內容）同時殺 divtight／uniform-mdr／雙路徑複合／parens-std 四路線（賞金 F1/F3/F6 修補）。

## D4 階梯哲學與收編清單

軸心＝語義鑑別（trace C8）。收編（=接受為聰明解，題面不提、不獵殺）：E1（011 20/20，279,208 ops，trace A3）、R2（011 20/20，trace A11）、E3′（012 20/20，fuzz 1200/1200，trace B4——`**` 是 Python 唯一高優先右結合運算子，右結合性隨選擇免費取得，屬已知教學殘餘，依守則⑤不以測資獵殺）、N1（C 層重寫）。完整判分預測見矩陣 V 表（V1–V12），apply 期全數 ship-e2e 重測（I-5）。

## D5 鑑別職責與斷言牆

plan_b.py `finalize()` 對每個錯誤路線類掛 predictor＋上界 assert（I-6：AC 引用上界，精確值為 measured 紀錄）：

| 路線 | 011 上界（實測） | 012 上界（實測） | trace |
|------|----------------|----------------|-------|
| E2 標準優先序 | ≤3（2） | ≤3（1） | A4/B5 |
| 加減結合序誤解 | ≤4（1） | ≤4（1） | A5/B3 |
| 乘除右結合 bug | ≤4（3） | ≤4（3） | A6/B7 |
| divtight | ≤4（4） | ≤4（3） | A10/B11 |
| L2R | ≤3（2） | — | A9 |
| parens-std | — | ≤8（8） | B12 |
| 雙路徑複合 | — | ≤8（8） | B13 |
| **聯集** | ≤6（4） | ≤9（8） | C13 |

答案分布：011=39 相異、012=42 相異、皆含正負（trace C10）。大型筆答案的 smooth-number 弱指紋為接受殘餘（賞金 F14：黑箱前提下僅助驗證不助生成）。

## D6 題面撰寫約束

- 禁資料結構術語（stack／堆疊／樹／LIFO）；兩題獨立情境（trace C11）：011=福利社老收銀機韌體怪癖；012=折價券由最後一張往前疊加、組合包＝括弧。
- 012 規則表述（trace B14，賞金 F11）：「往回套用」語感有分岔讀法，必須以「每張券作用於**其右側整段已計算的結果**」表述，並附 `10 - 4 - 3 + 2 * 6` 逐步拆解表；禁止只寫「從最後一張往前算」。
- 011 範例組（trace A2）含負中間值示範 `1 - 7 / 2 = -3`（賞金 F12）；012 括弧覆寫於規則節另附 worked example（entry 1 依 Q6 分區無括弧）。
- 深巢組合包以「歷史促銷資料的極端案例」語氣帶過，不需情境合理化 25 層（賞金 F13）。
- 值域、整除保證、除數為正、單一數字行合法、輸出可為負——逐條寫入題面（trace C2/C3/C4）。

## I-2 三軸攻擊面叉積表（設計期賞金掃描結果）

| X 成本規避 ＼ Y 語義弱化 | 完整語義 | 部分語義（結合序／優先序錯） | Z 分布投機 |
|---|---|---|---|
| eval＋運算子對調 | E1：011 收編 20/20；012 死於左結合 1/20 | swapleft 1/20 | — |
| eval＋`**` 編碼 | E3′：012 收編 20/20 | naive 檔 8/20（regex 破口） | — |
| eval＋regex 括弧化 | R2：011 收編 20/20 | — | — |
| eval 直呼（std） | — | E2：2/20、1/20 | gimme 憑證僅 entries 2-3 |
| 手寫 parser | 正解 20/20 | mdr 3/20；divtight ≤4；L2R 2/20；parens-std 8/20 | 雙路徑分支（`'(' in line`）8/20——PKline 封殺 |
| C 層重寫迴圈 | N1：收編（正確但 O(n²) C 層） | — | — |
| 形狀／答案指紋 | — | — | smooth 指紋＝接受殘餘（F14）；T/長度分類器無利可圖（各 band 內語義職責齊備） |

## I-3 設計期三張表

**表① 考點×entry 鑑別力矩陣**（每考點 ≥2 筆、≥1 筆在長度上四分位）：

| 考點 | 鑑別 entries（011） | 鑑別 entries（012） | 上四分位覆蓋 |
|------|--------------------|--------------------|--------------|
| 翻轉優先序 | 1,4,6,7,8-20 | 1,4,6,7-20 | 17-20 ✓ |
| 加減結合序 | 4-7,8-20（右變體僅得 entry 2） | 1,3,4,5,6,7-20（左變體僅得 entry 2） | 17-20 ✓ |
| 乘除左結合 | 4,5,6,7＋seeded/big | 4,5,6,9-20（PKline/DTkill） | 17-20 ✓ |
| 整除／負中間值 | 1,5,7＋seeded/big | 5＋seeded/big | ✓ |
| 括弧覆寫 | —（無括弧） | 9-20 | 17-20 ✓ |

**表② 反例義務表**（每條弱判定路線指名池中反例；空格＝缺陷）：所有路線之反例 entry 清單見矩陣 A4-A10／B3-B13 各列「實測」欄括號內容——每列非空 ✓；報表 `report_b.json` 逐 entry 記錄各路線 `*_ok` 布林可機械稽核。

**表③ 簽章去識別化檢核**：literal 家族參數（seeds、seg_len、final_mult）不出現在題面；答案非可見參數之封閉式（fold 值經 `small_divisor` 隨機游走）；殘餘弱指紋僅 F14（接受）。

## Implementation Contract

1. **Scaffold**：`pnpm new-challenge snack-bar-register --title "福利社老收銀機" --difficulty medium --category apcs --type competition` 與 `pnpm new-challenge coupon-combo-quote --title "折價券疊加試算" --difficulty hard --category apcs --type competition`；scaffold 自動配號應得 apcs011／apcs012（本分支現況 max=apcs010），若配號不符即停。
2. **Frontmatter**：`algorithm` 取 scaffold 預設底線版；`input_budget: 63488`；`testcase_plan` 為 20 個 literal 區塊，內容 byte-for-byte 等於 `design_b/literals/{a,b}_NN.txt`（由組裝腳本寫入，不手貼）；`params` 保留 scaffold 合法宣告（literal-only plan 下僅佔位，型別須通過 challenge-params 冒煙）。
3. **generator**：實作 D2 語義（迭代式段折疊），內建整除 assert；**reference_solution**：shunting-yard→RPN 異構實作（012 支援括弧、右結合加減）。兩者在全 40 筆 literal 上輸出一致（apply 期以腳本先行驗證再進瀏覽器）。
4. **題面**：依 D6 全部約束撰寫；範例區塊＝entry 1 內容原樣。
5. **驗證閘（I-5）**：`pnpm build:pools` 後，dev e2e 依 V 表 12 路線逐筆重測（agent-browser SOP），矩陣 ship-e2e 欄位補齊；任何 literal／generator 改動先標 STALE 再重測。scoreboard 斷言：`pnpm typecheck`、`pnpm lint`、params 冒煙、content-regression（兩題 reference_solution）全綠。
6. **修復紀律**：改數值先 `grep -n` 舊值全域列舉、改後歸零（I-7）；audit 輪的 side_effect_risk 機械抽成同步 checklist（I-8）；修復若新增／改動 literal 家族，當輪對新造物件重跑 I-3 表（I-4）。
