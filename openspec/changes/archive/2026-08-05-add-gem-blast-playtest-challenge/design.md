## Context

平台判題有三道 TLE 防線：(1) settrace op-counter，上限 10,000,000 事件，對 C 內建隱形（buildWrappedCode，.vitepress/theme/workers/worker-utils.ts）；(2) worker 內每筆 5 秒牆鐘軟旗標，Python 跑完後檢查、逾時判 TLE（pyodide.worker.ts 的 WALL_CLOCK_MS）；(3) 主執行緒 6 秒×筆數總預算硬殺（useExecutor.ts 的 WALL_CLOCK_KILL_MS）。本題語義為「相鄰兩字元相同即成對消除、兩側靠攏可連鎖，求消除後遺留長度」（等價 LeetCode 1047），聚合為 T 場 × 每場 N 版面取最大遺留值。出題前已以本機 CPython 重現 tracer 完成探針實測（數字為確定性 op 數）：

| 解法 × 形狀 | op 數 | vs 10M 上限 |
|---|---|---|
| stack 正解，任意形狀 L=20000 | 60,005 | 餘裕 166× |
| 天真解 A（每移除從頭重掃）@ 巢狀對消 L=20000 | 150,045,007 | 15× 超限 |
| 天真解 B（逐趟掃至不動點）@ 巢狀對消 L=20000 | 300,060,007 | 30× 超限 |
| 天真解 A @ 隨機 26 字母 L=20000 | 21,819,202 | 2.2× 超限（L=40000 約 8×） |
| 天真解 B @ 隨機 26 字母 L=20000 | 168,485 | 不超限（隨機測資殺不死） |
| str.replace 繞法 @ 巢狀 L=60000 | 約 4 萬（op 攔不到） | 本機牆鐘 2.89s，Pyodide 估 6~12s |

「巢狀對消形狀」定義：w ＋ reverse(w)，其中 w 為 ab 交錯字串——任一時刻唯一可消配對永遠在正中間，掃描類天真解每次移除都付出 O(L) 重掃成本。

## Goals / Non-Goals

**Goals:**

- 純 Python O(n²) 天真解（A：逐次重掃；B：逐趟不動點）在壓力筆全數 TLE，且最省角落 ≥2× op 上限。
- stack 類 O(n) 正解全 20 筆 AC，op 餘裕 ≥50×。
- 題面素養化：全文、tags、description 不出現堆疊／stack／資料結構等術語；題面公告版面長度上限 40000。
- str.replace 類 C 內建繞法依降級條款放行（見 Decisions 2 實測結論），題面與測資不再嘗試攔截。

**Non-Goals:**

- 不改判題引擎、Rust testcase-generator、op-counter、牆鐘機制。
- 不保證攔截所有 C 內建繞法；獵殺筆實測無效時降級並記錄，不開引擎工事。
- 不出教學文章、不動挑戰列表頁。

## Decisions

