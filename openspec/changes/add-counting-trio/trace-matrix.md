# add-counting-trio 追溯矩陣

本檔是本 change 的**單一真相來源**。散文（題目頁、spec delta、design.md）一律由本矩陣派生，不得反向。

## 欄位說明

| 欄 | 內容 | 可否機械檢查 |
|---|---|---|
| **id** | fact id，全檔唯一 | ✓ |
| **主張** | 該事實的正式敘述。其中的每個數字都必須等於「證據」欄某個可解析位址的值 | 由「證據」欄反查 |
| **證據** | 可解析位址 ＋ 散文說明，格式見下 | ✓（位址部分） |
| **題目頁** | `docs/challenge/<slug>.md` 內該事實出現的位置 | **✗ — 見〈題目頁欄為何不可機械檢查〉** |
| **spec** | `openspec/changes/add-counting-trio/specs/counting-trio-challenges/spec.md` | ✓（`(trace X)` 標記） |
| **design** | `openspec/changes/add-counting-trio/design.md` | ✓（`(fact X)` 標記） |

### 證據欄格式（本次定案，不得更動）

證據欄可含**零個或多個可解析位址**，一律寫成 markdown code span，形如 **相對路徑#鍵路徑**（此處刻意不加 code span，以免被 lint 當成真位址）

- 路徑相對於本 change 根目錄（`openspec/changes/add-counting-trio/`）。例：`measure/routes015.json#spelling_worst_op_margin`
- 鍵路徑以**點號**走 dict、以**方括號**走 list。例：`measure/routes015.json#routes[0].max_ops`
- `.jsonl` 檔以 label 定位：`measure/browser-verification.jsonl#label=cellscan.score`
- **可解析位址的判定：code span 內含井字號。** 不含井字號的 code span 是識別字或裸檔名，不是位址、不參與檢查
- **純敘述性的出處**（訪談記錄、原始碼行號、指令 stdout）**不**寫成 code span，維持散文即可
- 同一格可混用位址與散文：位址負責說「值在哪」，散文負責說「為什麼這個值能證明主張」
- **加入或修改任何位址前，必須實際解析一次**，確認鍵存在且值等於主張欄引用的數字
- 某事實若目前只有指令 stdout 或原始碼行號可查，證據欄必須明寫「**無持久化輸出**」，並列入〈尚未有可解析位址的事實〉

### 題目頁欄為何不可機械檢查

題目頁**不得**帶 `(trace X)` / `(fact X)` 標記——把 fact id 印在學生看得到的地方等於洩題。因此題目頁欄一律維持散文，**不作為機械檢查的目標**。

這個方向已由 `verify/check_frontmatter_pair.py` 的 **E 檢查**反向覆蓋：題面內文的**每一個數字**都必須對得回某個 fact id，對不回即 exit non-zero。也就是說「fact → 題目頁」不查，「題目頁 → fact」查得比標記更嚴，覆蓋率不因此有缺口。

### spec 欄與 design 欄的三種值

- `✓` — 該事實**必須**在該文件中以標記引用（spec 用 `(trace X)`、design 用 `(fact X)`，X 為 fact id）
- `—` — 該事實**不得**出現在該文件
- `△` — 刻意不檢查，後面必須接一句括號理由

判準（決定某一格該填什麼時照這個問）：

- **spec ✓**：該事實構成**契約**——它規定了「出貨的東西必須是什麼樣子」，違反即為缺陷。I/O 契約、測資計畫、路線得分與 op 數、共用授權約束都屬此類。
- **design ✓**：該事實是**論證**的一部分——維護者決策、量測方法論、刻意偏離、殘餘風險、驗收條件。design.md 不複述每一個 op 數；那是 spec 的工作。
- **`—`**：該事實在該文件中沒有位置。這是**受檢查的**方向（文件出現該標記即 FAIL），不是放棄。
- **`△`**：唯一真正不受保護的格子。本矩陣目前**零個 △**。

檢查器：`scripts/trace-lint.py`（跨 change 重用）。`python3 scripts/trace-lint.py openspec/changes/add-counting-trio` 有任何 FAIL 即 exit 1。

## 使用規約

1. 三份文件中的**每一個數字**都必須能對回本矩陣的某個 fact id。對不回的數字視為缺陷。
2. 任何稽核輪次**先從本矩陣派生檢查項**，再去讀散文。直接讀散文找碴會重複踩到「改了 A 忘了同步 B」這個本專案反覆出現的失效模式。
3. 「證據」欄的可解析位址是唯一權威。修法方向恆為「**跑腳本 → 用輸出覆寫散文**」；**禁止「補資料去符合既有散文」**，也禁止把估算值寫進主張欄。
4. 修改任何一列，必須同時檢查「spec」與「design」欄列出的每一處，缺一即為不同步。
5. 新增事實時，若當下拿不出可解析位址，先列進〈尚未有可解析位址的事實〉並標明缺口，不得以散文冒充證據。

---

## D 段：維護者決策（無量測證據，出處為訪談記錄）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| D1 | 三題皆 `category: apcs`、`type: competition`，id 由 scaffold 配發 | 2026-08-15 訪談 Q1（訪談記錄，無持久化輸出） | frontmatter | ✓ | ✓ |
| D2 | apcs016 刻意不建成本斷崖，鑑別點為情境轉譯 | 訪談 Q2（訪談記錄，無持久化輸出） | — | ✓ | ✓ |
| D3 | apcs015 保留逐列輸出 `k=1..n` | 訪談 Q3（訪談記錄，無持久化輸出） | 輸出說明 | ✓ | ✓ |
| D4 | apcs015 標 `difficulty: easy`，題面附 `k=1..5` 答案表，**不說破** `2×3` 區塊 | 訪談 Q4（訪談記錄，無持久化輸出） | 難度、範例表 | ✓ | ✓ |
| D5 | apcs017 兌換率固定為十二，不由輸入給定 | 訪談 Q5（訪談記錄，無持久化輸出） | 情境 | ✓ | ✓ |
| D6 | 三題情境：基地台佈點規劃／跑馬燈顯示計數／園遊會代幣兌換；apcs017 避開「裝箱」用語（apcs009 已用） | 訪談 Q6（訪談記錄，無持久化輸出） | 全篇 | ✓ | ✓ |
| D7 | **apcs015 的 n 上界為 1000**（訪談原訂 3000）。理由見 E7 | 訪談後續裁決 2026-08-15（訪談記錄，無持久化輸出）；裁決結果落地於 `measure/routes015.json#n_max`，被推翻的原訂值登記為 `measure/nbound015.json#rejected_n`、決議值為 `measure/nbound015.json#decided_n` | 輸入說明 | ✓ | ✓ |

---

