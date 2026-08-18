/**
 * Emit the real engine's plan inputs for one challenge as JSON.
 *
 * Uses the SAME path the shipped pool build uses (readChallenge →
 * buildPoolRequest → generateInputs), so the inputs measured here are
 * byte-identical to the ones the site ships, and the engine's own
 * input_budget check runs.
 */
import { writeFileSync } from 'node:fs'
import {
  readChallenge,
  buildPoolRequest,
  generateInputs,
  computePlanTotal,
} from '../../../../scripts/generate-pools.js'

const file = process.argv[2]!
const out = process.argv[3]!
const challenge = readChallenge(file)
const planTotal = computePlanTotal(challenge.testcase_plan!, file)
const { spec, count } = buildPoolRequest(challenge, file)
const inputs = await generateInputs(spec, count)
const blocks = Array.from({ length: Math.floor(inputs.length / planTotal) }, (_, b) =>
  inputs.slice(b * planTotal, (b + 1) * planTotal),
)
writeFileSync(
  out,
  JSON.stringify(
    {
      slug: challenge.slug,
      planTotal,
      poolCount: count,
      inputBudget: challenge.input_budget,
      generator: challenge.generator,
      reference_solution: challenge.reference_solution,
      blocks,
    },
    null,
    1,
  ),
)
console.log(
  `wrote ${out}: planTotal=${planTotal} poolCount=${count} blocks=${blocks.length} budget=${challenge.input_budget}`,
)
export {}
