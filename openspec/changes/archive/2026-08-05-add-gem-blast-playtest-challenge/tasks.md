## 1. 骨架與素材準備

- [x] 1.1 以 pnpm new-challenge gem-blast-playtest --title "寶石消除關卡測試" --difficulty medium --category apcs --type competition 建立骨架；驗證：檔案 docs/challenge/gem-blast-playtest.md 存在且 scaffold 配號 id 前綴為 apcs、category/type/difficulty 與參數一致。
- [x] 1.2 [P] 以離線腳本產生三份巢狀對消字串素材（L=20000 兩用途、L=60000 獵殺用；w=ab 交錯前綴＋反轉串接，全滅殘量 0），並以 stack 正解驗證殘量為 0；驗證：素材長度分別為 20000/60000、殘量檢查輸出 0。（⚠ 已由 design.md Decisions 2 降級條款取代：60KB 獵殺筆實測無效已移除，終態為 3 筆兩兩異長（30000/34001/38002）異殘量（0/1/2）的巢狀 literal、input_budget 42000、題面上限 1~40000；本條保留原文作歷史紀錄）

## 2. frontmatter 契約落地

- [x] 2.1 撰寫 params 三層結構（t int 1..3；rounds group repeat from t，內含 n int 1..5 與 boards alpha_lower min_len 3 max_len 50 count from n separator 換行）與 input_budget 65000、starter_code 空字串、無 testcase_count；驗證：node_modules/.bin/vitest --run scripts/challenge-params.test.ts 過。
- [x] 2.2 撰寫 testcase_plan 20 條目（1 範例 literal 置首含 max=0 場、9 暖身 band、5 隨機壓力 band override t=1/n=1/boards 30000..40000、2 筆 20KB 巢狀 literal、1 筆 60KB 獵殺 literal、2 邊界 literal 單顆→1 與多版面全滅→0）；驗證：pnpm build:pools 成功且該題池為 10 blocks × 20 筆、無條目超 65000 預算。（⚠ 已由 design.md Decisions 2 降級條款取代：60KB 獵殺筆實測無效已移除，終態為 3 筆兩兩異長（30000/34001/38002）異殘量（0/1/2）的巢狀 literal、input_budget 42000、題面上限 1~40000；本條保留原文作歷史紀錄）
- [x] 2.3 撰寫 generator（append/pop 掃描、聚合變數 best、讀入順序 t→每場 n→n 行版面）與 reference_solution（預配陣列＋top 索引雙指標版、線性時間）；驗證：兩者對 spec「Board residues」五組例值輸出一致，且 node_modules/.bin/vitest --run scripts/content-regression.test.ts 過。

## 3. 題面撰寫

- [x] 3.1 撰寫素養題面（消除遊戲測試員情境、二消規則敘述、動手推演＝範例一逐步、輸入說明含 T<=3/N<=5/版面長度 1..60000、輸出說明含 0 為合法答案、「部分測資的版面非常長」效率暗示、範例一與 plan 第一筆逐字元一致）；驗證：全文與 tags、description 以 grep 確認不含 stack、堆疊、資料結構、deque、佇列字樣。（⚠ 已由 design.md Decisions 2 降級條款取代：60KB 獵殺筆實測無效已移除，終態為 3 筆兩兩異長（30000/34001/38002）異殘量（0/1/2）的巢狀 literal、input_budget 42000、題面上限 1~40000；本條保留原文作歷史紀錄）

## 4. 驗證鏈

- [x] 4.1 3000 組隨機小寫字串（混合長度）雙實作互驗 generator 核心 vs reference 核心；驗證：零差異。
- [x] 4.2 探針複核：重現判題 tracer（settrace 全事件計數、10M 上限）跑天真解 A/B 與 stack 正解對全部 20 條目輸入；驗證：天真解 A 於 5 隨機壓力筆與 3 巢狀 literal 全部 ≥20M ops、天真解 B 於巢狀 literal 全部 ≥20M ops、正解全條目 ≤200k ops。
- [x] 4.3 dev 真機驗證（pnpm dev＋瀏覽器）：正解 20/20 AC、天真解 A 壓力筆 TLE、replace 繞法於 60KB 獵殺筆計時——逾 5 秒保留獵殺筆，未逾則依降級條款改為第三筆 20KB 巢狀 literal 並將實測數字補記 design；驗證：三種提交的 verdict 截圖或逐筆結果記錄於 change 目錄筆記。（實測結果：60KB 筆牆鐘 6984ms 但 verdict AC——軟旗標對同步碼結構性失效，已依降級條款改為第三筆 20KB 巢狀 literal，R2 audit 後三筆再改為異長異殘量設計，見 design.md Decisions 6；數據見 dev-verification-notes.md）

## 5. 收尾

- [x] 5.1 執行 pnpm typecheck 與 pnpm lint 確認無新增違規，且 git status 確認未帶入 gitignored 產物（docs/public/pools、key_material.rs、.env.pool）；驗證：兩指令 exit 0、狀態乾淨。
