## 1. 基礎相依與挑戰身分

- [x] 1.1 新增 `idb`（dependency）與 `fake-indexeddb`（devDependency）至 `package.json` 並安裝，使持久化層可 `import { openDB } from 'idb'`、測試可在 jsdom 注入假 IndexedDB，支撐「測試新增 fake-indexeddb 與 vitest setup」決策的前置相依。驗證：`pnpm install` 成功且 `pnpm typecheck` 不報缺少模組。
- [x] 1.2 [P] 讓 slug 成為挑戰資料的一等欄位——於 `docs/shared/challenge.data.ts` 的 `transform()` 產生 `slug`，並於 `Challenge`／`DataChallenge` 型別新增 `slug`；`ChallengeView` 改用此欄位而非從 url 反推，落實「slug 為持久化主鍵並升為 challenge 資料的一等欄位」決策、滿足「Slug-keyed records」需求。驗證：新增／擴充 data loader 單元測試斷言每筆 `slug` 等於檔名 basename，`pnpm typecheck` 綠。

## 2. 持久化基礎層（local-progress-store）

- [x] 2.1 以 idb adapter 實作 IndexedDB 存取層（`.vitepress/theme/persistence/db.ts`）：schema `version:1`、object store `progress`（keyPath `slug`）與 `sessions`（key `[slug, sessionId]`），對外提供 `isAvailable/getProgress/getAllProgress/upsertProgress/appendEvent/listSessions/pruneSessions/clearAll`；連線只在函式被呼叫時開啟，落實「以 idb adapter 加 client-only Pinia store 實作 IndexedDB 持久化」決策、滿足「Client-only IndexedDB access」「Feature detection and graceful degradation」「Slug-keyed records」需求。驗證：以 `fake-indexeddb` 的單元測試覆蓋 CRUD 與 `isAvailable()` 為 false 時 reads 回空、writes 為 no-op（涵蓋場景「IndexedDB unavailable」「Progress keyed by slug」）。
- [x] 2.2 以 client-only Pinia store 包裝 adapter（`.vitepress/theme/stores/progress.ts`）：`defineStore` setup body 內不得開啟資料庫連線，所有 IDB 存取置於 action、由元件 `onMounted` 初始化；IDB 不可用時降級為唯讀空狀態，續行「以 idb adapter 加 client-only Pinia store 實作 IndexedDB 持久化」決策、滿足「Client-only IndexedDB access」「Feature detection and graceful degradation」需求。驗證：單元測試斷言僅呼叫 `useProgressStore()`（未 mount）不觸發任何 IDB 開啟（涵蓋場景「Persistence initialises after mount」），且 IDB 不可用時 store reads 為空、writes 不丟例外。
- [x] 2.3 實作 sessions/challenge 軸保留上限 `pruneSessions(slug, keep=5)`：超過上限時砍最舊 session、保留的 session 事件完整不截斷，落實「保留上限下在 sessions/challenge 軸並保留完整 session」決策、滿足「Retention cap on sessions per challenge」需求。驗證：單元測試在同一 slug 寫入第 6 個 session 後，剩餘恰 5 個且每個事件數不變（涵蓋場景「Old sessions pruned, recent kept whole」）。
- [x] 2.4 [P] 以 `onupgradeneeded` 提供 schema 版本化升級路徑，較新版本開啟時執行升級或安全重置而不壞資料，滿足「Versioned schema」需求（延續「以 idb adapter 加 client-only Pinia store 實作 IndexedDB 持久化」決策的 schema 版本化面向）。驗證：單元測試以較高 version 開啟既有資料庫，升級 handler 被呼叫且無未捕捉例外（涵蓋場景「Upgrade path present」）。

## 3. 完成度追蹤（challenge-completion-tracking）

