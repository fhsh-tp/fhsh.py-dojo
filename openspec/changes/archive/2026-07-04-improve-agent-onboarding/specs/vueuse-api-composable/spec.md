## REMOVED Requirements

### Requirement: useApi composable provides useFetch wrapper

**Reason**: The `useApi` / `useWsApi` composables have no callers anywhere in the theme or docs source; they are fork-legacy scaffolding exercised only by their own test. Removing dead code reduces maintenance surface and eliminates a misleading API for future agents.

**Migration**: No migration is required because no component imports `useApi`. Any future HTTP need SHALL call `@vueuse/core`'s `useFetch` directly; the removed wrapper added no behavior over it. The implementation can be restored from git history if a real caller emerges.

### Requirement: useApi composable provides useWebSocket wrapper

**Reason**: The `useWsApi` WebSocket wrapper has no callers; the challenge runner communicates through Pyodide and WASM, not WebSockets. It is fork-legacy dead code.

**Migration**: No migration is required because no component imports `useWsApi`. Any future WebSocket need SHALL call `@vueuse/core`'s `useWebSocket` directly. The implementation can be restored from git history if required.

### Requirement: useApi composable is exported from theme composables index

**Reason**: With `useApi` and `useWsApi` removed, the barrel re-export in `.vitepress/theme/composables/index.ts` no longer has anything to export and is deleted alongside the composable.

**Migration**: No migration is required; the barrel continues to export the remaining composables (`useChallengeRunner`, `useExecutor`, `useWasm`) unchanged. Only the `useApi` / `useWsApi` named exports are removed.
