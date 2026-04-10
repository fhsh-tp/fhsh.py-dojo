## Why

目前挑戰題庫頁面（ChallengeListView）僅支援難度篩選，當題目數量持續增加後，學生難以快速找到特定題目。需要新增搜尋功能，讓學生能透過章節、題目名稱、題目說明、tag 等條件快速定位題目。

## What Changes

- 在 ChallengeListView 新增搜尋欄位（文字輸入），支援即時篩選
- 搜尋範圍涵蓋：題目名稱（title）、題目說明（description）、標籤（tags）、所屬章節（chapter）
- 在 Challenge 資料模型中新增 `chapter` 與 `description` 欄位
- 更新 challenge content loader 以載入新欄位
- 為每道挑戰題的 frontmatter 補上 `chapter` 與 `description` 欄位
- 搜尋與現有的難度篩選可同時作用（聯集篩選）

## Non-Goals

- 不做伺服器端搜尋或全文索引（VitePress 為靜態站台，純前端篩選即可）
- 不做分頁功能（題目數量尚在百題以內）
- 不做搜尋歷史或自動建議（autocomplete）
- 不做章節獨立下拉選單篩選（統一用搜尋欄位處理，輸入章節編號即可篩選）

## Capabilities

### New Capabilities

- `challenge-search`: 挑戰題庫頁面的客戶端搜尋功能，包含搜尋欄位 UI、多欄位即時篩選邏輯、以及 Challenge 資料模型的 chapter/description 擴充

### Modified Capabilities

（無）

## Impact

- 受影響的程式碼：
  - `.vitepress/theme/views/ChallengeListView.vue`（新增搜尋欄位 UI 與篩選邏輯）
  - `.vitepress/theme/types.d/challenge.type.ts`（新增 `chapter`、`description` 欄位）
  - `docs/shared/challenge.data.ts`（擴充 loader 載入 chapter、description）
  - `docs/challenge/*.md`（35 個挑戰題 frontmatter 補上 chapter、description）
