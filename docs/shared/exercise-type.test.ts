// @vitest-environment node
/**
 * Unit tests for the data-layer exercise-type resolution.
 *
 * These lock in the runtime-checked behaviour the data loader relies on: a
 * hand-authored or mistyped `type` value must resolve to `basic` rather than
 * being silently trusted as a valid ExerciseType.
 */
import { describe, it, expect } from 'vitest'

import { EXERCISE_TYPES, resolveExerciseType } from './exercise-type.js'

describe('EXERCISE_TYPES', () => {
  it('lists exactly the implemented exercise types', () => {
    expect([...EXERCISE_TYPES]).toEqual(['basic', 'competition'])
  })
})

describe('resolveExerciseType', () => {
  it('preserves an implemented value', () => {
    expect(resolveExerciseType('basic')).toBe('basic')
    expect(resolveExerciseType('competition')).toBe('competition')
  })

  it('resolves an absent value to basic', () => {
    expect(resolveExerciseType(undefined)).toBe('basic')
    expect(resolveExerciseType(null)).toBe('basic')
  })

  it('resolves a mistyped / deferred / future value to basic (no silent trust)', () => {
    for (const bad of ['gamified', 'fill_in_blank', 'guided', 'Basic', 'competiton', '', 42, {}]) {
      expect(resolveExerciseType(bad)).toBe('basic')
    }
  })
})
