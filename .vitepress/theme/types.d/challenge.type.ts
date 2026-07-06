export interface Challenge {
  id: number
  /** Per-challenge slug (markdown file basename). Primary key for local progress persistence. */
  slug: string
  title: string
  url: string
  difficulty: 'easy' | 'medium' | 'hard' | 'mystery'
  tags: string[]
  chapter: string
  description: string
}
