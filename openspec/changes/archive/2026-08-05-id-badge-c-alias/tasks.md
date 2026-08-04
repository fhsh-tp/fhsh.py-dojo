## 1. 內頁 id badge(TDD)

- [x] 1.1 [P] 擴充既有 `.vitepress/theme/__tests__/AppHeader.spec.ts`(沿用其 vitepress mock 與 mount helper),斷言(a)`id="py001"` 時存在 `data-testid="page-challenge-id"` 且文字恰為 `py001`、位於標題之前;(b)`id` 未傳或空字串時該元素不存在;(c)兩種情況下標題與難度徽章皆正常 render。先確認紅燈。(Requirement: Challenge page header displays the challenge id)
- [x] 1.2 `AppHeader.vue` 新增 optional prop `id`(預設 `''`),於 `<h1>` 前 render mono 低調小字 badge(色盤依頂欄底色調整)(`v-if` 空字串不 render、無任何互動),使 1.1 轉綠。(Requirement: Challenge page header displays the challenge id)
- [x] 1.3 `ChallengeView.vue` 以 `docs/shared/challenge-id` 的 `CHALLENGE_ID_PATTERN` 驗證 `frontmatter.id`(coerce 成字串,不合法 → `''`),經 `:id` 傳入 AppHeader;`pnpm typecheck` 通過。(Requirement: Challenge page header displays the challenge id)

- [x] 1.4 (round 1 audit 修正)`.vitepress/theme/__tests__/ChallengeView.spec.ts` 補 5 個頁面層 gate 測試:合法 id(py001)verbatim 顯示;59 / PY001 / "59" / 缺 id 均隱藏 badge 且 header 照常;以 mutation 自審驗證可攔截 gate 移除。(Requirement: Challenge page header displays the challenge id)

## 2. 別名規則換成 /c/(TDD)

- [x] 2.1 [P] `scripts/generate-redirects.test.ts`:所有行格式斷言改為 `/c/<id> /challenge/<slug> 302`,並新增斷言「輸出不含任何 `/challenge/<id>` 形式的來源路徑」;fail-loud 六情境(缺 id、壞 id、重複 id、非 slug 契約檔名、id-shaped 檔名、零檔案)斷言保留。先確認紅燈。(Requirement: Build step generates the Cloudflare Pages redirects file)
- [x] 2.2 `scripts/generate-redirects.ts`:`buildRedirects` 輸出行改為 `/c/${id} /challenge/${slug} 302\n`;檔頭 doc comment 與 id-shaped 錯誤訊息的理由改寫為「目錄身分混淆」(不再稱 /challenge/ 同名空間 loop);banner 與六種 fail-loud 行為不變,使 2.1 轉綠。(Requirement: Build step generates the Cloudflare Pages redirects file)

## 3. scaffold 訊息 wording 同步

- [x] 3.1 [P] `scripts/new-challenge.ts`:validateName 的 id-shaped 拒絕訊息與註解、checkRetired 的 id 訊息中 `/challenge/<id>` 敘述改為 `/c/<id>`/目錄身分混淆版本;`scripts/new-challenge.test.ts` pin 舊 wording 的斷言同步更新並通過(`retired-ledger.test.ts` 經查無 pin,未動);另 `scripts/retired-challenges.json` 的 `_comment` 別名敘述亦同步改為 `/c/<id>`(round 1 audit 修正)。(Requirement: CLI script scaffolds a new challenge file)

## 4. 文件同步

- [x] 4.1 [P] `Usage.md` id 欄位說明:別名敘述由 `/challenge/<id>` 改為 `/c/<id>`;通讀該段確認無其他殘留舊別名字樣(全檔 grep `/challenge/<id>` 為零)。(Requirement: Deployed alias URLs redirect to canonical slug URLs)

## 5. 全套驗證

- [x] 5.1 `pnpm test --run`、`pnpm typecheck`、`pnpm lint` 全綠;`pnpm build:redirects` 產出檔逐行皆為 `/c/` 規則且行數等於題目數。(Requirement: Build step generates the Cloudflare Pages redirects file)
- [x] 5.2 本機 `wrangler pages dev` 抽驗:`GET /c/py001` 回 3xx 且 Location 為 `/challenge/hello-world`;`GET /challenge/py001` 回 404;`GET /c/nonexistent` 回 404。(Requirement: Deployed alias URLs redirect to canonical slug URLs)
