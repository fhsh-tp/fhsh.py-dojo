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

原本的設計依據是「dev server 已透過 Vite 設定送出這兩個標頭，只有生產部署未送」。**該依據在 apply 期被實測推翻**：`.vitepress/config.mts` 確實宣告了 `vite.server.headers`，但 VitePress 2.0.0-alpha.16 不轉發它，dev server 實際上兩個標頭都沒有送。這個宣告自 Pyodide 整合以來一直無效而無人察覺，因為 Pyodide 本身並不需要 `SharedArrayBuffer`。

**標頭的擁有者是 Cloudflare，不是 Vite。** 唯一的定義寫在 `docs/public/_headers`，生產由 Cloudflare Pages 送出，本機以 `wrangler pages dev` 服務建置輸出來驗證同一份檔案。曾經考慮在 dev server 補一個 middleware 外掛使兩端行為一致，但那會造成兩套機制送同一組值、彼此可能漂移，且真正該被驗證的是會上線的那份 `_headers`，不是它的複製品。`config.mts` 中已證實無效的宣告一併移除——留著它會讓下一個維護者讀到一個不存在的保證。

**接受的後果**：`vitepress dev` 沒有跨來源隔離，因此開發期 `SharedArrayBuffer` 不存在，deadline 退化為每筆結束後才裁決。deadline 仍然生效，只是不即時；`deadline.ts` 每頁輸出一次開發者告警說明此狀態。凡是要驗證中斷行為或量測牆鐘的場合，一律在 `pnpm preview:cf` 之下進行。

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

## 已知殘餘（deadline 擋不住什麼）

本節記錄 deadline 的**邊界**。列在這裡的不是待辦，是本 change 明知且接受的限制；後續稽核不必重新發現，要處置請另開 change。

#### R1 不 poll 中斷訊號的單一 C 層呼叫

Pyodide 在直譯迴圈中檢查中斷緩衝區。一個從頭到尾待在 C 裡的呼叫不經過那個迴圈，因此中斷送不進去；elapsed 事後裁決要等它回來才會判，所以它會把時間用完才被判 TLE。實測 `sum(range(10**9))` 在 node 超支十萬毫秒以上。

多數 stdlib 呼叫**不受影響**——`re`、`math.factorial`、`math.comb`、三參數 `pow` 都會準時中斷（同一輪稽核的負面結果）。受影響的是少數會長時間停留在單一 C 迴圈內的呼叫。

處置：接受。整批的累計硬砍仍是最終上限，而這類提交會撞上它。要真正解決需要在 C 層加入輪詢點，屬於 Pyodide 上游而非本專案。

#### R2 降級路徑對不會回傳的提交是「不判」而非「晚判」

沒有跨來源隔離時中斷不可用，deadline 只剩事後裁決——而事後裁決需要程式先回來。一份無限迴圈的提交在降級路徑下永遠不回來，因此不會產生 TLE，只會撞上整批的累計硬砍。

處置：接受，並以部署面消除——生產環境由 `docs/public/_headers` 提供隔離，本機驗證走 `pnpm preview:cf`。真正處在降級狀態的只有 `vitepress dev`，那裡沒有學生。

#### R3 成本落在 deadline 以下的無洞察解法

deadline 是 5,000 ms 的閘，不是排名。任何在 5 秒內跑完且輸出正確的解法都會通過，無論它是否具備題目預期的洞察。C 層工作對 op 計數器隱形、對時鐘可見但可能很便宜，因此「用單一 stdlib 呼叫一步得出答案」的解法依然是合法的聰明解。

處置：接受，且與本 change 無關——這是選題階段的責任。`openspec/BACKLOG.md` 第 2.8 節的 stdlib 封閉形式盤點 SOP 因此繼續適用。

## Risks / Trade-offs

