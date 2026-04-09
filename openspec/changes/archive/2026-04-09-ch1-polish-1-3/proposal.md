## Why

`1-3.md`（布林值與流程控制）是模組一最複雜的章節，包含比較運算子、邏輯運算子、`if-elif-else`、巢狀 if、流程圖、閏年判斷等大量概念。以全部 15 條編輯規則（含 `ch1-editorial-rules-enhancement` 新增的 F-1、V-1、T-3、K-1 以及修訂的 P-1、S-2）審計後，發現相同模式的品質問題：破折號密度高、部分 code block 直接從標題跳入、複雜布林表達式的求值過程缺乏 step-by-step trace。此外發現 4 張圖片佔位符缺少 `![](path)` 行（F-1 違規）、Judge 解題段落 ~90 行無顏文字（K-1 違規）、以及 L225 的 kaomoji 跨 H2 邊界無回歸連接詞（S-2 違規）。

此變更獨立於 1-1、1-2 的修改，參照同一套編輯規則。

完整編輯規則定義見 `openspec/specs/python-ch1-content/spec.md` 以及 `phoenix-popular-science-article-style-enhance.md`。

## What Changes

### P-1 標點風格統一

逐行審計 `——` 的使用。1-3 的戲劇性描寫（天氣場景 hook、閏年的「順序很重要」）可保留合理的破折號；例行子句銜接改為逗號或冒號。

### C-1 Code block 對話式 lead-in

檢查以下 code block 是否有過場：
- 比較運算子示範 `print(3 > 2)` 等
- 邏輯運算子 `and` / `or` 示範
- 高中生活舉例（社團報名、段考免補考）
- `if` 基本判斷
- 縮排說明的 code block
- `if-else` 二選一
- `if-elif-else` 多選一（成績等第）
- 巢狀 if（超商打折）
- 閏年布林表達式
- 閏年多層 if-elif-else 寫法
- 順序錯誤的反例 code block

### M-1 求值模型顯性化

重點對象：`(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)` — 這是本章最複雜的表達式。需確認是否有 step-by-step trace 帶讀者走過「先算 `%`，再算 `==`/`!=`，再算 `and`，再算 `or`」的求值順序。應 callback 到 1-1 的 `print(1+1)` 基礎與 1-2 的 `int(input())` 模式。

### S-1 類比 meta-cognitive bridge

檢查以下比喻是否有「為什麼要用這個比喻」的鋪陳：
- 起床看天氣（hook，可能已足夠）
- 超商打折（巢狀 if 的比喻）
- 岔路口（流程控制的比喻）

### S-3 段落過場密度

檢查以下段落邊界：
- 「布林值」→「if-elif-else」（L127 `好，你學會問是非題了。接下來要學的是——根據答案做不同的事。`）
- 「if-elif-else」→「流程圖」（L231 `畫流程圖可能聽起來很無聊，但它是你解決複雜判斷的秘密武器。`）
- 「流程圖」→「Judge 解題實戰」（L295-296，目前只有 `---` 分隔）

### S-2 笑話後語氣銜接

掃描所有 kaomoji / 括號笑話後的下一句，確認有 callback connector。特別注意 L166 `ʅ（´◔౪◔）ʃ` 後的銜接。

### T-1 術語前向引用審計

1-3 建立在 1-1（I/O）和 1-2（變數、型別、運算）之上。需確認所有向後引用都是合法的，且 1-3 沒有使用 1-4 或模組二的概念（如迴圈、串列）。

### E-1 錯誤預防

檢查 `==` vs `=` 的混淆警告是否在 `if` 語法首次出現時就強調，而非延後。（L77-84 已有說明，確認位置和語氣。）另外檢查邏輯運算子引入處是否缺少 `score >= 60 and <= 80` 常見錯誤的警告。

### F-1 圖片佔位符雙行格式

4 張圖片（圖 9 L25、圖 10 L123、圖 11 L227、圖 12 L293）目前只有 `> 📷` caption 行，缺少前導的 `![](path)` image link 行。須補齊為 F-1 雙行格式。

### K-1 顏文字語氣密度

Judge 解題段落（L297-388，約 90 行散文）無任何顏文字或情感標點元素，遠超 30 行上限。需在此段落中至少插入 3 個情感標點元素。

### S-2（H2 邊界補充）

L225 的 kaomoji `╮(╯_╰)╭` 後接 H2 邊界（非 H3），S-2 的 H3 豁免不適用。需在 L231 的 H2 過場開頭加入回歸連接詞。

## Non-Goals

- 不改動文章結構或 H2 段落順序
- 不改動閏年流程圖的 ASCII art
- 不修改 frontmatter
- 不修改 `docs/challenge/*.md`

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

（無 — 編輯規則 spec 已在第一個 change 中建立）

## Impact

- 受影響的檔案：`docs/tutor/py/ch1/1-3.md`
