<template>
  <div class="selection-page" :class="[`view-${viewMode}`]">

    <!-- ═══════════════════════════════════════════ -->
    <!-- Hero View (Landing / Home)                  -->
    <!-- ═══════════════════════════════════════════ -->
    <template v-if="viewMode === 'hero'">

      <div class="hero-container">
        <!-- ── 풀블리드 히어로 슬라이더 (Chanel-style) ── -->
        <section class="sec-hero" @mouseenter="stopAutoplay" @mouseleave="startAutoplay">
          <div
            v-for="(slide, idx) in heroSlides"
            :key="'slide-' + idx"
            class="hero-slide"
            :class="{ 'is-active': activeSlide === idx }"
          >
            <template v-if="slide.type === 'single'">
              <img 
                :src="slide.src" 
                alt="ATTIQUE interior" 
                class="hero-img-full" 
                :loading="idx === 0 ? 'eager' : 'lazy'"
                :fetchpriority="idx === 0 ? 'high' : undefined"
                :decoding="idx === 0 ? undefined : 'async'"
              />
            </template>
            <template v-else>
              <div class="hero-dual">
                <img 
                  :src="slide.src1" 
                  alt="ATTIQUE interior" 
                  class="hero-img-half" 
                  :loading="idx === 0 ? 'eager' : 'lazy'"
                  :fetchpriority="idx === 0 ? 'high' : undefined"
                  :decoding="idx === 0 ? undefined : 'async'"
                />
                <img 
                  :src="slide.src2" 
                  alt="ATTIQUE interior" 
                  class="hero-img-half" 
                  :loading="idx === 0 ? 'eager' : 'lazy'"
                  :fetchpriority="idx === 0 ? 'high' : undefined"
                  :decoding="idx === 0 ? undefined : 'async'"
                />
              </div>
            </template>
          </div>

          <!-- ── 이미지 위 에디토리얼 텍스트 오버레이 (Chanel-style) ── -->
          <div class="hero-overlay">
            <h2 class="brand-title">Living Edit · Space Creation</h2>
            <p class="brand-desc1">
              가구 큐레이션부터 인테리어 시공까지,<br class="mobile-br" />
              한남동 쇼룸에서 완성하는 하이엔드 토탈 리빙
            </p>
          </div>

          <!-- ── 텍스트 가독성용 하단 비네팅 ── -->
          <div class="hero-vignette"></div>

          <!-- 슬라이드 인디케이터 -->
          <div class="hero-indicators" v-if="heroSlides.length > 1">
            <button
              v-for="(_, idx) in heroSlides"
              :key="'dot-' + idx"
              class="indicator-dot"
              :class="{ 'is-active': activeSlide === idx }"
              @click="goToSlide(idx)"
            />
          </div>
        </section>

        <!-- 모바일 전용 스크롤 인디케이터 -->
        <div class="scroll-indicator mobile-only">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
      </div>

      <!-- ── 섹션 3: 제품 슬라이더 (스크롤해야 보임) ── -->
      <section class="sec-selection">
        <div class="selection-header">
          <span class="selection-spacer"></span>
          <p class="selection-label">ATTIQUE SELECTION</p>
          <div class="selection-arrows">
            <button class="arrow-btn" :disabled="prodOffset === 0" @click="prodPrev">&#8249;</button>
            <button class="arrow-btn" :disabled="prodOffset >= maxOffset" @click="prodNext">&#8250;</button>
          </div>
        </div>
        <div class="prod-slider-wrap" ref="sliderWrapRef">
          <div class="prod-track" :style="trackStyle">
            <!-- 로딩 중 스켈레톤 -->
            <template v-if="isDataLoading && !selections.length">
              <div v-for="n in 3" :key="'skeleton-'+n" class="archive-item skeleton" :style="itemStyle">
                <div class="archive-img-wrap skeleton-img"></div>
                <div class="skeleton-info"></div>
              </div>
            </template>
            
            <!-- 실제 데이터 -->
            <div
              v-for="sel in selections"
              :key="sel.id"
              class="archive-item"
              :style="itemStyle"
              @click="viewSelection(sel.id)"
            >
              <div class="archive-img-wrap">
                <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" class="fade-in" @load="(e) => (e.target as HTMLElement).classList.add('loaded')" @error="(e) => (e.target as HTMLElement).classList.add('loaded')" />
              </div>
              <div class="archive-info">
                <h3 class="archive-name">{{ sel.title }}</h3>
                <button class="archive-btn">VIEW DETAILS</button>
              </div>
            </div>
          </div>
        </div>
      </section>

    </template>

    <!-- Grid Exhibition View (GNB Entry)            -->
    <!-- ═══════════════════════════════════════════ -->
    <div v-else class="global-page-container sel-grid-view">
      <header class="grid-header">
        <h1 class="global-eng-subtitle grid-title">Living Edit · <em>Space Creation.</em></h1>
        <p class="global-kor-desc grid-subtitle">제품당 1~2점만 입고되는 희소성 있는 셀렉션.</p>
        <p class="global-kor-desc grid-desc" style="opacity: 0.7; margin-top: 0.5rem;">한정 수량의 수입 오브제를 한남 쇼룸에서 직접 경험해 보세요.</p>
      </header>

      <div class="grid-container">
        <!-- 로딩 중 스켈레톤 -->
        <template v-if="isDataLoading && !selections.length">
          <div v-for="n in 8" :key="'grid-skeleton-'+n" class="archive-item skeleton">
            <div class="archive-img-wrap skeleton-img"></div>
            <div class="skeleton-info"></div>
          </div>
        </template>

        <!-- 실제 데이터 -->
        <div
          v-for="sel in selections"
          :key="sel.id"
          class="archive-item"
          @click="viewSelection(sel.id)"
        >
          <div class="archive-img-wrap">
            <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" class="fade-in" @load="(e) => (e.target as HTMLElement).classList.add('loaded')" @error="(e) => (e.target as HTMLElement).classList.add('loaded')" />
          </div>
          <div class="archive-info">
            <h3 class="archive-name">{{ sel.title }}</h3>
            <button class="archive-btn">VIEW DETAILS</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { selectionService, type Selection } from '@/services/selection.service'

