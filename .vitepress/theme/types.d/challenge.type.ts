import type { ChallengeCategory } from '../../../docs/shared/challenge-category'

export interface Challenge {
  /** String id: `<category prefix><3-digit ordinal>` (py001, apcs003). See docs/shared/challenge-id.ts. */
  id: string
  /** Per-challenge slug (markdown file basename). Primary key for local progress persistence. */
  slug: string
  title: string
  url: string
  difficulty: 'easy' | 'medium' | 'hard' | 'mystery'
  /** Catalogue the challenge belongs to; resolved (never a raw frontmatter string). */
  category: ChallengeCategory
  tags: string[]
  chapter: string
  description: string
}
