## Context

專案自 crypto-challenge fork 而來，改造為 Python 自學道場。目前 `.claude/skills/` 已進版控（內含 12 個 spectra-* skill 的實體 `SKILL.md` 目錄），但 0 個專案自訂領域 skill——出題流程、Phoenix 科普寫作 15 規則、Editorial Audit Loop（EAL）編審流程等領域知識散落在文件（`Usage.md`、`phoenix-popular-science-article-style-enhance.md`）與 spec（`editorial-audit-loop`）中，或依賴未進版控的全域 skill，無法可攜重用（報告風險 #3）。

同時題目 frontmatter 無「題型」分類。現況：`scripts/new-challenge.ts` 只處理 `difficulty`（easy/medium/hard），無 `type` 欄位；`docs/shared/challenge.data.ts` 的 `DataChallenge` 亦無 `type`。既有 54 題皆無 `type`。

參考素材：
- `phoenix-popular-science-article-style-enhance.md`（343 行）同時含 15 條寫作規則（P-1 / T-1 / S-1~3 / C-1 / E-1 / M-1 / O-1 / W-1 / T-2 / F-1 / V-1 / T-3 / K-1）與 EAL 工作流程（§三：掃描順序、≤3 輪、violation log）。
- `openspec/specs/editorial-audit-loop/spec.md` 為 EAL 的正式 spec（5 個 requirement）。
- `scripts/new-challenge.ts` 具 pure exported helpers（`validateDifficulty` / `parseArgs` / `buildContent` …），適合 TDD。

Phoenix 已定案：skill 放 `.claude/skills/<name>/`（與 spectra skill 並列、各自獨立子目錄）。

## Goals / Non-Goals

**Goals:**

- 把三件領域知識沉澱為隨 repo 版控、可攜、可 `/`叫用的 committed skill。
- 為題目建立可擴充的題型 taxonomy，本版落地 basic 與 competition。
- 保持既有 54 題完全相容（`type` 選填、預設 basic）。

**Non-Goals:**

- 不實作 `fill_in_blank` / `gamified` 的樣板或執行邏輯（僅於 spec 登錄為 deferred）。
- 不設計 `guided` 題型（僅 placeholder）。
- 不修改既有 54 題內容或 frontmatter。
- 不改寫 `editorial-audit-loop` spec 既有 requirement（skill 為其可執行封裝，不取代 spec）。
- 不動全域不可攜資產。

## Decisions

**D1：三個 skill 放 `.claude/skills/<name>/SKILL.md`，各自獨立子目錄。**
理由：Phoenix 定案。`.claude/skills/` 已版控且 spectra 升級只動 `spectra-*` 子目錄，故 `challenge-author` / `phoenix-sci-writing` / `eal-editorial-audit` 三個非 spectra 命名的子目錄不會被覆蓋。可被 Claude Code 原生 `/`叫用，且隨 repo 可攜。替代方案（頂層 `skills/`）被否決，因無法被 Claude Code 原生叫用。

**D2：skill 內容以「摘要契約 + 指向正本」封裝，不重複貼上全文。**
理由：15 條寫作規則與 EAL 流程的正本在 `phoenix-popular-science-article-style-enhance.md` 與 `editorial-audit-loop` spec。skill 提供可操作的摘要（規則 ID、判定要點、掃描順序、終止條件）並指向正本檔，避免內容雙寫漂移。

**D3：`type` 為選填、預設 `basic`，runtime union 只含已實作值。**
理由：既有 54 題無 `type`，選填 + 預設 basic 確保零破壞。validator 與 TS union 只接受 `basic | competition`（已實作）；`fill_in_blank` / `gamified` / `guided` 僅在 taxonomy spec 與 challenge-author skill 中登錄狀態，validator 目前拒絕它們，避免「接受了卻無樣板」的靜默失敗。taxonomy 因此可擴充但不會有半成品題型。

**D4：`type` 為 data-only 欄位，taxonomy 抽為單一真相來源 `docs/shared/exercise-type.ts`。**
理由：依既有 `challenge-type-unification` spec 的分層（view-layer 型別在 `challenge.type.ts`、data-only 欄位在 `DataChallenge`），`type` 屬 data/authoring metadata，加在 `DataChallenge`（`type: ExerciseType`），不動 view-layer `Challenge` interface。`EXERCISE_TYPES` / `ExerciseType` / `resolveExerciseType` 定義於 pure 模組 `docs/shared/exercise-type.ts`（不 import vitepress，故可獨立單元測試）；`challenge.data.ts` 的 transform 以 **`resolveExerciseType()` 做 runtime 檢查**（未知/typo 值 → `basic`），而非盲目的 `as ExerciseType` cast，確保手改的題目檔無法把未實作題型悄悄帶過 data layer。`scripts/new-challenge.ts` 保留自己的 `EXERCISE_TYPES`（避免 scripts↔app 跨匯入），並以測試斷言兩處 lockstep。

