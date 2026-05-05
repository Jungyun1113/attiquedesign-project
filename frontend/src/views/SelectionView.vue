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
            <h2 class="brand-title" v-reveal="{ delay: 200 }">Curated Living · Crafted Spaces</h2>
            <p class="brand-desc1" v-reveal="{ delay: 500 }">
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

      <!-- ═════ Brand intro — editorial introduction ═════ -->
      <section class="sec-intro" v-reveal>
        <div class="intro-inner">
          <span class="intro-kicker">ATTIQUE DESIGN</span>
          <h2 class="intro-title">
            공간에 깊이를 더하는,<br /><em>아띠끄 디자인.</em>
          </h2>
          <p class="intro-body">
            한남 쇼룸을 거점으로 인테리어 시공과 가구·소품 큐레이션을<br />
            함께 운영하는 인테리어 스튜디오입니다.<br /><br />
            미국과 유럽의 하이엔드 메종에서 직접 들여온 셀렉션과<br />
            1:1 맞춤 시공으로, 2012년부터 고객만의 공간을 완성해왔습니다.
          </p>
          <router-link to="/philosophy" class="intro-link">
            <span>More About Us</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="7" y1="17" x2="17" y2="7"></line>
              <polyline points="7 7 17 7 17 17"></polyline>
            </svg>
          </router-link>
        </div>
      </section>

      <!-- ═════ Editorial gallery — 3-up asymmetric ═════ -->
      <section class="sec-gallery">
        <div class="gallery-grid">
          <figure class="gallery-item gallery-lead" v-reveal="{ delay: 100 }">
            <img
              src="/images/showroom-building.png"
              alt="ATTIQUE DESIGN — Hannam showroom"
              loading="lazy"
            />
            <figcaption class="gallery-caption">
              <span class="gallery-place">HANNAM</span>
              <span class="gallery-sep"></span>
              <span class="gallery-text">Showroom</span>
            </figcaption>
          </figure>

          <figure class="gallery-item gallery-top" v-reveal="{ delay: 200 }">
            <img
              src="/images/about/original_second.png"
              alt="ATTIQUE DESIGN — Cheongdam archive"
              loading="lazy"
            />
            <figcaption class="gallery-caption">
              <span class="gallery-place">CHEONGDAM</span>
              <span class="gallery-sep"></span>
              <span class="gallery-text">Archive</span>
            </figcaption>
          </figure>

          <figure class="gallery-item gallery-bottom" v-reveal="{ delay: 300 }">
            <img
              src="/images/contact/consultation-table.png"
              alt="ATTIQUE DESIGN — Consultation table"
              loading="lazy"
            />
            <figcaption class="gallery-caption">
              <span class="gallery-place">PRIVATE</span>
              <span class="gallery-sep"></span>
              <span class="gallery-text">Consultation</span>
            </figcaption>
          </figure>
        </div>
      </section>

      <!-- ═════ Curation process — text + CTA to grid ═════ -->
      <section class="sec-curation" v-reveal>
        <div class="curation-inner">
          <span class="curation-kicker">SELECTION</span>
          <h2 class="curation-title">
            엄선된 셀렉션,<br /><em>아띠끄 디자인의 시선.</em>
          </h2>
          <p class="curation-body">
            해외 메종과 공방에서 직접 엄선한 가구와 오브제.<br /><br />
            한남 쇼룸의 1:1 프라이빗 컨설테이션을 통해 고객의 라이프스타일을 깊이 이해한 후,<br />
            선별된 셀렉션과 맞춤 시공으로 공간을 완성합니다.
          </p>
          <p class="curation-closer">
            큐레이션 · 컨설테이션 · 시공, 한자리에서.
          </p>
          <router-link to="/selection?view=grid" class="curation-cta">
            <span>View All Selection</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <line x1="7" y1="17" x2="17" y2="7"></line>
              <polyline points="7 7 17 7 17 17"></polyline>
            </svg>
          </router-link>
        </div>
      </section>

      <!-- ── 섹션 3: 제품 슬라이더 (refined Chanel-style) ── -->
      <section class="sec-selection">
        <div class="selection-header" v-reveal>
          <span class="selection-counter" v-if="selections.length">
            <span class="counter-current">{{ formattedSlideIndex }}</span>
            <span class="counter-divider"></span>
            <span class="counter-total">{{ formattedSlideTotal }}</span>
          </span>
          <span v-else class="selection-counter selection-counter-placeholder">— / —</span>
          <div class="selection-arrows">
            <button
              class="arrow-btn"
              :disabled="prodOffset === 0"
              @click="prodPrev"
              aria-label="Previous"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
            </button>
            <button
              class="arrow-btn"
              :disabled="prodOffset >= maxOffset"
              @click="prodNext"
              aria-label="Next"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </button>
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
              v-for="(sel, i) in selections"
              :key="sel.id"
              class="archive-item"
              :style="itemStyle"
              v-reveal="{ delay: i * 120 }"
              @click="viewSelection(sel.id)"
            >
              <div class="archive-img-wrap">
                <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" />
              </div>
              <div class="archive-info">
                <h3 class="archive-name">{{ sel.title }}</h3>
              </div>
            </div>
          </div>
        </div>

        <!-- Hermès-style thin progress track -->
        <div class="prod-progress" v-if="selections.length > 1">
          <div class="prod-progress-track">
            <div
              class="prod-progress-bar"
              :style="{
                width: progressBarWidth + '%',
                left: progressBarLeft + '%'
              }"
            ></div>
          </div>
        </div>
      </section>

    </template>

    <!-- Grid Exhibition View (GNB Entry)            -->
    <!-- ═══════════════════════════════════════════ -->
    <template v-else>
      <!-- ═════ Chanel-style merchandise bar ═════ -->
      <section class="sel-banner">
        <img
          src="/images/selection-bar.png"
          alt="ATTIQUE Selection"
          class="sel-banner-img"
          fetchpriority="high"
        />
        <div class="sel-banner-vignette"></div>
        <div class="sel-banner-overlay">
          <div class="sel-banner-stack">
            <span class="sel-banner-kr">셀렉션</span>
            <h1 class="sel-banner-en">Selection</h1>
          </div>
        </div>
      </section>

    <div class="global-page-container sel-grid-view">
      <header class="grid-header" v-reveal>
        <p class="global-kor-desc grid-subtitle">오랜 안목으로 골라낸, 단 한두 점의 오브제.</p>
        <p class="global-kor-desc grid-desc" style="opacity: 0.7; margin-top: 0.5rem;">
          미국과 유럽의 메종과 공방을 직접 찾아, 한 점씩 정성스럽게 들여옵니다.<br />
          클래식과 모던, 빈티지와 컨템포러리가 자연스럽게 어우러지는 조합 안에서<br />
          같은 디자인을 두 번 마주할 수 없는, 한남 쇼룸만의 셀렉션이 완성됩니다.<br /><br />
          한 점에 깃든 시간과 손길, 한남 쇼룸에서 직접 마주하실 수 있습니다.
        </p>
      </header>

      <!-- ═════ Filter / sort toolbar (acts as boundary) ═════ -->
      <div class="grid-toolbar" v-reveal>
        <ul class="filter-list">
          <li
            class="filter-item"
            :class="{ 'is-active': activeCategory === null }"
            @click="activeCategory = null"
          >
            <span>전체</span>
            <span class="filter-count">{{ selections.length }}</span>
          </li>
          <li
            v-for="cat in allCategories"
            :key="cat"
            class="filter-item"
            :class="{ 'is-active': activeCategory === cat }"
            @click="activeCategory = cat"
          >
            <span>{{ cat }}</span>
            <span class="filter-count">{{ countByCategory(cat) }}</span>
          </li>
        </ul>

        <div class="sort-control">
          <label for="sel-sort" class="sort-label">정렬</label>
          <select id="sel-sort" v-model="sortMode" class="sort-select">
            <option value="default">기본</option>
            <option value="asc">이름순 A–Z</option>
            <option value="desc">이름순 Z–A</option>
          </select>
        </div>
      </div>

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
          v-for="(sel, i) in displayedSelections"
          :key="sel.id"
          class="archive-item"
          v-reveal="{ delay: (i % 6) * 90 }"
          @click="viewSelection(sel.id)"
        >
          <div class="archive-img-wrap">
            <img :src="sel.images?.[0]?.image_url ?? ''" :alt="sel.title" />
          </div>
          <div class="archive-info">
            <h3 class="archive-name">{{ sel.title }}</h3>
          </div>
        </div>
      </div>
    </div>
    </template>

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
  }, 5000)
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

