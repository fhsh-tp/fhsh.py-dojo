## 1. 骨架與輸入契約

- [x] 1.1 用 `pnpm new-challenge` 依序建立 `hall-fan-coverage`、`club-room-allocation`、`radio-relay-tape` 三題骨架，一律帶 `--category apcs --type competition`，難度依序 medium、hard、medium。完成時三個檔案存在於 `docs/challenge/`，各自被自動配到唯一且連號的 `id`（預期 apcs018、apcs019、apcs020），且 `id` 未被手動填寫。驗證：`node_modules/.bin/vitest --run scripts/challenge-params.test.ts` 通過，且三題的 `id` 在全站唯一（以 grep 全部 `docs/challenge/*.md` 的 `id:` 欄位比對無重複）。
- [x] 1.2 三題的 `params` 全部改為欄位式，交付 The trio covers three techniques absent from the existing catalogue 所要求的三種核心技法各自的輸入形狀：每個重複欄位以 `count.from` 綁定先前宣告的整數參數、`separator` 為單一空白，且每個 `min`／`max` 都是字面常數。此即設計文件〈三題的輸入一律採欄位式，不用 group〉與規格 All three challenges use column-wise input 的落地。驗證：`scripts/challenge-params.test.ts` 通過（引擎不認識的型別或欄位會指名該題失敗），並人工核對三題 `params` 中無任何值域引用其他參數。

## 2. hall-fan-coverage 題目本體

- [x] 2.1 [P] 交付 hall-fan-coverage input, output and scale：輸入為第一行 R C、第二行 F、接著四行各 F 個整數（風域左上角列、左上角行、高、寬），輸出為單一整數即最大覆蓋台數；宣告上界 R=C=300、F=3000、高與寬各 150、左上角列與行各 151，`input_budget` 調高但低於 65536。此即設計文件〈A 題的矩形以「起點加長寬」表達，越界由測資分區的一致性規則保證〉與〈A 題的規模由「最便宜的暴力拼法必須死」反推，地板固定為 300×300 格點〉的落地。驗證：`pnpm build:pools` 成功且未報位元組預算超標；以手算的小案例（4 列 5 行 3 台吊扇）比對 `generator` 輸出為 3。
- [x] 2.2 [P] 撰寫 hall-fan-coverage 的題目說明，含情境敘述、輸入說明、輸出說明、範例、範例說明、邊界情況，並在題面明寫「風域保證完全落在地板範圍內」且不定義任何裁切規則。數學記號遵守 `openspec/specs/challenge-math-notation/spec.md` 的分類表。驗證：`node_modules/.bin/vitest --run scripts/latex-notation.test.ts` 通過；範例輸入與 `testcase_plan` 第一筆 `literal` 逐字相同（以 diff 比對）。

## 3. club-room-allocation 題目本體

- [x] 3.1 [P] 交付 club-room-allocation input, output and allocation rule：輸入為第一行 N、第二行 N 個開始分鐘、第三行 N 個借用時長；輸出第一行為最少教室數、第二行為 N 個依**輸入順序**排列的教室編號；分配規則為開始時間由早到晚、同時開始者依申請編號由小到大、每筆取當下編號最小的空教室、全滿則新開編號為現有間數加一。此即設計文件〈B 題以「編號最小的空教室」規則讓輸出唯一〉的落地。驗證：以規格中的四筆申請範例（起始 10/20/40/45、時長 30/30/10/10）比對 `generator` 輸出為 `3` 與 `1 2 1 3`。
- [x] 3.2 [P] 交付 club-room-allocation is not gated on a priority queue 所要求的規模設定：N 上界 6000、開始分鐘值域 1 到 9000、借用時長值域 30 到 105，時間軸為一週 10080 分鐘。N 取 6000 而非 4000 的理由是被砍路線的最便宜拼法（集合生成式）要到 N 約 4472 才會超過運算上限。此即設計文件〈B 題的斷崖切在 O(N²) 與 O(N·K) 之間，heapq 是優解而非必要〉的落地。驗證：以最大規模的一筆測資實際跑 `generator`，**以實測值**記錄最少教室數（不得以期望值代替，第一版即因此在規格寫下錯誤的「約 60 間」），確認落在數十間而非數百間，數值寫進 `measure/`。
- [x] 3.3 [P] 撰寫 club-room-allocation 的題目說明，把分配規則的四層（處理順序、同時開始的 tie-break、最小空號、新開編號）逐條寫清楚，並含範例與範例說明。驗證：`scripts/latex-notation.test.ts` 通過；範例輸入與 `testcase_plan` 第一筆 `literal` 逐字相同。

