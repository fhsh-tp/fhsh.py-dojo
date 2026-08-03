import type { ChallengeCategory } from '../../../docs/shared/challenge-category'

export interface Challenge {
  id: number
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
