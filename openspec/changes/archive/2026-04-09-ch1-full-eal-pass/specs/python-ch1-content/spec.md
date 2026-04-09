## MODIFIED Requirements

### Requirement: Chapter 1 sections follow emotional punctuation density rule K-1

Each tutorial section in `docs/tutor/py/ch1/` SHALL maintain a balanced density of emotional punctuation elements (kaomoji, parenthetical jokes, student dialogue interjections). Within any contiguous block of 30 lines of prose (excluding fenced code blocks, tables, and image placeholders), at least one emotional punctuation element SHALL be present. Within any contiguous block of 10 lines of prose, no more than one emotional punctuation element SHALL be present.

Additionally, kaomoji variety SHALL be maintained:

- The same kaomoji SHALL NOT appear more than twice within a single section file.
- Across all files within the same chapter (e.g., `1-1.md` through `1-4.md`), the same kaomoji SHALL NOT appear more than three times.
- Each section file SHALL use kaomoji from at least two different emotional categories as defined in the `phoenix-popular-science-article-style` kaomoji catalog: Resigned, Celebration, Shock, Frustration, Sadness, Cute, Mischievous, Confusion.

#### Scenario: Prose block has adequate emotional punctuation

- **WHEN** a contiguous block of 30 lines of prose (excluding code, tables, images) is identified in a tutorial section
- **THEN** at least one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Prose block does not have excessive emotional punctuation

- **WHEN** a contiguous block of 10 lines of prose is identified in a tutorial section
- **THEN** no more than one kaomoji, parenthetical joke, or student dialogue interjection SHALL be present within that block

#### Scenario: Kaomoji is not overused within a single file

- **WHEN** a tutorial section file is scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than twice in that file

#### Scenario: Kaomoji is not overused across a chapter

- **WHEN** all section files within a chapter are scanned for kaomoji usage
- **THEN** no single kaomoji SHALL appear more than three times across the entire chapter

#### Scenario: Kaomoji emotional variety is maintained

- **WHEN** a tutorial section file is scanned for kaomoji emotional categories
- **THEN** the file SHALL contain kaomoji from at least two different emotional categories
