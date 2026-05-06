## MODIFIED Requirements

### Requirement: APCS beginner transition format template

All practice problems in sections 1-3, 1-4, 2-1, 2-2, 2-3, and 2-4 — including both existing exercises and any exercises added in future changes — SHALL follow the APCS literacy exercise format defined in the `apcs-literacy-exercise-template` spec. "Practice problems" excludes Judge 解題實戰 teaching worked-examples (see `apcs-literacy-exercise-template` spec for the exclusion list).

This replaces the previous "APCS beginner transition format" template. The key differences from the previous format are:

1. **問題情境** replaces **題目說明**: The narrative SHALL be 150-300 Chinese characters (up from 2-3 sentences) and SHALL use a named character in a real-world scenario
2. **🔍 思考引導** is a new mandatory section: Each exercise SHALL include at least 1 scaffold element (Math Expression, Partial Flowchart, or Step Decomposition) as defined in the `apcs-literacy-exercise-template` spec
3. **範例說明** is a new mandatory section: Each exercise SHALL include a step-by-step computation trace of the most instructive example
4. The scope expands from "sections 2-1, 2-2, and 2-3" to "sections 1-3, 1-4, 2-1, 2-2, 2-3, and 2-4"

All other requirements from the `apcs-literacy-exercise-template` spec (input format, output format, sample I/O pairs, teacher hints) SHALL apply.

#### Scenario: Practice problem follows APCS literacy format

- **WHEN** a practice problem in sections 1-3, 1-4, 2-1, 2-2, 2-3, or 2-4 is parsed
- **THEN** it SHALL contain all mandatory sections defined in the `apcs-literacy-exercise-template` spec: 問題情境 (150-300 chars with named character), 思考引導 (with at least 1 scaffold), 輸入格式 (with constraints), 輸出格式, at least 2 sample I/O pairs, 範例說明 (with numbered steps), and 老師的提示

#### Scenario: Existing short-format exercises are upgraded

- **WHEN** an exercise that previously used the short format (1-2 sentence description + hint + ChallengeLink) is found in sections 2-1, 2-2, or 2-3
- **THEN** it SHALL be rewritten to the full APCS literacy format with all mandatory sections

#### Scenario: Section 1-3 tier format is replaced

- **WHEN** section 1-3's exercises are examined after the change
- **THEN** the tier system (★☆☆ through ★★★★) SHALL be removed and all exercises SHALL use the APCS literacy format instead
