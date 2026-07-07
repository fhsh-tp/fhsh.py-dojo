## Context

editor-settings v1 已上線兩個布林開關（autocomplete、closeBrackets），狀態 seam 為 `.vitepress/theme/composables/useEditorSettings.ts`——當初就以「defaults 合併、數值 clamp、schema 版本、SSR 安全」為設計目標，但 v1 只用到布林合併，clamp 與版本遷移尚未真正被行使。本 change 加入字級（`fontSize`）——第一個數值型設定——首次啟用這條路徑。

目前字級寫死在 `CodeEditor.vue` 的 `EditorView.theme({ '&': { ..., fontSize: '14px' } })`。編輯器的可切換行為已採 CodeMirror `Compartment` 即時 reconfigure（不重建、不丟游標與 undo），字級沿用同一模式。

約束：全站共用（沿用 v1 範圍）；localStorage 持久化；SSR 安全；繁中 UI；不得破壞既有 v1 儲存值。

## Goals / Non-Goals

**Goals**
- 使用者可在齒輪 popover 調整編輯器字級，範圍 `[10, 24]` px，預設 `14`（與現況一致）。
- 字級變更即時套用、不重建編輯器、保留游標與 undo。
- 資料契約穩健：非法／缺漏／舊版儲存值都收斂為合法設定，不拋例外。

**Non-Goals**
- 不做 font family、行高、Tab 寬度、行號、佈景、自動換行（各自後續 change）。
- 不做逐題字級。
- 不修 oneDark 亮暗未同步的既有問題。

## Decisions

### D1：字級範圍、預設、step — `[10, 24]`、預設 14、step 1
在 `editorConfig.ts` 新增 `FONT_SIZE_MIN = 10`、`FONT_SIZE_MAX = 24`、`FONT_SIZE_DEFAULT = 14`、`FONT_SIZE_STEP = 1`，作為 clamp、預設與 UI 步進的**單一事實來源**（避免像 v1 早期把數值散落各處）。預設 14 對齊目前寫死值，確保未改設定的使用者外觀不變。
- 替代方案：離散下拉選單（12/14/16/18）。捨棄理由——步進按鈕更直覺，且離散選單無法行使 clamp 邏輯（本 change 想要的正是通用數值 clamp 路徑）。

### D2：`fontSize` 正規化 — 先型別檢查、四捨五入取整、再 clamp
`normalizeEditorSettings` 對 `fontSize`：`typeof === 'number' && Number.isFinite` 才採用，否則回落 `FONT_SIZE_DEFAULT`；採用時 `Math.round` 取整後 clamp 到 `[FONT_SIZE_MIN, FONT_SIZE_MAX]`。順序為「取整 → clamp」，確保 `9.4 → 9 → 10`、`23.6 → 24 → 24`、`100 → 100 → 24`、`NaN/Infinity/字串 → 14`。
- 替代方案：只 clamp 不取整。捨棄理由——css px 用整數較乾淨，且步進以整數操作，浮點值來自竄改或舊資料，取整較保險。

### D3：schema 版本 `1 → 2`，additive 遷移
`EDITOR_SETTINGS_SCHEMA_VERSION` 改為 `2`。既有 v1 blob 沒有 `fontSize`，經 `normalizeEditorSettings` 的 defaults 合併補上 `14`，並將 `version` 改寫為 `2`；autocomplete／closeBrackets 既有選擇保留。此為純新增欄位的向前相容遷移，無破壞性資料轉換。
- 替代方案：不 bump 版本。捨棄理由——schema 形狀確實變了，誠實反映版本有利日後真正需要破壞性遷移時判讀。

### D4：字級以獨立 `fontSize` compartment 即時套用
在 `CodeEditor.vue` 新增 `fontSizeCompartment`，內容為 `EditorView.theme({ '&': { fontSize: \`${px}px\` } })`；同時將原本寫死於靜態 theme 的 `fontSize: '14px'` 移除（靜態 theme 保留 `height: 100%` 與 `.cm-scroller` 的 overflow／fontFamily）。既有的 settings `watch` 擴充為同時 reconfigure autocomplete、closeBrackets、fontSize 三個 compartment。
- 替代方案：直接改容器 DOM 的 inline style。捨棄理由——繞過 CodeMirror 佈局管理，且與 v1 既有 compartment 模式不一致。

