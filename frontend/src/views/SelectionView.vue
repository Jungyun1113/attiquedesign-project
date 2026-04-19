<template>
  <div class="selection-page" :class="[`view-${viewMode}`]">

    <!-- ═══════════════════════════════════════════ -->
    <!-- Hero View (Landing / Home)                  -->
    <!-- ═══════════════════════════════════════════ -->
    <template v-if="viewMode === 'hero'">

      <!-- ── 섹션 1: 히어로 슬라이더 (Full-Width Overlay) ── -->
      <section class="sec-hero" @mouseenter="stopAutoplay" @mouseleave="startAutoplay">
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
            <!-- 이미지 위 은은한 그라데이션 오버레이 -->
            <div class="hero-overlay-mask"></div>
          </div>
        </template>
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

        <!-- ── 히어로 텍스트 컨텐츠 (중앙 정렬) ── -->
        <div class="hero-content">
          <p class="brand-title">Living Edit · Space Creation</p>
          <div class="brand-desc-wrap">
            <p class="brand-desc1">하이엔드 수입 가구 큐레이션부터 맞춤형 공간 스타일링과 인테리어 시공까지.</p>
            <p class="brand-desc2">아띠끄 디자인 한남동 쇼룸에서 품격 있는 토탈 리빙을 경험해 보십시오.</p>
          </div>
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
  { type: 'dual',   src1: '/images/hero/hero-05.png', src2: '/images/hero/hero-04.png' },
]

const heroSlides = ref<HeroSlide[]>(fallbackSlides)

const pcSlides = computed(() => heroSlides.value)

const isMobile = ref(window.innerWidth <= 768)
const activeSlide = ref(0)
let autoplayTimer: ReturnType<typeof setInterval> | null = null

const currentLength = computed(() => pcSlides.value.length)

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
  loadSelections()
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  stopAutoplay()
})

// ── Selection 데이터 ──────────────────────────
const selections = ref<Selection[]>([])

async function loadSelections() {
  try {
    selections.value = await selectionService.getSelections()
    const apiImages = selections.value.flatMap(s => s.images ?? [])
    if (apiImages.length > 0) {
      heroSlides.value = apiImages.map(img => ({ type: 'single' as const, src: img.image_url }))
    }
  } catch {
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
}

.sec-hero {
  position: relative;
  width: 100%;
  height: 80vh;
  overflow: hidden;
  margin: 0;
  padding: 0;
  background-color: #F5F0E8;
}

.hero-overlay-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(245, 240, 232, 0.4) 0%, transparent 40%, transparent 60%, rgba(245, 240, 232, 0.4) 100%);
  pointer-events: none;
}

.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  max-width: 1200px;
  padding: 0 2rem;
  pointer-events: none;
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

.brand-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  font-weight: 400;
  font-style: italic;
  line-height: 1.4;
  color: #111111;
  margin: 0;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 40px rgba(255, 255, 255, 0.4);
}

.brand-desc-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 1.8rem;
}

.brand-desc1 {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #111111;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.9);
}

.brand-desc2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 300;
  color: #111111;
  line-height: 1.6;
  margin: 0;
  word-break: keep-all;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.9);
}

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

.prod-slider-wrap {
  overflow: hidden;
  width: 100%;
}

.prod-track {
  display: flex;
  gap: 16px;
  transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

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

@media (max-width: 768px) {
  .sec-hero {
    height: auto;
    aspect-ratio: 4 / 5; /* 모바일은 세로로 좀 더 길게 */
  }

  .hero-content {
    position: relative;
    top: 0;
    left: 0;
    transform: none;
    padding: 2.5rem 1.5rem;
    background-color: #F5F0E8; /* 모바일은 텍스트 가독성을 위해 배경 분리 */
  }

  .brand-title {
    font-size: 1.5rem;
    text-shadow: none;
  }

  .brand-desc1 {
    font-size: 14px;
    text-shadow: none;
  }

  .brand-desc-wrap {
    margin-top: 1rem;
    gap: 0.4rem;
  }

  .brand-title {
    font-size: 1.2rem;
  }

  .brand-desc1 {
    font-size: 13px;
  }

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
