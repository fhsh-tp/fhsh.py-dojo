import { createContentLoader, type ContentData } from 'vitepress'

/**
 * TutorArticle represents a single tutor page loaded at build time.
 */
export interface TutorArticle {
  title: string
  url: string
  description: string
  /** Derived from URL: /tutor/<subject>/... */
  subject: string
  chapter: number
  section: string
  createdTime: Date
  isIndex: boolean
  challenge?: string
}

declare const data: TutorArticle[]
export { data }

/** Parse subject from URL path: /tutor/<subject>/... → subject */
function subjectFromUrl(url: string): string {
  const match = url.match(/^\/tutor\/([^/]+)/)
  return match ? match[1]! : 'unknown'
}

const loader: {
  watch: string | string[]
  load: () => TutorArticle[] | Promise<TutorArticle[]>
} = createContentLoader('tutor/**/*.md', {
  includeSrc: false,
  render: false,
  excerpt: false,

  transform(rawData: ContentData[]): TutorArticle[] {
    return rawData.map(page => ({
      title: page.frontmatter.title ?? '無標題',
      url: page.url,
      description: page.frontmatter.description ?? '',
      subject: subjectFromUrl(page.url),
      chapter: page.frontmatter.chapter ?? 0,
      section: page.frontmatter.section ?? '',
      createdTime: page.frontmatter.createdTime
        ? new Date(page.frontmatter.createdTime)
        : new Date(0),
      isIndex: page.frontmatter.isIndex ?? false,
      challenge: page.frontmatter.challenge,
    }))
  },
})

export default loader