### D5：popover 字級控制為步進器（− 數字 +）
在 `EditorSettingsPopover.vue` 兩個開關之後加入一列：`−` 按鈕、目前字級數字（如 `14px`）、`+` 按鈕。`−` 在達 `FONT_SIZE_MIN` 時 `disabled`，`+` 在達 `FONT_SIZE_MAX` 時 `disabled`；點擊以 `FONT_SIZE_STEP` 增減後仍經 clamp 寫回 `settings.value.fontSize`。「重設為預設值」沿用既有 reset，已因 `DEFAULT_EDITOR_SETTINGS` 包含 `fontSize` 而自動還原為 14。
- 替代方案：拖曳 slider。捨棄理由——popover 空間小、觸控精度差，步進器對整數範圍更精確。

## Implementation Contract

**資料形狀（`useEditorSettings.ts`）**
- `EditorSettings` 介面新增 `fontSize: number`。
- `EDITOR_SETTINGS_SCHEMA_VERSION = 2`；`DEFAULT_EDITOR_SETTINGS.fontSize = FONT_SIZE_DEFAULT`（14）、`version = 2`。
- `normalizeEditorSettings(raw)` 對 `fontSize`：非有限數字 → `FONT_SIZE_DEFAULT`；有限數字 → `clamp(Math.round(n), FONT_SIZE_MIN, FONT_SIZE_MAX)`。既有 boolean 正規化與「不拋例外」保證不變。

**常數（`editorConfig.ts`）**
- 匯出 `FONT_SIZE_MIN = 10`、`FONT_SIZE_MAX = 24`、`FONT_SIZE_DEFAULT = 14`、`FONT_SIZE_STEP = 1`。

**即時套用（`CodeEditor.vue`）**
- 新增 `fontSizeCompartment`，初值由 `settings.value.fontSize` 決定；靜態 theme 不再含 `fontSize`。
- settings `watch` 監看 `[autocomplete, closeBrackets, fontSize]`，任一變更 dispatch 對應三 compartment 的 reconfigure；字級變更後編輯器字級即時改變，游標位置與 undo 歷史保留（不呼叫 `new EditorView`）。

**UI（`EditorSettingsPopover.vue`）**
- 新增字級列：`data-testid="font-size-decrease"`、`data-testid="font-size-value"`（顯示目前值）、`data-testid="font-size-increase"`。
- `−` 在 `fontSize <= FONT_SIZE_MIN` 時 disabled；`+` 在 `fontSize >= FONT_SIZE_MAX` 時 disabled。
- 點 `+`／`−` 後 `settings.value.fontSize` 變為 clamp 後的新值。

**驗收（測試目標）**
- `useEditorSettings.spec.ts`：新增字級 clamp 表格案例（見 spec Example）與 v1→v2 遷移案例（`{version:1, autocomplete:false}` → 含 `fontSize:14`、`version:2`，保留 `autocomplete:false`）。
- `EditorSettingsPopover.spec.ts`：新增字級步進案例（`+`／`−` 更新共享設定、邊界 disabled）。
- `editorFontSize.spec.ts`（新檔，真實 CodeMirror 堆疊）：字級 compartment 初始套用正確 px、reconfigure 後 DOM 反映新字級。
- `pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠（既有 MermaidDiagram flaky 不計）。

**In scope**：`fontSize` 欄位、常數、compartment、popover 步進器、上述測試。
**Out of scope**：其他編輯器設定項、逐題設定、oneDark 亮暗同步。

## Risks / Trade-offs

- [舊 v1 blob 遷移出錯導致既有選擇遺失] → `normalizeEditorSettings` 以 defaults 合併保留既有布林欄位，並加 v1→v2 遷移測試案例守門。
- [字級變更觸發 CodeMirror 重排造成閃動或捲動跳動] → 沿用 compartment reconfigure（非 rebuild），並在整合測試確認游標與 undo 保留；字級 px 為整數避免次像素抖動。
- [step/範圍常數與正規化 clamp 不一致，UI 能設出被 normalize 改寫的值] → 三者共用 `editorConfig.ts` 常數，單一事實來源。

## Migration Plan

無資料庫。localStorage 遷移為讀取時自動進行（lazy）：使用者下次載入頁面時 `normalizeEditorSettings` 補上 `fontSize` 並改寫 `version` 為 2，無需一次性腳本、無停機。回滾時 v2 blob 對舊碼而言多一個未知欄位，舊 `normalize` 會忽略之，不致崩潰。
