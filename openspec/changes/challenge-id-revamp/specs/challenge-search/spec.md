## MODIFIED Requirements

### Requirement: Search filters challenges by text matching across multiple fields

When the user types in the search input, the challenge list SHALL be filtered in real time. The query SHALL be normalized by trimming surrounding whitespace and lowercasing before matching. A challenge matches the search query if the normalized query is contained within any of the following lowercased fields: `title`, `description`, `tags` (joined as a single string), or `chapter` — or if the query matches the challenge `id` under the id matching rules below.

Id matching SHALL apply exactly one of two rules, chosen by the shape of the normalized query:

1. If the normalized query consists solely of decimal digits, it SHALL match a challenge whose id ordinal (the decimal integer obtained by stripping the id's leading non-digit characters) equals the query parsed as a decimal integer.
2. Otherwise, it SHALL match a challenge whose id starts with the normalized query.

Text-field matching and id matching SHALL be combined with OR: a challenge is shown when either matches. Because each catalogue page receives a category-filtered challenge list, id matching never crosses categories on a page.

#### Scenario: Search matches by title

- **WHEN** the user types "飲料" in the search input
- **THEN** only challenges whose title contains "飲料" SHALL be displayed

#### Scenario: Search matches by tag

- **WHEN** the user types "input" in the search input
- **THEN** all challenges that have "input" in their tags array SHALL be displayed

#### Scenario: Search matches by chapter

- **WHEN** the user types "ch1" in the search input
- **THEN** all challenges with `chapter` equal to `"ch1"` SHALL be displayed

#### Scenario: Search matches by description

- **WHEN** the user types "收銀" in the search input
- **THEN** challenges whose description contains "收銀" SHALL be displayed

#### Scenario: Pure-digit query matches id ordinal exactly

- **WHEN** the user types "3", "03", or "003" on the Python catalogue page
- **THEN** the challenge with id py003 SHALL be displayed via the id rule, together with any challenge whose text fields contain the query

##### Example: Digit query matrix on the Python page

| query | id-rule matches |
| --- | --- |
| 3 | py003 |
| 03 | py003 |
| 003 | py003 |
| 55 | (none — Python page has ordinals 1–54) |

#### Scenario: Non-digit query matches id by prefix

- **WHEN** the user types "py00" on the Python catalogue page
- **THEN** challenges py001 through py009 SHALL be displayed via the id rule

#### Scenario: Unpadded prefixed query does not match via id

- **WHEN** the user types "py3" on the Python catalogue page
- **THEN** no challenge SHALL be displayed via the id rule, because "py3" is not a prefix of any zero-padded id and is not a pure-digit query

#### Scenario: Search with no matches

- **WHEN** the user types a query that matches no challenge
- **THEN** the empty state message "沒有符合條件的挑戰。" SHALL be displayed
