## Context

判題引擎有三個執行 handler：`run`（dev 模式提交，worker 自行比對輸出）、`run_only`（生產模式提交，worker 只回傳 stdout 與 `timed_out` 旗標，由 WASM judge 產生判定）、`execute`（自訂 stdin 試跑，無判定）。三者共用 `buildWrappedCode` 產生的包裝碼與 `sys.settrace` op 計數器。

現況的時間防線只有兩道，且都不成立於「每筆測資」這個粒度：

1. worker 內的 5,000 ms 軟旗標是 `setTimeout` macrotask，而 `await pyodide.runPythonAsync(...)` 之後的 `clearTimeout` 是 microtask、必定先執行。對同步學生程式碼永遠不觸發。`run_only` 連這個失效旗標都沒有。
2. 主執行緒的「測資數 × 6,000 ms」一次性 timer 到期就終止 worker。粒度是整批，且終止時已回報的結果就是最終結果——未回報的測資不會產生列，導致被中斷的執行在結果表格上看起來全綠。

因為沒有時間防線，唯一的成本閘是 op 計數器，而它有兩條已實測的繞道：`sys.settrace(None)` 直接凍結計數（實測全場 5 ops）；把 K 次迴圈攤平到同一 source line 讓成本降為每 K 次 1 個 line 事件（實測稀釋 24 倍）。兩者都不是「解出題目」，是規避判題器。

本 change 的所有量測都在 node-Pyodide（`node_modules/pyodide`，與站台自架版本同源）完成，牆鐘數字僅作相對量級參考；瀏覽器覆核列為驗收條件。

## Goals / Non-Goals

**Goals:**

- 讓每筆測資有一個真正會生效的時間上限，且該上限不因學生停用 tracer 或改變程式碼排版而失效。
- 三個執行 handler 套用同一套 deadline 語義，生產路徑（`run_only`）首次獲得每筆時間上限。
- 在缺少 `SharedArrayBuffer` 的部署環境下降級而非失效。
- 累計硬砍觸發時，畫面呈現不得讓中斷的執行看起來像全部通過。

**Non-Goals:**

- 不更動 op 上限的數值與計數機制（`DEFAULT_OP_LIMIT` 與 `sys.settrace` 計數保持原樣）。既有題目的 op 斷崖校準因此完全不受影響。
- 不處理「全 literal 題目的測資輸入公開」這條答案外洩殘餘——那是不同的軸，與時間無關。
- 不為既有題目重新設計測資或重新校準斷崖。本 change 只量測既有題目是否受新 deadline 影響並記錄結果。
- 不引入 per-challenge 的 deadline frontmatter 旋鈕。deadline 為全站單一常數。

## Decisions

### D1：以中斷緩衝區實施 deadline，而非事後判定或終止 worker

三種可行機制：

| 機制 | 準時性 | 被中斷者是否停止耗用時間 | worker 存活 | 前提 |
|------|--------|--------------------------|-------------|------|
| 事後以 elapsed 補判 | 判定正確但延後 | 否，跑完才判 | 是 | 無 |
| 主執行緒終止 worker | 準時 | 是 | 否，須重建 Pyodide | 無 |
| 中斷緩衝區 | 準時 | 是 | 是 | 需 `SharedArrayBuffer` |

選中斷緩衝區。純事後判定的缺點是超時的測資仍會把時間耗盡，20 筆各超時就會撞上整批預算而觸發累計硬砍，回到「看起來全綠」的失敗模式——也就是說純事後判定會讓新的每筆 deadline 在最需要它的情境下反而引爆舊缺陷。終止 worker 雖然準時，但每次中斷都要重建 Pyodide 執行環境，一次提交可能中斷多筆。

量測依據：中斷實測在預算 3,000 ms 時於 3,001–3,004 ms 生效；中斷後 runtime 存活且無效能劣化（同一支基準解中斷前 228 ms、中斷後 225 ms、再次 223 ms）。

### D2：保留 elapsed 事後判定作為第二層與降級路徑

中斷是準時性機制，elapsed 事後判定是權威性機制。worker 在每筆結束後（無論正常回傳或拋出）都以自己量到的 elapsed 與 deadline 比較，超過即判 TLE。

保留這一層有兩個理由。其一，`SharedArrayBuffer` 需要跨來源隔離，若某個部署環境未送出對應標頭，中斷機制不可用而 elapsed 判定仍可用，功能降級而非失效。其二，它是中斷機制失效時的兜底：實測顯示 `except:`、`except KeyboardInterrupt:`、`except BaseException:` 與外層重試四種寫法都無法吞掉 Pyodide 的中斷，但這是 node-Pyodide 的觀察，第二層讓結論不成立時仍有防線。

