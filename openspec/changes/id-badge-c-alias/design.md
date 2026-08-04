## Context

challenge-id-revamp(已 archive)引入字串 id(py001/apcs001):id 顯示於目錄卡片(ChallengeCard 的 `data-testid="challenge-id"` mono 淺灰 badge)、支援序號感知搜尋、並由 `scripts/generate-redirects.ts` 產生 `/challenge/<id> /challenge/<slug> 302` 別名規則。該別名僅部署至 staging,從未進入 production release。

內頁(ChallengeView)的標題只存在於 `AppHeader.vue` 的單行頂欄(`← 返回 │ 標題 [難度] … 主題切換`),ProblemPanel 僅 render markdown 內文、不含標題,因此內頁目前沒有任何 id 顯示。

## Goals / Non-Goals

**Goals:**

- 學生在挑戰內頁能直接看到該題 id(與卡片同款視覺語言)
- 提供 `/c/<id>` 短別名,課堂口頭傳達與手動輸入成本最小化
- 別名規則整組替換(非並存),避免雙命名空間長期維護

**Non-Goals:**

- id badge 不做任何互動(不可點擊、無 tooltip、無複製短網址)——需求出現再補(YAGNI,已於討論定案)
- `/c/` 不接受 slug,只接受 id——slug 已有 `/challenge/<slug>` 正式網址
- 不保留 `/challenge/<id>` 舊別名——僅存在於 staging,從未面世,保留無受益者
- 不動卡片 badge、搜尋行為、id scheme 本身

## Decisions

1. **內頁 id 放 AppHeader 行內,不堆疊、不放 ProblemPanel**:頂欄維持單行高度,寫程式頁面的垂直空間留給編輯器;放 ProblemPanel 會隨題目敘述捲動而消失。樣式沿用 ChallengeCard badge 的視覺語言(mono、低調、小字),色盤依頂欄底色調整以維持可讀性。
2. **id 經由 prop 傳入 AppHeader,由 ChallengeView 負責驗證**:AppHeader 是展示元件,收到什麼就顯示什麼(空字串則不 render);`CHALLENGE_ID_PATTERN` 驗證放在 ChallengeView 取 `frontmatter.id` 之處,與 `challenge.data.ts` 的 sanitize-to-'' 慣例一致(不合法 → 傳空字串 → badge 不顯示)。驗證邏輯不重複實作,直接 import `docs/shared/challenge-id`。
3. **`/c/<id>` 每題一條 static 規則直達 slug(單跳),不用 splat**:splat(`/c/* /challenge/:splat`)雖只佔 1 條 dynamic 規則,但變成兩跳 302、`/c/亂字` 會轉去 `/challenge/亂字`、且佔據整個 `/c/*` 子樹。static 規則 59 條遠低於 CF Pages 2000 條上限;理論天花板(py999+apcs999=1998 條)仍在上限內。
4. **維持 302**:slug 改名時避免瀏覽器永久快取舊映射,與既有規則語意一致。
5. **id-shaped filename 守衛保留、rationale 改寫**:`/c/` 子樹與 `/challenge/` 分離後,id 形狀的 slug 不再與別名規則同名空間互撞(loop 風險消失),但仍會造成「目錄身分混淆」——例如 py001.md 檔案的 frontmatter id 若是 py002,`/challenge/py001`(slug)與 `/c/py001`(id)會指向不同題目。守衛照舊 fail-loud,僅改註解與錯誤訊息的理由敘述。

## Implementation Contract

**Behavior**

- 挑戰內頁頂欄在標題左側顯示該題 id(如 `py001`),mono 低調小字(色盤依頂欄底色調整);id 缺漏或不符 `^(py|apcs)\d{3}$` 時 badge 不 render(標題、難度、返回、主題切換不受影響)
- 部署站上 `GET /c/<id>` 回 3xx,Location 為該題的 extensionless slug 路徑 `/challenge/<slug>`;`/challenge/<id>` 不再有轉址規則(自然 404)
- `pnpm build:redirects` 產出的 `docs/public/_redirects` 每題恰一行 `/c/<id> /challenge/<slug> 302`,依 id code-unit 排序,檔首保留 generated banner

**Interface / data shape**

- `AppHeader.vue` props 新增 `id?: string`(預設 `''`);空字串 → 不 render badge;badge 帶 `data-testid="page-challenge-id"`(與卡片的 `challenge-id` 區隔)
- `ChallengeView.vue` 計算 `const challengeId = CHALLENGE_ID_PATTERN.test(String(frontmatter.value.id ?? '')) ? String(frontmatter.value.id) : ''` 並以 `:id` 傳入 AppHeader
- `buildRedirects(files)` 回傳值行格式改為 `/c/<id> /challenge/<slug> 302\n`;函式簽名、fail-loud 條件(缺 id、壞 id、重複 id、非 slug 契約檔名、id-shaped 檔名、零檔案)全部不變

**Failure modes**

- id 不合法:內頁 badge 靜默隱藏(與 challenge.data.ts sanitize-to-'' 一致;內頁不因壞 id 崩潰)
- generate-redirects 的六種 fail-loud 條件維持 exit non-zero 並指名檔案,錯誤訊息中 id-shaped 的理由敘述更新
- `/c/<不存在的id>`:無對應規則,CF 回 404(不做 catch-all)

**Acceptance criteria**

- 擴充既有 `.vitepress/theme/__tests__/AppHeader.spec.ts`:合法 id → badge 顯示且文字 verbatim;空字串/未傳 → badge 不存在;標題與難度不受 id 影響
- `generate-redirects.test.ts` 既有 13 測全數改斷言 `/c/` 行格式後通過;id-shaped、零檔案、重複 id 等 fail-loud 測試不變
- `new-challenge.test.ts` 若有 pin 到 `/challenge/<id>` 字樣的訊息斷言,同步更新
- `pnpm test --run`、`pnpm typecheck`、`pnpm lint` 全綠
- 本機 `wrangler pages dev` 抽驗:`/c/py001` → 302 → `/challenge/hello-world`;`/challenge/py001` → 404

**Scope boundaries**

- In scope:AppHeader/ChallengeView 顯示、generate-redirects 規則格式與 wording、new-challenge wording、Usage.md 敘述、相關測試
- Out of scope:卡片 badge、搜尋、id scheme、retired ledger 行為、pool/judge 管線、production release 流程

## Risks / Trade-offs

- **staging 期間已流出 `/challenge/<id>` 連結的風險**:別名上線至 staging 僅一日、對象是維護者本人,無學生流量;風險接受
- **`/c/` 命名空間佔用**:未來若要出 `/c/` 開頭的頁面會與別名規則衝突;以 static 規則(僅精確路徑)取代 splat 已把佔用縮到最小
- **badge 靜默隱藏 vs fail-loud**:內頁選擇靜默隱藏與資料層慣例一致;壞 id 的 fail-loud 守門已由 generate-redirects 與 content-regression 測試承擔,顯示層不重複把關
