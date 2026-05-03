<template>
  <header class="global-header" :class="{ 'is-scrolled': scrolled, 'is-menu-collapsed': menuCollapsed, 'is-hovered': hovered, 'is-solid': !isHeroRoute }">
    <div class="header-inner">
      <!-- Logo Center -->
      <div class="logo-wrap">
        <router-link to="/selection" class="logo-link" aria-label="ATTIQUE DESIGN">
          <span class="header-logo" role="img" aria-hidden="true"></span>
        </router-link>
      </div>

      <!-- Navigation Bottom -->
      <nav class="gnb">
        <ul class="gnb-list">
          <li v-for="item in menuItems" :key="item.path">
            <router-link 
              :to="item.path" 
              class="gnb-link" 
              :class="{ 'is-active': isLinkActive(item) }"
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isHeroRoute = computed(
  () => route.path === '/selection' && route.query.view !== 'grid'
)
const scrolled = ref(false)
const menuCollapsed = ref(isHeroRoute.value)
const hoveredRaw = ref(false)
const hovered = computed(() => hoveredRaw.value && isHeroRoute.value)
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
.global-header.is-solid {
  background-color: #953735;
  border-bottom-color: rgba(0, 0, 0, 0.03);
}

.global-header.is-hovered::before,
.global-header.is-solid::before {
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
.is-solid .header-logo {
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

@media (max-width: 768px) {
  .global-header {
    padding: 0.5rem 0 0.4rem;
  }
  .logo-wrap {
    margin-bottom: 0.4rem;
  }
  .header-inner {
    padding: 0 1rem;
  }
  .gnb-list {
    gap: 0.6rem 0.7rem; /* 한 줄에 다 들어오도록 메뉴 간격 축소 */
    flex-wrap: nowrap; /* 강제로 한 줄 유지 */
    justify-content: center;
    overflow-x: auto; /* 너무 작은 화면에서는 가로 스크롤 허용 (하지만 기본적으로 맞도록 설정) */
  }
  .gnb-link {
    font-size: 11px;
    letter-spacing: 0.05em;
    white-space: nowrap;
  }
  .logo-link {
    padding: 0;
  }
  .header-utils {
    display: none;
  }
}
</style>