### D3：判題執行改用同步 runPython

實測發現中斷產生的 `KeyboardInterrupt` 在 `runPythonAsync` 路徑上會從 Pyodide 內部的 Immediate 回呼冒出，成為未捕捉例外而終結整個行程——呼叫端的 try/catch 抓不到。改用同步 `runPython` 後，同一個中斷落在 try/catch 內，可正常分類為 TLE。

學生提交本來就是同步 Python，不使用 `runPythonAsync` 提供的 top-level await 能力，因此改為同步執行不損失任何既有行為。

### D4：中斷旗標只在使用者程式碼執行期間武裝

實測發現當中斷旗標在呼叫前就已設定時，中斷會落在 Pyodide 自身的 asyncio 機制內（實測 3 ms 即拋出，堆疊指向 `asyncio/tasks.py`），且該次之後 runtime 進入不可用狀態。

因此協定為：每筆測資開始執行前先清零旗標並遞增一個世代編號，武裝 watchdog；該筆結束後立即解除武裝並清零旗標。世代編號讓已排程但過期的 watchdog 回呼不會誤傷下一筆測資。

### D5：deadline 常數由既有題目的量測結果決定，不預先寫死

deadline 訂太低會把既有題目的正解與收編路線由 AC 變成 TLE，訂太高則擋不住繞道。因此常數的選定規則為：取全站既有題目的正解與所有已收編路線的**單筆最大牆鐘**，乘以一個明確的安全倍率，並確認該值仍低於兩條已知繞道路線的單筆牆鐘。

若量測顯示不存在同時滿足兩端的值（既有正解的最大單筆牆鐘已逼近或超過繞道路線），則本 change 的處置是記錄該衝突並保留舊行為，不得逕自選一個會誤殺既有題目的值。

瀏覽器比 node 慢，量測必須在瀏覽器完成，node 數字只用來排序候選題目、縮小要在瀏覽器實測的範圍。

### D6：生產環境以靜態 _headers 檔送出跨來源隔離標頭

`SharedArrayBuffer` 需要 `Cross-Origin-Opener-Policy: same-origin` 與 `Cross-Origin-Embedder-Policy: require-corp`。

原本的設計依據是「dev server 已透過 Vite 設定送出這兩個標頭，只有生產部署未送」。**該依據在 apply 期被實測推翻**：`.vitepress/config.mts` 確實宣告了 `vite.server.headers`，但 VitePress 2.0.0-alpha.16 不轉發它，dev server 實際上兩個標頭都沒有送。這個宣告自 Pyodide 整合以來一直無效而無人察覺，因為 Pyodide 本身並不需要 `SharedArrayBuffer`。若未發現，開發期的中斷路徑會靜默降級成事後裁決，正好隱藏本 change 要開發的行為本身。

因此兩端都要處理：dev 改用 `configureServer`／`configurePreviewServer` middleware 外掛設定標頭（已實測生效），生產則以靜態 `_headers` 檔提供。

採用靜態檔而非產生腳本：標頭內容不依賴任何題目資料，沒有需要從資料派生的部分，因此不需要像挑戰別名那樣的產生腳本。

風險是 `require-corp` 會擋掉未帶對應標頭的跨來源子資源。判斷依據：dev server 長期在同一組標頭下運作且站台正常，Pyodide 與 WASM 皆為自架同源資源。驗收時仍須逐頁確認。

### D7：結果表格分母改用測資總數

累計硬砍觸發時，得分「N / 總數」用的是 store 的測資總數（正確），但結果表格以已回報的列數為分母，於是三筆通過、十七筆未回報會顯示成三筆全綠。改為以測資總數為分母，未回報的測資顯示為未執行狀態。

## Implementation Contract

**行為**：學生提交一份執行時間超過 deadline 的程式碼時，該筆測資獲得 TLE 判定，且整份提交會繼續執行後續測資直到全部完成。此行為在 dev 模式（`run`）與生產模式（`run_only`）一致，且不因學生在程式碼中呼叫 `sys.settrace(None)`、將迴圈攤平到單行、或以任何形式的 `try`／`except` 包裹主要運算而改變。

**介面／資料形狀**：

- worker 在每筆測資結束時回報的結果訊息新增一個布林欄位，語義為「本筆是否因超過時間上限而終止」。`run_only` 沿用既有的 `timed_out` 欄位名，使 WASM judge 既有的 TLE 分支無須改動即可生效。`run` 的結果訊息以既有的 `verdict` 欄位表達 TLE。
- 主執行緒與 worker 之間新增一個共享的中斷緩衝區與一個世代編號，供 watchdog 武裝與解除。緩衝區不可用時，雙方協定為僅使用 elapsed 事後判定。
- `buildWrappedCode` 的簽章與既有呼叫端相容；若需要新增參數，既有的三個 handler 呼叫點必須同步更新。

