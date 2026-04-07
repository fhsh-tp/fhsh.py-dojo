---
layout: doc
title: 挑戰題庫
sidebar: false
---

<script setup lang="ts">
import { data as challenges } from './shared/challenge.data.ts'
</script>

<ChallengeListView :challenges="challenges" />
