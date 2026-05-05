<template>
  <div class="portfolio-page">

    <!-- ═════ Magazine masthead ═════ -->
    <header class="mag-masthead" v-reveal>
      <div class="mag-masthead-inner">
        <span class="mag-issue">ATTIQUE · ARCHIVE</span>
        <h1 class="mag-title">
          Curated <em>Spaces</em>.
        </h1>
        <p class="mag-lead">아띠끄가 짓고 채워온 공간의 아카이브.</p>
      </div>
    </header>

    <!-- ═════ Long editorial intro ═════ -->
    <section class="mag-intro" v-reveal>
      <p class="mag-intro-body">
        주거부터 상업, 드라마와 매거진 스타일링까지,<br />
        아띠끄가 십여 년간 마주해온 다양한 챕터를 한자리에 모았습니다.<br /><br />
        획일된 양식이 아닌, 머무는 이의 결을 따라<br />
        다르게 완성된 공간의 흔적들.
      </p>
      <p class="mag-intro-closer">
        한 권의 매거진처럼, 페이지를 넘기며 펼쳐 보세요.
      </p>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <span class="loading-text">Loading.</span>
    </div>

    <template v-else-if="categories.length">

      <!-- ═════ Chapter sub-nav (Chanel-style minimal) ═════ -->
      <nav class="chapter-nav" v-reveal>
        <ul class="chapter-list">
          <li
            v-for="cat in categories"
            :key="cat.id"
            class="chapter-item"
            :class="{ 'is-active': activeCategoryId === cat.id }"
            @click="activeCategoryId = cat.id"
          >
            <span class="chapter-kr">{{ cat.name }}</span>
            <span class="chapter-en">{{ catLabel(cat.id) }}</span>
          </li>
        </ul>
      </nav>

      <!-- ═════ Rich per-category description ═════ -->
      <div class="chapter-desc-wrap" v-reveal :key="activeCategoryId">
        <p class="chapter-desc">{{ richDesc }}</p>
      </div>

      <!-- ═════ Magazine spreads ═════ -->
      <div class="spread-list">
        <section
          v-for="(p, i) in (activeCategory?.portfolios ?? [])"
          :key="p.id"
          class="spread"
          :class="`spread-${variantOf(i)}`"
          v-reveal
        >
          <!-- ── Variant A · Cover (full-bleed) ── -->
          <template v-if="variantOf(i) === 'cover'">
            <router-link :to="`/portfolio/${p.id}`" class="cover-link">
              <figure class="cover-figure">
                <img class="cover-img" :src="firstImg(p)" :alt="p.title" loading="lazy" />
                <div class="cover-vignette"></div>

                <span class="cover-cat">{{ catLabel(p.category) }} · {{ catKr(p.category) }}</span>

                <figcaption class="cover-overlay">
                  <span class="cover-num">PROJECT {{ formattedNum(i) }}</span>
                  <h2 class="cover-title">{{ p.title }}</h2>
                  <span class="cover-cta">
                    <span>Into the Space</span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <line x1="7" y1="17" x2="17" y2="7"></line>
                      <polyline points="7 7 17 7 17 17"></polyline>
                    </svg>
                  </span>
                </figcaption>
              </figure>
            </router-link>
          </template>

          <!-- ── Variant B · Asymmetric 2-up ── -->
          <template v-else-if="variantOf(i) === 'asym'">
            <div class="asym-grid">
              <router-link :to="`/portfolio/${p.id}`" class="asym-main">
                <figure class="asym-figure">
                  <img :src="firstImg(p)" :alt="p.title" loading="lazy" />
                </figure>
              </router-link>

              <aside class="asym-side">
                <span class="spread-num">PROJECT {{ formattedNum(i) }}</span>
                <span class="spread-cat">{{ catLabel(p.category) }}</span>
                <h2 class="spread-title">{{ p.title }}</h2>

                <router-link
                  v-if="secondImg(p)"
                  :to="`/portfolio/${p.id}`"
                  class="asym-thumb"
                >
                  <img :src="secondImg(p)" :alt="p.title + ' detail'" loading="lazy" />
                </router-link>

                <router-link :to="`/portfolio/${p.id}`" class="spread-cta">
                  <span>View Project</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </router-link>
              </aside>
            </div>
          </template>

          <!-- ── Variant C · Centered single ── -->
          <template v-else-if="variantOf(i) === 'centered'">
            <div class="centered-spread">
              <header class="centered-head">
                <span class="spread-num">PROJECT {{ formattedNum(i) }}</span>
                <span class="centered-rule"></span>
                <span class="spread-cat">{{ catLabel(p.category) }}</span>
              </header>

              <h2 class="centered-title">
                <em>{{ p.title }}</em>
              </h2>

              <router-link :to="`/portfolio/${p.id}`" class="centered-figure-link">
                <figure class="centered-figure">
                  <img :src="firstImg(p)" :alt="p.title" loading="lazy" />
                </figure>
              </router-link>

              <footer class="centered-foot">
                <span class="centered-caption"><em>An ATTIQUE study.</em></span>
                <router-link :to="`/portfolio/${p.id}`" class="spread-cta">
                  <span>View Project</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </router-link>
              </footer>
            </div>
          </template>

          <!-- ── Variant D · Split (text · image) ── -->
          <template v-else>
            <div class="split-grid">
              <div class="split-text">
                <span class="split-big-num">{{ formattedNum(i) }}</span>
                <span class="spread-cat">{{ catLabel(p.category) }} · {{ catKr(p.category) }}</span>
                <h2 class="split-title">{{ p.title }}</h2>
                <router-link :to="`/portfolio/${p.id}`" class="spread-cta">
                  <span>View Project</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </router-link>
              </div>

              <router-link :to="`/portfolio/${p.id}`" class="split-figure-link">
                <figure class="split-figure">
                  <img :src="firstImg(p)" :alt="p.title" loading="lazy" />
                </figure>
              </router-link>
            </div>
          </template>
        </section>
      </div>
    </template>

    <div v-else class="empty-state">
      <p class="global-kor-desc">등록된 포트폴리오가 없습니다.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { portfolioService, type Portfolio, type PortfolioCategory } from '@/services/portfolio.service'

