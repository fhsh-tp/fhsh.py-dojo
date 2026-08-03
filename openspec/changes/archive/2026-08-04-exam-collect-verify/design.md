## Context

id 55《撲克牌重排計數》建立了「兩端抽出、疊放成堆」的機制認知（計數向）；本題是其驗證向姊妹題。規格由 2026-08-04 八題 grilling 討論定案，其中六項技術主張經 6 席對抗驗證（run `wf_85a29712-d89`）以窮舉腳本與引擎原始碼實測背書。既有基礎設施：測資引擎（Rust crate `testcase-generator`，params 八型別含 `enum`）、判題 op 計數（settrace、上限 10M、逐 pool 測資歸零）、testcase_plan（literal／band、`input_budget` 逐題覆寫）、challenge-params 與 content-regression 守門。

### 名詞表

| 名詞 | 定義 |
|------|------|
| 來源行 | 一排考卷「講台端→窗邊端」的座號序列，同排座號互不相同 |
| 收卷順序 | 依時間先後被收走的座號序列（每次只能收該排最左或最右端一張） |
| 回報 | 宣稱的最終考卷疊「由頂到底」座號序列；回報 = 收卷順序的反轉 |
| 合法回報 | 存在某種兩端收法能產生該回報 |
| 反轉陷阱行 | 把「收卷順序」誤當回報會誤判合法、正確判定為不合法的回報行 |
| 乙′ band | 來源用 enum 排列庫、查詢行用 enum 策展候選庫的隨機測資檔位 |
| 策展保證 | 對排列庫每個來源 i，M 條查詢的候選庫聯集中至少存在一條「正確語意與忘記反轉語意判定不同」的行 |

## Goals / Non-Goals

**Goals:**

- 一道 medium／competition／apcs 挑戰題，考「兩端取出＋堆疊反轉」判定，素養情境不出現 deque／stack 術語
- TLE 斷崖誠實成立：全枚舉（2^N）在壓力筆必死（最省寫法角落 ≥2× op 上限）；Python 層 O(N²) 在本題形（座號值域 ≤999＋單筆位元組預算）下數學上殺不到 2×，明定為穩定放行（≤0.7×，見 Decisions 5）；正解餘裕 ≥100×
- 防裸背答案：pool 10 blocks 因乙′ band 抽籤而互異，裸背通過率 ≤1/10

**Non-Goals:**

- 不改測資引擎（Rust）——所有測資以現有 params 能力（enum／int count／literal）表達
- 不做重複座號語意（左指標集 DP 路線已在討論中排除：正解僅 1.6× 餘裕、考點偏移）
- 不動其他題目、不動判題機制、不動列表頁
- 策展／壓力測資生成腳本為建置期一次性工具，不納入 repo（結果數據與驗證程序記錄於本檔，見「AC 驗證程序（可重建）」）

## Decisions

1. **判定語意＝模型 B**：回報反轉為收卷順序 e，對來源 s 做雙指標貪婪（`e[i]==s[l]` 取左、否則 `e[i]==s[r]` 取右、否則不合法）。相異值前提下貪婪嚴格正確（58 萬組窮舉 vs 暴力 DFS 零不一致；C1）。
2. **相異值**：題面明文「同排座號互不相同」。允許重複時固定平手貪婪必錯（C2 反例）且正解 DP 貼 TLE 線（C4），故排除。
3. **乙′ band 結構**：params 宣告固定形狀 T=1、N=6、M=8——`t`(int 1..1)、`header`(enum 單值 "6 8")、`src`(enum 10 個座號排列)、`q1..q8`(各 enum 10 個策展候選)。理由：`group.repeat` 只能引用 param 名（parser.rs:293-298）、多形狀需多份 params 宣告而引擎只允許一份；card-restack 的 `n1..n10` 為逐一宣告前例。
4. **策展候選設計**：所有候選皆為來源值域的排列（殺「只檢查重排」的混子解）；每條查詢行候選庫含對特定來源合法的行（期望每筆 ≈0.8 條合法）；含策展保證（見名詞表）。
5. **壓力筆殺傷設計**：N=800、M=18、T=1。2^800 使任何指數解第一行即死（探針實測倍率 2.00/元素、首爆 n≈23）；正解實測 worst 50,435 ops、餘裕 198×。Python 層 N² 線性掃描實測 0.38~0.58×——在「座號 ≤999 相異值＋單筆位元組預算」的題形下 N² 殺傷數學上到不了 2×，強推只得 1.0~1.2× flaky 帶，故明定為穩定放行（≤0.7×）並寫入 spec。`input_budget: 63488`（單筆實測 59,156 bytes < 預算 < 65536 硬上限）。C 層 N²（`list.pop(0)`）不可見也不需殺——它語意正確且 wall-clock 無虞。
6. **雙實作零共用邏輯**：generator＝反轉＋雙指標；reference_solution＝位置區間外擴（座號→位置表；回報首元素位置為起點，其後每元素位置須恰為目前連續區間左外側或右外側）。缺號（KeyError 防護）、重複座號（位置落在區間內）自然判不合法。
7. **範圍宣告**：1≤T≤10、1≤N≤800、1≤M≤50、座號 1..999；測資實際值不超出宣告。

