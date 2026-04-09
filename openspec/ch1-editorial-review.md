# Discussion Conclusion: Chapter 1 Editorial Review

> **Date**: 2026-04-07
> **Trigger**: Phoenix's manual edits to `docs/tutor/py/ch1/1-1.md` (unstaged)
> **Scope**: `docs/tutor/py/ch1/index.md`, `1-1.md`, `1-2.md`, `1-3.md`, `1-4.md`
> **Decision**: Establish and apply a unified editorial discipline across all Chapter 1 content

---

## 1. Background

Chapter 1 content (`1-1` through `1-4`, plus `index.md`) was generated in a single session (`764e762`) and committed as-is. Phoenix subsequently made manual edits to `1-1.md` that reveal a set of editorial standards the original generation did not consistently meet. These edits are not cosmetic — they expose systemic gaps in pedagogical scaffolding, terminology handling, and prose rhythm that affect the entire chapter.

This document catalogs every change, explains the pedagogical reasoning behind it, identifies the TBD markers as a map of remaining work, and derives a set of editorial rules that must be applied to all five files.

---

## 2. Complete Inventory of Changes in 1-1.md

### 2.1 Punctuation Normalization (4 instances)

| Line | Before | After | Category |
|------|--------|-------|----------|
| 110 | `答案——但我連` | `答案，但我連` | em-dash → comma |
| 118 | `computer——拆開來看` | `**computer**，拆開來看` | em-dash → comma + bold |
| 206 | `用途——它會讓程式暫停` | `用途：它會讓程式暫停` | em-dash → colon |
| 208 | `搜尋框——它就是一個` | `搜尋框：它就是一個` | em-dash → colon |

**Rationale**: The Chinese em-dash `——` carries strong rhetorical weight — it signals dramatic pause or abrupt insertion. In literary prose this is a tool; in educational prose for zero-base high school students, overuse creates a choppy, stop-start rhythm that interrupts the "walk with me" flow a tutorial needs. The replacements are context-sensitive:

- **Comma** when the clause is a natural continuation (`答案，但...` — the reader should flow forward, not pause)
- **Colon** when the following clause is an explanation of the preceding term (`用途：它會...` — the colon says "here's what this means")
- **Bold** added to `**computer**` to restore the emphasis that the em-dash was originally providing

**Rule derived**: **P-1 — Prefer commas/colons over em-dashes in tutorial prose.** Reserve `——` only for genuine dramatic effect in hooks and jokes, not for routine clause separation. Apply globally.

### 2.2 Terminology Forward-Reference Elimination (2 instances)

| Line | Before | After |
|------|--------|-------|
| 148 | `還是「一個指令名稱」` | `還是「一個指令或資料儲存空間的名稱」` |
| 152 | `電腦以為 Hello 是一個變數名稱` | `電腦以為 Hello 是一個指令或是資料儲存空間的名稱` |

**Rationale**: This is the most pedagogically significant change. The concept of "變數 (Variable)" is formally introduced in **1-2**, not 1-1. In 1-1, the word "變數" appears exactly once in the `input()` section (L222), where it is used as a controlled forward reference — immediately followed by a parenthetical explanation and a promise that "下一節會正式介紹".

The `print()` section (L148, L152) precedes the `input()` section, so "變數" has not been mentioned at all yet. Using "變數名稱" here forces the reader to either:

1. Already know what a variable is (violating the zero-base premise), or
2. Accept an unexplained term and carry forward cognitive debt

The replacement `指令或資料儲存空間的名稱` is carefully constructed:
- **「指令」** covers Python built-in names (functions, keywords) — things the learner can intuitively understand as "commands the computer already knows"
- **「資料儲存空間」** describes variables in plain language without introducing the formal term — "a named place where data is stored"
- Together they accurately describe Python's name resolution behavior (`Hello` without quotes → Python looks for it as either a built-in or a user-defined name) without requiring any prior knowledge