## 4. radio-relay-tape 題目本體

- [x] 4.1 [P] 交付 radio-relay-tape asks for the longest repeat-free run：輸入為第一行 N、第二行 N 個歌曲編號（**沒有 K 參數**）；輸出為最長的一段連續且歌曲兩兩相異的區段長度；歌曲編號值域 1 到 4000000、N 上界 7000。此即設計文件〈C 題改問「最長不重播段」，因為固定視窗問法在這個平台上殺不掉〉的落地。驗證：以規格中的短序列範例（N=7、序列 4 9 4 7 1 9 1）比對 `generator` 輸出為 4；並在最大規模測資上確認答案既非 1 也非 N，數值記入量測記錄。
- [x] 4.2 [P] 撰寫 radio-relay-tape 的題目說明，含情境敘述、輸入說明、輸出說明、範例、範例說明、邊界情況（整份序列完全不重複時答案為 N、整份序列只有一種歌時答案為 1）。驗證：`scripts/latex-notation.test.ts` 通過；範例輸入與 `testcase_plan` 第一筆 `literal` 逐字相同。

## 5. 測資分區與正解

- [x] 5.1 交付 Each challenge uses a twenty-entry staircase plan whose first entry is the worked example：三題各宣告 20 筆 `testcase_plan`，第一筆為與題面範例逐字相同的 `literal`，其餘 19 筆用 `count` 加 `override` 且規模單調遞增。此即設計文件〈三題共用階梯式測資分區，第一筆為題面範例〉的落地。驗證：以腳本逐筆讀出各筆的規模參數，確認單調不遞減，輸出表格寫進量測記錄；`pnpm build:pools` 成功。
- [x] 5.2 交付 hall-fan-coverage testcase entries keep rectangles inside the floor：逐筆評估 20 筆 `override` 後的有效上界，確認每一筆都滿足「風域最大起始列加最大高度減一不超過 R」與「風域最大起始行加最大寬度減一不超過 C」。驗證：把 20 筆的逐筆數值（R、C、r_max、c_max、h_max、w_max 與兩條不等式的左右值）寫成表格存進 `measure/`，任何一筆不成立即修正該筆 `override` 後重跑。
- [x] 5.3 交付 The cliff is stated from browser measurement across several spellings 所需的本機前置證據：三題各實作**至少兩種**被砍路線的拼法——最直觀的逐行迴圈，以及把內層工作推進 C 內建的最便宜拼法（A 題整列切片指定、B 題集合生成式、C 題任何可用的 C 內建寫法）——用與判題器同語意的 trace event 計數器逐筆量測。此即設計文件〈運算計數器對 C 層的工作是瞎的，斷崖必須以最便宜的拼法背書〉的落地。驗證：每題各拼法的逐筆 ops 寫成表格存進 `measure/cliff-<slug>.json`。**本機運算計數只是代理指標、不是分數**，最終判定一律以任務 7.1 的瀏覽器實測為準；本項的用途是在進瀏覽器之前先篩掉明顯不成立的規模設定。
- [x] 5.4 交付 Each challenge declares a reference solution written differently from its generator：三題各宣告一份與 `generator` 走不同演算法路線的 `reference_solution`（例如 hall-fan-coverage 的 `generator` 用二維差分、`reference_solution` 用逐列一維差分）。此即設計文件〈reference_solution 與 generator 必須是不同寫法〉的落地。驗證：`node_modules/.bin/vitest --run scripts/content-regression.test.ts` 通過，且輸出顯示三題為執行而非 skip（本機需有 python3），執行證據存進 `measure/`。

