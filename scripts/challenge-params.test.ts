// @vitest-environment node
/**
 * All-challenge params conformance gate.
 *
 * Every `docs/challenge/*.md` params declaration MUST be accepted by the
 * Rust/WASM engine parser and pass its input-size budget. This replaces the
 * retired generator-parity test as the guard against content-side drift:
 * a challenge declaring a type or field the engine does not support fails
 * HERE, naming the file — instead of silently shipping a degraded pool
 * (the `type: str` → literal "UNKNOWN_TYPE" incident on challenge id 22).
 *
 * Deliberately NO skip guards: a missing WASM artifact or an empty
 * challenge directory is a failure, not a skip — a gate that silently
 * skips is not a gate. The build pipeline (gen:keymaterial → build:wasm →
 * build:pools → test) guarantees the artifact exists in CI.
 */
import { readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { describe, expect, it } from 'vitest'

import { readChallenge } from './generate-pools.js'
import { ensureWasmArtifact, generatePoolInputs } from './wasm-input-generator.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')

describe('challenge params conformance', () => {
  it('WASM artifact is present (run `pnpm build:wasm` if this fails)', () => {
    expect(() => ensureWasmArtifact()).not.toThrow()
  })

  const files = readdirSync(CHALLENGES_DIR).filter((f) => f.endsWith('.md'))

  it('at least one challenge file exists', () => {
    expect(files.length).toBeGreaterThan(0)
  })

  it.each(files)('%s: params parse and fit the input budget', async (file) => {
    const challenge = readChallenge(join(CHALLENGES_DIR, file))
    // One generated sample proves the declaration parses, passes budget
    // enforcement, and actually renders. Seeded for reproducible failures.
    const inputs = await generatePoolInputs(
      {
        params: challenge.params,
        seed: challenge.slug,
        input_budget: challenge.input_budget,
      },
      1,
    )
    expect(inputs).toHaveLength(1)
    expect(typeof inputs[0]).toBe('string')
  })
})