## C 段：跨題共用事實（平台契約與量測方法論）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| C1 | 判題器每筆測資 op 上限為 10,000,000 | 上限定義於原始碼 .vitepress/theme/\_\_tests\_\_/pyodide-worker-run-only.spec.ts:97 的 `DEFAULT_OP_LIMIT = 10_000_000`（原始碼行號，無持久化輸出）；本 change 全部量測沿用同一常數並各自登記：`measure/routes015.json#op_limit`、`measure/cellscan-ops.json#op_limit`、`measure/shipped-code-ops.json#op_limit`、`measure/routes016.json#op_cap`、`measure/routes017.json#op_limit_per_case` | — | ✓ | — |
| C2 | 判題器的 op 計數器**不過濾 event 型別、不過濾檔名，且 `return _tracer` 使巢狀呼叫也被追蹤** | 判題器實作見原始碼 .vitepress/theme/workers/worker-utils.ts:72-77 的 `_tracer`（原始碼行號，無持久化輸出）。忠實複刻於 `verify/judge_ops.py`；`python3 verify/judge_ops.py` 的 self_test 印 `inline=4,008／helper=10,009（比值 2.50）`——若複刻漏計 call/return，兩數會相近。**self_test 只印到 stdout，無持久化輸出** | — | ✓ | ✓ |
| C3 | op 數與執行速度無關，只與 bytecode 執行路徑有關；Pyodide 跑同一份 CPython bytecode，故本機 op 數**原封不動搬到瀏覽器**。牆鐘則否 | 原理見 `verify/judge_ops.py` 模組 docstring（散文）。同一路線（r015_rowscan.py、n=1000）的 op 數：主 harness 為 `measure/routes015.json#routes[1].max_ops`、獨立交叉驗證為 `verify/crosscheck.json#a015[1].max_ops`（兩者相同）。第三支為 `measure/nbound015.json#direct_at_decided_n.rowscan_plain`（該檔由 measure/opprobe_015_nbound.py --json 產生），其值與前兩者差 1——量測外殼的固定開銷不同，不是路線差異；故「三支工具量到同一個值」不成立，正確的說法是「兩支完全相同、第三支差一個常數」 | — | ✓ | ✓ |
| C4 | 冷／暖行程接縫：`import math` 在冷行程首次執行時會被 tracer 數到 **278 個 importlib 事件**。**文件數字一律取冷行程值**（op 上限逐筆套用，冷值才是上界） | `verify/judge_ops.count_ops_source_fresh` docstring（散文）；原記載實測同一路線行內第一次 299、行內第二次 21、新行程 299。**無持久化 json 輸出**——2026-08-15 直呼 `count_ops_source('import math\nprint(1)\n','')` 重跑得 285／7，差值同為 278（絕對值隨量測外殼而異，差值才是本列的主張） | — | ✓ | ✓ |
| C5 | 牆鐘一律**重複 7 次取最小值**。單發量測會抓到排程尖峰：上一輪曾量到「比同路線更大的 n 還慢一倍」的值，物理上不可能（該次觀察的絕對值只存在於過程紀錄，見證據欄） | `curation/plan015.py` 的 `WALL_REPS=7`（原始碼常數）；登記值為 `measure/routes015.json#wall_clock_reps` 與 `measure/routes015.json#wall_clock_statistic`。「上一輪曾量到 803 ms」為過程觀察，**無持久化輸出** | — | ✓ | ✓ |
| C6 | 全 literal 測資輸入會進入 client bundle 且公開於 repo。此為**專案層級既有殘留**，與 apcs009–014 共有，本 change 不處理 | proposal.md 的 Non-Goals 段（散文，無持久化輸出）；生產建置只剝除 `generator` 與 `reference_solution` | — | ✓ | ✓ |
| C7 | `assemble.py` 內建禁用術語掃描與答案洩漏掃描，命中即 exit non-zero 且**一份片段都不寫出** | 掃描器自我測試記錄於 `measure/assemble_report.json#scanner_self_test`；正常一輪的命中數為 `measure/assemble_report.json#challenges[0].banned_term_hits`（016 為 `measure/assemble_report.json#challenges[1].banned_term_hits`、017 為 `measure/assemble_report.json#challenges[2].banned_term_hits`），總表為 `measure/assemble_report.json#problems`。負向控制為指令輸出、**無持久化**：把 015 的 `algorithm` 改成 `factorial_count` → rc=1、印「命中禁用術語 ['factorial']」且三份片段 sha 完全未變；在來源 yaml 插入 `expected_outputs:` → rc=1 | — | ✓ | ✓ |
| C8 | 三題 literal 一律由斷言牆產生、由 `assemble.py` 逐位元組搬運，**禁止手改** | `measure/assemble_report.json#challenges[0].byte_identical_to_source`、`measure/assemble_report.json#challenges[1].byte_identical_to_source`、`measure/assemble_report.json#challenges[2].byte_identical_to_source` 與 `measure/assemble_report.json#challenges[0].matches_assertion_wall_entries`、`measure/assemble_report.json#challenges[1].matches_assertion_wall_entries`、`measure/assemble_report.json#challenges[2].matches_assertion_wall_entries` 六格皆為 true。另刪掉產物後重跑三支 `plan01*.py` 與 `assemble.py`，產出與 repo 版 `diff` 全同（指令輸出，**無持久化**） | — | ✓ | ✓ |

---

