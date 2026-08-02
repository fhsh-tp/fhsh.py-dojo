## Summary

把 pillbox-reminder(id 58)的每場測資由 6 筆擴為 20 筆,結構對齊 id 57:1 筆題面範例 literal 置首 + 9 暖身 + 8 壓力 + 2 邊界 literal(新增「K=1 單次提醒」邊界,保留既有 tie 邊界)。

## Motivation

使用者(出題教師)指定 id 58 與 id 57 一致採 20 筆配置,提高覆蓋密度與配分空間。壓力筆 2→8 的判題成本已評估:TLE 解每筆以 op-counter 在 ~2.5s 內截斷(真 Pyodide 實測),8 筆合計遠低於前端 20 筆 × 6s 的整場預算。

## Proposed Solution

- testcase_plan 宣告順序:範例 literal(2↵3 5↵6)→ 暖身 band count 9(值域不變)→ 壓力 band count 8(值域不變,維持探針定案的 TLE 斷崖)→ 新 literal「2↵7 9↵1」(K=1,期望輸出單行 1)→ 既有 tie literal(3↵2 3 6↵12),合計 20 筆。
- 主 spec `scheduling-challenge-series` 的 Testcase plan partitioning 同步:id 58 改為 20 筆上述組成,置首範例條款與 TLE 門檻條款不變;pillbox 首筆 Scenario 的筆數描述同步更新,並新增 K=1 literal Example。
- 池結構變為 floor(200÷20)=10 blocks;重建池後跑守門測試與 dev 實測(含逐分鐘掃 AC×12+TLE×8)。

## Non-Goals (optional)

- 不動壓力 band 值域(探針定案值 periods 30000..50000、k 300..400 不變)。
- 不動題面、generator、reference_solution、params。

## Impact

- Affected specs: `scheduling-challenge-series`(MODIFIED: Testcase plan partitioning)
- Affected code:
  - Modified: docs/challenge/pillbox-reminder.md(僅 testcase_plan 區塊)
  - New: (none)
  - Removed: (none)
- 建置影響:id 58 池重洗為 200 筆(10 blocks × 20);TLE-heavy 提交的整場執行時間增至約 20~40 秒,仍在預算內。
