---
layout: page
title: APCS 挑戰
sidebar: false
---

<script setup lang="ts">
import { data as challenges } from './shared/challenge.data.ts'

const apcsChallenges = challenges.filter((c) => c.category === 'apcs')
</script>

<ChallengeListView :challenges="apcsChallenges" />
