## 1. 資料層：category taxonomy 與 loader

- [x] 1.1 建立 `docs/shared/challenge-category.ts`：匯出 `CHALLENGE_CATEGORIES = ['python', 'apcs'] as const`、`ChallengeCategory` 型別、`resolveChallengeCategory(raw: unknown)`（已知值原樣回傳，其餘一律回 `'python'`、不得 throw），JSDoc 鏡射 `exercise-type.ts` 風格。完成判準：`pnpm typecheck` 綠。（覆蓋 Requirement: Challenge category taxonomy and resolver）
- [x] 1.2 建立 `docs/shared/challenge-category.test.ts`：(a) resolver 邊界四類——已知值、缺值（`undefined`/`null`）、typo 與大小寫（`'apsc'`/`'APCS'`）、非字串（`42`）；(b) 全檔掃描 `docs/challenge/*.md` frontmatter，任何未知 `category` 值以錯誤訊息指名該檔案讓測試失敗。完成判準：`pnpm test --run docs/shared/challenge-category.test.ts` 綠。（覆蓋 Requirement: Challenge category taxonomy and resolver）
- [x] 1.3 `Challenge` 介面（`.vitepress/theme/types.d/challenge.type.ts`）新增必填 `category: ChallengeCategory`；`docs/shared/challenge.data.ts` transform 以 `resolveChallengeCategory(challenge.frontmatter.category)` 填值。完成判準：`pnpm typecheck` 綠，此時站台行為不變（全部題目 resolver 結果照舊）。（覆蓋 Requirement: Challenge data model includes category field）

## 2. UI 分頁：列表頁、nav、完成計數

- [x] 2.1 `docs/challenges.md`：title 改「Python 挑戰」，`<script setup>` 改餵 `challenges.filter((c) => c.category === 'python')`。完成判準：`/challenges` 只列 python 題。（覆蓋 Requirement: Category-filtered catalogue pages）
- [x] 2.2 新增 `docs/apcs-challenges.md`：`layout: page`、title「APCS 挑戰」、`sidebar: false`，`<script setup>` 餵 `challenges.filter((c) => c.category === 'apcs')` 給 `ChallengeListView`。完成判準：`/apcs-challenges` 只列 apcs 題，搜尋與難度篩選行為與現行一致。（覆蓋 Requirement: Category-filtered catalogue pages）
- [x] 2.3 `.vitepress/nav.yml`：移除「挑戰題庫」，改為「Python 挑戰」→ `/challenges`、「APCS 挑戰」→ `/apcs-challenges` 平級兩項（Python 在前）。完成判準：nav 顯示兩入口且連結正確。（覆蓋 Requirement: nav.yml defines static top navigation）
- [x] 2.4 `ChallengeListView.vue` 完成計數改頁內自算：分子改為 `props.challenges.filter((c) => progress.isCompleted(c.slug)).length`，不再使用 `progress.completedCount`；分母維持 `props.challenges.length`；計數不受搜尋與難度篩選影響。完成判準：一題只計入所屬頁。（覆蓋 Requirement: Page-scoped completion count）

## 3. 首頁與返回分流

- [x] 3.1 [P] `HomeView.vue`：「最新挑戰」拆為「最新 Python 挑戰」「最新 APCS 挑戰」兩區塊——各以 category 過濾後依 id 降序取 3，「查看全部 →」分別連 `/challenges` 與 `/apcs-challenges`；任一類為空時沿用現有 `v-else` 空狀態訊息模式。`docs/index.md` 不改。完成判準：兩區塊各列該類最新 3 題、連結各自正確。（覆蓋 Requirement: HomeView displays latest challenges）
- [x] 3.2 [P] 返回分流：`AppHeader.vue` 新增選填 prop `backUrl`（預設 `'/challenges'`），「← 返回」改 `router.go(backUrl)`；`ChallengeView.vue` 以 `resolveChallengeCategory(frontmatter.category)` 算出 `listUrl` 傳入 `AppHeader`，錯誤態「返回列表」按鈕共用同一 `listUrl`。完成判準：apcs 題返回 `/apcs-challenges`、python 題與缺值題返回 `/challenges`。（覆蓋 Requirement: Category-aware back navigation）

## 4. 工具鏈與內容收尾

- [x] 4.1 [P] `scripts/new-challenge.ts`：新增 `--category python|apcs` 旗標（預設 `python`），非法值以 exit code 1 印出 `[new-challenge] ERROR: --category must be one of: python, apcs`（鏡射 `validateDifficulty` 模式）；frontmatter 模板一律輸出 `category:` 行；usage 字串同步。`scripts/new-challenge.test.ts` 補三情境：省略旗標（產出 `category: python`）、`--category apcs`（產出 `category: apcs`）、非法值（exit 1 與錯誤訊息）。完成判準：`pnpm test --run scripts/new-challenge.test.ts` 綠。（覆蓋 Requirement: CLI script scaffolds a new challenge file; Generated skeleton is valid and parseable）
- [x] 4.2 [P] `Usage.md` 補 `category` 欄位契約：選填、值域 `python`/`apcs`、預設 `python`、未知值 runtime 歸 `python` 且測試層指名檔案失敗。完成判準：文件與 `challenge-category.ts` 值域一致。
- [x] 4.3 [P] 四題 APCS frontmatter 各加一行 `category: apcs`：`docs/challenge/card-restack-count.md`、`docs/challenge/buffer-audit-log.md`、`docs/challenge/print-farm-schedule.md`、`docs/challenge/pillbox-reminder.md`。內文與其他欄位不動。完成判準：四題出現在 `/apcs-challenges`，`/challenges` 剩 54 題。

- [x] 2.5 新增 `.vitepress/nav.test.ts`：讀取 `nav.yml` 並斷言每個 `CATEGORY_LIST_URL` 值都有對應 `link`（單向 lockstep，nav 可自由攜帶非 category 連結）。完成判準：`pnpm test --run .vitepress/nav.test.ts` 綠。（覆蓋 Requirement: nav.yml defines static top navigation）

## 5. 全站驗證

- [x] 5.1 `pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠；有紅修到綠。完成判準：三命令 exit 0。
