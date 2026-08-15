# add-counting-trio 追溯矩陣

本檔是本 change 的**單一真相來源**。散文（題目頁、spec delta、design.md）一律由本矩陣派生，不得反向。

**使用規約**

1. 三份文件中的**每一個數字**都必須能對回本矩陣的某個 fact id。對不回的數字視為缺陷。
2. 任何稽核輪次**先從本矩陣派生檢查項**，再去讀散文。直接讀散文找碴會重複踩到「改了 A 忘了同步 B」這個本專案反覆出現的失效模式。
3. 「證據」欄必須寫到**跑什麼指令、看到什麼值**的程度。只寫檔名不算證據。
4. 修改任何一列，必須同時檢查「位置」欄列出的每一處，缺一即為不同步。

**欄位說明**

- **題目頁** = `docs/challenge/<slug>.md`
- **spec** = `openspec/changes/add-counting-trio/specs/counting-trio-challenges/spec.md`
- **design** = `openspec/changes/add-counting-trio/design.md`
- `—` 表示該事實不應出現在該文件（例如鑑別點細節不得進題目頁，否則洩題）

---

## D 段：維護者決策（無量測證據，出處為訪談記錄）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| D1 | 三題皆 `category: apcs`、`type: competition`，id 由 scaffold 配發 | 2026-08-15 訪談 Q1 | frontmatter | 共用授權約束 | 決策表 Q1 |
| D2 | apcs016 刻意不建成本斷崖，鑑別點為情境轉譯 | 訪談 Q2 | — | 016 成本階梯 | 決策表 Q2、刻意偏離 2 |
| D3 | apcs015 保留逐列輸出 k=1..n | 訪談 Q3 | 輸出說明 | 015 I/O 契約 | 決策表 Q3 |
| D4 | apcs015 標 `difficulty: easy`，題面附 k=1..5 答案表，**不說破** 2×3 區塊 | 訪談 Q4 | 難度、範例表 | 共用授權約束 | 決策表 Q4、刻意偏離 1 |
| D5 | apcs017 兌換率固定為 12，不由輸入給定 | 訪談 Q5 | 情境 | 017 I/O 契約 | 決策表 Q5 |
| D6 | 三題情境：基地台佈點規劃／跑馬燈顯示計數／園遊會代幣兌換；017 避開「裝箱」用語（apcs009 已用） | 訪談 Q6 | 全篇 | — | 決策表 Q6 |
| D7 | **apcs015 的 n 上界為 1000**（原訂 3000）。理由見 E7 | 訪談後續裁決 2026-08-15 | 輸入說明 | 015 I/O 契約 | 決策表 Q7、E7 |

---

## C 段：跨題共用事實（平台契約與量測方法論）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| C1 | 判題器每筆測資 op 上限為 10,000,000 | `.vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts:97` 的 `DEFAULT_OP_LIMIT = 10_000_000` | — | 成本階梯 | 量測方法論 |
| C2 | 判題器的 op 計數器**不過濾 event 型別、不過濾檔名，且 `return _tracer` 使巢狀呼叫也被追蹤** | `.vitepress/theme/workers/worker-utils.ts:72-77` 的 `_tracer`。忠實複刻於 `verify/judge_ops.py`；`python3 verify/judge_ops.py` 的 self_test 印 `inline=4,008／helper=10,009（比值 2.50）`——若複刻漏計 call/return，兩數會相近 | — | — | 量測方法論 |
| C3 | op 數與執行速度無關，只與 bytecode 執行路徑有關；Pyodide 跑同一份 CPython bytecode，故本機 op 數**原封不動搬到瀏覽器**。牆鐘則否 | `verify/judge_ops.py` 模組 docstring；三支獨立工具（`plan015.py`、`crosscheck_trio.py`、`opprobe_015_nbound.py`）在 n=1000 對同一路線量到同一個 1,008,010 | — | 成本階梯 | 量測方法論、殘餘風險 |
| C4 | 冷／暖行程接縫：`import math` 在冷行程首次執行時會被 tracer 數到 **278 個 importlib 事件**。**文件數字一律取冷行程值**（op 上限逐筆套用，冷值才是上界） | `verify/judge_ops.count_ops_source_fresh` docstring；實測同一路線行內第一次 299、行內第二次 21、新行程 299 | — | — | 量測方法論 |
| C5 | 牆鐘一律**重複 7 次取最小值**。單發量測會抓到排程尖峰——上一輪曾量到 803 ms，比同路線更大的 n 還慢一倍，物理上不可能 | `plan015.py` 的 `WALL_REPS=7`；`measure/routes015.json` 的 `wall_clock_reps` / `wall_clock_statistic` | — | — | 量測方法論 |
| C6 | 全 literal 測資輸入會進入 client bundle 且公開於 repo。此為**專案層級既有殘留**，與 apcs009–014 共有，本 change 不處理 | `proposal.md` Non-Goals；生產建置只剝除 `generator` 與 `reference_solution` | — | 共用授權約束 | 範圍界線 |
| C7 | `assemble.py` 內建禁用術語掃描與答案洩漏掃描，命中即 exit non-zero 且**一份片段都不寫出** | 把 015 的 `algorithm` 改成 `factorial_count` → rc=1、印「命中禁用術語 ['factorial']」且三份片段 sha 完全未變；在來源 yaml 插入 `expected_outputs:` → rc=1 | — | 共用授權約束 | 交付物 |
| C8 | 三題 literal 一律由斷言牆產生、由 `assemble.py` 逐位元組搬運，**禁止手改** | 刪掉產物後重跑三支 `plan01*.py` 與 `assemble.py`，產出與 repo 版 `diff` 全同 | — | 各題測資計畫 | 交付物 |

