## ADDED Requirements

### Requirement: The trio covers three techniques absent from the existing catalogue

This change SHALL add exactly three challenges with `category: apcs` and `type: competition`, and each SHALL have as its core technique one that no existing challenge in the catalogue uses: two-dimensional difference arrays, sort-then-maintain-state, and a two-pointer sliding window driven by last-seen positions.

The gap this addresses SHALL be stated as a measured fact rather than an impression. Across the seventeen `category: apcs` challenges that exist before this change, the technique distribution is: single-pass simulation in seventeen, sorting in one, two-dimensional arrays in zero, prefix sums or difference arrays in zero, two-pointer or sliding window in zero, and frequency-table counting in zero.

#### Scenario: Each challenge names a distinct core technique

- **WHEN** the three new challenges are examined for their intended solution technique
- **THEN** the three techniques SHALL be pairwise distinct
- **AND** none of them SHALL be the single-pass simulation technique that the seventeen prior challenges use

#### Scenario: The trio does not reuse sorting as more than one core technique

- **WHEN** the core techniques of the three challenges are compared
- **THEN** at most one of them SHALL require sorting the input

### Requirement: Every challenge in the trio has a measured efficiency cliff

Each of the three challenges SHALL be designed so that a brute-force solution scores a partial score, and SHALL NOT score either zero or full marks. The score SHALL be at least 1 of 20 and at most 19 of 20, and the entries it fails SHALL be in the later part of the staircase rather than the earlier part.

Two gates can end a testcase: the per-testcase operation limit of 10,000,000 operations and the 5,000 ms wall-clock deadline. This specification SHALL NOT assert which of the two binds for a given challenge. Which one fires depends on the spelling of the submitted solution and on Pyodide's speed relative to CPython, and both vary between runs; the gate that actually fired SHALL be read from the browser measurement and recorded there.

The measured brute-force score of each challenge SHALL be recorded in this change's measurement record and SHALL be measured in the browser on the production judging path. Locally projected scores SHALL NOT be quoted, because a local harness that applies the deadline to per-entry timings cannot model a worker that dies and discards results already earned.

#### Scenario: Brute force earns partial credit, not zero

- **WHEN** the brute-force solution of any of the three challenges is submitted against its full twenty-entry plan in the browser
- **THEN** its score SHALL be at least 1 of 20 and at most 19 of 20
- **AND** the entries it passes SHALL form a prefix of the plan

### Requirement: The cliff is stated from browser measurement across several spellings

Every statement about what a route scores SHALL come from a browser measurement recorded in this change's measurement record, and SHALL name the spelling that was measured. Operation counts obtained from a local CPython harness SHALL NOT be quoted as scores; they are a proxy that has twice produced conclusions the browser overturned.

For each of the three challenges the record SHALL contain at least four measured submissions: the reference solution; the straightforwardly written brute force; that same brute force with its loop body folded onto one source line; and at least one spelling that pushes the brute force's inner work into a C builtin.

The standard the three challenges SHALL meet is exactly this, and SHALL NOT be raised without re-measuring all three:

1. The reference solution scores 20 of 20.
2. The straightforwardly written brute force scores at least 1 of 20 and at most 19 of 20.
3. A spelling that differs from a killed spelling **only in source formatting** also scores at least 1 of 20 and at most 19 of 20.

Clause 3 is a separate clause because the operation counter counts Python-level trace events, so folding a loop body onto the `while` or `for` line divides the counted operations per iteration without making the code any faster. Such a submission is caught only by the wall-clock deadline. This is a documented property of the platform: `openspec/specs/judge-deadline/spec.md` states that enforcement SHALL NOT depend on the operation counter and names the flattened-loop case explicitly.

Spellings that push the brute force's inner work into a C builtin — `map`, `itertools.compress`, slice assignment, `set` over a slice — SHALL be measured and recorded with their scores, and a full-marks result for such a spelling SHALL NOT block the challenge. Two such spellings do score full marks and are accepted: the rectangle fill written as `map` over a row slice, and the overlap rescan written as `itertools.compress` over a `map` comparison.