1. **壓力筆雙軌（隨機 band ＋ 巢狀 literal）而非單靠隨機**：探針證明隨機字串的可消配對集中在前端，天真解 B 幾趟即收斂（168k ops），單靠隨機 band 必漏殺。巢狀對消形狀引擎產不出（無 adversarial pattern 型別），故以 literal 條目落地。替代方案「擴充 Rust 引擎新增巢狀字串型別」因成本（Rust＋cargo test＋新 change）被否決。
2. **獵殺筆已依降級條款移除（2026-08-05 dev 真機實測定案）**：原設計以 60KB 巢狀 literal 搭配 worker 5 秒牆鐘軟旗標獵殺 replace 繞法。實測結果：繞法於該筆牆鐘 **6984ms > 5000ms，verdict 仍為 AC**。根因是平台機制而非數字——軟旗標是 setTimeout macrotask，同步 Python 計算期間 worker event loop 被鎖死，`runPythonAsync` 完成後的 await 接續（microtask）永遠先於過期 timer callback 執行並 `clearTimeout`，**同步學生碼在既有判題引擎下不可能觸發 5 秒軟旗標**（pyodide.worker.ts 內註解亦自述此 fallback 僅防 event loop 曾再進入的情況；唯一真實牆鐘是 useExecutor 的 6s×筆數總預算硬殺）。依 proposal Non-Goals（不為此開引擎工事）執行降級：60KB 筆改為第三筆 20KB 巢狀 literal，replace 繞法視為聰明解放行。此平台限制值得另開 change 評估（例如 run 完成後以 elapsed 補判 TLE），不在本 change 範圍。
3. **generator 用 stack 掃描、reference_solution 用雙指標陣列**：兩者演算法等價但實作路徑獨立（append/pop vs 預配陣列＋top 索引），可互抓實作錯誤；沿用 buffer-audit-log 的分工前例。reference 不得用 O(n²) 寫法——content-regression 會拿它跑含 30~38KB 巢狀筆的正式池。
4. **聚合變數命名 best**：使用者原稿以 max 為變數名遮蔽內建函式，教材示範不宜，generator 與 reference 一律改用 best。
5. **範例 literal 置首**：執行彈窗預設 stdin＝第一筆測資（ChallengeView defaultStdin 慣例），第一筆固定為題面範例一，且含一個全滅→0 的版面讓學生看見「0 是合法答案」。

6. **巢狀 literal 異長異殘量（R2 audit 定案）**：R2 對抗驗證證實三筆同長（20000）同殘量（0）literal 可被一行 `len(b)==20000` 長度分支＋print(0) 繞過（天真解 B 在全部隨機筆本就不超限）。修法：長度改 30000/34001/38002（落在壓力 band 值域內、無區間可判別）、殘量改 0/1/2（哨兵字母製造非零殘量，常數輸出必 WA）。探針複核：天真解 A/B 於三筆新 literal 全部 ≥2.5×10⁷ ops 觸限、正解 ≤115k ops。

## Implementation Contract

**Behavior**：學生於 /challenge/gem-blast-playtest 看到素養題面；提交 stack 類 O(n) 正解得 20/20 AC；提交天真解 A 或 B 在壓力筆（隨機長字串與巢狀 literal）得 TLE；提交 replace 繞法全 20 筆 AC（降級條款已觸發，繞法視為接受的聰明解）。斷崖的唯一執行機制是預設 settrace op-counter——關閉 tracer（sys.settrace(None)，BACKLOG 既載明為接受的 opt-out）或把二次方工作交給 C 內建的解法不在斷崖保證範圍內，此為平台級姿態、非本題可改變。

**Interface / data shape**（frontmatter 契約）：

- `layout: challenge`、`id`（scaffold 配號，預期 apcs006）、`title: 寶石消除關卡測試`、`difficulty: medium`、`category: apcs`、`type: competition`、`algorithm: gem_blast_playtest`、`input_budget: 40004`（＝引擎對壓力 band 的 worst-case 估算值，實測 40003 建置失敗並指名條目、40004 通過——任何把 band 或 literal 撐破題面 40000 上限的未來編輯都會在 build 期 loud fail；日後若恢復大型獵殺筆需連同此值一起調整）、`starter_code: ""`。
- `params` 三層：`t`（int 1..3）→ `rounds`（group，repeat from t）內含 `n`（int 1..5）與 `boards`（alpha_lower，min_len 3、max_len 50，count from n、separator "\n"）。band override 時壓力 band 收斂為 t=1、n=1、min_len 30000、max_len 40000。
- `testcase_plan` 共 20 條目、順序固定：1 範例 literal（置首）→ 9 暖身 band（base params 值域）→ 5 隨機壓力 band（override 如上）→ 3 筆兩兩異長異殘量巢狀 literal（長度 30000/34001/38002、殘量 0/1/2，字母對 ab/cd/ef＋核心外哨兵字母）→ 2 邊界 literal（單版面單顆→輸出 1；多版面全部全滅→輸出 0）。
- 輸出格式：T 行，每行一個整數＝該場 N 個版面遺留顆數的最大值。

