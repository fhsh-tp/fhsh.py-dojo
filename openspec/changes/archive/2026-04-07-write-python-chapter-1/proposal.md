## Why

fhsh.py-dojo 平台的 Python 自學課程目前只有章節骨架（index.md），尚無任何實際教學內容與 Judge 挑戰題。模組一（Chapter 1：與電腦溝通的基礎）是整門課程的起點，需要完整的教學文章和配套挑戰題，讓零基礎高一學生能夠自學 Python 基礎的 I/O、變數、運算、布林值與流程控制。

## What Changes

- 新增 4 個教學 section 檔案（`1-1.md` ~ `1-4.md`），使用 Phoenix 科普寫作風格，面向零基礎學生
- 新增 3 個例題 challenge（hello-world, beverage-cashier, leap-year），教學文中提供 step-by-step walkthrough
- 新增 7 個類題 challenge（self-introduction, parrot-echo, grade-average, change-calculator, seconds-converter, grade-level, triangle-check），供學生自行練習
- 更新 `ch1/index.md` 加入 `1-4` 總結連結
- 每個 section 搭配 Nano Banana Pro 圖片 prompt（美式火柴人四格漫畫），共 14 張圖片 placeholder

## Non-Goals (optional)

- 不涉及平台功能變更（VitePress、Pyodide、WASM 等基礎設施不變）
- 不包含圖片實際生成——僅提供完整的生成 prompt
- 不涉及模組二至模組四的內容

## Capabilities

### New Capabilities

- `python-ch1-content`: 模組一教學內容（4 個 section + 10 個 challenge），涵蓋 I/O、變數、型別、運算、布林值、流程控制

### Modified Capabilities

（無——本次變更純為內容新增，不修改任何既有 spec 的需求）

## Impact

- 新增檔案：`docs/tutor/py/ch1/1-1.md`, `1-2.md`, `1-3.md`, `1-4.md`
- 新增檔案：`docs/challenge/` 下 10 個 `.md` 檔案
- 修改檔案：`docs/tutor/py/ch1/index.md`（新增 1-4 連結）
- 依賴 spec：`tutor-article-structure`、`challenge-scaffold-script`、`challenge-link-component`、`tutor-data-loader`
