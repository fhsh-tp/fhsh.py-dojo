## MODIFIED Requirements

### Requirement: Retired slug and id ledger

The project SHALL maintain a ledger of retired challenge slugs and string ids so that a reused slug or id does not silently inherit a prior challenge's stored progress or catalogue identity. Ledger ids SHALL be stored as strings in the challenge id format. The scaffold tooling and content-regression checks SHALL consult the ledger, and their id handling SHALL parse string ids; an id scan that cannot parse any current challenge id SHALL fail loudly rather than silently skipping its assertions.

The scaffold tooling SHALL treat an unreadable or untrustworthy ledger as fail-closed. A ledger that is not valid JSON, is not a JSON object, has a `slugs` or `ids` field that is present but not an array, or contains an entry that is not a well-formed slug string (`slugs`) or challenge-id string (`ids`) SHALL cause the scaffold to exit non-zero with a message naming the offending entry, rather than proceeding with the reuse guard silently disarmed. An absent `slugs`/`ids` field SHALL be treated as empty, and unrecognised keys (such as `_comment`) SHALL be ignored.

#### Scenario: Reused slug is flagged

- **WHEN** an author attempts to scaffold a new challenge with a slug present in the retired ledger
- **THEN** the scaffold tooling reports the collision instead of silently reusing the name

#### Scenario: Reused string id is flagged

- **WHEN** an author attempts to scaffold a new challenge that would be assigned an id present in the retired ledger
- **THEN** the scaffold tooling reports the collision instead of silently reusing the id

#### Scenario: Ledger guard cannot degrade into a no-op

- **WHEN** the content-regression check scans docs/challenge/ ids against the ledger
- **THEN** the check SHALL assert that it actually parsed one id per challenge file, so a format drift surfaces as a test failure instead of skipped assertions

#### Scenario: Untrustworthy ledger fails closed

- **WHEN** the retired ledger carries a legacy numeric id (`"ids": [59]`), a numeric string (`"59"`), a wrong-case id (`"PY059"`), a non-array `ids` field, or a non-object root
- **THEN** the scaffold tooling SHALL exit non-zero naming the offending entry, instead of loading a ledger whose membership test can never match