They are accepted rather than chased because they cannot be defeated at any scale the 65536-byte input ceiling permits. The ceiling caps the rescan at roughly 26,500,000 compared pairs and the rectangle fill at roughly 22,800,000 cells; measured in the browser these spellings finish in 788 ms and 1,448 ms against a 5,000 ms deadline, so the largest feasible growth leaves them comfortably inside it. Raising the floor grid to buy more work would instead push the reference solution itself toward the deadline, because its cost is the grid area. The same acceptance was already granted to the C-builtin bypass in `gem-blast-challenge`.

The distinction that matters pedagogically is that every spelling a student is likely to write first — the nested loop, the plain `for` scan, the extend-until-repeat loop — earns a partial score, while the surviving spellings require deliberate fluency with `itertools` and `operator`.

#### Scenario: Four spellings per challenge are measured in the browser

- **WHEN** the measurement record for any of the three challenges is read
- **THEN** it SHALL contain browser-measured scores for the reference solution, the straightforward brute force, a formatting-only variant of that brute force, and a C-builtin variant
- **AND** each entry SHALL carry its per-testcase verdicts and per-testcase wall-clock times

#### Scenario: A formatting-only variant does not reach full marks

- **WHEN** a brute-force spelling is changed only by folding its loop body onto the loop header line
- **THEN** its score SHALL remain at least 1 of 20 and at most 19 of 20

##### Example: the formatting-only variants as measured

| Challenge | straightforward brute force | same code, body folded onto the loop line |
| --------- | --------------------------- | ----------------------------------------- |
| `hall-fan-coverage` | 12 of 20 | 15 of 20 |
| `club-room-allocation` | 14 of 20 | 14 of 20 |
| `radio-relay-tape` | 14 of 20 | 15, 16 and 15 of 20 over three runs |

#### Scenario: A surviving C-builtin spelling is recorded, not chased

- **WHEN** a spelling that performs the brute force's inner work in a C builtin scores 20 of 20
- **THEN** its score and slowest per-testcase time SHALL be recorded in the measurement record
- **AND** the challenge SHALL NOT be rescaled or rewritten on account of it

#### Scenario: The reference solution passes every entry

- **WHEN** the `reference_solution` of any of the three challenges is submitted against its full twenty-entry plan in the browser
- **THEN** it SHALL score 20 of 20

### Requirement: All three challenges use column-wise input

The three challenges SHALL express repeated records as one line per field, with the N values of a single field separated by a single space, declared with `count` using `from` to bind the count to a previously declared integer parameter.

A **repeated field** here means a field that occurs once per record, so that its length varies with the record count. A fixed-length header line whose length is the same in every testcase — such as the two integers R and C on the first line of `hall-fan-coverage` — is not a repeated field and SHALL declare a literal `count` instead of `count.from`; `from` cannot express it, because there is no record-count parameter to bind to.

Records SHALL NOT be expressed as one line per record with several differently-ranged values on that line. The testcase engine's `count` produces multiple values on one line only within a single declared value range, and a `group` block places each of its parameters on its own line, so a per-record line carrying differently-ranged values cannot be produced. The engine SHALL NOT be modified to support parameter ranges that reference other parameters.

#### Scenario: Repeated fields are declared with a bound count

- **WHEN** the `params` of any of the three challenges is examined
- **THEN** every field whose length varies with the record count SHALL declare `count` with `from` naming a previously declared single-valued integer parameter
- **AND** SHALL declare `separator` as a single space

#### Scenario: No parameter range references another parameter

- **WHEN** the `params` of any of the three challenges is examined
- **THEN** every `min` and every `max` SHALL be a literal constant

### Requirement: hall-fan-coverage input, output and scale

The challenge `hall-fan-coverage` SHALL read a hall floor divided into R rows by C columns of cells and F ceiling fans, and SHALL output the number of fans covering the single most-covered cell.

The input SHALL be: a first line with the two integers R and C separated by a single space; a second line with the integer F; then four lines, each holding F space-separated integers, giving in order the top row, the left column, the height and the width of each fan's rectangular coverage area.

Each fan's coverage rectangle SHALL be guaranteed to lie entirely inside the floor. This guarantee SHALL be stated in the problem text, and the problem text SHALL NOT define any clipping rule for rectangles that extend past the floor edge.

