<script setup lang="ts">
import { computed } from 'vue'
import type { Challenge } from '../types.d/challenge.type.ts'
import type { TutorArticle } from '../../../docs/shared/tutor.data'
import { CATEGORY_LIST_URL } from '../../../docs/shared/challenge-category'
import ChallengeCard from '../components/challenge/ChallengeCard.vue'

const props = defineProps<{
  tutorials: TutorArticle[]
  challenges: Challenge[]
}>()

// ── 最新教學：isIndex=false，依 createdTime 降序，取前 3 ────────────────────
const latestTutorials = computed(() =>
  [...props.tutorials]
    .filter(t => !t.isIndex)
    .sort((a, b) => new Date(b.createdTime).getTime() - new Date(a.createdTime).getTime())
    .slice(0, 3)
)

// ── 分類教學：依 subject → chapter 分組，chapter 升序，空群組不顯示 ──────────
interface ChapterGroup {
  chapter: number
  articles: TutorArticle[]
}
interface SubjectGroup {
  subject: string
  chapters: ChapterGroup[]
}

const subjectLabel: Record<string, string> = {
  py: 'Python 自學',
  alg: '演算法',
  ds: '資料結構',
}

const groupedTutorials = computed((): SubjectGroup[] => {
  const sections = props.tutorials.filter(t => !t.isIndex)
  if (sections.length === 0) return []

  const subjectMap = new Map<string, Map<number, TutorArticle[]>>()
  for (const article of sections) {
    if (!subjectMap.has(article.subject)) subjectMap.set(article.subject, new Map())
    const chMap = subjectMap.get(article.subject)!
    if (!chMap.has(article.chapter)) chMap.set(article.chapter, [])
    chMap.get(article.chapter)!.push(article)
  }

  return Array.from(subjectMap.entries()).map(([subject, chMap]) => ({
    subject,
    chapters: Array.from(chMap.entries())
      .sort(([a], [b]) => a - b)
      .map(([chapter, articles]) => ({ chapter, articles })),
  }))
})

// ── 最新 Python 挑戰：category=python，依 id 降序，取前 3 ────────────────────
const latestPythonChallenges = computed(() =>
  props.challenges
    .filter(c => c.category === 'python')
    .sort((a, b) => b.id - a.id)
    .slice(0, 3)
)

// ── 最新 APCS 挑戰：category=apcs，依 id 降序，取前 3 ────────────────────────
const latestApcsChallenges = computed(() =>
  props.challenges
    .filter(c => c.category === 'apcs')
    .sort((a, b) => b.id - a.id)
    .slice(0, 3)
)

const subjectLinkMap: Record<string, string> = {
  py: '/tutor/py/',
  alg: '/tutor/alg/',
  ds: '/tutor/ds/',
}
</script>

<template>
  <div class="home-view vp-raw">

    <!-- ── 最新教學 ────────────────────────────────────────────────────────── -->
    <section class="home-section">
      <h2 class="home-section__title">最新教學</h2>
      <div v-if="latestTutorials.length > 0" class="home-tutorial-grid">
        <a
          v-for="t in latestTutorials"
          :key="t.url"
          :href="t.url"
          class="home-tutorial-card"
        >
          <div class="home-tutorial-card__meta">
            <span class="home-tutorial-card__subject">{{ subjectLabel[t.subject] ?? t.subject }}</span>
            <span class="home-tutorial-card__section">§ {{ t.section }}</span>
          </div>
          <div class="home-tutorial-card__title">{{ t.title }}</div>
          <div class="home-tutorial-card__desc">{{ t.description }}</div>
        </a>
      </div>
      <p v-else class="home-empty">教學文章尚未建立，敬請期待。</p>
    </section>

    <!-- ── 分類教學 ────────────────────────────────────────────────────────── -->
    <section class="home-section">
      <h2 class="home-section__title">分類教學</h2>
      <div v-if="groupedTutorials.length > 0">
        <div
          v-for="sg in groupedTutorials"
          :key="sg.subject"
          class="home-subject-group"
        >
          <h3 class="home-subject-group__title">
            <a :href="subjectLinkMap[sg.subject] ?? `/tutor/${sg.subject}/`">
              {{ subjectLabel[sg.subject] ?? sg.subject }}
            </a>
          </h3>
          <div
            v-for="cg in sg.chapters"
            :key="cg.chapter"
            class="home-chapter-group"
          >
            <h4 class="home-chapter-group__title">第 {{ cg.chapter }} 模組</h4>
            <ul class="home-chapter-group__list">
              <li v-for="article in cg.articles" :key="article.url">
                <a :href="article.url">{{ article.title }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <p v-else class="home-empty">教學分類尚無內容，敬請期待。</p>
    </section>

    <!-- ── 最新 Python 挑戰 ─────────────────────────────────────────────────── -->
    <section class="home-section">
      <h2 class="home-section__title">
        最新 Python 挑戰
        <a :href="CATEGORY_LIST_URL.python" class="home-section__more">查看全部 →</a>
      </h2>
      <div v-if="latestPythonChallenges.length > 0" class="home-challenge-grid">
        <ChallengeCard
          v-for="c in latestPythonChallenges"
          :key="c.id"
          :challenge="c"
        />
      </div>
      <p v-else class="home-empty">挑戰題庫尚未建立，敬請期待。</p>
    </section>

    <!-- ── 最新 APCS 挑戰 ──────────────────────────────────────────────────── -->
    <section class="home-section">
      <h2 class="home-section__title">
        最新 APCS 挑戰
        <a :href="CATEGORY_LIST_URL.apcs" class="home-section__more">查看全部 →</a>
      </h2>
      <div v-if="latestApcsChallenges.length > 0" class="home-challenge-grid">
        <ChallengeCard
          v-for="c in latestApcsChallenges"
          :key="c.id"
          :challenge="c"
        />
      </div>
      <p v-else class="home-empty">挑戰題庫尚未建立，敬請期待。</p>
    </section>

  </div>
</template>

<style scoped>
.home-view {
  max-width: 1152px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

.home-section {
  margin-bottom: 3rem;
}

.home-section__title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  color: var(--vp-c-text-1);
}

.home-section__more {
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.home-section__more:hover {
  text-decoration: underline;
}

.home-tutorial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.home-tutorial-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 1.25rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  background: var(--vp-c-bg-soft);
  transition: border-color 0.2s, background 0.2s;
}

.home-tutorial-card:hover {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg-elv);
}

.home-tutorial-card__meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.home-tutorial-card__title {
  font-weight: 600;
  font-size: 1rem;
}

.home-tutorial-card__desc {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.home-subject-group {
  margin-bottom: 1.5rem;
}

.home-subject-group__title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.home-subject-group__title a {
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.home-chapter-group {
  margin-left: 1rem;
  margin-bottom: 0.75rem;
}

.home-chapter-group__title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
  margin-bottom: 0.375rem;
}

.home-chapter-group__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.home-chapter-group__list a {
  font-size: 0.875rem;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  padding: 0.125rem 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
}

.home-chapter-group__list a:hover {
  background: var(--vp-c-bg-soft);
}

.home-challenge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.home-empty {
  color: var(--vp-c-text-3);
  font-style: italic;
}
</style>
