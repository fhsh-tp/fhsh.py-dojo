## ADDED Requirements

### Requirement: ChallengeLink renders a styled link to a challenge

A Vue component at `.vitepress/theme/components/tutor/ChallengeLink.vue` SHALL accept a `slug` prop of type `string` and render a styled card linking to the corresponding challenge page at `/challenge/<slug>`.

The component SHALL:
1. Import `{ data as challenges }` from `docs/shared/challenge.data` using a relative path
2. Look up the challenge whose `url` ends with `/<slug>` or matches `slug` in the challenges array
3. Render the challenge `title`, a difficulty badge (using the challenge `difficulty` field), and a link to the challenge page

The component SHALL be registered globally in `.vitepress/theme/index.ts` so it is available in all Markdown files without explicit import.

#### Scenario: Known slug renders challenge card

- **WHEN** a tutor article contains `<ChallengeLink slug="hello-world" />`
- **THEN** the rendered output SHALL display the challenge title, difficulty badge, and a working link to `/challenge/hello-world`

#### Scenario: Unknown slug renders fallback

- **WHEN** `slug` does not match any challenge in `challenge.data`
- **THEN** the component SHALL render a disabled placeholder with text `挑戰題目尚未建立` and SHALL NOT throw a runtime error

#### Scenario: Component available without import in Markdown

- **WHEN** a tutor `.md` file contains `<ChallengeLink slug="…" />` with no `<script setup>` import
- **THEN** VitePress SHALL render the component without a "component not found" error
