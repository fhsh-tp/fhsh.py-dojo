## Context

Three counting problems adapted from a public problem set fill the `easy` gap in the APCS literacy series (`apcs001`–`apcs014` are all `medium` or `hard`). None of the three can be translated literally: their original discrimination rests on C++ integer overflow and on time limits calibrated for compiled languages, neither of which reproduces under Pyodide. Each therefore needs a re-derived discrimination axis.

All specification decisions come from a seven-point interview held on 2026-08-15. Every decision is recorded below together with what was rejected — an auditor who cannot see the rejected options will re-raise settled trade-offs as defects.

`trace-matrix.md` is this change's single source of truth. Every number below carries a fact id; prose derives from the matrix, never the other way round.

## Goals / Non-Goals

**Goals:**

- Ship three `category: apcs`, `type: competition` challenges whose life-context narratives never name the underlying mathematics.
- Give each challenge a discrimination axis that actually works under Pyodide, and make the three axes different from one another.
- Make every shipped number regenerable: assertion walls produce the literals, a shared module produces the operation counts, and both live in the repository.

**Non-Goals:**

- No engine change. The operation counter, the per-testcase deadline and the sandbox guard are untouched, and no existing challenge is recalibrated.
- No closing of the residue that all-literal test inputs reach the client bundle and are public in the repository (fact C6). It is project-level and shared with `apcs009`–`apcs014`.
- No general exchange-base parameter for the token challenge (decision D5).
- No teaching article.

## Decisions

### Interview decisions

| # | Decision | Rejected, and why |
|---|---|---|
| Q1 (D1) | All three go to the `apcs` series; ids assigned by the scaffold | "All to the `py` basics series" conflicts with the literacy framing; "two `py` plus one `apcs`" would need two authoring templates for one batch. Side effect: fills the series' missing `easy` rung |
| Q2 (D2) | `marquee-display-count` discriminates by context translation only; **no cost cliff is built** | "Rewrite as an adjacent-not-equal recurrence" is no longer the source problem and exceeds `easy`; "push n to 10^18 to force modular exponentiation" makes the wrong route die by `MemoryError` rather than by timeout, which is not a clean death |
| Q3 (D3) | `ap-layout-plan` keeps per-side-length output for 1 through n | "Ask about a single size" loses the row-of-numbers pattern that carries the teaching value |
| Q4 (D4) | `ap-layout-plan` is `easy`, its page carries the k=1..5 answer table, and it does **not** reveal the 2x3 block insight | "medium plus reveal the block" and "hard with no hint at all" |
| Q5 (D5) | The exchange rate is fixed at twelve | "Keep base ten" — the rule is published everywhere and a student can copy one line; "read the base from input" needs prime factorisation and is `hard` for this audience |
| Q6 (D6) | Access point layout / marquee display / fairground token exchange | Three alternates unused. The token challenge deliberately avoids packing vocabulary because `apcs009` is already a packing challenge |
| Q7 (D7) | See the parameter table below; three 20-entry all-literal plans, first entry equal to the page's worked example, independent `reference_solution` each | "Push 016 to 10^18" and "drop 017 to n <= 10^6" — the latter would make more students believe the factorial is computable |

### The n bound for `ap-layout-plan` is 1000, not 3000 (fact E7)

The interview settled on 3000. Measurement overturned it, and the maintainer re-decided.

The binding gate for this challenge is the operation counter, not the wall clock (fact E11). At n=3000 the three natural spellings of one and the same O(n^2) algorithm land on opposite sides of the limit: an explicit inner loop costs 9,051,479 operations and survives, a generator-expression `sum` costs 13,567,551 and dies, an extracted helper function costs 22,561,127 and dies. Two students with the same idea and the same output would receive opposite verdicts because one of them wrote `sum`. The page cannot warn about this without revealing that the challenge counts operations.

At n=1000 all three spellings survive with the most expensive one holding a 3.98x margin (fact E6). The discrimination is unaffected: the O(n^3) route already dies from n=249 upward in the browser, so any bound above roughly 250 discriminates identically. The bound of 3000 bought no difficulty, only the knife-edge.

The rejected alternative was to raise the bound to 4000, which kills all three O(n^2) spellings and admits only the closed form. That is a clean contract too, but it makes the challenge materially harder than `easy` — a student who groups by row offset but does not sum the arithmetic series would time out.

### Parameter table

| Challenge | Input | Bound | Output | Discrimination axis |
|---|---|---|---|---|
| `ap-layout-plan` | one integer n | 1 <= n <= 1000 | n lines | cost: per-cell scanning dies (fact E8) |
| `marquee-display-count` | one line, two integers n and k | 1 <= n <= 10^6, 0 <= k <= n | one line | context translation: the free count is n-k (fact F4) |
| `fair-token-exchange` | one integer n | 1 <= n <= 10^9 | one line | context translation: twelve is not ten (fact G4) |

### Measurement methodology

Three properties of the judge's operation counter are load-bearing and were each got wrong at least once during curation, so the reasoning is recorded rather than left to be rediscovered.

The counter increments on **every** trace event with no filtering of event type or filename, and its tracer returns itself so nested calls stay traced (fact C2). A probe that counts only `line` events systematically under-reports any spelling whose hot path contains a function call. This change therefore permits exactly one operation-counting implementation, `verify/judge_ops.py`; every other tool imports it. Its self-test fails if the reproduction ever loses the call and return events.

