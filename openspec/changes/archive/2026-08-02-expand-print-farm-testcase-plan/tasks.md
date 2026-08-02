## 1. 實作與驗證

- [x] 1.1 修改 docs/challenge/print-farm-schedule.md 的 testcase_plan 為 20 筆,落實 spec 需求 Testcase plan partitioning 的 print-farm 條款:暖身 band count 3→10、壓力 band count 2→8(override 內容不變),新增第二個 literal「2↵1↵7」(單一工單邊界,期望輸出 7);其餘 frontmatter 與題面逐字不動。驗收:yaml 解析後三段 count 為 10/8 + literal×2,合計 20。
- [x] 1.2 pnpm build:pools 重建成功:print-farm-schedule 池變為 200 筆(10 blocks × 20)、pillbox-reminder 維持 198 筆(33 blocks × 6),無 input_budget 超標。驗收:build 輸出零錯誤且兩題筆數如上。
- [x] 1.3 node_modules/.bin/vitest --run scripts/challenge-params.test.ts scripts/content-regression.test.ts 全綠(id 57 新池下 reference_solution 全 AC)。驗收:vitest 零 fail。
- [x] 1.4 dev server 快速 sanity:id 57 頁面測資列表呈現 20 筆(前 10 小規模、中 8 大規模、末 2 筆固定 literal,第 20 筆輸入為 2/1/7)。驗收:頁面實際顯示與宣告順序一致。