// ── Filter / sort ────────────────────────
const activeCategory = ref<string | null>(null)
const sortMode = ref<'default' | 'asc' | 'desc'>('default')

const allCategories = computed(() => {
  const set = new Set<string>()
  for (const s of selections.value) {
    if (s.category) set.add(s.category)
  }
  return [...set].sort()
})

function countByCategory(cat: string) {
  return selections.value.filter(s => s.category === cat).length
}

const displayedSelections = computed(() => {
  let items = selections.value
  if (activeCategory.value) {
    items = items.filter(s => s.category === activeCategory.value)
  }
  if (sortMode.value !== 'default') {
    items = [...items].sort((a, b) =>
      sortMode.value === 'asc'
        ? a.title.localeCompare(b.title, 'ko')
        : b.title.localeCompare(a.title, 'ko')
    )
  }
  return items
})

async function loadData() {
  try {
    isDataLoading.value = true
    // 전체 셀렉션 데이터
    const allData = await selectionService.getSelections({ limit: 500 })

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

// ── Slider counter / progress ──────────────
const formattedSlideIndex = computed(() =>
  String(prodOffset.value + 1).padStart(2, '0')
)
const formattedSlideTotal = computed(() =>
  String(selections.value.length).padStart(2, '0')
)
const progressBarWidth = computed(() => {
  const total = selections.value.length
  if (total === 0) return 0
  return (itemsPerView.value / total) * 100
})
const progressBarLeft = computed(() => {
  const total = selections.value.length
  if (total === 0) return 0
  return (prodOffset.value / total) * 100
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
    height: 100vh !important; /* 헤더가 오버레이되므로 풀 뷰포트 */
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
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(1.6rem, 3vw, 2.6rem);
  font-weight: 400;
  font-style: italic;
  line-height: 1.15;
  color: #FFFFFF;
  margin: 0;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 24px rgba(0, 0, 0, 0.25);
  white-space: nowrap;
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

/* ── Brand intro section ─────────────────────────────── */
.sec-intro {
  background-color: #F5F0E8;
  padding: 7rem 4rem 5rem;
}

.intro-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.4rem;
}

.intro-kicker {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: #7E1A2C;
  text-transform: uppercase;
}

.intro-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(1.8rem, 3.4vw, 2.8rem);
  font-weight: 400;
  line-height: 1.15;
  color: #312E2D;
  margin: 0.2rem 0 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.intro-title em {
  font-style: italic;
  color: #7E1A2C;
  font-weight: inherit;
}

.intro-body {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.85;
  color: #555250;
  margin: 0.6rem 0 0;
  font-weight: 400;
  word-break: keep-all;
}

.intro-link {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 1.4rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: #312E2D;
  text-decoration: none;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #312E2D;
  transition: gap 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.intro-link:hover {
  gap: 1rem;
  color: #7E1A2C;
  border-bottom-color: #7E1A2C;
}

/* ── Editorial gallery — 3-up asymmetric ─────────────── */
.sec-gallery {
  background-color: #F5F0E8;
  padding: 2rem 4rem 7rem;
}

.gallery-grid {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.9fr);
  grid-template-rows: auto auto;
  gap: 1.2rem;
}

.gallery-item {
  position: relative;
  margin: 0;
  overflow: hidden;
  isolation: isolate;
  background-color: #EFE9DD;
}

.gallery-lead {
  grid-row: 1 / span 2;
  aspect-ratio: 4 / 5;
}

.gallery-top {
  aspect-ratio: 16 / 11;
}

.gallery-bottom {
  aspect-ratio: 16 / 11;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.gallery-item:hover img {
  transform: scale(1.03);
}

.gallery-item::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.48) 0%,
    rgba(0, 0, 0, 0.12) 38%,
    transparent 65%);
  pointer-events: none;
  z-index: 2;
}

.gallery-caption {
  position: absolute;
  bottom: 1.2rem;
  left: 1.2rem;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
  pointer-events: none;
}

.gallery-place {
  font-weight: 600;
  letter-spacing: 0.36em;
}

.gallery-sep {
  display: inline-block;
  width: 18px;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.55);
}

