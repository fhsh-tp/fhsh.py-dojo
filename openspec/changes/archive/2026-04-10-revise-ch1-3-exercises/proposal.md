## Why

1-3.md 目前的「自己動手試試」區段只有 2 道無解答的自練題（成績等第、三角形判斷），缺乏鷹架設計。學生從閏年的詳解直接跳到無提示的題目，落差太大。需要重新設計為四層漸進式鷹架（★☆☆→★★★★），讓零基礎學生能一步步自學、不斷刷題，且每題都有獨特的生活情境避免無聊。

## What Changes

- 重寫 `docs/tutor/py/ch1/1-3.md` 的「自己動手試試」區段（約第 448–469 行）
- 新結構包含四個難度層級（Tier 1–4），共 10 道題目
- 每道題包含：情境化描述（3-5 行）、CT/數學素養提示、`<ChallengeLink>` 元件
- 層級之間有明確的技能說明，幫助學生選擇起始難度
- 保留現有的成績等第題目（移到 Tier 2），升級三角形判斷為三角形分類器（Tier 3）
- 保持 Phoenix 的對話式語氣與顏文字風格

## Non-Goals

- 不修改 1-3.md 的教學正文（布林值、if-elif-else、流程圖部分）
- 不修改閏年判斷器的主教學段落
- 不修改 Image Specification Appendix（由 Change B 處理）

## Capabilities

### New Capabilities

（無——此變更修改教學文章內容，不引入新的技術能力）

### Modified Capabilities

- `python-ch1-content`: 1-3 節的練習題區段從 2 題擴展為 10 題四層鷹架

## Impact

- 修改檔案：`docs/tutor/py/ch1/1-3.md`（「自己動手試試」區段重寫）
- 依賴：Change C（`create-ch1-new-challenges`）必須先完成，提供 challenge slug
