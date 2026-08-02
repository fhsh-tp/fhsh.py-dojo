## 1. 實作與驗證

- [x] 1.1 修改 docs/challenge/print-farm-schedule.md 的 testcase_plan,落實 spec 需求 Testcase plan partitioning 的置首範例條款:新增第一個條目 literal「2↵4↵2 3 5 7」(題面範例一,期望輸出 10),暖身 band count 10→9,其餘條目與順序不動,合計仍 20 筆。驗收:yaml 解析後條目順序為 literal/9/8/literal/literal,總數 20,首條 literal 內容與題面範例一逐字元一致。
- [x] 1.2 pnpm build:pools 重建成功(id 57 仍 200 筆=10 blocks×20)後,vitest challenge-params + content-regression 全綠。驗收:build 零錯誤、vitest 零 fail。
- [x] 1.3 dev server sanity:id 57 頁面「執行」面板預設 stdin 為「2↵4↵2 3 5 7」(=testcases[0].input=範例一),提交正解得 20/20 AC。驗收:兩者實測成立。