.gallery-text {
  font-family: 'Pretendard', sans-serif;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: none;
}

/* ── Curation process section ────────────────────────── */
.sec-curation {
  background-color: #F5F0E8;
  padding: 5rem 4rem 4rem;
  border-top: 1px solid rgba(49, 46, 45, 0.08);
}

.curation-inner {
  max-width: 760px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.4rem;
}

.curation-kicker {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: #7E1A2C;
  text-transform: uppercase;
}

.curation-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(1.8rem, 3.2vw, 2.6rem);
  font-weight: 400;
  line-height: 1.2;
  color: #312E2D;
  margin: 0.2rem 0 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.curation-title em {
  font-style: italic;
  color: #7E1A2C;
  font-weight: inherit;
}

.curation-body {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.85;
  color: #555250;
  margin: 0.6rem 0 0;
  font-weight: 400;
  word-break: keep-all;
}

.curation-closer {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: 16px;
  line-height: 1.6;
  color: #6D6059;
  margin: 0.4rem 0 0;
  letter-spacing: 0.005em;
  word-break: keep-all;
}

.curation-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 1.6rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: #F5F0E8;
  background-color: #312E2D;
  text-decoration: none;
  padding: 0.95rem 1.6rem;
  transition: background-color 0.4s ease, gap 0.3s ease;
}