## Implementation Contract

**行為 1：三個 committed 領域 skill（domain-skills capability）**
- 觀察行為：`.claude/skills/challenge-author/SKILL.md`、`.claude/skills/phoenix-sci-writing/SKILL.md`、`.claude/skills/eal-editorial-audit/SKILL.md` 三檔存在，各具合法 YAML frontmatter（至少 `name`、`description`）。
- 內容契約：
  - `challenge-author`：涵蓋命名規則、`pnpm new-challenge <name> --type <type>` 用法、frontmatter 欄位（含選填 `reference_solution`）、generator 撰寫要點、Rust/Python 產生器一致性提醒、`content-regression` 驗證步驟、basic 與 competition 兩型別的樣板差異。
  - `phoenix-sci-writing`：列出 15 條規則的 ID 與判定要點，並指向正本 `phoenix-popular-science-article-style-enhance.md`。
  - `eal-editorial-audit`：描述 EAL 掃描順序（P-1→T-1→S-1→S-2→S-3→C-1→E-1→M-1→F-1→V-1→T-3→K-1→O-1→W-1→T-2）、逐輪修正、≤3 輪或零違規終止、violation log 概念，並指向 `editorial-audit-loop` spec 與正本文件。
- 驗收：三檔存在；`js-yaml` 可解析各檔 frontmatter 且含 name/description；內容涵蓋上列契約項（內容審查 + grep 關鍵字）。
- 範圍邊界：只新增三個 skill，不改 spectra skill、不改全域資產。

**行為 2：題型 taxonomy 與 scaffold（challenge-exercise-type capability）**
- 觀察行為：
  - 題目 frontmatter 支援選填 `type` 欄位；未提供時視為 `basic`。
  - `pnpm new-challenge <name> --type competition` 產出的檔案 frontmatter 含 `type: competition`；未給 `--type` 時含 `type: basic`。
  - `--type` 值非 `basic`／`competition` 時，script 印出錯誤並以非零碼結束。
  - `docs/shared/challenge.data.ts` 載入題目時，`DataChallenge.type` 對缺 `type` 的題目解析為 `basic`。
- 介面／資料形狀：`new-challenge.ts` 匯出 `validateType(type: string): string | null` 與（擴充後的）`ParsedArgs`／`buildContent` 含 `type`；`challenge.data.ts` 匯出或內部定義 `ExerciseType = 'basic' | 'competition'`，`DataChallenge` 含 `type: ExerciseType`。
- 失敗模式：未知 `type` → 明確錯誤訊息 + 非零 exit（非靜默接受）；缺 `type` → 靜默預設 basic（相容既有題）。
- 驗收：`scripts/new-challenge.test.ts`（TDD）涵蓋 validateType 正/反例、parseArgs 預設 basic 與 `--type` 解析、buildContent 輸出含 `type`；`pnpm typecheck`／`pnpm lint`／`node_modules/.bin/vitest --run`／cargo 四道 gate 全綠；既有 54 題（無 type）在 `challenge.data.ts` 解析為 basic（測試或手動確認）。
- 範圍邊界：只實作 basic／competition；deferred／future 題型僅登錄於 spec 與 skill，不進 validator/union。

## Risks / Trade-offs

- [`.claude/skills/<custom>` 被 spectra 升級誤刪] → 使用非 `spectra-*` 命名，spectra 只管自身子目錄；於 design 記錄，並可於 apply 後確認三檔仍在。
- [`type` 加入 `DataChallenge` 破壞既有題型別或顯示] → 選填 + transform 預設 basic，只加 data-only 欄位、不動 view Challenge；typecheck + vitest 驗證。
- [skill 內容與正本漂移] → 採「摘要 + 指向正本」策略（D2），不雙寫全文。
- [validator 接受未實作題型造成半成品] → union/validator 只含已實作值（D3），未知值明確報錯。

## Migration Plan

- 部署：合併即生效；既有題目無需修改。新題目可用 `--type` 指定，省略則 basic。
- 回滾：三個 skill 與 scaffold/型別改動均可 `git revert` 單一 commit 回滾；`type` 為選填，回滾後既有題不受影響。

## Open Questions

- 無。skill 位置已由 Phoenix 定案；deferred／future 題型範圍已明列 Non-Goals。
