# Backlog — 已凍結的未來工作與已知債務

> 本檔收錄「已討論收斂但刻意延後」的功能構想,以及 adversarial review 挖出、
> 但不屬於當前 change 範圍的已知債務。每項含問題描述、證據位置、建議處理方向。
> 來源:2026-07-26/27 `upgrade-testcase-engine` 的 discuss 與多輪 adversarial review。

## Audit finding ID 對照表

| Audit ID | 章節 |
|----------|------|
| H1(R1,經 review 駁回降 Info) | 2.7 |
| judge oracle(R1 review 發現) | 2.6 |
| M-R2-2(.env.pool 權限) | 2.9 |
| M-R2-3(content-regression 覆蓋率) | 2.10 |
| L-R2-4(verdict_detail 白名單) | 2.11 |

---

## 1. testcase_plan — APCS 式測資分區(資料面已實作,計分面預留)

### 動機

APCS 題型慣例:「測資 1–3 佔 30 分(N ≤ 100)、測資 4–6 佔 70 分(N ≤ 10⁵)」。
資料面 = 同一輸入結構、不同 band 的參數值域;計分面 = 部分給分與 UI 呈現。

### 現況(資料面已實作)

資料面已由 change《implement-testcase-plan》完成實作(2026-07-27):band +
literal 測資、池層 block 選取、dev 模式支援、逐 band 預算、plan 納入 seed
雜湊。完整規格見 `openspec/specs/testcase-plan/spec.md`(archive 後存在)
與 `Usage.md` 的 testcase_plan 章節。實作觸及 `pool.rs` 的
`select_testcases`——此檔案與加密判題引擎同檔,屬安全敏感邏輯,故經獨立
change、完整 review 與 staging 驗證後才落地。

### 尚未實作:計分面

計分面(部分給分、band 加總、UI 呈現)仍屬 judge/前端範圍,與資料面分開
評估,尚未實作。在此之前,「此區測資佔 XX 分」仍以題目敘述文字表達。

---

## 2. Adversarial Review 停車場(既有債務,非本次範圍)

### 2.1 pool.rs session 洩漏

- **問題**:`select_testcases` 建立的 session 只有 `take_session`(判題)會
  remove;學生載入題目後不提交就離開,session(含 clone 的測資)永久留在
  static state。`LoadedPool` 亦無 unload API,SPA 跨題導覽會累積。
- **證據**:`testcase-generator/src/pool.rs:56,101-103,141-146,196`。
- **建議方向**:載入新池時逐出舊池;session 建立時淘汰同 challenge 的舊
  session;或 TTL。小 change,可獨立處理。

### 2.2 IndexedDB 配額靜默失敗

- **問題**:`appendEvent` 的 `catch { /* best-effort */ }` 吞掉
  `QuotaExceededError`——配額爆掉後學生的作答紀錄靜默停止寫入,匯出的
  學習歷程被截斷且無任何提示。
- **證據**:`.vitepress/theme/persistence/db.ts:123-125`;另 `appendEvent`
  為整包 read-modify-write,位元組成本 O(n²)(`db.ts:98-112`)。
- **建議方向**:quota 錯誤至少 console.warn + UI 提示一次;長期改 append-only
  結構或壓縮舊 session。

### 2.3 dev 模式 generator 無逾時且吞錯

- **問題**:`runGenerator` 無 timeout(對比 `submit()` 的 kill timer);
  generator 超過 op limit 時錯誤被 console.error 後照樣回傳空
  `expected_output`,dev 模式帶著全空期望輸出進判題→全部 WA 且 UI 無提示。
- **證據**:`.vitepress/theme/composables/useChallengeRunner.ts:157-190`、
  `.vitepress/theme/workers/pyodide.worker.ts:347`。
- **建議方向**:generator 錯誤時設 `errorMessage` 而非靜默;補 kill timer。

### 2.4 池無 params 指紋、URL 無 content hash