**Rule derived**: **T-1 — Never use a formal term before its teaching point.** If a concept must be referenced before it's taught, describe it in plain language. If unavoidable (e.g., `input()` section mentioning "變數"), use a controlled forward reference: introduce the term, immediately explain in parentheses, and state when it will be properly taught.

**Audit implications for other files**:
- 1-2: Uses "字串串接" — is this term explained before first use?
- 1-2: Uses `f"{result:.1f}"` in a hint — already handled as "偷學一招" (controlled forward reference)
- 1-3: Uses "布林值" — properly introduced as the section's teaching point
- 1-3: Relies on understanding of `int`, `float`, `str` from 1-2 — legitimate backward reference
- 1-4: Review-only, should not introduce new terms

### 2.3 Narrative Scaffolding Additions (2 instances)

| Line | Before | After | Technique |
|------|--------|-------|-----------|
| 120 | `你用過計算機吧？` | `為什麼先解釋「電腦就是計算機呢？」那就得問你一個問題：你用過計算機吧？` | Meta-cognitive bridge |
| 124 | `計算機不會自作主張` | `沒錯！計算機不會自作主張` | Callback connector |

**L120 — Meta-cognitive bridge**: The original text establishes `computer = 計算機` then immediately launches into the calculator analogy. The revised version inserts a self-aware question: "Why am I telling you about calculators?" This is Socratic scaffolding — it models the reader's expected confusion ("why is the teacher talking about calculators when I'm trying to learn print()?") and redirects it into a purposeful setup.

For zero-base learners, this is critical. Without it, the reader must trust the teacher's relevance without understanding it. With it, the reader knows the analogy has a purpose *before* hearing it, which dramatically improves comprehension and retention.

**L124 — Callback connector**: After the 阿飄 joke (a deliberate tension-breaker), the original text immediately returns to serious exposition. The addition of `沒錯！` serves two functions:
1. It's an affirmative callback to the pre-joke assertion ("a calculator wouldn't auto-show the answer")
2. It signals to the reader: "the joke is over, we're back to the point, and the point still stands"

**Rule derived**: **S-1 — Every analogy needs a meta-cognitive bridge.** Before diving into a metaphor or comparison, spend one sentence telling the reader *why* this comparison is being made. **S-2 — After humor/digressions, use explicit connectors to resume the narrative thread.**

### 2.4 TBD Markers (6 instances)

These are the most important artifacts in the diff — they constitute a *map of remaining editorial work*.

#### TBD-A: Code block transitions (3 instances)

```
L134: <!-- TBD 加一個過場 -->          (before 第一步: print("Hello"))
L161: <!-- TBD 再加一個過場 -->         (before 第二步: print(1+1))
L181: <!-- TBD 加一個過場 -->          (before 第三步: print("你好", "世界"))
```

**Diagnosis**: The `print()` section has three subsections (印文字, 印計算結果, 印多個東西), each of which goes directly from `### heading` to ` ```python ``` ` with zero conversational setup. Compare this to the rest of 1-1:

- The "程式語言" section: 5 paragraphs of analogy before any technical content
- The "Judge 系統" section: 4 paragraphs of context before the step-by-step
- The "計算機" setup: 6 paragraphs of scaffolding before `print("Hello")`

Then suddenly, within the print() section itself, each sub-step is bare metal — heading → code → output → one-line explanation. The density drops from "rich conversational tutorial" to "reference manual".

**What each transition needs**: 1–2 sentences that:
1. Create a bridge from the previous step ("OK, you can print text. But what if you want the computer to do math for you?")
2. Set up *why* the next step matters ("If print() could only show fixed text, it'd be no different from pasting a sticky note on the screen")

**Rule derived**: **C-1 — Every code block must have a conversational lead-in.** No `### heading` → ` ```code``` ` without at least one sentence of setup.

#### TBD-B: Quote mixing warning

