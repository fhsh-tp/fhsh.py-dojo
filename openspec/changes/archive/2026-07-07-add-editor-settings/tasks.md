## 1. useEditorSettings composable 與設定契約

- [x] 1.1 撰寫 `.vitepress/theme/__tests__/useEditorSettings.spec.ts`（紅燈）：涵蓋預設值 `{ version: 1, autocomplete: true, closeBrackets: true }`、缺欄位以 defaults 補齊、布林正規化、損壞 JSON 回退為預設、寫入後再讀取的 persistence round-trip、以及無 `window`（SSR）時回傳預設值且不觸碰 localStorage。驗證：`pnpm test --run useEditorSettings` 出現對應失敗案例。〔涵蓋需求：Persistent editor settings、Settings data contract with defaults merge and normalization、SSR-safe settings access〕
- [x] 1.2 實作 `.vitepress/theme/composables/useEditorSettings.ts`：定義 `EditorSettings`、`SCHEMA_VERSION`、穩定 localStorage key、defaults 合併與型別正規化、client 端模組級單例（共享 reactive ref）與 SSR 臨時預設值 ref。行為：`useEditorSettings()` 回傳跨元件共享、以 localStorage 持久化的 reactive ref。驗證：1.1 全數綠燈。〔涵蓋需求：Persistent editor settings、Default settings preserve current behavior、Settings data contract with defaults merge and normalization、SSR-safe settings access〕〔決策：以 localStorage（useLocalStorage）持久化，不用 IndexedDB、狀態集中於 useEditorSettings composable（模組級單例 + SSR 安全）、設定資料契約：schema 版本、defaults 合併與數值 clamp〕

## 2. CodeEditor 以 Compartment 即時套用設定

- [x] 2.1 擴充 `.vitepress/theme/__tests__/CodeEditor.spec.ts`（紅燈）：新增案例——`autocomplete: false` 時輸入不顯示完成下拉；`closeBrackets: false` 時輸入 `(` 不自動補 `)`；預設值下維持既有 autocomplete 與 bracket 行為（既有案例不回歸）；切換設定後為同一 EditorView 實例（未重建）。驗證：`pnpm test --run CodeEditor` 出現對應失敗案例。〔涵蓋需求：Automatic completion trigger、Bracket auto-closing、Live application without editor rebuild〕
- [x] 2.2 重構 `.vitepress/theme/components/editor/CodeEditor.vue`：引入 `Compartment`，以 `acCompartment` 包 `autocompletion()` 與 stdlib 完成來源、`bracketCompartment` 包 `closeBrackets()`；`onMounted` 建 EditorView 前先同步讀 `useEditorSettings()` 決定初始 extensions；`watch` 設定變更以 `dispatch({ effects: compartment.reconfigure(...) })` 即時套用。行為：切換兩開關即時生效，且不重建編輯器、保留游標與 undo 歷史。驗證：2.1 全數綠燈。〔涵蓋需求：Automatic completion trigger、Bracket auto-closing、Live application without editor rebuild、Default settings preserve current behavior〕〔決策：以 CodeMirror Compartment 即時 reconfigure，不重建編輯器〕

## 3. EditorSettingsPopover 元件

- [x] 3.1 [P] 撰寫 `.vitepress/theme/__tests__/EditorSettingsPopover.spec.ts`（紅燈）：點齒輪開啟 popover、顯示「自動完成」「括號自動閉合」兩開關且反映當前設定、切換開關即更新 `useEditorSettings()` 的值、點外部與按 Esc 關閉。驗證：`pnpm test --run EditorSettingsPopover` 出現對應失敗案例。〔涵蓋需求：Editor settings entry point〕
- [x] 3.2 實作 `.vitepress/theme/components/editor/EditorSettingsPopover.vue`：齒輪 ⚙ 按鈕 + popover 面板（兩開關 + 重設），以 `useEditorSettings()` 綁定；點外部／按 Esc 關閉；樣式對齊既有 Tailwind tokens（sky/emerald、gray/slate 邊框、dark 模式）。行為：面板開關即時改變全站設定並持久化。驗證：3.1 全數綠燈。〔涵蓋需求：Editor settings entry point〕〔決策：齒輪 popover 為獨立元件 EditorSettingsPopover〕

## 4. 掛載齒輪入口於題目頁

- [x] 4.1 於 `.vitepress/theme/views/ChallengeView.vue` 下方按鈕列掛載 `<EditorSettingsPopover />`（齒輪置於按鈕列右側區）。行為：題目頁按鈕列出現齒輪，點擊開啟設定 popover 且不干擾既有「執行／送出／下載紀錄」按鈕。驗證：`pnpm test --run ChallengeView`（既有測試不回歸）＋ 於 `pnpm dev` 題目頁手動確認齒輪出現、開關即時生效、重整後選擇仍在。〔涵蓋需求：Editor settings entry point〕

## 5. 靜態驗證與回歸

- [x] 5.1 執行 `pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠。行為：型別檢查、ESLint/prettier、全部單元測試皆通過，既有 editor-autocomplete 相關測試不回歸。驗證：三個指令皆 exit 0。
