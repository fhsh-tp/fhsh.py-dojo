## MODIFIED Requirements

### Requirement: Challenge ID continuity across Module 2

All challenge files referenced from Module 2 sections SHALL have sequential IDs with no gaps or duplicates when sorted numerically. Module 2 challenge IDs SHALL form a contiguous block that starts immediately after Module 1's last ID.

#### Scenario: Challenge IDs form continuous sequence

- **WHEN** all challenge IDs referenced from Module 2 are collected and sorted
- **THEN** the IDs SHALL form a continuous integer sequence with no gaps

#### Scenario: Per-chapter ID blocks are contiguous

- **WHEN** challenge IDs are grouped by chapter and sorted
- **THEN** each chapter's IDs SHALL form a contiguous block with no interleaving from other chapters
