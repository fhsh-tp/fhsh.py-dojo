## Summary

把 pillbox-reminder(id 58)testcase_plan 的第一筆改為「題面範例一」literal(Q=2/週期 3 5/K=6→輸出 1 2 1 1 2 1),總筆數維持 6(暖身 band 3→2),與 id 57 的置首範例慣例一致。

## Motivation

同 pin-print-farm-example-first:執行面板預設 stdin 取自第一筆測資(ChallengeView.vue 的 defaultStdin=testcases[0].input 餵給 RunModal),置首範例讓學生按「執行」時的預設輸入可直接對照題面「動手推演(2 種藥)」逐步驗算。使用者已確認 id 58 比照辦理。

## Proposed Solution

- testcase_plan 宣告順序改為:範例 literal(2↵3 5↵6)→ 暖身 band count 2 → 壓力 band count 2 → 既有 tie literal(3↵2 3 6↵12),合計 6 筆。
- 主 spec `scheduling-challenge-series` 的 Testcase plan partitioning 同步:id 58 的 6 筆組成改為「1 筆題面範例 literal 置首 + 2 暖身 + 2 壓力 + 1 tie 邊界 literal」,並將「第一筆 SHALL 為題面範例」條款擴為兩題通用;TLE 門檻條款不變。

## Non-Goals (optional)

- 不動壓力 band 值域(探針定案值不變)與 TLE 門檻。
- 不動題面、generator、reference_solution、params。

## Impact

- Affected specs: `scheduling-challenge-series`(MODIFIED: Testcase plan partitioning)
- Affected code:
  - Modified: docs/challenge/pillbox-reminder.md(僅 testcase_plan 區塊)
  - New: (none)
  - Removed: (none)
- 建置影響:id 58 池重洗(plan 內容參與 seed),仍為 33 blocks × 6。
