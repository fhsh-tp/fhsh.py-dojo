## MODIFIED Requirements

### Requirement: Mermaid plugin is registered via withMermaid wrapper

The VitePress configuration in `.vitepress/config.mts` SHALL use a custom markdown-it plugin registered via the `markdown.config` callback to transform Mermaid fenced code blocks into `<MermaidDiagram>` Vue component invocations. The `MermaidDiagram` component SHALL be registered as a global component in the theme's `enhanceApp` function. The configuration SHALL NOT use `withMermaid()` from `vitepress-plugin-mermaid`.

#### Scenario: Config uses markdown.config with mermaid plugin

- **WHEN** `.vitepress/config.mts` is inspected
- **THEN** the `markdown.config` callback SHALL invoke a custom mermaid markdown-it plugin
- **AND** the default export SHALL NOT use `withMermaid()` from `vitepress-plugin-mermaid`

#### Scenario: MermaidDiagram component is registered globally

- **WHEN** `.vitepress/theme/index.ts` is inspected
- **THEN** the `enhanceApp` function SHALL register `MermaidDiagram` as a global component via `app.component('MermaidDiagram', MermaidDiagram)`

### Requirement: Mermaid packages are installed as devDependencies

The `package.json` SHALL list `mermaid` as a `devDependency`. The `vitepress-plugin-mermaid` package SHALL NOT be present in `package.json`.

#### Scenario: mermaid present and vitepress-plugin-mermaid absent

- **WHEN** `package.json` is inspected
- **THEN** `devDependencies` SHALL contain `mermaid`
- **AND** `devDependencies` SHALL NOT contain `vitepress-plugin-mermaid`
- **AND** `dependencies` SHALL NOT contain `vitepress-plugin-mermaid`

### Requirement: Mermaid code blocks render as SVG diagrams

Markdown files containing fenced code blocks with the `mermaid` language identifier SHALL be rendered as interactive SVG diagrams in both the VitePress dev server and the production build output.

#### Scenario: Flowchart renders in dev server

- **WHEN** a Markdown file contains a fenced code block with language `mermaid` and valid flowchart syntax
- **THEN** the VitePress dev server SHALL display the code block as a rendered SVG flowchart diagram
- **AND** the raw Mermaid source text SHALL NOT be visible to the user

#### Scenario: Mindmap renders in production build

- **WHEN** the VitePress site is built with `vitepress build`
- **AND** a Markdown file contains a fenced code block with language `mermaid` and valid mindmap syntax
- **THEN** the generated HTML SHALL contain a rendered SVG mindmap diagram

#### Scenario: Invalid Mermaid syntax shows error gracefully

- **WHEN** a Markdown file contains a fenced code block with language `mermaid` and invalid syntax
- **THEN** the page SHALL NOT crash
- **AND** an error indicator SHALL be displayed in place of the diagram

#### Scenario: Mermaid loads only in browser context

- **WHEN** VitePress performs server-side rendering or static site generation
- **THEN** the mermaid library SHALL NOT be imported or evaluated
- **AND** no TypeError or initialization error SHALL occur

#### Scenario: Dark mode toggle re-renders diagrams

- **WHEN** a page contains a rendered Mermaid diagram
- **AND** the user toggles between dark and light mode
- **THEN** the diagram SHALL re-render with the appropriate theme (`dark` or `default`)

