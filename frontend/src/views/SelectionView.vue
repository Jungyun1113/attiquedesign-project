<template>
  <div class="selection-page" :class="[`view-${viewMode}`]">

    <!-- ═══════════════════════════════════════════ -->
    <!-- Hero View (Landing / Home)                  -->
    <!-- ═══════════════════════════════════════════ -->
    <template v-if="viewMode === 'hero'">

      <!-- ── 섹션 1: 히어로 슬라이더 ── -->
      <section class="sec-hero" @mouseenter="stopAutoplay" @mouseleave="startAutoplay">
        <!-- PC: 4슬라이드 (마지막은 2분할) -->
        <template v-if="!isMobile">
          <div
            v-for="(slide, idx) in pcSlides"
            :key="'pc-' + idx"
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
        </template>
        <!-- 모바일: 4슬라이드 (마지막은 2분할, PC와 동일) -->
        <template v-else>
          <div
            v-for="(slide, idx) in pcSlides"
            :key="'mo-' + idx"
            class="hero-slide"
            :class="{ 'is-active': activeSlide === idx }"
          >
            <template v-if="slide.type === 'single'">
              <img :src="slide.src" alt="ATTIQUE interior" class="hero-img-full" :loading="idx === 0 ? 'eager' : 'lazy'" />
            </template>
            <template v-else>
              <div class="hero-dual hero-dual--mobile">
                <img :src="slide.src1" alt="ATTIQUE interior" class="hero-img-half" loading="lazy" />
                <img :src="slide.src2" alt="ATTIQUE interior" class="hero-img-half" loading="lazy" />
              </div>
            </template>
          </div>
        </template>
      </section>

      <!-- ── 섹션 2: 브랜드 텍스트 ── -->
      <section class="sec-brand">
        <div class="sec-brand-left">
          <p class="brand-title">Living Edit · Space Creation</p>
        </div>
        <div class="sec-brand-right">
          <p class="brand-desc1">인테리어 시공부터 가구, 조명, 러그, 오브제까지.</p>
          <p class="brand-desc2">한남동 쇼룸에서 만나보실 수 있습니다.</p>
        </div>
      </section>

      <!-- ── 섹션 3: 제품 슬라이더 ── -->
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
              v-for="item in allObjects"
              :key="item.id"
              class="archive-item"
              :style="itemStyle"
            >
              <div class="archive-img-wrap">
                <img :src="item.img" :alt="item.name" loading="lazy" />
              </div>
              <div class="archive-info">
                <h3 class="archive-name">{{ item.name }}</h3>
                <button class="archive-btn" @click="enquireObject(item.id)">VIEW DETAILS</button>
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
          v-for="item in allObjects"
          :key="item.id"
          class="archive-item"
        >
          <div class="archive-img-wrap">
            <img :src="item.img" :alt="item.name" loading="lazy" />
          </div>
          <div class="archive-info">
            <h3 class="archive-name">{{ item.name }}</h3>
            <button class="archive-btn" @click="enquireObject(item.id)">VIEW DETAILS</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const viewMode = computed(() => (route.query.view === 'grid' ? 'grid' : 'hero'))

// ── 히어로 슬라이더 ──────────────────────────
type SingleSlide = { type: 'single'; src: string }
type DualSlide   = { type: 'dual';   src1: string; src2: string }
type HeroSlide   = SingleSlide | DualSlide

const pcSlides: HeroSlide[] = [
  { type: 'single', src: '/images/hero/hero-01.png' },
  { type: 'single', src: '/images/hero/hero-02.png' },
  { type: 'single', src: '/images/hero/hero-03.png' },
  { type: 'dual',   src1: '/images/hero/hero-05.png', src2: '/images/hero/hero-04.png' },
]

const isMobile = ref(window.innerWidth <= 768)
const activeSlide = ref(0)
let autoplayTimer: ReturnType<typeof setInterval> | null = null

const currentLength = computed(() => pcSlides.length)