- 既有題目的某個正解或收編路線單筆牆鐘超過選定的 deadline，導致線上題目由 AC 變 TLE → D5 規定常數必須由量測導出，且驗收條件要求逐題以 `reference_solution` 實際提交確認得分不變；衝突無解時保留舊行為。
- `COEP: require-corp` 擋掉某個未帶對應標頭的跨來源子資源，造成頁面資源載入失敗 → 已於 Cloudflare 本機執行環境（`pnpm preview:cf`）實測：兩個標頭皆送出、`crossOriginIsolated` 為真、`SharedArrayBuffer` 可用、console 無任何阻擋訊息、挑戰頁正常渲染。原本寫的理由「dev server 已長期在同一組標頭下運作」**不成立**——該宣告從未生效（E2）。Pyodide 與 WASM 均為同源自架；此變更獨立成一個 PR 以便單獨回滾。
- 所有機制量測皆來自 node-Pyodide，瀏覽器行為可能不同（特別是中斷是否同樣無法被 `except` 吞掉）→ 瀏覽器覆核列為驗收條件；D2 的第二層在該結論不成立時仍提供防線。
- 中斷機制在 worker 生命週期中留下不可觀察的狀態，使後續測資行為改變 → 驗收條件包含連續多筆中斷後仍能完成整批的情境。
- 新增 deadline 後，原本靠整批預算被動終止的無限迴圈提交改由每筆 deadline 終止，整批總時間上升（最壞為測資數 × deadline）→ 主執行緒的整批上限保留，作為總時間的最終保護。

## Migration Plan

1. 先在 dev 模式完成機制實作與單元測試。
2. 在 dev 站以兩條繞道路線與既有題目的 `reference_solution` 量測，依 D5 選定 deadline 常數。
3. 加入生產環境標頭，於 staging 部署後確認站台資源正常載入且 `SharedArrayBuffer` 可用。
4. 於 staging 以生產路徑（`run_only`）覆核 TLE 判定確實由 WASM judge 產生。

回滾策略：本 change 獨立成一個 PR。若 staging 出現資源載入問題，單獨回滾即可恢復；elapsed 事後判定的降級路徑使得即使標頭被移除，deadline 仍以較弱的形式生效。

## 量測結果（tasks 4.2–4.5，2026-08-11）

全部在 `pnpm preview:cf`（Cloudflare 本機執行環境，`crossOriginIsolated` 為真）的生產路徑上實測，重跑指令為 `openspec/changes/add-judge-deadline/measure/sweep.sh`，逐筆原始資料在同目錄的 `results.jsonl`。

#### 既有題目的 `reference_solution`（O2／O3 上界）

全站 66 題中有 16 題宣告 `reference_solution`，且 11 題宣告 `testcase_plan` 的成本軸題目全數包含在這 16 題之內。**16 題全部維持滿分。**

| 題目／路線 | 得分 | 單筆最大 | 全場 | 判定序列 |
|---|---|---|---|---|
| `prize-order-code` | 20/20 | 376 ms | 2421 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `rank-code-backfill` | 20/20 | 287 ms | 2356 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `coupon-combo-quote` | 20/20 | 47 ms | 199 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `prop-box-packing` | 20/20 | 39 ms | 104 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `snack-bar-register` | 20/20 | 34 ms | 183 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `gem-blast-playtest` | 20/20 | 28 ms | 218 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `magazine-typeset-check` | 20/20 | 20 ms | 143 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `exam-collect-verify` | 20/20 | 19 ms | 86 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `buffer-audit-log` | 6/6 | 12 ms | 34 ms | `AAAAAA` |
| `prime-check` | 6/6 | 5 ms | 16 ms | `AAAAAA` |
| `card-restack-count` | 20/20 | 4 ms | 42 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `pillbox-reminder` | 20/20 | 4 ms | 44 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `print-farm-schedule` | 20/20 | 4 ms | 44 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `hello-world` | 5/5 | 3 ms | 11 ms | `AAAAA` |
| `multiplication-table` | 5/5 | 3 ms | 11 ms | `AAAAA` |
| `password-check` | 5/5 | 3 ms | 11 ms | `AAAAA` |

**上界＝376 ms**（`prize-order-code`）。

覆蓋限制（誠實記錄）：其餘 50 題未宣告 `reference_solution`，因此沒有可量測的正解代理。它們是不含 `testcase_plan` 的基礎練習題，測資規模與上表末段同級（單筆 3–5 ms）。

#### 計數器看不見的繞道（O1 下界）

