## Why

Ch1（與電腦溝通的基礎）與 Ch2（迴圈與重複結構）已完成初稿，但跨章節審核後發現 Ch2 有 4 處「概念尚未介紹就被使用」的連貫性破洞（字串乘法、`\t` 跳脫字元、`f-string` 格式化、序列展開 `print(*range(...))`）；同時，其他老師反映 Ch2-1 的 `range()` 說明在「為什麼包頭不包尾」「省略鏈」「步長用語」等處有不嚴謹之處，並包含一處實際技術錯誤（「每隔 2 遍寫一次」應為「每次加 2」）。對「高一完全零基礎、自學」的學生而言，這些破洞與不一致會直接影響學習體驗，必須在更多學生使用前修正。

## What Changes

- **1-2.md**：在「資料型別」段落新增「字串也能做運算」小節，正式介紹字串 `+`（串接）與 `*`（重複）運算，為 Ch2 圖案題鋪路。
- **2-1.md**：
  - 補充「為什麼 range 包頭不包尾」的實際理由（Dijkstra 三點：長度好算、空集合自然、可乾淨切分）。
  - 重寫「三種寫法的省略鏈」為更誠實的「三種便利寫法對應三種場景」描述。
  - 新增「range 不是 list」的小提醒。
  - 通篇統一「步長/公差」用語為「每次加 N」「每次減 N」，特別修正錯誤描述「每隔 2 遍寫一次」。
- **2-4.md**：
  - 在九九乘法表使用 `\t` 與 `f-string` 之前新增 NOTE 區塊解釋這兩個語法。
  - 移除/改寫進階提示中提前出現的概念（`print(*range(...))` 序列展開、超出鋪陳的字串相加）。
- 不影響 Judge 題目的題目內容、不影響 Ch1-1、Ch1-3、Ch1-4、Ch2-2、Ch2-3、Ch2-5。

## Non-Goals (optional)

詳見 design.md 的 Goals / Non-Goals 章節。

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `python-ch1-content`: 1-2 新增字串運算（`+`、`*`）小節，更新章節結構需求。
- `python-ch2-2-1-content`: 2-1 重寫 range 說明、統一步長用語、補連貫性說明。
- `python-ch2-2-4-content`: 2-4 補 `\t` 與 `f-string` 的 inline 教學區塊、移除進階提示。
- `ch2-cross-chapter-audit`: 增補「字串運算、跳脫字元、f-string」三項概念在 Ch1+Ch2 內的「介紹前不得使用」連貫性檢查項目。

## Impact

- Affected specs:
  - 修改：`openspec/specs/python-ch1-content/spec.md`
  - 修改：`openspec/specs/python-ch2-2-1-content/spec.md`
  - 修改：`openspec/specs/python-ch2-2-4-content/spec.md`
  - 修改：`openspec/specs/ch2-cross-chapter-audit/spec.md`
- Affected code:
  - Modified:
    - `docs/tutor/py/ch1/1-2.md`
    - `docs/tutor/py/ch2/2-1.md`
    - `docs/tutor/py/ch2/2-4.md`
- Affected workflows:
  - 每個 Phase 完成後強制執行 `/spectra-audit`，由 3 個 sub-agent 並行稽核（連貫性、技術正確性、用語與教學品質）。
