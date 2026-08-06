## MODIFIED Requirements

### Requirement: Shared authoring constraints for the bracket duo
Both challenge pages SHALL use their life scenarios (1a theater prop-box packing log; 1b school-magazine typesetting checker) without any data-structure terminology (no stack/堆疊/樹 or algorithm-name keywords) (trace C1, batch requirement). Both challenges SHALL be `category: apcs`, `type: competition`, `difficulty: medium` (trace C2), and SHALL declare a `reference_solution` implemented independently from the `generator` (different data layout), verified by the content-regression suite (trace C9). Both starter_code fields SHALL be the empty string, so the editor loads blank and an unmodified submission emits no output and scores 0/20 (maintainer decision 2026-08-06, superseding the original read-input skeleton). The 1b challenge page's performance reminder SHALL be limited to the measured-true claim about per-character backward rescanning loops and SHALL NOT promise any route impossible (trace B10). Challenge ids SHALL be assigned by the `pnpm new-challenge` scaffold, never hand-written (trace C1).

#### Scenario: Content regression passes for both challenges
- **GIVEN** both challenges declare generator and reference_solution
- **WHEN** `scripts/content-regression.test.ts` runs against the built production pools
- **THEN** both reference solutions' outputs match the generators' expected outputs on all sampled entries

#### Scenario: Unmodified starter submission scores zero
- **GIVEN** a student opens either challenge and submits the editor content unchanged
- **WHEN** the empty program runs against the full 20-entry block
- **THEN** every testcase verdict is WA (no output produced) and the score is 0/20
