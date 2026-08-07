# 追溯矩陣（change C：add-exhibit-route-duo）

本檔為本 change 的**單一真相來源（SSOT）**。proposal／design／spec／題目頁面的每一句量化敘述都必須指回這裡的事實 ID；沒有 ID 的數字不得出現在任何文件。路線 ID 的機械正本是 `curation/plan013.py::CAPS` 與 `curation/plan014.py::CAPS`——本檔與 design 的路線清單必須與那兩個字典逐條對齊。

量測環境：node-Pyodide（`node_modules/pyodide`，與站台自架版本同源），harness＝`curation/probe.mjs`（複製 `worker-utils.ts::buildWrappedCode` 的 tracer 包裝）。牆鐘數字為 node 環境值，僅作**相對量級**參考；出貨前以瀏覽器 e2e（V 表）覆核。

---

## C 表：平台與判題機制

| ID | 事實 | 證據 |
|----|------|------|
| C1 | 每筆測資的 op 上限為 10,000,000 | `pyodide.worker.ts::DEFAULT_OP_LIMIT` |
| C2 | op 計數器＝`sys.settrace` 事件計數（call／line／return／exception 各記 1），內建函式的 C 層工作**不計數**；同一行塞多個敘述只算一個 line 事件 | `worker-utils.ts::buildWrappedCode` 的 `_tracer`；實測見 A3（C 層路線比正解便宜）與 B3（攤平寫法每球 1 op） |
| C3 | worker 端每筆測資另有 5,000 ms 軟旗標；旗標為 JS `setTimeout`，只能在同步 Python 執行結束後才觀察得到，命中即判 TLE（即使輸出正確） | `pyodide.worker.ts::WALL_CLOCK_MS` 與 `wallClockTle` 分支 |
| C4 | 主執行緒硬砍為 `測資數 × 6,000 ms` **累計**（20 筆＝120,000 ms），到期即 `stop()`：worker 被終止、分數以當下已回報的結果定案；未回報的測資不會產生列 | `useExecutor.ts::WALL_CLOCK_KILL_MS`、`totalBudget = testcases.length * WALL_CLOCK_KILL_MS` |
| C4b | C4 觸發時的畫面呈現：`ChallengeView` 的「得分：N / 總數」用的是 store 的總測資數（正確），但結果表格是以已回報列數為分母 → **中斷的執行可能在表格上看起來全綠**。本 change 以「陣亡提交的總牆鐘必須遠低於 120 s」規避（B7），不改引擎 | 設計期賞金 F17；`useExecutor.ts::stop()` 與 `TestResultPanel.vue` |
| C5 | 判定＝stdout 比對（兩側先 `trimEnd`，容忍尾端空白／換行後逐字相等）；未捕捉例外→RE；op 跳閘→TLE | `pyodide.worker.ts::computeVerdict`、`opLimitExceeded` |
| C6 | Pyodide `sys.getrecursionlimit()` = 1000；tracer 之下單框遞迴實測最深 994 層，超過拋 `RecursionError`（乾淨例外，非 worker 崩潰） | `curation/probe_depth.py`（二分量測，可用 `curation/probe.mjs` 重跑） |
| C7 | 單筆測資輸入硬上限 65,536 bytes 不可覆寫，`input_budget` 宣告值須小於此數；literal 條目以實際 byte 數計入 | `Usage.md`〈輸入規模預算〉 |
| C8 | `testcase_plan` 的 literal 內容參與正式池 seed 導出——改任何一字都會重洗整池 | `Usage.md`〈測資決定性〉 |
| C9 | 正式池存 `floor(200 ÷ 每場筆數)` 個 block；全 literal 計畫下各 block 內容相同 | `Usage.md`〈正式池結構〉 |
| C10 | 題目 `id` 由 `pnpm new-challenge` 配號，不得手填；`--category apcs` 決定前綴與上架頁 | `scripts/new-challenge.ts` |
| C11 | 生產建置只剝除 `generator` 與 `reference_solution`，**`testcase_plan` 的 literal 內容會原樣進入前端 bundle**；本專案的 repo 亦為公開，出貨測資輸入本來就可見 → 全 literal 題目的「離線算好答案再硬編碼」是**專案層既存殘餘**（apcs006、apcs009–012 同此），非本 change 新增；處置見〈賞金結果 F18〉 | `openspec/specs/generator-strip-plugin/spec.md`（明列 `testcase_plan` 保持原樣）、`ChallengeView.vue` 讀取 frontmatter |

