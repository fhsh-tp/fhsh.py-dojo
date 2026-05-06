## Why

第二章第 2 節需要教授 `while` 條件迴圈——這是學生在學會 `for` 固定次數迴圈（2-1）之後，面對「不知道要跑幾次」的情境時不可或缺的工具。Collatz 猜想（3N+1）作為 Judge 主例題，能讓學生直觀體驗條件式終止的威力。

## What Changes

- 新增教學文件 `docs/tutor/py/ch2/2-2.md`，涵蓋 while 迴圈概念、語法、追蹤表、常見錯誤與 Judge 演練
- 新增 3 道 Judge 關卡（ID 17–19），主例題為 Collatz 3N+1，另附 2 道練習題
- 建立新能力規格 `python-ch2-2-2-content`，記錄本節所有可驗證需求

## Non-Goals

- 不涵蓋 `break` / `continue`（屬 2-3 節範疇）
- 不涵蓋 `list`、`dict`、`tuple`（尚未教授）
- 不修改已在 2-1 變更中更新的 `tutor-article-structure` 規格
- 不新增新的 editorial rule（沿用 Ch1 的 P-1 至 K-1 全套規則）

## Capabilities

### New Capabilities

- `python-ch2-2-2-content`: 定義 2-2 節 while 條件迴圈的教學文件規格與 3 道 Judge 關卡（IDs 17–19）需求

### Modified Capabilities

(none)

## Impact

- Affected specs: `python-ch2-2-2-content`（新建）
- Affected code:
  - `docs/tutor/py/ch2/2-2.md`（新建教學文件）
  - `challenges/017/challenge.yaml`（新建，Collatz 3N+1 主例題）
  - `challenges/018/challenge.yaml`（新建，練習題 1）
  - `challenges/019/challenge.yaml`（新建，練習題 2）
