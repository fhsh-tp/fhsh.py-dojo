## 1. 真 Python 執行整合測試(TDD:先寫,先證明紅)

- [x] 1.1 新增 `.vitepress/theme/__tests__/worker-utils-python.spec.ts`(落實 design 決策「D3:整合測試執行載體 — 系統 python3 子行程」與 spec requirement「Op-count guard is verified by executing real Python」):以 `execFileSync('python3', ['-c', wrapped])` 執行 `buildWrappedCode` 產出(比照 `scripts/content-regression.test.ts` 的 python3 preflight-skip 模式);harness 於 wrapped code 後附加 `import sys as _t; _t.__stdout__.write(_output)` 讀回輸出。四個案例:(i) 扁平頂層超量迴圈(低 opLimit 如 50000)→ 子行程失敗且 stderr 含 "Operation limit exceeded";(ii) 扁平正常碼 → stdout 正確、零錯誤;(iii) 函式包裝超量碼 → 同樣觸發 "Operation limit exceeded";(iv) `opLimit: null` + 超量迴圈 → 正常跑完(此案例依賴任務 2.1 的簽名放寬,紅燈階段允許以型別暫時斷言)。驗證:在修復落地前執行此測試,案例 (i) 必須**失敗**(證明測到盲區)並留存紅燈輸出;案例 (ii) 應已綠(基準行為)。

## 2. Wrapper 修復與 generator 豁免

- [x] 2.1 修改 `.vitepress/theme/workers/worker-utils.ts` 的 `buildWrappedCode`(落實 design 決策「D1:修復方式 — settrace 後補掛當下 frame」與 spec requirement「Op-count guard covers flat top-level code」):簽名放寬為 `opLimit: number | null`;`opLimit` 為 number 時在 `sys.settrace(_tracer)` 之後補 `sys._getframe().f_trace = _tracer`(讓當下模組 frame 的行事件被計數);`opLimit` 為 `null` 時完全不注入 op-counter 區塊(不含 `_tracer` 定義、`sys.settrace` 安裝與 teardown 的 `sys.settrace(None)`),sandbox guard 與 stdin/stdout 區塊照舊。依 design 決策「D4:op 上限與門檻數字不動」,`DEFAULT_OP_LIMIT = 10_000_000` 與各處門檻數字一律不動。驗證:任務 1.1 的四個案例全綠;既有 `worker-utils.spec.ts` 全綠(必要時同步更新其字串斷言以反映新 wrapper 形狀);`pnpm typecheck` 通過。
- [x] 2.2 修改 `.vitepress/theme/workers/pyodide.worker.ts` 的 `handleGenerate`(落實 design 決策「D2:generator 豁免機制 — opLimit 傳 null 時整段不注入 tracer」與 spec requirement「Generator execution is exempt from the op-count guard」):改以 `buildWrappedCode(generatorCode, input, null)` 豁免模式執行 generator;`run`、`run_only`、`execute` 三個 handler 維持 `DEFAULT_OP_LIMIT` 不變。驗證:`pyodide-worker-generate.spec.ts` 全綠(必要時更新 mock 斷言),grep 確認僅 `handleGenerate` 傳 `null`。

## 3. 全題庫回歸與實機驗證

- [x] 3.1 執行 `pnpm test --run` 全套與 `pnpm lint`:全部既有測試(含 content-regression 全題庫、challenge-params 冒煙)綠燈,證明修復不影響正解、generator 與池建置契約(覆蓋 spec「Op-count guard covers flat top-level code」的 Normal flat code output is unaffected 場景)。驗證:命令零失敗。
- [x] 3.2 執行 `pnpm build:pools` 確認建置端(原生 python3,不經 wrapper)零影響、全部池正常重產;再以 `pnpm dev` 起站抽測至少 2 題(1 題一般、1 題 generator 運算量大者如 smallest-prime-factor,後者驗證 spec「Generator execution is exempt from the op-count guard」的 heavy computation 場景):dev 模式測資產生正常、提交正解得 AC。驗證:build:pools 零錯誤;兩題 dev 模式 AC。
- [x] 3.3 在 dev 站以扁平頂層 O(n²) 慢解實測 op-counter 生效(spec「Op-count guard covers flat top-level code」的 Flat top-level loop 場景在真 Pyodide 上的實機驗證):提交無函式包裝的超量迴圈碼,dev 模式顯示 TLE(而非跑到 wall-clock 或靜默)。驗證:TLE 徽章出現在超量測資列。
