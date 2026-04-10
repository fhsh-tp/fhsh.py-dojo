## 1. 資料模型擴充（Challenge data model includes chapter and description fields）

- [x] [P] 1.1 Challenge data model includes chapter and description fields：更新 `.vitepress/theme/types.d/challenge.type.ts`，新增 `chapter?: string` 與 `description?: string` 欄位（chapter 欄位格式為 `"ch1"`、`"ch2"` 等字串）
- [x] [P] 1.2 更新 `docs/shared/challenge.data.ts` content loader，在 `transform` 函式中從 frontmatter 擷取 `chapter` 和 `description`，缺少時預設為空字串（description 欄位來源為 frontmatter）

## 2. 挑戰題 Frontmatter 更新（Challenge frontmatter includes chapter and description）

- [x] 2.1 Challenge frontmatter includes chapter and description：為 `docs/challenge/*.md` 全部 35 個挑戰題的 frontmatter 補上 `chapter` 與 `description` 欄位。`chapter` 值根據 `docs/tutor/py/` 中 ChallengeLink 的引用位置決定（ch1 的題目標記為 `ch1`，ch2 標記為 `ch2`）。`description` 為一句話題目摘要。

## 3. 搜尋 UI 與篩選邏輯

- [x] 3.1 在 `ChallengeListView.vue` 難度篩選按鈕上方新增搜尋欄位（搜尋欄位位置與 UI）：使用 `<input type="search">` 佔滿容器寬度，placeholder 為「搜尋題目名稱、說明、標籤、章節...」（ChallengeListView displays a search input field）
- [x] 3.2 實作篩選邏輯：新增 `searchQuery` ref，將搜尋文字轉小寫後對 `title`、`description`、`tags.join(' ')`、`chapter` 進行 `includes()` 比對，任一欄位命中即匹配（Search filters challenges by text matching across multiple fields）。搜尋結果與難度篩選取交集 AND（Search and difficulty filter work together as intersection）

## 4. 驗證

- [x] 4.1 手動驗證：確認搜尋欄位正確顯示、輸入文字即時篩選、搜尋與難度篩選可同時作用、清空搜尋恢復原列表、無匹配時顯示空狀態訊息
