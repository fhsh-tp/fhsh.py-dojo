## Why

教學文件中的數學公式目前以 Unicode 純文字呈現（如 `ax²`、`b² − 4ac`），無法正確顯示分數、根號等複雜數學符號。在 `setup-vitepress-mermaid-math` change 完成 LaTeX 基礎設施後，需要將現有的數學純文字轉換為 LaTeX 語法，讓公式能以專業的排版方式呈現。

## What Changes

- 將 `docs/tutor/py/ch1/1-3.md` 中二次方程式相關文字轉換為 LaTeX inline math（`$...$`）語法
- 將 `docs/challenge/quadratic-discriminant.md` 中的數學公式轉換為 LaTeX 語法

## Non-Goals

- 不修改任何 ASCII art 圖形（由後續 `convert-ascii-to-mermaid` change 處理）
- 不修改 VitePress 設定或安裝套件（已由 `setup-vitepress-mermaid-math` 處理）
- 不新增新的數學公式，僅轉換現有純文字

## Capabilities

### New Capabilities

（無。此 change 僅修改內容呈現方式，不新增功能。）

### Modified Capabilities

- `python-ch1-content`: 1-3 節中的數學公式改用 LaTeX 語法呈現

## Impact

- 受影響的檔案：`docs/tutor/py/ch1/1-3.md`（line 518、520）、`docs/challenge/quadratic-discriminant.md`（line 34、39）
- 前置依賴：`setup-vitepress-mermaid-math` change 必須先完成