function startAutoplay() {
  stopAutoplay()
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
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  stopAutoplay()
})

// --- Space Data ---
interface SpaceObject { id: string; name: string; img: string }
interface SelectionSpace { id: string; title: string; subtitle: string; objects: SpaceObject[] }

const selectionSpaces: SelectionSpace[] = [
  {
    id: 'warm-sanctuary',
    title: 'Warm Sanctuary',
    subtitle: 'A curated space where dark walnut meets burgundy textiles',
    objects: [
      { id: 'obj-1', name: 'Walnut Console', img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=85' },
      { id: 'obj-2', name: 'Linen Armchair', img: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=600&q=85' },
      { id: 'obj-3', name: 'Ceramic Vase', img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=600&q=85' },
      { id: 'obj-4', name: 'Wool Rug', img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=600&q=85' },
      { id: 'obj-5', name: 'Brass Lamp', img: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=85' },
    ]
  },
  {
    id: 'nordic-calm',
    title: 'Nordic Calm',
    subtitle: 'Scandinavian minimalism with warm undertones',
    objects: [
      { id: 'obj-6', name: 'Oak Dining Table', img: 'https://images.unsplash.com/photo-1549497538-303791108f95?w=600&q=85' },
      { id: 'obj-7', name: 'Pendant Light', img: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=600&q=85' },
      { id: 'obj-8', name: 'Wool Throw', img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=600&q=85' },
      { id: 'obj-9', name: 'Minimal Vase', img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=600&q=85' },
    ]
  },
  {
    id: 'modern-noir',
    title: 'Maison Noir',
    subtitle: 'Bespoke luxury living with curated dark accents',
    objects: [
      { id: 'obj-10', name: 'Black Marble Table', img: 'https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=600&q=85' },
      { id: 'obj-11', name: 'Silver Sculpture', img: 'https://images.unsplash.com/photo-1554188248-986adbb73be4?w=600&q=85' },
      { id: 'obj-12', name: 'Leather Sofa', img: 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600&q=85' },
    ]
  },
]

const allObjects = computed(() => selectionSpaces.flatMap(s => s.objects))

function enquireObject(id: string) {
  router.push(`/selection/${id}`)
}

// ── 제품 슬라이더 ──────────────────────────
const sliderWrapRef = ref<HTMLElement | null>(null)
const wrapWidth = ref(0)
const prodOffset = ref(0)

const itemsPerView = computed(() => isMobile.value ? 2 : 3)
const maxOffset = computed(() => Math.max(0, allObjects.value.length - itemsPerView.value))

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
/* ─── 전체 페이지 ─────────────────────────────── */
.selection-page {
  background-color: #F5F0E8;
}

/* ─── 섹션 1: 히어로 슬라이더 ────────────────── */
.sec-hero {
  position: relative;
  width: 100%;
  height: 60vh;
  overflow: hidden;
  margin: 0;
  padding: 0;
  background-color: #e8e6e2;
}

.hero-slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.9s ease-in-out;
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
  gap: 4px;
}

.hero-dual--mobile {
  gap: 2px;
}

.hero-img-half {
  flex: 1;
  min-width: 0;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

/* ─── 섹션 2: 브랜드 텍스트 ──────────────────── */
.sec-brand {
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 120px;
  padding: 2rem 4rem;
  background-color: #F5F0E8;
  gap: 2rem;
  overflow: visible;
}

.sec-brand-left {
  flex: 0 0 40%;
}

.brand-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  font-weight: 400;
  font-style: italic;
  line-height: 1.4;
  color: #2C2C2A;
  margin: 0;
}

.sec-brand-right {
  flex: 0 0 60%;
}

.brand-desc1 {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: #5F5E5A;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
}

.brand-desc2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #888780;
  line-height: 1.6;
  margin-top: 0.3rem;
  word-break: keep-all;
}

/* ─── 섹션 3: 제품 슬라이더 ─────────────────── */
.sec-selection {
  padding: 3rem 4rem 4rem;
  background-color: #F5F0E8;
}

.selection-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.2rem;
}

.selection-spacer {
  flex: 1;
}

.selection-label {
  flex: 1;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.15em;
  color: #888780;
  text-align: center;
  text-transform: uppercase;
  margin: 0;
}

.selection-arrows {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  gap: 6px;
}

.arrow-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  line-height: 1;
  color: #2C2C2A;
  background: transparent;
  border: 1px solid rgba(44, 44, 42, 0.25);
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  padding: 0;
}

.arrow-btn:hover:not(:disabled) {
  background: #2C2C2A;
  color: #F5F0E8;
  border-color: #2C2C2A;
}

.arrow-btn:disabled {
  opacity: 0.25;
  cursor: default;
}

/* 슬라이더 트랙 */
.prod-slider-wrap {
  overflow: hidden;
  width: 100%;
}

.prod-track {
  display: flex;
  gap: 16px;
  transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* ─── Archive Item ───────────────────────────── */
.archive-item {
  flex: 0 0 auto;
  cursor: pointer;
}

.archive-img-wrap {
  width: 100%;
  height: 180px;
  background-color: #fff;
  overflow: hidden;
  margin-bottom: 0.6rem;
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.archive-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.archive-item:hover .archive-img-wrap img {
  transform: scale(1.05);
}

.archive-info {
  text-align: center;
}

.archive-name {
  font-family: 'Raleway', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #2C2C2A;
  margin: 0.6rem 0 0.5rem;
}

.archive-btn {
  display: inline-block;
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.15em;
  color: #312E2D;
  background: transparent;
  border: 1px solid rgba(49, 46, 45, 0.35);
  padding: 0.35rem 0.9rem;
  cursor: pointer;
  text-transform: uppercase;
  transition: background 0.2s ease, color 0.2s ease;
}

.archive-btn:hover {
  background: #312E2D;
  color: #F5F0E8;
}

/* ─── Grid Exhibition View ───────────────────── */
.sel-grid-view {
  padding-top: 1.5rem;
  padding-bottom: 8rem;
}

.grid-header {
  margin-bottom: 4rem;
  text-align: center;
}

.grid-title {
  font-family: 'Playfair Display', serif;
  font-size: 42px;
  color: #312E2D;
  margin-bottom: 1rem;
}

.grid-subtitle {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  color: #6D6059;
  letter-spacing: 0.02em;
}

.grid-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  color: rgba(109, 96, 89, 0.65);
  letter-spacing: 0.02em;
  margin-top: 0.4rem;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem 1.5rem;
}

/* ─── 모바일 (max-width: 768px) ──────────────── */
@media (max-width: 768px) {
  /* 섹션 1: 슬라이더 */
  .sec-hero {
    height: auto;
    aspect-ratio: 3 / 2;
  }

  .hero-slide {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  /* 섹션 2: 브랜드 텍스트 */
  .sec-brand {
    flex-direction: column;
    height: auto;
    min-height: unset;
    padding: 1.5rem;
    gap: 0.4rem;
    align-items: flex-start;
  }

  .sec-brand-left,
  .sec-brand-right {
    flex: none;
    width: 100%;
  }

  .brand-title {
    font-size: 1.2rem;
  }

  .brand-desc1 {
    font-size: 13px;
  }

  /* 섹션 3: 제품 슬라이더 */
  .sec-selection {
    padding: 2rem 1rem 2.5rem;
  }

  .archive-img-wrap {
    height: 140px;
  }

  .archive-name {
    font-size: 11px;
    margin: 0.4rem 0 0.35rem;
  }

  .archive-btn {
    font-size: 8px;
    padding: 0.3rem 0.6rem;
  }

  .arrow-btn {
    width: 28px;
    height: 28px;
    font-size: 18px;
  }

  /* Grid View */
  .grid-title {
    font-size: 28px;
  }

  .grid-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem 1rem;
  }

  .grid-container .archive-img-wrap {
    height: 120px;
  }
}
</style>