```
L155-156:
> [!WARNING] 想想英文文法
> <!-- TBD 說明不能把 `"` 跟 `'` 引號混用 （就是不能前雙後單這種包夾） -->
```

**Diagnosis**: The original text says `雙引號 " 或單引號 ' 都可以` but doesn't mention that you **cannot mix** them (`"Hello'`). This is a top-3 Python beginner syntax error. The `[!WARNING]` container + "想想英文文法" framing suggests the intended teaching strategy:

English grammar rule: opening and closing quotes must match → Python works the same way → `"..."` and `'...'` are both valid, but `"...'` is not.

This is an excellent analogy because the target audience (Taiwanese high school students) is actively learning English grammar and has internalized the "quotes must match" rule.

**Rule derived**: **E-1 — Address common beginner mistakes proactively**, especially syntax-level ones that would cause immediate WA/error. Don't wait for the "常見錯誤排查" section if the mistake relates to a concept just introduced.

#### TBD-C: Expression evaluation mental model

```
L174: <!-- TBD 說明 print(1+1) 時電腦中發生什麼事 -->
```

**Diagnosis**: This is the deepest pedagogical gap. The current text says `電腦會先算出 1+1 的結果，再把答案印出來` — one sentence for a concept that underpins every subsequent chapter:

- **1-1**: `print("Hello, " + name + "!")` — string concatenation evaluates before print
- **1-2**: `int(input())` — input() evaluates first, then int() wraps the result
- **1-2**: `total = quantity * price` — right-hand side evaluates before assignment
- **1-3**: `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)` — complex expression evaluation

The mental model needed is: **"Python evaluates from the inside out. It finishes computing the value inside the parentheses, then hands that result to the function."** If this is planted at `print(1+1)` in 1-1, it pays dividends all the way through 1-3.

**Rule derived**: **M-1 — When a code example implicitly demonstrates a fundamental concept, make it explicit.** The "inside-out evaluation" model is too important to be conveyed in a single throwaway sentence. It needs:
1. A clear statement of the model
2. A trace/walkthrough (e.g., `print(1+1)` → step 1: Python sees 1+1, computes 2 → step 2: Python sees print(2), prints "2")
3. A forward reference: "this pattern will come back when we learn int(input()) in the next section"

#### TBD-D: Section transition (print → input)

```
L202-206:
<!-- [START] TBD 過場太薄弱，需要加強 -->
電腦會說話了。但目前它只會自言自語——因為它還不會「聽」。
<!-- [END] TBD -->
```

**Diagnosis**: This is the major structural seam of 1-1. The article has two conceptual halves:
1. **Output** (print) — making the computer speak
2. **Input** (input) — making the computer listen

The transition between these halves is a single sentence. Compare to the narrative investment at every other structural boundary:
- Opening hook → "程式語言" section: 3 paragraphs
- "程式語言" → "Judge 系統": 2 paragraphs + callout box
- "Judge 系統" → "print()": 2 paragraphs of dialogue

The `[START]/[END]` wrapper signals this isn't a "add one more sentence" fix — the entire transition block needs redesign. Possible approaches:

1. **IPO callback**: "You've learned the O (Output) in IPO. Now let's learn the I (Input). Without input, your program is a monologue — it talks, but it never listens."
2. **Student dialogue**: "老師，我會讓電腦說話了。可是它怎麼知道我叫什麼名字？" → "好問題。它不知道——除非你告訴它。"
3. **Contrast setup**: Expand the "自言自語" metaphor — a robot that can only shout pre-programmed phrases vs. one that can ask questions and respond

**Rule derived**: **S-3 — Section-level transitions between major concepts require proportional scaffolding.** A one-sentence bridge is acceptable between sub-steps (e.g., 第一步 → 第二步). Between major conceptual shifts (output → input), the transition needs 2–4 sentences that: (a) summarize what was just learned, (b) identify the gap, and (c) motivate the next section.

---

## 3. Derived Editorial Rules (Summary)