## E 段：apcs015 基地台佈點規劃（`ap-layout-plan`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| E1 | 第 k 列答案 = `k²(k²−1)/2 − 4(k−1)(k−2)`（k≥3；k<3 時減數為 0）。前 8 項 `0, 6, 28, 96, 252, 550, 1056, 1848` | `curation/semantics015.py` 內含**完全獨立**的慢速參照（攤平 k² 格、枚舉所有無序格子對、逐對檢查 8 種偏移），與封閉式在 k=1..30 逐項相符；獨立復現代理另以自寫枚舉驗到 k=22 全符。**兩者皆只印到 stdout，無持久化 json 輸出**（前 8 項數列在任何 json 中都查不到） | 範例表（僅前 5 項，見 D4） | ✓ | — |
| E2 | 20 筆 literal 為 `8,1,2,3,4,6,21,72,249,250,325,400,475,550,625,700,775,850,925,1000` | literal 正本為 `measure/routes015.json#entries`（逐項相符）。導出規則見 `curation/plan015.py` 的 `derive_entries()`（前 5 筆固定＋(6,249) 幾何 4 點＋(250,1000) 線性 11 點）；筆數為 `measure/routes015.json#entry_count`；獨立復現代理自行重寫導出規則得**逐項相同**（過程紀錄，無持久化） | 第 1 筆 = 範例 | ✓ | — |
| E3 | 首筆 = 8，與題面範例**逐位元組相同**，且四條錯誤路線在該筆全部當場現形 | 首筆內容為 `measure/routes015.json#entries[0]`（＝`measure/assemble_report.json#challenges[0].first_entry`）。四條 WRONG 路線在該筆皆 false：`measure/routes015.json#routes[5].per_entry_ok[0]`、`measure/routes015.json#routes[6].per_entry_ok[0]`、`measure/routes015.json#routes[7].per_entry_ok[0]`、`measure/routes015.json#routes[8].per_entry_ok[0]` | 範例 | ✓ | — |
| E4 | REFERENCE（O(n) 封閉式）20/20，最大 op 3,010，對上限的餘裕 3,322.26 倍 | 路線身分 `measure/routes015.json#routes[0].file`、得分 `measure/routes015.json#routes[0].score_n`（滿分為 `measure/routes015.json#entry_count`）、op 數 `measure/routes015.json#routes[0].max_ops`、餘裕 `measure/routes015.json#routes[0].op_margin_vs_limit`（分母為 `measure/routes015.json#op_limit`） | — | ✓ | — |
| E5 | O(n²) 逐列累加路線的**三種寫法全部 ACCEPTED、全部 20/20**：明寫迴圈 1,008,010 op、`sum(genexp)` 1,510,510 op、抽小函式 2,509,511 op | 明寫迴圈 `measure/routes015.json#routes[1].max_ops`、sum 產生器 `measure/routes015.json#routes[2].max_ops`、抽小函式 `measure/routes015.json#routes[3].max_ops`；得分 `measure/routes015.json#routes[1].score_n`、`measure/routes015.json#routes[2].score_n`、`measure/routes015.json#routes[3].score_n`（滿分為 `measure/routes015.json#entry_count`）。獨立交叉驗證見 `verify/crosscheck.json#a015[1].max_ops`（與主 harness 相同）；第三支工具的直測值差 1，詳見 C3 | — | ✓ | — |
| E6 | 最貴寫法的 op 餘裕為 **3.98 倍**（10,000,000 ÷ 2,509,511），由斷言 `E-1` 鎖住（要求 ≥ 3 倍） | 餘裕值 `measure/routes015.json#spelling_worst_op_margin`、門檻 `measure/routes015.json#spelling_op_margin_required`、分子 `measure/routes015.json#op_limit`、分母 `measure/routes015.json#routes[3].max_ops`；`python3 curation/plan015.py` 印「斷言牆全數通過」（指令輸出，**無持久化**） | — | ✓ | ✓ |
| E7 | **n 上界必須是 1000 而非 3000。** n=3000 時三種寫法為 9,051,479 活／13,567,551 死／22,561,127 死——同一演算法因寫法不同而生死不同（刀鋒）。n=1500 餘裕降至 1.77 倍，n=2000 起即出現刀鋒；n=1000 直接實測最貴 2,509,512 op、餘裕 3.98 倍 | 全列出自 `measure/nbound015.json`（由 `python3 measure/opprobe_015_nbound.py --json` 產生）：決議值 `measure/nbound015.json#decided_n`、被推翻的原訂值 `measure/nbound015.json#rejected_n`；n=3000 三種寫法的外推 op 為 `measure/nbound015.json#extrapolated["3000"].rowscan_plain`、`measure/nbound015.json#extrapolated["3000"].rowscan_sum`、`measure/nbound015.json#extrapolated["3000"].rowscan_helper`；n=1500 最貴寫法餘裕 `measure/nbound015.json#knife_edge["1500"].worst_margin`；候選 n 清單為 `measure/nbound015.json#candidates`，首次出現刀鋒的 n 為 `measure/nbound015.json#first_knife_edge_n`（同筆 `measure/nbound015.json#knife_edge["2000"].spellings_alive` 記活幾種寫法）；決議上界的直接實測為 `measure/nbound015.json#direct_worst_ops` 與 `measure/nbound015.json#direct_worst_margin`。成長階數（驗證確為二次）見 `measure/nbound015.json#baseline.rowscan_plain.growth_ratio` 等三筆。決議上界另落地於 `measure/routes015.json#n_max` | — | ✓ | ✓ |
| E8 | KILLED（O(n³) 逐格掃描 × 8 偏移）：瀏覽器實測 **8/20**，第 9 筆（n=249）起死亡、共 12 筆。**死因是 op 上限而非 deadline**：出貨路線檔在 n=72 為 **5,278,547** op（未超標），在 n=249 為 **216,759,740** op（**21.68×** 超標）；瀏覽器上 12 筆死亡耗時介於 **1,921** 與 **2,139** ms 且與 n 無關，那是燒完 op 預算的固定時間，不是 5,000 ms 的 deadline | 得分 `measure/browser-verification.jsonl#label=cellscan.score`（滿分為 `measure/browser-verification.jsonl#label=cellscan.rows`）、死亡筆數 `measure/routes015.json#routes[4].dead_entries`、deadline 為 `measure/routes015.json#deadline_ms`、逐筆判決 `measure/browser-verification.jsonl#label=cellscan.verdicts`、逐筆耗時 `measure/browser-verification.jsonl#label=cellscan.per_ms`。op 數為 `measure/cellscan-ops.json#rows[0].ops`（第 `measure/cellscan-ops.json#rows[0].entry` 筆、n＝`measure/cellscan-ops.json#rows[0].n`）與 `measure/cellscan-ops.json#rows[1].ops`（第 `measure/cellscan-ops.json#rows[1].entry` 筆、n＝`measure/cellscan-ops.json#rows[1].n`、超標倍數 `measure/cellscan-ops.json#rows[1].times_over_limit`），由 measure/cellscan_op_probe.py 對**出貨路線檔本身**量得（n=249 一筆需 18 秒，主 harness 的 op 量測會先撞硬逾時，故 `measure/routes015.json#routes[4].per_entry_ops[8]` 為 null——這正是先前這個數字只活在散文裡的原因）。更早記載的 175,342,739／4,262,386 量自一支未進 repo 的重寫探針，已作廢 | 效能提醒（不指名路線） | ✓ | ✓ |
| E9 | 四條 WRONG_ANSWER 得分 1／2／2／0：算成有序、忘記扣干擾對、`k<3` 守門寫反、迴圈 0 起算 | `measure/routes015.json#routes[5].score_n`、`measure/routes015.json#routes[6].score_n`、`measure/routes015.json#routes[7].score_n`、`measure/routes015.json#routes[8].score_n`（路線身分見同各筆的 `file` 鍵） | — | ✓ | — |
| E10 | UNCLEAN_DEATH（`math.factorial` 展開）：瀏覽器實測 **0/20**，20 筆全部顯示「未執行」。本機投影法給的 8/20 是**錯的**——它無法建模「worker 死亡並丟棄全部結果」。該路線本機只量到 577 op，計數器完全看不見它的成本 | 兩次瀏覽器實測皆 0（滿分為 `measure/browser-verification.jsonl#label=factorial015.rows`）：`measure/browser-verification.jsonl#label=factorial015.score` 與 `measure/browser-verification.jsonl#label=factorial015_rerun.score`；判決全為 `-`：`measure/browser-verification.jsonl#label=factorial015.verdicts` 與 `measure/browser-verification.jsonl#label=factorial015_rerun.verdicts`；耗時陣列為空：`measure/browser-verification.jsonl#label=factorial015.per_ms` 與 `measure/browser-verification.jsonl#label=factorial015_rerun.per_ms`。本機投影值為 `measure/routes015.json#routes[9].browser_projected_score_n`，該路線 op 數為 `measure/routes015.json#routes[9].max_ops`。結果面板文字為「0 / 20 通過」且每列標示「未執行」（人工觀察，**無持久化**） | — | ✓ | ✓ |
| E11 | 牆鐘對本題**不具鑑別力**，且**不得以兩位小數寫進規範層**。本機量測顯示計時被 process 啟動地板主導；瀏覽器量測顯示每條被接受的路線都遠在 deadline 之內。兩地的三種寫法排序**互不一致**（本機增量 rowscan > helper > sum，瀏覽器 helper > sum > plain），這本身就是「牆鐘不是穩定量」的證據 | 數值以 `measure/routes015.json#process_start_floor_cpython_ms`、`measure/routes015.json#routes[0].max_entry_algorithm_increment_cpython_ms`（REFERENCE）、`measure/routes015.json#routes[1].max_entry_algorithm_increment_cpython_ms`／`measure/routes015.json#routes[2].max_entry_algorithm_increment_cpython_ms`／`measure/routes015.json#routes[3].max_entry_algorithm_increment_cpython_ms`（三種寫法）與 `measure/routes015.json#spelling_wall_pct_of_deadline` 為準，瀏覽器值以 W2 為準。**這些鍵的值每次重跑 harness 都會變，任何文件不得複製其小數**——本 change 曾因此在 spec 寫下五個過期數字。斷言 E-3 守的是「性質」（地板主導、佔比 ≤ 25%）而非數值 | — | ✓ | ✓ |

