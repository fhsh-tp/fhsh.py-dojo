## 1. 檔案改名與 frontmatter 重寫

- [x] 1.1 以 git 改名 docs/challenge/two-end-elimination.md → docs/challenge/buffer-audit-log.md(id 56 不變),並依 design「檔案改名與主 spec Purpose 補正」更新 title 為 緩衝區稽核日誌、algorithm 為 buffer_audit_log、tags 為 data structure 與 模擬、description 改為不提 deque 的一句話。驗證:git status 顯示 rename;frontmatter 的 algorithm 底線轉連字號等於新檔名(Usage.md 映射規則)。
- [x] 1.2 依 design「測資縮規模與預算精算」改寫測資宣告:params 的 cases.params.n 改 int 1..400;input_budget 改 8192;testcase_plan 依序三 band——count 3(override cases.params.n.max 20)、count 2(override cases.params.n.min 200)、count 1(override cases.params.n.min 1 與 max 1),總 6 筆、無 literal、無 testcase_count(落實 spec「Rescaled banded testcase plan with six testcases」)。驗證:pnpm test --run 的 scripts/challenge-params.test.ts 冒煙對本題無錯誤。
- [x] 1.3 依 design「generator 雙指標與 reference_solution deque 分工」重寫 generator:讀 T,逐筆讀 Ni 與 Ni 個整數,依 design「過程日誌語義與 tie 規則」以雙指標 l/r 模擬峰值輪(移除較小端,tie 移除 r 端)與谷值輪(移除較大端,tie 移除 r 端),各收集「依序移除的讀數+存活者」以單一空格 join 成一行,每筆輸出兩行(落實 spec「Competition-style input and process-log output」;不 import deque、不用內建 max/min 求答案)。驗證:以 spec 三個 Example(3,-5,8,1 → 1 3 -5 8 / 3 1 8 -5;5,2,5 → 5 2 5 / 5 5 2;單元素 64 → 64 / 64)手動餵入 python3 執行 generator 程式碼,輸出逐字元一致。
- [x] 1.4 重寫 reference_solution:collections.deque 實作同一過程(d[0]/d[-1] 比較、popleft()/pop() 移除、每輪一份新複本),輸出格式與 generator 完全一致(落實 spec「Two-pointer generator and deque reference solution division of labor」)。驗證:pnpm build:pools 後 pnpm test --run 的 content-regression 涵蓋本題且通過。

## 2. 題目敘述重寫(素養導向)

- [x] 2.1 依 design「素養情境:緩衝區稽核(不提 deque)」重寫題目本文:五段式結構(題目說明、動手推演、輸入說明、輸出說明、範例);情境=邊緣裝置感測讀數緩衝區+稽核日誌;動手推演以 3,-5,8,1 逐步走峰值輪與谷值輪,並含 tie 案例(5,2,5)說明「相等移除最新端」;輸入/輸出說明數字範圍與 frontmatter 一致(T 2..3、Ni 1..400、值 -999..999),tie 規則與「先峰值輪後谷值輪」以粗體明示;刪除效能提醒段落;範例區塊含單元素案例。驗證:grep 檢查全檔(排除 reference_solution 區塊)無 deque 與 雙端佇列 字樣(落實 spec「Buffer audit challenge content」的無洩題 Scenario);人工核算範例輸出正確。

## 3. 主 spec Purpose 補正

- [x] 3.1 將 openspec/specs/deque-challenge-series/spec.md 的 Purpose 段由「TBD - created by archiving change...」改為正式描述(deque 系列題目的內容契約:素養導向雙端操作題的輸入/輸出、測資分區、generator/reference 分工)。驗證:該檔 Purpose 段無 TBD 字樣;spectra validate 本 change 仍通過。

## 4. 建置與本機驗證

- [x] 4.1 pnpm build:pools 重產池。驗證:指令 exit 0;docs/public/pools/buffer-audit-log.bin 存在且體積數百 KB 級;two-end-elimination.bin 已被 cleanup 移除。
- [x] 4.2 全套檢查:pnpm test --run、pnpm typecheck、pnpm lint 三者 exit 0(冒煙與 content-regression 均涵蓋新題)。驗證:指令輸出全綠。
- [x] 4.3 pnpm dev 以 agent-browser 提交 deque 正解,得 6/6 AC(6 筆證明走 plan 路徑)。驗證:結果面板顯示 結果:6 / 6 通過,verdict 全 AC。

## 5. 生產建置 e2e(PR 更新前必做)

- [x] 5.1 pnpm build + pnpm docs:preview(port 4174)以 agent-browser 對 /challenge/buffer-audit-log 執行三場景:deque 正解 6/6 AC;舊語義單掃描解(每筆輸出一行 max min)全 WA(驗收 spec「Semantic separation between process-log solutions and result-only solutions」);方向顛倒錯解(峰值輪誤用「移除較大端」)WA×5 + AC×1——單元素 band 那筆無任何比較發生,方向錯解輸出與正解必然相同,AC 為語義必然。驗證:agent-browser snapshot 的 verdict 統計逐場相符(正解 AC×6;舊語義解 WA×6;方向錯解 WA×5+AC×1)。