The declared upper bounds SHALL be R and C at 300, F at 3000, fan height and width each at 150, and fan top row and left column each at 151. These bounds are derived from the 65536-byte per-testcase input ceiling and from the requirement that the **cheapest spelling** of the brute-force route exceed the operation limit; they SHALL NOT be lowered without re-deriving both.

At these bounds the mean rectangle area is approximately 5700 cells, so 3000 fans give approximately 17,100,000 cells. Measured in the browser, the nested-loop fill scores 12 of 20, the same code with its inner loop folded onto one line scores 15 of 20, and the slice-assignment fill scores 15 of 20. The earlier bounds of F at 2000 with height and width at 100 left the slice spelling well inside every gate.

The two spellings cross the limit at different scales, so the middle of the staircase contains entries where the nested spelling fails and the slice spelling passes. This SHALL NOT be treated as a defect. Both spellings SHALL be measured and both scores SHALL be recorded.

#### Scenario: Output is the maximum coverage count

- **WHEN** every cell's coverage count has been determined
- **THEN** the output SHALL be a single line holding the largest of those counts

##### Example: three overlapping fans on a small floor

- **GIVEN** a floor of 4 rows and 5 columns with 3 fans
- **AND** fan tops 1, 2, 1; fan lefts 1, 2, 3; fan heights 2, 2, 3; fan widths 3, 3, 2
- **WHEN** the coverage of every cell is counted
- **THEN** cell row 2 column 3 is covered by all three fans and the output is 3

#### Scenario: Per-row one-dimensional differencing is an accepted full-marks route

- **WHEN** a solution marks two positions per row per fan and accumulates along each row, at a cost of order F times height plus R times C
- **THEN** it SHALL score 20 of 20

#### Scenario: Filling every cell of every rectangle is the killed route

- **WHEN** a solution adds one to every cell inside every fan's rectangle, written as a nested loop, as that loop folded onto one line, or as a slice assignment
- **THEN** it SHALL score a partial score

##### Example: the three killed fill spellings as measured

| Spelling | Score | Slowest testcase |
| -------- | ----- | ---------------- |
| nested loop | 12 of 20 | 2,074 ms |
| nested loop folded onto one line | 15 of 20 | 2,951 ms |
| slice assignment with a list comprehension | 15 of 20 | 2,283 ms |

#### Scenario: The same fill written with map over a row slice survives

- **WHEN** the fill is written as `map` with `operator.add` over a row slice
- **THEN** it SHALL score 20 of 20 with a slowest testcase of approximately 1,448 ms
- **AND** this SHALL be recorded rather than treated as a defect, because the 65536-byte input ceiling caps the work at approximately 22,800,000 cells and cannot push this spelling past the 5,000 ms deadline

### Requirement: hall-fan-coverage testcase entries keep rectangles inside the floor

Every entry of the `testcase_plan` of `hall-fan-coverage` SHALL satisfy both of the following, where the names refer to that entry's effective bounds after any `override` is applied: the maximum fan top row plus the maximum fan height minus one SHALL NOT exceed R, and the maximum fan left column plus the maximum fan width minus one SHALL NOT exceed C.

This condition SHALL be verified entry by entry and the per-entry values SHALL be recorded in this change's measurement record. Verification is required because no existing gate detects its violation: a violating entry produces out-of-bounds rectangles silently, and because `generator` and `reference_solution` both read the same input, they agree with each other and `content-regression` stays green.

#### Scenario: Every entry satisfies the in-bounds condition

- **WHEN** the twenty entries of the plan are each evaluated for their effective bounds
- **THEN** each entry SHALL satisfy both inequalities
- **AND** the twenty per-entry evaluations SHALL appear in the measurement record

#### Scenario: A violating entry is not caught by existing gates

- **WHEN** an entry violates the in-bounds condition
- **THEN** `content-regression` SHALL still report agreement between `generator` and `reference_solution`
- **AND** the violation SHALL therefore be detected only by the entry-by-entry verification required above

### Requirement: club-room-allocation input, output and allocation rule

The challenge `club-room-allocation` SHALL read N room-booking applications and SHALL output both the minimum number of rooms that must be opened and the room number allocated to each application.