| 題目／路線 | 得分 | 單筆最大 | 全場 | 判定序列 |
|---|---|---|---|---|
| `gemblast_settrace` | 17/20 | 5009 ms | 31765 ms | `AAAAAAAAAAAAAAATTTAA` |
| `gemblast_strreplace`（**最貴寫法**，掃 26 字母；非代表值） | 18/20 | 5005 ms | 14298 ms | `AAAAAAAAAAAAAAAATTAA` |
| `gemblast_strreplace_set`（**最便宜寫法**，只掃 `set(s)`；代表值） | 20/20 | 3115 ms | 7188 ms | `AAAAAAAAAAAAAAAAAAAA` |
| `gemblast_naive` | 12/20 | 1868 ms | 14712 ms | `AAAAAAAAAATTTTTTTTAA` |
| `gemblast_flat` | 12/20 | 1835 ms | 14582 ms | `AAAAAAAAAATTTTTTTTAA` |

`gemblast_naive` 與 `gemblast_flat` 的 TLE 來自 **op 上限**（單筆最大僅 1.8 秒，遠低於 deadline）——計數器對它們一直有效，與本 change 無關。

真正由 deadline 產生的只有 `gemblast_settrace`：它把計數器凍結在 5 ops，對計數器完全隱形，三筆停在 5,009 ms——即 5,000 ms deadline 生效的指紋，真實耗時只知道**超過 5 秒**。這正是本 change 要關的洞。

`str.replace` 那兩列必須一起讀，且**只有第二列算數**。第一列掃過全部 26 個字母，是這條路線的最貴寫法；第二列只掃 `set(s)` 裡實際出現的字元，是任何學生都會自然寫出的最便宜寫法。收編路線的成本上界必須取最便宜寫法（本 change 的 RCA 把這條原則列為 I-16），因為只要有一種合理寫法能過，這條路線就沒有被 deadline 擋掉。真值是 **20/20、單筆最大 3,115 ms**：`str.replace` 繞道在 deadline 之下**完整通過**，該題保證不變。第一列保留在此僅作為「量錯寫法會得到相反結論」的留痕。

四條路線與 `reference_solution` 在 40 組隨機輸入下交叉驗證輸出一致，因此上述差異純粹來自成本。

#### 中斷呈現（D7）的驗收狀態

`gemblast_settrace` 是一份被 deadline 中斷三筆的提交，其結果表格回報 20 列、測資總數 20、得分 17，三者一致——D7 要求的「列數等於測資總數」在真實中斷情境下成立。

但要誠實記錄一件事：**觸發 D7 原始缺陷的那個情境（累計硬砍造成截斷）在本次量測中沒有發生，也變得更難發生**。累計預算是「測資數 × 6,000 ms」，而每筆現在最多 5,000 ms，20 筆的最壞總和是 100 秒、低於 120 秒的硬砍線。換句話說 deadline 順帶讓截斷情境退到邊緣。D7 的修正仍然保留為防線（單元測試以「已回報三筆、總數二十筆」直接斷言），但它在瀏覽器端的證據是「中斷提交的列數正確」，不是「硬砍截斷後的列數正確」。

#### 已收編路線（O3）——兩次量錯與最終真值

第一輪只量了 `reference_solution`，據此得出「上界 376 ms、餘裕 13.3 倍」。但本 change 自己寫進 spec 的條文要求上界涵蓋**每一條在已上線題目的 spec 中被記載為收編的路線**，而那些路線當時一條都沒量。

補量的第一版**兩條路線都實作錯了**，兩條都得到「deadline 殺掉了它」的相反結論。錯法同型：都取了該路線的最貴寫法，而收編路線的成本上界必須取**最便宜的合理寫法**（RCA 的 I-16）。留痕如下，第三欄才是有效值：

