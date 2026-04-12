## ADDED Requirements

### Requirement: All references are verified against authoritative sources

Each of the 23 references in `docs/tutor/py/ch1/reference.md` SHALL have been verified against at least one authoritative source. The verification source SHALL be one of: Semantic Scholar, CrossRef, publisher website, or institutional repository.

For academic papers (references #3–#14, #16, #22, #23), the entry SHALL include:
- Correct author names (not journal or publisher names)
- Correct publication year
- Correct title matching the authoritative record
- Correct venue (journal name, conference name, or publisher)
- DOI link where available in the authoritative record

For web resources (references #19, #20, #21), the external URL SHALL return HTTP 200 status (following redirects).

For policy and institutional documents (references #1, #2, #6, #17), the entry SHALL have either a locally stored PDF file that exists at the referenced path, or an external URL that returns HTTP 200 status, or both.

References that cannot be verified against any authoritative source SHALL be removed or replaced with a verified alternative.

#### Scenario: Academic reference has correct author field

- **WHEN** a reference entry for an academic paper is checked against Semantic Scholar or CrossRef
- **THEN** the author field in `reference.md` SHALL match the actual author names from the authoritative record, not the journal name or publisher name

#### Scenario: Academic reference includes DOI where available

- **WHEN** a reference entry for an academic paper has a DOI registered in Semantic Scholar or CrossRef
- **THEN** the reference entry SHALL include a DOI link in the format `[DOI](https://doi.org/<doi>)` or embedded in the existing URL

#### Scenario: Web resource URL is accessible

- **WHEN** a reference entry includes an external URL to a web resource
- **THEN** an HTTP GET request to that URL SHALL return status 200 (after following redirects), or status 403 with a valid HTML response body (indicating bot protection but resource existence)

#### Scenario: Unverifiable reference is handled

- **WHEN** a reference entry cannot be found in any authoritative source (Semantic Scholar, CrossRef, publisher website) AND its URL returns HTTP 404 or connection error
- **THEN** the reference entry SHALL be removed from `reference.md` and subsequent entries SHALL be renumbered

## MODIFIED Requirements

### Requirement: Reference page lists all academic sources

The system SHALL provide a `docs/tutor/py/ch1/reference.md` file with frontmatter `layout: doc` and `title: 模組一參考文獻`. The file SHALL list all verified academic references organized into four topic sections:

1. **數學素養 (Mathematical Literacy)** — PISA framework, Taiwan 108 curriculum math domain
2. **運算思維 (Computational Thinking)** — Wing, ISTE/CSTA, Barr & Stephenson, Brennan & Resnick, Shute et al., Grover & Pea
3. **整合研究 (Integration Research)** — Weintrop et al., Olteanu, Lee et al., systematic reviews
4. **台灣課綱與教育資源 (Taiwan Curriculum & Resources)** — 108 curriculum, Hsu & Hu, NRICH, Project Euler

Each entry MUST include: correct author(s), year, title, publication venue, and either a relative link to a local PDF (`./references/filename.pdf`) or a verified external URL. The total number of references SHALL be adjusted if any entries are removed due to verification failure.

#### Scenario: Reference page renders in sidebar

- **WHEN** VitePress builds the site
- **THEN** `reference.md` SHALL appear in the Chapter 1 sidebar navigation

#### Scenario: Local PDF links resolve correctly

- **WHEN** the reference page contains a relative link to `./references/filename.pdf`
- **THEN** clicking the link SHALL download the corresponding PDF from the `references/` directory

#### Scenario: All author fields contain actual author names

- **WHEN** a reference entry is for an academic paper with identifiable authors
- **THEN** the author field SHALL contain the actual author names, not the journal name, publisher name, or database name