---

## F 段：apcs016 跑馬燈顯示計數（`marquee-display-count`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| F1 | 答案 = `2^(n−k) mod 1000000007`；k=n 時為 1 | `curation/semantics016.py` 附「真的列舉所有畫面」的暴力參照，在 n ≤ 12 的**全部** (n,k) 組合相符；獨立復現代理以自寫列舉驗到 n=12 全符。**兩者皆只印到 stdout，無持久化 json 輸出** | 輸出說明 | ✓ | — |
| F2 | 20 筆 literal 首筆 `5 2`（答案 8），涵蓋 `k=0`、`k=n`、`n=1`、`n=1000000` | 首筆為 `measure/report016.json#per_entry[0].n` 與 `measure/report016.json#per_entry[0].k`，期望輸出 `measure/report016.json#per_entry[0].expected`（＝`measure/assemble_report.json#challenges[1].first_entry`）。涵蓋性：k>0 的筆數 `measure/report016.json#entries_k_pos`（餘 2 筆為 k=0）、k=n 的筆序 `measure/report016.json#k_eq_n_entries`、大 n 筆數 `measure/report016.json#entries_big_n`、n 上界 `measure/report016.json#max_n`、筆數 `measure/assemble_report.json#challenges[1].entry_count`。literal 正本為 `curation/out/frontmatter016.yaml` | 範例 | ✓ | — |
| F3 | REFERENCE（三參數 `pow`）與 A2（先算大整數再取餘數）各 20/20、最大 op 皆 **7**；A1（O(n) 迴圈）20/20、最大 op **2,000,009**，出現在 **entry 5 即 (1000000, 0)** | op 數 `measure/routes016.json#worst_traced_ops.REF_pow3`、`measure/routes016.json#worst_traced_ops.A2_bigint`、`measure/routes016.json#worst_traced_ops.A1_loop`；最壞筆身分 `measure/ops016.json#routes.A1_loop.worst_entry`（n＝`measure/ops016.json#routes.A1_loop.worst_entry_n`、k＝`measure/ops016.json#routes.A1_loop.worst_entry_k`）。得分 `measure/report016.json#scores.REF_pow3`、`measure/report016.json#scores.A1_loop`、`measure/report016.json#scores.A2_bigint`。op 來源為 `verify/judge_ops.py` | — | ✓ | — |
| F4 | 四條 WRONG_ANSWER 得分：忽略 k 得 2/20、把自由度看成 k 得 0/20、輸出 n−k 得 0/20、忘記取餘數得 6/20 | `measure/report016.json#scores.W1_ignore_k`、`measure/report016.json#scores.W2_use_k`、`measure/report016.json#scores.W3_plain_diff`、`measure/report016.json#scores.W4_nomod`；滿分為 `measure/assemble_report.json#challenges[1].entry_count`；同值另見 `measure/routes016.json#routes.W1_ignore_k.score` 等四筆 | — | ✓ | ✓ |
| F5 | 「忽略 k」無法歸零：契約強制涵蓋 `k=0`，而該路線在 `k=0` 時本來就對，故得 2/20。已把 `k>0` 的筆數推到 18 筆，即 `k=0` 只剩兩筆 | k>0 的筆數 `measure/report016.json#entries_k_pos`、總筆數 `measure/assemble_report.json#challenges[1].entry_count`（20 − 18 = 2 筆 k=0）、該路線得分 `measure/report016.json#scores.W1_ignore_k`；數學互斥，非資料瑕疵 | — | ✓ | ✓ |
| F6 | 「忘記取餘數」得 6/20：僅在 `n−k ≤ 29`（`2²⁹ < 1000000007`）的邊界筆正確，其餘各筆因整數轉字串位數上限拋 `ValueError` | 得分 `measure/report016.json#scores.W4_nomod`、滿分 `measure/assemble_report.json#challenges[1].entry_count`；該路線拋 `ValueError`（整數轉字串位數上限）的筆序為 `measure/report016.json#nomod_unprintable_entries`（9 筆），逐筆可列印旗標為 `measure/report016.json#per_entry[0].nomod_printable` 等 20 筆 | — | ✓ | — |

---

