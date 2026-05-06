## ADDED Requirements

### Requirement: Section 1-2 introduces string operators (concatenation and repetition)

Section `docs/tutor/py/ch1/1-2.md` SHALL include a dedicated subsection that formally introduces two string operators before any later chapter uses them:

1. **String concatenation `+`**: explains that `"Hello" + " " + "World"` produces `"Hello World"` and that the `+` operator on strings means joining (not arithmetic addition).
2. **String repetition with integer `*`**: explains that `"*" * 5` produces `"*****"` and that multiplying a string by a positive integer N repeats the string N times.

The subsection SHALL contrast string `+`/`*` with numeric `+`/`*` (same operator symbols, different semantics) and SHALL include at least one common-error note (e.g., `"abc" * 0` yields the empty string; `"abc" + 1` raises `TypeError`).

The subsection SHALL be positioned after the introduction of `str` (字串) within the existing "資料型別" H2 section and before the "input() 的型別陷阱" subsection, so that string operations are taught immediately after string type and before any I/O cast example.

#### Scenario: Section 1-2 contains string operator subsection

- **WHEN** the H3 headings under the "資料型別" H2 section of `docs/tutor/py/ch1/1-2.md` are listed in document order
- **THEN** an H3 subsection that introduces `+` (concatenation) and `*` (repetition) on strings SHALL appear after the H3 that introduces the three basic types and before the H3 that introduces `int(input())` cast usage

#### Scenario: String concatenation example produces correct output

- **WHEN** the code example `print("Hello" + " " + "World")` from the new subsection is executed
- **THEN** the output SHALL be exactly `Hello World` (one space between Hello and World, no trailing whitespace)

#### Scenario: String repetition example produces correct output

- **WHEN** the code example `print("*" * 5)` from the new subsection is executed
- **THEN** the output SHALL be exactly `*****` (five asterisks, no trailing whitespace)

#### Scenario: Subsection includes operator-overloading contrast note

- **WHEN** the new subsection is reviewed
- **THEN** it SHALL contain explicit prose stating that the `+` and `*` operators have different semantics for strings (join, repeat) versus numbers (add, multiply), so that a learner can answer the question "why does `+` join strings instead of adding them?"

#### Scenario: Subsection includes a common-error note

- **WHEN** the new subsection is reviewed
- **THEN** it SHALL include at least one warning, NOTE, or inline example of a common pitfall — for example, that `"abc" + 1` raises `TypeError` because `+` cannot mix str and int, and that `"abc" * 0` yields an empty string

##### Example: behavior table

| Expression | Result | Notes |
| ---------- | ------ | ----- |
| `"Hello" + "World"` | `"HelloWorld"` | concatenation, no implicit space |
| `"abc" * 3` | `"abcabcabc"` | repetition by positive integer |
| `"abc" * 0` | `""` | empty string |
| `"abc" + 1` | `TypeError` | cannot mix str and int with `+` |
| `"abc" * 1.5` | `TypeError` | repetition factor must be int, not float |
