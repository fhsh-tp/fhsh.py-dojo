export interface Challenge {
  id: number
  title: string
  url: string
  difficulty: 'easy' | 'medium' | 'hard' | 'mystery'
  tags: string[]
  chapter?: string
  description?: string
}
