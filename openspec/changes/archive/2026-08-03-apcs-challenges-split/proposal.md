## Why

挑戰題庫目前只有單一列表頁 `/challenges`，Python 基礎題與新加入的 APCS 系列題（撲克牌重排計數、緩衝區稽核日誌、列印工坊排程、智慧藥盒提醒）混在同一頁。兩類題目的受眾與難度定位不同：前者對應教學章節的自學進度，後者對接 APCS 檢測。混排會讓零基礎學生誤入進階題而受挫，也讓準備 APCS 的學生難以聚焦。

## What Changes

- 題目 frontmatter 新增選填欄位 `category`（`python` | `apcs`，預設 `python`），由資料層 loader 以 resolver 統一補預設值與擋未知值；沿用既有 `exercise-type` resolver 模式。題目檔案**不搬動**，slug 與學生進度完全不受影響。
- 新增 `docs/apcs-challenges.md`（URL `/apcs-challenges`，title「APCS 挑戰」），與 `/challenges` 共用 `ChallengeListView`，僅以 `category` 過濾；`docs/challenges.md` title 改為「Python 挑戰」。
- nav bar 的單一「挑戰題庫」入口改為平級兩入口：「Python 挑戰」→ `/challenges`、「APCS 挑戰」→ `/apcs-challenges`。
- `ChallengeListView` 的「已完成 X / Y」分子改為頁內自算（以當頁題目 slug 逐一查詢完成狀態），修正拆頁後全站分子對上當頁分母的錯帳。
- 首頁「最新挑戰」區塊拆為「最新 Python 挑戰」與「最新 APCS 挑戰」兩區塊，各依 id 降序取 3 題，「查看全部 →」各自指向所屬列表頁。
- 挑戰頁 header 的「← 返回」與錯誤狀態的「返回列表」按鈕，由回首頁 `/` 改為依題目 `category` 分流回所屬列表頁。
- `scripts/new-challenge.ts` 新增 `--category python|apcs` 旗標（預設 `python`），scaffold 產出的 frontmatter 一律帶 `category` 欄位；`Usage.md` 補欄位契約。
- id 55–58 四題 frontmatter 加上 `category: apcs`。

## Capabilities

### New Capabilities

- `challenge-category-catalogue`: 題目 category 分類法（值域、預設、未知值解析）、雙列表頁的過濾契約、頁內完成計數、依 category 分流的返回導航。

### Modified Capabilities

- `challenge-search`: `Challenge` 資料模型新增 `category` 欄位（loader transform 補預設值）。
- `site-nav-sidebar`: nav.yml 的「挑戰題庫」單一入口改為「Python 挑戰」「APCS 挑戰」平級兩入口。
- `site-homepage`: HomeView 的「最新挑戰」單一區塊改為依 category 拆分的兩區塊，各自帶「查看全部」連結。
- `challenge-scaffold-script`: new-challenge script 新增 `--category` 旗標與對應驗證，frontmatter 模板帶 `category` 欄位。

## Impact

- Affected specs: 新增 `challenge-category-catalogue`；修改 `challenge-search`、`site-nav-sidebar`、`site-homepage`、`challenge-scaffold-script`。
- Affected code:
  - New:
    - docs/apcs-challenges.md
    - docs/shared/challenge-category.ts
    - docs/shared/challenge-category.test.ts
  - Modified:
    - docs/challenges.md
    - .vitepress/nav.yml
    - .vitepress/theme/types.d/challenge.type.ts
    - docs/shared/challenge.data.ts
    - .vitepress/theme/views/ChallengeListView.vue
    - .vitepress/theme/views/HomeView.vue
    - .vitepress/theme/views/ChallengeView.vue
    - .vitepress/theme/components/layout/AppHeader.vue
    - scripts/new-challenge.ts
    - scripts/new-challenge.test.ts
    - Usage.md
    - docs/challenge/card-restack-count.md
    - docs/challenge/buffer-audit-log.md
    - docs/challenge/print-farm-schedule.md
    - docs/challenge/pillbox-reminder.md
  - Removed: （無）
