## 1. 重寫開場白 — Chapter 1 section 1-1 opening addresses learner motivation rule O-1

- [x] 1.1 [P] [Chapter 1 section 1-1 opening addresses learner motivation rule O-1] 將 `docs/tutor/py/ch1/1-1.md` L15-26（`<!-- [START] TBD 整段改掉 -->` 到 `<!-- [END] TBD -->`）替換為「為什麼要學程式」段落。結構：(a) Phoenix 親身故事——「我當年學程式的動機不太正當：是為了零用錢」，父親承諾學好給零用錢 (b) 轉折——「但學會之後，真的開啟新世界」 (c) 拉回學生——「你不需要為了零用錢，但你會發現程式能幫你做到很多以前想都沒想過的事」 (d) 銜接本章——「這一章，我們就從最簡單的開始」。整段保持 Phoenix 的對話語氣，比原段落更長（至少 4 段落）。移除 `[START]/[END] TBD` 註解

## 2. 改用逗號分隔取代字串串接 — Chapter 1 section 1-1 code examples match walkthrough text rule W-1

- [x] 2.1 [P] [Chapter 1 section 1-1 code examples match walkthrough text rule W-1] 簡化 hello-world challenge 輸出格式：將 `docs/challenge/hello-world.md` 的期望輸出從 `Hello, Alice!` 改為 `Hello, Alice`（移除 `!`），generator 改為 `print("Hello,", name)`，starter_code 與輸出說明同步更新
- [x] 2.2 將 `docs/tutor/py/ch1/1-1.md` 的解題實戰程式碼從 `print("Hello, " + name + "!")` 改為 `print("Hello,", name)`，完全使用逗號分隔，不引入 `+` 字串串接。同步更新：題目說明（Output 格式）、範例表、IPO 分析的 O 項
- [x] 2.3 重寫逐行解讀，從三行（`input()`、字串串接、`print()`）改為兩行（`input()`、`print("Hello,", name)` 逗號分隔自動補空格）
- [x] 2.4 重寫常見錯誤排查段落：移除「忘記驚嘆號」和「忘記逗號後的空格」（不再適用），改為「`"Hello,"` 裡面忘記逗號」（`print("Hello", name)` → `Hello Alice` → WA）
- [x] 2.5 更新類題一（自我介紹產生器）的提示：從「用字串串接（`+`）把它們組合起來」改為「在 `print()` 裡面用逗號把它們跟固定文字隔開就好」

## 3. 清除殘留 TBD 標記 — Chapter 1 sections contain no residual TBD markers rule T-2

- [x] 3.1 [Chapter 1 sections contain no residual TBD markers rule T-2] 移除 `docs/tutor/py/ch1/1-1.md` L287 的 `<!-- TBD 關於用 str binary adding ... -->` 註解
- [x] 3.2 全檔掃描 `docs/tutor/py/ch1/` 目錄，確認所有 `<!-- TBD`、`<!-- [START] TBD`、`<!-- [END] TBD -->` 註解已移除，無殘留

## 4. 重新生成 test pool

- [x] 4.1 執行 `pnpm build:pools` 重新生成所有 challenge 的 test pool（hello-world 輸出格式改變，pool 需重新生成）