- **問題**:池 payload 只有 `challenge_id`/`verdict_detail`/`testcases`,
  `load_pool` 只比對 slug;CDN 快取的舊 `.bin` 配新題目敘述無機制偵測。
- **證據**:`testcase-generator/src/pool.rs:89-94`、
  `scripts/generate-pools.ts` 的 `encryptPool` payload。
- **建議方向**:payload 加 params 指紋(如 FNV of params JSON)+ 前端載入時
  比對;或部署層 cache-busting。

### 2.5 WASM 產物新鮮度(殘餘風險)

- **問題**:`build:pools` 吃 `docs/public/wasm/` 的產物;開發者手動跳過
  `build:wasm` 時可能用舊引擎產池。常規路徑已由建置順序
  (gen:keymaterial → build:wasm → build:pools)消除,僅剩手動跳步情境。
- **建議方向**(若要根治):WASM 匯出引擎版本/原始碼指紋,`build:pools`
  比對 crate 原始碼 hash。優先級低。

### 2.6 judge() 是無節流的 AC/WA oracle(結構性)

- **問題**:WASM `judge()` 可離線、無限次呼叫;session 被消費後再呼叫
  `select_testcases` 即可續用。adversarial review 實測:336 次呼叫、83ms
  暴力還原單筆期望輸出。無後端架構下無法根治——加密池提供的是「不直接
  給答案」,不是「答案不可推導」。`select_testcases(slug, 200)` 亦可一次
  傾印全部池輸入。
- **證據**:`testcase-generator/src/judge.rs:53`、`pool.rs:120`。
- **建議方向**:誠實接受(教學平台威脅模型下,作弊成本已高於直接學會);
  若未來要加固,方向是 session 節流或 server-side 判題,皆屬架構級變更。

### 2.7 generate_pool_inputs 隨 WASM 發佈(Info)

- **問題**:建置期入口 `generate_pool_inputs` 也存在於瀏覽器載入的 WASM,
  seed 由公開資料(slug + params)導出,可重現正式池輸入序列。
- **評估**:與 2.6 的 `select_testcases(slug, 200)` 能力完全重疊,邊際風險
  為零;feature-gated 雙 wasm target 的維運成本不值得。記錄備查。

### 2.8 TLE 常數與大輸入(⚠️ 2026-07-28 更正:存在兩個未修復的判題缺口,下方結論在修復前不成立)

- **背景**:`DEFAULT_OP_LIMIT = 10_000_000`、`WALL_CLOCK_MS = 5000`、
  `WALL_CLOCK_KILL_MS = 6000` 皆寫死且無 frontmatter 旋鈕
  (`pyodide.worker.ts:96,98`、`useChallengeRunner.ts:58`);worker 內
  wall-clock guard 對純運算迴圈實質失效(`pyodide.worker.ts:157-183`)。
- **實測數據(2026-07-27,sys.settrace 全事件計數,與判題 op-counter 同邏輯)**:
  - 純 Python O(n²) 雙重迴圈在 n≈1600–2100 觸發 10,000,000 op 上限:單行
    body 比較計數型解法 n≈2000 時 10,001,999 ops;bubble sort n≈2110;
    雙 if 版 naive max/min n=2000 已達 16,000,175 ops。
  - C 實作內建對 settrace 完全隱形:`sorted()`/`max()` 對百萬元素僅產生
    8 個 trace 事件;`while lst: lst.pop(0)` 型解法(Python 迴圈 O(n) 行、
    C 層 memmove O(n²))在 n=12000 僅約 24,005 ops,**不會** TLE。
  - 教學解(deque 兩端淘汰兩輪)在單筆總元素 12,000 時約 108,033 ops,距
    上限餘裕 92.6 倍。
- **結論**:`testcase_plan` + `input_budget` 已可組出「效能感」題(大 band
  讓純 Python O(n²) TLE),不再需要「per-challenge TLE 旋鈕」作為前置。
  但 op-counter 抓不到 C 層複雜度這個結構性限制不變:list 線性掃描 /
  `pop(0)` 型解法即使 n 很大也不會觸發 TLE。
