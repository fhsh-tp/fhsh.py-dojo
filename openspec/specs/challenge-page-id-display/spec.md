# challenge-page-id-display Specification

## Purpose

TBD - created by archiving change 'id-badge-c-alias'. Update Purpose after archive.

## Requirements

### Requirement: Challenge page header displays the challenge id

The challenge page header rendered by `AppHeader.vue` SHALL display the challenge's string id immediately to the left of the title, styled as a small monospace low-emphasis (muted) label sharing the ChallengeCard id badge's visual language, with its palette adapted to stay legible on the header background, while the header keeps its single-row height. The label SHALL be non-interactive: no click handler, no tooltip, no link. The label element SHALL carry `data-testid="page-challenge-id"` (distinct from the card's `challenge-id`) and SHALL show the id verbatim without reformatting.

`AppHeader.vue` SHALL accept the id as an optional string prop defaulting to the empty string and SHALL NOT render the label element at all when the prop is empty. `ChallengeView.vue` SHALL derive the prop value from the page frontmatter: when `frontmatter.id` coerced to a string matches `^(py|apcs)\d{3}$` the value is that string, otherwise it is the empty string. Validation SHALL reuse the shared pattern exported by `docs/shared/challenge-id` rather than declaring a local copy. An invalid or missing id SHALL NOT affect the rendering of the title, difficulty badge, back button, or theme toggle.

#### Scenario: Valid id is shown verbatim

- **WHEN** the challenge page for a challenge whose frontmatter id is py001 renders
- **THEN** the header SHALL contain an element with `data-testid="page-challenge-id"` whose text is exactly py001, positioned before the title

#### Scenario: Missing or malformed id hides the label only

- **WHEN** the challenge page renders with a frontmatter id that is absent, empty, or not matching the challenge id pattern (for example 59 or PY001)
- **THEN** no element with `data-testid="page-challenge-id"` SHALL be rendered, and the title, difficulty badge, back button, and theme toggle SHALL render unchanged