The input SHALL be: a first line with the integer N; a second line with N space-separated integers giving each application's start minute; a third line with N space-separated integers giving each application's duration in minutes. Application i occupies the half-open interval from its start minute to its start minute plus its duration.

The allocation rule SHALL be: applications are processed in order of increasing start minute, and applications sharing a start minute are processed in order of increasing application number; each application is given the lowest-numbered room that is free at its start minute, and a new room is opened when every open room is occupied. Because the lowest free number is always taken, the set of open room numbers is always the consecutive range from one to the current count, and a newly opened room therefore takes the number one greater than that count.

The output SHALL be: a first line with the minimum number of rooms; a second line with N space-separated integers, where the i-th is the room allocated to the i-th application **in input order**, not in processing order.

This allocation rule exists to make the output unique. The source problem admits many valid allocations and is judged by a special judge; this site compares output verbatim against the generator's expected output and has no special judge, so an unconstrained allocation would judge correct solutions wrong.

#### Scenario: Output reports allocations in input order

- **WHEN** the applications are processed in start-minute order and each is allocated a room
- **THEN** the second output line SHALL list the allocations indexed by input position, not by processing position

##### Example: a freed room is reused by its number

| Application | Start | Duration | Occupies | Room |
| ----------- | ----- | -------- | -------- | ---- |
| 1 | 10 | 30 | 10 to 40 | 1 |
| 2 | 20 | 30 | 20 to 50 | 2 |
| 3 | 40 | 10 | 40 to 50 | 1 |
| 4 | 45 | 10 | 45 to 55 | 3 |

- **GIVEN** the four applications above
- **WHEN** they are processed in start-minute order
- **THEN** the minimum room count is 3 and the second output line is `1 2 1 3`

#### Scenario: Simultaneous starts break ties by application number

- **WHEN** two applications share the same start minute and both need a room
- **THEN** the one with the smaller application number SHALL receive the lower room number

### Requirement: club-room-allocation is not gated on a priority queue

The efficiency cliff of `club-room-allocation` SHALL separate a route that rescans all earlier applications from a route that maintains per-room state, and SHALL NOT separate a route that scans the open rooms from a route that uses a priority queue.

The reason SHALL be recorded so that later maintenance does not enlarge the scale in order to force a priority queue. The minimum room count is the maximum concurrent occupancy. Making the scan-the-open-rooms route exceed the operation limit at the N permitted by the 65536-byte input ceiling would require several hundred rooms in simultaneous use, which no school-room-booking scenario supports.

The declared upper bounds SHALL be N at 6000, start minute in the range one to 9000, and duration in the range thirty to one hundred and five minutes, over a one-week time axis of 10080 minutes.

N is 6000 rather than 4000 because the cheapest spelling of the killed route governs. A set comprehension over the earlier applications costs approximately one counted operation per compared pair, against approximately two for the expanded loop, so the cheapest spelling crosses the operation limit only above N of approximately 4472.

The maximum concurrent occupancy at these bounds SHALL be stated from measurement, never from the expected value. The expected concurrent occupancy is N times the mean duration divided by the length of the time axis, but the answer is the **maximum**, which runs materially higher: at the earlier bounds of N at 4000 and duration up to 240 minutes, the expected value was approximately 60 while four independent measurements gave 82, 85, 87 and 89. The duration ceiling is 105 minutes rather than 240 so that the measured maximum stays in the tens of rooms, which is the range a senior high school can actually offer. At the declared bounds the measured maximum on the largest plan entry is 64 rooms on the block the record's headline table uses, and 64 to 72 across all ten blocks of the shipped pool.

#### Scenario: Rescanning all earlier applications is the killed route

- **WHEN** a solution determines each application's room by scanning all earlier applications and testing each for time overlap, at a cost of order N squared
- **THEN** it SHALL score a partial score, both when the scan is written as an expanded loop and when it is written as a set comprehension

#### Scenario: Scanning the open rooms is an accepted full-marks route

- **WHEN** a solution sorts the applications and then, for each, scans the open rooms for the lowest-numbered one whose last end time has passed
- **THEN** it SHALL score 20 of 20

#### Scenario: A priority queue is an accepted full-marks route