---

## A 表：apcs013 展場動線重建

| ID | 事實 | 證據 |
|----|------|------|
| A0 | 出貨實測（ship-measured）：`reference_solution` 最壞 37,537 ops／13 ms；`generator` 最壞 71,663 ops／21 ms；收編的 `.index()` 路線最壞 25,036 ops／12 ms；收編的鏡射解最壞 77,609 ops／33 ms。全部遠低於 C1 | `probe.mjs` 對 `curation/literals/c013_*.txt` 全 20 筆 |
| A1 | 語義：每筆測資含 T 組；每組為「模式標記 M＋展區數 n＋兩串打卡序」。模式 1＝甲（進區先打卡→左岔→右岔）＋乙（左岔→打卡→右岔）求丙（左岔→右岔→打卡）；模式 2＝乙＋丙求甲 | `curation/semantics013.py`（正本） |
| A2 | 正解（雜湊索引＋顯式堆疊，無遞迴）成本約 31 ops/展區、與形狀無關 | `probe.mjs`；探針 n=2000 三形狀同為 62,035 ops |
| A3 | `.index()`＋切片天真解重活全在 C 層（C2），成本反而比正解低（出貨最壞 25,036 ops，見 A0）→ **不可獵殺，收編為聰明解**。附註（探針、非出貨形狀）：輸入預算容許的極端 n=6000 左鏈為 60,024 ops／715 ms，該形狀同時違反 A5 深度上限與 A8 byte 上限，只作上界參考 | `probe.mjs` 對出貨 literal 與探針輸入 |
| A4 | 純 Python 逐格掃描版在 n=2000 左鏈為 4,028,025 ops、未跳閘；要超過 C1 需 n≈6000 的深鏈，而該深度違反 A5 → 本題**不建 op 斷崖**，鑑別軸為語義 | `probe.mjs sol/c013_naive_scan.py`（探針） |
| A5 | 出貨測資的動線深度上限訂為 **300**（實際最深＝300）：由 C6（994 層）推得，對每層 1 框的遞迴解有 3.3 倍餘裕。實證：不調 recursionlimit 的遞迴解在深度 300 的第 19 筆為 17,847 ops、無 RecursionError | 設計決策＋`probe.mjs sol/c013_naive_norecur.py literals/c013_19.txt` |
| A6 | 路線清單與**出貨實測**得分（`plan013.py` 逐筆比對，非估算）：W1 模式盲 10／W5 只讀一次模式標記 11／W2 模式 2 取丙序首元素 10／W4 模式 2 展開順序誤為先左後右 10／W3 誤把編號排序當第二串 0／W6 只解第一組 2／W9 反轉第一串 0／W10 照抄第二串 0／W11 形狀字典（零重建）2／Z1 照抄第一串 0／Z2 反轉第二串 0／Z3 降序排序 0；收編：R1 鏡射解 20、`.index()` 天真解 20 | `curation/plan013.py::CAPS`＋`report013.json` 的 `*_ok` 逐筆欄位 |
| A6b | W4 的精確語義＝「模式 2 自尾端消耗丙序時，展開順序誤為先左後右」。**全程一致地把左右改名是本題的對稱性、輸出與正解相同，屬收編、不得獵殺** | `semantics013.py::route_W4_swaporder` |
| A7 | 展區編號為 1..n 的**隨機重排**（非依中間序排序），封殺「把編號排序當第二串」的假設（W3＝0） | `semantics013.py::make_case` |
| A8 | 每筆測資 byte 上限 50,000、`input_budget` 宣告 63,488（< C7）；出貨最大筆 20,588 bytes、最大 n＝1400 | `curation/report013.json` |
| A9 | 每筆測資至少一組**左右結構不對稱**（鏡射後結構簽章改變），機械斷言已實作 | `plan013.py` 的 `mirror_asym` 檢查、`semantics013.py::mirror`／`sig` |
| A10 | 形狀多樣性以**結構簽章**判定（不是形狀名稱）：每筆至少兩種簽章、至少一組非單一路徑。必要性實證：`spine` 在 n ≤ 120 時 `rest = 0`、退化成純左鏈；`zigzag` 任何長度都是單一路徑 | `plan013.py` 的 `sigs`／`chain` 斷言、`semantics013.py::is_chain` |
| A11 | 三重交叉：語義正本的建構→三序輸出、`gen013.py`（顯式堆疊）、`ref013.py`（分段遞迴＋位置雜湊）三者在全 20 筆 literal 上輸出一致 | apply 期腳本比對，0 筆不符 |
| A12 | **收編路線 R1（鏡射解）**：模式 2 的答案＝reverse(模式1(reverse(第二串), reverse(第一串)))，語義等價、實測 20/20、最壞 77,609 ops。題面不得出現任何暗示「兩種模式必須各寫一套」的句子 | `semantics013.py::route_R1_mirror`、A0 |
| A13 | 輸入無二義性：標號兩兩相異時，(甲,乙)→丙 與 (乙,丙)→甲 皆為單射，n ≤ 11 窮舉 0 碰撞；且任意兩個同集合排列都構成合法輸入 → 模式標記無法由資料自我推導，這是它必須存在的形式理由 | 設計期賞金 F13（窮舉證明） |
| A14 | **模式 2 的左鏈組別對「模式盲」誤讀免疫**（左鏈的乙與丙相同，誤讀後恰好輸出正確的甲；n=1..9 窮舉：每個 n 恰一形狀免疫且為左鏈）。因此「每筆含模式 2 的測資至少要有一組非單一路徑、n ≥ 3」是 W1＝10/20 的真正守門機制，已寫成斷言 | 設計期賞金 F16；`plan013.py` 的模式 2 非鏈斷言 |
| A15 | 範例筆豁免：第 1、11 筆為題面兩個範例，單組、n=7，不承擔鑑別責任——W6（只解第一組）與 W11（形狀字典）各拿這 2 筆即為契約地板。其餘 18 筆的最大 n 一律 ≥ 20，讓「窮舉所有形狀」的暴力解不可行 | `plan013.py::EXAMPLE_ENTRIES` 與 n ≥ 20 斷言 |

