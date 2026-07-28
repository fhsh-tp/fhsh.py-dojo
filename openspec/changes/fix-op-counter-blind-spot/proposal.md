## Problem

判題引擎的 op-counter(sys.settrace 計數器,唯一的 per-testcase TLE 防線)對**扁平頂層學生程式碼完全失效**:學生用最典型的寫法(不包函式、直接在頂層寫迴圈)提交時 `op_count` 恆為 0,無論跑多少操作都不會觸發 op 上限。後果分兩層:

- **dev 模式**(`run` handler):慢解/無限迴圈不會得到 TLE,只能等 wall-clock 旁路。
- **正式站**(`run_only` handler,無任何 per-case wall-clock):無限迴圈或慢速扁平解的實際結局是外層「N×6 秒總預算」把整個 Worker 強殺 → `resolve(null)` → 學生看到**零筆結果、0 通過、無任何錯誤訊息的靜默失敗**(實測 n=2500 扁平雙重迴圈跑 7.3 秒、op_count=0)。

此缺陷潛伏自判題 Worker 初建(2026-03-09),影響所有題目;現有測試全是字串/型別斷言、零 Python 執行,因此從未被抓到。

## Root Cause

`buildWrappedCode` 產生的 wrapper 在**模組頂層**呼叫 `sys.settrace(_tracer)`。CPython 的 `settrace` 只對「之後新建的 frame」生效,**不會回溯掛上當下正在執行的 frame**——而學生的扁平頂層程式碼正是內嵌在同一個模組 frame 裡執行。PEP 709(CPython 3.12+,Pyodide 0.29 適用)讓 comprehension 也內聯進當前 frame,同樣不建新 frame。只有「學生自己定義函式並呼叫」的部分才會建新 frame 而被計數——這解釋了為何既有量測(函式包裝情境)看起來一切正常。

## Proposed Solution

在 `sys.settrace(_tracer)` 之後補上一行,把 tracer 手動掛上當下 frame:

```python
sys.settrace(_tracer)
sys._getframe().f_trace = _tracer
```

已於本機 CPython 3.13 與 repo 內建 Pyodide 0.29 雙重實測有效(扁平雙重迴圈 n=2500 從 op_count=0 變為正確觸發 TimeoutError)。TimeoutError 拋出時 CPython 會自動解除 trace,不會洩漏到下一筆。

配套(缺陷潛伏 4 個月的根因是測試零 Python 執行,必須一併補上):

1. **真 Python 執行的整合測試**:以 Node 端可執行的方式實際跑 wrapped code,驗證「扁平頂層無限/超量迴圈會觸發 Operation limit exceeded」與「正常扁平碼不受影響」。
2. **generator 路徑豁免**:修復後 `handleGenerate` 跑 generator 也會開始計數(先前因盲區實質不設限)。generator 是可信程式碼(出題者寫的),但部分題目 generator 運算量大(`smallest-prime-factor` 最壞情境僅約 5 倍餘裕),須豁免計數或給予獨立高上限,避免修復反而弄壞建置/dev 測資產生。
3. **跨測資 trace 殘留防護(audit R1 發現的既有缺陷,一併修)**:wrapper 的 `sys.settrace(None)` teardown 寫在 user code 之後,一般例外(常態 RE 路徑)會跳過它,殘留的 tracer 在共用直譯器的下一次執行的 'call' 事件以無關的 NameError 毒殺下一筆正確測資(毒發一筆後自癒;真 Pyodide 實測 RE/AC 交錯情境成績 3/6 → 0/6)。修法:每個 handler 在 `globals.clear()` **之前**先執行 `sys.settrace(None)` 解毒(此時舊 tracer 狀態尚完整,解毒劑本身不會被毒到;實測成本 0.29ms/次)。
4. **真實內容過 wrapper 的冒煙**:content-regression 以裸 python3 執行、完全不經 wrapper,對本修復的執行路徑零覆蓋力——另建冒煙測試,把宣告 `reference_solution` 的題目全部經 `buildWrappedCode`(預設 10M 上限、tracing 生效)對正式池抽樣輸入執行,鎖住真實內容不被 wrapper 誤殺。

## Non-Goals

- **不改 verdict 映射**:修復後正式站的超限錯誤仍顯示為 RE(錯誤訊息含 Operation limit exceeded)。「正式站顯示 TLE 徽章」是後續 change《add-tle-verdict》的範圍(judge.rs 無 TLE 分支是獨立缺口)。
- **不動外層 N×6 秒總預算 kill 機制**與 dev 模式 wall-clock 旁路。
- **不處理學生主動 `sys.settrace(None)` 關閉計數**——教學平台威脅模型下接受,記入 BACKLOG。
- **不改 C 內建隱形的本質限制**(`list.pop(0)`、`sorted()` 等不產生行事件)——這是 settrace 的本質,不是 bug。

## Success Criteria

- 扁平頂層學生程式碼(無函式包裝)超過 op 上限時,dev 模式顯示 TLE、正式站回傳含「Operation limit exceeded」的 error(顯示為 RE),**不再是靜默零筆結果**。
- 某筆測資拋一般例外(RE)後,同次提交的下一筆正確測資不被殘留 tracer 毒殺:真 Python 序列測試(errored → 解毒 → 正確碼)綠燈,且 4 個 handler 的解毒佈線有 mock 驅動測試守門。
- 正常解不被修復誤殺——證據分層:(a) 宣告 `reference_solution` 的題目全部經 wrapper 對正式池抽樣輸入執行且輸出正確(自動化冒煙);(b) 其餘題目以架構推論(正解 op 量級 ~10^5 vs 上限 10^7,兩個數量級餘裕)+ 2 題 dev 實機抽測(vending-change 10/10 AC、smallest-prime-factor 6/6 AC)佐證。content-regression 全綠但它不經 wrapper 路徑,不作為本項證據。
- generator 路徑(dev 測資產生與 `handleGenerate`)不因修復被 op 上限誤殺:豁免模式有真 Python 測試,dev 實機抽測 generator 重運算題正常。
- 新增的整合測試「真正執行 Python」驗證扁平碼計數生效,取代純字串斷言的盲區。

## Impact

- Affected specs: `python-generator`(op-limit enforcement 對扁平頂層碼生效、generator 執行豁免、trace 狀態重置、真實內容過 wrapper 冒煙)、`pyodide-sandbox-guard`(注入順序 requirement 增列豁免模式例外)
- Affected code:
  - Modified: `.vitepress/theme/workers/worker-utils.ts`(buildWrappedCode 補掛當下 frame;generator 豁免參數)
  - Modified: `.vitepress/theme/workers/pyodide.worker.ts`(handleGenerate 以豁免模式呼叫 wrapper;4 個 handler 執行前解毒 resetTraceState)
  - Modified: `openspec/BACKLOG.md`(記錄學生主動 sys.settrace(None) 繞過 op-counter 的已知限制)
  - New: `.vitepress/theme/__tests__/worker-utils-python.spec.ts`(真 Python 執行整合測試,含跨執行 trace 殘留序列)
  - New: `.vitepress/theme/__tests__/pyodide-worker-trace-reset.spec.ts`(4 handler 解毒佈線守門,mock pyodide 驅動)
  - New: `scripts/wrapper-content-smoke.test.ts`(reference_solution 全數經 wrapper 對正式池抽樣執行)
