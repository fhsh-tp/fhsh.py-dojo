## ADDED Requirements

### Requirement: Mathematical expressions in section 1-3 use LaTeX syntax

Section `1-3.md` SHALL use LaTeX inline math syntax (`$...$`) for all mathematical expressions, including but not limited to quadratic equation notation (`$ax^2 + bx + c = 0$`), discriminant formula (`$D = b^2 - 4ac$`), and squared terms (`$b^2$`). Unicode superscript characters (e.g., `²`) SHALL NOT be used for mathematical notation.

#### Scenario: Quadratic equation formula renders as LaTeX

- **WHEN** a reader views section 1-3 in the browser
- **AND** the section discusses the quadratic equation
- **THEN** the formula SHALL be rendered as formatted LaTeX math (`$ax^2 + bx + c = 0$`) rather than plain Unicode text (`ax² + bx + c = 0`)

#### Scenario: Discriminant formula renders as LaTeX

- **WHEN** a reader views section 1-3 in the browser
- **AND** the section discusses the discriminant
- **THEN** the formula SHALL be rendered as formatted LaTeX math (`$D = b^2 - 4ac$`) rather than plain Unicode text (`D = b² − 4ac`)