| ID | Rule | Category | Status |
|----|------|----------|--------|
| **P-1** | Prefer commas/colons over em-dashes in tutorial prose. Reserve `——` for dramatic hooks/jokes only. Includes 5-point decision checklist. | Punctuation | **已修訂** |
| **T-1** | Never use a formal term before its teaching point. Use plain-language descriptions or controlled forward references. | Terminology | |
| **S-1** | Every analogy needs a meta-cognitive bridge — tell the reader *why* this comparison before making it. | Scaffolding | |
| **S-2** | After humor/digressions, use explicit connectors (沒錯！/ 回到正題 / etc.) to resume the thread. Includes H3 boundary relaxation. | Scaffolding | **已修訂** |
| **S-3** | Section-level transitions between major concepts require 2–4 sentences: summarize → identify gap → motivate. | Scaffolding | |
| **C-1** | Every code block must have a conversational lead-in. No heading → code without setup. | Code examples | |
| **E-1** | Address common beginner mistakes immediately after introducing the relevant syntax, not just in "錯誤排查". | Error prevention | |
| **M-1** | When a code example implicitly demonstrates a core concept (e.g., expression evaluation), make it explicit with a trace/walkthrough. | Mental models | |
| **F-1** | Image placeholders must use dual-line format: `![](path)` link + `> 📷` caption. No caption-only format. | Format | **新增** |
| **V-1** | VitePress custom containers must use `> [!TYPE]` syntax (with `!`). `> [TYPE]` without `!` will not render. | Format | **新增** |
| **T-3** | No empty custom container blocks. If content is not ready, wrap entire block in HTML comment. | Completeness | **新增** |
| **K-1** | Emotional punctuation density: at least 1 per 30 prose lines, no more than 1 per 10 prose lines. | Rhythm | **新增** |

---

## 4. Scope of Remaining Work

### 4.1 Immediate: Fill TBDs in 1-1.md

Six TBD markers need content:
1. Three code-block transitions (TBD-A)
2. Quote-mixing warning (TBD-B)
3. Expression evaluation explanation (TBD-C)
4. print→input section transition (TBD-D)

### 4.2 Cross-file: Apply editorial rules to 1-2, 1-3, 1-4, index

Each file needs to be audited against all 8 rules. Preliminary observations:

**1-2.md**:
- Multiple `——` usages (L19, and throughout) → P-1
- Code blocks for variable assignment/type conversion likely need lead-ins → C-1
- "置物櫃" analogy: does it have a meta-cognitive bridge? → S-1
- `int(input())` compound expression: is the evaluation model explicit? → M-1
- Transition "型別搞懂了？來看看數字能玩什麼花樣。" may be too thin → S-3

**1-3.md**:
- Multiple `——` usages → P-1
- `if-elif-else` code examples may need more conversational setup → C-1
- Complex boolean expression `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)` — evaluation model should callback to M-1 foundation → M-1
- Transition between "布林值" and "if-elif-else" sections → S-3

**1-4.md**:
- Primarily review content — lower density of issues expected
- Check that the "知識地圖" and "自我檢查表" accurately reflect final state of 1-1~1-3 after edits

**index.md**:
- May need title/description updates if section content changes significantly

### 4.3 Constraint: Phoenix Style Preservation

All edits must be written in Phoenix's established voice:
- Conversational, humorous, empathetic
- Traditional Chinese (Taiwan usage) with English for technical terms
- Student dialogue interjections as pedagogical devices
- Kaomoji for emotional punctuation
- Zero condescension — assumes the reader is smart but uninformed

---

## 5. Decision

**What was decided**: A systematic editorial pass across all Chapter 1 files, guided by 8 derived rules and 6 specific TBDs in 1-1.md.

**Rationale**: The changes Phoenix made to 1-1.md are not isolated cosmetic fixes — they establish a pedagogical discipline (terminology control, scaffolding density, mental model planting) that the AI-generated first draft didn't consistently achieve. Applying these rules retroactively to 1-2 through 1-4 will produce a coherent, learner-centered module rather than a collection of individually adequate but stylistically uneven sections.

**Next step**: `/spectra-propose` to create a formal change with file-level tasks.
