## Why

站台從一開始就開了 MathJax（`.vitepress/config.mts` 的 `markdown.math: true` 加上 `markdown-it-mathjax3`），教學文章大量在用，但**題目頁幾乎沒跟上**：71 道題裡只有 3 題用 LaTeX 寫數學陳述，其餘 55 題仍用 Unicode 記號與 ASCII 拼寫混寫，例如 `1 ≤ n ≤ 1500`、`n <= 100`、`2^(D−1)`、`k × k`。

這造成三個具體問題：

1. **讀者要自己解析 ASCII 指數**。`2^(D−1)` 對高中生不是一眼可讀的式子，`$2^{D-1}$` 才是。
2. **同一個約束在不同題目有四種寫法**（`≤`／`<=`／`小於等於`／`不超過`），學生跨題閱讀時得重新適應。
3. **沒有任何機制擋住繼續漂移**。`Usage.md` 的「Markdown 內文結構」完全沒提數學記號怎麼寫，新題目只會複製最近一題的寫法，混寫會持續擴散。

apcs013／apcs014 的試點已經證明轉換規則可行且渲染正確，現在把它推到全站並補上守門。

## What Changes

- **55 道題目頁的內文數學陳述改用 LaTeX**（frontmatter 完全不動），另有 8 頁原本沒有黑名單記號、但內文有裸的單字母變數（`hello-world` 的 `S`、`leap-year` 的 `Y`、`odd-even` 的 `n` 等），依分類表一併包成 LaTeX。已完成的 3 題不重做，內文完全沒有數學元素的 5 題不需處理。
- **`movie-ticket.md` 的 5 個裸貨幣 `$` 一併 escape 成 `\$`**。該頁票價寫成 `$150`／`$250`，目前僥倖沒被 MathJax 配對成公式（每個 `$` 前面都是空白，不是合法的結束定界符），但該頁本身要新增 `$\ge 65$`，同頁混用數學 `$` 與貨幣 `$` 是已知的定界符地雷。
- **新增 CI 守門測試**，把「題目頁內文不得出現裸數學記號」變成會讓 `pnpm test` 失敗的硬條件，防止新題目漂移回去。
- **`Usage.md` 的「Markdown 內文結構」新增數學記號小節**，把規則寫給出題者看，而不是只寫在 spec 裡。
- **補上行內公式渲染的 spec 覆蓋**。修正本身已在本分支的 commit `29e381c` 落地（Tailwind preflight 的 svg 區塊化規則讓每個行內 `$…$` 各佔一行），但當時沒有對應的 spec 與回歸測試；本 change 補齊，因為全站的轉換完全依賴這個修正。

### 實作期間的範圍修正（記實際值，不回頭美化）

初稿寫「53 題待轉、15 題無記號」，那是黑名單還有缺口時算出來的。缺口有三個：裸的 `<` 與 `>`、`!=`、`÷`。後果不只是漏抓幾個記號——`quadrant-classifier` 整頁 7 條不等式全用裸的 `<` `>` 寫，因此被盤點歸類成「內文無數學記號」，**整頁沒有任何人看過**。

黑名單補齊後（裸比較用「運算元 運算子 運算元」的 pattern，而不是把 `<` `>` 直接列成 token，否則會誤殺 HTML 標籤、引言行首與 `-->`），用同一份規則重測基準線：待轉 53 → **55**、無記號 15 → **13**。轉換完成後無記號再降到 **5**，因為那 8 頁的裸單字母變數依分類表也該包成 LaTeX。

`measure/notation-before.json` 與 `measure/lint-red.txt` 都已用擴充後的規則重新產生，不留兩種規則版本混用的數字。

## Non-Goals

- **不改 frontmatter 任何欄位**。`params`／`generator`／`testcase_plan` 進 pool hash，動了要重建測資池與 WASM；本 change 只碰 frontmatter 之後的內文。
- **不改教學文章**（`docs/tutor/` 底下）。那些頁面已經在用 LaTeX，且用的是 VitePress 的 `vp-doc` 樣式，與題目頁的 `prose` 樣式不同，混在一起會讓驗證面失焦。
- **不修 Tailwind Typography 的 `code::before/after` 反引號問題**。題目頁的行內 `<code>` 目前會多顯示一對反引號，使用者 2026-08-16 明確表示暫時不修。這是本 change 最容易被「順手修好」的東西，明列為排除項。
- **不改範例輸入／輸出區塊**。那些是字面資料，`5` 就是 `5`，不是數學陳述。
- **不追求把所有數字 LaTeX 化**。純散文裡的數字維持原樣，「模式 1」不寫成「模式 $1$」。

## Capabilities

### New Capabilities

- `challenge-math-notation`: 題目頁內文的數學記號撰寫約定——什麼寫成 LaTeX、什麼維持反引號、什麼維持純文字，以及據此建立的機械守門。

### Modified Capabilities

- `vitepress-math-support`: 新增一條要求，規定行內公式必須與同段落的前後文排在同一行；既有的三條要求（`$…$` 渲染、`markdown.math: true`、`markdown-it-mathjax3` 相依）不變。

## Impact

- Affected specs: `challenge-math-notation`（新增）、`vitepress-math-support`（修改）
- Affected code:
  - Modified: 63 個 `docs/challenge/` 底下的題目頁（55 頁待轉 + 8 頁裸變數；完整清單在 tasks.md），以及 `Usage.md`
  - New: `scripts/latex-notation.test.ts`（CI 守門）、`scripts/latex-notation-survey.py`（盤點與證物產生器）、`scripts/latex-notation-rules.json`（兩端共用的黑名單）
  - Removed: 無
- 不影響建置管線：pool hash 只吃 frontmatter 的 `params` 與 `testcase_plan`，內文改動不需要重跑 `gen:keymaterial` / `build:wasm` / `build:pools`。
- 分支必須疊在 `fix/challenge-wording` 之上，不能從 `staging` 開——`29e381c` 的 CSS 修正還沒進 `staging`，少了它全部轉換過的頁面會斷行。
