## ADDED Requirements

### Requirement: Build step generates the Cloudflare Pages redirects file

A script at `scripts/generate-redirects.ts` SHALL scan every markdown file under docs/challenge/, read each file's frontmatter id and derive its slug from the file basename, and write a plain-text redirects file to docs/public/_redirects. The file SHALL begin with a generated-file header comment line and SHALL contain exactly one redirect line per challenge file in the form `/challenge/<id> /challenge/<slug> 302`. Each slug SHALL match `^[a-z0-9-]+$` (the same contract enforced by the pool generator); a filename outside that contract SHALL fail the build naming the file, because a space or newline in a slug would corrupt the whitespace-delimited rule format. Redirect target paths SHALL NOT carry a `.html` extension. The script SHALL exit with a non-zero code and name the offending file when any challenge file is missing an id or has an id that does not match `^(py|apcs)\d{3}$`, and when two files declare the same id. The dev and build pipelines in package.json SHALL run this script so the file is always regenerated from current content.

#### Scenario: One valid line per challenge

- **WHEN** the generator runs against the full challenge set
- **THEN** the output SHALL contain exactly as many redirect lines as there are challenge files, each matching the documented line format, with no duplicate source paths

##### Example: Generated line

- **GIVEN** docs/challenge/collatz-steps.md declares id py031
- **WHEN** the generator runs
- **THEN** the output contains the line `/challenge/py031 /challenge/collatz-steps 302`

#### Scenario: Invalid or missing id fails loudly

- **WHEN** a challenge file has no id or an id not matching the required pattern
- **THEN** the generator SHALL exit non-zero and its error message SHALL name that file

#### Scenario: Duplicate id fails loudly

- **WHEN** two challenge files declare the same id
- **THEN** the generator SHALL exit non-zero and its error message SHALL name both files

### Requirement: Redirects file is generated output, not source

docs/public/_redirects SHALL be listed in .gitignore and SHALL NOT be committed, following the same convention as docs/public/pools/.

#### Scenario: Generated file stays out of version control

- **WHEN** the generator has produced docs/public/_redirects and git status is inspected
- **THEN** the file SHALL NOT appear as an untracked or modified path

### Requirement: Deployed alias URLs redirect to canonical slug URLs

On the deployed site, a request to `/challenge/<id>` for any existing challenge SHALL receive an HTTP 3xx response whose Location header is the extensionless canonical slug path for that challenge. Verification SHALL assert the 3xx class and the Location value only; it SHALL NOT assert the exact status code of any subsequent platform-level URL normalization, because that code differs between Cloudflare Pages and Workers static assets.

#### Scenario: Alias reaches the challenge page

- **WHEN** a browser requests /challenge/py003 on the deployed site
- **THEN** the response is a 3xx redirect with Location /challenge/<slug-of-py003> and the browser lands on the canonical challenge page