## G 段：apcs017 園遊會代幣兌換（`fair-token-exchange`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| G1 | 答案 = `min(v₂//2, v₃)`，其中 `v_p = Σ n//p^i`。`n=1..15` 為 `0,0,0,1,1,2,2,2,3,4,4,5,5,5,5` | `curation/semantics017.py` 附 `math.factorial` 反覆整除 12 的暴力參照，**逐一比對範圍**登記於 `measure/report017.json#brute_crosscheck_range`（＝n=1..299；見該檔第 17、99、101 行，`BRUTE_MAX_N = 400` 只是暴力函式的效能守門，非實際比對範圍）；獨立復現代理另以自寫實作驗到 n=199 全符。n=1..15 的數列**無持久化 json 輸出** | — | ✓ | — |
| G2 | 20 筆 literal 第 1 筆 `9`（答案 3），涵蓋 n=1、n=11、n=1000000000，且 ≥ 10⁸ 的有 5 筆 | 第 1 筆 `measure/report017.json#entries[0]`、答案 `measure/report017.json#expected[0]`（＝`measure/assemble_report.json#challenges[2].first_entry`）；全 20 筆見 `measure/report017.json#entries`；≥10⁸ 的筆數 `measure/report017.json#big_entries`、n 上界 `measure/report017.json#max_n`、筆數 `measure/assemble_report.json#challenges[2].entry_count`。literal 正本 `curation/out/frontmatter017.yaml`；`curation/plan017.py` 契約檢查（指令輸出，無持久化） | 範例 | ✓ | — |
| G3 | REFERENCE 與兩條 ACCEPTED 各 20/20，最大 op 155／156／166 | `measure/routes017.json#routes[0].max_ops`、`measure/routes017.json#routes[1].max_ops`、`measure/routes017.json#routes[2].max_ops`；得分 `measure/routes017.json#routes[0].score`、`measure/routes017.json#routes[1].score`、`measure/routes017.json#routes[2].score`（數值形式見 `measure/report017.json#scores.R_reference`，滿分為 `measure/assemble_report.json#challenges[2].entry_count`） | — | ✓ | — |
| G4 | 十進位尾零規則得 **2/20** | `measure/routes017.json#routes[3].score`（路線身分為同筆的 `file`＝r017_w1_decimal.py）；同值另見 `measure/report017.json#scores.W1_decimal_tail`，滿分為 `measure/assemble_report.json#challenges[2].entry_count` | — | ✓ | ✓ |
| G5 | 三條「取單邊」誤解路線得 11／11／**12**，**12/20 是本題結構允許的最低最高分**，無法再壓低 | 三筆得分 `measure/report017.json#scores.W2_forgot_half`、`measure/report017.json#scores.W3_only_v3`、`measure/report017.json#scores.W4_only_half_v2`（滿分為 `measure/assemble_report.json#challenges[2].entry_count`）。下界推導登記於 `measure/report017.json#guess_route_bound`，恆等式原文見 `measure/report017.json#guess_route_bound.why`（大意：只取 v₃ 與只取 v₂//2 的兩個得分之和，恆等於 20 加上平手筆數），其中 `measure/report017.json#guess_route_bound.identity_pair_sum`＝23、契約強制入列的平手筆 `measure/report017.json#guess_route_bound.forced_tie_entries`（n=1、11、10⁹，共 `measure/report017.json#guess_route_bound.tie_entries_in_plan` 筆）→ 較高者 ≥ ⌈23/2⌉ = `measure/report017.json#guess_route_bound.provable_best_max_score`。反事實（拿掉 n=11）下界為 `measure/report017.json#guess_route_bound.bound_without_n11` | — | ✓ | ✓ |
| G6 | `min(v₂, v₃)`（忘記每批十二枚需要兩個二）與「只取 v₃」**輸出恆等**，因 v₂ ≥ v₃ 對所有 n 成立，故無法獨立壓低 | 恆等旗標 `measure/report017.json#w2_w3_outputs_identical`；兩路線同分 `measure/report017.json#scores.W2_forgot_half` 與 `measure/report017.json#scores.W3_only_v3`。獨立代理對 n=1..4999 逐一驗證（過程紀錄，**無持久化**） | — | ✓ | — |
| G7 | UNCLEAN_DEATH（`math.factorial` 後反覆除以十二）：瀏覽器實測 **0/20**，與 E10 同型。本機記錄的 13/20 同樣是投影法的產物，非真實得分。最大 op 98,699（冷行程）＝上限的 0.99%，證明成本躲在 C 呼叫內、計數器看不見 | 瀏覽器得分 `measure/browser-verification.jsonl#label=factorial017.score`（滿分為 `measure/browser-verification.jsonl#label=factorial017.rows`）、判決 `measure/browser-verification.jsonl#label=factorial017.verdicts`（全為 `-`）；本機投影得分 `measure/routes017.json#routes[7].score`；op 數 `measure/routes017.json#routes[7].max_ops`、佔比 `measure/routes017.json#routes[7].max_ops_pct_of_limit` | — | ✓ | ✓ |
| G8 | 該路線在 n ≥ 10⁸ 於瀏覽器**必定不可行**，支柱是**記憶體**不是時間：n=10⁸ 的大整數本身即 314,159,123 bytes（約 300 MiB），n=10⁹ 為 3,556,832,228 bytes | n=10⁸ 為 `measure/routes017.json#memory_pillar.rows[2].bytes_of_bigint`（＝`measure/routes017.json#unclean_probe.extrapolated.100000000.bytes_of_bigint`，MiB 值 `measure/routes017.json#memory_pillar.rows[2].mib_of_bigint`）、n=10⁹ 為 `measure/routes017.json#memory_pillar.rows[3].bytes_of_bigint`，由 measure/routes017_measure.py 的 `bigint_footprint()` 產生、`measure/routes017.json#memory_pillar.deterministic` 為 true。時間外推**不作結論支柱**：同一份資料記錄的對數斜率為 `measure/routes017.json#unclean_probe.loglog_slope_central_from_minima`＝1.74、`measure/routes017.json#unclean_probe.loglog_slope_envelope`＝[1.72, 1.747]，區間本身即涵蓋約 1.6% 的離散度；先前記載的「1.769 vs 重跑 1.741，差 21%」在 repo 中查無出處，已作廢 | — | ✓ | — |

---

## B 段：建置期與自動化驗證（2026-08-15 關閉）

> 本段四列的證據全為指令 stdout，**無任何持久化 json 輸出**，因此都沒有可解析位址。見〈尚未有可解析位址的事實〉。

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| B1 | 三題 `reference_solution` 對**正式加密池**與 `generator` 輸出一致 | `pnpm build:pools`（71 池、0 失敗）後 `vitest --run scripts/content-regression.test.ts --reporter=verbose`：`ap-layout-plan` ✓ 346 ms、`marquee-display-count` ✓ 385 ms、`fair-token-exchange` ✓ 118 ms，各抽樣 20 個池索引。**指令輸出，無持久化** | — | ✓ | ✓ |
| B2 | 三題 `params` 宣告通過引擎守門 | `vitest --run scripts/challenge-params.test.ts` → 76 tests passed（該測試以掃全目錄方式涵蓋三題）。**指令輸出，無持久化** | — | — | ✓ |
| B5 | 三題題面**內文**通過禁用術語掃描 | `verify/check_frontmatter_pair.py` 的 D 檢查已進 repo 並沿用 `assemble.py` 的 `scan_banned`；另加棋類補掃。硬命中為零，唯一軟命中見 S6。**該腳本的 `--json` 只印到 stdout、未落檔，無持久化** | — | ✓ | — |
| B6 | 建置與既有測試無回歸 | `pnpm typecheck` 乾淨；`pnpm lint` 0 errors（21 個既有 warnings，皆不在本 change 觸及的檔案）；`vitest --run` 58 檔 **821 passed / 50 skipped**（基線 809 passed，+12 來自三題）。**指令輸出，無持久化** | — | — | ✓ |

