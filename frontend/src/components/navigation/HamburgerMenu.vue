<template>
  <!-- 햄버거 버튼 (Fixed, 우측 상단) -->
  <button
    class="hamburger-btn"
    :class="{ 'is-open': isOpen, 'theme-light': isLightTheme }"
    @click="toggle"
    aria-label="메뉴 열기/닫기"
  >
    <span class="hamburger-line hamburger-line--1"></span>
    <span class="hamburger-line hamburger-line--2"></span>
  </button>

  <!-- 풀스크린 오버레이 메뉴 -->
  <Teleport to="body">
    <transition name="overlay-fade">
      <div v-if="isOpen" class="menu-overlay" @click.self="close">
        <nav class="menu-nav">
          <ul class="menu-list">
            <li
              v-for="(item, index) in menuItems"
              :key="item.id"
              class="menu-item"
              :style="{ transitionDelay: `${0.08 * index + 0.15}s` }"
              :class="{ 'is-visible': isOpen }"
            >
              <button class="menu-link" @click="navigateTo(item.id)">
                <span class="menu-number">0{{ index }}</span>
                <span class="menu-label">{{ item.label }}</span>
              </button>
            </li>
          </ul>
        </nav>

        <!-- 하단 연락처 -->
        <div class="menu-footer" :class="{ 'is-visible': isOpen }">
          <p>Seoul, Hannam-dong</p>
          <p>hello@attiquedesign.com</p>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useActiveSection } from '@/composables/useActiveSection'

const props = defineProps<{
  sectionIds: string[]
}>()

const emit = defineEmits<{
  navigate: [sectionId: string]
}>()

const isOpen = ref(false)

const menuItems = [
  { id: 'intro', label: 'Index' },
    { id: 'philosophy', label: 'Philosophy' },
    { id: 'portfolio', label: 'Portfolio' },
    { id: 'selection', label: 'Selection' },
    { id: 'contact', label: 'Contact' },
  ]

const { activeSectionIndex } = useActiveSection(props.sectionIds)

// 밝은 배경 섹션 (1: Philosophy, 3: Selection, 4: Contact)
const isLightTheme = computed(() => {
  return [1, 3, 4].includes(activeSectionIndex.value)
})

function toggle() {
  isOpen.value = !isOpen.value
  document.body.style.overflow = isOpen.value ? 'hidden' : ''
}

function close() {
  isOpen.value = false
  document.body.style.overflow = ''
}

function navigateTo(id: string) {
  close()
  // 약간의 딜레이 후 스크롤 (오버레이 닫히는 애니메이션과 겹치지 않게)
  setTimeout(() => {
    emit('navigate', id)
  }, 300)
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════
   HAMBURGER BUTTON
   ═══════════════════════════════════════════════════════════ */
.hamburger-btn {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 7px;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  mix-blend-mode: difference;
}

.hamburger-line {
  display: block;
  width: 28px;
  height: 1px;
  background: #fff;
  transition: all 0.4s cubic-bezier(0.76, 0, 0.24, 1);
  transform-origin: center;
}

/* 밝은 배경에서 → 어두운 선 (mix-blend-mode가 처리하므로 기본 흰색 유지) */

/* X 모프 (열린 상태) */
.hamburger-btn.is-open .hamburger-line--1 {
  transform: rotate(45deg) translate(2.5px, 2.5px);
}
.hamburger-btn.is-open .hamburger-line--2 {
  transform: rotate(-45deg) translate(2.5px, -2.5px);
}

/* ═══════════════════════════════════════════════════════════
   FULLSCREEN OVERLAY
   ═══════════════════════════════════════════════════════════ */
.menu-overlay {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: #6D2122;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
}

/* Transition */
.overlay-fade-enter-active {
  transition: opacity 0.5s ease;
}
.overlay-fade-leave-active {
  transition: opacity 0.4s ease;
}
.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}

/* ═══════════════════════════════════════════════════════════
   MENU NAV
   ═══════════════════════════════════════════════════════════ */
.menu-nav {
  flex: 1;
  display: flex;
  align-items: center;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.menu-item {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.menu-item.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.menu-link {
  display: flex;
  align-items: baseline;
  gap: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.6rem 0;
  text-decoration: none;
  transition: transform 0.4s ease, color 0.4s ease;
}

.menu-link:hover {
  transform: translateX(12px);
}

.menu-number {
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  font-weight: 300;
  letter-spacing: 0.15em;
  color: rgba(255, 255, 255, 0.35);
  min-width: 24px;
}

.menu-label {
  font-family: 'Playfair Display', serif;
  font-size: clamp(48px, 9vw, 96px);
  font-weight: 400;
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 0.03em;
  line-height: 1.1;
  transition: color 0.4s ease, transform 0.4s ease;
}

.menu-link:hover .menu-label {
  color: #F5E6D3;
}

.menu-link:hover .menu-number {
  color: rgba(245, 230, 211, 0.6);
}

/* ═══════════════════════════════════════════════════════════
   MENU FOOTER
   ═══════════════════════════════════════════════════════════ */
.menu-footer {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  letter-spacing: 0.25em;
  color: rgba(255, 255, 255, 0.35);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.5s ease 0.5s, transform 0.5s ease 0.5s;
}

.menu-footer.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.menu-footer p {
  margin: 0;
}

/* ═══════════════════════════════════════════════════════════
   MOBILE
   ═══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  .hamburger-btn {
    top: 1.2rem;
    right: 1.2rem;
  }
  .menu-overlay {
    padding: 3rem 1.5rem;
  }
  .menu-list {
    gap: 0.1rem;
  }
  .menu-link {
    gap: 0.8rem;
  }
}
</style>
