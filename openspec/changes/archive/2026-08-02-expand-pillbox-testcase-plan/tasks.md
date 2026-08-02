## 1. 實作與驗證

- [x] 1.1 修改 docs/challenge/pillbox-reminder.md 的 testcase_plan,落實 spec 需求 Testcase plan partitioning 的 pillbox 20 筆條款:暖身 band count 2→9、壓力 band count 2→8(override 值域皆不變),於 tie literal 之前新增 literal「2↵7 9↵1」(K=1 單次提醒邊界,期望輸出單行 1),範例 literal 仍置首,合計 20 筆。驗收:yaml 解析後條目順序為 literal/9/8/literal/literal,總數 20,首條=範例一、第 19 條=「2↵7 9↵1」。
- [x] 1.2 pnpm build:pools 重建成功(id 58 變為 200 筆=10 blocks×20)後,vitest challenge-params + content-regression 全綠。驗收:build 零錯誤、vitest 零 fail。
- [x] 1.3 dev server sanity:id 58「執行」彈窗預設 stdin 仍為「2↵3 5↵6」;提交正解得 20/20 AC;提交逐分鐘掃解得 AC×12+TLE×8(範例+9 暖身+2 literal AC、8 壓力 TLE)。驗收:三項實測成立。
