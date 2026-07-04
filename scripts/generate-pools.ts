#!/usr/bin/env npx tsx
/**
 * Build script: generate encrypted testcase pools for all challenges.
 *
 * 1. Read all docs/challenge/*.md files and parse frontmatter
 * 2. For each challenge, generate random inputs via Python (replicating WASM param logic)
 * 3. Execute generator code via Python subprocess to produce expected outputs
 * 4. Encrypt each pool with AES-256-GCM
 * 5. Write to docs/public/pools/<algorithm>.bin
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
import { generateKeyMaterial } from './generate-key-material.js'

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
const POOL_SIZE = 200 // testcases per pool
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
   * Optional Python reference solution (a full program that reads stdin and
   * prints the correct answer). Independent of `generator`; used only by the
   * content-layer regression test to verify a known-correct solution earns AC.
   */
  reference_solution?: string
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

  if (!algorithm) throw new Error(`Missing 'algorithm' in ${filePath}`)
  if (!generator) throw new Error(`Missing 'generator' in ${filePath}`)
  if (!params) throw new Error(`Missing 'params' in ${filePath}`)

  return { slug, algorithm, generator, params, testcase_count, verdict_detail, reference_solution }
}

// ── Input generation via Python ────────────────────────────────────────────

/**
 * Generate random inputs using a Python script that replicates the WASM
 * param-based generation logic. This avoids needing to load the WASM
 * module at build time.
 */
export function generateInputs(params: Record<string, unknown>, count: number): string[] {
  const script = `
import json, random, string, sys

params = json.loads(sys.stdin.read())
count = ${count}

def gen_value(spec):
    t = spec.get("type", "")
    if t == "int":
        return str(random.randint(spec.get("min", 0), spec.get("max", 100)))
    elif t == "alpha_upper":
        length = random.randint(spec.get("min_len", 1), spec.get("max_len", 10))
        mul = spec.get("multiple_of", 1)
        if mul > 1:
            lo = max(1, (spec.get("min_len", 1) + mul - 1) // mul)
            hi = spec.get("max_len", 10) // mul
            length = random.randint(lo, hi) * mul
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    elif t == "alpha_lower":
        length = random.randint(spec.get("min_len", 1), spec.get("max_len", 10))
        mul = spec.get("multiple_of", 1)
        if mul > 1:
            lo = max(1, (spec.get("min_len", 1) + mul - 1) // mul)
            hi = spec.get("max_len", 10) // mul
            length = random.randint(lo, hi) * mul
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    elif t == "alpha_mixed":
        length = random.randint(spec.get("min_len", 1), spec.get("max_len", 10))
        mul = spec.get("multiple_of", 1)
        if mul > 1:
            lo = max(1, (spec.get("min_len", 1) + mul - 1) // mul)
            hi = spec.get("max_len", 10) // mul
            length = random.randint(lo, hi) * mul
        return ''.join(random.choices(string.ascii_letters, k=length))
    elif t == "hex_string":
        length = random.randint(spec.get("min_len", 1), spec.get("max_len", 10))
        mul = spec.get("multiple_of", 1)
        if mul > 1:
            lo = max(1, (spec.get("min_len", 1) + mul - 1) // mul)
            hi = spec.get("max_len", 10) // mul
            length = random.randint(lo, hi) * mul
        return ''.join(random.choices('0123456789abcdef', k=length))
    elif t == "printable_ascii":
        length = random.randint(spec.get("min_len", 1), spec.get("max_len", 10))
        mul = spec.get("multiple_of", 1)
        if mul > 1:
            lo = max(1, (spec.get("min_len", 1) + mul - 1) // mul)
            hi = spec.get("max_len", 10) // mul
            length = random.randint(lo, hi) * mul
        chars = [chr(c) for c in range(0x21, 0x7f)]
        return ''.join(random.choices(chars, k=length))
    elif t == "enum":
        return random.choice(spec.get("values", ["?"]))
    else:
        return "UNKNOWN_TYPE"

def gen_param_line(spec):
    count_spec = spec.get("count", {})
    if isinstance(count_spec, dict):
        mn = count_spec.get("min", 1)
        mx = count_spec.get("max", 1)
        sep = count_spec.get("separator", " ")
    else:
        mn = mx = 1
        sep = " "
    n = random.randint(mn, mx)
    values = [gen_value(spec) for _ in range(n)]
    return sep.join(values)

for _ in range(count):
    lines = []
    for name in params:
        lines.append(gen_param_line(params[name]))
    print(json.dumps("\\n".join(lines)))
`
  const output = execFileSync('python3', ['-c', script], {
    input: JSON.stringify(params),
    encoding: 'utf-8',
    timeout: 30_000,
  })

  return output
    .trim()
    .split('\n')
    .map((line) => JSON.parse(line) as string)
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
): Buffer {
  const payload = JSON.stringify({
    challenge_id: challengeId,
    verdict_detail: verdictDetail,
    testcases,
  })

  const nonce = randomBytes(12)
  const cipher = createCipheriv('aes-256-gcm', key, nonce)
  const encrypted = Buffer.concat([cipher.update(payload, 'utf-8'), cipher.final()])
  const tag = cipher.getAuthTag()

  // [magic 6B][version 1B][nonce 12B][ciphertext][tag 16B]
  return Buffer.concat([MAGIC, Buffer.from([POOL_VERSION]), nonce, encrypted, tag])
}

// ── Main ───────────────────────────────────────────────────────────────────

function main() {
  console.log('[generate-pools] Starting pool generation...')

  // Read encryption key and generate key_material.rs unconditionally —
  // WASM compilation depends on this file regardless of whether challenges exist.
  const key = getPoolKey(PROJECT_ROOT)
  generateKeyMaterial(key, PROJECT_ROOT)

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

  // Verify Python runtime and packages are available (only needed for pool generation)
  preflightCheckPython()

  let success = 0
  let failed = 0
  const producedSlugs = new Set<string>()

  for (const file of files) {
    const filePath = join(CHALLENGES_DIR, file)
    console.log(`  Processing: ${file}`)

    try {
      const challenge = readChallenge(filePath)

      // Generate random inputs
      const inputs = generateInputs(challenge.params, POOL_SIZE)
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
  main()
}