**失敗模式**：

- `SharedArrayBuffer` 不可用：不拋錯、不阻擋執行，改以 elapsed 事後判定，且此降級狀態必須可被開發者觀察到（例如一次性的 console 訊息），不得靜默。
- 中斷落在 Pyodide 內部機制而使 runtime 不可用：以 D4 的武裝時機規避。若仍發生，該次提交的後續測資會連鎖失敗，因此驗收必須包含「連續多筆中斷後仍能正確完成整批」的情境。
- 學生程式碼捕捉中斷例外：由 D2 的第二層裁決兜底。

**驗收條件**：

- 對兩條已知繞道路線（提交開頭呼叫 `sys.settrace(None)` 的版本、把迴圈攤平到單行的版本）在瀏覽器實際提交，兩者在超時的測資上獲得 TLE，而非 AC。
- 對每一個既有題目的 `reference_solution` 在瀏覽器實際提交，全部維持原有得分。任何得分變化都是阻擋條件，必須回到 D5 重新選定常數。
- 一份會在中途被中斷多筆的提交，其結果表格的列數等於測資總數，且得分與列數一致。
- 單元測試覆蓋：包裝碼組成、降級路徑的判定邏輯、世代編號使過期 watchdog 失效的行為。
- `pnpm typecheck` 與 `pnpm lint` 全綠。

**範圍內**：三個執行 handler 的 deadline 語義、watchdog 與中斷協定、elapsed 事後判定、降級路徑、生產環境標頭、結果表格分母、相關 spec 條文修訂、`openspec/BACKLOG.md` 第 2.8 節的狀態更新。

**範圍外**：op 上限數值與計數機制、既有題目的測資與斷崖重新設計、per-challenge deadline 旋鈕、全 literal 題目的測資公開殘餘、WASM judge 內部的判定邏輯（既有 TLE 分支已存在且沿用）。

`generate` handler **刻意不套用 deadline**：它執行的是題目作者提供的受信任 generator，本來就以 `opLimit: null` 豁免 op 計數。無限迴圈的 generator 會卡住預覽頁，這是 `openspec/BACKLOG.md` §2.3 已記錄並明確延後的獨立問題，不在本 change 併修。因此 `generate` 保留非同步執行入口，而三個判題 handler 改為同步。

## Risks / Trade-offs

- 既有題目的某個正解或收編路線單筆牆鐘超過選定的 deadline，導致線上題目由 AC 變 TLE → D5 規定常數必須由量測導出，且驗收條件要求逐題以 `reference_solution` 實際提交確認得分不變；衝突無解時保留舊行為。
- `COEP: require-corp` 擋掉某個未帶對應標頭的跨來源子資源，造成頁面資源載入失敗 → dev server 已長期在同一組標頭下運作，Pyodide 與 WASM 均為同源自架；驗收時逐頁確認，且此變更獨立成一個 PR 以便單獨回滾。
- 所有機制量測皆來自 node-Pyodide，瀏覽器行為可能不同（特別是中斷是否同樣無法被 `except` 吞掉）→ 瀏覽器覆核列為驗收條件；D2 的第二層在該結論不成立時仍提供防線。
- 中斷機制在 worker 生命週期中留下不可觀察的狀態，使後續測資行為改變 → 驗收條件包含連續多筆中斷後仍能完成整批的情境。
- 新增 deadline 後，原本靠整批預算被動終止的無限迴圈提交改由每筆 deadline 終止，整批總時間上升（最壞為測資數 × deadline）→ 主執行緒的整批上限保留，作為總時間的最終保護。

## Migration Plan

1. 先在 dev 模式完成機制實作與單元測試。
2. 在 dev 站以兩條繞道路線與既有題目的 `reference_solution` 量測，依 D5 選定 deadline 常數。
3. 加入生產環境標頭，於 staging 部署後確認站台資源正常載入且 `SharedArrayBuffer` 可用。
4. 於 staging 以生產路徑（`run_only`）覆核 TLE 判定確實由 WASM judge 產生。

回滾策略：本 change 獨立成一個 PR。若 staging 出現資源載入問題，單獨回滾即可恢復；elapsed 事後判定的降級路徑使得即使標頭被移除，deadline 仍以較弱的形式生效。

## Open Questions

- deadline 的具體數值由 D5 的量測決定，於實作期間釘定。
- 既有題目中是否存在單筆牆鐘已逼近候選 deadline 的路線，須由量測回答；若存在，依 D5 的規則處置。
