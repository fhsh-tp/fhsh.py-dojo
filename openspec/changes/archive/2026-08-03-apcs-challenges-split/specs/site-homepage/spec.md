## MODIFIED Requirements

### Requirement: HomeView displays latest challenges

`HomeView.vue` SHALL display two latest-challenge sections in place of the former single 最新挑戰 section:

- 最新 Python 挑戰: the 3 challenges with resolved category `'python'` having the highest `id` values, sorted by `id` descending, with a `查看全部 →` link to `/challenges`.
- 最新 APCS 挑戰: the 3 challenges with resolved category `'apcs'` having the highest `id` values, sorted by `id` descending, with a `查看全部 →` link to `/apcs-challenges`.

Each challenge SHALL be rendered as a card showing: `title`, `difficulty`, and a link to the challenge page. `docs/index.md` SHALL keep passing the full unfiltered challenge array; the category split SHALL happen inside `HomeView.vue`.

#### Scenario: Each section shows its own top three

- **WHEN** Python challenges with ids 1–54 and APCS challenges with ids 55–58 exist
- **THEN** 最新 Python 挑戰 SHALL display ids 54, 53, 52 and 最新 APCS 挑戰 SHALL display ids 58, 57, 56

#### Scenario: View-all links point to the matching catalogue

- **WHEN** a user clicks 查看全部 in the 最新 Python 挑戰 section
- **THEN** the browser SHALL navigate to `/challenges`; the corresponding link in 最新 APCS 挑戰 SHALL navigate to `/apcs-challenges`

#### Scenario: A category with no challenges shows an empty state

- **WHEN** one category has zero challenges
- **THEN** that section SHALL render an empty state message instead of throwing an error, and the other section SHALL render normally