---

## E 段：apcs015 基地台佈點規劃（`ap-layout-plan`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| E1 | 第 k 列答案 = `k²(k²−1)/2 − 4(k−1)(k−2)`（k≥3；k<3 時減數為 0）。前 8 項 `0, 6, 28, 96, 252, 550, 1056, 1848` | `curation/semantics015.py` 內含**完全獨立**的慢速參照（攤平 k² 格、枚舉所有無序格子對、逐對檢查 8 種偏移），與封閉式在 k=1..30 逐項相符；獨立復現代理另以自寫枚舉驗到 k=22 全符 | 範例表（僅前 5 項，見 D4） | I/O 契約 | — |
| E2 | 20 筆 literal 為 `8,1,2,3,4,6,21,72,249,250,325,400,475,550,625,700,775,850,925,1000` | `curation/plan015.py` 的 `derive_entries()` 機械導出（前 5 筆固定＋(6,249) 幾何 4 點＋(250,1000) 線性 11 點）；獨立復現代理自行重寫導出規則得**逐項相同** | 第 1 筆 = 範例 | 測資計畫 | — |
| E3 | 第 1 筆 = 8，與題面範例**逐位元組相同**，且四條錯誤路線在該筆全部當場現形 | `measure/routes015.json` 各 WRONG 路線 `per_entry_ok[0]` 皆 false | 範例 | 測資計畫 | — |
| E4 | REFERENCE（O(n) 封閉式）20/20，最大 op 3,010＝上限的 0.030% | `measure/routes015.json` `r015_ref_formula.py`：`score 20/20`、`max_ops 3010` | — | 成本階梯 | 量測表 |
| E5 | O(n²) 逐列累加路線的**三種寫法全部 ACCEPTED、全部 20/20**：明寫迴圈 1,008,010 op、`sum(genexp)` 1,510,510 op、抽小函式 2,509,511 op | `measure/routes015.json` 三筆 `r015_rowscan*.py`；三支獨立工具量到相同值 | — | 成本階梯 | 量測表 |
| E6 | 最貴寫法的 op 餘裕為 **3.98 倍**（10,000,000 ÷ 2,509,511），由斷言 E-1 鎖住（要求 ≥ 3 倍） | `curation/plan015.py` 的 `spelling_worst_op_margin`；`python3 curation/plan015.py` 印「斷言牆全數通過」 | — | 成本階梯 | 量測表、殘餘風險 |
| E7 | **n 上界必須是 1000 而非 3000。** n=3000 時三種寫法為 9,051,479 活／13,567,551 死／22,561,127 死——同一演算法因寫法不同而生死不同（刀鋒）。n=1500 餘裕降至 1.77 倍，n=2000 起即出現刀鋒 | `measure/opprobe_015_nbound.py`：成長階數實測 3.98/3.98/3.99（符合二次），逐候選外推＋n=1000 直接實測 | — | I/O 契約 | 決策表 Q7、刻意偏離 1 |
| E8 | KILLED（O(n³) 逐格掃描 × 8 偏移）：瀏覽器實測 **8/20**，第 9 筆（n=249）起死亡、共 12 筆。**死因是 op 上限而非 deadline**：出貨路線檔 `curation/routes/r015_cellscan.py` 在 n=72 為 **5,278,547** op（過），在 n=249 為 **216,759,740** op（**21.68×** 超標）；瀏覽器上 12 筆死亡耗時一律約 1,950 ms 且**與 n 無關**，那是燒完 10,000,000 op 的固定時間，不是 5,000 ms 牆鐘 | `measure/browser-verification.jsonl` 的 `cellscan`：`score 8`、`verdicts AAAAAAAATTTTTTTTTTTT`、`per_ms` 第 9 筆起 1952/1990/1951/1972/2139/…；op 由 `verify/judge_ops.count_ops_source_fresh` 對**路線檔本身**量得，n=72 之值與 `measure/routes015.json` 的 `per_entry_ops[7]` 相符。先前記載的 175,342,739／4,262,386 量自一支未進 repo 的重寫探針而非出貨路線檔，已作廢 | 效能提醒（不指名路線） | 成本階梯 | 量測表 |
| E9 | 四條 WRONG_ANSWER 得分 1／2／2／0：算成有序、忘記扣干擾對、k<3 守門寫反、迴圈 0 起算 | `measure/routes015.json` 四筆 `r015_w*.py` | — | 誤解路線鑑別 | 量測表 |
| E10 | UNCLEAN_DEATH（`math.factorial` 展開）：瀏覽器實測 **0/20**，20 筆全部顯示「未執行」。本機投影法給的 8/20 是**錯的**——它無法建模「worker 死亡並丟棄全部結果」 | `measure/browser-verification.jsonl` 的 `factorial015` 與 `factorial015_rerun`（兩次皆 `score 0`、`verdicts` 全為 `-`、`per_ms` 為空）；結果面板文字為「0 / 20 通過」且每列標示「未執行」 | — | 成本階梯（列為已知殘留） | 刻意偏離 3、殘餘風險 |
| E11 | 牆鐘對本題**不具鑑別力**：process 啟動地板 14.53 ms，REFERENCE 的演算法增量僅 0.86 ms，三種 O(n²) 寫法佔 deadline 的 4.62%／3.18%／5.01% | `measure/routes015.json` 的 `process_start_floor`、`per_entry_algorithm_increment_cpython_ms`、逐路線 `wall_clock_note`；斷言 E-3 在此性質改變時會叫 | — | 成本階梯 | 量測表 |

