## 1. 骨架與雙實作

- [x] 1.1 以 `pnpm new-challenge exam-collect-verify --title 收卷順序驗證 --difficulty medium --category apcs --type competition` 建立骨架；確認自動配發的 id 未與現有題衝突、檔案位於 docs/challenge/exam-collect-verify.md。（覆蓋 Requirement: Exam-collection challenge content 的 frontmatter 基本欄位）
- [x] 1.2 先寫互驗腳本再填實作（TDD）：scratchpad 腳本實作暴力 DFS 基準，接著撰寫 generator（反轉＋雙指標貪婪、每組輸出一行計數）與 reference_solution（位置區間外擴法，零共用遍歷邏輯），跑 N≤6 全排列窮舉與 3000 組 N=800 隨機互驗，驗收標準＝三方零不一致，且判定語意逐字對齊 Requirement: Report-verification semantics（含非排列回報不合法、輸出 T 行計數）。（覆蓋 Requirement: Exam-collection dual implementation and verification、Requirement: Report-verification semantics）

## 2. 題面

- [x] 2.1 撰寫題面：素養情境（兩位監考老師兩端收卷疊一疊、驗 M 份回報）、動手推演（`3 1 4 2` 的合法收法逐步圖解＋一條卡死示範）、輸入輸出說明（含三項明文保證：同排座號互不相同、回報為由頂到底、座號 1..999）、範例＝設計定稿（兩組，答案 1 與 2）；用語一致性以 design.md 名詞表為準（來源行／收卷順序／回報／合法回報）。驗收：`grep -iE "deque|雙端佇列|stack|堆疊"` 在 generator/reference_solution 區塊外零命中。（覆蓋 Requirement: Exam-collection challenge content 的題面與禁字條款）

## 3. 測資

- [x] 3.1 宣告 params 乙′ 形狀（t: int 1..1、header: enum ["6 8"]、src: enum 10 排列、q1..q8: 各 enum 10 候選）並撰寫離線策展腳本：生成排列庫與候選庫，驗證（a）所有候選皆為來源值域排列（b）策展保證——每個來源在八條候選庫聯集中至少一條正反語意判定不同（c）合法行出現率每筆期望 0.5~1.5 條。驗收＝腳本三項檢查全過。（覆蓋 Requirement: Exam-collection testcase plan with twenty entries 的 band 條款）
- [x] 3.2 構造 20 筆 testcase_plan：範例 literal 置首＋考點 literal 9 筆（N=5..12、每筆至少一條反轉陷阱行，離線腳本驗證陷阱行存在且兩語意計數不同）＋乙′ band 4 筆＋壓力 literal 3 筆（T=1、N=800、M=18：全合法／長前綴近似／混合，`input_budget: 63488`）＋邊界 literal 3 筆（N=1、M=1、T=10 混排）。驗收＝腳本斷言 20 筆結構、各檔位型態與範圍宣告內含性，並逐列核對 design.md 型別×邊界矩陣（測資覆蓋）的每一格都有對應檔位。（覆蓋 Requirement: Exam-collection testcase plan with twenty entries 的檔位結構）
- [x] 3.3 TLE 探針全角落網格：重現 worker-utils.ts settrace 計數，實測「最省事件全枚舉」與「Python 層 N² 逐步線性搜尋」在三筆壓力筆的 op 數 ≥2×10M，正解在全 20 筆各筆 ≤1/100×10M；不達標即上調 N 並回寫題面範圍。（覆蓋 Requirement: testcase plan 的 stress scenario）

## 4. 建置與守門

- [x] 4.1 `pnpm build:pools` 成功後，解析池輸出驗證 10 blocks 至少兩塊內容相異（裸背答案不可全過）。（覆蓋 Scenario: Pool blocks differ under band randomization）
- [x] 4.2 全守門綠：`node_modules/.bin/vitest --run scripts/challenge-params.test.ts scripts/content-regression.test.ts`、`pnpm typecheck`、`pnpm lint`、`pnpm test --run`。（覆蓋 Requirement: Exam-collection dual implementation and verification 的 regression scenario）
