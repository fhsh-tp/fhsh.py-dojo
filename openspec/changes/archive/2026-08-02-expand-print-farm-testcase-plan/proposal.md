## Summary

把 print-farm-schedule(id 57)的每場測資由 6 筆擴為 20 筆(10 暖身 + 8 壓力 + 2 literal),提高覆蓋密度;pillbox-reminder(id 58)維持 6 筆不變。

## Motivation

使用者(出題教師)手動驗題後指定 id 57 需要 20 筆測資——現行 6 筆對 medium 基礎排程題的配分與覆蓋密度偏低;id 58 因含 TLE 壓力筆(每筆判題成本高)維持 6 筆。

## Proposed Solution

- testcase_plan 依原三段結構等比放大:暖身 3→10、壓力 2→8、literal 1→2(新增「單一工單」邊界 m=2/n=1/工時 7→答案 7,與既有「機台多於工單」邊界互補)。
- 主 spec `scheduling-challenge-series` 的 Testcase plan partitioning 需求由「兩題一律 6 筆」改為「id 57 = 20 筆、id 58 = 6 筆」,其餘條款(literal 邊界指定、pillbox TLE 門檻)不變。
- 池結構隨之變為 floor(200÷20)=10 blocks;重建池後跑 challenge-params 與 content-regression 守門。

## Non-Goals (optional)

- 不動 pillbox-reminder 的 testcase_plan 與 TLE 門檻(探針定案值不變)。
- 不新增中間規模 band(n 介於 8~200 的過渡帶)——維持與原設計相同的三段結構,如需再另案。
- 不動題面、generator、reference_solution、params 值域。

## Impact

- Affected specs: `scheduling-challenge-series`(MODIFIED: Testcase plan partitioning)
- Affected code:
  - Modified: docs/challenge/print-farm-schedule.md(僅 testcase_plan 區塊)
  - New: (none)
  - Removed: (none)
- 建置影響:id 57 池重洗(seed 含 plan 內容)、10 blocks × 20 筆;判題單場 20 筆皆輕量計算,前端執行時間與 6 筆同量級。
