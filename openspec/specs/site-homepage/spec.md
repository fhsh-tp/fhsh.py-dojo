## ADDED Requirements

### Requirement: HomeView replaces ChallengeListView as the homepage component

`docs/index.md` SHALL import both `tutor.data.ts` and `challenge.data.ts` and render `HomeView.vue` in place of the current `ChallengeListView`. A new `HomeView.vue` component SHALL be created at `.vitepress/theme/views/HomeView.vue`.

`ChallengeListView` SHALL remain unchanged and be used at `docs/challenge/index.md` for the standalone challenge list page. `docs/challenge/index.md` SHALL be a new file with `layout: doc` and a `<ChallengeListView :challenges="challenges" />` component.

#### Scenario: Homepage renders HomeView

- **WHEN** a user visits the site root `/`
- **THEN** the page SHALL display `HomeView` with three sections: 最新教學, 分類教學, 最新挑戰

#### Scenario: Challenge list accessible at /challenge/

- **WHEN** a user visits `/challenge/`
- **THEN** the page SHALL display `ChallengeListView` with the full challenge list


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

---

### Requirement: HomeView displays latest tutorial articles

The 最新教學 section of `HomeView.vue` SHALL display the 3 most recently created tutor section articles (where `isIndex === false`), sorted by `createdTime` in descending order.

Each article SHALL be rendered as a card showing: `title`, `description`, `subject`, `section`, and a link to the article URL.

#### Scenario: Three most recent articles shown

- **WHEN** 5 tutor articles exist with different `createdTime` values
- **THEN** the 最新教學 section SHALL display exactly the 3 articles with the most recent `createdTime`

#### Scenario: No tutor articles

- **WHEN** no tutor articles exist (`tutor.data` returns an empty array)
- **THEN** the 最新教學 section SHALL render an empty state message instead of throwing an error


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

---

### Requirement: HomeView displays tutorials grouped by chapter

The 分類教學 section of `HomeView.vue` SHALL display all tutor section articles (where `isIndex === false`) grouped by `subject` and then by `chapter`, sorted by `chapter` ascending within each subject.

#### Scenario: Articles grouped by subject and chapter

- **WHEN** tutor articles exist across subjects `py` (chapters 1–4) and `alg` (chapter 1)
- **THEN** the 分類教學 section SHALL show a group for `py` with chapters 1–4 and a group for `alg` with chapter 1, each listing the articles within that chapter

#### Scenario: Empty subject group is hidden

- **WHEN** `docs/tutor/alg/` contains no section articles
- **THEN** the `alg` group SHALL NOT appear in the 分類教學 section


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

---

### Requirement: HomeView displays latest challenges

The 最新挑戰 section of `HomeView.vue` SHALL display the 3 challenges with the highest `id` values, sorted by `id` in descending order.

Each challenge SHALL be rendered as a card showing: `title`, `difficulty`, and a link to the challenge page.

#### Scenario: Three highest-id challenges shown

- **WHEN** 10 challenges exist with ids 1–10
- **THEN** the 最新挑戰 section SHALL display challenges with ids 10, 9, and 8

#### Scenario: No challenges exist

- **WHEN** the challenges array is empty
- **THEN** the 最新挑戰 section SHALL render an empty state message instead of throwing an error

## Requirements


<!-- @trace
source: add-tutorial-content-system
updated: 2026-04-05
code:
  - docs/index.md
  - docs/tutor/alg/.gitkeep
  - .vitepress/nav.yml
  - docs/tutor/py/ch2/index.md
  - docs/challenge/index.md
  - .vitepress/config.mts
  - docs/tutor/py/.gitkeep
  - .vitepress/theme/index.ts
  - scripts/new-tutor.ts
  - package.json
  - .vitepress/theme/views/HomeView.vue
  - docs/tutor/py/ch3/index.md
  - docs/tutor/py/ch1/index.md
  - .vitepress/theme/components/tutor/ChallengeLink.vue
  - docs/shared/tutor.data.ts
  - docs/challenge/.gitkeep
  - docs/tutor/py/ch4/index.md
  - docs/tutor/py/index.md
  - docs/tutor/ds/.gitkeep
-->

### Requirement: HomeView replaces ChallengeListView as the homepage component

`docs/index.md` SHALL import both `tutor.data.ts` and `challenge.data.ts` and render `HomeView.vue` in place of the current `ChallengeListView`. A new `HomeView.vue` component SHALL be created at `.vitepress/theme/views/HomeView.vue`.

`ChallengeListView` SHALL remain unchanged and be used at `docs/challenge/index.md` for the standalone challenge list page. `docs/challenge/index.md` SHALL be a new file with `layout: doc` and a `<ChallengeListView :challenges="challenges" />` component.

#### Scenario: Homepage renders HomeView

- **WHEN** a user visits the site root `/`
- **THEN** the page SHALL display `HomeView` with three sections: 最新教學, 分類教學, 最新挑戰

#### Scenario: Challenge list accessible at /challenge/

- **WHEN** a user visits `/challenge/`
- **THEN** the page SHALL display `ChallengeListView` with the full challenge list

---
### Requirement: HomeView displays latest tutorial articles

The 最新教學 section of `HomeView.vue` SHALL display the 3 most recently created tutor section articles (where `isIndex === false`), sorted by `createdTime` in descending order.

Each article SHALL be rendered as a card showing: `title`, `description`, `subject`, `section`, and a link to the article URL.

#### Scenario: Three most recent articles shown

- **WHEN** 5 tutor articles exist with different `createdTime` values
- **THEN** the 最新教學 section SHALL display exactly the 3 articles with the most recent `createdTime`

#### Scenario: No tutor articles

- **WHEN** no tutor articles exist (`tutor.data` returns an empty array)
- **THEN** the 最新教學 section SHALL render an empty state message instead of throwing an error

---
### Requirement: HomeView displays tutorials grouped by chapter

The 分類教學 section of `HomeView.vue` SHALL display all tutor section articles (where `isIndex === false`) grouped by `subject` and then by `chapter`, sorted by `chapter` ascending within each subject.

#### Scenario: Articles grouped by subject and chapter

- **WHEN** tutor articles exist across subjects `py` (chapters 1–4) and `alg` (chapter 1)
- **THEN** the 分類教學 section SHALL show a group for `py` with chapters 1–4 and a group for `alg` with chapter 1, each listing the articles within that chapter

#### Scenario: Empty subject group is hidden

- **WHEN** `docs/tutor/alg/` contains no section articles
- **THEN** the `alg` group SHALL NOT appear in the 分類教學 section

---
### Requirement: HomeView displays latest challenges

The 最新挑戰 section of `HomeView.vue` SHALL display the 3 challenges with the highest `id` values, sorted by `id` in descending order.

Each challenge SHALL be rendered as a card showing: `title`, `difficulty`, and a link to the challenge page.

#### Scenario: Three highest-id challenges shown

- **WHEN** 10 challenges exist with ids 1–10
- **THEN** the 最新挑戰 section SHALL display challenges with ids 10, 9, and 8

#### Scenario: No challenges exist

- **WHEN** the challenges array is empty
- **THEN** the 最新挑戰 section SHALL render an empty state message instead of throwing an error