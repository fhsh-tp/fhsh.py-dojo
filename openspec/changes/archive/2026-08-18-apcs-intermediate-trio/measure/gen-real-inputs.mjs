// Emit the twenty plan inputs produced by the REAL Rust/WASM engine (seeded by
// the challenge slug, exactly as scripts/generate-pools.ts does), so the
// op-count measurement runs on the bytes students actually receive rather than
// on a Python replica of the input generator.
import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..')
const { generatePoolInputs } = await import(path.join(REPO, 'scripts/wasm-input-generator.ts'))

const [specPath, outPath] = process.argv.slice(2)
const spec = JSON.parse(readFileSync(specPath, 'utf8'))
const inputs = await generatePoolInputs(spec, 20)
if (inputs.length !== 20) throw new Error(`expected 20 inputs, got ${inputs.length}`)
writeFileSync(outPath, JSON.stringify(inputs), 'utf8')
console.error(`[gen-real-inputs] ${inputs.length} engine inputs -> ${outPath}`)
