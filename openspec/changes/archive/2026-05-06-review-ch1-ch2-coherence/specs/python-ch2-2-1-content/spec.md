## ADDED Requirements

### Requirement: Section 2-1 explains the rationale for half-open range intervals

Section `docs/tutor/py/ch2/2-1.md` SHALL contain a NOTE or TIP block that explains WHY `range(start, stop)` excludes `stop` (the half-open interval design). The explanation SHALL list at least the following three rationales, each presented as one short sentence using a concrete example a Taiwan high-school student can verify by hand:

1. **Length is easy to compute**: `range(a, b)` contains exactly `b - a` numbers, so `range(1, 7)` has `7 - 1 = 6` numbers without any +1 or -1 correction.
2. **Empty interval is natural**: `range(5, 5)` represents zero numbers; with closed intervals an empty interval would require an awkward notation such as `[5, 4]`.
3. **Clean splitting**: `range(0, 10)` can be split as `range(0, 5)` followed by `range(5, 10)` with no overlap and no gap, which matches how list slicing and divide-and-conquer algorithms work.

The block SHALL be positioned within or immediately adjacent to the existing "常見錯誤：差一錯誤" subsection so that the rationale appears together with the off-by-one warning. The previous hand-waving phrase "用久了你會發現這個設計其實很方便（後面會解釋為什麼）" SHALL be removed or rewritten so that the section no longer defers the explanation indefinitely.

#### Scenario: Three rationales appear together

- **WHEN** the rationale block in section 2-1 is reviewed
- **THEN** the block SHALL contain three labelled rationales (length, empty interval, clean splitting), each with a concrete numeric example a learner can verify

#### Scenario: Indefinite deferral phrase is removed

- **WHEN** section 2-1 is scanned for the phrase pattern "用久了你會發現這個設計其實很方便（後面會解釋為什麼）"
- **THEN** zero occurrences SHALL remain

---

### Requirement: Section 2-1 includes a "range is not a list" note

Section `docs/tutor/py/ch2/2-1.md` SHALL contain a NOTE block that addresses the common beginner confusion of treating `range(n)` as a list. The block SHALL:

1. Show that `print(range(5))` outputs `range(0, 5)`, not `0 1 2 3 4` or `[0, 1, 2, 3, 4]`.
2. Explain in one sentence that `range` is a "lazy sequence" object that produces numbers on demand rather than storing them eagerly.
3. Show that `list(range(5))` produces `[0, 1, 2, 3, 4]` for the case where the learner wants to inspect the full sequence — and explicitly mark `list` as a forward reference (taught in a later chapter).

The block MUST appear after the three-form `range()` teaching is complete and before the section's "本節小結" closing summary, so that learners encounter the clarification while the `range()` material is still fresh.

#### Scenario: Note explains print(range(n)) output

- **WHEN** the "range is not a list" note in section 2-1 is reviewed
- **THEN** it SHALL contain a code example or inline statement showing that `print(range(5))` outputs `range(0, 5)`

#### Scenario: Note shows list(range(n)) inspection method

- **WHEN** the "range is not a list" note in section 2-1 is reviewed
- **THEN** it SHALL contain a code example or inline statement showing that `list(range(5))` outputs `[0, 1, 2, 3, 4]`, with `list` marked as a forward reference

---

### Requirement: Section 2-1 uses unified step terminology

Section `docs/tutor/py/ch2/2-1.md` SHALL use a single, unified terminology for describing the `step` parameter of `range()`:

- For positive `step` (forward iteration): the section SHALL use the phrase pattern "每次加 N" (where N is the absolute value).
- For negative `step` (backward iteration): the section SHALL use the phrase pattern "每次減 N" (where N is the absolute value, no negative sign in the phrase).
- The Mathematical synonym 「步長」may be used in formal definitions and 「公差」may be used in arithmetic-progression contexts, but the running prose SHALL consistently use 「每次加 N」/「每次減 N」.

The following alternative phrases SHALL NOT appear when describing `step` in section 2-1: 「每次跳 N」, 「每次增加 N」, 「每隔 N 遍」, 「每次加 -N」.

In particular, the existing description "如果你想『每隔 2 遍寫一次』" is technically incorrect (it describes a strided sequence with stride 3, not 2) and SHALL be rewritten to use the unified phrase 「每次加 2」.

#### Scenario: Step terminology is unified to "每次加 N" / "每次減 N"

- **WHEN** section 2-1 is scanned for descriptions of the `step` parameter
- **THEN** every description SHALL use the phrase pattern 「每次加 N」 (positive step) or 「每次減 N」 (negative step)

#### Scenario: Misleading "每隔 N 遍" phrase is removed

- **WHEN** section 2-1 is scanned for the phrase 「每隔 2 遍寫一次」 or similar 「每隔 N 遍」 patterns referring to `step`
- **THEN** zero occurrences SHALL remain

