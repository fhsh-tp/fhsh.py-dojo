/**
 * Exercise-type taxonomy — single source of truth for the data layer.
 *
 * Only the implemented values are typed here. The full extensible taxonomy also
 * registers `fill_in_blank` and `gamified` (deferred) and `guided` (future
 * placeholder); those are documented in the `challenge-exercise-type` spec and
 * the challenge-author skill but are intentionally NOT accepted at runtime until
 * they have templates.
 *
 * `scripts/new-challenge.ts` keeps its own copy of this list for build-time
 * scaffolding; `scripts/new-challenge.test.ts` asserts the two stay in lockstep.
 */
export const EXERCISE_TYPES = ['basic', 'competition'] as const
export type ExerciseType = (typeof EXERCISE_TYPES)[number]

/**
 * Resolve a raw frontmatter `type` value to a known exercise type.
 *
 * Unlike a blind `as ExerciseType` cast, this validates at runtime: an absent,
 * mistyped, or not-yet-implemented value resolves to `basic` rather than being
 * silently trusted. Hand-authored challenge files therefore cannot smuggle an
 * unknown exercise type past the data layer.
 */
export function resolveExerciseType(raw: unknown): ExerciseType {
  return (EXERCISE_TYPES as readonly unknown[]).includes(raw) ? (raw as ExerciseType) : 'basic'
}
