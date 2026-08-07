## Problem

apcs009–apcs012 四題出貨時的 starter_code 帶有讀輸入迴圈與提示註解骨架，但使用者（維護者 Phoenix）希望這批題目的起始程式碼為**空白編輯器**，讓學生從零開始。另外 `bracket-check-challenges` 主 spec 的「Shared authoring constraints」要求 starter_code「讀輸入但不輸出」，與空白要求牴觸，需同步修訂。

## Root Cause

出題時沿用 scaffold 慣例（非空 starter 骨架），未向使用者確認這批競賽題的 starter 政策；spec 依當時實作寫死了骨架行為。

## Proposed Solution

四題 frontmatter 的 starter_code 改為空字串；`bracket-check-challenges` 主 spec 對應 SHALL 改為「starter_code SHALL 為空，未修改直接提交得 0/20」。expression-eval-challenges spec 無 starter 條款，不需修訂。

## Success Criteria

- 四題 frontmatter `starter_code` 皆為空字串；編輯器載入為空白（ChallengeView 以 `?? ''` 處理，空字串安全）
- 未修改直接提交＝無輸出 → 全 WA、0/20（比原骨架更不可能白拿分）
- challenge-params 冒煙、content-regression、typecheck、lint 全綠；literal／generator／params 不變，判題塊不受影響

## Impact

- Affected specs: `bracket-check-challenges`（MODIFIED：Shared authoring constraints）
- Affected code:
  - Modified: docs/challenge/prop-box-packing.md、docs/challenge/magazine-typeset-check.md、docs/challenge/snack-bar-register.md、docs/challenge/coupon-combo-quote.md
