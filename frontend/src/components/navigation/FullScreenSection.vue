<template>
  <section
    :id="id"
    class="full-screen-section"
    :class="bgClass"
  >
    <slot />
  </section>
</template>

<script setup lang="ts">
defineProps<{
  id: string        // 앵커 ID (예: 'intro', 'philosophy')
  bgClass?: string  // 선택적 배경 Tailwind 클래스
}>()
</script>

<style scoped>
.full-screen-section {
  height: 100dvh;
  scroll-snap-align: start;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
