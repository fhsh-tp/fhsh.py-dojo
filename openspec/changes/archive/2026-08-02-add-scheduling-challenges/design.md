## Context

題庫已有單資料流過程輸出題(deque 系列,`openspec/specs/deque-challenge-series/`),testcase_plan 機制(band/override/literal)已落地並經 e2e 驗證(`openspec/specs/testcase-plan/`)。判題引擎自 2026-07-28 起具備 TLE verdict(op-count 探測,上限 10M ops),但 op-counter 對 C 內建隱形——效能門檻只能靠「數量級斷崖」而非精細閾值。本 change 為純內容新增:兩道排程素養題,零引擎改動。

素材來源:2022 運算思維推動計畫「工作中的海狸」(多工作者排程)與 UVa 1203 "Argus"(週期事件優先佇列模擬)。UVa 1203 的原題定位:約束淘汰逐分鐘掃時間軸,但 O(K×Q) 線性掃與 heap 皆放行——逼「事件驅動思維」而非特定資料結構。

### 名詞表

| 名詞 | 定義 |
|------|------|
| 機台(printer) | 題一的資源單位,編號 1..m,狀態=下次空閒時刻 |
| 工單(job) | 題一的工作單位,依輸入順序派發,屬性=工時(小時) |
| 完工時刻(makespan) | 題一輸出:所有工單完成的最晚時刻,自 t=0 起算 |
| 排程(schedule) | 題二的週期提醒登記,隱含編號 i=輸入順序 1..Q |
| 提醒事件(event) | 題二排程 i 於 週期×1、×2、×3… 分鐘各觸發一次 |
| 預告序列 | 題二輸出:依時刻排序的前 K 個事件之排程編號,同時刻→編號小者先 |
| 暖身/壓力/literal band | testcase_plan 三段:手算規模/大規模/手寫邊界 |

## Goals / Non-Goals

**Goals:**

- 兩題素養題面:只描述現實處理模式,題面與 tags 零解法字眼。
- 題二以壓力 band 製造數量級效能斷崖:逐分鐘掃 TLE、線性掃與 heapq 皆 AC(餘裕 ≥20×,探針實測)。
- generator 與 reference_solution 異寫法互驗(掃描 vs heapq)。

**Non-Goals:**

- 不做 DAG 相依排程(海狸原題的前置關係)——輸入複雜度與認知負荷跳級,棄用。
- 不逼 heapq(淘汰線性掃)——log 倍差距門檻不可調,重蹈 id 56 教訓,棄用。
- 不動 Rust 引擎、scripts、前端;不新增 params 型別。
- 不含發 PR/release;本 change 止於 archive + commit。

## Decisions

1. **題一無相依多站派工**(vs 忠實還原海狸 DAG):規則單一(最早空閒機台接手、同時空閒→編號小者),學生只需維護 m 個空閒時刻;DAG 需維護可行集合且隨機產生受限,教學價值/成本比劣。
2. **題一輸出 makespan 單一整數**(vs 第 K 件完工時刻):零 tie 糾纏,與題二的序列輸出區隔明確。
3. **題二隱含編號 1..Q**(vs UVa 1203 明給編號):引擎無法產生互不重複的隨機值;隱含編號零撞號、tie 規則「編號小者先」=「先登記者先」在情境中自然。
4. **效能定位=忠於 UVa 1203**:壓力 band 參數形狀「Q 小(3~5)、週期大(3 萬~5 萬)、K 中(300~400)」使逐分鐘掃需千萬級迭代(TLE),線性掃 K×Q≈2000 次迭代(AC);上界已由 op 探針實測定案(見 Implementation Contract 效能門檻小節)。初版 2 萬~5 萬/200~400 經探針實測最省角落僅 1.04× 超限、緊貼門檻,故收緊下限。
5. **輸入單批、數列一行空白分隔**:引擎限制「不同參數各占一行」,故 m、n(或 Q、K)各一行,數列以 count.from + 預設空白 separator 單行渲染。
6. **難度與型別**:皆 `type: competition`(著重限制邊界、不講做法);題一 medium、題二 hard(誠實標示效能門檻);tags 僅「模擬、排程」。
7. **單一 change 包兩題**:純內容新增、驗證流程完全相同,tasks 內部按題分組。

## Implementation Contract

### 題一 print-farm-schedule(列印工坊排程,id 由 scaffold 自動分配)

- **語義**:讀入 m(機台數)、n(工單數)、n 個工時。工單依輸入順序逐張派發:交給「下次空閒時刻最早」的機台;多台同時最早→機台編號最小者。機台自空閒時刻起連續印完該工單。輸出=所有機台完工時刻的最大值(單一整數、一行)。
- **輸入格式**(stdin 三行):`m`↵`n`↵`t1 t2 … tn`(空白分隔)。
- **驗證範例**:m=2、n=4、工時 `2 3 5 7` → 工單1→機1(0~2)、工單2→機2(0~3)、工單3→機1(2~7)、工單4→機2(3~10)→輸出 `10`。
- **frontmatter 草案**:params `m:int 2..5`、`n:int 1..400`、`times:int 1..5000, count.from n, separator " "`;testcase_plan=3 筆暖身(override m 2..3、n 3..8、times 1..20)+2 筆壓力(override n 200..400)+1 筆 literal(`3`↵`2`↵`5 9`,機台多於工單→答案 9)。
- **generator**:list 掃描 m 個空閒時刻取 (時刻,編號) 最小;**reference_solution**:heapq 存 (空閒時刻, 機台編號) tuple。

