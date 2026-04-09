## Why

`1-1.md` 是 Chapter 1 的第一節，也是零基礎學生接觸的第一份教材。Phoenix 手動編輯後發現 6 個需要補充內容的 TBD 標記，以及在標點符號、術語前向引用、敘事鋪陳等方面的系統性品質問題。作為全章的開篇，1-1 的品質標準會影響學生對後續章節的信任與學習動力。此變更同時建立 8 條編輯規則（P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1），作為 1-2、1-3、1-4 修改的基準。

完整分析見 `openspec/ch1-editorial-review.md`。

## What Changes

### 填補 6 個 TBD

1. **TBD-A**（L134, L161, L181）：為 `print()` 三個子步驟（印文字、印計算結果、印多個東西）的 code block 前補上 1~2 句對話式過場，建立「為什麼要學這個」的認知鋪陳
2. **TBD-B**（L155-156）：在引號說明後補上 `[!WARNING]` 區塊，用英文文法的「引號成對」規則類比 Python 的 `"` / `'` 不能混用
3. **TBD-C**（L174）：在 `print(1+1)` 後補上「由內而外求值（Inside-out Evaluation）」的心智模型說明，含 step-by-step trace，為 1-2 的 `int(input())` 打下基礎
4. **TBD-D**（L202-206）：重新設計 `print()` → `input()` 的段落過場，從一句話擴展為 2~4 句的概念銜接（摘要已學 → 指出缺口 → 引出下一段）

### 套用已確立的編輯修改（Phoenix 已完成，需保留）

Phoenix 已在 working copy 中完成的修改：
- **P-1**：4 處破折號 `——` 改為逗號/冒號
- **T-1**：2 處「變數名稱」改為「指令或資料儲存空間的名稱」
- **S-1**：計算機比喻前加 meta-cognitive bridge
- **S-2**：阿飄笑話後加「沒錯！」callback connector

### 全檔審計

以 8 條規則對全檔做一次完整掃描，確認 Phoenix 手動修改以外的段落是否也有違反的情況。

## Non-Goals

- 不改動文章結構或 H2 段落順序
- 不新增或修改圖片佔位符（Image Specification Appendix 不動）
- 不修改 frontmatter
- 不修改 `docs/challenge/*.md` 挑戰題內容

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `python-ch1-content`：新增 8 條內容品質要求（P-1 標點風格, T-1 術語前向引用, S-1/S-2/S-3 敘事鋪陳, C-1 code block lead-in, E-1 錯誤預防, M-1 心智模型顯性化），補充現有的結構性 requirements

## Impact

- 受影響的 spec：`python-ch1-content`
- 受影響的檔案：`docs/tutor/py/ch1/1-1.md`
