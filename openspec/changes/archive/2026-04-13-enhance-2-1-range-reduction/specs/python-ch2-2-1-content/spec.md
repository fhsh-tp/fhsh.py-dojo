## ADDED Requirements

### Requirement: Knowledge Point B includes range parameter reduction consolidation and arithmetic progression callout

Section 2-1 SHALL contain a subsection under `## range() 的完整用法` titled `### range 的三種寫法，其實是同一招`, positioned after the `### range(start, stop, step)：指定步長` subsection and before the `### 常見錯誤：差一錯誤` subsection.

This subsection SHALL:

1. Explain that `range(start, stop, step)` is the single complete form, and that `range(start, stop)` and `range(stop)` are shorthand versions that omit parameters with default values (`step` defaults to `1`, `start` defaults to `0`)
2. Use a step-by-step "peeling off" narrative structure: first demonstrate step omission (default `1`), then start omission (default `0`)
3. Include two fenced code block examples demonstrating the expansion: `range(3, 7)` expanding to `range(3, 7, 1)`, and `range(5)` expanding to `range(0, 5, 1)`
4. Include an ASCII flow diagram inside a fenced code block, showing the three-level reduction chain from `range(start, stop, step)` down to `range(stop)`, with annotations for each omitted parameter's default value
5. End with a `> [!TIP] 📌 數學小彩蛋` VitePress container that connects `range` output to arithmetic progressions (等差數列), mapping `start` to 首項 (a₁) and `step` to 公差 (d), and quoting the Python Tutorial 4.3 definition: "It generates arithmetic progressions."

The subsection SHALL comply with all 14 editorial rules applicable to non-opening sections, as defined in the `python-ch2-2-1-content` and `python-ch1-content` specs (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, W-1, T-2). O-1 (Opening Motivation) is not applicable as this is not a section opening.

#### Scenario: Parameter reduction subsection exists in correct position

- **WHEN** the H3 headings under `## range() 的完整用法` are listed in document order
- **THEN** `### range 的三種寫法，其實是同一招` SHALL appear after `### range(start, stop, step)：指定步長` and before `### 常見錯誤：差一錯誤`

#### Scenario: Three shorthand forms are expanded to their full equivalents

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain code demonstrating that `range(5)` is equivalent to `range(0, 5, 1)` AND that `range(3, 7)` is equivalent to `range(3, 7, 1)`

#### Scenario: Peeling-off narrative follows correct order

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** the explanation of step omission (`step` defaults to `1`) SHALL appear before the explanation of start omission (`start` defaults to `0`)

#### Scenario: Flow diagram shows reduction chain in a fenced code block

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain an ASCII diagram inside a fenced code block, with three levels showing `range(start, stop, step)` at the top, `range(start, stop)` in the middle, and `range(stop)` at the bottom, with each transition annotated with the omitted parameter and its default value

#### Scenario: Arithmetic progression callout uses correct container syntax and content

- **WHEN** the `> [!TIP]` callout at the end of the subsection is reviewed
- **THEN** it SHALL use `> [!TIP]` syntax (V-1 compliant), contain the exact Python Tutorial quote "It generates arithmetic progressions.", and explicitly map `start` to 首項 (a₁) and `step` to 公差 (d)

#### Scenario: No new kaomoji exceed the per-file limit

- **WHEN** the entire `docs/tutor/py/ch2/2-1.md` file is scanned for kaomoji occurrences after the insertion
- **THEN** each distinct kaomoji used in the new subsection SHALL appear at most 2 times in the entire file (K-1 compliant)