---

## S 段：實際出貨碼（與 E/F/G 段的路線檔是**不同對象**）

E4／E5／F3／G3 描述的是 `curation/routes/` 底下的**學生路線檔**。隨題目出貨、實際會被判題鏈執行的是 frontmatter 內的 `generator` 與 `reference_solution`，兩者是重新拼寫的版本，op 數不等於路線表中的任何一筆。2026-08-15 的交叉驗證指出此追溯落差，故獨立成段。

> `verify/check_frontmatter_pair.py` 是本段大部分事實的量測器。2026-08-15 為它加上 `--json-out`，結果落成 `verify/frontmatter-pair.json`（F 檢查也一併納入），S1／S4／S5／S6／S9 因此才有可解析位址；在那之前這些數字只活在 stdout 裡。**修改本段任何數字前，先重跑 `python3 verify/check_frontmatter_pair.py --json-out`。**

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| S1 | 三題出貨碼的 `generator` 與 `reference_solution` 對各自 20 筆 literal，與 `curation/semantics0XX.py` 的獨立參照**三方完全相符** | `python3 verify/check_frontmatter_pair.py --json-out` → 三題各 20 筆全符：`verify/frontmatter-pair.json#apcs015.triple_ok`、`verify/frontmatter-pair.json#apcs016.triple_ok`、`verify/frontmatter-pair.json#apcs017.triple_ok`，rc=0。該腳本另做 7 項變異負向控制（改一位數字、gen 抄 ref、改 input_budget、非空 starter_code、內文插入禁用詞、插入無出處數字）全部 rc=1（指令輸出，無持久化） | — | ✓ | ✓ |
| S2 | 出貨碼 op 數（冷行程，20 筆取最大）：apcs015 為 6,008／2,005,018；apcs016 為 7／2,000,012；apcs017 為 154／164。全部在上限內，最緊的是兩題的 `reference_solution`，各佔 20.05% 與 20.00%，餘裕 4.99 與 5.00 倍 | apcs015：`measure/shipped-code-ops.json#challenges[0].programs.generator.max_ops`／`measure/shipped-code-ops.json#challenges[0].programs.reference_solution.max_ops`；apcs016：`measure/shipped-code-ops.json#challenges[1].programs.generator.max_ops`／`measure/shipped-code-ops.json#challenges[1].programs.reference_solution.max_ops`；apcs017：`measure/shipped-code-ops.json#challenges[2].programs.generator.max_ops`／`measure/shipped-code-ops.json#challenges[2].programs.reference_solution.max_ops`。佔比 `measure/shipped-code-ops.json#challenges[0].programs.reference_solution.max_ops_pct_of_limit` 與 `measure/shipped-code-ops.json#challenges[1].programs.reference_solution.max_ops_pct_of_limit`；餘裕 `measure/shipped-code-ops.json#challenges[0].programs.reference_solution.margin_x` 與 `measure/shipped-code-ops.json#challenges[1].programs.reference_solution.margin_x`。全表由 `verify/measure_shipped_code.py` 產生 | — | ✓ | — |
| S3 | 三題的 `generator` 與 `reference_solution` 走**不同推導路徑**：apcs015 為封閉式 vs 逐列累加；apcs016 為次方運算取餘數 vs 反覆加倍累乘；apcs017 為遞增門檻累加 vs 反覆 divmod | 三份題目頁 frontmatter；`check_frontmatter_pair.py` 的 A′ 檢查確認兩者非同一份程式碼。apcs016 原為同一推導的兩種拼寫（`pow(2,e,MOD)` vs `2**e % MOD`），已於交叉驗證後改寫（A′ 檢查結果為布林，不落數字） | — | ✓ | ✓ |
| S4 | 四鍵（`algorithm`／`params`／`input_budget`／`testcase_plan`）與 `curation/out/frontmatter0XX.yaml` **逐位元組相同**：apcs015 為 599 bytes、apcs016 為 791 bytes、apcs017 為 651 bytes | `check_frontmatter_pair.py` 的 B 檢查，另以 `yaml.safe_load` 解析後二次比對。位元組數為 `verify/frontmatter-pair.json#apcs015.four_key_bytes_n`、`verify/frontmatter-pair.json#apcs016.four_key_bytes_n`、`verify/frontmatter-pair.json#apcs017.four_key_bytes_n`（相同與否見同筆的 `four_key_identical`）。四鍵清單另可對 `measure/assemble_report.json#challenges[0].keys` | — | — | ✓ |
| S5 | 三題題面內文的**每一個數字**都能對回本矩陣的 fact id：apcs015 有 81 個（17 種）、apcs016 有 53 個（8 種）、apcs017 有 97 個（13 種），對不回者為零 | `check_frontmatter_pair.py` 的 E 檢查，逐一列出數字與其 fact id。個數為 `verify/frontmatter-pair.json#apcs015.numbers.total`／`verify/frontmatter-pair.json#apcs015.numbers.distinct_count`、`verify/frontmatter-pair.json#apcs016.numbers.total`／`verify/frontmatter-pair.json#apcs016.numbers.distinct_count`、`verify/frontmatter-pair.json#apcs017.numbers.total`／`verify/frontmatter-pair.json#apcs017.numbers.distinct_count`；對不回的筆數為三筆 `numbers.unmatched_count`（例：`verify/frontmatter-pair.json#apcs015.numbers.unmatched_count`） | — | ✓ | ✓ |
| S6 | 三題全頁禁用術語掃描零硬命中。唯一軟命中為 apcs016 的「馬」×2，出自情境名詞「跑馬燈」，**判定為誤報** | `check_frontmatter_pair.py` 的 D 檢查（沿用 `assemble.py` 的 `scan_banned`），詞庫大小為 `measure/assemble_report.json#banned_terms_count.en`（66 條）與 `measure/assemble_report.json#banned_terms_count.zh`（49 條）；組裝期零命中見 `measure/assemble_report.json#challenges[1].banned_term_hits`。全頁補掃的「馬」×2 為 `verify/frontmatter-pair.json#apcs016.banned.soft_full`（apcs015 與 apcs017 的同欄為空陣列） | — | ✓ | — |
| S7 | apcs015 題面的效能提醒寫「超出單筆測資的**執行量上限**」。**先前寫成「時間限制」是錯的**：E8 證明該路線死於 op 上限。措辭刻意不指名是哪一種限制的細節，避免洩漏系統以什麼為成本軸 | 措辭本體在 docs/challenge/ap-layout-plan.md 的提醒段（散文，無持久化輸出）；依據為 E8 的瀏覽器實測與 op 量測（位址見 E8 列） | 效能提醒 | ✓ | ✓ |
| S8 | apcs016 的 `params` 宣告 `min: 0`，與題面宣告的 `1 <= n` 不一致。因 `nk` 為單一參數帶 `count: 2`、n 與 k 共用值域，下界取聯集。三題 `testcase_plan` 全為 literal，band 不會被使用，判題無影響；若日後改用 band 會現形 | 宣告值 `measure/assemble_report.json#challenges[1].params.nk.min`（＝0），同筆 `measure/assemble_report.json#challenges[1].params.nk.count` 記 `count: 2`；正本為 `curation/out/frontmatter016.yaml`。交叉驗證代理的裁決建議 4（過程紀錄，無持久化）。四鍵已凍結，未更動 | — | — | ✓ |
| S9 | 三題 frontmatter 的**欄位集合一致**：皆具備 `layout`／`id`／`title`／`difficulty`／`category`／`type`／`tags`／`description`／`algorithm`／`params`／`input_budget`／`testcase_plan`／`generator`／`reference_solution`／`starter_code` 十五個鍵，無一題多鍵或少鍵，且 `tags` 三題皆非空 | `verify/check_frontmatter_pair.py` 的 F 檢查（逐題比對鍵集合並拒絕空 `tags`），鍵數與一致性登記於 `verify/frontmatter-pair.json#frontmatter_fields.required_key_count`、`verify/frontmatter-pair.json#frontmatter_fields.key_sets_identical`，逐題鍵數見 `verify/frontmatter-pair.json#frontmatter_fields.per_challenge.apcs017.key_count`、`tags` 非空見同筆的 `tags_nonempty`。此列因 2026-08-15 稽核發現 apcs017 的 `tags` 為空陣列而新增——矩陣先前完全未追蹤 `tags`，是覆蓋缺口而非單一筆誤 | frontmatter | — | ✓ |