---

## B 表：apcs014 彈珠台軌道預測

| ID | 事實 | 證據 |
|----|------|------|
| B1 | 語義：機台共 D 層——第 1..D−1 層是翻板（第 k 層 2^(k−1) 片，初始全部朝左），第 D 層是 2^(D−1) 個袋子（左至右編號 1 起）。彈珠依翻板方向落下並把該翻板扳向另一側；穿過第 D−1 層後入袋。輸出第 I 顆球的袋號 | `curation/semantics014.py`（正本） |
| B1b | **球數可超過袋數**：機台狀態以 2^(D−1) 顆球為週期，bag(D, I) = bag(D, ((I−1) mod 2^(D−1)) + 1)，對任意 I 良定義。因此值域取 1 ≤ I ≤ 10,000,000（見 B4 的理由）；題面不得再寫「每顆球落入相異袋子」 | `semantics014.py` 說明＋交叉驗證（D=2..11 連跑 3 個週期，0 筆不符） |
| B2 | 三獨立實作（O(D) 奇偶直推／逐球全模擬／(I−1) 反向讀取）交叉驗證覆蓋 D=2..11 的整個週期與跨週期值，並含 D 至 20、I 取 {1, 2, 2^(D−1)−2, 2^(D−1)−1, 2^(D−1), 5,000,000, 9,999,999} 的抽樣，0 筆不符。D=4 落袋順序＝1,5,3,7,2,6,4,8 | `curation/semantics014.py` 與 apply 期交叉驗證腳本 |
| B3 | **op 成本模型（設計期賞金修正）**：op 計數器只數 line 事件（C2），逐球模擬可把整段下降攤平到同一行，實測**每球約 1 op**（一般寫法 4.158 ops/step、單行 while 1.105 ops/step，攤平版 ≈ 1 op/球）。因此門檻必須用**球數**而非步數 | `probe.mjs` 對 `curation/routes/r014_naive.py`／`r014_lean.py`／`r014_flat.py` |
| B4 | 舊值域（I ≤ 2^(D−1)）下 op 斷崖**數學上不可建**：單組球數上限 524,288 → 攤平版 ≈ 524K ops／組，需 19 組才過 C1；而收編的逐層計數解在第 5 組就跳閘 → 區間空集合。移除該上限（B1b）後，斷崖恢復：攤平版成本 ∝ 球數，逐層計數成本 ∝ 2^(D−1) 與球數無關，兩者可用「小 D、大球數」分離 | 設計期賞金 F5/F6；`probe.mjs` 實測 |
| B5 | 出貨階梯：第 1–14 筆總步數 ≤ 1,000,000（實際最大 994,999），任何逐球寫法皆可過；第 15–20 筆總球數 ≥ 20,000,000（實際最小 20,051,251）且總步數 ≤ 45,000,000（實際最大 40,985,330，用小 D 控制陣亡提交的牆鐘）→ 逐球模擬 = 14/20 | `curation/report014.json` |
| B6 | **實測三種逐球寫法全部 14/20**：一般寫法（最壞 2,526 ms、全場 23,061 ms）、單行 while 精簡版（5,021 ms／33,480 ms）、依 D 動態攤平的對抗版（5,066 ms／27,759 ms）——三者都在第 15–20 筆跳閘 | `probe.mjs` 對三支 `curation/routes/r014_*.py` |
| B7 | 陣亡提交的總牆鐘最壞 33,480 ms（node），對照 C4 的 120,000 ms 累計預算有 3.6 倍餘裕 → 不會觸發 C4b 的中斷呈現問題 | 同 B6 |
| B8 | **收編路線**（語義正確、必須維持 20/20）：L1 逐層計數（顯式 if/else 的最貴寫法，出貨最壞 3,932,655 ops／1,038 ms）、P1 先取週期再逐球模擬（最壞 4,683,393 ops／1,110 ms）。殺手筆因此受兩條斷言保護：逐層計數 op 模型 ≤ 8,000,000（取最貴寫法 5 ops/內圈）、單組「週期內球數」≤ 100,000 | `probe.mjs`；`plan014.py::LEVELWISE_OPS_CAP`／`PERIOD_BALL_CAP` |
| B9 | 零洞察／誤解路線出貨實測全數 0/20：Z1 原樣輸出球號、Z2 固定輸出 1、Z3 固定輸出最大袋號、E1 不做反向（等價於「讀取方向相反」）、E2 袋號 0-based、E3 輸出翻板編號、E4 奇偶方向相反、E5 多走一層、E6 只解第一組。第 1 筆（＝題面範例）額外斷言：必須讓 Z1/Z2/Z3/E1/E4/E5 當場現形 | `curation/plan014.py::CAPS` 與 entry 1 斷言、`report014.json` |
| B9b | 結構斷言（防退化資料）：每筆 ≥2 組、同筆不得有重複的 (D, I)（否則 memo 寫法對半砍成本）、每筆至少一組 I ≥ 2、每筆至少一組同時滿足 bag ≠ I、bag ≠ 1、bag ≠ 2^(D−1)、bag ≠ 週期內球號。**bag(I)=I ⟺ (I−1) 在 D−1 位下為回文**，出貨測資不得整筆由不動點組成 | `curation/plan014.py` 結構斷言區 |
| B10 | 出貨實測：`generator` 最壞 200 ops、`reference_solution` 最壞同量級（皆為 O(D)）；每筆測資 ≤ 50 bytes，`input_budget` 沿用預設 4096 即足 | `probe.mjs`、`report014.json` |

