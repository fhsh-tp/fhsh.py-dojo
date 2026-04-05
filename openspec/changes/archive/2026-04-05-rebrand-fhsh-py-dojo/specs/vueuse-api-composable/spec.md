## ADDED Requirements

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

---

### Requirement: useApi composable provides useWebSocket wrapper

The `.vitepress/theme/composables/useApi.ts` file SHALL export a `useWsApi` function that wraps `@vueuse/core`'s `useWebSocket`. The wrapper SHALL accept a `url` parameter and an optional `options` parameter compatible with VueUse `UseWebSocketOptions`. The wrapper SHALL return the full `UseWebSocketReturn` object without modification.

#### Scenario: WebSocket connection via useWsApi

- **WHEN** a component calls `useWsApi('wss://example.com/ws')`
- **THEN** it SHALL receive a reactive `UseWebSocketReturn` object with `data`, `status`, `send`, and `close` properties

#### Scenario: WebSocket options are forwarded

- **WHEN** a component calls `useWsApi(url, { autoReconnect: true, heartbeat: true })`
- **THEN** the underlying `useWebSocket` call SHALL receive the same `autoReconnect` and `heartbeat` options

---

### Requirement: useApi composable is exported from theme composables index

The `.vitepress/theme/composables/index.ts` (or equivalent barrel export) SHALL export `useApi` and `useWsApi` so they are accessible as `@/composables`.

#### Scenario: Named export is accessible

- **WHEN** a Vue component imports `{ useApi, useWsApi }` from `@/composables`
- **THEN** both functions SHALL be available and callable
