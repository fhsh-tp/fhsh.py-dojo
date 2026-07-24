## Problem

挑戰頁編輯器下方 action bar 的「下載紀錄」按鈕,點擊後面板以 `absolute` 向下展開,但 action bar 位於 `overflow-hidden` 且高度受限的 flex column 內,面板被祖先容器裁切:預設高度下學生看不到(或只看到一小截)姓名/班級欄位與下載按鈕,必須先展開「執行/提交」結果區把容器撐高才看得到,在 tablet 視窗更嚴重。另外該面板點擊外部不會關閉、按 Escape 也不會關閉,只能再點一次按鈕。

## Root Cause

`DownloadRecordButton.vue` 的面板是流內 `absolute right-0 mt-2`(向下開),而 z-index 無法逃離祖先的 overflow 裁切——這與 `EditorSettingsPopover.vue` 檔頭註解記載的同一個已知問題完全相同。設定齒輪當初已用「Teleport 到 body + fixed 定位向上開」解掉,但下載紀錄面板是另一個 change 實作的,未沿用該方案,也未實作外點/Escape 關閉。兩個 popover 各自為政,沒有互斥機制。

## Proposed Solution

抽出共用 composable `useAnchoredPopover`,封裝已在 `EditorSettingsPopover.vue` 驗證過的完整方案,並讓兩個 popover 都改用它:

1. **定位**:Teleport 到 body、`fixed` 定位、面板底緣貼觸發鈕上緣、右緣對齊觸發鈕右緣(向上開),含視窗邊界 clamp(`Math.max(8, ...)`)。
2. **關閉行為**:`mousedown` 外點關閉(沿用「拖曳分隔線前先關閉」的既有 gotcha 處理)、Escape 關閉、window resize 重定位、unmount 清理 listeners。
3. **互斥**:composable 內維護 module-level「目前開啟的 popover」registry,開啟任一 popover 時自動關閉另一個。
4. **下載面板專屬**:面板改 `v-show`(關閉重開後保留已填的姓名/班級)、加 `max-height` + `overflow-y-auto`(矮視窗時面板內部捲動而非頂出視窗)。
5. `EditorSettingsPopover.vue` 重構為使用同一 composable,對外行為不變(既有測試不改斷言全綠)。

## Non-Goals

- 不改動 action bar 版面配置、按鈕順序與樣式。
- 不改動下載內容格式(Markdown/JSON)、匯出邏輯與 IndexedDB 讀取。
- 不引入第三方 floating/popover 函式庫(floating-ui 等):現有錨定公式已驗證足夠,兩個 popover 尚不構成引入相依的理由。
- 不處理行動裝置直向手機的全螢幕 sheet 型 UI(目前站台以桌機/平板為主要情境)。

## Success Criteria

- 預設高度(未展開執行/提交結果區)下,點「下載紀錄」面板即完整可見,含桌面(1440×900)與 tablet(1024×768、768×1024)視窗。
- 下載面板點擊外部或按 Escape 即關閉;拖曳編輯器分隔線時面板先關閉不脫錨。
- 設定 popover 開啟時點「下載紀錄」,設定關閉、下載開啟;反向亦然(互斥)。
- 填入姓名後關閉再重開,姓名仍保留。
- `EditorSettingsPopover` 既有測試不修改斷言全數通過;`DownloadRecordButton` 既有下載流程測試全數通過。
- `pnpm typecheck`、`pnpm lint`、`pnpm test -- --run` 全綠。

## Impact

- Affected specs: anchored-popover(新)、progress-record-export(修改)、editor-settings(修改)
- Affected code:
  - New:
    - .vitepress/theme/composables/useAnchoredPopover.ts
    - .vitepress/theme/__tests__/useAnchoredPopover.spec.ts
  - Modified:
    - .vitepress/theme/components/editor/DownloadRecordButton.vue
    - .vitepress/theme/components/editor/EditorSettingsPopover.vue
    - .vitepress/theme/__tests__/DownloadRecordButton.spec.ts
  - Removed: (none)
