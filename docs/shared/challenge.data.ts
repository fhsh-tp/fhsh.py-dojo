import { createContentLoader, type ContentData } from 'vitepress'
import type { Challenge } from '../../.vitepress/theme/types.d/challenge.type'
import { resolveExerciseType, type ExerciseType } from './exercise-type'
import { resolveChallengeCategory } from './challenge-category'
import { deriveChallengeSlug } from './challenge-slug'
import { CHALLENGE_ID_PATTERN, compareChallengeId } from './challenge-id'

export type { ExerciseType }

export interface DataChallenge extends Challenge {
  algorithm: string
  params: object
  testcase_count?: number
  type: ExerciseType
}

declare const data: DataChallenge[]
export { data }
export type { Challenge }

const loader: {
  watch: string | string[]
  load: () => DataChallenge[] | Promise<DataChallenge[]>
} = createContentLoader('challenge/**/*.md', {
  includeSrc: false, // 如果不需要全文搜尋，建議設為 false 以減少 bundle size
  render: false,
  excerpt: false,

  /**
   * 轉換原始資料
   * @param rawData VitePress 載入的原始資料
   */
  transform(rawData: ContentData[]): DataChallenge[] {
    const challenges = rawData
      .map((challenge, idx) => {
        return {
          // A missing or malformed id is a content error; the fail-loud gates
          // are build:redirects (in the dev/build pipeline) and the ledger
          // test. The loader stays total and sanitizes to '' so a mid-edit
          // frontmatter never renders garbage (e.g. "[object Object]") into
          // the card badge during dev hot reload.
          id: ((raw) => (CHALLENGE_ID_PATTERN.test(raw) ? raw : ''))(
            String(challenge.frontmatter.id ?? ''),
          ),
          slug: deriveChallengeSlug(challenge.url),
          title: challenge.frontmatter.title || `挑戰 #${idx + 1}`,
          url: challenge.url,
          difficulty: challenge.frontmatter.difficulty || 'mystery',
          category: resolveChallengeCategory(challenge.frontmatter.category),
          type: resolveExerciseType(challenge.frontmatter.type),
          algorithm: challenge.frontmatter.algorithm ?? '',
          params: challenge.frontmatter.params ?? {},
          testcase_count: challenge.frontmatter.testcase_count ?? 5,
          tags: challenge.frontmatter.tags || ['challenge'],
          chapter: challenge.frontmatter.chapter || '',
          description: challenge.frontmatter.description || '',
        }
      }).sort((a, b) => compareChallengeId(a.id, b.id))

    return challenges
  },
})

export default loader