- **WHEN** a solution sorts the applications and maintains room availability in a priority queue
- **THEN** it SHALL score 20 of 20

### Requirement: radio-relay-tape asks for the longest repeat-free run

The challenge `radio-relay-tape` SHALL read a request sequence of N song numbers and SHALL output the length of the longest contiguous run whose songs are pairwise distinct.

The input SHALL be: a first line with the integer N; a second line with N space-separated integers giving the song numbers in request order. There SHALL NOT be a window-length parameter.

This challenge SHALL NOT ask how many fixed-length segments are repeat-free. That question cannot carry an efficiency cliff on this platform at any scale the 65536-byte input ceiling permits, and the reason is structural rather than a matter of tuning: the killed route's cheapest spelling is one `len(set(slice))` call per window, whose cost the operation counter records as a constant independent of the window length. It was measured at 17,392 operations for N of 7000 and window length 1000, which is 578 times under the limit, with a wall-clock of 0.062 seconds in CPython. The largest N times window length the input ceiling permits is approximately 24,500,000 element operations, roughly 1.2 seconds, which is under half the wall-clock deadline.

The longest-run question is immune to that spelling because its inner loop terminates on a data-dependent condition — extend until the arriving song has already been seen — which cannot be expressed as a single C builtin call on a fixed slice. Any spelling using `set` must still drive the extension from Python.

The song-number value domain SHALL be the range one to 4000000 and SHALL NOT be narrowed. In a random sequence over a domain of size S, the expected extension from any start is approximately the square root of twice S, so the domain is what sets the killed route's cost at N times roughly 2828. A small alphabet caps every run at the number of distinct symbols and collapses the killed route to linear.

The domain SHALL NOT be lowered to 1000000. At that domain the expected extension is roughly 1414, and the killed route's formatting-only variant — the same loop with its body folded onto the `while` line — was measured at 20 of 20, 19 of 20 and 20 of 20 over three browser runs, its slowest testcase landing between 4,249 ms and 4,519 ms against the 5,000 ms deadline. Raising the domain to 4000000 costs no input bytes, because both bounds are seven characters wide, and it moves that variant to 15, 16 and 15 of 20 over three runs.

The declared upper bound SHALL be N at 7000.

#### Scenario: Output is the longest repeat-free run length

- **WHEN** every contiguous run of the sequence is considered
- **THEN** the output SHALL be a single line holding the length of the longest run whose songs are pairwise distinct

##### Example: a short request sequence

- **GIVEN** N is 7 and the sequence is 4, 9, 4, 7, 1, 9, 1
- **WHEN** the longest repeat-free run is sought
- **THEN** the run 4, 7, 1, 9 starting at position 3 has length 4, no longer run exists, and the output is 4

#### Scenario: Extending from every start is the killed route

- **WHEN** a solution takes each start position and extends rightward until it meets a song already seen since that start, at a cost of order N times the mean run length
- **THEN** it SHALL score a partial score

#### Scenario: Two pointers with last-seen positions is the accepted route

- **WHEN** a solution advances a right pointer across the sequence and moves the left pointer to one past the previous occurrence whenever the arriving song was already inside the window
- **THEN** it SHALL score 20 of 20

#### Scenario: Binary search on run length also earns only a partial score

- **WHEN** a solution binary-searches the run length at each start position, testing a candidate length by comparing the size of the set of that slice against the length
- **THEN** it SHALL score a partial score, measured at 16 of 20 with a slowest testcase of approximately 5,005 ms
- **AND** the specification SHALL NOT describe it as a full-marks route, which is what it was at the earlier value domain of 1000000

### Requirement: Each challenge uses a twenty-entry staircase plan whose first entry is the worked example

Each of the three challenges SHALL declare a `testcase_plan` of exactly twenty entries. The first entry SHALL be a `literal` whose content is byte-for-byte identical to the input shown in the challenge text's worked example. The remaining nineteen entries SHALL use `count` with `override` and SHALL increase in scale monotonically, so that a brute-force route fails part-way through the plan rather than on its first large entry.

#### Scenario: The first entry matches the worked example

- **WHEN** the first entry's `literal` is compared with the input block of the challenge text's example section
- **THEN** the two SHALL be byte-for-byte identical

#### Scenario: Scale increases monotonically across the plan

