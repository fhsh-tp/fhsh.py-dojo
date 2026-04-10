## Summary

統一 Challenge 型別定義、修正防禦性 fallback、收緊 difficulty union type，消除三項 3-agent 安全稽核中發現的型別安全隱患。

## Motivation

在 `add-challenge-search` 的 3-agent 安全稽核中，發現三個預先存在的型別問題：

1. **兩個發散的 `Challenge` interface（Medium）**：`challenge.type.ts`（view-layer）和 `challenge.data.ts`（data-layer）各自定義 `Challenge`，`tags` 在前者為必填、後者為選填，欄位也不一致，易導致型別漂移
2. **`||` fallback 靜默替換有效值（Low）**：`id` 和 `testcase_count` 使用 `||` 做 fallback，當 frontmatter 值為 `0` 時會被靜默替換為預設值
3. **`difficulty` union type 被 `| string` 架空（Low）**：`'easy' | 'medium' | 'hard' | string` 等同於 `string`，TypeScript 的型別窄化完全失效

這些問題觸及的檔案與 `add-challenge-search` 相同，趁此次變更一併修正。

## Proposed Solution

- 將 `challenge.type.ts` 定為 view-layer 唯一型別來源，`tags` 設為必填 `string[]`，`difficulty` 改為 `'easy' | 'medium' | 'hard' | 'mystery'`
- `challenge.data.ts` 移除重複的 `Challenge` interface，改為 `import type { Challenge }` 並定義 `interface DataChallenge extends Challenge` 擴充 data-only 欄位（`algorithm`、`params`、`testcase_count`）
- `id` 和 `testcase_count` 的 fallback 從 `||` 改為 `??`，保留 `0` 為有效值

## Non-Goals

- 不重構 `ChallengeView.vue` 或 `useChallengeRunner.ts` 的 frontmatter 存取方式（它們直接讀取 `frontmatter.value`，不經過 data loader）
- 不為 `params` 建立細緻的型別定義（`object` → `Record<string, ...>`），留待未來需要時處理
- 不新增 path alias（`@theme/`），維持現有相對路徑慣例

## Capabilities

### New Capabilities

- `challenge-type-unification`: Challenge 型別統一與防禦性 fallback 修正，涵蓋 interface 合併、nullish coalescing、difficulty union 收緊

### Modified Capabilities

（無）

## Impact

- 受影響的程式碼：
  - `.vitepress/theme/types.d/challenge.type.ts`（canonical view-layer type：`tags` 改必填、`difficulty` union 收緊）
  - `docs/shared/challenge.data.ts`（移除重複 interface、import + extends、`||` → `??`）
- 消費端元件（無需修改，僅需驗證編譯通過）：
  - `.vitepress/theme/views/ChallengeListView.vue`
  - `.vitepress/theme/views/HomeView.vue`
  - `.vitepress/theme/components/challenge/ChallengeCard.vue`
  - `.vitepress/theme/components/tutor/ChallengeLink.vue`
