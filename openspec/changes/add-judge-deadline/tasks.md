## 1. 中斷協定與同步執行（D1／D3／D4）

- [x] 1.1 為中斷緩衝區協定寫失敗測試：測試涵蓋「武裝後寫入中斷值會讓執行中的 Python 拋出可被 handler 捕捉的例外」、「世代編號不同的過期到期不會影響當前執行」、「該筆結束後旗標歸零」。測試檔放在 `.vitepress/theme/__tests__/`，命名與既有 worker 測試一致。驗收目標：新測試在實作前失敗、實作後通過。
- [x] 1.2 在 worker 建立中斷緩衝區的註冊與武裝／解除函式：接受緩衝區與世代編號，於使用者程式碼執行前武裝、結束後立即解除並清零。實作 D4 的時機約束——旗標不得跨越 Pyodide 自身的初始化或清理工作。驗收目標：1.1 的三項測試通過。 對應 spec 需求：The deadline is enforced by an interrupt buffer armed per testcase。
- [x] 1.3 將 `run` handler 的執行改為同步 Pyodide 執行入口（D3），並把中斷產生的例外分類為逾時而非 RE。驗收目標：`pyodide-worker-verdict-detail.spec.ts` 與 `pyodide-worker-trace-reset.spec.ts` 維持全綠，且逾時分類有新測試覆蓋。 對應 spec 需求：Sandbox guard is injected before user code in every execution。
- [x] 1.4 將 `run_only` handler 改為同步執行並在逾時時設定既有的 `timed_out` 結構化欄位，使 WASM judge 既有的 TLE 分支生效。驗收目標：`pyodide-worker-run-only.spec.ts` 擴充一個逾時情境並通過。 對應 spec 需求：Production judging receives the deadline verdict。
- [x] 1.5 將 `execute` handler 改為同步執行並套用同一套 deadline 語義，逾時時回傳逾時結果且不終止 Worker。驗收目標：`pyodide-worker-execute.spec.ts` 擴充逾時情境並通過。 對應 spec 需求：Execute Composable Method。

## 2. 主執行緒 watchdog 與第二層裁決（D1／D2）

- [x] 2.1 為 watchdog 與降級路徑寫失敗測試：涵蓋「每筆測資各自武裝與解除」、「`SharedArrayBuffer` 不可用時不拋錯且改用 elapsed 裁決」、「降級狀態會產生一次性的開發者可見訊息」。驗收目標：新測試在實作前失敗。
- [x] 2.2 在 `useExecutor.ts` 與 `useChallengeRunner.ts` 建立每筆測資的 watchdog 武裝與解除，並保留既有的整批上限作為總時間的最終保護。驗收目標：`useExecutor.spec.ts`、`useChallengeRunner-dev.spec.ts`、`useChallengeRunner-prod.spec.ts` 全綠，加上 2.1 的新測試通過。 對應 spec 需求：Every judged testcase has an enforced wall-clock deadline。
- [x] 2.3 實作 elapsed 事後裁決（D2）：三個 handler 在每筆結束時，無論正常回傳或拋出，都以 worker 自行量測的 elapsed 與 deadline 比較，超過即判逾時。驗收目標：一份「捕捉中斷例外後繼續執行」的測試提交在該筆得到逾時判定。 對應 spec 需求：Student code cannot suppress the deadline verdict。
- [x] 2.4 實作無 `SharedArrayBuffer` 的降級路徑：不拋錯、不阻擋執行、不對學生顯示環境相關錯誤，僅以 elapsed 裁決並輸出一次性開發者訊息。驗收目標：2.1 的降級測試通過。 對應 spec 需求：Judging degrades rather than fails without SharedArrayBuffer。

## 3. 呈現與部署（D6／D7）

- [x] 3.1 [P] 修正結果表格分母（D7）：改以測資總數為分母，未回報的測資顯示為未執行且與通過列視覺可辨。先寫一個「已回報三筆、總數二十筆」的元件測試斷言列數為二十，再實作。驗收目標：新測試通過，且 `ChallengeView.spec.ts` 維持全綠。 對應 spec 需求：Interrupted batches are displayed honestly。
- [x] 3.2 [P] 新增 `docs/public/_headers`，送出 `Cross-Origin-Opener-Policy: same-origin` 與 `Cross-Origin-Embedder-Policy: require-corp`（D6）。驗收目標：檔案存在且內容為 Cloudflare Pages 的 `_headers` 格式；於 staging 部署後以瀏覽器開發者工具確認回應標頭含這兩項且 `crossOriginIsolated` 為真。

