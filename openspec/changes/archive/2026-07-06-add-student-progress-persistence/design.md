## Context

站台為 VitePress 2 + Vue 3 + Pinia + Pyodide 的純前端專案，目前**零持久化**（全 in-memory Pinia）。本設計依 `.spectra/research/student-progress-persistence.md`（v4，經多輪對抗式審查）與 editor 快照粒度模擬實驗（`.spectra/research/edit-granularity-experiment.py`，程式碼經 3 輪審查驗證）落地。關鍵既有約束：`docs:build` 會做 SSR render（`indexedDB`/`window` server 端為 undefined）；判題結果於 worker 邊界（`buildTestcaseResultFields`）即依 `verdict_detail` 剝除答案；executor store 以 slug 分桶；Run（`useExecutor.execute`）目前完全不經 store。

## Goals / Non-Goals

**Goals:**

- 學生跨 session 保留「完成了哪些挑戰」，並在題庫頁看到徽章與計數。
- 卡關時保留可下載的作答軌跡（edit/run/submit），供 LLM／教師分析盲點。
- 全程 client-only、feature-detect 降級，絕不破壞 SSR build 或既有測試。
- 匯出絕不外洩答案金鑰。

**Non-Goals:**

- 不做 instant／無停頓刪除的捕捉（需 change-level logging）——列 future work。
- 不做 Big O／複雜度回饋、跨裝置同步、教師端彙總工具。
- 不做後端、不做帳號登入；資料綁瀏覽器 profile、匿名。
- 不新增 `/progress` 儀表板頁（本次僅卡片徽章＋計數）。

## Decisions

### 以 idb adapter 加 client-only Pinia store 實作 IndexedDB 持久化

採 `idb`（~1KB Promise 封裝）建單一 adapter，其上以 Pinia store 提供響應式狀態。選 Pinia 而非 module-level 單例 composable：VitePress SSG 每頁 `createApp()` 會建**全新 Pinia 實例**（結構性 per-render 隔離），避免 build 期跨頁 state 洩漏；module 單例只能靠約定。**所有 IDB 存取一律在元件 `onMounted` 或 store action 內**（絕不在 `defineStore` body），因 store setup body 於 SSR 首次 `useStore()` 即執行。無 IDB（無痕模式）時 feature-detect 後降級為唯讀空狀態，站台功能不受影響。替代方案（原生 IDB／`dexie`／`idb-keyval`+`@vueuse/integrations`）分別因冗長／過重／相依成本被否決。

### slug 為持久化主鍵並升為 challenge 資料的一等欄位

以 slug（非 numeric id）為所有紀錄主鍵，與 executor 既有 keying 一致且人類可讀。slug 於 `docs/shared/challenge.data.ts` 的 `transform()` 產生為 `DataChallenge`／`Challenge` 型別的一等欄位，元件不得再從 rendered url 反推（對 `cleanUrls` 敏感）；`ChallengeView` 亦改用同一來源，避免兩條推導路徑分歧。

### ProgressRecord 與完成判定加 status 守衛

`ProgressRecord = { slug, status:'completed'|'attempted', firstCompletedAt?, lastAttemptAt, bestPassed, total }`。於 submit 完成後寫入，**必須先 `if (executorStore.status !== 'done') return`**：dev 的中止（Stop）路徑不呼叫 `setDone`，會讓 `passed===total===0` 觸發 vacuous「完成」。best-effort 語意，徽章為自我追蹤、非成績。

### SessionTimeline 以 discriminated union 記錄 edit/run/submit

每題每次作答 session 一條時間軸：`SessionEvent = {ts,kind:'edit',code} | {ts,kind:'run',stdin,stdout,error?} | {ts,kind:'submit',code,summary:{passed,total},results:[{index,verdict,elapsed_ms,error?}]}`。因 `ExecuteResult` 僅 `{stdout,elapsed_ms,error}`（無 verdict/index），一開始即設計為 union，勿事後補。

### Editor 捕捉用 debounced watcher 並以每題 editor_capture_debounce_ms 設定

editor 編輯以 `@vueuse/core` `watchDebounced` 監看既有 `code` ref（零新相依、不碰 CodeMirror 內部）；跟上一筆全文相同則去重。debounce 間隔為新 frontmatter 欄位 **`editor_capture_debounce_ms`，全域預設 1000（ms）、可逐題覆寫**（解析須做上下界防呆）。實驗證實 1.0s 對「深思型 dead-end」捕捉 96–99%、為乾淨且可日後調細的預設。

### Run 事件新增專屬 seam

現 `useExecutor.execute()` 只 resolve Promise、不碰 store。新增 seam 讓 Run（含 stdin/stdout/error）以 `run` 事件進 SessionTimeline，經 `RunModal` 或 recorder 注入，不改變 execute 既有回傳契約。

### 保留上限下在 sessions/challenge 軸並保留完整 session

