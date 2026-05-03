<template>
  <header class="global-header" :class="{ 'is-scrolled': scrolled, 'is-menu-collapsed': menuCollapsed, 'is-hovered': hovered, 'is-solid': !isHeroRoute, 'is-mobile-open': mobileMenuOpen }">
    <div class="header-inner">
      <!-- Logo Center (desktop only) -->
      <div class="logo-wrap">
        <router-link to="/selection" class="logo-link" aria-label="ATTIQUE DESIGN">
          <span class="header-logo" role="img" aria-hidden="true"></span>
        </router-link>
      </div>

      <!-- Mobile hamburger toggle -->
      <button
        type="button"
        class="menu-toggle"
        :class="{ 'is-open': mobileMenuOpen }"
        :aria-label="mobileMenuOpen ? '메뉴 닫기' : '메뉴 열기'"
        :aria-expanded="mobileMenuOpen"
        @click.stop="toggleMobileMenu"
      >
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>

      <!-- Navigation Bottom -->
      <nav class="gnb">
        <ul class="gnb-list">
          <li v-for="item in menuItems" :key="item.path">
            <router-link
              :to="item.path"
              class="gnb-link"
              :class="{ 'is-active': isLinkActive(item) }"
              @click="mobileMenuOpen = false"
            >
              {{ item.label }}
            </router-link>
          </li>
        </ul>
      </nav>

    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isHeroRoute = computed(
  () => route.path === '/selection' && route.query.view !== 'grid'
)
const scrolled = ref(false)
const menuCollapsed = ref(isHeroRoute.value)
const hoveredRaw = ref(false)
const hovered = computed(() => hoveredRaw.value && isHeroRoute.value)
const mobileMenuOpen = ref(false)

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

watch(() => route.fullPath, () => {
  mobileMenuOpen.value = false
})
const menuItems = [
  { label: '소개', path: '/philosophy' },
  { label: '셀렉션', path: '/selection?view=grid' },
  { label: '포트폴리오', path: '/portfolio' },
  { label: '인테리어 문의', path: '/contact' },
]

function isLinkActive(item: { label: string; path: string }) {
  // 1. Selection의 경우: 경로가 /selection 이고 query.view가 grid일 때만 active
  if (item.label === '셀렉션') {
    return route.path === '/selection' && route.query.view === 'grid'
  }

  // 2. 나머지는 단순 경로 포함 여부 (또는 완전 일치)로 판단
  // router-link의 기본 active 로직과 유사하게 구현
  return route.path.startsWith(item.path.split('?')[0])
}

// ── Aesop-style minimal header ─────────────────────────
// 페이지 상단이거나 커서가 상단 영역에 있을 때만 메뉴 노출, 그 외에는 로고만
const SHOW_AT_TOP = 100         // 스크롤이 이 값 이하이면 항상 노출
const HOVER_REVEAL_PX = 120     // 커서가 화면 상단 120px 이내면 노출
let cursorNearTop = false
let scrollFrame = 0

function refreshMenuState() {
  if (isHeroRoute.value) {
    menuCollapsed.value = !cursorNearTop
    return
  }
  const atTop = window.scrollY < SHOW_AT_TOP
  menuCollapsed.value = !atTop && !cursorNearTop
}

function handleScroll() {
  if (scrollFrame) return
  scrollFrame = requestAnimationFrame(() => {
    scrolled.value = window.scrollY > 20
    refreshMenuState()
    scrollFrame = 0
  })
}

function handleMouseMove(e: MouseEvent) {
  const next = e.clientY <= HOVER_REVEAL_PX
  if (next !== cursorNearTop) {
    cursorNearTop = next
    hoveredRaw.value = next
    refreshMenuState()
  }
}

function handleMouseLeave() {
  cursorNearTop = false
  hoveredRaw.value = false
  refreshMenuState()
}

onMounted(() => {
  refreshMenuState()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('mousemove', handleMouseMove, { passive: true })
  document.addEventListener('mouseleave', handleMouseLeave)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseleave', handleMouseLeave)
  if (scrollFrame) cancelAnimationFrame(scrollFrame)
})
</script>

<style scoped>
.global-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 1000;
  background-color: transparent;
  padding: 0.4rem 0 0.5rem;
  transition: background-color 0.3s ease;
  border-bottom: 1px solid transparent;
}

/* 사진 위에서도 버건디 글자가 또렷하게 보이도록 상단에 부드러운 크림 그라디언트 */
.global-header::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(245, 240, 232, 0.85) 0%,
    rgba(245, 240, 232, 0.55) 60%,
    rgba(245, 240, 232, 0) 100%
  );
  pointer-events: none;
  z-index: -1;
  transition: opacity 0.3s ease;
}

.global-header.is-hovered,
.global-header.is-solid,
.global-header.is-mobile-open {
  background-color: #953735;
  border-bottom-color: rgba(0, 0, 0, 0.03);
}

