# 追溯矩陣 — add-expression-eval-duo（apcs011／apcs012）

> 單一真相來源。proposal／design／spec 的 prose 一律由本矩陣派生；任何數值修改先改此處，
> 再依 I-7（grep 舊值歸零）同步三份文件。`measured` 狀態：`design-probe`＝設計期探針
> （CPython + probe_harness）；`ship-e2e`＝出貨後瀏覽器實測（apply 期補）。
> 量測四元組：harness=probe_harness.py（settrace 複刻）× 程式身分=design_b/{sol,bounty}/*.py
> × 輸入=design_b/literals/ × 版本=plan_b.py seeds (1101, 1202)（design-bounty 修補後版）。
> 設計期賞金（wf_b2660959-6d7，19 agents）已跑完：F1–F6 已修補並重驗，詳見「賞金結果」節。

## C — 共通事實

| ID | 事實 | 值／狀態 | evidence 出處 | proposal | design | spec |
|----|------|---------|--------------|----------|--------|------|
| C1 | 判題 op 上限／總時間預算 | `10_000_000` ops/test；120s 累計 | worker-utils.ts（change A 已錨定） | Why | D1 | — |
| C2 | 輸入格式：首行 T（`T ≥ 1`）、續 T 行運算式；token 間單一空白；輸出 T 行整數；單一數字行合法 | 固定 | plan_b.py `finalize()`＋literals（a_02 含單數字行） | What | D2 | 輸入輸出 requirement |
| C3 | 運算元非負整數；實測最大 `3791`（規格保證 `< 10000`）；中間值可為負，實測峰值 `44865`（規格保證 `\|值\| < 100000`）；無一元負號 | measured | design_b 量測（design-probe） | What | D2 | 值域 requirement |
| C4 | 除法保證整除；除數（除號右運算元求值後）恆為**正整數**，實測最小 `1`；`0 / d = 0` 合法 | assert 全 40 筆 | plan_b.py eval assert＋量測 | What | D2 | 整除 requirement |
| C5 | 關聯輸入無法由 8 型別引擎原生生成 → 全 literal 策展 | 40/40 literal | change A 先例 | Why | D3 | — |
| C6 | input_budget | `63488`；最大 entry `50084` bytes（b_20） | plan_b.py 輸出（design-probe） | — | D3 | — |
| C7 | op 斷崖不可建：重寫類天真解重活皆 C 層 | b011_rewrite `83_398` ops on 35KB → PASS | probe_b.py（design-probe） | Why | D4 | — |
| C8 | 得分階梯軸心＝語義鑑別（非 TLE）；語義完全正確的繞道一律收編 | 見 V 表 | C7＋Q5/Q6 無 TLE 要求 | Why | D4 | 判分 requirement |
| C9 | literal 內容參與池 seed；任何 literal 改動＝全池重洗 | 行為既知 | change A 教訓 | — | D3 | — |
| C10 | 答案分布：相異值數／正負混合 | 011=`39` 種、012=`42` 種；皆含正負 | plan_b.py assert（design-probe） | — | D5 | — |
| C11 | 題面禁資料結構術語；兩題獨立生活情境 | Q9 拍板 | grilling 決策 | What | D6 | 題面 requirement |
| C12 | 難度：011=medium、012=hard；category=apcs、type=competition | Q2 拍板 | grilling 決策 | What | — | — |
| C13 | 錯誤路線**聯集**上界：任一 entry 被任何已建模錯誤路線拿下的總數 | 011=`4/20`、012=`8/20`（=無括弧結構性下限） | plan_b `wrong_union` assert（design-probe） | — | D5 | 判分 requirement |
| C14 | 判題 op 計數器為單發跳閘（TimeoutError 可被 try/except 吞掉重試）——平台級議題，本 change 階梯不依賴 TLE 故零影響；已記錄待平台 change | 平台議題 | 賞金 judge-mech lens（實測 buildWrappedCode） | — | D1 note | — |

## A — apcs011 福利社老收銀機（snack-bar-register）

| ID | 事實 | 值／狀態 | evidence 出處 | proposal | design | spec |
|----|------|---------|--------------|----------|--------|------|
| A1 | 語義：加減先於乘除；加減左結合；乘除左結合；無括弧 | 固定 | Q5/Q6 拍板＋semantics.eval011 | What | D2 | 語義 requirement |
| A2 | 範例 entry（T=5）：`3 + 5 * 2`=`16`、`10 - 4 - 3 + 2 * 6`=`30`、`2 * 3 + 4`=`14`、`1 - 7 / 2`=`-3`（負中間值示範）、`7`=`7` | verified | probe_b.py＋plan_b（design-probe） | — | D2 | Example 區塊 |
| A3 | E1 對調繞道（+↔\*、-↔/ ＋ dunder 包裝 eval）語義完全正確 → 收編 | `20/20`；`279_208` ops on 50KB | verify（design-probe） | Non-Goals | D4 | — |
| A4 | E2 標準優先序 eval 上界 | ≤`3`；實測 `2/20`（entries 2,3） | plan_b assert＋verify | — | D5 | 判分 requirement |
| A5 | 加減右結合誤解上界 | ≤`4`；實測 `1/20`（entry 2） | plan_b assert＋verify | — | D5 | 判分 requirement |
| A6 | 乘除右結合 bug（遞迴下降 `expr:=term op expr`）上界 | ≤`4`；實測 `3/20`（entries 1,2,3） | plan_b assert（design-probe） | — | D5 | 判分 requirement |
| A7 | 20 筆結構：1 範例(T=5)／2-3 gimme／4-7 手工考點（含 L2R、divtight 鑑別行）／8-12 seeded 中型／13-16 大型／17-20 規模 30-50KB | 固定 | plan_b.build_011 | — | D3 | 測資 requirement |
| A8 | 正解 ops 餘裕 | 單筆峰值 `28_864`；全 20 筆累計 `161_108` ops／`0.036`s | HARNESS（design-probe） | — | D4 | — |
| A9 | L2R（全運算子同優先序左到右）上界 — 賞金 F5 | ≤`3`；實測 `2/20`（entries 2,3） | plan_b `l2r` assert＋b011_l2r 實測 | — | D5 | 判分 requirement |
| A10 | divtight（`/` 比 `*` 更緊）上界 — 賞金 F1 旁系 | ≤`4`；實測 `4/20`（entries 1,2,3,11） | plan_b `divtight` assert | — | D5 | 判分 requirement |
| A11 | R2 regex 括弧化＋eval 繞道（將加減段用 regex 包括弧再 std eval）語義正確 → 收編 — 賞金 F15 | `20/20` | bounty/a011_regexparen.py 實測 | Non-Goals | D4 | — |

## B — apcs012 折價券疊加試算（coupon-combo-quote）

| ID | 事實 | 值／狀態 | evidence 出處 | proposal | design | spec |
|----|------|---------|--------------|----------|--------|------|
| B1 | 語義：加減先於乘除且**右結合**；乘除左結合；括弧可覆寫；括弧自 entry 9 起 | 固定 | Q6 拍板＋semantics.eval012 | What | D2 | 語義 requirement |
| B2 | 範例：`10 - 4 - 3 + 2 * 6` = `66`（10-(4-(3+2))=11 → 11*6）。**修正 grilling 紀錄筆誤**：紀錄中的 5/30 為左結合（011 語義）值 | verified | probe_b.py（design-probe） | — | D2 | Example 區塊 |
| B3 | E1 左結合對調繞道上界 | ≤`4`；實測 `1/20`（entry 2） | plan_b assert＋verify | — | D5 | 判分 requirement |
| B4 | E3 冪次編碼路線類（+/- → `**` 標記）：**詞法補丁後語義完全正確 → 收編（E3′）**；e3_predict 僅表徵未補丁檔案 b012_pow.py 的 regex 破口，非路線類上界 — 賞金 F2 | E3′=`20/20`（fuzz 1200/1200）；naive 檔 `8/20` | bounty/b012_pow2.py＋fuzz_pow2.py（design-probe） | Non-Goals | D4 | — |
| B5 | E2 標準優先序 eval 上界 | ≤`3`；實測 `1/20`（entry 2） | plan_b assert＋verify | — | D5 | 判分 requirement |
| B6 | 教科書全遞迴 recursive descent 為合法正解：段長 ≤600、括弧深 ≤25 → 最深 `604` Python frames；已直接對出貨 Pyodide WASM 量測通過（賞金 judge-mech lens 去風險化） | `20/20`；`86_447` ops on 35KB | verify＋pyodide_recursion_probe.mjs | — | D2/D4 | — |
| B7 | 乘除右結合 bug（uniform）上界 | ≤`4`；實測 `3/20`（entries 1,2,3） | plan_b assert＋verify | — | D5 | 判分 requirement |
| B8 | 20 筆結構：1-8 無括弧（1 範例／2 gimme／3-6 手工／7-8 seeded＋DTkill 行）／9 括弧入門（含 PKline 鑑別行）／10-16 巢狀 2-25 層＋PKline／17-20 規模＋PKline | 固定 | plan_b.build_012 | — | D3 | 測資 requirement |
| B9 | 正解 ops 餘裕 | 單筆峰值 `72_106`；全 20 筆累計 `308_093` ops／`0.046`s | HARNESS（design-probe） | — | D4 | — |
| B10 | generator＝段折疊迭代式；reference_solution＝獨立異構實作（shunting-yard／RPN） | 待 apply | 設計決策 | What | D2 | — |
| B11 | divtight（`/` 比 `*` 更緊）上界 — 賞金 F1 主案 | ≤`4`；實測 `3/20`（entries 1,2,3；修補前 `15/20`） | plan_b assert＋b012_divtight 實測 | — | D5 | 判分 requirement |
| B12 | parens-std（括弧內改用標準規則）上界 — 賞金 F6 | ≤`8`；實測 `8/20`（entries 1-8＝結構性下限：無括弧段語義全對者應得） | plan_b assert＋b012_parenstd 實測 | — | D5 | 判分 requirement |
| B13 | 雙路徑複合解（無括弧行正確＋括弧行帶 mdr bug）上界 — 賞金 F3 | ≤`8`；實測 `8/20`（修補前 `20/20`；PKline=括弧行內同層雙乘除鑑別行封殺） | plan_b `hybrid_ok` assert＋sol_hybrid012 實測 | — | D5 | 判分 requirement |
| B14 | 「往回套用」語感有分岔讀法（逐次套用 vs 巢狀分組）——頁面規則必須以「每張券作用於其右側整段已計算結果」＋範例逐步拆解表述 — 賞金 F11 | 頁面撰寫約束 | page-lang lens | — | D6 | 題面 requirement |

## V — 判分預測表（I-6：AC 用上界式；精確值為 measured 紀錄非 AC）

| ID | 路線 | 011 | 012 | 狀態 |
|----|------|-----|-----|------|
| V1 | 正解（generator 同構） | `20/20` | `20/20` | design-probe ✓，ship-e2e ✓ |
| V2 | 教科書全遞迴（012） | — | `20/20` | design-probe ✓，ship-e2e ✓ |
| V3 | E1 對調 eval | `20/20`（收編） | `1/20` | design-probe ✓，ship-e2e ✓ |
| V4 | E2 標準優先序 eval | `2/20` | `1/20` | design-probe ✓，ship-e2e ✓ |
| V5 | L2R 全左到右 | `2/20` | — | design-probe ✓，ship-e2e ✓ |
| V6 | 乘除右結合 bug（uniform） | `3/20` | `3/20` | design-probe ✓ |
| V7 | E3′ 冪次編碼（詞法補丁版） | — | `20/20`（收編） | design-probe ✓，ship-e2e ✓ |
| V8 | divtight（/ 比 * 緊） | `4/20` | `3/20` | design-probe ✓，ship-e2e ✓ |
| V9 | parens-std | — | `8/20` | design-probe ✓，ship-e2e ✓ |
| V10 | 雙路徑複合（hybrid） | — | `8/20` | design-probe ✓，ship-e2e ✓ |
| V11 | N1 list-rewrite C 路線 | `20/20`（收編） | — | design-probe ✓ |
| V12 | R2 regex 括弧化＋eval | `20/20`（收編） | — | design-probe ✓，ship-e2e ✓ |

## 賞金結果（design bounty wf_b2660959-6d7）

| # | finding | 處置 | 驗證 |
|---|---------|------|------|
| F1 | 012 divtight 15/20（must-fix） | 修補：divtight predictor＋assert ≤4＋DTkill 行（e4/5/7/8）＋PKline（e9-20）→ `3/20` | b012_divtight 逐筆 ✓ |
| F2 | E3 8/20 上界非結構性、3 行詞法補丁 → 20/20（must-fix） | **收編 E3′**（改文件不改測資，遵守則⑤）；撤「結構性鎖死」全稱句（守則④） | b012_pow2 20/20 ✓ |
| F3 | 雙路徑複合解 20/20（must-fix） | 修補：PKline 括弧行內同層雙乘除鑑別行（e9-20）＋hybrid predictor assert ≤8 → `8/20` | sol_hybrid012 逐筆 ✓ |
| F4 | 聯集無上界（should-fix） | 修補：`wrong_union` assert（011 ≤6 實測 4；012 ≤9 實測 8） | report ✓ |
| F5 | 011 L2R 6/20 未建模（should-fix） | 修補：l2r predictor＋assert ≤3＋範例筆與 e4-6 鑑別行 → `2/20` | b011_l2r 逐筆 ✓ |
| F6 | 012 parens-std 9/20（should-fix） | 修補：predictor＋assert ≤8＋e9 PSkill 行 → `8/20` | b012_parenstd 逐筆 ✓ |
| F8 | 規格洞：單數字行／T 下限／除數符號／值域未載明 | 修補：C2/C3/C4 補錨定（除數恆正 min=1、運算元 max=3791、中間值峰值 44865） | 量測 ✓ |
| F9 | op 跳閘可 try/except 重試（平台級） | 記錄 C14；本 change 零影響；待平台 change | buildWrappedCode 實測 |
| F11 | 「往回套用」語感分岔（66 vs -54） | B14 頁面撰寫約束 | page-lang ✓ |
| F12 | 範例未覆蓋負中間值 | A2 範例筆加 `1 - 7 / 2` | ✓ |
| F14 | 大型筆答案 7-smooth／含大質數因子之弱指紋 | 接受殘餘（黑箱前提下僅助驗證不助生成）；記錄 | note |
| F15 | 011 regex 括弧化繞道 | 收編 A11／V12 | a011_regexparen 20/20 ✓ |
| F16 | float 除法＋int() 與 // 不可區分 | 非問題（整除保證下該路線語義正確） | note |

## 已知殘餘（收編清單）

| 路線 | 理由 | 處置 |
|------|------|------|
| E1 對調 eval（011） | 語義完全正確；需真正理解翻轉優先序 | 收編；成本數據見 A3 |
| R2 regex 括弧化＋eval（011） | 語義正確；需理解「加減段先算」的分段本質 | 收編；A11 |
| E3′ 冪次編碼（012） | 語義完全正確（fuzz 1200/1200）；`**` 為 Python 唯一右結合高優先序運算子，右結合性隨選擇免費取得——已知教學殘餘，不以測資獵殺（守則⑤） | 收編；B4／V7 |
| N1 list-rewrite（011/012） | 重活全在 C 層，op counter 與牆鐘皆無法獵殺 | 收編；不寫不可能性承諾（守則④） |
| parens-std／hybrid／E3-naive 的 8/20 | ＝無括弧段（entries 1-8）結構性下限：正確解出全部無括弧語義者理應得 8 | 接受；C13 聯集鎖 8 |