const router = useRouter()
const route = useRoute()

const viewMode = computed(() => (route.query.view === 'grid' ? 'grid' : 'hero'))

// ── 히어로 슬라이더 ──────────────────────────
type SingleSlide = { type: 'single'; src: string }
type DualSlide   = { type: 'dual';   src1: string; src2: string }
type HeroSlide   = SingleSlide | DualSlide

const fallbackSlides: HeroSlide[] = [
  { type: 'single', src: '/images/hero/hero-01.jpg' },
  { type: 'single', src: '/images/hero/hero-02.jpg' },
  { type: 'single', src: '/images/hero/hero-03.jpg' },
]

const heroSlides = ref<HeroSlide[]>([
  { type: 'single', src: '/images/hero/hero-01.jpg' },
  { type: 'single', src: '/images/hero/hero-02.jpg' },
  { type: 'single', src: '/images/hero/hero-03.jpg' },
  { type: 'dual',   src1: '/images/hero/hero-04.jpg', src2: '/images/hero/hero-05.jpg' }
])
const activeSlide = ref(0)
let autoplayTimer: ReturnType<typeof setInterval> | null = null

const currentLength = computed(() => heroSlides.value.length)

function goToSlide(idx: number) {
  activeSlide.value = idx
}

function startAutoplay() {
  stopAutoplay()
  if (currentLength.value <= 1) return
  autoplayTimer = setInterval(() => {
    activeSlide.value = (activeSlide.value + 1) % currentLength.value
  }, 2000)
}

function stopAutoplay() {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

const isMobile = ref(window.innerWidth <= 768)

function handleResize() {
  const wasMobile = isMobile.value
  isMobile.value = window.innerWidth <= 768
  if (wasMobile !== isMobile.value) {
    activeSlide.value = 0
    prodOffset.value = 0
    startAutoplay()
  }
  updateWrapWidth()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  updateWrapWidth()
  startAutoplay()
  loadData()
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  stopAutoplay()
})

// ── 데이터 로딩 ──────────────────────────
const selections = ref<Selection[]>([])
const isDataLoading = ref(true)

