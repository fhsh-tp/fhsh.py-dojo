## MODIFIED Requirements

### Requirement: Retired slug and id ledger

The project SHALL maintain a ledger of retired challenge slugs and string ids so that a reused slug or id does not silently inherit a prior challenge's stored progress or catalogue identity. Ledger ids SHALL be stored as strings in the challenge id format. The scaffold tooling and content-regression checks SHALL consult the ledger, and their id handling SHALL parse string ids; an id scan that cannot parse any current challenge id SHALL fail loudly rather than silently skipping its assertions.

#### Scenario: Reused slug is flagged

- **WHEN** an author attempts to scaffold a new challenge with a slug present in the retired ledger
- **THEN** the scaffold tooling reports the collision instead of silently reusing the name

#### Scenario: Reused string id is flagged

- **WHEN** an author attempts to scaffold a new challenge that would be assigned an id present in the retired ledger
- **THEN** the scaffold tooling reports the collision instead of silently reusing the id

#### Scenario: Ledger guard cannot degrade into a no-op

- **WHEN** the content-regression check scans docs/challenge/ ids against the ledger
- **THEN** the check SHALL assert that it actually parsed one id per challenge file, so a format drift surfaces as a test failure instead of skipped assertions
