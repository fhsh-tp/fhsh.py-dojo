## ADDED Requirements

### Requirement: Repository provides committed challenge-authoring skill

The repository SHALL provide a committed skill at `.claude/skills/challenge-author/SKILL.md` with valid YAML frontmatter containing at least `name` and `description`. The skill body SHALL guide an agent through authoring a new challenge: the kebab-case naming rule, the `pnpm new-challenge` scaffold invocation including the `--type` flag, the challenge frontmatter fields including the optional `reference_solution` field, generator authoring guidance, the requirement to keep the Rust and Python generators in sync, the `content-regression` verification step, and the template differences between the `basic` and `competition` exercise types.

#### Scenario: challenge-author skill exists with valid frontmatter

- **WHEN** a tool reads `.claude/skills/challenge-author/SKILL.md`
- **THEN** the file SHALL exist
- **AND** its YAML frontmatter SHALL parse and contain `name` and `description`

#### Scenario: challenge-author skill covers the authoring contract

- **WHEN** an agent follows the challenge-author skill to create a challenge
- **THEN** the skill SHALL direct it to use `pnpm new-challenge` with `--type`
- **AND** it SHALL describe the `reference_solution` field and the `content-regression` verification

### Requirement: Repository provides committed Phoenix science-writing skill

The repository SHALL provide a committed skill at `.claude/skills/phoenix-sci-writing/SKILL.md` with valid YAML frontmatter containing at least `name` and `description`. The skill body SHALL enumerate the fifteen editorial rules by identifier (P-1, T-1, S-1, S-2, S-3, C-1, E-1, M-1, O-1, W-1, T-2, F-1, V-1, T-3, K-1) with the checkable intent of each, and SHALL point to the canonical source document `phoenix-popular-science-article-style-enhance.md` for full detail.

#### Scenario: phoenix-sci-writing skill exists with valid frontmatter

- **WHEN** a tool reads `.claude/skills/phoenix-sci-writing/SKILL.md`
- **THEN** the file SHALL exist
- **AND** its YAML frontmatter SHALL parse and contain `name` and `description`

#### Scenario: phoenix-sci-writing skill enumerates the fifteen rules

- **WHEN** an agent reads the phoenix-sci-writing skill
- **THEN** it SHALL find all fifteen rule identifiers (P-1 through K-1)
- **AND** it SHALL find a pointer to `phoenix-popular-science-article-style-enhance.md`

### Requirement: Repository provides committed editorial-audit-loop skill

The repository SHALL provide a committed skill at `.claude/skills/eal-editorial-audit/SKILL.md` with valid YAML frontmatter containing at least `name` and `description`. The skill body SHALL describe the Editorial Audit Loop: the fixed per-round rule scan order, applying fixes between rounds, termination after zero violations or a maximum of three rounds, and the violation-log concept. It SHALL point to the `editorial-audit-loop` specification as the normative source.

#### Scenario: eal-editorial-audit skill exists with valid frontmatter

- **WHEN** a tool reads `.claude/skills/eal-editorial-audit/SKILL.md`
- **THEN** the file SHALL exist
- **AND** its YAML frontmatter SHALL parse and contain `name` and `description`

#### Scenario: eal-editorial-audit skill describes the loop termination rule

- **WHEN** an agent runs the Editorial Audit Loop via the skill
- **THEN** the skill SHALL state that the loop terminates after zero violations or a maximum of three rounds
- **AND** it SHALL reference the `editorial-audit-loop` specification
