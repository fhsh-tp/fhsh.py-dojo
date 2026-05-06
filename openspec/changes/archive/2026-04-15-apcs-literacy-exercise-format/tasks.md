## 0. 前置準備（實作前必讀）

實作各節練習題改寫前，必須先讀取以下檔案以取得完整格式規範：
1. `specs/apcs-literacy-exercise-template/spec.md` — 9 個必要區塊的完整結構與順序
2. `design.md` 決策一（格式模板）、決策二（鷹架類型格式）— 各 scaffold 的 Markdown 語法
3. `design.md` 決策四（敘事風格）— 角色命名與情境類型

**改寫邊界規則**：
- 保留 `## 自己動手試試！` 標題及其介紹段落
- 刪除 Tier 分級標題（★☆☆ 等）和分級說明段落（僅限 1-3）
- 將每道練習題原地改寫為新格式（從 `###` 或 `####` 標題到下一個同級或更高標題為止）
- 不修改 `## 自己動手試試！` 之前的教學正文，也不修改 `## 本節小結` 之後的內容
- Judge 解題實戰區塊（含 IPO 分析、Step-by-Step、Trace Table）不改寫
- 已有 題目說明 + 輸入格式 + 輸出格式 + 範例 的全描述題，保留現有 I/O 資料，在其基礎上擴充問題情境、加入思考引導、加入範例說明

## 1. 格式模板確立與驗證

- [x] 1.1 撰寫一道完整的 APCS 素養式練習題範例（以 1-3 的 BMI 題為原型），驗證 APCS literacy exercise format template structure 的所有 9 個必要區塊是否可在 VitePress 中正常渲染（含 Mermaid 流程圖、LaTeX 公式、callout），對應決策一：APCS 素養式格式模板結構
- [x] 1.2 確認三種鷹架元素（數學表達 / 部分流程圖 / 拆解思路）的 Markdown 語法在 VitePress 中正確呈現——特別驗證 Mermaid code block 在 blockquote（`> ` 前綴）內是否正常渲染。對應 scaffold section provides at least one scaffold type 的三種類型格式，驗證決策二：鷹架元素類型與選用準則中定義的格式。若 Mermaid-in-blockquote 渲染失敗，需先解決後才能進行 Type B 鷹架寫作。

## 2. 改寫 1-3 練習題（if-elif-else 主題）

**檔案**：`docs/tutor/py/ch1/1-3.md`（`## 自己動手試試！` 區塊，約 line 438 起）
**主要鷹架**：Type B 流程圖（≥ 60%）｜次要：Type A 數學（公式題）、Type C 拆解（複合題）
**角色表**：小安、阿翔、小芳、阿宏、小恩、阿玲、小凱、阿瑜、小蓁、阿傑（每題依序使用，不重複）

- [x] 2.1 改寫 Tier 1 暖身題（`odd-even`、`sign-check`）為 APCS 素養式格式：問題情境使用 named character（problem narrative uses APCS literacy style），主要使用 Type B 流程圖鷹架（scaffold type selection follows section-topic mapping），確保 tier-based difficulty labels are removed。`odd-even` 情境種子：小安和同學玩撲克牌紅黑分堆遊戲。`sign-check` 情境種子：阿翔在科學實驗中記錄溫度變化的正負。
- [x] 2.2 改寫 Tier 2 基礎應用題（`grade-level`、`bmi-classifier`、`quadrant-classifier`）為 APCS 素養式格式：`bmi-classifier` 使用 Type A 數學表達鷹架（$$BMI = W / H^2$$），`grade-level` 和 `quadrant-classifier` 使用 Type B 流程圖鷹架，每題問題情境 150-300 字。`grade-level` 情境種子：小芳幫班導師寫成績單自動化工具。`bmi-classifier` 情境種子：阿宏體育課的體適能健檢。`quadrant-classifier` 情境種子：小恩在數學課學直角座標系。
- [x] 2.3 改寫 Tier 3 數學建模題（`triangle-classify`、`quadratic-discriminant`、`taxi-fare`、`movie-ticket`）為 APCS 素養式格式：公式題使用 Type A 數學表達 + Type B 流程圖複合鷹架，每題加入 example explanation traces computation step by step。`triangle-classify` 情境種子：阿玲做美術作業需要判斷三角形類型。`quadratic-discriminant` 情境種子：小凱做數學作業檢查二次方程式。`taxi-fare` 情境種子：阿瑜和朋友出遊搭計程車分攤車資。`movie-ticket` 情境種子：小蓁幫全家人買電影票。
- [x] 2.4 改寫 Tier 4 綜合挑戰題（`date-validator`）為 APCS 素養式格式：使用 Type C 拆解思路 + Type B 流程圖複合鷹架，確認 input format uses APCS-standard specification（含值域限制）。情境種子：阿傑開發行事曆 App 需要驗證使用者輸入的日期。

