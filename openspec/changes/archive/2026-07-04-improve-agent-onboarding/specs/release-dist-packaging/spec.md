## MODIFIED Requirements

### Requirement: Dist packaging in dual formats

The workflow SHALL package the contents of `.vitepress/dist/` into a `.tar.gz` archive.
The workflow SHALL package the contents of `.vitepress/dist/` into a `.zip` archive.
The archive filenames SHALL follow the pattern `fhsh-py-dojo-{tag}.tar.gz` and `fhsh-py-dojo-{tag}.zip` where `{tag}` is the git tag name (e.g., `v1.0.0`).
The archives SHALL contain the dist contents directly at the root level (not nested under a `dist/` directory).

#### Scenario: Archive contents

- **WHEN** a user extracts `fhsh-py-dojo-v1.0.0.tar.gz`
- **THEN** the extracted directory SHALL contain `index.html`, `assets/`, `wasm/`, and all other build outputs at the top level

### Requirement: Asset upload to GitHub Release

The workflow SHALL upload both `.tar.gz` and `.zip` archives to the GitHub Release as downloadable assets.
The workflow SHALL use `softprops/action-gh-release` for upload.
The workflow SHALL overwrite existing assets with the same filename if the workflow is re-run.
The workflow SHALL create a new release if one does not exist for the tag (push tag scenario).
The workflow SHALL update the existing release if one already exists (UI release scenario).

#### Scenario: Assets visible on release page

- **WHEN** the workflow completes successfully
- **THEN** the GitHub Release page SHALL display both `fhsh-py-dojo-{tag}.tar.gz` and `fhsh-py-dojo-{tag}.zip` as downloadable assets

#### Scenario: Workflow re-run

- **WHEN** the workflow is re-run for the same tag
- **THEN** the existing assets SHALL be overwritten with freshly built archives
