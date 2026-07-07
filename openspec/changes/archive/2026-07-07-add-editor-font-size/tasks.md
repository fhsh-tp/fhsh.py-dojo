## 1. 字級常數與資料契約

- [x] 1.1 在 `.vitepress/theme/composables/editorConfig.ts` 匯出字級常數 `FONT_SIZE_MIN = 10`、`FONT_SIZE_MAX = 24`、`FONT_SIZE_DEFAULT = 14`、`FONT_SIZE_STEP = 1`，作為 clamp／預設／步進的單一事實來源。完成時：其餘檔案改由此匯入這些值，無散落魔術數字。驗證：`pnpm typecheck` 通過，且 useEditorSettings 與 EditorSettingsPopover 皆 import 這些常數（程式碼審視）。〔決策：D1：字級範圍、預設、step — `[10, 24]`、預設 14、step 1〕
- [x] 1.2 [TDD] 在 `.vitepress/theme/composables/useEditorSettings.ts` 將 `EditorSettings` 新增 `fontSize: number`、`EDITOR_SETTINGS_SCHEMA_VERSION` 改為 `2`、`DEFAULT_EDITOR_SETTINGS.fontSize = FONT_SIZE_DEFAULT`，並讓 `normalizeEditorSettings` 對 `fontSize` 以「非有限數字→預設 14；有限數字→`clamp(Math.round(n), 10, 24)`」正規化。完成時：讀取 v1 舊值會補上 `fontSize:14` 並升為 `version:2` 且保留既有布林選擇，越界／浮點／非數字值收斂為合法整數，皆不拋例外。驗證：先於 `.vitepress/theme/__tests__/useEditorSettings.spec.ts` 增列 spec Example 的 clamp 表格案例與 v1→v2 遷移案例（紅），再實作至通過（綠）——`pnpm test --run useEditorSettings` 綠。〔涵蓋需求：Settings data contract with defaults merge and normalization〕〔決策：D2：`fontSize` 正規化 — 先型別檢查、四捨五入取整、再 clamp；D3：schema 版本 `1 → 2`，additive 遷移〕

## 2. 編輯器即時套用

- [x] 2.1 [P] [TDD] 在 `.vitepress/theme/components/editor/CodeEditor.vue` 新增 `fontSizeCompartment`（內容為 `EditorView.theme({ '&': { fontSize: '<px>px' } })`，初值取自 `settings.value.fontSize`），移除靜態 theme 中寫死的 `fontSize: '14px'`（保留 `height:100%` 與 `.cm-scroller` 設定），並將既有 settings `watch` 擴充為同時 reconfigure autocomplete／closeBrackets／fontSize。完成時：字級變更即時反映於編輯器且不重建 view、游標與 undo 保留。驗證：先新增 `.vitepress/theme/__tests__/editorFontSize.spec.ts`（真實 CodeMirror 堆疊）斷言「初始渲染為 settings 指定 px」「reconfigure 後 DOM 字級更新」（紅），再實作至綠——`pnpm test --run editorFontSize` 綠。〔涵蓋需求：Adjustable editor font size〕〔決策：D4：字級以獨立 `fontSize` compartment 即時套用〕

## 3. Popover 字級控制

- [x] 3.1 [P] [TDD] 在 `.vitepress/theme/components/editor/EditorSettingsPopover.vue` 兩個開關後新增字級步進列：`data-testid="font-size-decrease"`、`data-testid="font-size-value"`（顯示如 `14px`）、`data-testid="font-size-increase"`；點擊以 `FONT_SIZE_STEP` 增減並經 clamp 寫回 `settings.value.fontSize`，`−` 於 `<= FONT_SIZE_MIN` 時 disabled、`+` 於 `>= FONT_SIZE_MAX` 時 disabled；沿用既有「重設為預設值」使字級還原 14。完成時：使用者可用步進器調整字級、邊界時對應按鈕停用、reset 還原為 14。驗證：先於 `.vitepress/theme/__tests__/EditorSettingsPopover.spec.ts` 增列「按 `+`／`−` 更新共享 fontSize」「邊界 disabled」「reset 還原 fontSize」案例（紅），再實作至綠——`pnpm test --run EditorSettingsPopover` 綠。〔涵蓋需求：Adjustable editor font size〕〔決策：D5：popover 字級控制為步進器（− 數字 +）〕

## 4. 整體驗證

- [x] 4.1 執行完整品質關卡並確認全綠：`pnpm typecheck`、`pnpm lint`、`pnpm test --run`（既有 `MermaidDiagram` flaky 逾時不計，需與乾淨 base 比對確認無關）。完成時：新增與既有測試全數通過、型別與 lint 無誤。驗證：三道指令輸出無新失敗。
