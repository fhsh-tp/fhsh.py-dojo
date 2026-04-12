## ADDED Requirements

### Requirement: Chapter 1 appendix contains Python keywords reference table

The file `docs/tutor/py/ch1/appendix.md` SHALL contain a dedicated H1 section titled `# Python Keywords Table` that presents a complete reference table for all Python 3.13 reserved words.

The table SHALL list every hard keyword returned by `keyword.kwlist` (35 entries: `False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`) and every soft keyword returned by `keyword.softkwlist` (4 entries: `_`, `case`, `match`, `type`), for a total of 39 rows.

The table SHALL be grouped by semantic category using H2 subheadings (for example: 常數值 / 邏輯運算 / 條件判斷 / 迴圈控制 / 函式與類別 / 例外處理 / 匯入 / 範圍與作用域 / 非同步 / 其他 / 軟關鍵字). Each row SHALL contain at minimum: the keyword itself, a one-line Traditional Chinese description, and a "first-taught" column indicating the chapter/section where the keyword is introduced or `—` if not yet taught.

The appendix SHALL include an introductory paragraph before the table explaining:
1. What "reserved words" are and why Python forbids using them as identifiers
2. A concrete `SyntaxError` example showing what happens if a learner tries `if = 3`
3. A pedagogical note distinguishing hard keywords from soft keywords (soft keywords are reserved only in specific contexts)

Keywords introduced in Chapter 1 (`True`, `False`, `and`, `or`, `not`, `if`, `elif`, `else`) SHALL be visually marked (e.g., with a checkmark emoji or the cell value `1-3`) so learners can self-assess progress.

#### Scenario: Appendix contains all 39 Python 3.13 keywords

- **WHEN** `docs/tutor/py/ch1/appendix.md` is rendered as HTML
- **THEN** the `# Python Keywords Table` section SHALL contain at least one row per keyword in `keyword.kwlist` and `keyword.softkwlist` under Python 3.13 (39 rows total)

#### Scenario: Chapter 1 taught keywords are marked

- **WHEN** a learner reads the keywords table after finishing section 1-3
- **THEN** the rows for `True`, `False`, `and`, `or`, `not`, `if`, `elif`, and `else` SHALL display a "first-taught" indicator pointing to section `1-3` (or an equivalent visual marker)

#### Scenario: Reserved word explanation precedes the table

- **WHEN** the appendix is read top-to-bottom
- **THEN** an explanatory paragraph defining "reserved words" and showing a `SyntaxError` example SHALL appear before the first keyword row of the table

#### Scenario: Soft keywords are distinguished from hard keywords

- **WHEN** the keywords table is rendered
- **THEN** soft keywords (`_`, `case`, `match`, `type`) SHALL be placed under a distinct subheading or column value that clearly identifies them as "soft" / context-sensitive keywords separate from hard keywords

## MODIFIED Requirements

### Requirement: Chapter 1 sections contain no residual TBD markers rule T-2

All `<!-- [START] TBD ... -->` / `<!-- [END] TBD -->` comment pairs and standalone `<!-- TBD ... -->` comments SHALL be resolved and removed from `docs/tutor/py/ch1/1-1.md` and `docs/tutor/py/ch1/appendix.md`. No placeholder or deferred-content markers SHALL remain in published tutorial sections of Chapter 1.

#### Scenario: No TBD markers in 1-1.md

- **WHEN** `docs/tutor/py/ch1/1-1.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found

#### Scenario: No TBD markers in appendix.md

- **WHEN** `docs/tutor/py/ch1/appendix.md` is scanned for HTML comment patterns matching `TBD`
- **THEN** zero matches SHALL be found