**Failure modes**：build:pools 對超預算 literal 直接失敗並指名條目；params 拼錯欄位由 scripts/challenge-params.test.ts 指名擋下；reference 與 generator 不一致由 content-regression 測試擋下。

**Acceptance criteria**：

1. `pnpm build:pools` 成功，池 10 blocks × 20 筆。
2. `node_modules/.bin/vitest --run scripts/content-regression.test.ts` 過（確定性 20-of-200 抽樣；未覆蓋的 plan 位置由 wrapper 冒煙 [0,100,199] 與 dev 全 20 筆人工驗證補齊並記錄於 dev-verification-notes）。
3. `node_modules/.bin/vitest --run scripts/challenge-params.test.ts` 過。
4. 3000 組隨機字串雙實作互驗（generator 核心 vs reference 核心）零差異。
5. 探針複核（重現 tracer）：天真解 A/B 於每一壓力條目 op ≥ 2×10M；正解於全部條目 op ≤ 10M/50。
6. dev 真機（pnpm dev＋瀏覽器）：正解 20/20 AC；天真解 A 壓力筆 TLE；replace 繞法全筆 AC 且無單筆逾 120s 總預算風險（見 Decisions 2 實測結論）。

**Scope boundaries**：in scope＝docs/challenge/gem-blast-playtest.md 單檔＋本 change 的 spec/design/tasks；out of scope＝引擎、判題、列表頁、教學文章、其他題目。

## Risks / Trade-offs

- **literal 進公開 repo**：巢狀 literal 輸入可被學生預計算並 hardcode 該筆輸出；攻擊「單一長度分支＋print(0)」在異長異殘量設計下被封堵（dev 實測 13/20：隨機壓力筆 WA×5、異殘量筆 WA×2）；攻擊「三份長度鍵 hardcode {30000:0, 34001:1, 38002:2}＋逐趟式天真解」**不被封堵**（R3 實測 20/20 AC，最大單筆 553,532 events）——對讀過公開 plan 的學生，spec 條款 (b) 無執行機制，此與已接受的 replace 繞法、settrace(None) opt-out 同屬平台級姿態，已明文列入 spec 的 outside-the-cliff 清單。接受，理由：成本高於 replace 繞法而效益相同，且 14/20 隨機筆仍需正確程式。
- **replace 繞法放行**：牆鐘軟旗標對同步碼結構性失效（Decisions 2），繞法將得 20/20 AC。高中生自行想到並驗證 replace 收斂等價的機率低；視為聰明解。
- **frontmatter 約 +102KB，且 literal 會進 production bundle**：strip-generator plugin 只剝 generator 與 reference_solution（BUILD_STRIPPED_FIELDS），`testcase_plan` 連同全部 literal 原文會隨頁面資料送達瀏覽器（ChallengeView 讀取、prod 僅用於 computePlanTotal 計筆數）。實測 gzip 後三筆巢狀 literal 僅約 0.3KB（高度重複字串），傳輸成本可忽略；學生可讀性與「公開 repo 可見」屬同一風險面，已由隨機筆佔 14/20 的結構抵銷。⚠️ 勿把 testcase_plan **整欄** strip——prod runner 的 effectiveTestcaseCount 會退回 testcase_count 預設 5，與 20 筆 plan block 直接衝突。「只遮 literal 值、保留 key」技術上可行（computePlanTotal 只讀 e.count 與 'literal' in e），但違反 generator-strip-plugin baseline spec 的 testcase_plan remain-intact 條款且波及全部含 literal 題目，屬另案——已登錄 BACKLOG §2.12。接受現狀。
- **繞法整批時間**：replace 繞法最慢單筆（38KB 巢狀）dev 實測 3.2s、三筆巢狀合計 ~7.2s，整批遠低於 6s×20=120s 總預算，無誤觸硬殺疑慮。