### AC 驗證程序（可重建）與實測數據

驗證腳本為一次性離線工具，不入 repo；以下判定式足以重寫等價腳本（禁寫入 repo 的內容：source×candidate 合法對照表、band 逐欄合法標記、槽位語意配置、各筆期望輸出——這四類只會擴大背答案面）。

1. **三方互驗**：generator 邏輯（反轉＋雙指標）、reference 邏輯（位置區間外擴）、暴力 DFS（memo on (l,r)）三方比對——N≤6 全排列 s×q 窮舉＋非排列樣本、N=800 隨機（已知合法／隨機重排／合法擾動）。實測：535,217 組窮舉＋3,000 組大 N，**零不一致**；另以「從 .md 抽 frontmatter 原文執行」端到端重驗 400 組＋大 N 煙霧，零不一致。
2. **TLE 探針**：重現 `.vitepress/theme/workers/worker-utils.ts` settrace 計數（每事件 +1、上限 10M、逐 pool 測資歸零）。實測：正解全 literal worst 50,435 ops（餘裕 198×）、band 最壞抽籤 163 ops；最省事件全枚舉倍率 2.00／元素、首爆 n≈23（壓力筆 N=800 天文數字絕殺）；Python 層 N² 線性掃描 0.38～0.58×（穩定放行側）。
3. **策展驗證**：(a) 全候選皆為值域 V 排列；(b) 策展保證＝每個來源 j 在八條候選庫聯集中 ∃ correct≠forgot 的行（forgot＝不反轉直接兩端比對），實測每來源 diff 候選 9～17 條；(c) 期望合法行數 E＝Σ_i avg_{j,k} legal(src_j, cand_{i,k})，實測 **E=0.750**（區間 0.5~1.5）。
4. **語意級測資分類 gate**：判別 literal 9 筆逐筆分類（nonperm＝多重集不符；legal＝反轉後貪婪成功；trap＝反轉失敗但不反轉成功；餘為 nonprod），每筆四類 ≥1、header M＝實際行數、兩語意計數不同。round 1 修復後實測 9/9 全過。
5. **池驗證**：`generatePoolInputs`（正式 request 形狀）200 筆→10 blocks 全相異、56/200 相異輸入（16 literal＋4 band×10 抽籤）。

### 型別×邊界矩陣（測資覆蓋）

| 維度 | 邊界 | 覆蓋檔位 |
|------|------|----------|
| N | 1（單張，回報即該座號）／2（任何重排皆合法）／800（壓力上限） | 邊界筆／範例第二組／壓力筆 |
| M | 1／18（壓力）／50 不出現（宣告上界鬆，允許） | 邊界筆／壓力筆 |
| T | 1／10（多組小 N 混排） | 壓力筆等／邊界筆 |
| 回報類型 | 合法／反轉陷阱／排列但取不出／非排列（重複座號、缺號） | 範例＋考點筆每筆混合 |
| 座號值 | 非連續、非 1..N 的相異值（如 3 1 4 2；策展庫用散值） | 全檔位 |

## Implementation Contract

