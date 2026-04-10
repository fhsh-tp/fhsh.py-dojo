## 1. View-layer 型別修正（Challenge type is the single source of truth）

- [x] 1.1 Challenge type in challenge.type.ts is the single source of truth for view-layer fields：更新 `.vitepress/theme/types.d/challenge.type.ts`，將 `difficulty` 從 `'easy' | 'medium' | 'hard' | string` 改為 `'easy' | 'medium' | 'hard' | 'mystery'`（移除 `| string`，新增 `'mystery'` 對應 loader 預設值）

## 2. Data-layer 型別統一（No duplicate Challenge interface in data loader）

- [x] 2.1 在 `docs/shared/challenge.data.ts` 頂部新增 `import type { Challenge } from '../../.vitepress/theme/types.d/challenge.type'`，移除原本重複的 `Challenge` interface，新增 `interface DataChallenge extends Challenge { algorithm: string; params: object; testcase_count?: number }`
- [x] 2.2 將 `docs/shared/challenge.data.ts` 中 `declare const data` 的型別從 `Challenge[]` 改為 `DataChallenge[]`，並將 `transform` 函式的回傳型別從 `Challenge[]` 改為 `DataChallenge[]`

## 3. 防禦性 fallback 修正（Numeric fallbacks use nullish coalescing）

- [x] 3.1 Numeric fallbacks in content loader use nullish coalescing：在 `docs/shared/challenge.data.ts` 的 `transform` 函式中，將 `id: challenge.frontmatter.id || idx + 1` 改為 `id: challenge.frontmatter.id ?? idx + 1`，將 `testcase_count: challenge.frontmatter.testcase_count || 5` 改為 `testcase_count: challenge.frontmatter.testcase_count ?? 5`

## 4. 驗證

- [x] 4.1 確認 TypeScript 編譯無錯誤：執行型別檢查，驗證 `ChallengeListView.vue`、`ChallengeCard.vue`、`HomeView.vue`、`ChallengeLink.vue` 四個消費端元件皆無型別錯誤