Operation counts are independent of execution speed and transfer unchanged to the browser, because Pyodide executes the same CPython bytecode (fact C3). Wall-clock numbers do not transfer and are treated as indicative only, with a fixed multiplier of four applied to local CPython timings and stated as an estimate everywhere it appears.

Wall clock is sampled seven times and the minimum is taken (fact C5). Operation counts destined for documents are taken from a **fresh interpreter process**, because a module's first import is charged to the first testcase that triggers it — `import math` costs 278 events cold and zero warm (fact C4).

### Deliberate deviations

These are settled trade-offs, not defects. An audit that re-raises them is re-litigating a maintainer decision.

1. **`ap-layout-plan` is labelled `easy` although brute-force enumeration cannot pass.** The difficulty label measures the depth of the mathematical reasoning, which the maintainer places inside the senior-high curriculum, not the depth of the programming technique. This is the series' first `easy` challenge carrying a cost cliff.
2. **`marquee-display-count` has no cost cliff at all.** Decision D2. Every reasonable spelling passes, including the O(n) loop.
3. **The `math.factorial` route on two of the challenges does not die cleanly.** Browser measurement made this precise, and narrower than the original statement. A `math.factorial` call with a moderate argument returns quickly, and expensive work following it runs at bytecode level and *is* interrupted cleanly — a bounded variant receives a clean timeout at 5,041 ms and scores 19/20 (fact W3). What defeats the interrupt is a single C call with an argument so large that it never returns: the flag is never examined, the worker dies, and **every** result is discarded, so the student sees 0/20 with all entries marked not executed rather than the score the surviving entries earned (facts E10, G7, W4). The page recovers on the next submission (fact W5). The counter cannot see any of this: the two routes consume 577 and 98,699 operations. This is an engine-level residue of the same family as `sys.settrace(None)` and is out of scope here.

## Implementation Contract

**Observable behaviour.** Three new challenge pages appear under `/apcs-challenges` with ids assigned by the scaffold. Each accepts the input shape in the parameter table, produces the output described in its I/O contract, and judges twenty testcases. A submission implementing any route marked ACCEPTED or REFERENCE in the trace matrix scores 20/20; a submission implementing any route marked KILLED or WRONG_ANSWER scores exactly the value recorded there.

**Data shape.** Each page's frontmatter carries `layout`, `id`, `title`, `difficulty`, `category: apcs`, `type: competition`, `algorithm`, `params`, `input_budget`, a 20-entry all-literal `testcase_plan`, `generator`, `reference_solution`, and `starter_code` set to the empty string. The `algorithm`, `params`, `input_budget` and `testcase_plan` values are produced by `curation/assemble.py` and copied byte-for-byte; they are never hand-edited. `generator` and `reference_solution` are implemented independently of each other.

**Failure modes.** `assemble.py` exits non-zero and writes no file when it detects a banned data-structure or algorithm term, an expected-answer key in its input, or a comment inside a testcase plan (fact C7). Each assertion wall exits non-zero without emitting literals when any of its contracts is violated. These failures are loud by design; there is no fallback path that ships partial output.

**Acceptance criteria.**

- `python3 curation/plan015.py`, `plan016.py`, `plan017.py` each exit zero and regenerate their literals identically after the outputs are deleted.
- `python3 curation/assemble.py` reproduces the three frontmatter fragments byte-for-byte, and rejects a deliberately poisoned input.
- `python3 verify/judge_ops.py` self-test passes.
- `python3 verify/crosscheck_trio.py` reports no mismatch against an independently written expectation.
- `pnpm build:pools` succeeds and `scripts/content-regression.test.ts` passes for all three challenges (fact B1, proven).
- `scripts/challenge-params.test.ts` passes (fact B2, proven).
- Every number in every page, in the spec delta and in this document maps to a fact id in `trace-matrix.md`.

**Scope boundaries.** In scope: three challenge pages, the curation evidence, the trace matrix, one spec delta. Out of scope: engine behaviour, existing challenges, the public-literal residue, teaching articles, and any change to the operation limit or the deadline.

## Risks / Trade-offs

**Browser verification is complete, and it overturned three conclusions that local measurement had produced.** The kill mechanism of the per-cell scanning route was recorded as a deadline timeout; it is in fact the operation limit, and the page's performance note had to be reworded accordingly (facts E8, S7). The two `math.factorial` routes were recorded at 8/20 and 13/20 by projecting the deadline onto local per-entry timings; both actually score 0/20, because that projection cannot model a worker that dies and discards results already earned (facts E10, G7, W4).

The general lesson is recorded here because it will recur: the operation count transfers from local CPython to the browser unchanged, but **anything derived from wall clock, including a route's score, does not** — a projected score is a model, and this model was wrong about three of the twenty-six routes. Only the browser evidence in the trace matrix's W section may be quoted as a browser score.

**One wrong route on `fair-token-exchange` scores 12/20 and cannot be pushed lower.** Because the answer is a minimum of two quantities, one of the two single-quantity routes matches on every entry, so the two scores sum to twenty plus the number of ties; the three entries the contract forces into the plan are all ties, which floors the better route at twelve (fact G5). This is proven rather than assumed, and the assertion wall locks the achieved bound. A student guessing that route collects sixty percent.

**One wrong route on `marquee-display-count` cannot be pushed below 2/20** for the mirror-image reason: the contract requires covering k=0, and the route that ignores k is correct exactly there (fact F5).

**The wall-clock multiplier of four is an assumption.** Where a conclusion depends on it, the trace matrix records how far the multiplier would have to move to overturn the conclusion. No disposition in this change flips within a multiplier range of three to five.
