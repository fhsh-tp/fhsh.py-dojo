## 1. 目錄結構與靜態導航

- [x] 1.1 建立 `docs/tutor/` 多科目目錄佈局：新增 `py/`, `alg/`, `ds/` 子目錄及各 `.gitkeep`，確認 tutor directory follows multi-subject layout
- [x] 1.2 建立 `.vitepress/nav.yml`，定義含 教學（py/alg/ds）與挑戰題庫的靜態導航；nav.yml defines static top navigation
- [x] 1.3 更新 `config.mts`：以 `js-yaml` 讀取 `nav.yml` 並賦值給 `themeConfig.nav`；nav.yml 管理靜態導航

## 2. tutor.data.ts 內容載入器

- [x] 2.1 建立 `docs/shared/tutor.data.ts`，宣告 `TutorArticle` 介面，使用 `createContentLoader('tutor/**/*.md', …)` 載入全部教學文章；content loader scans all tutor articles
- [x] 2.2 在 `transform()` 中實作 `subject` 欄位：從 URL 路徑 `/tutor/<subject>/…` 解析第一個 path segment；subject field is derived from URL path；subject 欄位從 URL 路徑解析，不在 frontmatter 重複宣告
- [x] 2.3 在 `transform()` 中實作 `isIndex` 欄位：讀取 `frontmatter.isIndex ?? false`；loader distinguishes index pages from section articles

## 3. 動態 Sidebar Builder

- [x] 3.1 在 `config.mts` 中實作 `buildTutorSidebar(docsDir: string)` 函式：掃描 `docs/tutor/<subject>/chN/`，讀取 frontmatter `title`，排序（index.md 置首，其餘字母序），產生 multi-sidebar 物件；buildTutorSidebar generates multi-sidebar at build time；動態 sidebar builder 取代靜態 sidebar.yml
- [x] 3.2 在 `buildTutorSidebar` 中處理空目錄邊界情況：目錄不存在或無 `.md` 檔案時回傳 `{}` 而不拋出錯誤
- [x] 3.3 設定 `themeConfig.sidebar` 為 `buildTutorSidebar(srcDir)` 的回傳值；no sidebar for challenge pages（不為 `/challenge/` 產生 sidebar key）

## 4. new-tutor.ts 腳本

- [x] 4.1 建立 `scripts/new-tutor.ts`：解析 `<subject> <chapter> <section>` 位置參數及 `--title`, `--description`, `--challenge` 選項；CLI script scaffolds a new tutor article file
- [x] 4.2 實作章節驗證：`<chapter>` 不符合 `ch<N>` 格式時以 code 1 退出並印出對應錯誤訊息；invalid chapter format
- [x] 4.3 實作目標檔案已存在檢查：已存在時以 code 1 退出並印出 `[new-tutor] ERROR: <path> already exists.`；output file already exists
- [x] 4.4 實作 `createdTime` 注入：使用 UTC+8 ISO 8601 格式（`YYYY-MM-DDTHH:mm:ss+08:00`）
- [x] 4.5 實作 index 頁模板差異化：`<section>` 為 `index` 時產生含 `isIndex: true` 的 frontmatter，並省略 `section` 與 `challenge` 欄位；generate index page scaffold
- [x] 4.6 新增 `"new-tutor"` script entry 至 `package.json`，透過 `npx tsx` 執行；npm script entry runs the tutor generator

## 5. ChallengeLink.vue 元件

- [x] 5.1 建立 `.vitepress/theme/components/tutor/ChallengeLink.vue`：接受 `slug: string` prop，以相對路徑 import `docs/shared/challenge.data`，查找對應挑戰；ChallengeLink renders a styled link to a challenge；ChallengeLink.vue 直接 import challenge.data.ts
- [x] 5.2 實作 unknown slug fallback：slug 不符合任何挑戰時渲染「挑戰題目尚未建立」佔位訊息而不拋出錯誤
- [x] 5.3 在 `.vitepress/theme/index.ts` 全域註冊 `ChallengeLink` 元件；component available without import in Markdown

## 6. HomeView.vue 與首頁改版

- [x] 6.1 建立 `.vitepress/theme/views/HomeView.vue` 骨架，接受 `tutorials: TutorArticle[]` 與 `challenges: Challenge[]` props；HomeView replaces ChallengeListView as the homepage component；HomeView.vue 取代 ChallengeListView 作為首頁元件
- [x] 6.2 實作 HomeView「最新教學」區塊：過濾 `isIndex === false`，依 `createdTime` 降序取前 3 筆，空陣列時顯示空狀態訊息；HomeView displays latest tutorial articles
- [x] 6.3 實作 HomeView「分類教學」區塊：依 `subject` → `chapter` 分組，chapter 升序，空群組不顯示；HomeView displays tutorials grouped by chapter
- [x] 6.4 實作 HomeView「最新挑戰」區塊：依 `id` 降序取前 3 筆，空陣列時顯示空狀態訊息；HomeView displays latest challenges
- [x] 6.5 更新 `docs/index.md`：import `tutor.data.ts` 與 `challenge.data.ts`，改用 `<HomeView :tutorials="tutorials" :challenges="challenges" />`
- [x] 6.6 新增 `docs/challenge/index.md`：使用 `layout: doc`，import `challenge.data.ts`，渲染 `<ChallengeListView :challenges="challenges" />`

## 7. 初始課程骨架頁面

- [x] 7.1 建立 `docs/tutor/py/index.md`：frontmatter 含 `layout: doc`, `title: Python 自學`, `isIndex: true`
- [x] 7.2 建立 `docs/tutor/py/ch1/index.md` 至 `docs/tutor/py/ch4/index.md`：frontmatter 含各模組標題（模組一～四）及 `isIndex: true`；tutor article frontmatter schema（index 頁部分）