.curation-cta:hover {
  background-color: #7E1A2C;
  gap: 1rem;
}

.sec-selection {
  padding: 1.5rem 8% 6rem; /* 상단 여백을 5rem -> 1.5rem으로 대폭 축소 */
  background-color: #F5F0E8;
}

.selection-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.4rem;
}

/* ── Editorial slide counter (Hermès-style) ── */
.selection-counter {
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  font-family: 'Inter', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 300;
  letter-spacing: 0.18em;
  color: #312E2D;
}

.counter-current {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: 18px;
  font-weight: 400;
  color: #312E2D;
  letter-spacing: 0.01em;
  line-height: 1;
}

.counter-divider {
  display: inline-block;
  width: 22px;
  height: 1px;
  background-color: rgba(49, 46, 45, 0.35);
}

.counter-total {
  font-family: 'Inter', 'Pretendard', sans-serif;
  font-style: normal;
  font-size: 13px;
  font-weight: 300;
  letter-spacing: 0.06em;
  color: rgba(49, 46, 45, 0.55);
}

.selection-counter-placeholder {
  font-family: 'Inter', 'Pretendard', sans-serif;
  font-size: 12px;
  letter-spacing: 0.18em;
  color: rgba(49, 46, 45, 0.4);
}

/* ── Refined arrow controls ── */
.selection-arrows {
  display: flex;
  gap: 8px;
}

.arrow-btn {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #312E2D;
  background: transparent;
  border: 1px solid rgba(49, 46, 45, 0.2);
  border-radius: 50%;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, opacity 0.3s ease;
}

.arrow-btn:hover:not(:disabled) {
  background-color: #312E2D;
  color: #F5F0E8;
  border-color: #312E2D;
}

.arrow-btn:disabled {
  opacity: 0.3;
  cursor: default;
}

.arrow-btn svg {
  display: block;
}

