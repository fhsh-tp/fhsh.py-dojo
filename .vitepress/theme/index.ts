// https://vitepress.dev/guide/custom-theme
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { createPinia } from 'pinia'
import Layout from './Layout.vue'
import ChallengeListView from './views/ChallengeListView.vue'
import ChallengeView from './views/ChallengeView.vue'
import HomeView from './views/HomeView.vue'
import ChallengeLink from './components/tutor/ChallengeLink.vue'
import MermaidDiagram from './components/MermaidDiagram.vue'
import './tailwind.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout,
  async enhanceApp({ app, router, siteData }) {
    app.use(createPinia())
    app.component('ChallengeListView', ChallengeListView)
    app.component('ChallengeView', ChallengeView)
    app.component('HomeView', HomeView)
    app.component('ChallengeLink', ChallengeLink)
    app.component('MermaidDiagram', MermaidDiagram)
  }
} satisfies Theme
