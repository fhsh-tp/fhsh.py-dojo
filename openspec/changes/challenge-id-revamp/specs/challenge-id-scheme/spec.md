## ADDED Requirements

### Requirement: Challenge id is a category-prefixed zero-padded string

Every challenge frontmatter `id` SHALL be a string matching `^(py|apcs)\d{3}$`: a category prefix followed by a 3-digit zero-padded ordinal. The prefix SHALL map one-to-one to the challenge's resolved category (`python` maps to `py`, `apcs` maps to `apcs`). The ordinal of an id SHALL be defined as the decimal integer obtained by stripping all leading non-digit characters. Ids SHALL be unique across the whole site; uniqueness within a prefix combined with distinct prefixes guarantees this.

#### Scenario: Valid ids

- **WHEN** the challenge content gate scans all files under docs/challenge/
- **THEN** every frontmatter id SHALL match the pattern, and no two files SHALL share the same id

##### Example: Format mapping

| category | ordinal | id |
| --- | --- | --- |
| python | 1 | py001 |
| python | 54 | py054 |
| apcs | 3 | apcs003 |

#### Scenario: Per-category ordinals are contiguous from 1

- **WHEN** all ids sharing a prefix are collected and their ordinals sorted
- **THEN** the ordinals SHALL form a contiguous integer sequence starting at 1

### Requirement: Catalogue ordering derives from id string comparison

The challenge data layer and every view that orders challenges by id SHALL compare id values with plain code-unit lexicographic string comparison (not locale-aware collation, whose result varies by runtime ICU build). Within a single category prefix this ordering SHALL equal ordinal ordering (guaranteed by zero-padding). Ordering across different prefixes in a mixed list is lexicographic (all `apcs` ids sort before all `py` ids) and SHALL carry no user-facing meaning: every user-facing list SHALL be filtered to a single category before ordering is presented.

#### Scenario: Same-prefix ordering equals ordinal ordering

- **WHEN** a category page sorts its challenges by id ascending
- **THEN** py002 SHALL appear before py010, and py010 before py054

#### Scenario: Latest-challenges lists remain ordinal-ordered

- **WHEN** the homepage builds its per-category latest-challenges lists by sorting ids descending and taking the first three
- **THEN** each list SHALL contain the three highest ordinals of that category, in descending ordinal order

### Requirement: Renumbering never touches slugs or student data keys

The id migration SHALL NOT rename or move any challenge markdown file. Slugs (file basenames), IndexedDB progress records, session records, downloaded record files, and testcase pool identities SHALL remain byte-for-byte unaffected by id renumbering.

#### Scenario: Existing student progress survives renumbering

- **WHEN** a student who completed a challenge before the migration reloads the catalogue after the migration ships
- **THEN** the challenge SHALL still be shown as completed, because the progress record key (slug) is unchanged