- [x] 3.1 於 `ChallengeView.handleSubmit` 完成後寫入 `ProgressRecord`，並以 `if (executorStore.status !== 'done') return` 守衛：僅在 `status==='done' && passed===total && total>0` 記為 `completed`（首次設 `firstCompletedAt`），中止（Stop）路徑不得誤記完成，落實「ProgressRecord 與完成判定加 status 守衛」決策、滿足「Completion recorded on fully-passing submit」「Best-effort progress semantics」需求。驗證：單元測試「全 AC → completed」（場景「All testcases pass」）與「Submit 後 Stop（status 仍 running、passed=total=0）→ 不記」（場景「Aborted submission is not completed」）。
- [x] 3.2 [P] 新增 `CompletionBadge.vue` 並於 `ChallengeCard.vue` 依 completed 狀態顯示 ✓ 徽章（含 `aria-label`），滿足「Completion shown on catalogue」需求。驗證：元件測試傳入 completed prop 顯示徽章、未完成不顯示。
- [x] 3.3 於 `ChallengeListView.vue` 顯示「已完成 X／54」全域計數，數值不受難度／搜尋 filter 影響，滿足「Completion shown on catalogue」需求。驗證：單元測試 12 題 completed 時顯示 12/54，且切換 filter 後計數不變（涵蓋場景「Badge and count reflect stored progress」）。

## 4. 作答軌跡錄製（session-work-recording）

- [x] 4.1 定義 `SessionEvent` discriminated union（`edit｜run｜submit`）與 `useSessionRecorder` composable（起／停 session、append 事件、寫入 `sessions` store），落實「SessionTimeline 以 discriminated union 記錄 edit/run/submit」決策、滿足「Session timeline of edit, run, and submit events」需求。驗證：typecheck 綠；單元測試「edit→run→edit→submit」事件依時序且各帶 `kind` 與 `ts`（涵蓋場景「Mixed events recorded in order」）。
- [x] 4.2 以 `@vueuse/core` `watchDebounced` 監看 editor `code` ref 捕捉 `edit` 事件，間隔取自 `editor_capture_debounce_ms`；跟上一筆全文相同時去重不記，落實「Editor 捕捉用 debounced watcher 並以每題 editor_capture_debounce_ms 設定」決策、滿足「Debounced editor capture configurable per challenge」「Consecutive identical edits deduplicated」需求。驗證：單元測試「停頓達預設 1000ms 記一筆」（場景「Default debounce applied」）「連續相同 buffer 不重複記」（場景「Unchanged buffer not re-recorded」）。
- [x] 4.3 [P] 解析 frontmatter `editor_capture_debounce_ms` 並做上下界／型別防呆，非整數或超界回退預設 1000，續行「Editor 捕捉用 debounced watcher 並以每題 editor_capture_debounce_ms 設定」決策、滿足「Debounced editor capture configurable per challenge」需求。驗證：單元測試「未設→1000」「設 300→300」（場景「Per-challenge override honoured」）「設非法值→1000」。
- [x] 4.4 為 Run（execute）新增專屬 seam：於 `RunModal.vue`／`useExecutor.execute` 追加 `run` 事件（stdin/stdout/error）到目前 session，且不改變 `execute` 既有回傳契約，落實「Run 事件新增專屬 seam」決策、滿足「Run activity captured through a dedicated seam」需求。驗證：單元測試「執行後 session 多一筆 run 事件」且 `execute` 回傳值與現行一致（涵蓋場景「Run recorded without changing execute contract」）。
- [x] 4.5 於 submit 寫入 `submit` 事件（code＋per-testcase verdicts），只取 executor store 快照既有欄位，並隨事件保存當下 `verdictDetail`，續行「SessionTimeline 以 discriminated union 記錄 edit/run/submit」與「匯出雙格式並保證答案金鑰安全」決策、滿足「Session timeline of edit, run, and submit events」「Answer keys never exported」需求。驗證：單元測試 submit 事件含 verdicts；hidden 題之事件不含 expected 欄位。

## 5. 紀錄匯出（progress-record-export）