#### Scenario: Negative step is described with positive magnitude

- **WHEN** section 2-1 describes a `range(...)` call with a negative `step`
- **THEN** the prose SHALL describe the behavior as "每次減 |step|" (using the absolute value), not as "每次加 -|step|"

##### Example: replacement table

| Old phrase | Replacement |
| ---------- | ----------- |
| 「如果你想『每隔 2 遍寫一次』」 | 「如果你想『每次加 2』，產生像 0, 2, 4, 6, 8 這樣的數列」 |
| 「`i` 每次跳 2」 | 「`i` 每次加 2」 |
| 「每次加 -2」 | 「每次減 2」 |
| 「從 1 開始，每次跳 2」 | 「從 1 開始，每次加 2」 |

## MODIFIED Requirements

### Requirement: Knowledge Point B includes range parameter reduction consolidation and arithmetic progression callout

Section 2-1 SHALL contain a subsection under `## range() 的完整用法` titled `### range 的三種寫法，其實是同一招`, positioned after the `### range(start, stop, step)：指定步長` subsection and before the `### 常見錯誤：差一錯誤` subsection.

This subsection SHALL:

1. Frame the three forms of `range()` as **three convenient call styles** that the language provides for three common scenarios, rather than as a single form with "omitted" parameters. The three styles are: full form `range(start, stop, step)`, two-argument form `range(start, stop)` (used when the step is `1`), and one-argument form `range(stop)` (used when both the start is `0` and the step is `1`).
2. Use a step-by-step narrative structure that introduces the three styles in order of increasing parameter count: first show one-argument form, then two-argument, then full form, OR present the full form and then explain how the shorter forms cover the most common defaults — but in either order, the prose SHALL avoid claiming that the shorter forms are "really" the full form with hidden default arguments.
3. Include two fenced code block examples that show the three forms producing equivalent sequences in their respective common scenarios — for example, `range(5)` for "from 0 with step 1", `range(3, 7)` for "from start with step 1", and `range(0, 10, 2)` for "with explicit step".
4. Include a diagram (ASCII inside a fenced code block, or Mermaid) that summarises the three styles side-by-side with a short label for each (e.g., "shortest", "with start", "with step"), without using the word 「省略」 (omission) or claiming hidden defaults.
5. End with a `> [!TIP] 📌 數學小彩蛋` VitePress container that connects `range` output to arithmetic progressions (等差數列), mapping `start` to 首項 (a₁) and `step` to 公差 (d), and quoting the Python Tutorial 4.3 definition: "It generates arithmetic progressions."

The subsection SHALL comply with all 14 editorial rules applicable to non-opening sections, as defined in the `python-ch2-2-1-content` and `python-ch1-content` specs (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, W-1, T-2). O-1 (Opening Motivation) is not applicable as this is not a section opening.

#### Scenario: Parameter reduction subsection exists in correct position

- **WHEN** the H3 headings under `## range() 的完整用法` are listed in document order
- **THEN** `### range 的三種寫法，其實是同一招` SHALL appear after `### range(start, stop, step)：指定步長` and before `### 常見錯誤：差一錯誤`

#### Scenario: Three forms are presented as convenient styles, not as omissions

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** the prose SHALL describe the three forms as "三種便利寫法" or equivalent neutral phrasing
- **AND** the prose SHALL NOT use the word 「省略」 to describe how `range(5)` relates to `range(0, 5, 1)`
- **AND** the prose SHALL NOT claim that `range(5)` is "really" `range(0, 5, 1)` with default arguments

#### Scenario: Three forms each have a labelled code example

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain at least one code example for each of the three forms (`range(stop)`, `range(start, stop)`, `range(start, stop, step)`), each labelled with the scenario it covers

#### Scenario: Diagram summarises three styles without omission language

- **WHEN** the parameter reduction subsection is reviewed
- **THEN** it SHALL contain a diagram (ASCII inside a fenced code block, or Mermaid) showing the three styles side-by-side with neutral labels
- **AND** the diagram annotations SHALL NOT contain the word 「省略」 or any phrase claiming hidden defaults

#### Scenario: Arithmetic progression callout uses correct container syntax and content

- **WHEN** the `> [!TIP]` callout at the end of the subsection is reviewed
- **THEN** it SHALL use `> [!TIP]` syntax (V-1 compliant), contain the exact Python Tutorial quote "It generates arithmetic progressions.", and explicitly map `start` to 首項 (a₁) and `step` to 公差 (d)

#### Scenario: No new kaomoji exceed the per-file limit

- **WHEN** the entire `docs/tutor/py/ch2/2-1.md` file is scanned for kaomoji occurrences after the rewrite
- **THEN** each distinct kaomoji used in the rewritten subsection SHALL appear at most 2 times in the entire file (K-1 compliant)
