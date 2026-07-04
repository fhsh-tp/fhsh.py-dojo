# agent-onboarding-docs Specification

## Purpose

TBD - created by archiving change 'improve-agent-onboarding'. Update Purpose after archive.

## Requirements

### Requirement: Agent instruction files carry project domain content outside managed blocks

Each of `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` SHALL contain a project domain section placed AFTER the Spectra managed block delimiter `<!-- SPECTRA:END -->`. The domain content SHALL NOT be placed inside the managed block, because the managed block is overwritten on Spectra template upgrades. The domain section SHALL cover the technology stack, the build command reference, the challenge frontmatter contract summary, and the maintenance reading list. Each file SHALL reference Spectra skills using that file's own established invocation syntax.

#### Scenario: Domain section survives outside the managed block

- **WHEN** a maintainer reads any of the three instruction files
- **THEN** a project domain section SHALL appear after the `<!-- SPECTRA:END -->` marker
- **AND** the managed block content between `<!-- SPECTRA:START -->` and `<!-- SPECTRA:END -->` SHALL remain unmodified

#### Scenario: Technology stack and build commands are documented

- **WHEN** an agent reads the domain section
- **THEN** it SHALL find the technology stack (VitePress, Vue, Pyodide, Rust/WASM testcase-generator, pnpm)
- **AND** it SHALL find a build command reference listing the purpose of `pnpm dev`, `build:pools`, `build:wasm`, `build:pyodide`, `gen:keymaterial`, `typecheck`, `lint`, and `test`

#### Scenario: Challenge contract and reading list are documented

- **WHEN** an agent prepares to add or maintain a challenge
- **THEN** the domain section SHALL summarize the challenge frontmatter contract including the optional `reference_solution` field
- **AND** the domain section SHALL list `CONTRIBUTE.md`, `README.md`, and `Usage.md` as required reading

#### Scenario: File-specific invocation syntax is preserved

- **WHEN** the domain section references a Spectra skill in `AGENTS.md`
- **THEN** it SHALL use that file's Codex-style invocation syntax rather than the Claude slash syntax

---
### Requirement: Fork-legacy documentation is consistent

The repository documentation SHALL present a single consistent onboarding story. The `CONTRIBUTE.md` file SHALL state the Node.js major version as 22 or newer, matching the README badge. The `CONTRIBUTE.md` phase headings SHALL be numbered consecutively without gaps. The new-challenge standard operating procedure in `Usage.md` SHALL present `pnpm new-challenge` as the primary path and SHALL agree with `CONTRIBUTE.md`. The `CHANGELOG.md` file SHALL contain an `## [Unreleased]` section recording notable changes made after the 1.0.0 release. The default challenge title fallback in the challenge data loader SHALL be a neutral label that does not reference cryptography.

#### Scenario: Node version agreement

- **WHEN** a maintainer compares the Node version in `CONTRIBUTE.md` and the README badge
- **THEN** both SHALL state 22 or newer

#### Scenario: Consecutive phase numbering

- **WHEN** a maintainer reads the phase headings in `CONTRIBUTE.md`
- **THEN** the phase numbers SHALL form a consecutive sequence with no missing number

#### Scenario: New-challenge SOP agreement

- **WHEN** a maintainer follows the new-challenge instructions in `Usage.md`
- **THEN** the primary instruction SHALL be `pnpm new-challenge`
- **AND** it SHALL NOT contradict the SOP in `CONTRIBUTE.md`

#### Scenario: Changelog records post-1.0.0 changes

- **WHEN** a maintainer reads `CHANGELOG.md`
- **THEN** an `## [Unreleased]` section SHALL record notable changes made after 1.0.0

#### Scenario: Neutral default challenge title

- **WHEN** a challenge without an explicit title is loaded
- **THEN** the fallback title SHALL be a neutral label that does not contain the word for cryptography