- [x] 5.1 [P] 實作 `progressExport.ts` 產生 Markdown（含給 LLM 的提示前言）與 JSON，序列化只取 store 快照既有欄位並依保存的 `verdictDetail` 於序列化當下二次把關，落實「匯出雙格式並保證答案金鑰安全」決策、滿足「Student-initiated download in two formats」「Answer keys never exported」需求。驗證：單元測試 hidden 題匯出不含任何 expected（場景「Hidden expected output excluded」）；輸出含 slug 與 title（場景「Download produces a file」）。
- [x] 5.2 匯出提供瘦身／完整切換，預設瘦身（保留有意義變化點與各 run/submit 前最後一版），完整版含所有事件；完整軌跡於 IDB 恆保留，續行「匯出雙格式並保證答案金鑰安全」決策、滿足「Thinned export by default with full toggle」需求。驗證：單元測試「預設輸出為瘦身」（場景「Default is thinned」）「選完整含全部事件」（場景「Full export available」）。
- [x] 5.3 匯出可選填姓名／班級並嵌入內容與建議檔名，含中文題名之檔名移除不合法字元，滿足「Optional identity for teacher handoff」需求。驗證：單元測試「提供身分→內容與檔名含之」「非法檔名字元被移除」（涵蓋場景「Identity embedded when provided」）。
- [x] 5.4 新增 `DownloadRecordButton.vue`（含 `aria-label`）掛於挑戰頁（AppHeader／結果列旁），以 Blob + anchor 觸發下載，滿足「Student-initiated download in two formats」需求。驗證：元件測試點擊呼叫匯出並產生下載；手動確認在現行 CSP 下 blob 下載可用。

## 6. 退役登記表與 scaffold

- [x] 6.1 建立退役 slug／id 登記表並於 `scripts/new-challenge.ts`（slug 走既有 `existsSync`、id 走 `computeNextId`）與 content-regression 測試檢查，重用退役 slug／id 時報錯，落實「退役 slug／id 登記表防重用誤判」決策、滿足「Retired slug and id ledger」需求。驗證：測試「以退役 slug 或 id scaffold → 被 flag」（涵蓋場景「Reused slug is flagged」）。
- [x] 6.2 [P] `scripts/new-challenge.ts` scaffold 產物加入 `editor_capture_debounce_ms` 選填欄位說明（預設 1000、可逐題覆寫），續行「Editor 捕捉用 debounced watcher 並以每題 editor_capture_debounce_ms 設定」決策、滿足「Debounced editor capture configurable per challenge」需求。驗證：手動 scaffold 一題，產出 frontmatter 含該欄位註解或範例。

## 7. 測試設施、文件與驗收

- [x] 7.1 新增 `fake-indexeddb` 的 vitest setup（`.vitepress/theme/__tests__/setup-idb.ts` 並於 `vitest.config.ts` 註冊），使 jsdom 環境下 IDB 相關測試可執行，落實「測試新增 fake-indexeddb 與 vitest setup」決策。驗證：setup 生效後 adapter 測試在 `pnpm test --run` 下通過。
- [x] 7.2 修復既有測試：`ChallengeCard`／`ChallengeListView`／`AppHeader`／`ChallengeView` specs 不因新 store／IDB 掛載而失敗（保持 prop-driven 或補 Pinia／IDB mock），續行「測試新增 fake-indexeddb 與 vitest setup」決策。驗證：`pnpm test --run` 全綠。
- [x] 7.3 [P] 於 `Usage.md` 新增 `editor_capture_debounce_ms` 欄位規格（用途、預設 1000、範圍、可逐題覆寫），滿足「Debounced editor capture configurable per challenge」需求的文件面。驗證：內容審查確認欄位、預設值與範圍皆記載。
- [x] 7.4 全綠驗收：`pnpm typecheck`、`pnpm lint`、`pnpm test --run` 通過，且 `pnpm build` 不因 SSR 觸及 IndexedDB 而失敗，落實「以 idb adapter 加 client-only Pinia store 實作 IndexedDB 持久化」決策中「絕不破壞 SSR build」的約束。驗證：四項指令皆以 exit code 0 完成。
