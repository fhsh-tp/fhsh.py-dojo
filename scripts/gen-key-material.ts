#!/usr/bin/env npx tsx
/**
 * Standalone key-material generator.
 *
 * Writes `testcase-generator/src/key_material.rs` (gitignored, embedded by the
 * WASM crate) WITHOUT running the full `build:pools` pipeline. CI uses this
 * before `cargo test`, because the Rust crate has an unconditional
 * `mod key_material;` and therefore fails to compile on a clean checkout where
 * that file has never been committed. The generated key is ephemeral and only
 * needs to exist for the crate to compile; the unit tests do not depend on its
 * value.
 */
import { resolve } from 'node:path'

import { getPoolKey } from './pool-key.js'
import { generateKeyMaterial } from './generate-key-material.js'

const root = resolve(import.meta.dirname, '..')
generateKeyMaterial(getPoolKey(root), root)
console.log('[gen-key-material] wrote testcase-generator/src/key_material.rs')
