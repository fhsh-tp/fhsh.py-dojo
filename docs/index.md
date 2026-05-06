---
layout: home

hero:
  name: "Python 自學道場"
  text: "台北市立復興高級中學"
  tagline: 在解題中學習 Python 程式設計
  image:
    light: /assets/LOGO-light.svg
    dark: /assets/LOGO-dark.svg
    alt: LOGO

---

<script setup lang="ts">
import { data as tutorials } from './shared/tutor.data.ts'
import { data as challenges } from './shared/challenge.data.ts'
</script>

<HomeView :tutorials="tutorials" :challenges="challenges" />
