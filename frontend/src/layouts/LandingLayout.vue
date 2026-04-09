<template>
  <!-- 랜딩 전용 레이아웃: HamburgerMenu + 콘텐츠만 (상단 GNB 없음) -->
  <div class="landing-wrapper">
    <router-view ref="homeRef" />
    <HamburgerMenu
      :section-ids="sectionIds"
      @navigate="handleNavigate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HamburgerMenu from '@/components/navigation/HamburgerMenu.vue'

const sectionIds = ['intro', 'philosophy', 'portfolio', 'selection', 'contact']
const homeRef = ref<any>(null)

function handleNavigate(sectionId: string) {
  const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
  const el = document.getElementById(sectionId)
  if (!el) return

  if (scrollRoot) {
    scrollRoot.scrollTo({ top: el.offsetTop, behavior: 'smooth' })
  } else {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.landing-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden; /* 스크롤은 ScrollSnapContainer 내부에서만 */
}
</style>
