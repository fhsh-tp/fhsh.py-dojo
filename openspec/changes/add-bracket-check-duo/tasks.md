## 1. Scaffold

- [x] 1.1 執行 `pnpm new-challenge prop-box-packing --title "道具箱裝箱檢查" --difficulty medium --category apcs --type competition`，確認 scaffold 配號成功（預期 apcs009，以實配為準；矩陣 C1/C2），檔案 docs/challenge/prop-box-packing.md 存在（spec「Shared authoring constraints for the bracket duo」：id 由 scaffold 配號）
- [x] 1.2 執行 `pnpm new-challenge magazine-typeset-check --title "校刊排版檢查器" --difficulty medium --category apcs --type competition`，確認配號（預期 apcs010）與檔案 docs/challenge/magazine-typeset-check.md 存在（同上 requirement）

## 2. 測資策展（離線腳本 → literal）

- [x] 2.1 依 design「D1. 相關性輸入以「literal 策展＋enum soup band」解決（C8）」在 scratchpad 撰寫策展腳本：產生 1a 的 literal 條目（題面範例、交錯陷阱 7 筆（短第 4/9/12/15/18 筆＋長第 17/19 筆）、各分區 OK 保底、第 20 筆 62KB 深度 31000 混種深巢；矩陣 C6/A3/A6/A8）與 1b 的 literal 條目（題面範例、無括號邊界筆、六筆互異獵殺形（矩陣 B4 參數表，lean 下限 m×2k≥20M）；矩陣 C6/B4/B7），並驗算每條 literal 位元組數 < 63488（C4）
- [x] 2.2 依 spec「Prop-box packing testcase plan」與 design「D2. params 骨架（兩題同構）」完成 1a frontmatter：params 骨架＋ 20 條 testcase_plan（band values/count override 依分區 C5/A7、literal 貼入），`input_budget: 63488`；並依 spec「Prop-box packing performance envelope and bypass disposition」與 design「D3. 1a 繞道處置：收編（A4，rank-code-duo D6.b 判例）」確認題面與測資不含不可能性承諾、第 20 筆 stress 不誤殺正解
- [x] 2.3 依 spec「Magazine typeset testcase plan」與 design「D4. 1b 斷崖：op counter 逐筆爆殺（B4）」完成 1b frontmatter：同構 params（enum values 含雜訊字元集 B3）＋ 20 條 testcase_plan（獵殺筆位置 14/15/16/18/19/20），`input_budget: 63488`

## 3. generator / reference / starter / 題面

- [x] 3.1 依 spec「Prop-box packing check challenge (1a) I/O contract」與 design「D5. generator 與 reference_solution 分工（C9）」撰寫 1a generator（stack 存字元＋dict 配對表）與 reference_solution（stack 存索引，佈局獨立），輸出恰 `OK`/`NG`（A2）；starter_code 讀入骨架
- [x] 3.2 依 spec「Magazine typeset check challenge (1b) I/O contract」與 design「D5. generator 與 reference_solution 分工（C9）」撰寫 1b generator（stack 存 (字元,位置) tuple）與 reference_solution（雙平行 list），輸出三分支位置語義（B1/B2）；starter_code 讀入骨架
- [x] 3.3 依 design「D6. 題面（素養層，A2/B1 派生）」撰寫兩題題面（範例＝testcase_plan 第 1 筆 literal 逐字一致 C6；無資料結構術語、無不可能性承諾 A4/B6），1b 輸出說明含三分支全文與殘留分支範例；完成後對照 spec「Shared authoring constraints for the bracket duo」逐項自查（情境、無術語、reference_solution 獨立寫法）

## 4. 驗證閉環

- [x] 4.1 `pnpm build:pools` 零錯誤（含 budget 檢查 C4）；`node_modules/.bin/vitest --run scripts/challenge-params.test.ts` 通過
- [x] 4.2 `node_modules/.bin/vitest --run scripts/content-regression.test.ts` 兩題通過（C9；spec「Shared authoring constraints for the bracket duo」Scenario: Content regression passes for both challenges）
- [x] 4.3 dev server e2e：依預測矩陣 V1–V8 逐路線提交，驗證 spec「Prop-box packing performance envelope and bypass disposition」（1a ref 20/20、1a replace 20/20 收編）、spec「Prop-box packing testcase plan」Scenario（1a 計數器 13/20，WA 恰第 4/9/12/15/17/18/19 筆）、spec「Magazine typeset performance envelope」（1b ref 20/20）、spec「Magazine typeset testcase plan」Scenario（1b 回頭掃描 14/20，恰第 14/15/16/18/19/20 筆爆殺），逐筆 verdict 與預測零偏差；結果記入 change 目錄 dev-verification-notes.md
