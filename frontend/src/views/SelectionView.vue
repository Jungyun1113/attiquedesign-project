<template>
  <div class="selection-page" :class="[`view-${viewMode}`]">

    <!-- ═══════════════════════════════════════════ -->
    <!-- Hero View (Landing / Home)                  -->
    <!-- ═══════════════════════════════════════════ -->
    <template v-if="viewMode === 'hero'">

      <div class="hero-container">
        <!-- ── 섹션 1: 히어로 슬라이더 (상단 이미지 영역) ── -->
        <section class="sec-hero" @mouseenter="stopAutoplay" @mouseleave="startAutoplay">
          <div
            v-for="(slide, idx) in heroSlides"
            :key="'slide-' + idx"
            class="hero-slide"
            :class="{ 'is-active': activeSlide === idx }"
          >
            <template v-if="slide.type === 'single'">
              <img :src="slide.src" alt="ATTIQUE interior" class="hero-img-full" :loading="idx === 0 ? 'eager' : 'lazy'" />
            </template>
            <template v-else>
              <div class="hero-dual">
                <img :src="slide.src1" alt="ATTIQUE interior" class="hero-img-half" loading="lazy" />
                <img :src="slide.src2" alt="ATTIQUE interior" class="hero-img-half" loading="lazy" />
              </div>
            </template>
          </div>

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

        <!-- ── 섹션 2: 히어로 텍스트 (하단 텍스트 전용 영역) ── -->
        <section class="sec-hero-text">
          <div class="hero-text-content">
            <h2 class="brand-title">Living Edit · Space Creation</h2>
            <div class="brand-desc-wrap">
              <p class="brand-desc1">
                가구 큐레이션부터 인테리어 시공까지,<br class="mobile-br" />
                한남동 쇼룸에서 완성하는 하이엔드 토탈 리빙
              </p>
            </div>
          </div>
        </section>
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
            <div
              v-for="sel in selections"
              :key="sel.id"
              class="archive-item"
              :style="itemStyle"
              @click="viewSelection(sel.id)"
            >
              <div class="archive-img-wrap">
                <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" loading="lazy" />
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

    <!-- ═══════════════════════════════════════════ -->
    <!-- Grid Exhibition View (GNB Entry)            -->
    <!-- ═══════════════════════════════════════════ -->
    <div v-else class="sel-grid-view container-page">
      <header class="grid-header">
        <h1 class="grid-title">Living Edit · Space Creation.</h1>
        <p class="grid-subtitle">아띠끄의 안목으로 엄선한 가구와 오브제.</p>
        <p class="grid-desc">미국과 유럽에서 직수입한 셀렉션을 한남동 쇼룸에서 만나보실 수 있습니다.</p>
      </header>

      <div class="grid-container">
        <div
          v-for="sel in selections"
          :key="sel.id"
          class="archive-item"
          @click="viewSelection(sel.id)"
        >
          <div class="archive-img-wrap">
            <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" loading="lazy" />
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
  { type: 'single', src: '/images/hero/hero-01.png' },
  { type: 'single', src: '/images/hero/hero-02.png' },
  { type: 'single', src: '/images/hero/hero-03.png' },
]

const heroSlides = ref<HeroSlide[]>(fallbackSlides)
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
  }, 4500)
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

