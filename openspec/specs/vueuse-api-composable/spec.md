# vueuse-api-composable Specification

## Purpose

Defines the `useApi` composable that wraps VueUse's `useFetch` and `useWebSocket` primitives, providing a unified reactive API abstraction for HTTP and WebSocket communication within the VitePress theme.

## Requirements

### Requirement: useApi composable provides useFetch wrapper

The `.vitepress/theme/composables/useApi.ts` file SHALL export a `useApi` function that wraps `@vueuse/core`'s `useFetch`. The wrapper SHALL accept a `url` parameter and an optional `options` parameter compatible with VueUse `UseFetchOptions`. The wrapper SHALL return the full `UseFetchReturn` object without modification.

#### Scenario: HTTP GET request via useApi

- **WHEN** a component calls `useApi('https://example.com/api/data')`
- **THEN** it SHALL receive a reactive `UseFetchReturn` object with `data`, `error`, `isFetching`, and `execute` properties

#### Scenario: Custom options are forwarded

- **WHEN** a component calls `useApi(url, { method: 'POST', body: payload })`
- **THEN** the underlying `useFetch` call SHALL receive the same `method` and `body` options

#### Scenario: @vueuse/core is listed as a dependency

- **WHEN** `package.json` is read
- **THEN** `@vueuse/core` SHALL be listed in `dependencies`


<!-- @trace
source: rebrand-fhsh-py-dojo
updated: 2026-04-05
code:
  - docs/challenge/caesar-advanced.md
  - .vitepress/theme/composables/useApi.ts
  - LICENSE
  - docs/challenge/rsa-basic.md
  - docs/challenge/rail-fence-encrypt.md
  - Usage.md
  - docs/challenge/caesar-custom-table.md
  - .vitepress/config.mts
  - docs/index.md
  - CHANGELOG.md
  - .vitepress/theme/composables/index.ts
  - docs/challenge/enigma-simplified.md
  - docs/challenge/caesar-basic.md
  - README.md
  - docs/challenge/vigenere-encrypt.md
  - requirements.txt
  - package.json
  - docs/challenge/des-ecb-cbc.md
tests:
  - .vitepress/theme/__tests__/useApi.spec.ts
-->

---
### Requirement: useApi composable provides useWebSocket wrapper

The `.vitepress/theme/composables/useApi.ts` file SHALL export a `useWsApi` function that wraps `@vueuse/core`'s `useWebSocket`. The wrapper SHALL accept a `url` parameter and an optional `options` parameter compatible with VueUse `UseWebSocketOptions`. The wrapper SHALL return the full `UseWebSocketReturn` object without modification.

#### Scenario: WebSocket connection via useWsApi

- **WHEN** a component calls `useWsApi('wss://example.com/ws')`
- **THEN** it SHALL receive a reactive `UseWebSocketReturn` object with `data`, `status`, `send`, and `close` properties

#### Scenario: WebSocket options are forwarded

- **WHEN** a component calls `useWsApi(url, { autoReconnect: true, heartbeat: true })`
- **THEN** the underlying `useWebSocket` call SHALL receive the same `autoReconnect` and `heartbeat` options


<!-- @trace
source: rebrand-fhsh-py-dojo
updated: 2026-04-05
code:
  - docs/challenge/caesar-advanced.md
  - .vitepress/theme/composables/useApi.ts
  - LICENSE
  - docs/challenge/rsa-basic.md
  - docs/challenge/rail-fence-encrypt.md
  - Usage.md
  - docs/challenge/caesar-custom-table.md
  - .vitepress/config.mts
  - docs/index.md
  - CHANGELOG.md
  - .vitepress/theme/composables/index.ts
  - docs/challenge/enigma-simplified.md
  - docs/challenge/caesar-basic.md
  - README.md
  - docs/challenge/vigenere-encrypt.md
  - requirements.txt
  - package.json
  - docs/challenge/des-ecb-cbc.md
tests:
  - .vitepress/theme/__tests__/useApi.spec.ts
-->

---
### Requirement: useApi composable is exported from theme composables index

The `.vitepress/theme/composables/index.ts` (or equivalent barrel export) SHALL export `useApi` and `useWsApi` so they are accessible as `@/composables`.

#### Scenario: Named export is accessible

- **WHEN** a Vue component imports `{ useApi, useWsApi }` from `@/composables`
- **THEN** both functions SHALL be available and callable

<!-- @trace
source: rebrand-fhsh-py-dojo
updated: 2026-04-05
code:
  - docs/challenge/caesar-advanced.md
  - .vitepress/theme/composables/useApi.ts
  - LICENSE
  - docs/challenge/rsa-basic.md
  - docs/challenge/rail-fence-encrypt.md
  - Usage.md
  - docs/challenge/caesar-custom-table.md
  - .vitepress/config.mts
  - docs/index.md
  - CHANGELOG.md
  - .vitepress/theme/composables/index.ts
  - docs/challenge/enigma-simplified.md
  - docs/challenge/caesar-basic.md
  - README.md
  - docs/challenge/vigenere-encrypt.md
  - requirements.txt
  - package.json
  - docs/challenge/des-ecb-cbc.md
tests:
  - .vitepress/theme/__tests__/useApi.spec.ts
-->