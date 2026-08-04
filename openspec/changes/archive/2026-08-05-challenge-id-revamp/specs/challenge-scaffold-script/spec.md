## MODIFIED Requirements

### Requirement: CLI script scaffolds a new challenge file

A script at `scripts/new-challenge.ts` SHALL accept positional command-line arguments and generate a `docs/challenge/<kebab-name>.md` file containing a complete, valid challenge frontmatter skeleton and Markdown body.

The script SHALL accept the following arguments:
1. `<name>` (required) — kebab-case challenge name; used as the output filename
2. `--title <string>` (optional) — display title; defaults to title-cased version of `<name>`
3. `--difficulty <easy|medium|hard>` (optional) — defaults to `easy`
4. `--algorithm <snake_case>` (optional) — defaults to `<name>` with hyphens replaced by underscores
5. `--category <python|apcs>` (optional) — defaults to `python`

The generated frontmatter SHALL include all mandatory fields defined in `Usage.md`: `layout`, `id`, `title`, `difficulty`, `tags`, `algorithm`, `testcase_count`, `params`, `generator`, and `starter_code`. The generated frontmatter SHALL always include an explicit `category` line carrying the resolved `--category` value. Each optional field SHALL use a sensible placeholder value so the file is immediately parseable by `scripts/generate-pools.ts`.

The `id` field SHALL be a string in the challenge id format: the category's prefix (`python` maps to `py`, `apcs` maps to `apcs`) followed by a 3-digit zero-padded ordinal. The ordinal SHALL be the maximum existing ordinal among ids sharing that prefix across all `docs/challenge/*.md` files, plus 1. If no challenge file carries that prefix, the ordinal SHALL default to 1 (for example py001). Id computation SHALL parse string ids; files whose id does not match the challenge id format SHALL cause the script to exit non-zero naming the file, rather than being silently ignored.

The script SHALL exit with a non-zero code and a descriptive error message if:
- `<name>` is not provided
- `<name>` contains characters other than lowercase letters, digits, and hyphens
- `<name>` is itself id-shaped (matches the challenge id pattern, e.g. py001) — slugs and /challenge/<id> aliases share one URL namespace
- `--difficulty` is not one of `easy`, `medium`, or `hard`
- `--category` is not one of `python` or `apcs`
- The output file already exists (to prevent accidental overwrite)

#### Scenario: Generate scaffold with defaults

- **WHEN** `pnpm new-challenge bubble-sort` is executed
- **THEN** `docs/challenge/bubble-sort.md` is created with `algorithm: bubble_sort`, `difficulty: easy`, `category: python`, `id` set to the next py ordinal (zero-padded string), and placeholder `generator` and `starter_code` blocks

##### Example: Per-category next id

- **GIVEN** existing ids py001–py054 and apcs001–apcs005
- **WHEN** `pnpm new-challenge bubble-sort --category apcs` is executed
- **THEN** the generated frontmatter contains `id: apcs006`

#### Scenario: Generate scaffold with explicit options

- **WHEN** `pnpm new-challenge linear-search --title "線性搜尋" --difficulty medium --algorithm linear_search --category apcs` is executed
- **THEN** `docs/challenge/linear-search.md` is created with `title: 線性搜尋`, `difficulty: medium`, `algorithm: linear_search`, and `category: apcs`

#### Scenario: Output file already exists

- **WHEN** the target `docs/challenge/<name>.md` file already exists
- **THEN** the script exits with code 1 and prints `[new-challenge] ERROR: docs/challenge/<name>.md already exists. Aborting to prevent overwrite.`

#### Scenario: Invalid difficulty value

- **WHEN** `--difficulty` is set to a value other than `easy`, `medium`, or `hard`
- **THEN** the script exits with code 1 and prints `[new-challenge] ERROR: --difficulty must be one of: easy, medium, hard`

#### Scenario: Invalid category value

- **WHEN** `--category` is set to a value other than `python` or `apcs`
- **THEN** the script exits with code 1 and prints `[new-challenge] ERROR: --category must be one of: python, apcs`

#### Scenario: Invalid name format

- **WHEN** `<name>` contains uppercase letters or non-kebab characters (e.g., `BubbleSort` or `bubble_sort`)
- **THEN** the script exits with code 1 and prints `[new-challenge] ERROR: <name> must be kebab-case (lowercase letters, digits, hyphens only)`

#### Scenario: Id-shaped name is rejected

- **WHEN** `pnpm new-challenge py001` is executed
- **THEN** the script exits with code 1 and its error message states that id-shaped names are not allowed because slugs and aliases share the /challenge/ namespace

#### Scenario: Unparseable existing id fails loudly

- **WHEN** any existing `docs/challenge/*.md` file carries an id that does not match the challenge id format
- **THEN** the script exits non-zero and its error message names that file