async function loadData() {
  try {
    isDataLoading.value = true
    // 1. 슬라이더 전용 데이터 (category: 'slider')
    await selectionService.getSelections({ category: 'slider', limit: 20 })
    
    // 2. 전체 셀렉션 데이터 (초기 로딩량 최적화: 100 -> 24)
    const allData = await selectionService.getSelections({ limit: 24 })

    // 슬라이더가 아닌 셀렉션만 제품 영역에 표시
    selections.value = allData.filter((s: Selection) => s.category !== 'slider')
  } catch (error) {
    console.error('Data loading failed:', error)
    selections.value = []
  } finally {
    isDataLoading.value = false
  }
}

function viewSelection(selectionId: string) {
  router.push(`/selection/${selectionId}`)
}

// ── 제품 슬라이더 ──────────────────────────
const sliderWrapRef = ref<HTMLElement | null>(null)
const wrapWidth = ref(0)
const prodOffset = ref(0)

const itemsPerView = computed(() => isMobile.value ? 2 : 3)
const maxOffset = computed(() => Math.max(0, selections.value.length - itemsPerView.value))

const GAP = 20

const trackStyle = computed(() => {
  if (!wrapWidth.value) return {}
  const n = itemsPerView.value
  const itemW = (wrapWidth.value - GAP * (n - 1)) / n
  const px = prodOffset.value * (itemW + GAP)
  return { transform: `translateX(-${px}px)` }
})

const itemStyle = computed(() => {
  if (!wrapWidth.value) return {}
  const n = itemsPerView.value
  const itemW = (wrapWidth.value - GAP * (n - 1)) / n
  return { width: `${itemW}px` }
})

function prodPrev() {
  prodOffset.value = Math.max(0, prodOffset.value - 1)
}

function prodNext() {
  prodOffset.value = Math.min(maxOffset.value, prodOffset.value + 1)
}

function updateWrapWidth() {
  wrapWidth.value = sliderWrapRef.value?.offsetWidth ?? 0
}
</script>

<style scoped>
.selection-page {
  background-color: #F5F0E8;
  width: 100%;
}

/* ── 히어로 컨테이너: 100vh 고정 ── */
.hero-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #F5F0E8;
  position: relative;
}

/* ── 풀블리드 히어로 (Chanel-style: 이미지가 전체 영역 차지) ── */
.sec-hero {
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #1a1a1a; /* 이미지 로딩 전 다크 배경 */
}

.hero-slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-slide.is-active {
  opacity: 1;
}

.hero-img-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.hero-dual {
  display: flex;
  width: 100%;
  height: 100%;
  gap: 0; /* 사진 사이 간격 제거 */
}

.hero-img-half {
  flex: 1;
  min-width: 0;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

@media (min-width: 1024px) {
  .hero-container {
    height: calc(100vh - 90px) !important; /* 헤더 공간 확보 */
  }
  .sec-hero {
    height: 100%;
  }
  /* PC도 cover 유지 — 이미지가 가장자리까지 꽉 채워지는 풀블리드 (Chanel-style) */
}

.hero-indicators {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}

.indicator-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: all 0.3s ease;
}

.indicator-dot.is-active {
  background: #fff;
  transform: scale(1.25);
}

/* ── 이미지 위 에디토리얼 오버레이 (Chanel-style) ── */
.hero-overlay {
  position: absolute;
  left: 4rem;
  bottom: 4rem;
  z-index: 5;
  max-width: 560px;
  pointer-events: none;
}

.hero-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.55) 0%,
    rgba(0, 0, 0, 0.15) 35%,
    transparent 60%);
  z-index: 2;
  pointer-events: none;
}

.brand-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 4vw, 3.4rem);
  font-weight: 400;
  font-style: italic;
  line-height: 1.15;
  color: #FFFFFF;
  margin: 0;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 24px rgba(0, 0, 0, 0.25);
}

.brand-desc1 {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.6;
  margin: 1.2rem 0 0;
  word-break: keep-all;
  text-shadow: 0 1px 12px rgba(0, 0, 0, 0.35);
}

.brand-desc2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 300;
  color: #2C2C2C;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
}

.mobile-br {
  display: none;
}

@media (max-width: 768px) {
  .mobile-br {
    display: block;
  }
}

.sec-selection {
  padding: 1.5rem 8% 6rem; /* 상단 여백을 5rem -> 1.5rem으로 대폭 축소 */
  background-color: #F5F0E8;
}

