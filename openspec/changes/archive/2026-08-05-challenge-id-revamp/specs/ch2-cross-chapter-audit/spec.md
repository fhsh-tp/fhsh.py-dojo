## MODIFIED Requirements

### Requirement: Challenge ID continuity across Module 2

All challenge files referenced from Module 2 sections SHALL carry string ids in the challenge id format, and their ordinals (the decimal integer after the category prefix) SHALL be sequential with no gaps or duplicates when sorted numerically within the `py` prefix. Module 2 challenge ordinals SHALL form a contiguous block that starts immediately after Module 1's last ordinal.

#### Scenario: Challenge ordinals form continuous sequence

- **WHEN** all challenge ids referenced from Module 2 are collected and their ordinals sorted
- **THEN** the ordinals SHALL form a continuous integer sequence with no gaps

#### Scenario: Per-chapter ordinal blocks are contiguous

- **WHEN** challenge ordinals are grouped by chapter and sorted
- **THEN** each chapter's ordinals SHALL form a contiguous block with no interleaving from other chapters