const categories = ref<PortfolioCategory[]>([])
const loading = ref(true)
const activeCategoryId = ref('')

onMounted(async () => {
  try {
    categories.value = await portfolioService.getGroupedByCategory()
    if (categories.value.length) activeCategoryId.value = categories.value[0].id
  } catch {
    categories.value = []
  } finally {
    loading.value = false
  }
})

const activeCategory = computed(() =>
  categories.value.find(c => c.id === activeCategoryId.value) ?? categories.value[0]
)

// Rich per-category descriptions (Chanel-style luxury copy)
const CATEGORY_RICH: Record<string, string> = {
  residential:
    '한 사람의 일상이 머무는 가장 사적인 공간.\n클래식과 모던, 색과 소재의 균형 안에서 머무는 이의 결을 따라 다르게 완성합니다.\n공간의 처음부터 마지막 한 올까지, 한남 쇼룸의 1:1 큐레이션으로.',
  commercial:
    '브랜드의 정체성이 공간의 언어가 되는 자리.\nF&B, 리테일, 오피스 — 그 브랜드만의 결을 따라 풀어낸 아띠끄의 상업 프로젝트.\n방문하는 이의 시선과 동선을 함께 설계합니다.',
  drama:
    '도깨비, 상속자들, 괜찮아 사랑이야.\n극 중 인물의 일상이 그 자리에서 진짜처럼 머물도록,\n스토리와 인물의 결을 공간으로 옮겨낸 아띠끄의 스타일링.',
  magazine:
    '행복이 가득한 집, 메종, 까사리빙, 노블레스.\n한 컷의 페이지가 곧 한 사람의 일상이 되도록,\n국내 대표 리빙 매거진과 함께 만들어온 아띠끄의 스타일링 아카이브.',
}

const richDesc = computed(
  () =>
    CATEGORY_RICH[activeCategoryId.value] ??
    activeCategory.value?.description ??
    ''
)

const VARIANTS = ['cover', 'asym', 'centered', 'split'] as const
type Variant = typeof VARIANTS[number]

const variantOf = (i: number): Variant => VARIANTS[i % VARIANTS.length]
const formattedNum = (i: number) => String(i + 1).padStart(2, '0')
const catLabel = (catId: string) => (catId ?? '').toUpperCase()
const catKr = (catId: string) =>
  categories.value.find(c => c.id === catId)?.name ?? ''
