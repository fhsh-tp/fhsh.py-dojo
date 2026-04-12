## ADDED Requirements

### Requirement: Section 1-3 uses Mermaid flowchart for leap year logic

Section `1-3.md` SHALL use a Mermaid `flowchart TD` diagram to illustrate the leap year decision logic, replacing the existing ASCII art flowchart. The Mermaid diagram SHALL preserve the same logical structure: three sequential divisibility checks (400, 100, 4) with Yes/No branches leading to 閏年 or 平年 outcomes. The diagram SHALL include a custom Mermaid theme configuration for consistent visual styling.

#### Scenario: Leap year flowchart renders as Mermaid SVG

- **WHEN** a reader views section 1-3 in the browser
- **AND** the page reaches the flowchart section
- **THEN** the leap year decision logic SHALL be displayed as a rendered Mermaid flowchart SVG
- **AND** no ASCII art code block SHALL be present for this diagram

#### Scenario: Flowchart preserves correct decision logic

- **WHEN** the Mermaid flowchart is inspected
- **THEN** it SHALL contain three diamond-shaped decision nodes for `year % 400 == 0`, `year % 100 == 0`, and `year % 4 == 0`
- **AND** each decision node SHALL have Yes and No branches
- **AND** the terminal nodes SHALL display 閏年 or 平年

### Requirement: Section 1-4 uses Mermaid mindmap for knowledge map

Section `1-4.md` SHALL use a Mermaid `mindmap` diagram to illustrate the Module 1 knowledge map, replacing the existing ASCII art tree. The Mermaid diagram SHALL preserve the same hierarchical structure: root node 程式語言（Python） branching into three sections (1-1 I/O 基礎, 1-2 資料與運算, 1-3 流程控制) with their respective skill nodes.

#### Scenario: Knowledge map renders as Mermaid SVG

- **WHEN** a reader views section 1-4 in the browser
- **AND** the page reaches the knowledge map section
- **THEN** the Module 1 knowledge map SHALL be displayed as a rendered Mermaid mindmap SVG
- **AND** no ASCII art code block SHALL be present for this diagram

#### Scenario: Mindmap preserves all skill nodes

- **WHEN** the Mermaid mindmap is inspected
- **THEN** it SHALL contain a root node for 程式語言（Python）
- **AND** it SHALL contain three branch nodes for the three sections
- **AND** each branch SHALL list the same skill items as the original ASCII tree