---

## V 表：出貨後量測

「離線」欄＝CPython 逐筆比對（`plan013.py`／`plan014.py`），「node-Pyodide」欄＝`curation/probe.mjs` 實測（含 op 上限與例外分類），「瀏覽器」欄＝dev 站 agent-browser 實際提交。

| ID | 路線 | 路線檔 | 題目 | 契約 | 離線 | node-Pyodide | 瀏覽器 |
|----|------|--------|------|------|------|--------------|--------|
| V1 | `reference_solution` | `ref013.py` | apcs013 | 20/20 | 20/20 ✓ | 最壞 37,537 ops ✓ | 20/20 ✓ |
| V2 | `reference_solution` | `ref014.py` | apcs014 | 20/20 | 20/20 ✓ | 最壞 200 ops ✓ | 20/20 ✓ |
| V3 | `.index()` 天真解（收編） | `routes/r013_indexnaive.py` | apcs013 | 20/20 | 20/20 ✓ | 最壞 25,036 ops ✓ | 20/20 ✓ |
| V4 | R1 鏡射解（收編） | `routes/r013_r1_mirror.py` | apcs013 | 20/20 | 20/20 ✓ | 最壞 77,609 ops ✓ | 20/20 ✓ |
| V5 | W1 模式盲 | `routes/r013_w1_modeblind.py` | apcs013 | 10/20 | 10/20 ✓ | — | 10/20 ✓ |
| V6 | W5 只讀一次模式標記 | `routes/r013_w5_markeronce.py` | apcs013 | 11/20 | 11/20 ✓ | — | 11/20 ✓ |
| V7 | W2 丙序取首元素 | `routes/r013_w2_postfirst.py` | apcs013 | ≤ 10/20 | 10/20 ✓ | — | 10/20 ✓ |
| V8 | W4 展開順序顛倒 | `routes/r013_w4_swaporder.py` | apcs013 | ≤ 10/20 | 10/20 ✓ | — | 10/20 ✓ |
| V9 | W11 形狀字典（零重建） | `routes/r013_w11_shapelib.py` | apcs013 | 2/20 | 2/20 ✓ | — | 2/20 ✓ |
| V10 | 逐球模擬（一般寫法） | `routes/r014_naive.py` | apcs014 | 14/20 | — | 14/20、全場 23,061 ms ✓ | 14/20 ✓ |
| V11 | 逐球模擬（單行精簡版） | `routes/r014_lean.py` | apcs014 | 14/20 | — | 14/20、全場 33,480 ms ✓ | 14/20 ✓ |
| V12 | 逐球模擬（攤平對抗版） | `routes/r014_flat.py` | apcs014 | 14/20 | — | 14/20、全場 27,759 ms ✓ | 14/20 ✓ |
| V13 | L1 逐層計數（收編） | `routes/r014_levelwise.py` | apcs014 | 20/20 | 20/20 ✓ | 最壞 3,932,655 ops ✓ | 20/20 ✓ |
| V14 | P1 取週期再模擬（收編） | `routes/r014_periodic.py` | apcs014 | 20/20 | 20/20 ✓ | 最壞 4,683,393 ops ✓ | 20/20 ✓ |
| V15 | E1 不做反向 | `routes/r014_e1_noreverse.py` | apcs014 | 0/20 | 0/20 ✓ | — | 0/20 ✓ |
| V16 | Z1 原樣輸出球號 | `routes/r014_z1_echo.py` | apcs014 | 0/20 | 0/20 ✓ | — | 0/20 ✓ |
| V17 | content-regression（兩題） | — | 兩題 | 全數一致 | 19 passed ✓ | — | 不適用 |
| V18 | challenge-params 冒煙 | — | 兩題 | 通過 | 73 passed ✓ | — | 不適用 |