.global-header.is-hovered::before,
.global-header.is-solid::before,
.global-header.is-mobile-open::before {
  opacity: 0;
}

/* Aesop-style: 메뉴는 페이지 상단이거나 커서가 상단에 올 때만 노출 */
.gnb {
  width: 100%;
  opacity: 1;
  max-height: 80px;
  transform: translateY(0);
  transition:
    opacity 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    max-height 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    margin-top 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.global-header.is-menu-collapsed .gnb {
  opacity: 0;
  max-height: 0;
  transform: translateY(-6px);
  margin-top: -0.6rem;
  pointer-events: none;
}

/* 모바일/터치 디바이스에서는 호버가 없으므로 항상 메뉴 노출 */
@media (hover: none) {
  .global-header.is-menu-collapsed .gnb {
    opacity: 1;
    max-height: 80px;
    transform: none;
    margin-top: 0;
    pointer-events: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .gnb {
    transition: none;
  }
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding: 0 2rem;
}

.logo-wrap {
  margin-bottom: 0.5rem;
}

.logo-link {
  display: inline-block;
  padding: 0;
  line-height: 0; /* img 아래 여분 공간 제거 */
}

.header-logo {
  display: block;
  height: 80px;
  aspect-ratio: 990 / 495;
  background-color: #953735;
  -webkit-mask-image: url('/logo-text.svg');
  mask-image: url('/logo-text.svg');
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  transition: background-color 0.3s ease;
}

.is-hovered .header-logo,
.is-solid .header-logo,
.is-mobile-open .header-logo {
  background-color: #F5F0E8;
}

.is-mobile-open .hamburger-line {
  background-color: #F5F0E8;
}

.gnb {
  width: 100%;
}

.gnb-list {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 5rem;
  padding: 0;
  margin: 0;
}

.gnb-link {
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
  color: #953735;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: geometricPrecision;
  text-decoration: none;
  padding: 0.5rem 0 0;
  position: relative;
  opacity: 0.9;
  transition: color 0.3s ease, opacity 0.3s ease;
}

.is-hovered .gnb-link,
.is-solid .gnb-link {
  color: #F5F0E8;
}

.gnb-link:hover, .gnb-link.is-active {
  opacity: 1;
}

.gnb-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 1px;
  background-color: currentColor;
  transition: width 0.3s ease;
  transform: translateX(-50%);
}

.gnb-link:hover::after, .gnb-link.is-active::after {
  width: 100%;
}

.header-utils {
  display: none;
}

/* ── Mobile hamburger toggle (hidden on desktop) ───── */
.menu-toggle {
  display: none;
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1100;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 5px;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  isolation: isolate;
}

.hamburger-line {
  display: block;
  width: 22px;
  height: 1.5px;
  background-color: #953735;
  transition: transform 0.3s ease, opacity 0.3s ease, background-color 0.3s ease;
  transform-origin: center;
}

.is-solid .hamburger-line {
  background-color: #F5F0E8;
}

.menu-toggle.is-open .hamburger-line:nth-child(1) {
  transform: translateY(6.5px) rotate(45deg);
}

.menu-toggle.is-open .hamburger-line:nth-child(2) {
  opacity: 0;
}

.menu-toggle.is-open .hamburger-line:nth-child(3) {
  transform: translateY(-6.5px) rotate(-45deg);
}

@media (max-width: 768px) {
  .global-header {
    padding: 0;
  }

  .header-inner {
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 0;
    height: 56px;
  }

  /* Logo on left, smaller */
  .logo-wrap {
    margin: 0;
    padding-left: 1rem;
  }

  .header-logo {
    height: 36px;
  }

  /* Show hamburger */
  .menu-toggle {
    display: flex;
  }

  /* GNB: hidden by default, slides down when open.
     Override desktop .is-menu-collapsed positioning. */
  .global-header .gnb,
  .global-header.is-menu-collapsed .gnb {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    width: 100%;
    background-color: #953735;
    overflow: hidden;
    max-height: 0;
    opacity: 0;
    pointer-events: none;
    transition:
      max-height 0.4s cubic-bezier(0.22, 1, 0.36, 1),
      opacity 0.3s ease;
    transform: none;
    margin: 0;
  }

  .global-header.is-mobile-open .gnb,
  .global-header.is-mobile-open.is-menu-collapsed .gnb {
    max-height: 360px;
    opacity: 1;
    pointer-events: auto;
    transform: none;
    margin: 0;
  }

  .gnb-list {
    flex-direction: column;
    gap: 0;
    padding: 0.4rem 0;
    margin: 0;
  }

  .gnb-list li {
    width: 100%;
  }

  .gnb-link {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 0.95rem 1.5rem;
    font-size: 14px;
    letter-spacing: 0.04em;
    color: #F5F0E8 !important;
    text-align: left;
    white-space: nowrap;
  }

  .gnb-link::after {
    display: none;
  }

  .gnb-link.is-active {
    background-color: rgba(0, 0, 0, 0.15);
  }
}
</style>
