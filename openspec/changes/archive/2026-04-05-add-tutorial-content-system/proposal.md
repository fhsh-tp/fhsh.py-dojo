## Why

目前 `docs/tutor/` 與 `docs/challenge/` 皆為空目錄，網站缺乏教學內容架構。為了能讓課程內容依據大綱逐步填入，並確保每次新增文章或題目時有一致的 workflow，需要先建立完整的內容系統基礎設施。

## What Changes

- 新增 `docs/tutor/` 多科目目錄結構（py / alg / ds），並定義 tutor 文章的 frontmatter schema
- 新增 `scripts/new-tutor.ts` 腳本，統一 tutor 文章的 scaffold 方式（平行於現有的 `new-challenge.ts`）
- 新增 `docs/shared/tutor.data.ts` 內容載入器，掃描全部 `tutor/**/*.md` 並以結構化資料輸出
- 新增 `.vitepress/nav.yml` 與動態 sidebar 產生邏輯，取代目前 `config.mts` 中的空陣列
- 新增 `ChallengeLink.vue` 元件，讓 tutor 文章底部可以連結到對應的 Judge 挑戰
- 重新設計首頁，呈現「最新教學」、「分類教學」、「最新挑戰」三個區塊

## Non-Goals

- 解答（解題說明）內容：留到後續 change 實作
- `tutor/alg/` 與 `tutor/ds/` 的實際文章內容：架構建立後由獨立 change 填充
- 進度追蹤 / 學習紀錄功能：不在此次 scope

## Capabilities

### New Capabilities

- `tutor-article-structure`: `docs/tutor/` 多科目目錄佈局與 tutor 文章 frontmatter schema（title、description、subject、chapter、section、createdTime、challenge）
- `tutor-scaffold-script`: `scripts/new-tutor.ts` CLI 腳本，接受 `<subject> <chapter> <section>` 並產生符合 schema 的 tutor 文章骨架，自動注入 `createdTime`
- `tutor-data-loader`: `docs/shared/tutor.data.ts`，使用 VitePress `createContentLoader` 掃描 `tutor/**/*.md`，輸出含 `subject`（從路徑解析）的結構化資料陣列
- `site-nav-sidebar`: `.vitepress/nav.yml`（靜態）+ `config.mts` 中動態掃描 `docs/tutor/` 產生 multi-sidebar 物件的函式
- `challenge-link-component`: `.vitepress/theme/components/tutor/ChallengeLink.vue`，接受 challenge slug，查詢 `challenge.data.ts` 後渲染帶難度 badge 的連結卡片
- `site-homepage`: `HomeView.vue` 取代現有首頁 `ChallengeListView`，呈現最新教學（`createdTime` 降序、顯示 3 篇）、分類教學（依 chapter 分組）、最新挑戰（`id` 降序、顯示 3 題）

### Modified Capabilities

（無）

## Impact

- Affected specs: 全部為新建 capabilities（見上方）
- Affected code:
  - `.vitepress/config.mts` — 加入 `js-yaml` 載入 `nav.yml`、新增動態 sidebar builder 函式
  - `.vitepress/nav.yml` — 新增檔案
  - `.vitepress/theme/components/tutor/ChallengeLink.vue` — 新增檔案
  - `docs/shared/tutor.data.ts` — 新增檔案
  - `docs/index.md` — 重新設計，改用 `HomeView.vue`
  - `docs/challenge/index.md` — 新增獨立挑戰列表頁
  - `docs/tutor/py/index.md`、`docs/tutor/py/ch1/index.md`（及各章節）— 新增目錄結構
  - `scripts/new-tutor.ts` — 新增檔案
  - `package.json` — 新增 `new-tutor` script entry
