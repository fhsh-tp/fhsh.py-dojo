# Spec: challenge-dual-theme

## Purpose

Defines the dual-theme (dark/light mode) requirements for the FHSH Python 自學道場（台北市立復興高級中學 Python 自學道場）site. Dark mode follows a Matrix Terminal aesthetic; light mode follows a SOC/SIEM aesthetic. Theme state is controlled by VitePress and persisted to localStorage.

---

### Requirement: Tailwind dark variant targets VitePress dark class

The system SHALL configure Tailwind CSS 4's dark mode variant to target the `.dark` class on the `<html>` element (as set by VitePress) rather than the `prefers-color-scheme` media query.

#### Scenario: Dark variant activates via html.dark class

- **WHEN** VitePress sets the `.dark` class on the `<html>` element
- **THEN** all Tailwind `dark:` prefixed classes SHALL be applied to descendant elements

#### Scenario: Dark variant does not activate from media query alone

- **WHEN** the OS is in dark mode but VitePress has not set `.dark` on `<html>`
- **THEN** `dark:` prefixed Tailwind classes SHALL NOT be applied


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: AppHeader provides a dark/light mode toggle

The `AppHeader` component SHALL include a toggle button that switches between dark and light mode, synchronizing with VitePress's theme state.

#### Scenario: Toggle switches to light mode

- **WHEN** the current mode is dark and the user clicks the toggle button
- **THEN** the theme SHALL switch to light mode, the `.dark` class SHALL be removed from `<html>`, and the preference SHALL be persisted to localStorage

#### Scenario: Toggle switches to dark mode

- **WHEN** the current mode is light and the user clicks the toggle button
- **THEN** the theme SHALL switch to dark mode, the `.dark` class SHALL be added to `<html>`, and the preference SHALL be persisted to localStorage

#### Scenario: Toggle reflects current mode

- **WHEN** the page loads in dark mode
- **THEN** the toggle button SHALL display a sun icon (indicating "switch to light")

#### Scenario: Toggle reflects light mode on load

- **WHEN** the page loads in light mode
- **THEN** the toggle button SHALL display a moon icon (indicating "switch to dark")


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: ChallengeCard applies dual-theme styles

The `ChallengeCard` component SHALL apply dark mode styles (Matrix Terminal aesthetic) via `dark:` prefixed classes and light mode styles (SOC/SIEM aesthetic) as base classes.

#### Scenario: Dark mode card appearance

- **WHEN** dark mode is active
- **THEN** the card SHALL have a near-black background, dark border, and on hover SHALL display an emerald border with a neon glow shadow (`box-shadow` with emerald color)

#### Scenario: Light mode card appearance

- **WHEN** light mode is active
- **THEN** the card SHALL have a white background, a blue-200 border, and on hover SHALL display a blue-500 border with a blue-tinted shadow

#### Scenario: Difficulty badge colors adapt to theme

- **WHEN** dark mode is active
- **THEN** difficulty badges SHALL use dark semi-transparent backgrounds (e.g., `bg-green-900/60`, `bg-yellow-900/60`, `bg-red-900/60`)

#### Scenario: Difficulty badge colors in light mode

- **WHEN** light mode is active
- **THEN** difficulty badges SHALL use bright saturated backgrounds (e.g., `bg-green-100 text-green-700`, `bg-yellow-100 text-yellow-700`, `bg-red-100 text-red-700`)


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: ChallengeListView filter buttons apply dual-theme styles

The filter buttons in `ChallengeListView` SHALL apply dual-theme styles: emerald active state in dark mode, blue active state in light mode.

#### Scenario: Dark mode active filter

- **WHEN** dark mode is active and a filter button is selected
- **THEN** the active button SHALL have an emerald background with neon glow

#### Scenario: Light mode active filter

- **WHEN** light mode is active and a filter button is selected
- **THEN** the active button SHALL have a blue-600 (`#1D4ED8`) background with white text


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: ChallengeView root container applies dual-theme background

The `ChallengeView` root container SHALL use a near-black background in dark mode and a light ice-blue background in light mode.

#### Scenario: Dark mode background

- **WHEN** dark mode is active
- **THEN** the ChallengeView root SHALL apply `bg-gray-950` (current dark background)

#### Scenario: Light mode background

- **WHEN** light mode is active
- **THEN** the ChallengeView root SHALL apply a light background (`bg-slate-50` or equivalent)


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: AppHeader applies dual-theme styles