- **⚠️ 2026-07-28 更正(adversarial review 實測發現,雙獨立驗證)**:
  1. 上方實測數字全部是「**函式包裝**」情境的量測值。正式判題 wrapper
     (`worker-utils.ts` `buildWrappedCode`)在模組頂層呼叫 `sys.settrace`,
     CPython 不回溯追蹤當下 frame——**扁平頂層學生程式碼(典型寫法)
     op_count 恆為 0**,含 `while True: pass`(結局是外層 N×6s 總預算強殺
     → prod 端零筆結果的靜默失敗)。最小修法:settrace 後補
     `sys._getframe().f_trace = _tracer`(已實測有效)。
  2. `testcase-generator/src/judge.rs` 的 `judge()` **沒有 TLE 分支**
     (只有 AC/WA/RE;`wasm-pool-judge/spec.md` prose 有列 TLE 但無驗收
     Scenario,實作照 Scenario 寫而蒸發)。正式站永遠不會出現 TLE 徽章,
     op-limit 例外顯示為 RE。
  因此「已可組出效能感題」的結論在上述兩缺口修復前**不成立**。建議修復
  路線:Change 1《fix-op-counter-blind-spot》(含真正執行 Python 的整合
  測試——現有測試全為字串/型別斷言,是缺口潛伏的根因;generator 路徑
  豁免或獨立上限)→ Change 2《add-tle-verdict》(先補 spec Scenario,
  worker 傳結構化 timed_out 欄位,勿用字串比對)。細節見 2026-07-28
  RCA(deque 題 handoff 未決 0)。
- **2026-07-28 進度**:Change 1《fix-op-counter-blind-spot》已實作(扁平碼
  計數生效 + generator 豁免 + 跨測資 trace 殘留解毒 + 真 Python 整合測試
  與真實內容過 wrapper 冒煙)。**已知限制(接受,不修)**:學生可
  `import sys; sys.settrace(None)` 主動關閉 op-counter——它是防意外無限
  迴圈的防線、非防蓄意繞過的沙盒,繞過者結局是撞外層 wall-clock/總預算;
  教學平台威脅模型下接受。

### 2.9 .env.pool 檔案權限(M-R2-2)

- **問題**:`scripts/pool-key.ts` 的 `writeFileSync` 未指定 mode,金鑰檔以
  umask 預設(通常 0644)落地,共用機器上全機可讀。
- **評估**:此金鑰設計上本就會嵌入公開發佈的 WASM(XOR 混淆僅為 obfuscation),
  威脅模型見 2.6——權限加固屬衛生性措施。修法一行(`{ mode: 0o600 }`),
  另需手動 `chmod 600` 既有檔案。
- **建議方向**:低優先;可與 2.6/2.7 的威脅模型文件化一併處理。

### 2.10 content-regression 覆蓋率地板過低(M-R2-3)

- **問題**:55 題僅 4 題宣告 `reference_solution`,coverage floor 僅要求
  `> 0`;綠燈的內容保證有限。
- **評估**:屬內容投入問題,非引擎問題;floor 貿然提高會立即紅燈。
- **建議方向**:於 challenge-author skill/scaffold 將 `reference_solution`
  列為新題預設必填;存量題目逐步補齊後再提高 floor 門檻。

### 2.11 verdict_detail 建置期無白名單(L-R2-4)

- **問題**:`generate-pools.ts` 的 `readChallenge` 不驗證 `verdict_detail`
  值;拼錯會進加密池,至瀏覽器端 serde 反序列化才以可捕捉錯誤失敗
  (fail-closed,前端顯示載入失敗訊息)——屬 DX/timing 問題。
- **建議方向**:`readChallenge` 加 `['hidden','actual','full']` 白名單,
  一行成本,適合夾帶在下一個觸碰該檔的 change。
