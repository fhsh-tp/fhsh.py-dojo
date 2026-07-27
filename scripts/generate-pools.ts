#!/usr/bin/env npx tsx
/**
 * Build script: generate encrypted testcase pools for all challenges.
 *
 * 1. Read all docs/challenge/*.md files and parse frontmatter
 * 2. For each challenge, generate random inputs via the Rust/WASM engine
 *    (the same single source of truth the browser uses), seeded by slug
 * 3. Execute generator code via Python subprocess to produce expected outputs
 * 4. Encrypt each pool with AES-256-GCM
 * 5. Write to docs/public/pools/<slug>.bin
 * 6. Generate key_material.rs for WASM embedding
 */
import { execFileSync } from 'node:child_process'
import { createCipheriv, randomBytes } from 'node:crypto'
import {
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from 'node:fs'
import { basename, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

import { getPoolKey } from './pool-key.js'
import { ensureWasmArtifact, generatePoolInputs, type PoolSpec } from './wasm-input-generator.js'

// ── WASM preflight check ──────────────────────────────────────────────────

/**
 * Input generation runs on the Rust/WASM engine (single source of truth
 * with the browser runtime), so the artifact must exist before any
 * challenge is processed. Build order: gen:keymaterial → build:wasm →
 * build:pools.
 */
function preflightCheckWasm(): void {
  try {
    ensureWasmArtifact()
  } catch (err) {
    console.error('[generate-pools] ERROR:', err instanceof Error ? err.message : err)
    process.exit(1)
  }
}

// ── Python preflight check ────────────────────────────────────────────────

function preflightCheckPython(): void {
  // 1. Check python3 is available
  try {
    execFileSync('python3', ['--version'], { encoding: 'utf-8', timeout: 10_000 })
  } catch {
    console.error(
      '[generate-pools] ERROR: python3 is not available.\n' +
        '  Pool generation requires Python 3.10+.\n' +
        '  Please install Python 3 and ensure "python3" is on your PATH.',
    )
    process.exit(1)
  }

  // 2. Check PyYAML is importable
  try {
    execFileSync('python3', ['-c', 'import yaml'], { encoding: 'utf-8', timeout: 10_000 })
  } catch {
    console.error(
      '[generate-pools] ERROR: Python package "PyYAML" is not installed.\n' +
        '  Run: pip install -r requirements.txt',
    )
    process.exit(1)
  }

  // 3. Check pycryptodome is importable (warn only — not all challenges need it)
  try {
    execFileSync('python3', ['-c', 'from Crypto.Cipher import DES'], {
      encoding: 'utf-8',
      timeout: 10_000,
    })
  } catch {
    console.warn(
      '[generate-pools] WARNING: Python package "pycryptodome" is not installed.\n' +
        '  Challenges that require Crypto will fail.\n' +
        '  Run: pip install -r requirements.txt',
    )
  }
}

// ── Constants ──────────────────────────────────────────────────────────────

const PROJECT_ROOT = resolve(import.meta.dirname, '..')
const CHALLENGES_DIR = resolve(PROJECT_ROOT, 'docs/challenge')
const POOLS_DIR = resolve(PROJECT_ROOT, 'docs/public/pools')
export const POOL_SIZE = 200 // testcases per pool
export const MAGIC = Buffer.from('CXPOOL', 'ascii')
export const POOL_VERSION = 0x01

// ── Slug helpers ───────────────────────────────────────────────────────────

const SLUG_PATTERN = /^[a-z0-9-]+$/
const SLUG_MAX_LEN = 64

/**
 * Derive a slug from a challenge markdown file path: the basename with the
 * `.md` extension removed. Returns the full basename unchanged when the file
 * does not end with `.md`; pair with `validateSlug` to reject such cases.
 */
export function deriveSlug(filePath: string): string {
  return basename(filePath, '.md')
}

/**
 * Throw if `slug` is unsafe for use as a pool filename. Rejects empty strings,
 * path separators, parent traversal, characters outside `[a-z0-9-]`, and
 * lengths exceeding `SLUG_MAX_LEN`. Error message always includes `filePath`
 * to aid debugging.
 */
export function validateSlug(slug: string, filePath: string): void {
  if (slug.length === 0) {
    throw new Error(`Invalid slug: empty (from file ${filePath})`)
  }
  if (slug.length > SLUG_MAX_LEN) {
    throw new Error(
      `Invalid slug "${slug}" (from file ${filePath}): exceeds max length ${SLUG_MAX_LEN}`,
    )
  }
  if (slug.includes('/') || slug.includes('\\') || slug.includes('..')) {
    throw new Error(
      `Invalid slug "${slug}" (from file ${filePath}): contains path separator or parent-directory token`,
    )
  }
  if (!SLUG_PATTERN.test(slug)) {
    throw new Error(`Invalid slug "${slug}" (from file ${filePath}): must match ${SLUG_PATTERN}`)
  }
}

/**
 * Build a `slug → fullPath` map for the given list of markdown filenames,
 * rejecting any slug that fails `validateSlug` and any duplicate slug (where
 * two filenames produce the same slug). Throws on the first violation so the
 * caller can surface a single actionable error to CI.
 */
export function collectAndValidateSlugs(
  files: string[],
  challengesDir: string,
): Map<string, string> {
  const seen = new Map<string, string>()
  for (const file of files) {
    const fullPath = join(challengesDir, file)
    if (!file.endsWith('.md')) {
      // Defense in depth: even if `validateSlug`'s allowed-char regex is ever
      // relaxed (e.g. to permit `.`), a non-markdown file SHALL never produce
      // a pool.
      throw new Error(`Challenge file must have .md extension: ${fullPath}`)
    }
    const slug = deriveSlug(fullPath)
    validateSlug(slug, fullPath)
    const prior = seen.get(slug)
    if (prior !== undefined) {
      throw new Error(`Duplicate slug "${slug}" produced by two files: ${prior} and ${fullPath}`)
    }
    seen.set(slug, fullPath)
  }
  return seen
}

/**
 * Remove `*.bin` files in `poolsDir` whose basename (without `.bin`) is not in
 * `validSlugs`. Skips non-`.bin` entries (such as `.gitkeep`) and subdirectories.
 * Returns the list of deleted file names. No-op if `poolsDir` does not exist.
 */
export function cleanupObsoletePools(poolsDir: string, validSlugs: Set<string>): string[] {
  if (!existsSync(poolsDir)) return []
  const deleted: string[] = []
  for (const entry of readdirSync(poolsDir)) {
    if (!entry.endsWith('.bin')) continue
    const full = join(poolsDir, entry)
    if (lstatSync(full).isDirectory()) continue
    const slug = entry.slice(0, -'.bin'.length)
    if (validSlugs.has(slug)) continue
    rmSync(full)
    deleted.push(entry)
  }
  return deleted
}

// ── Frontmatter parsing ────────────────────────────────────────────────────

export interface ChallengeInfo {
  slug: string
  algorithm: string
  generator: string
  params: Record<string, unknown>
  testcase_count?: number
  verdict_detail?: string
  /**
   * Optional per-input worst-case byte budget override (bytes). Passed to
   * the WASM engine, which enforces default 4096 and hard cap 65536.
   */
  input_budget?: number
  /**
   * Optional Python reference solution (a full program that reads stdin and
   * prints the correct answer). Independent of `generator`; used only by the
   * content-layer regression test to verify a known-correct solution earns AC.
   */
  reference_solution?: string
  /**
   * Optional testcase partition plan (band/literal entries). Passed verbatim
   * to the WASM engine, which owns full validation; mutually exclusive with
   * `testcase_count`. When present the pool is built as consecutive blocks
   * and the payload carries `plan_block_size`.
   */
  testcase_plan?: unknown[]
}

const VALID_VERDICT_DETAILS = ['hidden', 'actual', 'full'] as const

/**
 * TS-side mirror of the engine's plan-total rule: Σ band counts + one per
 * literal entry. Used to size the pool request; the engine independently
 * recomputes and enforces the multiple-of-total contract, so any drift
 * between the two fails the build loudly. Entry-shape validation belongs to
 * the engine — this only rejects counts it cannot even sum.
 */
export function computePlanTotal(plan: unknown[], filePath: string): number {
  let total = 0
  for (const entry of plan) {
    const e = entry as Record<string, unknown>
    if (e !== null && typeof e === 'object' && 'literal' in e) {
      total += 1
    } else {
      const c = e?.count
      if (typeof c !== 'number' || !Number.isInteger(c) || c < 1) {
        throw new Error(
          `'testcase_plan' entry has invalid 'count' in ${filePath} (band entries need a positive integer count)`,
        )
      }
      total += c
    }
  }
  if (total < 1) {
    throw new Error(`'testcase_plan' must contain at least one entry in ${filePath}`)
  }
  return total
}

function parseFrontmatter(content: string): Record<string, unknown> {
  const match = content.match(/^---\n([\s\S]*?)\n---/)
  if (!match) throw new Error('No frontmatter found')
  // Simple YAML parser for our known structure — we use a Python helper
  // since we already need Python for generators anyway.
  const yaml = match[1]!
  const result = JSON.parse(
    execFileSync(
      'python3',
      [
        '-c',
        `
import sys, yaml, json
data = yaml.safe_load(sys.stdin.read())
print(json.dumps(data))
`,
      ],
      { input: yaml, encoding: 'utf-8', timeout: 10_000 },
    ),
  )
  return result
}

export function readChallenge(filePath: string): ChallengeInfo {
  const content = readFileSync(filePath, 'utf-8')
  const fm = parseFrontmatter(content)

  const slug = deriveSlug(filePath)
  const algorithm = fm.algorithm as string
  const generator = fm.generator as string
  const params = fm.params as Record<string, unknown>
  const testcase_count = (fm.testcase_count as number) ?? 10
  const verdict_detail = (fm.verdict_detail as string) ?? 'hidden'
  const reference_solution = fm.reference_solution as string | undefined
  const input_budget = fm.input_budget as number | undefined
  const testcase_plan = fm.testcase_plan as unknown[] | undefined

  if (!algorithm) throw new Error(`Missing 'algorithm' in ${filePath}`)
  if (!generator) throw new Error(`Missing 'generator' in ${filePath}`)
  if (!params) throw new Error(`Missing 'params' in ${filePath}`)

  if (input_budget !== undefined && (!Number.isInteger(input_budget) || input_budget < 1)) {
    throw new Error(
      `'input_budget' must be a positive integer in ${filePath} ` +
        `(omit the field to use the default; 0 does not mean "unlimited")`,
    )
  }

  // Mutual exclusion is checked on the RAW frontmatter — `testcase_count`
  // above has already been defaulted, which must not count as a declaration.
  if (testcase_plan !== undefined && fm.testcase_count !== undefined) {
    throw new Error(
      `'testcase_plan' and 'testcase_count' are mutually exclusive in ${filePath} ` +
        `(the plan's band counts already determine the per-session testcase count)`,
    )
  }
  if (testcase_plan !== undefined && !Array.isArray(testcase_plan)) {
    throw new Error(`'testcase_plan' must be a YAML list in ${filePath}`)
  }

  if (
    fm.verdict_detail !== undefined &&
    !VALID_VERDICT_DETAILS.includes(fm.verdict_detail as (typeof VALID_VERDICT_DETAILS)[number])
  ) {
    throw new Error(
      `'verdict_detail' must be one of ${VALID_VERDICT_DETAILS.join(', ')} in ${filePath} ` +
        `(got '${String(fm.verdict_detail)}')`,
    )
  }

  return {
    slug,
    algorithm,
    generator,
    params,
    testcase_count,
    verdict_detail,
    reference_solution,
    input_budget,
    testcase_plan,
  }
}

// ── Input generation via WASM (single source of truth) ────────────────────

/**
 * Generate random inputs with the SAME Rust/WASM engine the browser uses.
 * `seed` (the challenge slug) makes pool content deterministic for
 * identical challenge declarations; `input_budget` (optional frontmatter
 * field) raises the per-input worst-case byte budget up to the engine's
 * hard cap. Engine-side errors (parse validation, budget violations) are
 * thrown to the caller — the build must abort, never continue on a
 * possibly-trapped WASM instance.
 */
export async function generateInputs(spec: PoolSpec, count: number): Promise<string[]> {
  return generatePoolInputs(spec, count)
}

// ── Generator execution ────────────────────────────────────────────────────

export interface TestcaseResult {
  input: string
  expected_output: string
}

export function runGenerator(generatorCode: string, inputs: string[]): TestcaseResult[] {
  // Build a Python script that runs the generator for each input
  const script = `
import json, sys, io

generator_code = ${JSON.stringify(generatorCode)}
inputs = json.loads(sys.stdin.read())

for raw_input in inputs:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(raw_input)
    captured = io.StringIO()
    sys.stdout = captured

    exec_globals = {"__builtins__": __builtins__}
    try:
        exec(generator_code, exec_globals)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    raw_output = captured.getvalue().rstrip()

    # Support JSON factory format
    tc_input = raw_input
    tc_output = raw_output
    if raw_output.startswith('{'):
        try:
            parsed = json.loads(raw_output)
            if isinstance(parsed, dict) and "input" in parsed and "expected_output" in parsed:
                tc_input = parsed["input"]
                tc_output = parsed["expected_output"]
        except json.JSONDecodeError:
            pass

    print(json.dumps({"input": tc_input, "expected_output": tc_output}))
`

  const output = execFileSync('python3', ['-c', script], {
    input: JSON.stringify(inputs),
    encoding: 'utf-8',
    timeout: 120_000, // 2 min for pycryptodome etc
    // Big-integer answers (e.g. 2^N for N up to 10^4) across a 200-testcase
    // pool can exceed Node's 1 MB default maxBuffer.
    maxBuffer: 64 * 1024 * 1024,
  })

  return output
    .trim()
    .split('\n')
    .map((line) => JSON.parse(line) as TestcaseResult)
}

// ── Encryption ─────────────────────────────────────────────────────────────

export function encryptPool(
  key: Buffer,
  challengeId: string,
  verdictDetail: string,
  testcases: TestcaseResult[],
  planBlockSize?: number,
): Buffer {
  const payload = JSON.stringify({
    challenge_id: challengeId,
    verdict_detail: verdictDetail,
    testcases,
    // Only plan pools carry the field — non-plan payloads stay shape-identical
    // to the previous format.
    ...(planBlockSize !== undefined ? { plan_block_size: planBlockSize } : {}),
  })

  const nonce = randomBytes(12)
  const cipher = createCipheriv('aes-256-gcm', key, nonce)
  const encrypted = Buffer.concat([cipher.update(payload, 'utf-8'), cipher.final()])
  const tag = cipher.getAuthTag()

  // [magic 6B][version 1B][nonce 12B][ciphertext][tag 16B]
  return Buffer.concat([MAGIC, Buffer.from([POOL_VERSION]), nonce, encrypted, tag])
}

// ── Main ───────────────────────────────────────────────────────────────────

async function main() {
  console.log('[generate-pools] Starting pool generation...')

  // Read the encryption key. key_material.rs generation is NOT this
  // script's job anymore — gen:keymaterial owns it as step 1 of the build
  // chain (before build:wasm), so the compiled WASM and the pools always
  // share the same key. Rewriting it here would also dirty the Rust crate
  // on every pool build, forcing a full recompile next cargo run.
  const key = getPoolKey(PROJECT_ROOT)

  // Ensure output directory exists
  if (!existsSync(POOLS_DIR)) {
    mkdirSync(POOLS_DIR, { recursive: true })
  }

  // Find all challenge files
  if (!existsSync(CHALLENGES_DIR)) {
    mkdirSync(CHALLENGES_DIR, { recursive: true })
  }
  const files = readdirSync(CHALLENGES_DIR).filter((f) => f.endsWith('.md'))
  if (files.length === 0) {
    console.warn(
      '[generate-pools] No challenge files found in',
      CHALLENGES_DIR,
      '— skipping pool generation',
    )
    return
  }

  // Validate slug shape + uniqueness BEFORE running Python, so a bad challenge
  // filename fails fast without spending 30+s on input generation.
  try {
    collectAndValidateSlugs(files, CHALLENGES_DIR)
  } catch (err) {
    console.error('[generate-pools] ERROR:', err instanceof Error ? err.message : err)
    process.exit(1)
  }

  // Verify the WASM engine artifact and the Python runtime are available.
  preflightCheckWasm()
  preflightCheckPython()

  let success = 0
  let failed = 0
  const producedSlugs = new Set<string>()

  for (const file of files) {
    const filePath = join(CHALLENGES_DIR, file)
    console.log(`  Processing: ${file}`)

    try {
      const challenge = readChallenge(filePath)

      // testcase_plan challenges are built as consecutive blocks: the pool
      // holds floor(POOL_SIZE / plan_total) full plan rounds and the payload
      // carries plan_block_size so selection returns one whole block. The
      // engine independently enforces count % plan_total == 0, so a drift
      // between this computation and the engine's fails the build loudly.
      const planTotal =
        challenge.testcase_plan !== undefined
          ? computePlanTotal(challenge.testcase_plan, file)
          : undefined
      const requestCount =
        planTotal !== undefined ? Math.floor(POOL_SIZE / planTotal) * planTotal : POOL_SIZE
      if (planTotal !== undefined && requestCount < planTotal) {
        throw new Error(
          `'testcase_plan' total ${planTotal} exceeds POOL_SIZE ${POOL_SIZE} in ${file} — ` +
            `the pool cannot hold even one block`,
        )
      }

      // Generate random inputs via the WASM engine. Any engine error
      // (parse validation, budget violation, or a trap) aborts the whole
      // build immediately: a trapped WASM instance must never be reused,
      // and a bad spec must never ship a silently-degraded pool.
      let inputs: string[]
      try {
        inputs = await generateInputs(
          {
            params: challenge.params,
            seed: challenge.slug,
            input_budget: challenge.input_budget,
            ...(challenge.testcase_plan !== undefined
              ? { testcase_plan: challenge.testcase_plan }
              : {}),
          },
          requestCount,
        )
      } catch (err) {
        console.error(
          `[generate-pools] FATAL: input generation failed for ${file}:`,
          err instanceof Error ? err.message : err,
        )
        process.exit(1)
      }
      console.log(`    Generated ${inputs.length} inputs`)

      // Run generator to produce expected outputs
      const testcases = runGenerator(challenge.generator, inputs)
      console.log(`    Generated ${testcases.length} testcases`)

      // Encrypt pool — challenge_id is the per-challenge slug so multiple
      // challenges sharing an `algorithm` value get independent pools.
      const encrypted = encryptPool(
        key,
        challenge.slug,
        challenge.verdict_detail ?? 'hidden',
        testcases,
        planTotal,
      )

      // Write pool file at <slug>.bin (NOT <algorithm>.bin).
      const outPath = join(POOLS_DIR, `${challenge.slug}.bin`)
      writeFileSync(outPath, encrypted)
      console.log(`    Written: ${outPath} (${encrypted.length} bytes)`)

      producedSlugs.add(challenge.slug)
      success++
    } catch (err) {
      console.error(`    ERROR in ${file}:`, err instanceof Error ? err.message : err)
      failed++
    }
  }

  // Only clean up obsolete pools when EVERY challenge succeeded. A partial
  // failure (some succeed, some fail) would otherwise silently delete pools
  // for the failed challenges, leaving prod fetching 404s for them. Better
  // to leave the previous pool in place until the failure is fixed.
  if (success > 0 && failed === 0) {
    const deleted = cleanupObsoletePools(POOLS_DIR, producedSlugs)
    if (deleted.length > 0) {
      console.log(
        `[generate-pools] Removed ${deleted.length} obsolete pool(s): ${deleted.join(', ')}`,
      )
    }
  } else if (failed > 0) {
    console.warn(
      `[generate-pools] Cleanup skipped — ${failed} challenge(s) failed; obsolete pools preserved to avoid wiping pools for failed challenges.`,
    )
  }

  console.log(`[generate-pools] Done: ${success} pools generated, ${failed} failed`)

  if (failed > 0) {
    process.exit(1)
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch((err) => {
    console.error('[generate-pools] FATAL:', err instanceof Error ? err.message : err)
    process.exit(1)
  })
}
