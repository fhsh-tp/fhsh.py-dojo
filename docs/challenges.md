---
layout: page
title: Python 挑戰
sidebar: false
---

<script setup lang="ts">
import { data as challenges } from './shared/challenge.data.ts'

const pythonChallenges = challenges.filter((c) => c.category === 'python')
</script>

<ChallengeListView :challenges="pythonChallenges" />