### 題二 pillbox-reminder(智慧藥盒提醒)

- **語義**:讀入 Q(藥品數)、Q 個週期(第 i 個=藥品 i 的提醒週期,分鐘)、K。藥品 i 於 週期×j(j=1,2,3…)分鐘觸發提醒。全部事件依 (時刻, 編號) 遞增排序,輸出前 K 個事件的藥品編號,一行一個(共 K 行)。
- **輸入格式**(stdin 三行):`Q`↵`p1 p2 … pQ`(空白分隔)↵`K`。
- **驗證範例**:Q=2、週期 `3 5`、K=6 → 輸出 `1 2 1 1 2 1`(各一行;t=3,5,6,9,10,12)。tie 範例:週期 `2 3`、K=7 → t=6 同時刻①先②後 → `1 2 1 1 2 1 2`。
- **frontmatter 草案**:params `q:int 2..5`、`periods:int 2..50000, count.from q, separator " "`、`k:int 1..400`;testcase_plan=3 筆暖身(override periods 2..30、k 5..20)+2 筆壓力(override q 3..5、periods 30000..50000、k 300..400)+1 筆 literal(`3`↵`2 3 6`↵`12`,t=6/t=12 三重 tie→`1 2 1 1 2 3 1 2 1 1 2 3`)。
- **generator**:維護 Q 個「下次觸發時刻」,每輪線性掃取 (時刻,編號) 最小後推進該排程;**reference_solution**:heapq 存 (下次時刻, 編號, 週期)。
- **效能門檻(壓力 band,已實測定案 2026-08-02)**:探針重現 worker-utils.ts buildWrappedCode 的 settrace 計數(每 trace 事件計 1 op,DEFAULT_OP_LIMIT=10,000,000),於全角落網格(Q∈{3,5}×週期∈{20000,30000,50000} 全同×K∈{200,300,400})實測三種寫法。定案 band=q 3..5、periods 30000..50000、k 300..400:逐分鐘掃最省角落(Q=5、週期 30000、K=300)=23,400,609 ops(2.34× 必 TLE);線性掃最貴角落 5,529 ops(餘裕 1809×);heapq 最貴角落 1,616 ops(餘裕 6188×)。三種寫法對 spec 全部 Example 輸出逐字元一致。初版 periods 20000..50000/k 200..400 的最省角落僅 10,400,409 ops(1.04×),不滿足穩健斷崖,棄用。

### 共同契約

- 題面結構(兩題同):情境段(現實處理模式)→動手推演段(題一甘特圖/題二逐分鐘表)→輸入說明→輸出說明→範例(題二範例必含 tie 案例)。
- 素養約束:題面與 tags 禁用詞——排序、佇列、堆疊、heap、優先、掃描、模擬時間軸、資料結構;tags 固定為「模擬」「排程」。（「模擬」為既有 tag 分類慣例,不視為解法字眼。）
- 驗收出口:`pnpm build:pools` 成功;`scripts/challenge-params.test.ts` 全綠;`scripts/content-regression.test.ts` 兩題 reference_solution 對正式池全 AC;agent-browser e2e(正解 AC、錯解 WA、題二逐分鐘掃 TLE)。
- Scope in:兩個題目 md 檔 + openspec 工件。Scope out:引擎/scripts/前端/CI、PR 與 release。

### 追溯矩陣({面向×邊界}→{期望行為→驗收出口})

| # | 面向 | 邊界/情境 | 期望行為 | 驗收出口 |
|---|------|-----------|----------|----------|
| T1 | 題一派工 | 同時空閒(t=0 全機台) | 編號小者接手 | spec S1 場景+範例 10 |
| T2 | 題一邊界 | 機台多於工單(literal m=3,n=2) | 答案=max(工時)=9 | spec S2 場景+content-regression |
| T3 | 題一壓力 | n=200..400 | 狀態維護正確、無效能門檻 | content-regression |
| T4 | 題二 tie | 同時刻多藥(literal t=6 三重) | 編號遞增輸出 1,2,3 | spec S4 場景+content-regression |
| T5 | 題二效能 | 壓力 band worst-case | 逐分鐘掃 TLE、線性掃/heapq AC | 探針數據+e2e TLE 實測 |
| T6 | 輸出格式 | 題一單行整數/題二 K 行 | 逐字元一致 | content-regression+e2e |
| T7 | 素養約束 | 題面+tags | 禁用詞零出現 | audit 檢核 |

## Risks / Trade-offs

- [壓力 band 門檻誤傷或漏放] → 探針實測 + 數量級斷崖(千萬 vs 十萬級)+ 餘裕 ≥20× 驗收;不達標調 band 重測,不硬上。
- [literal 手寫 stdin 與 generator 語義不符] → literal 的期望輸出由 generator 即時計算(機制保證),另以追溯矩陣 T2/T4 在 content-regression 中覆蓋。
- [generator 於建置期以 CPython 跑 33 blocks×6 筆] → 兩題 generator 均為線性掃(K×Q≤2000/筆),建置耗時可忽略。
- [題面禁用詞遺漏] → audit 階段以 T7 專項檢核,禁用詞表列於共同契約。

## Migration Plan

無遷移需求(純新增)。回滾=刪除兩個題目 md 檔並重跑 build:pools。
