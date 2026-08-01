## ADDED Requirements

### Requirement: Build-time verdict_detail whitelist

`readChallenge` SHALL validate that `verdict_detail`, when declared, is one of `hidden`, `actual`, or `full`, and SHALL throw an error naming the file and the allowed values otherwise. An absent field SHALL keep defaulting to `hidden`.

#### Scenario: typo fails the build

- **WHEN** a challenge declares `verdict_detail: ful`
- **THEN** the pool build fails with an error naming the file and listing the allowed values

#### Scenario: absent field defaults

- **WHEN** a challenge declares no `verdict_detail`
- **THEN** the pool is built with `hidden`