## 6. 說明圖

- [x] 6.1 [P] 交付 hall-fan-coverage 的說明圖：畫出地板格點與三台吊扇的風域矩形、重疊處的累加次數，以及差分的四角標記與還原結果。依 Each challenge ships one explanatory figure built by the existing plate pipeline，畫布 1280 px 寬直式、最小字級 24 px，經 plate 腳本對輸出至 `docs/public/assets/challenge/<id>/圖一.png`。此即設計文件〈說明圖沿用 apcs013／apcs014 的既有管線〉的落地。驗證：PNG 產出成功且腳本中無低於 24 px 的字級（以 grep 字級常數核對）。
- [x] 6.2 [P] 交付 club-room-allocation 的說明圖：時間軸上的借用區間甘特圖，標出每筆分到的教室編號，並突顯某一間教室被釋放後立刻被下一筆取用的那一刻。畫布與字級限制同上。驗證：PNG 產出成功且字級核對通過。
- [x] 6.3 [P] 交付 radio-relay-tape 的說明圖：一維點播序列與其中最長的不重播區間，畫出雙指標右端往前推、撞見重複時左端跳到「上次出現位置的下一格」的那一步。畫布與字級限制同上。驗證：PNG 產出成功且字級核對通過。

## 7. 量測與驗收

- [x] 7.1 交付 Every challenge in the trio has a measured efficiency cliff 的實測證據：在 `pnpm preview:cf` 起的 Cloudflare 本機執行環境（:8788，唯一送出 COOP/COEP 因而 SharedArrayBuffer 與 deadline 真正生效的路徑）上，對三題各提交 `reference_solution`、最直觀寫法的暴力解、**只差排版的折行變體**，以及至少一種把內層工作推進 C 內建的拼法。完成條件為三題的 `reference_solution` 皆得 20/20，且最直觀寫法與折行變體皆落在 1/20 到 19/20 之間；C 內建拼法若拿滿分則記錄其得分與最慢一筆耗時，不視為缺陷。驗證：所有提交的得分、逐筆 verdict 與逐筆耗時寫進 `measure/browser-cliff.json` 與 `measure/browser-cliff.jsonl`；不得引用本機運算計數當作分數。
- [x] 7.2 交付三張說明圖在實際欄寬下的可讀性證據：在瀏覽器量測三張圖在題目頁的顯示寬度與最小字級的螢幕像素值，確認無水平溢出且最小字級不低於 12 螢幕像素。驗證：量測數值寫進 `measure/`。
- [x] 7.3 交付 Traceability matrix for the trio 的一致性核對：逐列比對矩陣中的核心技法、被砍路線與可接受路線，與三題各自的規格條目及實測結果一致。驗證：核對表寫進 `measure/`，任何不一致即修正規格而非修正量測值。

## 8. 守門與整合

- [x] 8.1 交付全站守門綠燈：`pnpm typecheck`、`pnpm lint`、`node_modules/.bin/vitest --run` 全數通過，其中 `challenge-params`、`content-regression`、`latex-notation` 三支必須確實執行三題而非 skip。驗證：三支測試的輸出摘要存進 `measure/`。
- [x] 8.2 交付可建置的產物：`pnpm build:pools` 與 `pnpm build` 成功，三題的加密測資池產出且未超出位元組預算，三題頁面在本機 dev 站（於 repo 根目錄執行 `pnpm docs:dev`，不可用 `vitepress dev docs`）可正常開啟、圖片載入、可提交作答。驗證：本機實際開啟三頁各提交一次 `reference_solution` 得 20/20。
