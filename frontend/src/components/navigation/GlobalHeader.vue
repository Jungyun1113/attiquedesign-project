<template>
  <header class="global-header" :class="{ 'is-scrolled': scrolled }">
    <div class="header-inner">
      <!-- Logo Center -->
      <div class="logo-wrap">
        <router-link to="/selection" class="logo-link">
          <img src="/logo.svg" alt="ATTIQUE DESIGN" class="header-logo" />
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const scrolled = ref(false)
const menuItems = [
  { label: 'About', path: '/philosophy' },
  { label: 'Interior', path: '/interior' },
  { label: 'Selection', path: '/selection?view=grid' },
  { label: 'Portfolio', path: '/portfolio' },
  { label: 'Contact', path: '/contact' },
]

function isLinkActive(item: { label: string; path: string }) {
  // 1. Selection의 경우: 경로가 /selection 이고 query.view가 grid일 때만 active
  if (item.label === 'Selection') {
    return route.path === '/selection' && route.query.view === 'grid'
  }
  
  // 2. 나머지는 단순 경로 포함 여부 (또는 완전 일치)로 판단
  // router-link의 기본 active 로직과 유사하게 구현
  return route.path.startsWith(item.path.split('?')[0])
}

function handleScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.global-header {
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 1000;
  background-color: #F5F0E8;
  padding: 1rem 0 1.2rem;
  transition: all 0.4s ease;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
}

.global-header.is-scrolled {
  padding: 0.7rem 0 0.8rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
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
  margin-bottom: 0.8rem;
  transition: transform 0.4s ease;
}

.logo-link {
  display: inline-block;
  background-color: #953735;
  padding: 0 1.4rem;
  line-height: 0; /* img 아래 여분 공간 제거 */
}

.is-scrolled .logo-wrap {
  transform: scale(0.65);
  margin-bottom: 0.4rem;
}

.header-logo {
  height: 87px;
  width: auto;
  display: block;
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
  font-family: 'Raleway', sans-serif;
  font-size: 13px; /* 모바일과 비슷한 비율로 글씨를 더 키움 (기존 11px) */
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.15em; /* 글씨가 커진 만큼 자간을 살짝 좁힘 (기존 0.3em) */
  color: #222222;
  text-decoration: none;
  padding: 0.5rem 0 0;
  position: relative;
  opacity: 0.8;
  transition: opacity 0.3s ease;
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
  background-color: #953735;
  transition: all 0.3s ease;
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
    padding: 1.4rem 0 0.4rem; /* 상단 여백을 늘려 로고를 살짝 아래로 내림 */
  }
  .logo-wrap {
    margin-bottom: 0.8rem; /* 로고가 내려온 만큼 메뉴와의 간격을 좁힘 */
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
    font-size: 10.5px; /* 한 줄에 들어올 수 있도록 12px에서 소폭 축소 */
    letter-spacing: 0.05em; /* 글자 간격 축소 */
    white-space: nowrap;
  }
  .header-logo {
    height: 65px;
  }
  .logo-link {
    padding: 0 1rem;
  }
  .header-utils {
    display: none;
  }
}
</style>