## 3. 改寫 1-4 練習題（模組一總結）

**檔案**：`docs/tutor/py/ch1/1-4.md`（`## 模組一畢業考` 區塊）
**主要鷹架**：Type C 拆解 ｜次要：Type A 數學
**角色表**：小威

- [x] 3.1 改寫 `vending-change` 練習題為 APCS 素養式格式：使用 Type C 拆解思路 + Type A 數學表達鷹架（決策四：問題情境敘事風格），teacher hint provides strategy without solution。情境種子：小威在學校福利社打工操作找零機。

## 4. 改寫 2-1 練習題（for 迴圈主題）

**檔案**：`docs/tutor/py/ch2/2-1.md`（兩個 `## 自己動手試試！` 區塊 + 後續全描述題）
**主要鷹架**：Type A 數學（≥ 50%）｜次要：Type B 流程圖
**角色表**：小琳、阿豪、小穎、阿軒、小蕾、阿志、小潔、阿廷
**注意**：此檔有 2 個「自己動手試試」區塊（分別在 `number-sum` 和 `countdown` Judge 解題之後），不要修改 Judge 解題實戰區塊本身

- [x] 4.1 改寫短格式練習題（`repeat-greeting`、`factorial`、`odd-numbers`、`range-sum`）為 APCS 素養式格式：主要使用 Type A 數學表達鷹架（決策三：各節鷹架選用對照表），每題問題情境 150-300 字。`repeat-greeting` 情境種子：小琳寫迎新活動的自動歡迎訊息。`factorial` 情境種子：阿豪計算社團分組的排列數。`odd-numbers` 情境種子：小穎在數學課做等差數列練習。`range-sum` 情境種子：阿軒計算零用錢累積儲蓄。
- [x] 4.2 改寫全描述題（`arithmetic-sum`、`number-staircase`、`star-square`、`even-countdown`）為 APCS 素養式格式：遵循 existing full-description exercises are augmented not rewritten from scratch 需求，保留現有 I/O 資料，升級問題情境敘事、加入思考引導鷹架區塊、加入範例說明逐步追蹤（決策五：範例說明撰寫規範）。`arithmetic-sum` 使用 Type A 數學。`number-staircase`/`star-square` 使用 Type C 拆解。`even-countdown` 使用 Type A 數學 + Type B 流程圖。

## 5. 改寫 2-2 練習題（while 迴圈主題）

**檔案**：`docs/tutor/py/ch2/2-2.md`（`## 自己動手試試！` 區塊 + 後續全描述題）
**主要鷹架**：Type B 流程圖（≥ 50%）｜次要：Type A 數學、Type C 拆解
**角色表**：小茵、阿博、小婷、阿達、小雯、阿誠
**注意**：不修改 `collatz-steps` Judge 解題實戰區塊。`guess-number-simple` 的 slug 名稱具誤導性——實際題目是「加總達標步數」（累加到目標），非猜數字遊戲，寫情境時以實際題意為準。

