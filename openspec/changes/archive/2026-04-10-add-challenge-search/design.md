## Context

挑戰題庫頁面（`ChallengeListView.vue`）目前僅提供難度篩選按鈕。隨著題目從 35 題持續增加，學生需要更快速的方式定位題目。目前的 Challenge 資料模型缺少 `chapter` 和 `description` 欄位，需要擴充。

現有資料流：`docs/challenge/*.md` frontmatter → `challenge.data.ts` content loader → `ChallengeListView.vue` → `ChallengeCard.vue`

## Goals / Non-Goals

**Goals:**

- 提供單一搜尋欄位，能同時比對 title、description、tags、chapter
- 搜尋與難度篩選可同時作用
- 搜尋為即時篩選（keystroke 觸發），不需按下搜尋按鈕
- 擴充 Challenge 資料模型以包含 chapter 與 description

**Non-Goals:**

- 不做模糊搜尋（fuzzy search）或權重排序，使用簡單的字串包含比對即可
- 不做章節下拉選單，章節篩選統一由搜尋欄位處理
- 不做搜尋 debounce（題目數量少，即時計算效能足夠）

## Decisions

### 搜尋欄位位置與 UI

搜尋欄位放置在難度篩選按鈕的上方，佔滿容器寬度。使用 `<input type="search">` 以獲得瀏覽器原生的清除按鈕（×）。包含 placeholder 提示搜尋範圍。

**替代方案：** 放在難度篩選同一行的右側 → 手機版空間不足，且視覺層級不明確。

### 篩選邏輯

搜尋文字轉為小寫後，對 `title`、`description`、`tags`（join 為字串）、`chapter` 四個欄位進行 `includes()` 比對。任一欄位命中即為匹配。搜尋與難度篩選取交集（AND）。

**替代方案：** 使用正則表達式搜尋 → 過度複雜，學生不需要正則搜尋功能。

### chapter 欄位格式

使用字串格式如 `"ch1"`、`"ch2"`，與教材目錄結構一致。在 frontmatter 中以 `chapter: ch1` 形式填寫。不使用數字格式（`1`、`2`），因為字串格式可直接用於搜尋比對且語義更清楚。

**替代方案：** 從 ChallengeLink 使用位置自動反推章節 → 耦合度高，且有些題目可能跨章出現，不可靠。

### description 欄位來源

在 frontmatter 新增 `description` 欄位，填寫一句話的題目摘要（與 markdown body 的第一段相同或精簡版本）。不使用 content loader 的 `excerpt` 功能，因為 excerpt 會載入整個 HTML 渲染結果，增加 bundle size。

**替代方案：** 啟用 `includeSrc: true` 並從 markdown 原始碼擷取 → bundle size 大幅增加，不適合靜態站台。

## Risks / Trade-offs

- [35 個 markdown 檔案需手動補 frontmatter] → 一次性工作，可透過腳本輔助或逐步補齊；缺少欄位時 description/chapter 預設為空字串，搜尋仍可正常運作
- [新增 chapter/description 欄位增加 data bundle size] → 每題增加約 50-100 bytes，35 題約 2-3.5 KB，影響可忽略
- [搜尋欄位在無題目時的空狀態] → 顯示「沒有符合條件的挑戰」，與現有難度篩選空狀態一致
