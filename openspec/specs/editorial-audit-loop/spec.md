# editorial-audit-loop Specification

## Purpose

Defines an iterative Editorial Audit Loop (EAL) workflow for verifying Chapter 1 tutorial content against the full set of editorial rules. The workflow ensures systematic, repeatable quality checks that catch violations missed by single-pass reviews.

## Requirements

### Requirement: Editorial Audit Loop workflow exists for Chapter 1 content

The project SHALL define an Editorial Audit Loop (EAL) workflow that iteratively verifies all Chapter 1 tutorial content (`docs/tutor/py/ch1/1-1.md` through `1-4.md` and `appendix.md`) against the full set of editorial rules defined in the `python-ch1-content` spec. The workflow SHALL be documented as a reusable process, not a one-time ad hoc check.

#### Scenario: EAL workflow is documented

- **WHEN** a contributor needs to verify Chapter 1 content quality
- **THEN** a documented EAL workflow SHALL exist that specifies the exact sequence of checks, the scan order, the recording format for violations, and the termination conditions

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
-->


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: EAL workflow scans all rules in a defined order per round

Each round of the EAL workflow SHALL scan all target files against every editorial rule in a fixed order. The scan order SHALL be: P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, F-1, V-1, T-3, K-1, O-1, W-1, T-2. For each rule, every target file SHALL be scanned. The scan SHALL produce a violation log entry for each finding, including: file path, line number, rule ID, violation description, and suggested fix.

#### Scenario: Single round scans all rules across all files

- **WHEN** one round of the EAL workflow is executed
- **THEN** every rule from P-1 through T-2 SHALL be checked against every target file, and all violations SHALL be recorded in the violation log

#### Scenario: Violation log entry contains required fields

- **WHEN** a violation is detected during a scan
- **THEN** the log entry SHALL include: file path, line number (or line range), rule ID, a description of the violation, and a specific suggested fix (not a generic instruction)

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
-->


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: EAL workflow terminates after zero violations or maximum 3 rounds

The EAL workflow SHALL terminate when either: (a) a completed round produces zero violations across all files and all rules, or (b) three rounds have been completed, whichever comes first. After termination, the workflow SHALL produce a summary report listing: number of rounds executed, total violations found per round, and any remaining violations after the final round.

#### Scenario: Early termination on clean round

- **WHEN** a round of the EAL workflow produces zero violations
- **THEN** the workflow SHALL terminate immediately without starting another round, and the summary report SHALL indicate a clean pass

#### Scenario: Termination at maximum rounds

- **WHEN** three rounds have been completed and violations still remain
- **THEN** the workflow SHALL terminate, and the summary report SHALL list all remaining violations from the third round with their rule IDs, file paths, and line numbers

#### Scenario: Summary report is produced

- **WHEN** the EAL workflow terminates (by either condition)
- **THEN** a summary report SHALL be produced containing: the number of rounds executed, a per-round violation count, and (if applicable) a detailed list of remaining violations

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
-->


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: EAL workflow applies fixes between rounds

Between each round of the EAL workflow, all violations detected in the current round SHALL be fixed before the next round begins. Fixes SHALL be applied directly to the target files. The next round SHALL then re-scan all files from scratch (not just re-check previously violated lines), because fixing one violation can introduce new violations or resolve cascade issues.

#### Scenario: Fixes applied before next round

- **WHEN** a round of the EAL workflow detects N violations (N > 0) and the maximum round count has not been reached
- **THEN** all N violations SHALL be fixed in the target files before the next round begins

#### Scenario: Next round re-scans from scratch

- **WHEN** a new round begins after fixes have been applied
- **THEN** the scan SHALL cover all files and all rules from the beginning, not just the previously violated locations

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
-->


<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->

---
### Requirement: EAL workflow is reusable across chapters

The EAL workflow definition SHALL be parameterizable by target directory, so that it can be applied to future chapters (e.g., `docs/tutor/py/ch2/`) without modification to the workflow logic. The rule set to scan SHALL be configurable, defaulting to the full set but allowing a subset for focused audits.

#### Scenario: Workflow applied to a different chapter

- **WHEN** the EAL workflow is invoked with target directory `docs/tutor/py/ch2/`
- **THEN** the workflow SHALL scan all `.md` files in that directory against the configured rule set, using the same scan order, logging format, and termination conditions as for Chapter 1

#### Scenario: Subset rule audit

- **WHEN** the EAL workflow is invoked with a rule subset (e.g., only P-1 and C-1)
- **THEN** only the specified rules SHALL be scanned, and the termination and reporting conditions SHALL apply to that subset

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
-->

<!-- @trace
source: ch1-editorial-rules-enhancement
updated: 2026-04-09
code:
  - docs/public/assets/tutor/py/1-1/圖二.png
  - docs/public/assets/tutor/py/ch1/圖五.png
  - docs/tutor/py/ch1/1-2.md
  - docs/public/assets/tutor/py/1-1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖三.png
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/tutor/py/ch1/appendix.md
  - docs/public/assets/tutor/py/ch1/圖八.png
  - docs/public/assets/tutor/py/ch1/圖二.png
  - docs/public/assets/tutor/py/1-1/圖三.png
  - docs/public/assets/tutor/py/ch1/圖六.png
  - docs/public/assets/tutor/py/ch1/圖四.png
  - docs/public/assets/tutor/py/ch1/圖一.png
  - docs/public/assets/tutor/py/ch1/圖七.png
  - docs/public/assets/tutor/py/1-1/圖四.png
  - docs/tutor/py/ch1/1-1.md
-->