## Why

目前 1-3 到 2-4 各節的練習題（類題 / 自己動手試試）存在兩種格式：**短描述類題**（1-2 句 + 提示）與**基本全描述題**（題目說明 + I/O 格式 + 範例表）。兩者都缺少 APCS 實作題的核心特質——**長篇素養情境敘述**，也缺少適合零基礎高中生的**思考鷹架**（數學公式對照、部分流程圖、逐步拆解引導）。

需要將這些練習題統一升級為「APCS 素養式」格式：保留 APCS 的結構化題目框架（問題情境 → 輸入格式 → 輸出格式 → 範例 → 範例說明），並在此基礎上加入教學鷹架元素，讓學生在面對較長的題目敘述時，仍有足夠的線索完成解題。這同時也是為未來 APCS 應試做閱讀長題的準備。

## What Changes

- **定義全新的「APCS 素養式」練習題格式模板**，包含以下元素：
  - **問題情境**：3-5 句以上的敘事情境，使用具名角色（如「小明」「小華」），嵌入真實生活場景
  - **🔍 思考引導**（鷹架區塊）：根據題目特性提供 1-3 種輔助引導，包括：
    - **數學表達**：將題目轉化為數學公式，讓學生看到「文字 → 數學 → 程式」的轉譯過程
    - **部分流程圖**：以 Mermaid 繪製含有遮蔽區塊（`???`）的流程圖，讓學生思考缺失步驟
    - **拆解思路**：以條列方式引導學生把大問題拆成小步驟
  - **輸入格式**：APCS 標準格式，逐行說明 + 值域限制
  - **輸出格式**：精確描述
  - **範例**（至少 2 組）：含輸入/輸出表格
  - **範例說明**：逐步追蹤範例計算過程（APCS 風格）
  - **老師的提示**：策略性提示，不含完整解法

- **改寫 1-3 到 2-4 各節的所有練習題**，從現有格式（短類題 / 基本全描述）升級為新的 APCS 素養式格式：
  - 1-3：10 題（Tier 1-4 的自己動手試試練習題，不含 Judge 解題實戰的 `leap-year`）
  - 1-4：1 題（`vending-change`）
  - 2-1：8 題（4 題短類題 + 4 題全描述，不含 Judge 解題實戰的 `number-sum`、`countdown`）
  - 2-2：6 題（2 題短類題 + 4 題全描述，不含 Judge 解題實戰的 `collatz-steps`）
  - 2-3：7 題（4 題短類題 + 3 題全描述，不含 Judge 解題實戰的 `first-divisor`、`skip-multiples`）
  - 2-4：6 題（全部全描述，不含 Judge 解題實戰的 `nested-triangle`、`multiplication-table`）
  - **合計：38 題**

- **保留既有的 ChallengeLink 連結與 challenge 檔案**：改的是 tutor 文章中的題目呈現方式，不動 `docs/challenge/` 的測資與解題機制

## Non-Goals

- **不新增題目**：此變更僅改寫現有題目的呈現格式，不增加新的練習題
- **不修改 challenge 檔案**：`docs/challenge/*.md` 的 frontmatter、generator、starter_code 不在範圍內
- **不修改 1-1、1-2 的類題**：這兩節的類題教學 `input()`/`print()`/算術，題目本身極短，不適合硬套長篇素養格式
- **不涉及 2-5**：2-5 為模組二總結，目前無練習題，不在此變更範圍
- **不修改教學正文**：各節的概念講解、程式碼範例、Trace Table 等教學內容不受影響，僅改寫「自己動手試試」/ 類題區塊
- **不改寫 Judge 解題實戰**：各節的「Judge 解題實戰」教學範例（含 IPO 分析、Step-by-Step 程式碼、Trace Table、常見錯誤分析）雖然內嵌 ChallengeLink，但其結構服務於教學示範，不屬於學生獨立練習題，不在改寫範圍。排除的 slug：`leap-year`（1-3）、`number-sum`、`countdown`（2-1）、`collatz-steps`（2-2）、`first-divisor`、`skip-multiples`（2-3）、`nested-triangle`、`multiplication-table`（2-4）
- **不增加流程圖 Mermaid 支援**：專案已有 `vitepress-mermaid-support` spec，此處直接使用
- **若現有練習題只有 1 組範例，需新增第 2 組**：此屬格式補齊，不算「新增題目」

## Capabilities

### New Capabilities

- `apcs-literacy-exercise-template`: 定義 APCS 素養式練習題的完整格式規範，包含問題情境敘事結構、鷹架元素類型（數學表達 / 部分流程圖 / 拆解思路）的使用時機與格式、I/O 規格寫法、範例說明撰寫規範、以及各鷹架元素的品質標準

### Modified Capabilities

- `python-ch2-enhanced-exercises`: 將現有的「APCS 初級銜接格式」需求升級為「APCS 素養式格式」，所有練習題需符合新的 `apcs-literacy-exercise-template` 規範

## Impact

- 受影響的 specs：
  - 新建 `apcs-literacy-exercise-template` spec
  - 修改 `python-ch2-enhanced-exercises` spec（格式需求升級）
- 受影響的程式碼 / 內容檔案：
  - `docs/tutor/py/ch1/1-3.md` — 改寫 10 題練習題格式
  - `docs/tutor/py/ch1/1-4.md` — 改寫 1 題練習題格式
  - `docs/tutor/py/ch2/2-1.md` — 改寫 8 題練習題格式
  - `docs/tutor/py/ch2/2-2.md` — 改寫 6 題練習題格式
  - `docs/tutor/py/ch2/2-3.md` — 改寫 7 題練習題格式
  - `docs/tutor/py/ch2/2-4.md` — 改寫 6 題練習題格式
- 不影響任何 JavaScript/TypeScript/Vue 程式碼
- 不影響 `docs/challenge/` 下的 challenge 檔案
- 依賴 `vitepress-mermaid-support` spec 提供的 Mermaid 渲染能力（已存在）
