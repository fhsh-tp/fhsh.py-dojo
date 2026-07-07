## Why

有程式底子的學生在 v1 編輯器設定（自動完成、括號自動閉合）之後，進一步反映預設字級偏小、長時間閱讀吃力，且不同螢幕（教室投影、筆電、平板）合適的字級不同。字級是 editor-settings 規劃時明確延後的第一個後續項目，也是第一個**數值型**設定——正好啟用 `useEditorSettings.ts` 當初就為「數值 clamp／schema 版本遷移」預留、但 v1 尚未用到的機制。

## What Changes

- 在 editor-settings 資料契約新增數值欄位 `fontSize`（單位 px），預設 `14`，與目前編輯器外觀一致（目前 14px 寫死在 `EditorView.theme`）。
- `normalizeEditorSettings` 首次處理數值欄位：非數字或非有限值時回落預設；數字則四捨五入為整數並 clamp 到合法範圍 `[10, 24]`。
- schema 版本由 `1` 升到 `2`；既有 v1 儲存值（沒有 `fontSize`）讀取時自動補上預設 `14`，不丟失既有的 autocomplete／closeBrackets 選擇、不拋例外。
- 將目前寫死於 `EditorView.theme` 的 `fontSize: '14px'` 移入新的 CodeMirror `Compartment`，由 `useEditorSettings` 的 `fontSize` 驅動；字級變更即時套用、不重建編輯器、保留游標與 undo 歷史（沿用 v1 的 compartment reconfigure 模式）。
- 齒輪 ⚙ popover 新增字級控制項：`−` / `+` 步進按鈕（step 1）與目前字級數字顯示；達下限時 `−` 停用、達上限時 `+` 停用；「重設為預設值」一併將字級還原為 `14`。

## Non-Goals (optional)

- 不做字型家族（font family）切換、行高（line height）、Tab 寬度、行號開關、佈景切換、自動換行——這些仍留待各自後續 change。
- 不做逐題（per-challenge）字級；沿用 v1 的全站共用範圍。
- 不在此 change 修正 oneDark 未跟站台亮暗同步的既有問題。

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `editor-settings`: 資料契約新增數值型 `fontSize` 欄位並要求 clamp 正規化與 schema v1→v2 遷移；齒輪 popover 新增字級步進控制項。

## Impact

- Affected specs: `editor-settings`（新增「Adjustable editor font size」需求；修改「Settings data contract with defaults merge and normalization」需求以涵蓋數值 clamp）
- Affected code:
  - Modified:
    - `.vitepress/theme/composables/useEditorSettings.ts`（新增 `fontSize`、bump schema 版本、數值 clamp 正規化）
    - `.vitepress/theme/composables/editorConfig.ts`（新增字級範圍／預設／step 常數）
    - `.vitepress/theme/components/editor/CodeEditor.vue`（新增 fontSize compartment、移除寫死字級、watch 加入 fontSize）
    - `.vitepress/theme/components/editor/EditorSettingsPopover.vue`（新增字級步進控制項）
  - New:
    - `.vitepress/theme/__tests__/editorFontSize.spec.ts`（字級 clamp／遷移／即時套用的整合測試）
