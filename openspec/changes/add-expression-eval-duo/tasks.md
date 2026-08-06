## 1. Scaffold 與組裝

- [x] 1.1 執行兩次 scaffold（snack-bar-register medium／coupon-combo-quote hard，皆 --category apcs --type competition），確認自動配號恰為 apcs011 與 apcs012（Implementation Contract 1）；配號不符即停並回報
- [x] 1.2 撰寫組裝腳本（scratchpad）落實 spec「Snack-bar register challenge (apcs011) I/O contract and semantics」與「Coupon-stacking challenge (apcs012) I/O contract and semantics」的 frontmatter 面：input_budget 63488、20 筆 literal testcase_plan（byte-for-byte 等於 design_b/literals/{a,b}_NN.txt，落實「Snack-bar register testcase plan and discrimination duties」與「Coupon-stacking testcase plan and discrimination duties」）、generator（D2 段折疊迭代式＋整除 assert，落實「Shared value domain and exact-division guarantee」）、reference_solution（shunting-yard→RPN 異構）、starter_code；驗收：腳本內建斷言（literal 位元組相等、generator=reference 全 40 筆輸出一致）全過

## 2. 題面撰寫

- [x] 2.1 撰寫 apcs011 題面，落實「Challenge-page language constraints」與「Score-ladder disposition and co-opted routes」（不提收編路線、不寫不可能性）：福利社老收銀機情境、值域/整除/除數為正/單數字行/答案可負逐條寫入、範例區塊=entry 1 原樣（含 1 - 7 / 2 = -3）；驗收：對照 trace C2/C3/C4/A1/A2 逐列勾稽、無資料結構術語
- [x] 2.2 撰寫 apcs012 題面，落實「Challenge-page language constraints」：折價券疊加情境、右結合以「每張券作用於其右側整段已計算結果」表述＋10 - 4 - 3 + 2 * 6 逐步拆解表（trace B14）、括弧覆寫 worked example、與 011 的 30/66 對照（trace B2）；驗收：同上逐列勾稽

## 3. 建置與本機驗證

- [x] 3.1 pnpm gen:keymaterial → build:wasm → build:pools 依序執行成功；node_modules/.bin/vitest --run scripts/challenge-params.test.ts 綠
- [x] 3.2 node_modules/.bin/vitest --run scripts/content-regression.test.ts 綠（兩題 reference_solution 對正式池 Accepted，落實「Verification and measurement discipline」前半）；pnpm typecheck 與 pnpm lint 綠

## 4. dev e2e 與量測閘（I-5）

- [x] 4.1 pnpm dev 起站，依 agent-browser SOP 對 V 表具路線檔之 11 條路線（V1-V5／V7-V12，15 次提交）逐路線提交、逐筆核對（期望值見 trace-matrix V 表；V6 無路線檔，維持 design-probe 並於 spec 明文豁免；驗證「Snack-bar register testcase plan and discrimination duties」「Coupon-stacking testcase plan and discrimination duties」「Score-ladder disposition and co-opted routes」的實測面）；任何偏差即停
- [x] 4.2 將 ship-e2e 實測回填 trace-matrix.md（V 表狀態欄）並撰寫 dev-verification-notes.md（每路線 per-entry 判定表），完成「Verification and measurement discipline」

## 5. 收尾

- [x] 5.1 檢查禁區：docs/public/pools/、key_material.rs、.env.pool 未入 staging；git status 乾淨列表核對
- [x] 5.2 自審 checklist（I-7 grep 舊值歸零：30/66、上界值、byte 數等關鍵數字三文件一致；I-8 無未消費 side_effect）後回報 audit loop 就緒
