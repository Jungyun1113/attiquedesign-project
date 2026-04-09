<template>
  <nav class="vertical-side-nav" :class="{ 'theme-dark-bg': isDarkBackground }">
    <ul class="nav-list">
      <li
        v-for="(item, index) in navItems"
        :key="item.id"
        class="nav-item"
        :class="{ active: activeSectionIndex === index }"
        @click="scrollToSection(item.id)"
      >
        <!-- 섹션 라벨 (왼쪽) -->
        <span class="nav-label">{{ item.label }}</span>
        <!-- 도트 -->
        <span class="nav-dot"></span>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useActiveSection } from '@/composables/useActiveSection'

const navItems = [
  { id: 'intro',       label: 'INTRO' },
  { id: 'philosophy',  label: 'PHILOSOPHY' },
  { id: 'interior',    label: 'INTERIOR' },
  { id: 'selection',   label: 'SELECTION' },
  { id: 'contact',     label: 'CONTACT' },
]

const { activeSectionIndex, scrollToSection } = useActiveSection(
  navItems.map((item) => item.id)
)

// 어두운 배경을 가진 섹션 인덱스들 (0: Intro, 2: Portfolio)
const isDarkBackground = computed(() => {
  return [0, 2].includes(activeSectionIndex.value)
})
</script>

<style scoped>
.vertical-side-nav {
  position: fixed;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  transition: all 0.5s ease;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: flex-end;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  cursor: pointer;
}

/* ==============================================================
   공통 레이아웃
   ============================================================== */
.nav-label {
  font-family: 'Montserrat', sans-serif;
  font-size: 8px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  transition: all 0.4s ease;
  white-space: nowrap;
}

.nav-dot {
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid transparent;
  transition: all 0.4s ease;
  flex-shrink: 0;
}

/* 활성화 상태 도트 크기 증가 */
.nav-item.active .nav-dot {
  width: 10px;
  height: 10px;
}

/* ==============================================================
   THEME: 어두운 배경일 때 (Light 텍스트)
   ============================================================== */
.theme-dark-bg .nav-label {
  color: rgba(255, 255, 255, 0.4); 
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
}
.theme-dark-bg .nav-item.active .nav-label {
  color: rgba(255, 255, 255, 1);
}
.theme-dark-bg .nav-item:hover .nav-label {
  color: rgba(255, 255, 255, 0.8);
}

.theme-dark-bg .nav-dot {
  background-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
}
.theme-dark-bg .nav-item.active .nav-dot {
  width: 10px;
  height: 10px;
  background-color: #8B0000;
  border: 1.5px solid #8B0000;
  box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.35), 0px 2px 4px rgba(0, 0, 0, 0.4);
}
.theme-dark-bg .nav-item:hover:not(.active) .nav-dot {
  background-color: rgba(255, 255, 255, 0.8);
}

/* ==============================================================
   THEME: 밝은 배경일 때 (Dark 텍스트)
   ============================================================== */
.vertical-side-nav:not(.theme-dark-bg) .nav-label {
  color: rgba(0, 0, 0, 0.3);
  text-shadow: none; /* 밝은 배경에는 그림자 불필요 */
}
.vertical-side-nav:not(.theme-dark-bg) .nav-item.active .nav-label {
  color: rgba(0, 0, 0, 0.9);
}
.vertical-side-nav:not(.theme-dark-bg) .nav-item:hover .nav-label {
  color: rgba(0, 0, 0, 0.6);
}

.vertical-side-nav:not(.theme-dark-bg) .nav-dot {
  background-color: rgba(0, 0, 0, 0.25);
  box-shadow: none;
}
.vertical-side-nav:not(.theme-dark-bg) .nav-item.active .nav-dot {
  width: 10px;
  height: 10px;
  background-color: #8B0000;
  border: 1.5px solid #8B0000;
  box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.25);
}
.vertical-side-nav:not(.theme-dark-bg) .nav-item:hover:not(.active) .nav-dot {
  background-color: rgba(0, 0, 0, 0.5);
}

/* --- 모바일 --- */
@media (max-width: 768px) {
  .vertical-side-nav {
    right: 1rem;
  }
  .nav-label {
    display: none;
  }
}
</style>
