## MODIFIED Requirements

### Requirement: nav.yml defines static top navigation

A YAML file at `.vitepress/nav.yml` SHALL define the VitePress top navigation array. `config.mts` SHALL load this file at build time using `js-yaml` (`yaml.load(fs.readFileSync(…))`) and assign it to `themeConfig.nav`.

The `nav.yml` SHALL define the following structure:

```yaml
- text: 教學
  items:
    - text: Python 自學
      link: /tutor/py/
    - text: 演算法
      link: /tutor/alg/
    - text: 資料結構
      link: /tutor/ds/
- text: Python 挑戰
  link: /challenges
- text: APCS 挑戰
  link: /apcs-challenges
```

The former single `挑戰題庫` entry SHALL be replaced by the two sibling entries `Python 挑戰` (linking to `/challenges`) and `APCS 挑戰` (linking to `/apcs-challenges`), in that order.

#### Scenario: nav.yml is loaded by config.mts

- **WHEN** VitePress builds the site
- **THEN** the top navigation SHALL display the items defined in `.vitepress/nav.yml`

#### Scenario: Both catalogue entries are shown as siblings

- **WHEN** a user views the top navigation on any page
- **THEN** `Python 挑戰` and `APCS 挑戰` SHALL appear as two top-level entries, with `Python 挑戰` before `APCS 挑戰`, and no `挑戰題庫` entry SHALL remain

#### Scenario: nav.yml file is missing

- **WHEN** `.vitepress/nav.yml` does not exist
- **THEN** `config.mts` SHALL fall back to an empty array `[]` without throwing an error