- **Behavior**：學生程式讀 stdin（T→每組「N M」→來源行→M 行回報，空白分隔），輸出 T 行，每行一個整數＝該組合法回報數。判定語意見 Decisions 1。
- **Interface / data shape**：`docs/challenge/exam-collect-verify.md` frontmatter——`layout: challenge`、`id`（scaffold 配發）、`title: 收卷順序驗證`、`difficulty: medium`、`category: apcs`、`type: competition`、`tags: [data structure, 模擬]`、`algorithm: exam_collect_verify`、`input_budget: 63488`、`params`（Decisions 3 形狀）、`testcase_plan` 20 筆（範例 1＋考點 9＋乙′ band 4＋壓力 3＋邊界 3，第一筆 literal＝題面範例）、`generator`、`reference_solution`、`starter_code: ""`。
- **Failure modes**：非排列回報（重複／缺號／外來座號）由兩實作自然判不合法，不 crash；generator 對任意符合格式的輸入必須輸出 T 行整數。
- **Acceptance criteria**：
  1. 雙實作互驗：N≤6 全排列窮舉 vs 暴力 DFS 零不一致；N=800 隨機 3000 組互驗一致
  2. TLE 探針：重現 worker-utils.ts settrace 計數，壓力筆對「最省事件全枚舉」≥2×10M ops（外插自倍率擬合）；「Python 層 N² 逐步線性搜尋」≤0.7×10M（穩定放行、不設 flaky 帶）；正解全 20 筆各筆 ≤1/100×10M
  3. 策展驗證腳本：策展保證成立＋每條查詢行候選庫 10 條皆為來源值域排列＋合法行出現率實測落於每筆期望 0.5~1.5 條
  4. `pnpm build:pools` 成功、`scripts/challenge-params.test.ts` 與 `scripts/content-regression.test.ts` 通過（正解對正式加密池全 AC）、`pnpm typecheck`／`lint`／`test --run` 綠
  5. 題面含：情境敘述（不出現 deque／stack／佇列／堆疊字眼）、動手推演（含一條合法收法逐步圖解與一條卡死示範）、輸入輸出說明（含三項明文保證：座號互不相同、回報為由頂到底、座號 1..999）、範例＝Q5 定稿內容
- **Scope boundaries**：僅新增一個挑戰檔案；引擎、判題、頁面、其他題目零改動。

## Risks / Trade-offs

- **壓力筆體積（量化後知情接受）**：實測（基準 commit a517701；量測法＝frontmatter 自 `testcase_plan:` 至下一頂層鍵、gzip -9、KB 採 1000 B）testcase_plan 區約 184.3KB（gzip 約 56KB），佔題檔約 96%，三筆壓力 literal 各約 59.2KB。後續編輯僅在 ±1KB 內浮動，不改變本項知情接受的結論。成本形態＝上述體積即每位開啟本題頁面的訪客一次性下載量（同前，gzip 約 56KB），無執行期 CPU 開銷。界定：challenge.data.ts 白名單映射（includeSrc: false）使 plan 不進列表頁 chunk，重量僅限本題頁；prod 端 plan 唯一用途是推出測資總數 20，判題輸入來自加密池。literal 是「輸入」不是答案（generator/reference_solution 由 build 剝除），且 band 逐 block 隨機使硬編 16 筆答案無法 AC——同一份 literal 本就在公開 repo，進 bundle 未新增洩漏管道。若未來要減重，唯一不挖洞的槓桿是在 delta spec 內縮小壓力筆 N（指數解 n≈23 即超限）並重跑探針；不得在本 change 夾帶 build 期剝除。
- **band 的防護邊界**：乙′ band 針對的是「盲背固定輸出序列」（通過率壓至 ≤1/10）；具備離線重建測資能力的攻擊面（公開 repo＋可解密池）屬站方既接受基線，本題未新增管道。
- **乙′ 策展是手工資產**：候選庫品質決定 band 筆鑑別力；以 AC-3 的驗證腳本鎖住，不依賴人工目測。
- **N² 線性掃描落在灰帶邊緣**：事件常數更重的 N² 變體（每迭代 3~5 事件）會落在 0.9~1.5×，個別學生可能不穩定；這是題形（座號值域×位元組預算）的固有限制，已以 0.58× worst 實測數據壓在穩定側。
- **reference_solution 對合約外輸入的行為**：回報行 token 數 < N 的畸形輸入下，ref（位置區間外擴）會判合法而 generator 判不合法——現行測資契約（每行恰 N 值，由生成腳本與語意級 gate 斷言）下不可達；刻意不在解法層加防護（spec 已凍結兩演算法形狀，加防護＝挖洞），記錄於此供未來手寫 literal 者知悉。
- **探針為本機 CPython 近似**：與 Pyodide 同 minor 版（3.13）事件語意一致，但常數可能有個位數百分比差——所有貼線判斷均要求 ≥2× 邊際吸收。
- **N=800 相異座號 vs 座號 ≤999**：999 個可用座號放 800 張，構造可行但接近上限；壓力筆生成腳本直接取 1..999 抽樣 800 個排列，無機率風險。