---

## W 段：瀏覽器實測（2026-08-15，`pnpm preview:cf` 於 localhost:8788，COOP `same-origin` ＋ COEP `require-corp` 已確認送出）

本段是本 change **唯一無法在本機證明**的部分。它推翻了三條先前以「本機量測 + 投影」得出的結論（E8 的死因、E10 與 G7 的得分），這正是它存在的理由。

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| W1 | 三題 `reference_solution` 在真實 Pyodide 各 **20/20**。單筆最大牆鐘：apcs015 為 375 ms、apcs016 為 441 ms（**三題中最緊**）、apcs017 為 8 ms；三題 deadline 皆 5,000 ms，故最緊的一題也還有一個數量級的餘裕 | 得分 `measure/browser-verification.jsonl#label=ref015.score`、`measure/browser-verification.jsonl#label=ref016.score`、`measure/browser-verification.jsonl#label=ref017.score`；最大牆鐘 `measure/browser-verification.jsonl#label=ref015.max_ms`、`measure/browser-verification.jsonl#label=ref016.max_ms`、`measure/browser-verification.jsonl#label=ref017.max_ms`。滿分為 `measure/browser-verification.jsonl#label=ref015.rows`；deadline 為 `measure/routes015.json#deadline_ms`、`measure/routes016.json#deadline_ms`、`measure/routes017.json#deadline_ms_per_case`（皆 5000 ms） | — | — | ✓ |
| W2 | apcs015 的三種 O(n²) 寫法在真實 Pyodide **全部 20/20**，單筆最大 269／335／706 ms。**這是 n 上界下修為 1000 的決定性驗證**——刀鋒確實消除 | 得分 `measure/browser-verification.jsonl#label=rowscan_plain.score`、`measure/browser-verification.jsonl#label=rowscan_sum.score`、`measure/browser-verification.jsonl#label=rowscan_helper.score`；n 上界 `measure/routes015.json#n_max`；最大牆鐘 `measure/browser-verification.jsonl#label=rowscan_plain.max_ms`、`measure/browser-verification.jsonl#label=rowscan_sum.max_ms`、`measure/browser-verification.jsonl#label=rowscan_helper.max_ms` | — | ✓ | ✓ |
| W3 | `math.factorial` **本身可以**被 deadline 乾淨中斷。有界變體（`n > 200000` 時改走正解）在第十四筆（n=65610）得乾淨 TLE、**5,041 ms**，全體 19/20。昂貴的不是 `factorial(65610)` 本身（該次計時見證據欄），而是其後的整除迴圈，那是 bytecode 層級 | 判決字串 `measure/browser-verification.jsonl#label=probe_factorial_small.verdicts`（第 14 位為 `T`）、該筆耗時 `measure/browser-verification.jsonl#label=probe_factorial_small.per_ms[13]`、總分 `measure/browser-verification.jsonl#label=probe_factorial_small.score`（滿分為 `measure/browser-verification.jsonl#label=probe_factorial_small.rows`）；第 14 筆的 n 為 `measure/report017.json#entries[13]`。探針本體為 measure/solutions/probe_factorial_small.py。「`factorial(65610)` 本身僅約 0.07 秒」為過程觀察，**無持久化**（故不寫進主張欄） | — | ✓ | ✓ |
| W4 | 真正殺死 worker 的是**巨大參數的單一 C 呼叫**（例如 n=10⁸ 的 factorial），它永遠不返回、中斷旗標永遠檢查不到。後果是**整份提交的 20 筆結果全部被丟棄**，學生看到 0/20 全「未執行」，**沒有部分分數** | 本列為 E10／G7 與 W3 的對照推論，自身無獨立量測：對照組位址見 `measure/browser-verification.jsonl#label=factorial015.score`（滿分為 `measure/browser-verification.jsonl#label=factorial015.rows`）、`measure/browser-verification.jsonl#label=factorial017.score`（皆 0）與 `measure/browser-verification.jsonl#label=probe_factorial_small.score`（19）——同一支 `math.factorial`，參數有界時乾淨判 TLE、無界時全盤皆墨 | — | ✓ | ✓ |
| W5 | 分頁與 worker **會復原**：不乾淨死亡後緊接著提交正解，立刻回到 20/20。2026-08-15 的 e2e 補測以**同一題**的死亡→復原序列驗證，不再倚賴跨題推論 | 同題序列：`measure/browser-verification.jsonl#label=factorial017_pre_recovery.score`（0，該筆 `measure/browser-verification.jsonl#label=factorial017_pre_recovery.rows` 為 20 且判定全空）緊接 `measure/browser-verification.jsonl#label=ref017_recovered_after_017.score`（20，`measure/browser-verification.jsonl#label=ref017_recovered_after_017.max_ms` 為 6 ms）。另有兩筆較早的跨題觀察 `measure/browser-verification.jsonl#label=ref015_after_unclean.score`（20）與 `measure/browser-verification.jsonl#label=ref017_after_unclean.score`（20）。**更正紀錄**：本列先前宣稱的 `factorial017_pre_recovery` 在當時的 jsonl 中並不存在（該次量測用 `tail` 而非 `tee`，輸出未落盤），為 2026-08-15 稽核抓到的缺陷；現已實際補測入庫 | — | ✓ | ✓ |
| W6 | `import math` 本身不被沙箱守衛阻擋 | `measure/browser-verification.jsonl#label=probe_import_math.score`（20）與 `measure/browser-verification.jsonl#label=probe_import_math.max_ms`（4.0 ms）。此為排除 E10／G7 之 0/20 另有他因的對照實驗；探針本體為 measure/solutions/probe_import_math.py | — | — | ✓ |
| W7 | **e2e 使用者旅程全綠**：列表頁列出全部 apcs id 且三題標題皆在；三個 `/c/` 短網址別名皆以轉址碼導向正確的 `/challenge/<slug>` 並在跟隨後回 200；三個題目頁皆回 200 且洩題詞彙（`2×3`、`3×2`、`騎士`、`棋`）**零命中**；三題正解在 e2e 重測各得滿分 | 可機械化觀察見 `measure/e2e-smoke.json#listing.apcs_ids_found`、同檔 `measure/e2e-smoke.json#aliases[0].redirect_status`、`measure/e2e-smoke.json#aliases[0].followed_status`、`measure/e2e-smoke.json#problems`（空陣列即全數通過）；提交結果見 `measure/browser-verification.jsonl#label=e2e_ref016.score` 與 `measure/browser-verification.jsonl#label=e2e_ref017.score`。apcs015 另以互動方式走完全程（貼入正解、點「提交」），結果面板讀出「20 / 20 通過」且 20 列判定全為 AC，並確認 id 徽章、難度顯示「簡單」、偏移表含「列差」「行差」、小規模答案表齊備、效能提醒措辭為「執行量上限」（S7）。**牆鐘值刻意不寫入本列**，理由見 E11 | 全篇 | — | ✓ |
| W8 | **`preview:cf` 不會產生 `_redirects`**，因此本機預覽時所有 `/c/` 短網址一律 404。這是預覽腳本的保真度缺口，**不是生產缺陷**：`preview:cf` 只跑 `docs:build`，完整的 `pnpm build` 才含 `build:redirects`，而 Cloudflare Pages 跑的是完整 build | `package.json` 的 `preview:cf` 與 `build` 兩條 script 的差異。對照實驗：既有的 `/c/apcs013`、`/c/apcs014`、`/c/py001` 在同一個預覽站台起初為 200 而三個新 id 為 404，手動跑過 `pnpm build:redirects` 並同步進 dist 後三者皆正常，證明差異來自產物新舊而非題目本身。`docs/public/_redirects` 為 gitignored 建置產物（`.gitignore:76`），故不隨本 change 進版控 | — | — | ✓ |