The `AppHeader` SHALL use a dark border-bottom in dark mode and a deep navy blue background in light mode to reinforce the SOC/SIEM aesthetic.

#### Scenario: Dark mode header

- **WHEN** dark mode is active
- **THEN** the header SHALL have a dark border-bottom (`border-gray-800`) with transparent/dark background

#### Scenario: Light mode header

- **WHEN** light mode is active
- **THEN** the header SHALL display a deep navy blue background (`bg-blue-900` or equivalent) with light-colored text


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: ProblemPanel prose mode adapts to theme

The `ProblemPanel` SHALL use `prose-invert` in dark mode and standard `prose` in light mode.

#### Scenario: Dark mode prose

- **WHEN** dark mode is active
- **THEN** the `ProblemPanel` SHALL apply the `prose-invert` Tailwind Typography class

#### Scenario: Light mode prose

- **WHEN** light mode is active
- **THEN** the `ProblemPanel` SHALL apply the standard `prose` class without inversion


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

---

### Requirement: TestResultPanel and RunButton apply dual-theme styles

`TestResultPanel` and `RunButton` SHALL apply light mode base styles with `dark:` prefixed overrides for dark mode, ensuring all interactive states are legible in both themes.

#### Scenario: TestResultPanel dark mode

- **WHEN** dark mode is active
- **THEN** the result table, borders, and text SHALL use the existing dark palette (`border-gray-800`, `bg-gray-900`, `text-gray-400` etc.)

#### Scenario: TestResultPanel light mode

- **WHEN** light mode is active
- **THEN** the result table SHALL use white/light backgrounds with blue-tinted borders and dark readable text

#### Scenario: RunButton light mode

- **WHEN** light mode is active and the button is in the ready state
- **THEN** the Run button SHALL remain visually prominent (emerald or blue) with sufficient contrast against the light background

## Requirements


<!-- @trace
source: dark-light-mode-theming
updated: 2026-03-16
code:
  - .vitepress/theme/views/ChallengeListView.vue
  - .vitepress/theme/components/editor/TestResultPanel.vue
  - .vitepress/theme/tailwind.css
  - .vitepress/theme/views/ChallengeView.vue
  - .vitepress/theme/components/editor/RunButton.vue
  - .vitepress/theme/components/layout/SplitPane.vue
  - .vitepress/theme/components/challenge/SkeletonChallengeCard.vue
  - .vitepress/theme/components/challenge/ProblemPanel.vue
  - .vitepress/theme/components/layout/AppHeader.vue
  - .vitepress/theme/components/challenge/ChallengeCard.vue
tests:
  - .vitepress/theme/__tests__/TestResultPanel.spec.ts
  - .vitepress/theme/__tests__/RunButton.spec.ts
  - .vitepress/theme/__tests__/ChallengeCard.spec.ts
  - .vitepress/theme/__tests__/ChallengeListView.spec.ts
  - .vitepress/theme/__tests__/AppHeader.spec.ts
  - .vitepress/theme/__tests__/ProblemPanel.spec.ts
-->

### Requirement: Tailwind dark variant targets VitePress dark class

The system SHALL configure Tailwind CSS 4's dark mode variant to target the `.dark` class on the `<html>` element (as set by VitePress) rather than the `prefers-color-scheme` media query.

#### Scenario: Dark variant activates via html.dark class

- **WHEN** VitePress sets the `.dark` class on the `<html>` element
- **THEN** all Tailwind `dark:` prefixed classes SHALL be applied to descendant elements

#### Scenario: Dark variant does not activate from media query alone

- **WHEN** the OS is in dark mode but VitePress has not set `.dark` on `<html>`
- **THEN** `dark:` prefixed Tailwind classes SHALL NOT be applied

---
### Requirement: AppHeader provides a dark/light mode toggle

The `AppHeader` component SHALL include a toggle button that switches between dark and light mode, synchronizing with VitePress's theme state.

#### Scenario: Toggle switches to light mode

- **WHEN** the current mode is dark and the user clicks the toggle button
- **THEN** the theme SHALL switch to light mode, the `.dark` class SHALL be removed from `<html>`, and the preference SHALL be persisted to localStorage

#### Scenario: Toggle switches to dark mode

- **WHEN** the current mode is light and the user clicks the toggle button
- **THEN** the theme SHALL switch to dark mode, the `.dark` class SHALL be added to `<html>`, and the preference SHALL be persisted to localStorage

#### Scenario: Toggle reflects current mode

