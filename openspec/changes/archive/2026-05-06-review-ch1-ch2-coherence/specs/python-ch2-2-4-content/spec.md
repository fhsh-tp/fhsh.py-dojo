## ADDED Requirements

### Requirement: Section 2-4 introduces escape character `\t` and f-string before first use

Section `docs/tutor/py/ch2/2-4.md` SHALL contain a NOTE block (or two adjacent NOTE blocks) that explains the `\t` escape character and the `f"..."` f-string syntax BEFORE the first code block in the section that uses either feature.

The escape-character explanation SHALL:
1. State that `\t` inside a string literal represents the **Tab** character (製表符).
2. State that `\t` advances the cursor to the next tab stop, which is the standard mechanism for column alignment in console output.
3. Mention briefly that strings can contain other backslash-prefixed special characters (called 跳脫字元 / escape characters), with `\n` (newline) named as an example, so the learner has a category label rather than thinking `\t` is a one-off symbol.

The f-string explanation SHALL:
1. State that an `f` prefix on a string literal (e.g., `f"Hello, {name}"`) enables embedded expressions inside `{ ... }` braces.
2. Explain the format-spec form `f"{value:N}"` where `N` is a positive integer that pads the value to at least `N` characters wide (right-aligned by default).
3. Note that f-string was previewed in section 1-2 as "後面才會學" and is now being formally introduced.

The NOTE blocks SHALL be positioned in document order before the first occurrence of `\t` AND before the first occurrence of `f"..."` in section 2-4.

#### Scenario: Escape character note appears before first \t usage

- **WHEN** section 2-4 is parsed in document order
- **THEN** a NOTE block explaining `\t` SHALL appear before the first code block containing the literal `"\t"` or `'\t'`

#### Scenario: F-string note appears before first f"..." usage

- **WHEN** section 2-4 is parsed in document order
- **THEN** a NOTE block explaining f-string syntax (including the `:N` format spec) SHALL appear before the first code block containing an `f"..."` literal

#### Scenario: F-string note covers width format spec

- **WHEN** the f-string NOTE block is reviewed
- **THEN** it SHALL contain at least one example showing `f"{value:N}"` where `N` is a positive integer, with prose explaining that the value is padded to at least `N` characters wide and is right-aligned by default

#### Scenario: Escape character note labels the category

- **WHEN** the `\t` NOTE block is reviewed
- **THEN** it SHALL contain the term 「跳脫字元」 (escape character) and SHALL mention at least one other escape character (e.g., `\n`) as a category example

---

### Requirement: Section 2-4 hints SHALL NOT use unintroduced advanced syntax

The "老師的提示" NOTE blocks attached to practice problems in section `docs/tutor/py/ch2/2-4.md` SHALL NOT introduce or rely on Python syntax that has not yet been formally taught in any preceding section (Ch1 1-1 through Ch2 2-4 inclusive). The following advanced features SHALL NOT appear in 2-4 hints, regardless of brevity:

- Sequence unpacking with `*` in a function call (e.g., `print(*range(1, i+1))` or `print(*sequence)`).
- List, dict, tuple, set literal syntax (e.g., `[1, 2, 3]`, `(1, 2)`, `{1, 2}`).
- List comprehension or generator expression syntax (e.g., `[x for x in ...]`, `(x for x in ...)`).
- Function definition (`def`), lambda (`lambda`), or any callable construction.
- Slicing syntax (`a[i:j]`, `a[::-1]`, etc.).
- The walrus operator `:=`.

If a hint genuinely needs an alternative approach beyond the doubly-nested loop and the string operators introduced in 1-2, the hint SHALL describe it in prose only (e.g., "another approach uses string repetition `"*" * n`") without showing unintroduced syntax.

#### Scenario: No unpacking in 2-4 hints

- **WHEN** the "老師的提示" NOTE blocks in section 2-4 are scanned for the pattern `print(*` or `*range(` or `*list(` or any leading-`*` argument-unpacking usage
- **THEN** zero matches SHALL be found

#### Scenario: No list/comprehension/lambda/slicing in 2-4 hints

- **WHEN** the "老師的提示" NOTE blocks in section 2-4 are scanned for syntax fragments matching list literal `[...]`, list comprehension `[x for ...]`, generator `(x for ...)`, `def `, `lambda `, slicing `[...:...]`, or `:=`
- **THEN** zero matches SHALL be found, except for syntax explicitly listed as taught in or before Ch2 2-4 (e.g., the `[!NOTE]` markdown container which is unrelated to Python list syntax)

#### Scenario: String repetition hint is allowed because 1-2 introduces it

- **WHEN** a "老師的提示" NOTE block in section 2-4 references string repetition such as `"*" * n` or `" " * (n - i)`
- **THEN** the hint SHALL be accepted (this syntax is formally taught in Ch1 1-2 by the `python-ch1-content` capability)