---

## 尚未有可解析位址的事實

以下事實**目前沒有**任何可解析位址可查，數字只活在指令 stdout、原始碼行號或訪談記錄裡。它們是下一支追溯 lint 的已知盲區，補齊方式一律是「讓既有腳本把結果落成 json」，**不是**把數字抄進更多散文。

| 事實 | 缺什麼 | 補法 |
|---|---|---|
| C2（self_test 的 4,008／10,009／2.50）、C4（278 事件與 299／21／299） | `verify/judge_ops.py` 的 self_test 只印 stdout | self_test 落成 `measure/judge-ops-selftest.json` |
| B1／B2／B5／B6 全段 | 建置與 vitest 的輸出未留存 | 將關鍵行數／耗時落成 `measure/build-verification.json` |
| E1（前 8 項數列）、F1（n ≤ 12 全組合）、G1（`n=1..15` 數列） | `curation/semantics01*.py` 的交叉驗證只印 stdout | 三支 `semantics01*.py` 加 `--json`，落成各自的 crosscheck 檔 |
| G5／G6 的「獨立代理對 n=1..4999 逐一驗證」 | 該次驗證只留過程紀錄 | 併入 `semantics017.py` 的 `--json`，把驗證範圍寫成鍵 |
| D 段全部 | 本質為維護者決策，無外部真值 | 不補。只能檢查「有沒有被引用」，不能檢查「對不對」 |

2026-08-15 已關閉的缺口（原本列在本表，現已有位址）：**E7 全列**與 **C3 的第三支工具**（`measure/opprobe_015_nbound.py --json` → `measure/nbound015.json`）；**S1／S4／S5／S6／S9**（`verify/check_frontmatter_pair.py --json-out` → `verify/frontmatter-pair.json`，F 檢查已納入）。

### 因查無出處而從主張欄刪去的數字

方向是「跑腳本 → 用輸出覆寫散文」，找不到出處的數字一律移出主張欄，**不補資料去遷就它**。以下五個數字經此處理，其中三個已被有出處的量取代：

| 原數字 | 所在列 | 處置 |
|---|---|---|
| 上限的 0.030% | E4 | json 無此鍵，改用有鍵的 `op_margin_vs_limit`＝3,322.26 倍；spec 同步改寫 |
| 死亡耗時「一律約 1,950 ms」 | E8 | 實測 12 筆落在 1,921–2,139 ms（中位數才是 1,951），改寫成實際區間；spec 同步改寫 |
| 「其中 4 筆是契約強制入列」 | F6 | `measure/report016.json` 查無對應鍵，整句刪去；spec 同步刪去 |
| deadline 餘裕 13.3／11.3／625 倍 | W1 | 倍數無鍵，改寫成「最大牆鐘 ＋ deadline」兩個有鍵的量 |
| 單發牆鐘 803 ms、`factorial(65610)` 約 0.07 秒 | C5、W3 | 純過程觀察，移到證據欄留存，不再出現在主張欄 |

## 尚未取得證據的事實

**目前為空。** B1／B2／B5／B6 由建置期驗證關閉（B 段），B3／B4 由瀏覽器實測關閉並在過程中推翻了三條先前結論（W 段）。

本區塊保留不刪：任何後續變更若引入無證據的主張，必須先列在這裡，且三份文件在證據補齊前不得宣稱其成立。