- **WHEN** the effective scale parameter of entries two through twenty is read in plan order
- **THEN** each SHALL be greater than or equal to the previous one

### Requirement: Each challenge declares a reference solution written differently from its generator

Each of the three challenges SHALL declare `reference_solution`, and that solution SHALL take a different implementation route from the same challenge's `generator`. Two programs expressing the same logic SHALL NOT be used, because `content-regression` then verifies only that a program agrees with a paraphrase of itself.

The verification SHALL be recorded as having executed rather than skipped. `content-regression` skips silently when python3 is absent, so a green local run is not by itself evidence that the check ran.

#### Scenario: The two implementations take different routes

- **WHEN** a challenge's `generator` and `reference_solution` are compared
- **THEN** they SHALL differ in algorithmic route, not only in variable naming or statement order

#### Scenario: The regression check is recorded as executed

- **WHEN** `content-regression` is run for this change
- **THEN** the record SHALL show the three challenges as executed and SHALL NOT show them as skipped

### Requirement: Each challenge ships one explanatory figure built by the existing plate pipeline

Each of the three challenges SHALL ship one figure at `docs/public/assets/challenge/<id>/圖一.png`, produced by a plate script pair under `scripts/figures/` following the pipeline established for `apcs013` and `apcs014`: a Python script that emits HTML, and a shell script that converts that HTML to PNG through headless Chrome.

Each figure SHALL be authored on a 1280-pixel-wide portrait canvas and SHALL set no glyph below 24 authored pixels. The challenge page renders the problem text in a fixed left pane measured at 643 CSS pixels, so a 1280-pixel canvas displays at approximately half scale and a 24-pixel glyph lands at approximately 12 pixels on screen. These two values SHALL be treated as the binding constraint and SHALL NOT be relaxed on aesthetic grounds.

The fonts the plate scripts embed live under a Git LFS path, so rebuilding a figure requires pulling LFS objects first. Neither CI nor the site build reads those fonts.

#### Scenario: Figure canvas and minimum type size

- **WHEN** a plate script for any of the three challenges is examined
- **THEN** its canvas width SHALL be 1280 pixels
- **AND** no glyph size in it SHALL be below 24 pixels

#### Scenario: Figure is readable at the rendered column width

- **WHEN** a challenge page carrying one of the three figures is measured in a browser
- **THEN** the figure's rendered width SHALL fit the problem-text column without horizontal overflow
- **AND** the smallest glyph SHALL render at no less than 12 screen pixels

### Requirement: Traceability matrix for the trio

The following matrix SHALL be the single source of truth for which challenge carries which technique, which route is killed, and which requirement governs it. Prose elsewhere in this specification SHALL be consistent with this matrix, and any change to a challenge's technique, killed route or scale SHALL update this matrix in the same change.

| Challenge | Core technique | Killed route | Accepted routes | Scale bound source |
| --------- | -------------- | ------------ | --------------- | ------------------ |
| `hall-fan-coverage` | two-dimensional difference array | fill every cell of every rectangle, as a nested loop, as that loop folded, or as a slice assignment | two-dimensional differencing; per-row one-dimensional differencing; the fill written with `map` (accepted, recorded) | 65536-byte input ceiling and the two judging gates |
| `club-room-allocation` | sort then maintain per-room state | rescan all earlier applications for overlap, as a loop, as that loop folded, or as a set comprehension | scan the open rooms; priority queue; the rescan written with `itertools.compress` (accepted, recorded) | 65536-byte input ceiling and realistic concurrent-room count |
| `radio-relay-tape` | two-pointer sliding window with last-seen positions | extend from every start until a repeat, including the formatting-only fold and the binary-search variant | two pointers with last-seen positions | 65536-byte input ceiling and the mean run length set by the value domain of 4000000 |

#### Scenario: Matrix and prose agree

- **WHEN** each row of the matrix is compared with the corresponding per-challenge requirement above
- **THEN** the technique, the killed route and the accepted routes SHALL agree in both places

#### Scenario: Matrix is updated alongside any behavioural change

- **WHEN** a challenge's technique, killed route or scale bound is changed
- **THEN** the matrix row for that challenge SHALL be updated in the same change