| 路線 | 出處 | **真值（最便宜寫法）** | 量錯的第一版 |
|---|---|---|---|
| `math.perm` ＋ Legendre 尾零計數（prize-order-code） | `rank-code-challenges/spec.md`「documented surviving alternative solution」 | **20/20，單筆最大 2,234 ms** | 12/20、最慢完成筆 3,880 ms——第一版以 `while p % 10 == 0: p //= 10` 逐位除十剝尾零，那是矩陣 F11 早已記錄的死路，不是 spec 指名的 Legendre 公式 |
| `str.replace`（gem-blast） | `gem-blast-challenge/spec.md`「accepted alternative solution」 | **20/20，單筆最大 3,115 ms** | 18/20、兩筆停在 deadline——第一版掃過全部 26 個字母，而非只掃 `set(s)` 內實際出現的字元 |
| `math.factorial` 逐查詢（rank-code-backfill，對照組） | 同 spec 要求它**必須**失敗 | 0/20 | 符合預期，無需重量 |

**D5 的可行域不是空集合。** deadline 必須低於兩條 op 繞道（實測 >5,000 ms），又必須高於全部收編路線（最大 3,115 ms）。3,115 < 5,000 < 真實繞道成本，兩個條件同時成立，5,000 ms 是可行解。

#### D5 衝突的處置：衝突不存在，兩份 spec 修訂已撤銷

先前記載的「維持 5,000 ms 並修訂 `rank-code-challenges` 條文」是建立在 12/20 這個錯誤量測上的決定。真值 20/20 之下，該題主 spec 現行條文「it is accepted (20/20 AC)」原本就正確，deadline 沒有改變它——**該份 delta 已整份刪除**。

`gem-blast-challenge` 的 delta 不能一併刪除：該題主 spec 自己寫著「the change that implements that repair SHALL amend this clause」，是一條指名本 change 的無條件義務。留下的修訂改記真值——繞道 20/20、單筆最大 3,115 ms、**維持被接受**、測資不動——並補上一件與量測無關而確實成立的事：`sys.settrace(None)` 這類凍結計數器的解不再豁免於斷崖保證（實測 17/20，三筆被 deadline 截斷）。

#### 釘定（task 4.5）

`DEADLINE_MS = 5,000`。此值亦等於平台原本就打算生效、但因 macrotask 排序而從未觸發的那個 `setTimeout` 常數。兩個上界：

| 上界種類 | 值 | 出處 | 餘裕 |
|---|---|---|---|
| 正解（16 支 `reference_solution`） | 376 ms | `prize-order-code` | 13.3 倍 |
| **收編路線（有拘束力者）** | **3,115 ms** | `str.replace`（gem-blast，最便宜寫法） | **1.61 倍** |

有拘束力的是第二列。`DEADLINE_MS` 必須高於每一條已上線 spec 明文接受的路線，而其中最慢的一條在 3,115 ms——**5,000 ms 只比它高 60%**。先前文件所報的「餘裕 13.3 倍」只涵蓋正解，不是這個常數實際受到的約束。

殘餘風險（誠實記錄）：3,115 ms 是在一台開發機、一次量測下得到的值。比該機器慢 1.61 倍以上的裝置會讓這條 spec 明文接受的路線開始 TLE，而題目資料一個 byte 都沒動。本 change 不擴大範圍處理它，但它是後續調高常數或補上機器係數時的第一順位依據。

#### O4：gem-blast 的 `str.replace` 繞道（結論不翻面）

`gem-blast-challenge` 的 spec 記載此繞道被**接受**為聰明解，理由是「牆鐘旗標對同步碼失效，測資殺不掉它」。理由消失了（deadline 現在對同步碼有效），但結論不變：最便宜寫法實測 **20/20、單筆最大 3,115 ms**，仍在 deadline 之內。

該繞道**仍然通過完整計畫**，該題測資一個 byte 都沒有更動。修訂後的條文把接受的依據從「旗標失效」改寫為「單筆牆鐘低於 deadline」，並記入實測值。

## Open Questions

1. **1.61 倍的餘裕是否足夠**（見〈釘定〉）。目前的常數只比最慢的合法收編路線高 60%，且該值來自單機單次量測。維持現值不需任何動作；若要提高，須連帶處理「20 筆最壞總和不得超過累計硬砍 120 秒」的上限。
2. **`expression-eval-challenges` 登記的 4 條收編路線尚未量測**（task 4.4 曾被誤標為完成）。它們同屬「已上線 spec 明文接受」，若其中任何一條慢於 3,115 ms，上表第二列的上界與 1.61 倍的餘裕都要下修。