/* ── Hermès-style progress track below slider ── */
.prod-progress {
  margin-top: 2rem;
  padding: 0 2px;
}

.prod-progress-track {
  position: relative;
  height: 1px;
  width: 100%;
  background-color: rgba(49, 46, 45, 0.12);
  overflow: hidden;
}

.prod-progress-bar {
  position: absolute;
  top: 0;
  height: 1px;
  background-color: #312E2D;
  transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1),
              left 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  min-width: 24px;
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
  background: radial-gradient(
    ellipse at 50% 30%,
    #F5F0E8 0%,
    #EBE3D3 65%,
    #E2D7BF 100%
  );
  overflow: hidden;
  margin-bottom: 0.8rem;
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
  text-align: center;
}

.archive-name {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.04em;
  color: #312E2D;
  margin: 0;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.archive-item:hover .archive-name {
  color: #7E1A2C;
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
    height: auto;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  /* 모바일: 100vh 대신 이미지 본연의 비율(3:2)로 컨테이너 사이즈를 맞춰
     사진은 잘리지도, 위아래 빈 여백도 생기지 않도록 함 */
  .sec-hero {
    flex: none;
    height: auto;
    aspect-ratio: 3 / 2;
    position: relative;
  }

  .hero-overlay {
    left: 1.5rem;
    right: 1.5rem;
    bottom: 2rem;
    max-width: none;
  }

  .brand-title {
    font-size: clamp(0.95rem, 4.4vw, 1.25rem);
  }

  .brand-desc1 {
    font-size: 11px;
    margin-top: 0.5rem;
    line-height: 1.5;
  }

  /* 인디케이터 위치 조정 */
  .hero-indicators {
    bottom: 10px;
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

  /* Brand intro */
  .sec-intro {
    padding: 4rem 1.5rem 3rem;
  }

  .intro-inner {
    gap: 1rem;
  }

  .intro-kicker {
    font-size: 10px;
    letter-spacing: 0.3em;
  }

  .intro-title {
    font-size: clamp(1.4rem, 6vw, 2rem);
  }

  .intro-body {
    font-size: 13px;
    line-height: 1.75;
  }

  .intro-link {
    font-size: 10px;
    letter-spacing: 0.22em;
    margin-top: 0.8rem;
  }

  /* Curation section */
  .sec-curation {
    padding: 3.5rem 1.5rem 3rem;
  }

  .curation-inner {
    gap: 1rem;
  }

  .curation-kicker {
    font-size: 10px;
    letter-spacing: 0.3em;
  }

  .curation-title {
    font-size: clamp(1.4rem, 6vw, 2rem);
  }

  .curation-body {
    font-size: 13px;
    line-height: 1.75;
  }

  .curation-closer {
    font-size: 14px;
  }

  .curation-cta {
    font-size: 10px;
    letter-spacing: 0.22em;
    padding: 0.85rem 1.4rem;
    margin-top: 1.2rem;
  }

  /* Gallery: stack to single column */
  .sec-gallery {
    padding: 1rem 1.5rem 4rem;
  }

  .gallery-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }

  .gallery-lead {
    grid-row: auto;
    aspect-ratio: 4 / 5;
  }

  .gallery-top,
  .gallery-bottom {
    aspect-ratio: 4 / 3;
  }

  .gallery-caption {
    bottom: 0.9rem;
    left: 0.9rem;
    font-size: 9px;
    letter-spacing: 0.28em;
    gap: 0.5rem;
  }

  .gallery-sep {
    width: 14px;
  }

  .gallery-text {
    font-size: 10px;
  }
}

/* ── Chanel-style merchandise banner ─────────────────── */
.sel-banner {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  background-color: #1a1a1a;
}

.sel-banner-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.sel-banner-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right,
    rgba(0, 0, 0, 0.42) 0%,
    rgba(0, 0, 0, 0.22) 40%,
    rgba(0, 0, 0, 0.06) 75%,
    transparent 100%);
  z-index: 2;
  pointer-events: none;
}

