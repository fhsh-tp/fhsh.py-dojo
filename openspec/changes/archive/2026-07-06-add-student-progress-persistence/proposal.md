## Why

目前站台為純前端、無任何持久化——學生重新整理即失去所有作答狀態，無法得知自己完成了哪些挑戰，卡關時也無從留下可供 LLM／教師分析的軌跡。這是把 `staging` 推上 `main` 前的最後一條缺口。設計與取捨已於 `.spectra/research/student-progress-persistence.md`（v4，經多輪對抗式審查收斂）與 editor 快照粒度模擬實驗（`.spectra/research/edit-granularity-experiment.py`）完成驗證。

## What Changes

- 新增本機（IndexedDB）持久化基礎層：`idb` adapter + Pinia store，以 slug 為主鍵、SSR-safe（僅 client 端於 `onMounted`／action 存取）、無 IDB 時 feature-detect 優雅降級、schema 版本化與保留上限（cap）。
- **完成度追蹤**：每題記錄 `ProgressRecord`（`completed`／`attempted`、時間戳、最佳通過數）；`ChallengeCard` 顯示 ✓ 徽章、題庫頁顯示「已完成 X／54」計數；於 submit 完成（`status==='done'`）時寫入，best-effort（徽章為自我追蹤、非成績）。
- **作答軌跡錄製**：以 `SessionTimeline`（`edit｜run｜submit` 事件的 discriminated union，per slug per session）記錄；editor 編輯以 debounced watcher 捕捉，**debounce 間隔為每題 frontmatter 欄位 `editor_capture_debounce_ms`，全域預設 1000（ms）、可逐題覆寫**；Run 事件新增專屬 seam（現 `useExecutor.execute` 不經 store）。
- **紀錄匯出**：學生可主動下載——Markdown（含給 LLM 的提示前言）＋ JSON（可機器彙整）雙格式、可選填姓名／班級、預設輸出為瘦身版並可切換完整版；序列化只含 store 快照既有欄位（答案金鑰於 worker 邊界已剝除）。
- slug 升為 `docs/shared/challenge.data.ts` 與 `Challenge` 型別的一等欄位；新增輕量「退役 slug／id 登記表」避免重用誤判。
- 相依新增 `idb`；測試新增 `fake-indexeddb` 與對應 vitest setup（jsdom 無 indexedDB）。

## Capabilities

### New Capabilities

- `local-progress-store`: IndexedDB 持久化基礎層——`idb` adapter + client-only Pinia store、slug 主鍵、SSR-safe 存取規範、feature-detect 降級、schema 版本化、保留上限（sessions/challenge 軸）、退役 slug／id 登記表。
- `challenge-completion-tracking`: 每題完成度紀錄與題庫頁徽章／計數呈現。
- `session-work-recording`: 作答軌跡錄製（edit/run/submit 事件、debounced editor 捕捉與每題 debounce 設定、Run 事件 seam）。
- `progress-record-export`: 學生主動下載紀錄（Markdown＋JSON、瘦身／完整切換、可選身分、答案金鑰安全序列化）。

### Modified Capabilities

(none)

## Impact

- Affected specs: 新增 `local-progress-store`、`challenge-completion-tracking`、`session-work-recording`、`progress-record-export`
- Affected code:
  - New:
    - `.vitepress/theme/persistence/db.ts`
    - `.vitepress/theme/stores/progress.ts`
    - `.vitepress/theme/composables/useSessionRecorder.ts`
    - `.vitepress/theme/lib/progressExport.ts`
    - `.vitepress/theme/components/challenge/CompletionBadge.vue`
    - `.vitepress/theme/components/editor/DownloadRecordButton.vue`
    - `.vitepress/theme/__tests__/setup-idb.ts`
  - Modified:
    - `.vitepress/theme/views/ChallengeView.vue`
    - `.vitepress/theme/views/ChallengeListView.vue`
    - `.vitepress/theme/components/challenge/ChallengeCard.vue`
    - `.vitepress/theme/components/editor/RunModal.vue`
    - `.vitepress/theme/composables/useExecutor.ts`
    - `.vitepress/theme/components/layout/AppHeader.vue`
    - `docs/shared/challenge.data.ts`
    - `.vitepress/theme/types.d/challenge.type.ts`
    - `scripts/new-challenge.ts`
    - `Usage.md`
    - `vitest.config.ts`
    - `package.json`
  - Removed: (none)
- Dependencies: 新增 `idb`（dependency）、`fake-indexeddb`（devDependency）
