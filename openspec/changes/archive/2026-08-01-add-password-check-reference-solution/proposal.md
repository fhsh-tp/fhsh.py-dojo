## Summary

為 password-check(id 31,全站唯一 factory 型且無 reference_solution 的題目)補上 reference_solution,讓 content-regression 測試自動覆蓋全站最後一題。

## Motivation

2026-07-28 staging 全題庫 e2e 時發現 password-check 是唯一「factory 型 generator 且無 reference_solution」的題目——generator 輸出 JSON {input, expected_output},其本體不是學生正解,e2e 當時只能手寫解暫代。補上 reference_solution 後,content-regression 會以正式池樣本自動驗證「學生視角正解對 factory 轉換後輸入能得到期望輸出」,全站 56 題的 factory 缺口歸零。scripts/generate-pools.ts 的 runGenerator 對一般解會包裝成 {input: 原輸入, expected_output: stdout},scripts/content-regression.test.ts 已原生支援此比對路徑,無需改任何測試程式。

## Proposed Solution

- 在 docs/challenge/password-check.md frontmatter 新增 reference_solution:讀密碼與上限 K,迴圈逐行讀猜測,猜對印 OK 並 break,K 次皆錯以 for-else 印 LOCKED。輸入資料保證:猜對後不再有後續行、全錯時恰有 K 行,故不會觸發 EOF。
- 一併把主 spec openspec/specs/password-check-pool-gen/spec.md 的 Purpose 由 archive 佔位 TBD 補為正式描述(與 delta 應用不重疊)。
- 池不受影響:池 seed 僅含 slug/params/plan,reference_solution 不參與;以 build:pools 前後池檔 hash 一致驗證 byte-identical。

## Non-Goals

- 不改 generator、params、題目敘述與任何學生可見內容;不動判題行為(reference_solution 僅供建置期測試)。
- 不做 e2e(零執行期改動,池 byte-identical 由 hash 證明)。
- 不動其他題目與引擎。

## Impact

- Affected specs: `password-check-pool-gen`(ADDED 1 條 requirement:reference_solution 與 content-regression 覆蓋;Purpose 補正)
- Affected code:
  - Modified: docs/challenge/password-check.md(frontmatter 加一欄)、openspec/specs/password-check-pool-gen/spec.md(Purpose 段)
  - New: (無)
  - Removed: (無)