---

## F 段：apcs016 跑馬燈顯示計數（`marquee-display-count`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| F1 | 答案 = `2^(n−k) mod 1000000007`；k=n 時為 1 | `curation/semantics016.py` 附「真的列舉所有畫面」的暴力參照，在 n ≤ 12 的**全部** (n,k) 組合相符；獨立復現代理以自寫列舉驗到 n=12 全符 | 輸出說明 | I/O 契約 | — |
| F2 | 20 筆 literal 第 1 筆 `5 2`（答案 8），涵蓋 k=0、k=n、n=1、n=1000000 | `curation/out/frontmatter016.yaml`；`measure/report016.json` 的 `entries_k_pos` / `entries_big_n` | 範例 | 測資計畫 | — |
| F3 | REFERENCE（三參數 `pow`）與 A2（先算大整數再取餘數）各 20/20、最大 op 皆 **7**；A1（O(n) 迴圈）20/20、最大 op **2,000,009**，出現在 **entry 5 即 (1000000, 0)** | `measure/routes016.json` 的 `worst_traced_ops`；op 來源為 `verify/judge_ops.py` | — | 成本階梯 | 量測表 |
| F4 | 四條 WRONG_ANSWER 得分：忽略 k 得 2/20、把自由度看成 k 得 0/20、輸出 n−k 得 0/20、忘記取餘數得 6/20 | `measure/routes016.json` 四筆 `W*` | — | 誤解路線鑑別 | 量測表 |
| F5 | 「忽略 k」無法壓到 0/20：契約強制涵蓋 k=0，而該路線在 k=0 時本來就對。已把 k=0 壓到最少的 2 筆 | `measure/report016.json` 的 `entries_k_pos`；數學互斥，非資料瑕疵 | — | 誤解路線鑑別 | 殘餘風險 |
| F6 | 「忘記取餘數」得 6/20 的 6 筆全部來自 `n−k ≤ 29`（2²⁹ < 1000000007）的邊界筆，其中 4 筆是契約強制入列 | `measure/report016.json`；該路線在其餘 9 筆拋 `ValueError`（整數轉字串位數上限） | — | 誤解路線鑑別 | 量測表 |