const firstImg = (p: Portfolio) =>
  p.images[0]?.image_url ?? p.cover_image_url ?? ''
const secondImg = (p: Portfolio) =>
  p.images[1]?.image_url ?? ''
</script>

<style scoped>
.portfolio-page {
  background-color: #F5F0E8;
  color: #312E2D;
  min-height: calc(100vh - 160px);
}

/* ── Masthead ───────────────────────────────────────── */
.mag-masthead {
  padding: 5rem 4rem 3rem;
  max-width: 1320px;
  margin: 0 auto;
}

.mag-masthead-inner {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mag-issue {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: #953735;
  text-transform: uppercase;
}

.mag-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2.2rem, 5vw, 4.2rem);
  font-weight: 400;
  line-height: 1.05;
  margin: 0;
  letter-spacing: -0.01em;
  color: #312E2D;
}

.mag-title em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.mag-lead {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
  word-break: keep-all;
}

/* ── Long editorial intro ───────────────────────────── */
.mag-intro {
  max-width: 720px;
  margin: 0 auto;
  padding: 1rem 4rem 4rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}

.mag-intro-body {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.85;
  color: #555250;
  margin: 0;
  font-weight: 400;
  word-break: keep-all;
}

.mag-intro-closer {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: 16px;
  line-height: 1.6;
  color: #6D6059;
  margin: 0;
  letter-spacing: 0.01em;
  word-break: keep-all;
}

/* ── Chanel-style chapter nav (middle-dot separators) ── */
.chapter-nav {
  max-width: 1320px;
  margin: 0 auto;
  padding: 1.4rem 4rem;
  border-top: 1px solid rgba(49, 46, 45, 0.1);
  border-bottom: 1px solid rgba(49, 46, 45, 0.1);
}

.chapter-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: center;
  gap: 0;
  row-gap: 0.6rem;
}

.chapter-item {
  display: inline-flex;
  align-items: baseline;
  gap: 0.6rem;
  padding: 0.4rem 0;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;
}

.chapter-item + .chapter-item::before {
  content: '·';
  margin: 0 1.6rem;
  color: rgba(49, 46, 45, 0.25);
  font-size: 14px;
  align-self: center;
  pointer-events: none;
}

.chapter-kr {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.02em;
  color: rgba(49, 46, 45, 0.55);
  transition: color 0.3s ease;
}

.chapter-en {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 9px;
  font-weight: 400;
  letter-spacing: 0.3em;
  color: rgba(49, 46, 45, 0.4);
  text-transform: uppercase;
  transition: color 0.3s ease;
}

.chapter-item:hover .chapter-kr,
.chapter-item:hover .chapter-en {
  color: #312E2D;
}

.chapter-item.is-active .chapter-kr {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-weight: 400;
  font-size: 17px;
  color: #953735;
}

.chapter-item.is-active .chapter-en {
  color: #953735;
  opacity: 0.9;
}

/* ── Rich per-category description ──────────────────── */
.chapter-desc-wrap {
  max-width: 760px;
  margin: 0 auto;
  padding: 3rem 4rem 0;
  text-align: center;
  animation: chapter-fade 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes chapter-fade {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.chapter-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.85;
  color: #6D6059;
  white-space: pre-line;
  margin: 0;
  font-weight: 400;
  word-break: keep-all;
}

/* ── Spread list ────────────────────────────────────── */
.spread-list {
  display: flex;
  flex-direction: column;
  padding: 5rem 0 8rem;
}

.spread {
  margin-bottom: 8rem;
}

.spread:last-child {
  margin-bottom: 0;
}

/* Shared spread typography */
.spread-num {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.34em;
  color: #953735;
  text-transform: uppercase;
}

.spread-cat {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 400;
  letter-spacing: 0.3em;
  color: rgba(49, 46, 45, 0.55);
  text-transform: uppercase;
}

.spread-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(1.8rem, 3vw, 2.6rem);
  font-weight: 400;
  line-height: 1.15;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.spread-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: #312E2D;
  text-decoration: none;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #312E2D;
  align-self: flex-start;
  transition: gap 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.spread-cta:hover {
  gap: 1rem;
  color: #953735;
  border-bottom-color: #953735;
}

/* ───────────────────────────────────────────────────────
   A · Cover (full-bleed)
   ─────────────────────────────────────────────────── */
.cover-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.cover-figure {
  position: relative;
  width: 100%;
  height: 85vh;
  min-height: 560px;
  margin: 0;
  overflow: hidden;
  isolation: isolate;
  background-color: #1a1a1a;
}

.cover-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.cover-link:hover .cover-img {
  transform: scale(1.03);
}

.cover-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.18) 40%,
    rgba(0, 0, 0, 0.15) 80%,
    rgba(0, 0, 0, 0.35) 100%);
  z-index: 2;
  pointer-events: none;
}