.selection-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.selection-label {
  font-family: 'Montserrat', sans-serif;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.2em;
  color: #888780;
  text-transform: uppercase;
  margin: 0;
}

.selection-arrows {
  display: flex;
  gap: 8px;
}

.arrow-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #2C2C2A;
  background: transparent;
  border: 1px solid rgba(44, 44, 42, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
}

.arrow-btn:hover:not(:disabled) {
  background: #2C2C2A;
  color: #F5F0E8;
  border-color: #2C2C2A;
}

.arrow-btn:disabled {
  opacity: 0.2;
  cursor: default;
}

.prod-slider-wrap {
  overflow: hidden;
}

.prod-track {
  display: flex;
  gap: 20px;
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

.archive-item {
  flex: 0 0 auto;
  cursor: pointer;
}

.archive-img-wrap {
  width: 100%;
  aspect-ratio: 4 / 5;
  background-color: #F5F0E8;
  overflow: hidden;
  margin-bottom: 1rem;
}

.archive-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.8s ease;
}

.archive-item:hover .archive-img-wrap img {
  transform: scale(1.04);
}

.archive-info {
  text-align: left;
}

.archive-name {
  font-family: 'Raleway', sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #2C2C2C;
  margin: 0 0 0.8rem;
}

.archive-btn {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.1em;
  color: #312E2D;
  background: transparent;
  border: 1px solid rgba(49, 46, 45, 0.2);
  padding: 0.5rem 1rem;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.archive-btn:hover {
  background: #312E2D;
  color: #F5F0E8;
}

.scroll-indicator {
  display: none;
}

/* ── 모바일 최적화 ── */
@media (max-width: 768px) {
  .scroll-indicator.mobile-only {
    display: flex;
    position: absolute;
    bottom: 2rem; /* 풀블리드 이미지 하단으로 이동 */
    left: 50%;
    transform: translateX(-50%);
    color: rgba(255, 255, 255, 0.7); /* 어두운 이미지 위 가독성 */
    animation: bounce 2.5s infinite;
    z-index: 10;
    justify-content: center;
  }
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0) translateX(-50%); }
    40% { transform: translateY(-8px) translateX(-50%); }
    60% { transform: translateY(-4px) translateX(-50%); }
  }

  .hero-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  .sec-hero {
    flex: 1;
    height: 100%;
    position: relative;
  }

  .hero-overlay {
    left: 1.5rem;
    right: 1.5rem;
    bottom: 5rem;
    max-width: none;
  }

  .brand-title {
    font-size: 1.7rem;
  }

  .brand-desc1 {
    font-size: 13px;
    margin-top: 0.8rem;
  }

  /* 인디케이터 위치 조정 */
  .hero-indicators {
    bottom: 12px; /* 이미지가 38svh로 고정되었으므로 다시 하단 12px 위치로 복구 */
  }

  .selection-header {
    margin-bottom: 1.2rem; /* 헤더와 사진 사이 간격을 줄여 사진이 더 많이 보이게 함 */
  }

  .sec-selection {
    padding: 0.5rem 1.5rem 4rem; 
  }

  .archive-img-wrap {
    margin-bottom: 0.8rem;
  }

  .archive-name {
    font-size: 12px;
  }
}

/* GNB 그리드 뷰 */
.sel-grid-view {
  /* 글로벌 컨테이너가 기본 padding 제공 */
}

.grid-header {
  text-align: left;
  margin-bottom: 5rem; /* PC에서 사진과의 여백 확보 */
}

@media (max-width: 768px) {
  .grid-header {
    margin-bottom: 3rem; /* 모바일은 기존 여백 유지 */
  }
}

.grid-title {
  white-space: nowrap; /* 타이틀만 줄바꿈 방지 */
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem 2rem;
}

@media (max-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .grid-header {
    margin-bottom: 2.5rem;
  }
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem 1rem;
  }
}

/* ── 스켈레톤 & 애니메이션 ── */
.fade-in {
  opacity: 0;
  transition: opacity 0.8s ease-out;
}
.fade-in.loaded {
  opacity: 1;
}

.skeleton-img {
  background: linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-info {
  width: 60%;
  height: 14px;
  background: #eee;
  margin-top: 10px;
  border-radius: 2px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
