<template>
  <div ref="containerRef" class="scroll-snap-container">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const containerRef = ref<HTMLElement | null>(null)
</script>

<style scoped>
.scroll-snap-container {
  width: 100%;
  height: 100dvh;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

/* 브라우저 기본 스크롤바 숨김 (디자인 기획 반영) */
.scroll-snap-container::-webkit-scrollbar {
  display: none;
}
.scroll-snap-container {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
