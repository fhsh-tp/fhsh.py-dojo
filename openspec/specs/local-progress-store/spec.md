# local-progress-store Specification

## Purpose

TBD - created by archiving change 'add-student-progress-persistence'. Update Purpose after archive.

## Requirements

### Requirement: Client-only IndexedDB access

The persistence layer SHALL access IndexedDB exclusively from client-side lifecycle hooks (component `onMounted`, or store actions invoked from them) and SHALL NOT perform any IndexedDB, `window`, or `indexedDB` access during server-side rendering or static build. The store's `defineStore` setup body MUST NOT open a database connection.

#### Scenario: Static build does not touch IndexedDB

- **WHEN** the site is produced by the production build, which SSR-renders every page
- **THEN** no code path reads or writes `indexedDB`, and the build completes without a ReferenceError

#### Scenario: Persistence initialises after mount

- **WHEN** a challenge page mounts on the client
- **THEN** the store opens the database inside `onMounted` or an action called from it, never at module evaluation or store setup time

---
### Requirement: Feature detection and graceful degradation

The persistence layer SHALL detect whether IndexedDB is usable and, when it is not, SHALL degrade to a read-only empty state so that all challenge, run, and submit functionality continues to work unaffected.

#### Scenario: IndexedDB unavailable

- **WHEN** `indexedDB` is absent or throws on open
- **THEN** availability detection returns false, reads return empty results, writes are no-ops, and the student can still solve and submit challenges normally

---
### Requirement: Slug-keyed records

All persisted records SHALL be keyed by the per-challenge slug, and the slug SHALL be provided as a first-class field of the challenge catalogue data rather than derived from a rendered URL at the presentation layer.

#### Scenario: Progress keyed by slug

- **WHEN** progress is written for a challenge whose file is `docs/challenge/arithmetic-sum.md`
- **THEN** the record is stored under key `arithmetic-sum`, matching the key the executor already uses

---
### Requirement: Retention cap on sessions per challenge

The persistence layer SHALL bound stored recording data by capping the number of retained work sessions per challenge, keeping the most recent sessions in full and discarding the oldest beyond the cap. The cap MUST NOT truncate the event list within a retained session.

#### Scenario: Old sessions pruned, recent kept whole

- **GIVEN** the cap is 5 sessions per challenge
- **WHEN** a sixth session for the same challenge is recorded
- **THEN** the oldest session is removed and the five most recent sessions are retained with all their events intact

---
### Requirement: Retired slug and id ledger

The project SHALL maintain a ledger of retired challenge slugs and numeric ids so that a reused slug or id does not silently inherit a prior challenge's stored progress. The scaffold tooling and content-regression checks SHALL consult the ledger.

#### Scenario: Reused slug is flagged

- **WHEN** an author attempts to scaffold a new challenge with a slug present in the retired ledger
- **THEN** the scaffold tooling reports the collision instead of silently reusing the name

---
### Requirement: Versioned schema

The IndexedDB schema SHALL carry an explicit version, and schema changes SHALL be handled through the database upgrade path with backward-compatible migration or safe discard.

#### Scenario: Upgrade path present

- **WHEN** the database is opened at a newer schema version than the stored one
- **THEN** the upgrade handler runs and either migrates or safely resets, without data corruption or an unhandled error
