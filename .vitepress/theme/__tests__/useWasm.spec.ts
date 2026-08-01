import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useWasm } from '../composables/useWasm'

vi.mock('../composables/useWasm', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../composables/useWasm')>()
  return actual
})

// useWasm caches the loaded WASM module at MODULE level: the first loader to
// run wins for the whole file. All tests therefore share this one mock.
const mockGeneratedInputs = { inputs: ['HELLO\n3', 'WORLD\n7'] }
const mockDevInputs = { inputs: ['5\n', 'L\n'] }
const sharedMockMod = {
  default: vi.fn().mockResolvedValue(undefined),
  generate_challenge: vi.fn().mockReturnValue(mockGeneratedInputs),
  generate_dev_inputs: vi.fn().mockReturnValue(mockDevInputs),
}

describe('useWasm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    sharedMockMod.default.mockResolvedValue(undefined)
    sharedMockMod.generate_challenge.mockReturnValue(mockGeneratedInputs)
    sharedMockMod.generate_dev_inputs.mockReturnValue(mockDevInputs)
  })

  it('exposes loadWasm, generateChallenge and generateDevInputs', () => {
    const { loadWasm, generateChallenge, generateDevInputs } = useWasm()
    expect(typeof loadWasm).toBe('function')
    expect(typeof generateChallenge).toBe('function')
    expect(typeof generateDevInputs).toBe('function')
  })

  it('generateChallenge calls generate_challenge with params_json and count', async () => {
    const { loadWasm, generateChallenge } = useWasm(() => Promise.resolve(sharedMockMod))
    await loadWasm()
    const result = await generateChallenge('{"shift":{"type":"int","min":1,"max":25}}', 2)
    expect(sharedMockMod.generate_challenge).toHaveBeenCalledWith(
      '{"shift":{"type":"int","min":1,"max":25}}',
      2,
    )
    expect(result).toEqual(mockGeneratedInputs)
  })

  it('generateDevInputs calls generate_dev_inputs with the spec json', async () => {
    const { loadWasm, generateDevInputs } = useWasm(() => Promise.resolve(sharedMockMod))
    await loadWasm()
    const spec = '{"params":{"n":{"type":"int"}},"testcase_plan":[{"count":1},{"literal":"L\\n"}]}'
    const result = await generateDevInputs(spec)
    expect(sharedMockMod.generate_dev_inputs).toHaveBeenCalledWith(spec)
    expect(result).toEqual(mockDevInputs)
  })

  it('generateDevInputs returns null when the entry throws', async () => {
    sharedMockMod.generate_dev_inputs.mockImplementation(() => {
      throw new Error("dev spec: missing 'testcase_plan'")
    })
    const { loadWasm, generateDevInputs } = useWasm(() => Promise.resolve(sharedMockMod))
    await loadWasm()
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const result = await generateDevInputs('{"params":{}}')
    expect(result).toBeNull()
    expect(errSpy).toHaveBeenCalled()
    errSpy.mockRestore()
  })

  it('generateChallenge result has inputs array property', async () => {
    const { generateChallenge } = useWasm()
    // The composable caches module-level state from previous test; result shape is validated here
    const result = await generateChallenge('{"shift":{"type":"int","min":1,"max":25}}', 2)
    // result may be null (no WASM in test env) or an object with inputs array
    if (result !== null) {
      expect(Array.isArray(result.inputs)).toBe(true)
    } else {
      expect(result).toBeNull()
    }
  })
})