## 4. deadline 常數的量測與釘定（D5）

- [ ] 4.1 建立瀏覽器量測腳本：對指定題目與指定解法逐筆回報單筆牆鐘與判定。腳本每個外部命令都必須有失敗訊號，不得以重導向吞掉錯誤輸出。驗收目標：對一個已知會逾時的解法執行時，腳本明確回報失敗而非靜默通過。
- [ ] 4.2 量測兩條已知繞道路線在瀏覽器的單筆牆鐘：提交開頭呼叫 `sys.settrace(None)` 的版本、把迴圈攤平到單行的版本。驗收目標：兩者的單筆牆鐘數字被記錄於 design 的 Open Questions 對應段落。
- [ ] 4.3 量測全站既有題目的 `reference_solution` 單筆最大牆鐘，先以 node 探針排序候選、再對牆鐘最高的題目在瀏覽器實測。驗收目標：產出一張「題目 × 單筆最大牆鐘」表並寫入 design。
- [ ] 4.4 量測 gem-blast 的 str.replace 繞道在現行 20 筆計畫下的逐筆牆鐘（`gem-blast-challenge` 修訂條文要求記錄於本 change 的 design）。驗收目標：逐筆數字寫入 design，且不修改該題任何測資。 對應 spec 需求：Bypass acceptance after hunt downgrade。
- [ ] 4.5 依 D5 的規則選定 deadline 常數並釘進程式碼：須大於 4.3 與 4.4 的最大值乘上明確的安全倍率，且小於 4.2 的繞道牆鐘。若不存在同時滿足兩端的值，改為記錄衝突並保留舊行為。驗收目標：常數與其推導在 design 中有對應數字，且該數字與程式碼常數一致。 對應 spec 需求：The deadline constant is derived from measurement of shipped challenges。

## 5. 驗收與文件

- [ ] 5.1 瀏覽器端逐條驗收：兩條繞道路線在超時測資上得到 TLE；每個既有題目的 `reference_solution` 得分與本 change 之前相同；一份會被中斷多筆的提交其結果表格列數等於測資總數且與得分一致。驗收目標：三項逐條記錄實測結果，任一項不符即回到 4.5。
- [ ] 5.2 更新 `openspec/BACKLOG.md` 第 2.8 節：標記牆鐘缺口已修復、更正該節中「`judge.rs` 沒有 TLE 分支」的過期敘述（該分支已存在並由 `timed_out` 驅動）、更正「`sys.settrace(None)` 為接受的繞過」的敘述。驗收目標：該節不再包含與現況矛盾的結論。
- [ ] 5.3 執行 `pnpm typecheck` 與 `pnpm lint` 與完整測試套件。驗收目標：三者全綠，且輸出貼進本 change 的驗證紀錄。

## 6. 需求與設計決策的覆蓋對照

本節是 tasks 對 spec 需求與 design 決策的覆蓋矩陣，供稽核逐條追溯；不新增工作項。

| spec 需求 | 覆蓋任務 |
|---|---|
| Every judged testcase has an enforced wall-clock deadline | 1.2、1.3、1.4、1.5、2.3 |
| The deadline is enforced by an interrupt buffer armed per testcase | 1.1、1.2、2.2 |
| Student code cannot suppress the deadline verdict | 2.3、5.1 |
| Judging degrades rather than fails without SharedArrayBuffer | 2.1、2.4 |
| Production judging receives the deadline verdict | 1.4、5.1 |
| The deadline constant is derived from measurement of shipped challenges | 4.1、4.2、4.3、4.4、4.5 |
| Interrupted batches are displayed honestly | 3.1、5.1 |
| Execute Composable Method | 1.5、2.2 |
| Sandbox guard is injected before user code in every execution | 1.3、1.4、1.5 |
| Bypass acceptance after hunt downgrade | 4.4 |

| design 決策 | 覆蓋任務 |
|---|---|
| D1：以中斷緩衝區實施 deadline，而非事後判定或終止 worker | 1.1、1.2、2.2 |
| D2：保留 elapsed 事後判定作為第二層與降級路徑 | 2.1、2.3、2.4 |
| D3：判題執行改用同步 runPython | 1.3、1.4、1.5 |
| D4：中斷旗標只在使用者程式碼執行期間武裝 | 1.1、1.2 |
| D5：deadline 常數由既有題目的量測結果決定，不預先寫死 | 4.1、4.2、4.3、4.4、4.5 |
| D6：生產環境以靜態 _headers 檔送出跨來源隔離標頭 | 3.2 |
| D7：結果表格分母改用測資總數 | 3.1 |