- **WHEN** the page loads in dark mode
- **THEN** the toggle button SHALL display a sun icon (indicating "switch to light")

#### Scenario: Toggle reflects light mode on load

- **WHEN** the page loads in light mode
- **THEN** the toggle button SHALL display a moon icon (indicating "switch to dark")

---
### Requirement: ChallengeCard applies dual-theme styles

The `ChallengeCard` component SHALL apply dark mode styles (Matrix Terminal aesthetic) via `dark:` prefixed classes and light mode styles (SOC/SIEM aesthetic) as base classes.

#### Scenario: Dark mode card appearance

- **WHEN** dark mode is active
- **THEN** the card SHALL have a near-black background, dark border, and on hover SHALL display an emerald border with a neon glow shadow (`box-shadow` with emerald color)

#### Scenario: Light mode card appearance

- **WHEN** light mode is active
- **THEN** the card SHALL have a white background, a blue-200 border, and on hover SHALL display a blue-500 border with a blue-tinted shadow

#### Scenario: Difficulty badge colors adapt to theme

- **WHEN** dark mode is active
- **THEN** difficulty badges SHALL use dark semi-transparent backgrounds (e.g., `bg-green-900/60`, `bg-yellow-900/60`, `bg-red-900/60`)

#### Scenario: Difficulty badge colors in light mode

- **WHEN** light mode is active
- **THEN** difficulty badges SHALL use bright saturated backgrounds (e.g., `bg-green-100 text-green-700`, `bg-yellow-100 text-yellow-700`, `bg-red-100 text-red-700`)

---
### Requirement: ChallengeListView filter buttons apply dual-theme styles

The filter buttons in `ChallengeListView` SHALL apply dual-theme styles: emerald active state in dark mode, blue active state in light mode.

#### Scenario: Dark mode active filter

- **WHEN** dark mode is active and a filter button is selected
- **THEN** the active button SHALL have an emerald background with neon glow

#### Scenario: Light mode active filter

- **WHEN** light mode is active and a filter button is selected
- **THEN** the active button SHALL have a blue-600 (`#1D4ED8`) background with white text

---
### Requirement: ChallengeView root container applies dual-theme background

The `ChallengeView` root container SHALL use a near-black background in dark mode and a light ice-blue background in light mode.

#### Scenario: Dark mode background

- **WHEN** dark mode is active
- **THEN** the ChallengeView root SHALL apply `bg-gray-950` (current dark background)

#### Scenario: Light mode background

- **WHEN** light mode is active
- **THEN** the ChallengeView root SHALL apply a light background (`bg-slate-50` or equivalent)

---
### Requirement: AppHeader applies dual-theme styles

The `AppHeader` SHALL use a dark border-bottom in dark mode and a deep navy blue background in light mode to reinforce the SOC/SIEM aesthetic.

#### Scenario: Dark mode header

- **WHEN** dark mode is active
- **THEN** the header SHALL have a dark border-bottom (`border-gray-800`) with transparent/dark background

#### Scenario: Light mode header

- **WHEN** light mode is active
- **THEN** the header SHALL display a deep navy blue background (`bg-blue-900` or equivalent) with light-colored text

---
### Requirement: ProblemPanel prose mode adapts to theme

The `ProblemPanel` SHALL use `prose-invert` in dark mode and standard `prose` in light mode.

#### Scenario: Dark mode prose

- **WHEN** dark mode is active
- **THEN** the `ProblemPanel` SHALL apply the `prose-invert` Tailwind Typography class

#### Scenario: Light mode prose

- **WHEN** light mode is active
- **THEN** the `ProblemPanel` SHALL apply the standard `prose` class without inversion

---
### Requirement: TestResultPanel and RunButton apply dual-theme styles

`TestResultPanel` and `RunButton` SHALL apply light mode base styles with `dark:` prefixed overrides for dark mode, ensuring all interactive states are legible in both themes.

#### Scenario: TestResultPanel dark mode

- **WHEN** dark mode is active
- **THEN** the result table, borders, and text SHALL use the existing dark palette (`border-gray-800`, `bg-gray-900`, `text-gray-400` etc.)

#### Scenario: TestResultPanel light mode

- **WHEN** light mode is active
- **THEN** the result table SHALL use white/light backgrounds with blue-tinted borders and dark readable text

#### Scenario: RunButton light mode

- **WHEN** light mode is active and the button is in the ready state
- **THEN** the Run button SHALL remain visually prominent (emerald or blue) with sufficient contrast against the light background