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

## 1. testcase_plan — APCS 式測資分區(功能預留)

### 動機

APCS 題型慣例:「測資 1–3 佔 30 分(N ≤ 100)、測資 4–6 佔 70 分(N ≤ 10⁵)」。
資料面 = 同一輸入結構、不同 band 的參數值域;計分面 = 部分給分與 UI 呈現。

### 已凍結的設計草案(兩層模型)

頂層 spec 已為此預留:WASM `generate_pool_inputs` 的 spec 物件遇到
`testcase_plan` 鍵會回報 "reserved, not yet implemented"(不靜默忽略)。

```yaml
params:            # 基準輸入結構(已於 upgrade-testcase-engine 落地)
  ...
testcase_plan:     # 保留欄位;宣告時各 band 的 count 總和取代 testcase_count
  - count: 3
    override:                       # 鏡射 params 形狀的部分補丁
      cases: { params: { n: { max: 100 } } }
  - count: 2
    override:
      cases: { params: { n: { min: 1000, max: 100000 } } }
  - literal: "1\n5\n"               # 手工釘死的邊界測資(期望輸出仍由 generator 算)
```

設計要點:`override` 合併後跑同一套 parse 期驗證;`testcase_plan` 與
`testcase_count` 並存為 parse 錯誤(不搞優先權猜謎)。

### 為什麼延後(α 方案的池層代價)

plan 與現行池架構正面相撞:池為 200 筆 iid 測資、prod 每場 session 隨機抽
`testcase_count` 筆(`pool.rs:110` `select_testcases`、`generate-pools.ts` 的
`POOL_SIZE`)。隨機子集沒有 band 結構,literal 邊界測資可能整場沒被抽到。

**α 方案草案**(實作 plan 時的路線):池格式加選填 `plan_block_size` 欄位,
plan 題的池改存「整組 block」(如 200÷6≈33 組),`select_testcases` 對 plan
題改抽一整個 block;`judge.rs` 不動。估計 Rust 約 50–80 行 + 池格式版本欄位
+ 測試。**風險**:動到池隔離這個安全敏感層(2026-07-04
isolate-testcase-pools 特地加固的區域),必須獨立 change、完整 review、
staging 驗證,不可與其他工作綁包。

**邊界劃定**:計分面(部分給分、band 加總、UI)另屬 judge/前端範圍,與資料面
分開評估;在那之前「此區測資佔 XX 分」以題目敘述文字表達。

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

### 2.8 TLE 常數與大輸入(已由 input_budget 圍堵)

- **背景**:`DEFAULT_OP_LIMIT = 10_000_000`、`WALL_CLOCK_MS = 5000`、
  `WALL_CLOCK_KILL_MS = 6000` 皆寫死且無 frontmatter 旋鈕
  (`pyodide.worker.ts:96,98`、`useChallengeRunner.ts:58`);worker 內
  wall-clock guard 對純運算迴圈實質失效(`pyodide.worker.ts:157-183`)。
- **現狀**:輸入規模預算(預設 4096 bytes)使教學題不會逼近這些門檻;
  若未來要出「效能感」題型(大 N 逼 O(n²) 超時),需先做 per-challenge
  TLE 旋鈕並重測 settrace 下的實際 op/秒。

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