---

## G 段：apcs017 園遊會代幣兌換（`fair-token-exchange`）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| G1 | 答案 = `min(v₂//2, v₃)`，其中 `v_p = Σ n//p^i`。n=1..15 為 `0,0,0,1,1,2,2,2,3,4,4,5,5,5,5` | `curation/semantics017.py` 附 `math.factorial` 反覆整除 12 的暴力參照，在 n ≤ 400 相符；獨立復現代理以自寫實作驗到 n=199 全符 | — | I/O 契約 | — |
| G2 | 20 筆 literal 第 1 筆 `9`（答案 3），涵蓋 n=1、n=11、n=1000000000，且 ≥ 100000000 的有 5 筆 | `curation/out/frontmatter017.yaml`；`curation/plan017.py` 契約檢查 | 範例 | 測資計畫 | — |
| G3 | REFERENCE 與兩條 ACCEPTED 各 20/20，最大 op 155／156／166 | `measure/routes017.json` | — | 成本階梯 | 量測表 |
| G4 | 十進位尾零規則得 **2/20** | `measure/routes017.json` `r017_w1_decimal.py` | — | 誤解路線鑑別 | 量測表 |
| G5 | 三條「取單邊」誤解路線得 11／11／**12**，**12/20 是本題結構允許的最低最高分**，無法再壓低 | `measure/report017.json` 的 `guess_route_bound`：`score(只取v₃) + score(只取v₂//2) ≡ 20 + #(平手)`，契約強制入列的 n=1、11、10⁹ 全是平手 → 較高者 ≥ ⌈23/2⌉ = 12。獨立復現代理重算 11+12=23=20+3 ✓ 並驗證反事實（拿掉 n=11 仍得下界 11） | — | 誤解路線鑑別 | 量測表、殘餘風險 |
| G6 | `min(v₂, v₃)`（忘記一批 12 需要兩個 2）與「只取 v₃」**輸出恆等**，因 v₂ ≥ v₃ 對所有 n 成立，故無法獨立壓低 | `measure/report017.json`；獨立代理對 n=1..4999 逐一驗證 | — | 誤解路線鑑別 | 量測表 |
| G7 | UNCLEAN_DEATH（`math.factorial` 後反覆除 12）：瀏覽器實測 **0/20**，與 E10 同型。本機記錄的 13/20 同樣是投影法的產物，非真實得分。最大 op 98,699（冷行程）＝上限的 0.99%，證明成本躲在 C 呼叫內、計數器看不見 | `measure/browser-verification.jsonl` 的 `factorial017`；`measure/routes017.json` 的 `max_ops` | — | 成本階梯（列為已知殘留） | 刻意偏離 3 |
| G8 | 該路線在 n ≥ 10⁸ 於瀏覽器**必定不可行**，支柱是**記憶體**不是時間：n=10⁸ 的大整數本身即 314,159,123 bytes（約 300 MiB），n=10⁹ 為 3,556,832,228 bytes | `measure/routes017.json` 的 `unclean_probe.extrapolated`（鍵名為 `bytes_of_bigint`），由 `measure/routes017_measure.py` 的 `bigint_footprint()` 產生。時間外推**不作結論支柱**：同一份資料記錄的對數斜率為 `loglog_slope_central_from_minima` = 1.74、`loglog_slope_envelope` = [1.72, 1.747]，區間本身即涵蓋約 1.6% 的離散度；先前記載的「1.769 vs 重跑 1.741，差 21%」在 repo 中查無出處，已作廢 | — | 成本階梯 | 量測表、殘餘風險 |

---

## B 段：建置期與自動化驗證（2026-08-15 關閉）

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| B1 | 三題 `reference_solution` 對**正式加密池**與 `generator` 輸出一致 | `pnpm build:pools`（71 池、0 失敗）後 `vitest --run scripts/content-regression.test.ts --reporter=verbose`：`ap-layout-plan` ✓ 346 ms、`marquee-display-count` ✓ 385 ms、`fair-token-exchange` ✓ 118 ms，各抽樣 20 個池索引 | — | 共用授權約束 | 驗收條件 |
| B2 | 三題 `params` 宣告通過引擎守門 | `vitest --run scripts/challenge-params.test.ts` → 76 tests passed（該測試以掃全目錄方式涵蓋三題） | — | — | 驗收條件 |
| B5 | 三題題面**內文**通過禁用術語掃描 | `verify/check_frontmatter_pair.py` 的 D 檢查已進 repo 並沿用 `assemble.py` 的 `scan_banned`；另加棋類補掃。硬命中為零，唯一軟命中見 S6 | — | 共用授權約束 | — |
| B6 | 建置與既有測試無回歸 | `pnpm typecheck` 乾淨；`pnpm lint` 0 errors（21 個既有 warnings，皆不在本 change 觸及的檔案）；`vitest --run` 58 檔 **821 passed / 50 skipped**（基線 809 passed，+12 來自三題） | — | — | 驗收條件 |