async function loadData() {
  try {
    // 1. 슬라이더 전용 데이터 (category: 'slider')
    const sliderData = await selectionService.getSelections({ category: 'slider', limit: 20 })
    
    // 2. 전체 셀렉션 데이터
    const allData = await selectionService.getSelections({ limit: 100 })

    // 로컬 이미지 기반 슬라이더 구성 (S3 이슈 대응 및 사용자 요청 반영)
    heroSlides.value = [
      { type: 'single', src: '/images/hero/hero-01.png' },
      { type: 'single', src: '/images/hero/hero-02.png' },
      { type: 'single', src: '/images/hero/hero-03.png' },
      { type: 'dual',   src1: '/images/hero/hero-04.png', src2: '/images/hero/hero-05.png' } // 마지막 듀얼 슬라이드
    ]

    // 슬라이더가 아닌 셀렉션만 제품 영역에 표시
    selections.value = allData.filter((s: Selection) => s.category !== 'slider')
  } catch (error) {
    console.error('Data loading failed:', error)
    selections.value = []
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

const GAP = 16

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
}

/* ── 섹션 1: 이미지 영역 ── */
.sec-hero {
  flex: 1; /* 남은 공간 차지 */
  position: relative;
  width: 100%;
  max-height: 70vh; /* PC에서 이미지 영역 제한 */
  overflow: hidden;
  background-color: #F5F0E8; /* 검은색에서 아이보리로 변경 */
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
    height: calc(100vh - 190px) !important; /* 헤더 높이를 넉넉히 제외하여 문구까지 한 화면에 고정 */
  }
  .sec-hero {
    flex: 1;
    height: auto;
    max-height: none;
  }
  .hero-img-full {
    object-fit: contain; /* 단일 사진 전체 표시 */
  }
  .hero-img-half {
    object-fit: contain; /* 듀얼 사진도 자르지 않고 전체 표시 */
  }
  /* 두 사진이 가운데서 달라붙도록 각각 정렬 */
  .hero-img-half:first-child {
    object-position: right; 
  }
  .hero-img-half:last-child {
    object-position: left;
  }
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
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: all 0.3s ease;
}

.indicator-dot.is-active {
  background: #fff;
  transform: scale(1.4);
}

/* ── 섹션 2: 텍스트 영역 ── */
.sec-hero-text {
  height: 22vh;
  min-height: 160px;
  background-color: #F5F0E8;
  display: flex;
  align-items: center; /* 세로 중앙 */
  padding: 0 8%; /* 기본 여백 */
}

.hero-text-content {
  width: 100%;
  max-width: 1200px;
  text-align: left;
}

@media (min-width: 1024px) {
  .sec-hero-text {
    height: auto; 
    padding: 2rem 0 3rem; 
    justify-content: center;
  }
  .hero-text-content {
    /* 사진의 일반적인 너비(3:2 비율 기준 약 100vh)를 고려하여 최대 너비 설정 */
    max-width: 100vh; 
    padding: 0 2rem;
  }
}

.brand-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.4rem;
  font-weight: 400;
  font-style: italic;
  line-height: 1.2;
  color: #000000;
  margin: 0;
  letter-spacing: -0.01em;
}

.brand-desc-wrap {
  margin-top: 1rem; /* 간격 축소 */
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.brand-desc1 {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #000000;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
}

.brand-desc2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 300;
  color: #000000;
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
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 1rem;
}

.archive-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  color: #2C2C2A;
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

/* ── 모바일 최적화 ── */
@media (max-width: 768px) {
  .hero-container {
    height: 100vh;
  }

  .hero-container {
    height: calc(100vh - 120px); /* 헤더 높이 제외한 전체 화면 */
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .sec-hero {
    height: 48vh; /* 이미지 영역을 줄여서 문구가 보이도록 조정 */
    max-height: 48vh;
  }

  .sec-hero-text {
    flex: 1;
    height: auto;
    padding: 1.5rem 1.5rem 0; /* 하단 여백을 0.5rem에서 0으로 완전히 제거 */
    align-items: flex-start; /* 문구를 상단으로 밀착 */
  }

  .brand-title {
    font-size: 1.6rem;
    margin-bottom: 0.8rem;
  }

  .brand-desc-wrap {
    margin-top: 0.8rem;
    gap: 0.4rem;
  }

  .brand-desc1 {
    font-size: 13px;
  }

  .brand-desc2 {
    font-size: 11px;
    opacity: 0.6;
  }

  /* 인디케이터 위치 조정 */
  .hero-indicators {
    bottom: 12px;
  }

  .sec-selection {
    padding: 0 1.5rem 4rem; /* 상단 여백을 완전히 제거하여 본문을 위로 밀착 */
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
  padding: 4rem 8% 8rem;
}

.grid-header {
  margin-bottom: 5rem;
  text-align: left;
}

.grid-title {
  font-family: 'Playfair Display', serif;
  font-size: 3.2rem;
  color: #111;
  margin-bottom: 1.5rem;
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
  .grid-container {
    grid-template-columns: 1fr;
  }
  .grid-title {
    font-size: 2.2rem;
  }
}
</style>
