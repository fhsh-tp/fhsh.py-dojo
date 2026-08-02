## 1. 題二壓力 band 探針與規模定案

- [x] 1.1 [P] 在 scratchpad 撰寫 op 探針腳本:重現判題引擎 settrace op-counter 計數邏輯,量測三種寫法(逐分鐘掃時間軸/線性掃下次觸發時刻/heapq)於壓力 band worst-case(Q=5、periods 20000..50000、K=400)的 op 數。驗收:輸出三組數字,逐分鐘掃 >10,000,000、線性掃與 heapq 皆 <500,000(餘裕 ≥20×)。
- [x] 1.2 依探針數據定案題二壓力 band 的 periods/k 上下界,落實 spec 需求 Testcase plan partitioning 的效能門檻條款;若 1.1 驗收不達標,調整參數(加大週期下限或上調 K)重測至達標,並將最終數據記入 design.md 的效能門檻小節。驗收:定案值與探針數據一致且已回填。

## 2. 題一 print-farm-schedule(列印工坊排程)

- [x] 2.1 以 pnpm new-challenge print-farm-schedule --title "列印工坊排程" --difficulty medium --type competition 建立骨架,id 由腳本自動分配。驗收:docs/challenge/print-farm-schedule.md 存在且 id 無衝突。
- [x] 2.2 [P] 填寫 frontmatter,實現 spec 需求 Print-farm dispatch semantics 與 Input format contracts(遵循 design「題一 print-farm-schedule(列印工坊排程,id 由 scaffold 自動分配)」契約與名詞表用語):params(m:int 2..5;n:int 1..400;times:int 1..5000 count.from n separator 空白)、testcase_plan(3 暖身 override m 2..3/n 3..8/times 1..20 + 2 壓力 override n 200..400 + 1 literal「3↵2↵5 9」)、generator(list 線性掃 m 個空閒時刻取 (時刻,編號) 最小)、reference_solution(heapq 存 (空閒時刻,機台編號))、tags 模擬+排程。驗收:m=2/n=4/times「2 3 5 7」時 generator 輸出 10;literal 筆輸出 9;scripts/challenge-params.test.ts 綠。
- [x] 2.3 [P] 撰寫素養題面,滿足 spec 需求 Literacy statement and dual-implementation validation 與 design「共同契約」的題面結構:情境段(自動派單系統的處理模式)、動手推演段(m=2 範例甘特圖走到輸出 10)、輸入/輸出說明、範例區。驗收:題面與 tags 對照 design.md 禁用詞表零出現;範例與 spec Example 數值逐字一致。

## 3. 題二 pillbox-reminder(智慧藥盒提醒)

- [x] 3.1 以 pnpm new-challenge pillbox-reminder --title "智慧藥盒提醒" --difficulty hard --type competition 建立骨架(於 2.1 之後執行,避免 id 分配競態)。驗收:docs/challenge/pillbox-reminder.md 存在且 id 無衝突。
- [x] 3.2 [P] 填寫 frontmatter,實現 spec 需求 Pillbox periodic event semantics 與 Input format contracts:params(q:int 2..5;periods:int 2..50000 count.from q separator 空白;k:int 1..400)、testcase_plan(3 暖身 override periods 2..30/k 5..20 + 2 壓力 override 依 1.2 定案值 + 1 literal「3↵2 3 6↵12」)、generator(維護 Q 個下次觸發時刻、每輪線性掃取 (時刻,編號) 最小)、reference_solution(heapq 存 (下次時刻,編號,週期))、tags 模擬+排程。驗收:Q=2/periods「3 5」/K=6 時 generator 輸出六行 1 2 1 1 2 1;literal 筆輸出十二行 1 2 1 1 2 3 1 2 1 1 2 3;challenge-params test 綠。
- [x] 3.3 [P] 撰寫素養題面,滿足 spec 需求 Literacy statement and dual-implementation validation 與 design「共同契約」的題面結構:情境段(藥盒登記順序=編號、同分鐘先登記者先顯示)、動手推演段(週期 3 5 逐分鐘表)、輸入/輸出說明、範例區(必含 tie 範例:週期 2 3、K=7 → 1 2 1 1 2 1 2)。驗收:禁用詞零出現;範例與 spec Example 數值逐字一致。

## 4. 建置與回歸驗證

- [x] 4.1 pnpm build:pools 成功,兩題加密池生成(每場 6 筆、33 blocks),無 input_budget 超標——驗證 spec 需求 Testcase plan partitioning 的分區宣告可建置。驗收:build 輸出零錯誤,docs/public/pools/ 出現兩題池檔。
- [x] 4.2 node_modules/.bin/vitest --run scripts/challenge-params.test.ts scripts/content-regression.test.ts 全綠:兩題 reference_solution 對正式池全 AC,覆蓋 design「追溯矩陣({面向×邊界}→{期望行為→驗收出口})」的 T2/T4/T6 列。驗收:vitest 零 fail。

## 5. e2e 瀏覽器實測(依 pipeline 於 audit+commit 後執行)

- [x] 5.1 pnpm build 後以 vitepress preview 起站(指定未占用 port,不動他人 4173),agent-browser 驅動兩題:貼上 reference_solution 同款正解,判題 6/6 AC。驗收:兩題皆顯示 Accepted。
- [x] 5.2 agent-browser 負對照:題一貼「單機序列化解」(輸出工時總和)得 WA;題二貼「tie 反向解」(同時刻編號大者先)於 literal 筆得 WA、貼「逐分鐘掃解」於壓力筆得 TLE。驗收:三種錯誤寫法各自顯示預期 verdict。