.cover-cat {
  position: absolute;
  top: 1.8rem;
  right: 2rem;
  z-index: 3;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.32em;
  color: rgba(255, 255, 255, 0.86);
  text-transform: uppercase;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.cover-overlay {
  position: absolute;
  left: 4rem;
  bottom: 3.5rem;
  z-index: 5;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  max-width: 640px;
  color: #FFFFFF;
}

.cover-num {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.36em;
  color: rgba(255, 255, 255, 0.86);
  text-transform: uppercase;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.cover-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 4.4vw, 3.6rem);
  font-weight: 400;
  line-height: 1.08;
  margin: 0;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 22px rgba(0, 0, 0, 0.35);
  color: #F5F0E8;
}

.cover-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.3);
  margin-top: 0.4rem;
  align-self: flex-start;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
  transition: gap 0.3s ease, border-color 0.3s ease;
}

.cover-link:hover .cover-cta {
  gap: 1rem;
  border-bottom-color: rgba(255, 255, 255, 1);
}

/* ───────────────────────────────────────────────────────
   B · Asymmetric 2-up
   ─────────────────────────────────────────────────── */
.asym-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 0.7fr);
  gap: 2.5rem;
  align-items: start;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 4rem;
}

.asym-main {
  display: block;
  text-decoration: none;
  align-self: stretch;
}

.asym-figure {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  margin: 0;
  overflow: hidden;
  background-color: #EFE9DD;
}

.asym-figure img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.asym-main:hover .asym-figure img {
  transform: scale(1.03);
}

.asym-side {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 1rem;
}

.asym-side .spread-cat {
  margin-top: -0.4rem;
}

.asym-side .spread-title {
  margin-top: 0.4rem;
  margin-bottom: 0.6rem;
}

.asym-thumb {
  display: block;
  width: 100%;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  background-color: #EFE9DD;
  margin: 1rem 0 0.6rem;
}

.asym-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.asym-thumb:hover img {
  transform: scale(1.03);
}

/* ───────────────────────────────────────────────────────
   C · Centered single
   ─────────────────────────────────────────────────── */
.centered-spread {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 2rem;
}

.centered-head {
  display: inline-flex;
  align-items: center;
  gap: 1rem;
}

.centered-rule {
  display: block;
  width: 28px;
  height: 1px;
  background-color: rgba(149, 55, 53, 0.5);
}

.centered-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 3.6vw, 3.2rem);
  font-weight: 400;
  line-height: 1.1;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.01em;
}

.centered-title em {
  font-style: italic;
}

.centered-figure-link {
  display: block;
  width: 100%;
  text-decoration: none;
}

.centered-figure {
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background-color: #EFE9DD;
  margin: 0;
}

.centered-figure img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.centered-figure-link:hover .centered-figure img {
  transform: scale(1.03);
}

.centered-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-top: 0.6rem;
}

.centered-caption {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: 14px;
  color: #6D6059;
  letter-spacing: 0.005em;
}

.centered-caption em {
  font-style: italic;
}

/* ───────────────────────────────────────────────────────
   D · Split (text · image)
   ─────────────────────────────────────────────────── */
.split-grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 3rem;
  align-items: stretch;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 4rem;
}

.split-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  padding-right: 1rem;
}

.split-big-num {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: clamp(3rem, 6vw, 5.4rem);
  font-weight: 400;
  line-height: 1;
  color: #953735;
  letter-spacing: -0.02em;
  margin-bottom: 0.4rem;
}

.split-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 3.4vw, 2.8rem);
  font-weight: 400;
  line-height: 1.15;
  color: #312E2D;
  margin: 0.4rem 0 0.6rem 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.split-figure-link {
  display: block;
  text-decoration: none;
  align-self: stretch;
}

