/**
 * Pool encryption key management.
 *
 * Reads the 256-bit AES-GCM key from `.env.pool` (hex string).
 * If the file does not exist, generates a new random key and writes it.
 */
import { randomBytes } from 'node:crypto'
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

const KEY_BYTES = 32 // AES-256
const ENV_FILE = '.env.pool'

/** Resolve `.env.pool` relative to project root. */
function envPath(root: string): string {
  return resolve(root, ENV_FILE)
}

/**
 * Read the pool encryption key (returns 32-byte Buffer).
 *
 * Key creation is opt-in (`create: true`, used only by gen-key-material,
 * the first step of the build chain). Every other caller — build:pools in
 * particular — fails loudly when `.env.pool` is missing: silently minting
 * a fresh key mid-chain would encrypt pools with a key the already-built
 * WASM does not hold, and the mismatch would only surface in students'
 * browsers.
 */
export function getPoolKey(projectRoot: string, opts: { create?: boolean } = {}): Buffer {
  const p = envPath(projectRoot)

  if (existsSync(p)) {
    const hex = readFileSync(p, 'utf-8').trim()
    if (!/^[0-9a-f]{64}$/i.test(hex)) {
      throw new Error(`.env.pool must contain a 64-char hex string, got ${hex.length} chars`)
    }
    return Buffer.from(hex, 'hex')
  }

  if (!opts.create) {
    throw new Error(
      `.env.pool not found at ${p}. The key must exist BEFORE the WASM is built ` +
        '(the compiled WASM embeds it). Run: pnpm gen:keymaterial && pnpm build:wasm',
    )
  }

  // First build: generate a random key
  const key = randomBytes(KEY_BYTES)
  writeFileSync(p, key.toString('hex') + '\n', 'utf-8')
  console.log(`[pool-key] Generated new pool encryption key → ${p}`)
  return key
}
