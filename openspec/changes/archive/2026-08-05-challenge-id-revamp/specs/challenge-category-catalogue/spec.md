## ADDED Requirements

### Requirement: ChallengeCard displays the challenge id

Every ChallengeCard SHALL render the challenge's string id (for example py003) as a visible label alongside the title, on every surface that renders ChallengeCard (both catalogue pages and the homepage latest-challenges lists). The label SHALL show the id verbatim without reformatting.

#### Scenario: Card shows the id on a catalogue page

- **WHEN** the Python catalogue page renders the challenge whose id is py003
- **THEN** the card SHALL display the text py003 alongside the challenge title

#### Scenario: Card shows the id on the homepage

- **WHEN** the homepage latest-challenges list renders a challenge card
- **THEN** the card SHALL display that challenge's id verbatim