cap 於 **sessions/challenge 軸**（保留最近 5 次作答 session），**每次保留的 session 快照完整不砍**——砍 snapshots/session 會毀掉正要蒐集的 stuck 軌跡。實驗顯示未 cap 時長 stuck session 可投影到百 MB 級；此 cap 將最壞界在數十 MB、平常單位數 MB。

### 匯出雙格式並保證答案金鑰安全

學生可下載：Markdown（含給 LLM 的提示前言）＋ JSON（可機器彙整），可選填姓名／班級嵌入內容與檔名（中文檔名須 sanitize）；**預設瘦身版**（只留有意義變化點＋各 run/submit 前最後一版）、可切換完整版。序列化**只取 store 快照既有欄位**；每筆 attempt 另存 `verdictDetail` 以在匯出邊界二次把關，杜絕未來 regression 洩漏 hidden 期望輸出。

### 退役 slug／id 登記表防重用誤判

slug 與 numeric id 皆可能「刪除後重用」導致舊進度誤亮綠勾。以輕量登記表記錄退役 slug／id，於 `scripts/new-challenge.ts`（slug 走既有 `existsSync`、id 走 `computeNextId`）與 content-regression 測試檢查，避免重用。

### 測試新增 fake-indexeddb 與 vitest setup

jsdom 無 `indexedDB`。新增 `fake-indexeddb` devDependency 與 vitest setup 檔注入；掛 `ChallengeView` 的既有測試以現有 mock 模式處理；`ChallengeCard`／`ChallengeListView`／`AppHeader`（目前零 Pinia setup）保持 prop-driven 或補 Pinia setup，避免打爆既有測試。

## Implementation Contract

**資料形狀（IndexedDB，schema `version:1`）：**
- object store `progress`（keyPath `slug`）存 `ProgressRecord`。
- object store `sessions`（key `[slug, sessionId]`）存 `SessionRecord = { slug, sessionId, startedAt, events: SessionEvent[], verdictDetailAtCapture }`。
- adapter 提供：`isAvailable()`、`getProgress(slug)`／`getAllProgress()`、`upsertProgress(rec)`、`appendEvent(slug, sessionId, evt)`、`listSessions(slug)`、`pruneSessions(slug, keep=5)`、`clearAll()`。無 IDB 時 `isAvailable()` 回 false，其餘為 no-op／回空。

**Frontmatter 契約：** 新增選填 `editor_capture_debounce_ms:int`（預設 1000；解析 clamp 到合理區間，非法值回退預設）。文件更新於題目規格說明。

**行為（可觀察）：**
- 學生全 AC 提交後，題庫頁該題卡片顯示 ✓、計數 +1；重新整理後仍在。
- 作答期間 editor 停頓 ≥ 該題 debounce 時，靜默存一筆 edit 事件；按執行存 run 事件；判題存 submit 事件。
- 點「下載紀錄」得一個檔（預設 Markdown 瘦身版），內容不含任何 hidden 期望輸出。
- 無 IDB／無痕：一切照常運作，僅不持久化、徽章不亮、下載為當下 session 內容或停用。

**失敗模式：** IDB 存取例外一律吞掉並降級（不得中斷作答）；SSR／build 期絕不觸及 IDB；配額滿時 prune 後重試一次，仍失敗則靜默略過該筆。

**驗收：** `pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠；新增單元測試涵蓋 adapter（fake-indexeddb）、完成判定的 status 守衛、SessionTimeline 去重與 cap、匯出的答案金鑰安全（hidden 題匯出不含 expected）；`pnpm build` 不因 SSR 觸及 IDB 而失敗。

**Scope 邊界：** in scope＝上述四 capability 的紀錄／呈現／匯出；out of scope＝instant-delete 捕捉、Big O、跨裝置同步、教師彙總、`/progress` 頁。

## Risks / Trade-offs

- [SSR build 崩潰] → 所有 IDB 存取限 `onMounted`／action，CI `pnpm build` 守門。
- [答案金鑰外洩] → 只序列化 store 快照欄位＋每筆存 verdictDetail 於匯出邊界二次把關＋content-regression 擋題目誤設 `verdict_detail: full`。
- [長 stuck session 撐大儲存] → sessions/challenge cap（保留完整、砍舊 session）。
- [slug／id 重用誤判] → 退役登記表；殘餘風險為 best-effort（可接受，非成績）。
- [instant 刪除抓不到] → 明列 future work，本次不承諾。
- [打爆既有測試] → fake-indexeddb setup＋元件維持 prop-driven／補 Pinia setup。

## Migration Plan

無伺服器端資料，僅前端。首次上線 schema `version:1`；未來變更以 IDB `onupgradeneeded` 版本化遷移，向後相容或安全捨棄。Rollback＝移除相關元件掛載與相依即可，既有作答流程不依賴本功能。

## Open Questions

- 教師端是否另需 CSV（除 Markdown＋JSON）批次彙整格式——本次先出 Markdown＋JSON，CSV 視回饋再議。
- debounce 若實務顯示需更細（0.3s）由每題欄位個別調整，全域預設維持 1000。
