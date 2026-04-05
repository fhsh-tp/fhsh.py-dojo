import { createContentLoader, type ContentData } from 'vitepress'

/**
 * 定義 Challenge 的資料結構
 * 匯出此介面，方便在 Vue 元件中 import 使用
 */
export interface Challenge {
  id: number
  title: string
  url: string
  difficulty: 'easy' | 'medium' | 'hard' | string
  algorithm: string
  params: object
  testcase_count?: number
  tags?: string[]
}

declare const data: Challenge[]
export { data }

const loader: {
  watch: string | string[]
  load: () => Challenge[] | Promise<Challenge[]>
} = createContentLoader('challenge/**/*.md', {
  includeSrc: false, // 如果不需要全文搜尋，建議設為 false 以減少 bundle size
  render: false,
  excerpt: false,

  /**
   * 轉換原始資料
   * @param rawData VitePress 載入的原始資料
   */
  transform(rawData: ContentData[]): Challenge[] {
    const challenges = rawData
      .map((challenge, idx) => {
        return {
          id: challenge.frontmatter.id || idx + 1,
          title: challenge.frontmatter.title || `密碼學挑戰 #${idx + 1}`,
          url: challenge.url,
          difficulty: challenge.frontmatter.difficulty || 'mystery',
          algorithm: challenge.frontmatter.algorithm,
          params: challenge.frontmatter.params,
          testcase_count: challenge.frontmatter.testcase_count || 5,
          tags: challenge.frontmatter.tags || ['challenge'],
        }
      }).sort((a, b) => a.id - b.id)

    return challenges
  },
})

export default loader