.split-figure {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 480px;
  aspect-ratio: 4 / 5;
  margin: 0;
  overflow: hidden;
  background-color: #EFE9DD;
}

.split-figure img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.split-figure-link:hover .split-figure img {
  transform: scale(1.03);
}

/* ── Loading / empty ────────────────────────────────── */
@keyframes quiet-pulse {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.7; }
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
}

.loading-text {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 300;
  letter-spacing: 0.18em;
  color: #312E2D;
  text-transform: uppercase;
  animation: quiet-pulse 3s ease-in-out infinite;
}

.empty-state {
  padding: 4rem 4rem 8rem;
  max-width: 1320px;
  margin: 0 auto;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 1100px) {
  .mag-masthead,
  .mag-intro,
  .chapter-nav,
  .chapter-desc-wrap,
  .asym-grid,
  .centered-spread,
  .split-grid,
  .empty-state {
    padding-left: 2.5rem;
    padding-right: 2.5rem;
  }

  .cover-overlay {
    left: 2.5rem;
    bottom: 2.5rem;
  }

  .cover-cat {
    right: 2.5rem;
    top: 1.5rem;
  }
}

@media (max-width: 768px) {
  .mag-masthead {
    padding: 3rem 1.5rem 2rem;
  }

  .mag-intro {
    padding: 0.5rem 1.5rem 2.5rem;
    gap: 1.2rem;
  }

  .mag-intro-body {
    font-size: 13px;
    line-height: 1.75;
  }

  .mag-intro-closer {
    font-size: 14px;
  }

  .chapter-nav {
    padding: 1rem 1.5rem;
  }

  .chapter-item + .chapter-item::before {
    margin: 0 0.7rem;
  }

  .chapter-kr {
    font-size: 13px;
  }

  .chapter-en {
    font-size: 8px;
    letter-spacing: 0.26em;
  }

  .chapter-item.is-active .chapter-kr {
    font-size: 15px;
  }

  .chapter-desc-wrap {
    padding: 1.8rem 1.5rem 0;
  }

  .chapter-desc {
    font-size: 13px;
    line-height: 1.75;
  }

  .spread-list {
    padding: 3rem 0 5rem;
  }

  .spread {
    margin-bottom: 4.5rem;
  }

  /* A · Cover */
  .cover-figure {
    height: auto;
    aspect-ratio: 4 / 5;
    min-height: 0;
  }

  .cover-cat {
    top: 1rem;
    right: 1.2rem;
    font-size: 9px;
    letter-spacing: 0.28em;
  }

  .cover-overlay {
    left: 1.4rem;
    right: 1.4rem;
    bottom: 1.4rem;
    gap: 0.7rem;
  }

  .cover-num {
    font-size: 9px;
    letter-spacing: 0.32em;
  }

  .cover-title {
    font-size: clamp(1.4rem, 6.5vw, 2rem);
  }

  .cover-cta {
    font-size: 10px;
    letter-spacing: 0.22em;
  }

  /* B · Asymmetric → stack */
  .asym-grid {
    grid-template-columns: 1fr;
    gap: 1.4rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }

  .asym-side {
    padding-top: 0.4rem;
    gap: 0.8rem;
  }

  .asym-thumb {
    aspect-ratio: 4 / 3;
    margin: 0.5rem 0 0.5rem;
  }

  /* C · Centered */
  .centered-spread {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    gap: 1.3rem;
  }

  .centered-figure {
    aspect-ratio: 4 / 3;
  }

  .centered-foot {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }

  .centered-caption {
    font-size: 12px;
  }

  /* D · Split → stack */
  .split-grid {
    grid-template-columns: 1fr;
    gap: 1.4rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }

  .split-text {
    padding-right: 0;
    gap: 0.7rem;
  }

  .split-big-num {
    font-size: clamp(2.4rem, 13vw, 3.6rem);
  }

  .split-figure {
    min-height: 0;
    aspect-ratio: 4 / 5;
  }

  .spread-title,
  .split-title {
    font-size: clamp(1.4rem, 6vw, 2rem);
  }

  .spread-cta {
    font-size: 10px;
    letter-spacing: 0.22em;
  }
}

@media (max-width: 600px) {
  .empty-state {
    padding: 2rem 1.5rem 4rem;
  }
}
</style>