---

## S 段：實際出貨碼（與 E/F/G 段的路線檔是**不同對象**）

E4／E5／F3／G3 描述的是 `curation/routes/` 底下的**學生路線檔**。隨題目出貨、實際會被判題鏈執行的是 frontmatter 內的 `generator` 與 `reference_solution`，兩者是重新拼寫的版本，op 數不等於路線表中的任何一筆。2026-08-15 的交叉驗證指出此追溯落差，故獨立成段。

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| S1 | 三題出貨碼的 `generator` 與 `reference_solution` 對各自 20 筆 literal，與 `curation/semantics0XX.py` 的獨立參照**三方完全相符** | `python3 verify/check_frontmatter_pair.py` → 三題各 `20 / 20`，rc=0。該腳本另做 7 項變異負向控制（改一位數字、gen 抄 ref、改 input_budget、非空 starter_code、內文插入禁用詞、插入無出處數字）全部 rc=1 | — | 共用授權約束 | 實作契約 |
| S2 | 出貨碼 op 數（冷行程，20 筆取最大）：015 為 6,008／2,005,018；016 為 7／2,000,012；017 為 154／164。全部在上限內，最緊的是兩題的 `reference_solution`，各佔 20.05% 與 20.00%，餘裕 4.99 與 5.00 倍 | `measure/shipped-code-ops.json`，由 `verify/measure_shipped_code.py` 產生 | — | 成本階梯 | 實作契約 |
| S3 | 三題的 `generator` 與 `reference_solution` 走**不同推導路徑**：015 為封閉式 vs 逐列累加；016 為次方運算取餘數 vs 反覆加倍累乘；017 為遞增門檻累加 vs 反覆 divmod | 三份題目頁 frontmatter；`check_frontmatter_pair.py` 的 A′ 檢查確認兩者非同一份程式碼。016 原為同一推導的兩種拼寫（`pow(2,e,MOD)` vs `2**e % MOD`），已於交叉驗證後改寫 | — | 共用授權約束 | 實作契約 |
| S4 | 四鍵（`algorithm`／`params`／`input_budget`／`testcase_plan`）與 `curation/out/frontmatter0XX.yaml` **逐位元組相同**：015 為 599 bytes、016 為 791 bytes、017 為 651 bytes | `check_frontmatter_pair.py` 的 B 檢查，另以 `yaml.safe_load` 解析後二次比對 | — | 實作契約 | 實作契約 |
| S5 | 三題題面內文的**每一個數字**都能對回本矩陣的 fact id：015 有 81 個（17 種）、016 有 53 個（8 種）、017 有 97 個（13 種），對不回者為零 | `check_frontmatter_pair.py` 的 E 檢查，逐一列出數字與其 fact id | — | — | 實作契約 |
| S6 | 三題全頁禁用術語掃描零硬命中。唯一軟命中為 apcs016 的「馬」×2，出自情境名詞「跑馬燈」，**判定為誤報** | `check_frontmatter_pair.py` 的 D 檢查（沿用 `assemble.py` 的 `scan_banned`，BANNED_EN 66 條／BANNED_ZH 49 條），另加棋類詞彙補掃 | — | 共用授權約束 | — |
| S7 | 015 題面的效能提醒寫「超出單筆測資的**執行量上限**」。**先前寫成「時間限制」是錯的**：E8 證明該路線死於 op 上限。措辭刻意不指名是哪一種限制的細節，避免洩漏系統以什麼為成本軸 | `docs/challenge/ap-layout-plan.md` 的提醒段；依據 E8 的瀏覽器實測與 op 量測 | 效能提醒 | — | — |
| S8 | 016 的 `params` 宣告 `min: 0`，與題面宣告的 `1 <= n` 不一致。因 `nk` 為單一參數帶 `count: 2`、n 與 k 共用值域，下界取聯集。三題 `testcase_plan` 全為 literal，band 不會被使用，判題無影響；若日後改用 band 會現形 | `curation/out/frontmatter016.yaml`；交叉驗證代理的裁決建議 4。四鍵已凍結，未更動 | — | — | 殘餘風險 |
| S9 | 三題 frontmatter 的**欄位集合一致**：皆具備 `layout`／`id`／`title`／`difficulty`／`category`／`type`／`tags`／`description`／`algorithm`／`params`／`input_budget`／`testcase_plan`／`generator`／`reference_solution`／`starter_code` 十五個鍵，無一題多鍵或少鍵，且 `tags` 三題皆非空 | `verify/check_frontmatter_pair.py` 的 F 檢查（逐題比對鍵集合並拒絕空 `tags`）。此列因 2026-08-15 稽核發現 apcs017 的 `tags` 為空陣列而新增——矩陣先前完全未追蹤 `tags`，是覆蓋缺口而非單一筆誤 | frontmatter | 共用授權約束 | — |

