## ADDED Requirements

### Requirement: Chapter 1 appendix image specifications use ordered lists

The `docs/tutor/py/ch1/appendix.md` file's "Image Specification Appendix" section SHALL format each image's property entries as an ordered list using standard Markdown numbered syntax (`1. 2. 3. 4.`), not as unordered bullet lists.

Each image entry SHALL contain exactly four ordered items in the following fixed sequence:
1. **類型**：image type and narrative role (e.g., 四格漫畫（Hook）)
2. **意圖**：teaching intent — what concept this image reinforces
3. **完整 Prompt**：the full English AI generation prompt
4. **備註**：production notes for rendering or composition

This ordered list format SHALL be compatible with standard Markdown as rendered by both VitePress and Slidev (no Slidev-specific extensions required; plain `1. 2. 3. 4.` syntax is sufficient).

#### Scenario: Image specification entries render as numbered list

- **WHEN** a user visits `docs/tutor/py/ch1/appendix.md` in the browser
- **THEN** each image's property block (類型, 意圖, 完整 Prompt, 備註) MUST be rendered as a numbered ordered list with items 1 through 4

#### Scenario: Ordered list is valid Slidev-compatible Markdown

- **WHEN** the appendix content is imported into a Slidev presentation file
- **THEN** the ordered list SHALL render correctly without requiring any Slidev-specific syntax, because standard Markdown `1. Item` numbered lists are natively supported by Slidev
