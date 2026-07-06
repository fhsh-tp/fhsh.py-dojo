/**
 * Vitest global setup: jsdom provides no IndexedDB, so install an in-memory
 * fake so persistence-layer tests can run. Tests that need isolation stub a
 * fresh `IDBFactory` per case (see persistence/db.spec.ts).
 */
import 'fake-indexeddb/auto'
