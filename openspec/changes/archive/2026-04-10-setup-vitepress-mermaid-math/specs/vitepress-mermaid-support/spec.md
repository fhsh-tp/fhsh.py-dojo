## ADDED Requirements

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

### Requirement: Mermaid plugin is registered via withMermaid wrapper

The VitePress configuration in `.vitepress/config.mts` SHALL use the `withMermaid()` wrapper from `vitepress-plugin-mermaid` to register the Mermaid rendering plugin.

#### Scenario: Config uses withMermaid wrapper

- **WHEN** `.vitepress/config.mts` is inspected
- **THEN** the default export SHALL be wrapped with `withMermaid()` from `vitepress-plugin-mermaid`

### Requirement: Mermaid packages are installed as devDependencies

The `package.json` SHALL list `vitepress-plugin-mermaid` and `mermaid` as `devDependencies`.

#### Scenario: Packages present in devDependencies

- **WHEN** `package.json` is inspected
- **THEN** `devDependencies` SHALL contain `vitepress-plugin-mermaid` and `mermaid`
