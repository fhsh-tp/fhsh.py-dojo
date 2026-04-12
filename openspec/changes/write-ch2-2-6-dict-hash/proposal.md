## Why

第 2-6 節教授 Python 字典（Dict）的 Key-Value 結構與雜湊查找原理，讓學生理解為什麼字典的查找速度遠優於串列的線性搜尋。這是 Chapter 2（Module 2）的第六節，在學生已學會 for/while 迴圈、串列操作後，進一步介紹高效的資料結構。

## What Changes

- 新增教學文章 `docs/tutor/py/ch2/2-6.md`，涵蓋兩個知識點：
  - 字典的 Key-Value 結構（建立、存取、新增、修改）
  - 雜湊查找 vs 線性搜尋的速度差異
  - Tuple 作為介紹性知識（旁白，不單獨出題）
- 新增 6 道挑戰題（ID 41–46），分成兩組：
  - ID 41（範例）、42–43（練習）：對應 Dict KV 結構
  - ID 44（範例）、45–46（練習）：對應雜湊查找 vs 線性搜尋
- 每道挑戰包含 YAML frontmatter、generator、starter_code，符合現有挑戰格式

## Non-Goals

- Tuple 不單獨出題；本節中 Tuple 僅作為 Dict 概念的補充介紹
- 不涵蓋進階字典用法（dict comprehension、巢狀 dict）——留給後續章節
- 不修改任何現有挑戰（ID 1–40）

## Capabilities

### New Capabilities

- `python-ch2-2-6-content`: Chapter 2 第 2-6 節教學內容與配套挑戰題（字典 Key-Value 結構、Tuple 旁白、雜湊查找 vs 線性搜尋），包含 `docs/tutor/py/ch2/2-6.md` 及挑戰題 ID 41–46

### Modified Capabilities

(none)

## Impact

- 新增檔案：
  - `docs/tutor/py/ch2/2-6.md`
  - `docs/challenge/py/ch2/41.md`
  - `docs/challenge/py/ch2/42.md`
  - `docs/challenge/py/ch2/43.md`
  - `docs/challenge/py/ch2/44.md`
  - `docs/challenge/py/ch2/45.md`
  - `docs/challenge/py/ch2/46.md`
- 無現有檔案被修改
- 依賴：現有的 tutor-article-structure spec、python-ch1-content spec（editorial rules P-1 through K-1）
