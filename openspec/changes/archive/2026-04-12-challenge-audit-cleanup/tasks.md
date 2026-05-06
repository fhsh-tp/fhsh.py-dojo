## 1. Mystery difficulty UI 對應（Mystery difficulty has explicit UI label and styling in all components）

- [x] [P] 1.1 Mystery difficulty has explicit UI label and styling in all components：在 `ChallengeCard.vue` 的 `difficultyClass` 新增 `mystery: 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700'`，`difficultyLabel` 新增 `mystery: '未知'`
- [x] [P] 1.2 在 `ChallengeLink.vue` 的 `difficultyLabel` 新增 `mystery: '未知'`，`difficultyClass` 新增 `mystery: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300'`
- [x] [P] 1.3 在 `AppHeader.vue` 的 `difficultyLabel` 新增 `mystery: '未知'`，`difficultyClass` 新增 `mystery: 'bg-gray-700 text-gray-100 dark:bg-gray-700 dark:text-gray-200'`

## 2. Data loader fallback 補齊（Data loader provides fallback values for algorithm and params）

- [x] 2.1 Data loader provides fallback values for algorithm and params：在 `docs/shared/challenge.data.ts` 的 `transform` 函式中，將 `algorithm: challenge.frontmatter.algorithm` 改為 `algorithm: challenge.frontmatter.algorithm ?? ''`，將 `params: challenge.frontmatter.params` 改為 `params: challenge.frontmatter.params ?? {}`

## 3. 移除冗餘 null guard（Search filter removes redundant null guards）

- [x] 3.1 Search filter removes redundant null guards：在 `ChallengeListView.vue` 搜尋篩選中，將 `(c.description ?? '').toLowerCase()` 改為 `c.description.toLowerCase()`，將 `(c.tags ?? []).some(...)` 改為 `c.tags.some(...)`，將 `(c.chapter ?? '').toLowerCase()` 改為 `c.chapter.toLowerCase()`

## 4. 驗證

- [x] 4.1 確認 TypeScript 編譯無錯誤，並驗證 dev server 正常運作
