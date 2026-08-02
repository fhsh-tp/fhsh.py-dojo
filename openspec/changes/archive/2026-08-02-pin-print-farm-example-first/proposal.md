## Summary

把 print-farm-schedule(id 57)testcase_plan 的第一筆改為「題面範例一」literal(m=2/n=4/工時 2 3 5 7→答案 10),總筆數維持 20(暖身 band 10→9)。

## Motivation

挑戰頁「執行」面板的預設 stdin 取自第一筆測資(ChallengeView.vue 的 defaultStdin = testcases[0].input)。現行第一筆是暖身 band 隨機值,學生按「執行」看到的輸入與題面範例不同;釘為範例一後,預設執行輸入可直接對照題面「動手推演」逐步驗算,教學回饋一致。

## Proposed Solution

- testcase_plan 宣告順序改為:範例 literal(2↵4↵2 3 5 7)→ 暖身 band count 9 → 壓力 band count 8 → 既有兩筆 literal(機台多於工單、單一工單),合計 20 筆。
- 主 spec `scheduling-challenge-series` 的 Testcase plan partitioning 同步:id 57 的 20 筆組成改為「1 筆題面範例 literal 置首 + 9 暖身 + 8 壓力 + 2 邊界 literal」,並明文規定第一筆 SHALL 為題面範例(使執行面板預設輸入=範例輸入)。

## Non-Goals (optional)

- 不動 pillbox-reminder(id 58)——同樣手法可套用(其範例一 2↵3 5↵6),如需另案。
- 不動前端 defaultStdin 邏輯。

## Impact

- Affected specs: `scheduling-challenge-series`(MODIFIED: Testcase plan partitioning)
- Affected code:
  - Modified: docs/challenge/print-farm-schedule.md(僅 testcase_plan 區塊)
  - New: (none)
  - Removed: (none)
- 建置影響:id 57 池重洗(plan 內容參與 seed),仍為 10 blocks × 20。
