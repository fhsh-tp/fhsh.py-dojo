## ADDED Requirements

### Requirement: Module 2 sections SHALL NOT use Python features before they are introduced anywhere in Ch1 or earlier Ch2 sections

Every Python feature used in any code block, hint, or example inside `docs/tutor/py/ch2/*.md` SHALL have been formally introduced (with a teaching block, NOTE/TIP, or dedicated subsection) in either Chapter 1 (`docs/tutor/py/ch1/*.md`) OR an earlier section of Chapter 2 (`docs/tutor/py/ch2/*.md` whose section number is lower than the current file's section number).

The cross-chapter audit SHALL specifically verify the following features are introduced before first use:

| Feature | First-use file | Required introduction location |
| ------- | -------------- | ------------------------------ |
| String concatenation `+` (str + str) | first appearance in any Ch2 file | Ch1 1-2 (per `python-ch1-content` Section 1-2 string operator subsection) |
| String repetition `*` (str * int) | first appearance in any Ch2 file | Ch1 1-2 (per `python-ch1-content` Section 1-2 string operator subsection) |
| Escape character `\t` in string literal | Ch2 2-4 multiplication-table example | Ch2 2-4 NOTE block before first `\t` usage (per `python-ch2-2-4-content`) |
| Escape character `\n` in string literal | first appearance in any Ch2 file | mentioned in the `\t` NOTE block as a sibling escape character, OR a dedicated NOTE if it appears before the `\t` example |
| f-string syntax `f"..."` | Ch2 2-4 multiplication-table example | Ch2 2-4 NOTE block before first f-string usage (per `python-ch2-2-4-content`) |
| f-string format spec `:N` (width padding) | Ch2 2-4 multiplication-table example | Ch2 2-4 f-string NOTE block (per `python-ch2-2-4-content`) |

The audit SHALL flag any Ch2 file that uses one of these features without the corresponding introduction being present at or before the use site.

#### Scenario: String concatenation in Ch2 has Ch1 1-2 introduction

- **WHEN** any Ch2 section file contains a code block, hint, or example that uses string `+` to concatenate two strings
- **AND** Ch1 1-2 has been audited for the string-operator subsection required by `python-ch1-content`
- **THEN** the audit SHALL pass for that Ch2 file's string-concatenation usage

#### Scenario: String repetition in Ch2 has Ch1 1-2 introduction

- **WHEN** any Ch2 section file contains `"<string>" * <int>` (string repetition by integer)
- **AND** Ch1 1-2 has been audited for the string-operator subsection required by `python-ch1-content`
- **THEN** the audit SHALL pass for that Ch2 file's string-repetition usage

#### Scenario: \t escape character in Ch2 has 2-4 introduction

- **WHEN** Ch2 2-4 contains a code block using the `\t` escape character
- **AND** Ch2 2-4 contains the NOTE block required by `python-ch2-2-4-content`
- **THEN** the audit SHALL pass for the `\t` usage

#### Scenario: f-string in Ch2 has 2-4 introduction

- **WHEN** Ch2 2-4 contains a code block using f-string syntax `f"..."`
- **AND** Ch2 2-4 contains the NOTE block required by `python-ch2-2-4-content`
- **THEN** the audit SHALL pass for the f-string usage

#### Scenario: Audit fails on missing introduction

- **WHEN** any Ch2 file uses one of the listed features
- **AND** the required introduction location does not contain the feature's introduction
- **THEN** the audit SHALL report a Critical violation identifying the file, line, and feature

##### Example: violation report

| File | Line | Feature | Status |
| ---- | ---- | ------- | ------ |
| `docs/tutor/py/ch2/2-4.md` | 461 | f-string `f"{i*j:4}"` | requires NOTE block before line 461 |
| `docs/tutor/py/ch2/2-4.md` | 170 | escape `\t` | requires NOTE block before line 170 |
| `docs/tutor/py/ch2/2-4.md` | 56 | string repetition `"*" * i` | requires Ch1 1-2 introduction (see `python-ch1-content`) |

---

### Requirement: Module 2 hints SHALL NOT introduce syntax that is forbidden by per-section specs

The cross-chapter audit SHALL verify that the "老師的提示" NOTE blocks in any Ch2 section do not contain Python syntax that has been explicitly forbidden in that section's per-section spec (e.g., `python-ch2-2-4-content` forbids unpacking `*`, list/dict/tuple literals, comprehensions, `def`, `lambda`, slicing, walrus in 2-4 hints).

#### Scenario: Forbidden syntax in hint triggers audit failure

- **WHEN** the cross-chapter audit scans a Ch2 file's "老師的提示" NOTE blocks
- **AND** a hint contains syntax forbidden by that section's per-section spec
- **THEN** the audit SHALL report a Critical violation citing the per-section spec and the forbidden syntax
