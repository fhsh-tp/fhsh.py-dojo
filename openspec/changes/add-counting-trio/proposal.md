## Why

The APCS literacy series (`apcs001`–`apcs014`) has no `easy` entry. Every existing challenge is `medium` or `hard`, so a student finishing the `py` basics series (`py054`) faces a difficulty cliff with nothing in between. Three counting problems adapted from a public problem set fill that gap while extending the series into a topic it does not yet cover: closed-form counting and factor counting, both of which sit inside the senior-high mathematics curriculum.

The three source problems cannot be translated literally. Their original discrimination rests on C++ integer overflow and on time limits calibrated for compiled languages; in Python the overflow trap does not exist and one of the three collapses into a single-line answer. Each therefore needs a re-derived discrimination axis, and the three axes are deliberately different so the trio does not test the same skill three times.

## What Changes

Three new `category: apcs`, `type: competition` challenges are added, each with a life-context narrative that never names the underlying mathematics:

- `ap-layout-plan` (`easy`): given a square site of side `k` tiled into `k × k` cells, count placements of two access points that do not interfere, for every side length from 1 to `n`, one result per line. Interference is defined in the page as an explicit table of eight relative offsets. Discrimination is by cost: scanning every cell pair per side length is infeasible, while the closed form and an incremental route both pass.
- `marquee-display-count` (`easy`): a display board of `n` cells, each lit or dark, of which `k` named cells are permanently dark; count the distinct pictures, modulo 1000000007. Discrimination is by context translation — the free positions are `n - k`, not `n`. No cost cliff is built.
- `fair-token-exchange` (`medium`): the number of orderings of `n` people is the small-token count; twelve small tokens exchange for one of the next rank only when they exactly fill a batch; report the highest rank reachable. Discrimination is by context translation — twelve is two squared times three, so the widely published base-ten rule produces a wrong answer here.

Each challenge declares a 20-entry all-literal `testcase_plan` whose first entry is byte-identical to the page's worked example, a `reference_solution` implemented independently of its `generator`, and an empty `starter_code`. All literal content is produced by an assertion wall under the change's curation directory, never hand-edited, so every number in the specification can be regenerated.

## Non-Goals

- No change to the operation counter, the per-testcase deadline, or any existing challenge. The trio is authored against the engine as it stands after the deadline work.
- No attempt to close the residue that all-literal test inputs reach the client bundle and are public in the repository. That residue is project-level, shared with every earlier all-literal challenge, and is tracked separately.
- No general base parameter for the token exchange challenge. The base is fixed at twelve; reading the base from input was considered and rejected as beyond the declared difficulty.
- No teaching article. The trio ships as challenge pages only.

## Capabilities

### New Capabilities

- `counting-trio-challenges`: the I/O contracts, testcase plans, cost ladders and authoring constraints of the three counting challenges.

### Modified Capabilities

(none)

## Impact

- Affected specs: `counting-trio-challenges` (new)
- Affected code:
  - New: docs/challenge/ap-layout-plan.md
  - New: docs/challenge/marquee-display-count.md
  - New: docs/challenge/fair-token-exchange.md
  - New: openspec/changes/add-counting-trio/curation/semantics015.py
  - New: openspec/changes/add-counting-trio/curation/semantics016.py
  - New: openspec/changes/add-counting-trio/curation/semantics017.py
  - New: openspec/changes/add-counting-trio/curation/plan015.py
  - New: openspec/changes/add-counting-trio/curation/plan016.py
  - New: openspec/changes/add-counting-trio/curation/plan017.py
  - New: openspec/changes/add-counting-trio/curation/assemble.py
  - New: openspec/changes/add-counting-trio/curation/routes/
  - New: openspec/changes/add-counting-trio/measure/browser-verification.jsonl
  - New: openspec/changes/add-counting-trio/trace-matrix.md
  - Modified: (none)
  - Removed: (none)