---

## 賞金結果（設計期，I-1；10 條 lens × 對抗驗證）

| ID | 攻擊家族／缺陷 | 處置 | 落點 |
|----|----------------|------|------|
| F1 | apcs014 逐球模擬可攤平到每球 1 op（op 下界比原記錄低 21 倍） | 修：成本模型改用球數（B3） | `plan014.py::KILL_BALL_MIN`、`routes/r014_flat.py` |
| F2 | 舊值域下「收編逐層計數 ⇒ op 斷崖不可建」的結構性矛盾 | 修：移除 I ≤ 2^(D−1) 上限（B1b／B4） | `semantics014.py`、題面值域 |
| F3 | I = 2^(D−1) 是排列不動點（bag = I），零洞察路線白拿殺手筆 | 修：加入 Z1/Z2/Z3 路線與不動點結構斷言（B9／B9b） | `plan014.py` |
| F4 | 「D 層翻板 vs 2^(D−1) 個袋子」物理敘述自相矛盾，使 E5 變成題面 bug | 修：改寫為「第 1..D−1 層翻板、第 D 層袋子」（B1） | 題面、spec、SSOT |
| F5 | 題面範例落在邊界筆，與 `print(I)`／多走一層兩種誤讀相容 | 修：第 1 筆加 (4,11) 並加斷言「範例筆必須鑑別 Z/E 家族」 | `plan014.py` entry 1 斷言 |
| F6 | 殺手筆兩組測資完全相同，memo 寫法可對半砍成本 | 修：同筆禁止重複 (D, I)（B9b） | `plan014.py` |
| F7 | E4／E5 的上界過鬆、E5 的「每筆至少一組 I≥2」前提未寫成斷言 | 修：兩者收緊為 =0/20＋加結構斷言 | `plan014.py::CAPS` |
| F8 | B2 交叉驗證未覆蓋出貨極值 | 修：擴充到 D 至 20、含跨週期與近上限抽樣（B2） | `semantics014.py` 驗證腳本 |
| F9 | 收編路線的餘裕用最精簡寫法計算（方向錯誤） | 修：改用**最貴**合理寫法（顯式 if/else，5 ops/內圈）推導上限（B8） | `plan014.py::LEVELWISE_OPS_CAP` |
| F10 | 形狀字典路線（零重建）在出貨資料上得 5/20，斷言牆無此路線 | 修：收進 ROUTES、上界 2/20（僅範例筆），並把 entry 2/3/7/12 拉大（A6／A15） | `semantics013.py::route_W11_shapelib` |
| F11 | A10 以形狀「名稱」判多樣性；`spine` 在 n ≤ 120 退化成純左鏈 | 修：改用結構簽章＋非鏈斷言（A10） | `plan013.py`、`semantics013.py::sig` |
| F12 | 退化公式家族只守 4 選 2（缺照抄第一串／反轉第二串／降序） | 修：補 Z1/Z2/Z3 路線，上界皆 0/20（A6） | `semantics013.py` |
| F13 | 輸入無二義性（窮舉證否） | 採納為事實 A13 | SSOT |
| F14 | W7 ID 在文件與程式碼指兩條不同路線；W3／R1 未登記；V7 指向不存在的路線 | 修：改名 W5_markeronce、補登 W3／R1／W11／Z 家族、V 表重寫 | 本檔 A6／A12、design D5 |
| F15 | A9（鏡射不對稱）是 SSOT 宣稱但未實作的斷言 | 修：實作 `mirror_asym` 斷言（A9） | `plan013.py` |
| F16 | 模式 2 的左鏈組別對模式盲免疫，W1＝10/20 的守門機制未記錄 | 修：寫成事實 A14＋結構斷言 | 本檔、`plan013.py` |
| F17 | C4 累計硬砍在結果表格上可能呈現為全綠 | 記錄為 C4b＋以 B7 的牆鐘餘裕規避；引擎修正屬另案 | 本檔 C4b |
| F18 | `testcase_plan` literal 進入生產 bundle → 可離線算答案硬編碼 | **接受殘餘**：repo 本身公開，出貨測資輸入原已可見；apcs006／apcs009–012 同此，非本 change 新增。建議另開 change 處理（生產期遮蔽 literal 值＋私有測資），不以測資調整規避 | 本檔 C11 |
| F19 | A3 引用的 n=6000 極端輸入不存在於出貨資料且違反 A5／A8 | 修：降級為附註並標明「探針輸入、非出貨形狀」（A3） | 本檔 A3 |
| F20 | C5「逐字比對」過度描述（實為 trimEnd 容忍） | 修：改寫 C5 | 本檔 C5 |
| F21 | 小 n 範例筆（1／2／11／12）對窮舉形狀解毫無鑑別力 | 修：非範例筆最大 n 一律 ≥ 20，範例筆明記豁免（A15） | `plan013.py` |
| F22 | W4「左右岔顛倒」措辭有一種讀法是正確解 | 修：改寫為指向實作語義並註記對稱性屬收編（A6b） | 本檔 A6b |
