## 1. 實作與驗證

- [x] 1.1 修改 docs/challenge/pillbox-reminder.md 的 testcase_plan,落實 spec 需求 Testcase plan partitioning 的置首範例條款:新增第一個條目 literal「2↵3 5↵6」(題面範例一,期望輸出六行 1 2 1 1 2 1),暖身 band count 3→2,壓力 band 與 tie literal 不動,合計仍 6 筆。驗收:yaml 解析後條目順序為 literal/2/2/literal,總數 6,首條 literal 內容與題面範例一逐字元一致。
- [x] 1.2 pnpm build:pools 重建成功(id 58 仍 198 筆=33 blocks×6)後,vitest challenge-params + content-regression 全綠。驗收:build 零錯誤、vitest 零 fail。
- [x] 1.3 dev server sanity:id 58 頁面「執行」彈窗預設 stdin 為「2↵3 5↵6」;提交正解得 6/6 AC;提交逐分鐘掃解得 AC×4+TLE×2(範例+暖身×2+tie literal AC、壓力×2 TLE)。驗收:三項實測成立。
