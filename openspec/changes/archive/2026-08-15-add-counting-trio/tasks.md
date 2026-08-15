## 1. 建立題目骨架

- [x] 1.1 用 scaffold 建立三題（禁止手動建檔，id 必須由腳本配發）：`pnpm new-challenge ap-layout-plan --title "基地台佈點規劃" --difficulty easy --category apcs --type competition`、`pnpm new-challenge marquee-display-count --title "跑馬燈顯示計數" --difficulty easy --category apcs --type competition`、`pnpm new-challenge fair-token-exchange --title "園遊會代幣兌換" --difficulty medium --category apcs --type competition`。驗收：三個檔案存在於 `docs/challenge/`，配到的 id 依序遞增且與既有 apcs 題不衝突，`category: apcs` 已寫入。

## 2. 寫入題目內容

- [x] 2.1 [P] `ap-layout-plan`：把 `curation/out/frontmatter015.yaml` 的 `algorithm`／`params`／`input_budget`／`testcase_plan` 四個鍵**逐位元組**貼入 frontmatter（禁止改動任何字元），補上 `generator`、`reference_solution`（兩者實作必須互相獨立）、`starter_code: ""`。題面內文須含：8 種偏移的明確表格、k=1..5 的答案表（0/6/28/96/252）、輸入輸出說明、n ≤ 1000 的範圍。**不得**出現棋類詞彙、不得說破 2×3 區塊、不得宣稱任何路線不可行。驗收：`grep` 確認四個鍵的值與片段相同；題面每個數字都能對回 `trace-matrix.md` 的 fact id。
- [x] 2.2 [P] `marquee-display-count`：同上，來源為 `frontmatter016.yaml`。題面須把取餘數寫成「除以 1000000007 之後的餘數」，**不得**出現「模」「二進位」等術語。範例用 `5 2` → `8`，並說明為何是 8。驗收同 2.1。
- [x] 2.3 [P] `fair-token-exchange`：同上，來源為 `frontmatter017.yaml`。題面須用「排成一列的不同順序數」與「每 12 枚剛好整批換一枚」的生活語言，**不得**出現階乘／進位／質因數／模等詞。範例用 `9` → `3`，並逐步說明。驗收同 2.1。
- [x] 2.4 三題的 `generator` 與 `reference_solution` 交叉驗證：以 `curation/semantics0XX.py` 的獨立慢速參照，對每題的 20 筆 literal 逐筆比對兩份實作的輸出，全部相符才算通過。驗收：新增 `verify/check_frontmatter_pair.py` 並執行，印出三題各 20/20 相符。

## 3. 補上題面的守門

- [x] 3.1 擴充 `curation/assemble.py` 的禁用術語掃描，使其涵蓋**題面內文**（目前只掃 frontmatter 片段，見 trace-matrix 待補事實 B5）。掃描對象為三個 `docs/challenge/*.md` 的完整內容。驗收：故意在某題題面插入禁用詞後執行，exit non-zero 並指名該題與該詞；移除後回到 exit 0。

## 4. 建置與自動化驗證

- [x] 4.1 依固定順序執行 `pnpm gen:keymaterial` → `pnpm build:wasm` → `pnpm build:pools`，確認三題的加密測資池產生成功。驗收：建置 exit 0，`docs/public/pools/` 下出現三題的池檔（**不得** commit）。
- [x] 4.2 執行 `node_modules/.bin/vitest --run scripts/challenge-params.test.ts`，證明三題的 `params` 宣告通過引擎守門。驗收：三題皆 pass，補上 trace-matrix 待補事實 B2 的證據欄。
- [x] 4.3 執行 `node_modules/.bin/vitest --run scripts/content-regression.test.ts`，證明三題的 `reference_solution` 對正式加密池與 `generator` 輸出一致。驗收：三題皆 pass，補上 trace-matrix 待補事實 B1 的證據欄。
- [x] 4.4 執行 `pnpm typecheck`、`pnpm lint`、`node_modules/.bin/vitest --run`。驗收：typecheck 乾淨、lint 0 errors、既有測試無新增失敗。

## 5. 瀏覽器實測（本 change 唯一無法在本機證明的部分）

- [x] 5.1 以 `pnpm preview:cf`（wrangler，非 dev server）起本機站台，對 `ap-layout-plan` 實測三條 O(n²) 寫法與 O(n³) 逐格掃描路線，記錄每筆實際得分與耗時。驗收：三條 O(n²) 皆 20/20，逐格掃描為 8/20，寫入 `measure/browser-verification.jsonl`，補上待補事實 B3。
- [x] 5.2 實測 `math.factorial` 路線在真實瀏覽器的行為（是否卡住分頁、中斷緩衝區能否救回）。**執行前先存檔，預期分頁可能需要強制關閉。** 驗收：如實記錄觀察到的行為（含「無法乾淨中斷」這個預期結果）到同一份 jsonl，補上待補事實 B4。
- [x] 5.3 實測三題的 `reference_solution` 在瀏覽器各得 20/20。驗收：三筆結果寫入 jsonl。

## 6. 收尾

- [x] 6.1 更新 `trace-matrix.md`：把 B1–B5 五條待補事實的證據欄填上，並將它們從「尚未取得證據」區移入正式段落。驗收：矩陣中不再有空的證據欄。
- [x] 6.2 全文對帳：逐一檢查三個題目頁、spec delta、design.md 中的**每一個數字**都能對回矩陣的 fact id。驗收：新增 `verify/check_number_traceability.py` 並執行，列出所有對不回的數字（應為空）。

## 7. 任務↔需求↔矩陣 追溯對照

本表讓稽核可從需求或 fact id 反查該由哪個任務交付，不必讀散文推斷。

| spec 需求 | 交付任務 | 相關 fact id |
|---|---|---|
| Access point layout plan I/O contract | 2.1、2.4 | D3、D7、E1、E7 |
| Access point layout plan testcase plan | 2.1、4.2 | C8、E2、E3、E6、E8 |
| Access point layout plan cost ladder and bypass disposition | 5.1、5.2 | C1、C2、C3、E4、E5、E9、E10、E11 |
| Marquee display count I/O contract and discrimination | 2.2、2.4、5.3 | D2、F1、F2、F3、F4、F5、F6 |
| Fair token exchange I/O contract and discrimination | 2.3、2.4、5.3 | D5、G1–G8 |
| Shared authoring constraints for the counting trio | 1.1、3.1、4.3、6.2 | C4、C5、C6、C7、D1、D4、D6 |

| design 決策段 | 交付任務 |
|---|---|
| Interview decisions | 1.1（D1 由 scaffold 配 id）、2.1–2.3（D2–D6 的情境與措辭約束） |
| The n bound for ap-layout-plan is 1000, not 3000 | 2.1（frontmatter 的 params 上界）、5.1（三種寫法在瀏覽器同生的實測） |
| Parameter table | 2.1–2.3、4.2 |
| Measurement methodology | 5.1–5.3（唯一未由本機證明的軸）、6.1 |
| Deliberate deviations | 2.1（easy 標籤不改）、5.2（math.factorial 死法不乾淨的實測） |
