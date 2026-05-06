## Summary

修正 pre-staging 3-agent 安全稽核中發現的三項 Low-severity 問題：`'mystery'` difficulty 缺少 UI 對應、data loader 的 `algorithm`/`params` 缺少 fallback、搜尋篩選中的冗餘 null guard。

## Motivation

在 `add-challenge-search` 與 `challenge-type-safety` 完成後的全面性 pre-staging 稽核中，三位對手角色（壞蛋、懶惰的開發者、搞混的開發者）共同識別出以下殘留問題：

1. **`'mystery'` difficulty 缺少 UI 對應**：`Challenge.difficulty` 的型別已包含 `'mystery'`，但 `ChallengeCard.vue`、`ChallengeLink.vue`、`AppHeader.vue` 的 `difficultyLabel` 和 `difficultyClass` 均未包含 `'mystery'` 項目。雖有 `??` fallback，但會顯示原始字串 "mystery" 而非友善的中文標籤
2. **`algorithm`/`params` 無 fallback**：`challenge.data.ts` 的 transform 中，`algorithm` 和 `params` 直接傳遞 frontmatter 值且無預設值，但 `DataChallenge` interface 宣告為必填。若 frontmatter 缺少這兩個欄位，runtime 值為 `undefined`，造成型別與實際不符
3. **冗餘 null guard**：`ChallengeListView.vue` 搜尋邏輯中的 `(c.tags ?? [])` 、`(c.description ?? '')` 、`(c.chapter ?? '')` 在型別統一後已不必要（loader 保證有值），應移除以反映正確的型別契約

## Proposed Solution

- 在 `ChallengeCard.vue`、`ChallengeLink.vue`、`AppHeader.vue` 的 `difficultyLabel` 新增 `mystery: '未知'`，`difficultyClass` 新增對應的灰色樣式
- 在 `challenge.data.ts` 的 transform 中為 `algorithm` 和 `params` 加上 `?? ''` 和 `?? {}` fallback
- 移除 `ChallengeListView.vue` 搜尋篩選中的冗餘 `??` guard

## Non-Goals

- 不在難度篩選按鈕中新增 `'mystery'` 選項（mystery 是 fallback 值，不應作為正式篩選類別）
- 不修改 `ChallengeView.vue` 或 `useChallengeRunner.ts` 的 frontmatter 存取方式

## Capabilities

### New Capabilities

- `challenge-audit-cleanup`: 稽核修正——mystery difficulty UI 對應、data loader fallback 補齊、冗餘 null guard 清理

### Modified Capabilities

（無）

## Impact

- 受影響的程式碼：
  - `.vitepress/theme/components/challenge/ChallengeCard.vue`（新增 mystery 的 label 和 class）
  - `.vitepress/theme/components/tutor/ChallengeLink.vue`（新增 mystery 的 label 和 class）
  - `.vitepress/theme/components/layout/AppHeader.vue`（新增 mystery 的 label 和 class）
  - `docs/shared/challenge.data.ts`（`algorithm`/`params` 加 fallback）
  - `.vitepress/theme/views/ChallengeListView.vue`（移除冗餘 `??` guard）