---

## W 段：瀏覽器實測（2026-08-15，`pnpm preview:cf` 於 localhost:8788，COOP `same-origin` ＋ COEP `require-corp` 已確認送出）

本段是本 change **唯一無法在本機證明**的部分。它推翻了三條先前以「本機量測 + 投影」得出的結論（E8 的死因、E10 與 G7 的得分），這正是它存在的理由。

| id | 主張 | 證據 | 題目頁 | spec | design |
|---|---|---|---|---|---|
| W1 | 三題 `reference_solution` 在真實 Pyodide 各 **20/20**。單筆最大牆鐘與各自的 deadline 餘裕：apcs015 為 375 ms（13.3 倍）、apcs016 為 441 ms（**11.3 倍，三題中最緊**）、apcs017 為 8 ms（625 倍） | `measure/browser-verification.jsonl` 的 `ref015`／`ref016`／`ref017` 的 `max_ms` | — | — | 驗收條件 |
| W2 | apcs015 的三種 O(n²) 寫法在真實 Pyodide **全部 20/20**，單筆最大 269／335／706 ms。**這是 n 上界下修為 1000 的決定性驗證**——刀鋒確實消除 | `measure/browser-verification.jsonl` 的 `rowscan_plain`／`rowscan_sum`／`rowscan_helper` | — | 成本階梯 | 決策表 Q7 |
| W3 | `math.factorial` **本身可以**被 deadline 乾淨中斷。有界變體（n > 200000 時改走正解）在第 14 筆（n=65610）得乾淨 TLE、**5,041 ms**，全體 19/20。因 factorial(65610) 僅約 0.07 秒，昂貴的是其後的整除迴圈，那是 bytecode 層級 | `measure/browser-verification.jsonl` 的 `probe_factorial_small`：`verdicts AAAAAAAAAAAAATAAAAAA`、`per_ms` 第 14 筆 5041 | — | — | 刻意偏離 3 |
| W4 | 真正殺死 worker 的是**巨大參數的單一 C 呼叫**（例如 n=10⁸ 的 factorial），它永遠不返回、中斷旗標永遠檢查不到。後果是**整份提交的 20 筆結果全部被丟棄**，學生看到 0/20 全「未執行」，**沒有部分分數** | E10／G7 的 0/20 與 W3 的 19/20 對照：同一支 `math.factorial`，參數有界時乾淨判 TLE、無界時全盤皆墨 | — | 成本階梯 | 刻意偏離 3、殘餘風險 |
| W5 | 分頁與 worker **會復原**：不乾淨死亡後緊接著提交正解，兩題皆立刻回到 20/20 | `measure/browser-verification.jsonl` 的 `ref015_after_unclean`（20/20、max 368 ms）與 `ref017_after_unclean`（20/20、max 3 ms，其前一筆 `factorial017_pre_recovery` 為 0/20，確保復原測試確實接在不乾淨死亡之後） | — | — | 殘餘風險 |
| W6 | `import math` 本身不被沙箱守衛阻擋 | `measure/browser-verification.jsonl` 的 `probe_import_math`：20/20、max 2 ms。此為排除 E10／G7 之 0/20 另有他因的對照實驗 | — | — | — |

---

## 尚未取得證據的事實

**目前為空。** B1／B2／B5／B6 由建置期驗證關閉（B 段），B3／B4 由瀏覽器實測關閉並在過程中推翻了三條先前結論（W 段）。

本區塊保留不刪：任何後續變更若引入無證據的主張，必須先列在這裡，且三份文件在證據補齊前不得宣稱其成立。


