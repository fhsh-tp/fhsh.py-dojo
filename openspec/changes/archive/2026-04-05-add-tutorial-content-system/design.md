## Context

本專案為 VitePress 靜態網站，已有完整的 Judge 挑戰基礎設施（`ChallengeView`、`challenge.data.ts`、`new-challenge.ts`），但 `docs/tutor/` 目錄與首頁尚未建立。`config.mts` 的 `nav` 與 `sidebar` 為空陣列。另一個既有專案已驗證 `nav.yml` + js-yaml 的 VitePress nav 管理模式，以及 `posts.data.ts` + `vpHelper.ts` 的內容 scaffold 模式。本設計在此脈絡下擴充教學內容系統。

## Goals / Non-Goals

**Goals:**

- 建立 `docs/tutor/` 多科目目錄結構與 frontmatter schema
- 以 config.mts 動態 sidebar + nav.yml 取代空白導航設定
- 提供 `pnpm new-tutor` 統一 scaffold workflow
- 實作 `tutor.data.ts` 全科目內容載入
- 首頁展示最新教學、分類教學、最新挑戰
- `ChallengeLink.vue` 讓 tutor 文章連結到 Judge 挑戰

**Non-Goals:**

- 實際 tutor 文章內容（by 後續 change）
- `tutor/alg/` 與 `tutor/ds/` 的課程內容
- 解答 / 解題說明功能
- 學習進度追蹤
- 搜尋功能整合

## Decisions

### nav.yml 管理靜態導航

採用 js-yaml 在 `config.mts` 載入 `.vitepress/nav.yml`，與現有另一專案的模式一致。Nav 項目數量少（4 項）且變動稀少，YAML 比 TypeScript 物件更易讀且版本控制友善。

**備選**：直接在 `config.mts` 寫靜態物件 → 已知可行但不一致，拒絕。

### 動態 sidebar builder 取代靜態 sidebar.yml

在 `config.mts` 中實作 `buildTutorSidebar()` 函式，於 build time 掃描 `docs/tutor/<subject>/chN/` 目錄，讀取各 `.md` 檔案的 frontmatter `title` 欄位，按檔名字母序排列（`index.md` 強制排首位，`1-1.md` < `1-2.md` 字母序自然正確）。

**備選**：靜態 `sidebar.yml`（現有另一專案的模式）→ 課程文章有明確的章節結構，動態產生零維護成本；若手動維護 YAML，每次新增章節都需同步更新，違反 DRY。

### subject 欄位從 URL 路徑解析，不在 frontmatter 重複宣告

`tutor.data.ts` 透過解析 URL（`/tutor/<subject>/…`）推導 `subject` 值，避免 frontmatter 與檔案位置之間的冗餘與潛在不一致。

**備選**：frontmatter 顯式宣告 `subject: py` → 彈性稍高但多一個必填欄位，拒絕。

### ChallengeLink.vue 直接 import challenge.data.ts

`ChallengeLink.vue` 接受 `slug: string` prop，直接 `import { data as challenges } from '…/docs/shared/challenge.data'`，在元件內查找對應題目。VitePress data files 在 build time 被編譯為靜態模組，theme 目錄下的 Vue 元件可直接 import。

**備選**：tutor .md 頁面自行 import data 再以 props 傳入 → 需要在每篇文章的 `<script setup>` 中重複查找邏輯，且 `new-tutor.ts` 產生的模板更複雜，拒絕。

### HomeView.vue 取代 ChallengeListView 作為首頁元件

`docs/index.md` 改為使用新的 `HomeView.vue`，原 `ChallengeListView` 保留並移至 `docs/challenge/index.md` 使用。

**備選**：修改現有 `ChallengeListView` 加入教學區塊 → 違反 Single Responsibility，且 challenge list page 仍需要純挑戰視圖，拒絕。

## Risks / Trade-offs

- [Risk] `buildTutorSidebar()` 在 `docs/tutor/` 為空時（build CI）可能產生警告 → Mitigation: 對空目錄優雅降級，回傳空陣列
- [Risk] VitePress alpha（2.0.0-alpha.16）API 可能與 1.x 有差異，`transformPageData` 等鉤子行為需驗證 → Mitigation: 所有 config 改動均在 dev 環境驗證後才納入
- [Risk] `ChallengeLink` 直接 import data file，若路徑 alias 設定不正確將導致 build error → Mitigation: 使用相對路徑，並在 spec 中明確規範路徑格式
