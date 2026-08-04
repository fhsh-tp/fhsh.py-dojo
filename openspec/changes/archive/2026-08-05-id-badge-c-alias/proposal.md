## Why

挑戰 id(py001/apcs001)已顯示於目錄卡片並支援搜尋,但學生進入題目內頁後看不到 id,老師口頭指定題號時學生無法當場對照;同時 `/challenge/<id>` 別名路徑過長,不利課堂口頭傳達與手動輸入。兩者共享同一動機:讓學生在任何頁面都看得到 id,並能用最短路徑以 id 直達題目。`/challenge/<id>` 別名目前僅部署於 staging、從未進入 production release,現在整組替換為 `/c/<id>` 是零成本時機。

## What Changes

- 挑戰內頁頂欄(AppHeader)於標題左側新增 mono 低調配色 id badge(沿用卡片視覺語言、依頂欄底色調整):純顯示、無互動;id 缺漏或不符 `CHALLENGE_ID_PATTERN` 時 badge 整個不顯示、標題照常
- **BREAKING**(僅影響 staging,從未進 production):`_redirects` 別名規則由 `/challenge/<id> /challenge/<slug> 302` 整組改為 `/c/<id> /challenge/<slug> 302`;`/challenge/<id>` 不再轉址(回 404)
- id-shaped filename 守衛(generate-redirects 與 new-challenge scaffold)行為保留,拒絕理由改寫:`/c/` 子樹下 alias loop 風險消失,但 id 形狀的 slug 仍會造成目錄身分混淆
- Usage.md 的 id 欄位說明同步改寫別名敘述

## Capabilities

### New Capabilities

- `challenge-page-id-display`: 挑戰內頁頂欄顯示該題 id 的規格(顯示位置、來源與驗證、缺漏時的行為)

### Modified Capabilities

- `challenge-alias-redirects`: 別名規則來源路徑由 `/challenge/<id>` 改為 `/c/<id>`(轉址目標、302 語意、fail-loud 守衛均不變);部署站驗證情境同步改用 `/c/<id>`
- `challenge-scaffold-script`: id-shaped filename 拒絕理由改寫(不再以 /challenge/ 同名空間 loop 為由,改為目錄身分混淆),拒絕行為本身不變

## Impact

- Affected specs: `challenge-page-id-display`(新增)、`challenge-alias-redirects`、`challenge-scaffold-script`
- Affected code:
  - Modified:
    - .vitepress/theme/components/layout/AppHeader.vue
    - .vitepress/theme/views/ChallengeView.vue
    - .vitepress/theme/__tests__/AppHeader.spec.ts
    - .vitepress/theme/__tests__/ChallengeView.spec.ts
    - scripts/generate-redirects.ts
    - scripts/generate-redirects.test.ts
    - scripts/new-challenge.ts
    - scripts/new-challenge.test.ts
    - scripts/retired-challenges.json
    - Usage.md
  - New:
    - (none)
  - Removed:
    - (none)
