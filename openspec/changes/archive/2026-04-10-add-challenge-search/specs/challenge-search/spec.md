## ADDED Requirements

### Requirement: Challenge data model includes chapter and description fields

The `Challenge` interface in `challenge.type.ts` SHALL include a `chapter` field of type `string` (e.g., `"ch1"`, `"ch2"`) and a `description` field of type `string`. Both fields SHALL be optional (defaulting to empty string when absent from frontmatter).

The content loader in `challenge.data.ts` SHALL extract `chapter` and `description` from each challenge markdown file's frontmatter and include them in the loaded data.

#### Scenario: Challenge with chapter and description in frontmatter

- **WHEN** a challenge markdown file has `chapter: ch1` and `description: 讀取名字並打招呼` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `chapter` equal to `"ch1"` and `description` equal to `"讀取名字並打招呼"`

#### Scenario: Challenge without chapter or description in frontmatter

- **WHEN** a challenge markdown file does not have `chapter` or `description` in its frontmatter
- **THEN** the loaded Challenge object SHALL have `chapter` equal to `""` and `description` equal to `""`

### Requirement: ChallengeListView displays a search input field

The ChallengeListView SHALL render a text search input (`<input type="search">`) above the difficulty filter buttons. The input SHALL span the full width of the container and include a placeholder indicating the searchable fields (e.g., "搜尋題目名稱、說明、標籤、章節...").

#### Scenario: Search input is visible on page load

- **WHEN** the user navigates to the challenge list page
- **THEN** a search input field SHALL be visible above the difficulty filter buttons
- **AND** the input SHALL have an empty value

#### Scenario: Search input has descriptive placeholder

- **WHEN** the search input is empty
- **THEN** the placeholder text SHALL indicate the searchable fields

### Requirement: Search filters challenges by text matching across multiple fields

When the user types in the search input, the challenge list SHALL be filtered in real time. A challenge matches the search query if the lowercased query string is contained within any of the following lowercased fields: `title`, `description`, `tags` (joined as a single string), or `chapter`.

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

#### Scenario: Search with no matches

- **WHEN** the user types a query that matches no challenge
- **THEN** the empty state message "沒有符合條件的挑戰。" SHALL be displayed

### Requirement: Search and difficulty filter work together as intersection

When both a search query and a difficulty filter are active, the displayed challenges SHALL be the intersection (AND) of both filters. A challenge MUST match the search query AND the selected difficulty to be shown.

#### Scenario: Combined search and difficulty filter

- **WHEN** the user selects difficulty "easy" AND types "ch1" in the search input
- **THEN** only challenges that are both easy difficulty AND belong to ch1 SHALL be displayed

#### Scenario: Clear search restores difficulty-only filter

- **WHEN** the user has both search query and difficulty filter active
- **AND** the user clears the search input
- **THEN** the list SHALL show all challenges matching the selected difficulty

### Requirement: Challenge frontmatter includes chapter and description

Each challenge markdown file in `docs/challenge/*.md` SHALL include `chapter` and `description` fields in its YAML frontmatter. The `chapter` field SHALL use the format `ch<N>` matching the tutorial chapter the challenge belongs to. The `description` field SHALL be a one-sentence summary of the challenge.

#### Scenario: Existing challenge files have chapter and description

- **WHEN** the challenge data is loaded
- **THEN** each challenge that has been updated SHALL have a non-empty `chapter` and `description` value
