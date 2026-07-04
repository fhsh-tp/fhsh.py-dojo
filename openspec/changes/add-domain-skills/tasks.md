## 1. 題型 taxonomy：scaffold、型別與文件（TDD）

- [x] 1.1 於 `scripts/new-challenge.ts` 新增 `validateType`、`parseArgs` 的 `--type` 旗標（預設 `basic`）與 `buildContent` 輸出 `type` 欄位，並以 TDD 在 `scripts/new-challenge.test.ts` 先寫失敗測試、後實作至綠，涵蓋：`validateType('competition')` 通過、`validateType('gamified')` 回錯、無 `--type` 時 `parseArgs` 得 `type: 'basic'`、`--type competition` 被解析、`buildContent` 產出含 `type:`。滿足規格需求 Scaffold script validates and emits the exercise type。驗證：`node_modules/.bin/vitest --run scripts/new-challenge.test.ts` 全綠。
- [x] 1.2 於 `docs/shared/challenge.data.ts` 的 `DataChallenge` 新增 `type: ExerciseType`，並在 `transform` 以 `resolveExerciseType()`（來自 `docs/shared/exercise-type.ts`）做 runtime 解析——缺 `type` 或未知值皆解析為 `basic`（見 task 4.1，取代原先的 `?? 'basic'` 盲轉）。滿足規格需求 Data loader resolves exercise type with a basic default。驗證：`pnpm typecheck` 綠，且既有無 `type` 的題目在資料層解析為 `basic`。
- [x] 1.3 於 `Usage.md` 文件化 `type` 欄位與可擴充 taxonomy 狀態（`basic`／`competition` 已實作、`fill_in_blank`／`gamified` deferred、`guided` future placeholder），並指向 `.claude/skills/challenge-author/` skill。滿足規格需求 Challenge frontmatter supports an extensible exercise-type taxonomy。驗證：`grep -n "type\|competition\|fill_in_blank\|gamified\|guided" Usage.md` 涵蓋上述值與狀態。

## 2. 三個 committed 領域 skill（.claude/skills/）

- [x] 2.1 建立 `.claude/skills/challenge-author/SKILL.md`（YAML frontmatter 含 `name`/`description`），內容涵蓋 kebab-case 命名、`pnpm new-challenge <name> --type <type>` 用法、frontmatter 欄位（含選填 `reference_solution`）、generator 撰寫要點、Rust/Python 產生器一致性提醒、`content-regression` 驗證步驟、`basic` 與 `competition` 樣板差異。滿足規格需求 Repository provides committed challenge-authoring skill。驗證：檔案存在、`js-yaml` 可解析 frontmatter 含 name/description、內容審查涵蓋上列項。
- [x] 2.2 建立 `.claude/skills/phoenix-sci-writing/SKILL.md`（frontmatter 含 `name`/`description`），列出 15 條規則 ID（P-1、T-1、S-1、S-2、S-3、C-1、E-1、M-1、O-1、W-1、T-2、F-1、V-1、T-3、K-1）與各自判定要點，並指向正本 `phoenix-popular-science-article-style-enhance.md`。滿足規格需求 Repository provides committed Phoenix science-writing skill。驗證：`grep` 15 個規則 ID 皆在、且含正本檔指向。
- [x] 2.3 建立 `.claude/skills/eal-editorial-audit/SKILL.md`（frontmatter 含 `name`/`description`），描述 EAL 掃描順序（P-1→T-1→S-1→S-2→S-3→C-1→E-1→M-1→F-1→V-1→T-3→K-1→O-1→W-1→T-2）、逐輪修正、≤3 輪或零違規終止、violation log 概念，並指向 `editorial-audit-loop` spec 與正本文件。滿足規格需求 Repository provides committed editorial-audit-loop skill。驗證：`grep` 掃描順序與「3」輪終止敘述、含 `editorial-audit-loop` 指向。

## 3. 整體驗證

- [x] 3.1 跑四道 gate 確認全綠並驗證三個 skill frontmatter 可解析：`pnpm typecheck`、`pnpm lint`、`node_modules/.bin/vitest --run`、`pnpm gen:keymaterial && cargo test --manifest-path testcase-generator/Cargo.toml`。驗證：typecheck/lint 綠、vitest 全 passed（含新 new-challenge.test.ts）、cargo 73 passed、三個 SKILL.md 的 YAML frontmatter 皆可被 js-yaml 解析。

## 4. Audit round-1 修正（對抗式審查後）

- [x] 4.1 將題型 taxonomy 抽為單一真相來源 `docs/shared/exercise-type.ts`（`EXERCISE_TYPES`、`ExerciseType`、`resolveExerciseType`），`challenge.data.ts` 改用 `resolveExerciseType` 做 runtime 驗證（未知/typo 值解析為 basic 而非以 `as` 靜默信任），並新增 `docs/shared/exercise-type.test.ts` 覆蓋 absent/valid/invalid。同步將 `DataChallenge` 的 data-only 欄位列舉更新至 spec，滿足規格需求 Challenge type in challenge.type.ts is the single source of truth for view-layer fields。驗證：`node_modules/.bin/vitest --run docs/shared/exercise-type.test.ts` 全綠、typecheck 綠。
- [x] 4.2 `new-challenge.ts` 的 `parseArgs` 支援 `--flag=value` 語法（避免 `--type=competition` 被靜默丟棄），並在 `new-challenge.test.ts` 加 `--type=value` 與 `EXERCISE_TYPES` lockstep 測試。驗證：`node_modules/.bin/vitest --run scripts/new-challenge.test.ts` 全綠。
- [x] 4.3 修正 `phoenix-sci-writing` skill 的 V-1 規則（正本為 `> [!TYPE]` callout 語法，非 `:::` container），並於 `Usage.md` 加註頂層 `type` 與 params `type` 的免混淆說明。驗證：SKILL.md V-1 含 `> [!TYPE]`、Usage.md 含免混淆註記。
