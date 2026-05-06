## ADDED Requirements

### Requirement: Content loader scans all tutor articles

A VitePress data loader at `docs/shared/tutor.data.ts` SHALL use `createContentLoader('tutor/**/*.md', …)` to load all Markdown files under `docs/tutor/` at build time.

The loader SHALL export a `TutorArticle` interface with the following fields:

```ts
interface TutorArticle {
  title: string         // from frontmatter.title
  url: string           // VitePress page URL
  description: string   // from frontmatter.description
  subject: string       // derived from URL: /tutor/<subject>/...
  chapter: number       // from frontmatter.chapter
  section: string       // from frontmatter.section
  createdTime: Date     // parsed from frontmatter.createdTime
  isIndex: boolean      // from frontmatter.isIndex ?? false
  challenge?: string    // from frontmatter.challenge (optional)
}
```

The loader SHALL export the typed data array as `data` and provide a default export of the loader object, following the same pattern as `docs/shared/challenge.data.ts`.

#### Scenario: Data is available at build time

- **WHEN** a Vue component imports `{ data } from '…/shared/tutor.data'`
- **THEN** `data` SHALL be a `TutorArticle[]` array containing all parsed tutor articles

#### Scenario: Empty tutor directory

- **WHEN** no `.md` files exist under `docs/tutor/`
- **THEN** the loader SHALL return an empty array without throwing an error

---

### Requirement: subject field is derived from URL path

The `subject` field SHALL be extracted from the URL by parsing the path segment immediately following `/tutor/` (e.g., URL `/tutor/py/ch1/1-1` → `subject: "py"`).

#### Scenario: Python article subject extraction

- **WHEN** a file at `docs/tutor/py/ch1/1-1.md` is loaded
- **THEN** the resulting `TutorArticle.subject` SHALL equal `"py"`

#### Scenario: Algorithm article subject extraction

- **WHEN** a file at `docs/tutor/alg/ch1/1-1.md` is loaded
- **THEN** the resulting `TutorArticle.subject` SHALL equal `"alg"`

---

### Requirement: Loader distinguishes index pages from section articles

The loader SHALL set `isIndex: true` for files whose frontmatter contains `isIndex: true`, and `isIndex: false` otherwise. Consumers SHALL use this field to filter between chapter overview pages and section articles.

#### Scenario: Section article isIndex flag

- **WHEN** a section file (e.g., `1-1.md`) without `isIndex` in frontmatter is loaded
- **THEN** `TutorArticle.isIndex` SHALL be `false`

#### Scenario: Index page isIndex flag

- **WHEN** a chapter `index.md` with `isIndex: true` in frontmatter is loaded
- **THEN** `TutorArticle.isIndex` SHALL be `true`
