## MODIFIED Requirements

### Requirement: Build step generates the Cloudflare Pages redirects file

A script at `scripts/generate-redirects.ts` SHALL scan every markdown file under docs/challenge/, read each file's frontmatter id and derive its slug from the file basename, and write a plain-text redirects file to docs/public/_redirects. The file SHALL begin with a generated-file header comment line and SHALL contain exactly one redirect line per challenge file in the form `/c/<id> /challenge/<slug> 302`. Each slug SHALL match `^[a-z0-9-]+$` (the same contract enforced by the pool generator); a filename outside that contract SHALL fail the build naming the file, because a space or newline in a slug would corrupt the whitespace-delimited rule format. Redirect target paths SHALL NOT carry a `.html` extension. The script SHALL exit with a non-zero code and name the offending file when any challenge file is missing an id or has an id that does not match `^(py|apcs)\d{3}$`, when two files declare the same id, and when a file basename is itself id-shaped (matching the id pattern) — an id-shaped slug no longer collides with the alias rules under `/c/`, but it would still blur the catalogue identity: the id-shaped `/challenge/<slug>` page and the `/c/<same-token>` alias could then name two different challenges. The script SHALL also exit non-zero when zero challenge files are found, instead of writing an empty redirects file that silently kills every alias. The dev and build pipelines in package.json SHALL run this script so the file is always regenerated from current content. The output SHALL NOT contain any `/challenge/<id>` source-path rule: the pre-`/c/` alias form is fully replaced, not kept alongside.

#### Scenario: One valid line per challenge

- **WHEN** the generator runs against the full challenge set
- **THEN** the output SHALL contain exactly as many redirect lines as there are challenge files, each matching the documented line format, with no duplicate source paths and no `/challenge/<id>`-form source paths

##### Example: Generated line

- **GIVEN** docs/challenge/collatz-steps.md declares id py031
- **WHEN** the generator runs
- **THEN** the output contains the line `/c/py031 /challenge/collatz-steps 302`

#### Scenario: Invalid or missing id fails loudly

- **WHEN** a challenge file has no id or an id not matching the required pattern
- **THEN** the generator SHALL exit non-zero and its error message SHALL name that file

#### Scenario: Id-shaped filename fails loudly

- **WHEN** a challenge file basename (without .md) matches the challenge id pattern, for example a file named py001.md
- **THEN** the generator SHALL exit non-zero and its error message SHALL name that file

#### Scenario: Zero challenge files fails loudly

- **WHEN** the generator finds no challenge markdown files at all
- **THEN** it SHALL exit non-zero instead of writing a redirects file with no rules

#### Scenario: Duplicate id fails loudly

- **WHEN** two challenge files declare the same id
- **THEN** the generator SHALL exit non-zero and its error message SHALL name both files

### Requirement: Deployed alias URLs redirect to canonical slug URLs

On the deployed site, a request to `/c/<id>` for any existing challenge SHALL receive an HTTP 3xx response whose Location header is the extensionless canonical slug path for that challenge (`/challenge/<slug>`). Verification SHALL assert the 3xx class and the Location value only; it SHALL NOT assert the exact status code of any subsequent platform-level URL normalization, because that code differs between Cloudflare Pages and Workers static assets. A request to `/challenge/<id>` SHALL NOT be redirected: the pre-`/c/` alias form never shipped to production and is removed rather than kept as a second namespace.

#### Scenario: Alias reaches the challenge page

- **WHEN** a browser requests /c/py003 on the deployed site
- **THEN** the response is a 3xx redirect with Location /challenge/<slug-of-py003> and the browser lands on the canonical challenge page

#### Scenario: Retired alias form is not redirected

- **WHEN** a browser requests /challenge/py003 on the deployed site
- **THEN** no redirect rule matches and the site serves its normal not-found response