- [x] 5.1 改寫短類題（`digit-counter`、`number-reverse`）為 APCS 素養式格式：主要使用 Type B 流程圖鷹架，確認 existing short-format exercises are upgraded（APCS beginner transition format template 修改需求）。`digit-counter` 情境種子：小茵好奇手機號碼有幾位數。`number-reverse` 情境種子：阿博玩數字鏡像遊戲。
- [x] 5.2 改寫全描述題（`guess-number-simple`、`gcd-euclid`、`digital-root`、`perfect-number`）為 APCS 素養式格式：`gcd-euclid` 使用 Type A 數學（$$\gcd(a,b) = \gcd(b, a \mod b)$$）+ Type B 流程圖複合鷹架，範例說明以決策五：範例說明撰寫規範格式逐步追蹤輾轉相除過程。`guess-number-simple` 情境以累加達標為主題（小婷存錢達標）。`digital-root` 使用 Type B 流程圖。`perfect-number` 使用 Type A 數學 + Type B 流程圖。

## 6. 改寫 2-3 練習題（break/continue 主題）

**檔案**：`docs/tutor/py/ch2/2-3.md`（兩個類題區塊 + 後續全描述題）
**主要鷹架**：Type B 流程圖（≥ 60%）｜次要：Type C 拆解
**角色表**：小柔、阿杰、小萱、阿磊、小韻、阿銘、小瑤
**注意**：不修改 `first-divisor` 和 `skip-multiples` Judge 解題實戰區塊

- [x] 6.1 改寫短類題（`password-check`、`target-sum`、`sum-skip-fives`、`digit-sum-skip`）為 APCS 素養式格式：主要使用 Type B 流程圖鷹架展示 break/continue 的流程控制。`password-check` 情境種子：小柔設計社團網站的登入系統。`target-sum` 情境種子：阿杰在便利商店湊滿額集點。`sum-skip-fives` 情境種子：小萱在數學課做特殊加總練習。`digit-sum-skip` 情境種子：阿磊研究數字的各位數加總規律。
- [x] 6.2 改寫全描述題（`prime-check`、`perfect-numbers-range`、`smallest-prime-factor`）為 APCS 素養式格式：`prime-check` 使用 Type A 數學 + Type B 流程圖複合鷹架，`perfect-numbers-range` 使用 Type C 拆解 + Type B 流程圖，`smallest-prime-factor` 使用 Type B 流程圖。

## 7. 改寫 2-4 練習題（巢狀迴圈主題）

**檔案**：`docs/tutor/py/ch2/2-4.md`（`## 自己動手試試！` 區塊）
**主要鷹架**：Type C 拆解（≥ 60%）｜次要：Type B 流程圖
**角色表**：小晴、阿峰、小涵、阿偉、小嵐、阿彥
**注意**：不修改 `nested-triangle` 和 `multiplication-table` Judge 解題實戰區塊

- [x] 7.1 改寫圖形題（`star-rectangle`、`inverted-triangle`、`isosceles-triangle`）為 APCS 素養式格式：主要使用 Type C 拆解思路鷹架將圖形拆解為外圈/內圈子問題（section 1-3 tier format is replaced 的精神延伸到所有節）。每題的拆解步驟需明確區分「外層迴圈控制列數」和「內層迴圈控制每列內容」。
- [x] 7.2 改寫進階題（`number-pyramid`、`star-diamond`、`pair-count`）為 APCS 素養式格式：使用 Type C 拆解 + Type B 流程圖複合鷹架，`pair-count` 加入 Type A 數學表達（組合數公式）。

## 8. 整體品質檢查

- [x] 8.1 驗證所有改寫後的練習題符合 APCS literacy exercise format template structure（9 個必要區塊完整、順序正確）
- [x] 8.2 驗證各節的鷹架選用比例符合 scaffold type selection follows section-topic mapping 的百分比要求（1-3 ≥ 60% Type B、2-1 ≥ 50% Type A、2-4 ≥ 60% Type C）
- [x] 8.3 驗證所有問題情境的具名角色在同一 `.md` 檔內不重複（problem narrative uses APCS literacy style），且字數在 150-300 字範圍
- [x] 8.4 驗證所有範例說明遵循決策五：範例說明撰寫規範（編號步驟、具體數字、明確結論）
- [x] 8.5 確認 APCS beginner transition format template 修改需求的所有 scenario 通過：短類題已升級、Tier 格式已移除、所有題目符合新格式