.sel-banner-overlay {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: clamp(5rem, 12vw, 11rem);
  pointer-events: none;
  color: #FFFFFF;
}

.sel-banner-stack {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.sel-banner-kr {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.42em;
  color: rgba(255, 255, 255, 0.86);
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.sel-banner-en {
  font-family: 'Inter', 'Pretendard', sans-serif;
  font-size: clamp(1.7rem, 3.2vw, 2.6rem);
  font-weight: 300;
  line-height: 1;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #FFFFFF;
  margin: 0;
  text-shadow: 0 2px 22px rgba(0, 0, 0, 0.35);
}

@media (max-width: 768px) {
  .sel-banner {
    height: 200px;
  }

  .sel-banner-overlay {
    padding-left: clamp(2rem, 8vw, 4rem);
  }

  .sel-banner-stack {
    gap: 0.4rem;
  }

  .sel-banner-kr {
    font-size: 10px;
    letter-spacing: 0.36em;
  }

  .sel-banner-en {
    font-size: clamp(1.2rem, 5.5vw, 1.7rem);
  }
}

/* GNB 그리드 뷰 */
.sel-grid-view {
  /* 글로벌 컨테이너가 기본 padding 제공 */
}

.grid-header {
  text-align: center;
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

/* ── Filter / sort toolbar ───────────────────────────── */
.grid-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid rgba(49, 46, 45, 0.12);
  border-bottom: 1px solid rgba(49, 46, 45, 0.12);
  margin: 3rem 0 4rem;
  flex-wrap: wrap;
}

.filter-list {
  list-style: none;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.6rem;
  padding: 0;
  margin: 0;
}

.filter-item {
  display: inline-flex;
  align-items: baseline;
  gap: 0.4rem;
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.04em;
  color: rgba(49, 46, 45, 0.55);
  cursor: pointer;
  transition: color 0.3s ease;
  padding: 0.2rem 0;
  border-bottom: 1px solid transparent;
}

.filter-item:hover {
  color: #312E2D;
}

.filter-item.is-active {
  color: #7E1A2C;
  border-bottom-color: #7E1A2C;
}

.filter-count {
  font-family: 'Inter', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 300;
  letter-spacing: 0.02em;
  color: rgba(49, 46, 45, 0.4);
}

.filter-item.is-active .filter-count {
  color: rgba(126, 26, 44, 0.6);
}

.sort-control {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
}

.sort-label {
  font-family: 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(49, 46, 45, 0.55);
}

.sort-select {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.04em;
  color: #312E2D;
  background-color: transparent;
  border: none;
  border-bottom: 1px solid rgba(49, 46, 45, 0.2);
  padding: 0.25rem 1.4rem 0.25rem 0;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23312E2D' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
  background-repeat: no-repeat;
  background-position: right 0.2rem center;
  background-size: 10px;
  transition: border-color 0.3s ease;
}

.sort-select:focus {
  outline: none;
  border-bottom-color: #7E1A2C;
}

@media (max-width: 768px) {
  .grid-toolbar {
    margin: 2rem 0 2.5rem;
    padding: 0.8rem 0;
    gap: 0.8rem;
  }

  .filter-list {
    gap: 1rem;
  }

  .filter-item {
    font-size: 11px;
  }

  .filter-count {
    font-size: 9px;
  }

  .sort-label {
    font-size: 10px;
    letter-spacing: 0.16em;
  }

  .sort-select {
    font-size: 11px;
  }
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4rem 1.4rem;
}

@media (min-width: 1400px) {
  .grid-container {
    grid-template-columns: repeat(4, 1fr);
    gap: 4.5rem 1.2rem;
  }
}

@media (max-width: 1024px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem 1rem;
  }
}

@media (max-width: 640px) {
  .grid-header {
    margin-bottom: 2.5rem;
  }
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 2.4rem 0.7rem;
  }

  .archive-name {
    font-size: 11px;
  }
}

/* 스켈레톤 & 애니메이션 제거됨 */
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
