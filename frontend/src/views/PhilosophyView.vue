<template>
  <div class="philosophy-page" :class="{ 'is-visible': isLoaded }">

    <!-- ═════ Full-bleed editorial hero ═════ -->
    <section class="philo-hero">
      <img
        src="/images/showroom-building.png"
        alt="ATTIQUE DESIGN — Hannam showroom building"
        class="philo-hero-img"
        fetchpriority="high"
      />
      <div class="hero-vignette"></div>

      <div class="hero-overlay">
        <span class="hero-kicker" v-reveal="{ delay: 100 }">ATTIQUE DESIGN · ABOUT</span>
        <h1 class="hero-title" v-reveal="{ delay: 200 }">
          Where Curation<br />Meets <em>Living.</em>
        </h1>
        <p class="hero-meta" v-reveal="{ delay: 400 }">
          <span class="hero-meta-place">HANNAM</span>
          <span class="hero-meta-sep"></span>
          <span class="hero-meta-addr">서울시 용산구 한남대로 21길 27 · 아띠끄빌딩</span>
        </p>
      </div>
    </section>

    <!-- ═════ Brand story — editorial pull-quote × body ═════ -->
    <section class="philo-section story-section">
      <div class="story-grid">
        <div class="story-aside" v-reveal>
          <span class="block-label">BRAND STORY</span>
          <h2 class="story-pullquote">
            공간에 깊이를 더하는,<br /><em>아띠끄디자인.</em>
          </h2>
        </div>
        <div class="story-body" v-reveal="{ delay: 150 }">
          <p class="story-text">
            미국과 유럽의 하이엔드 가구와 소품을 국내에 직접 소개하고자 아띠끄 디자인을 설립했습니다.
          </p>
          <p class="story-text">
            청담 쇼룸을 시작으로 인테리어와 리빙을 아우르는 브랜드로 자리잡았고,
            단일 브랜드가 아닌 대표의 안목으로 엄선한 다양한 해외 가구와 소품을
            조합해 고객만의 공간을 완성해왔습니다.
          </p>
          <p class="story-text">
            2020년 한남동 아띠끄빌딩을 신축하고 쇼룸을 이전해,
            인테리어 시공과 가구·소품 판매를 이어오고 있습니다.
          </p>
        </div>
      </div>
    </section>

    <!-- ═════ History — Cheongdam chapter ═════ -->
    <section class="philo-section history-section">
      <header class="section-head" v-reveal>
        <span class="block-label">CHAPTER · 01</span>
        <h2 class="section-title">
          Cheongdam <em>Origins.</em>
        </h2>
        <p class="section-lead">
          청담 쇼룸에서 시작된, 큐레이션과 라이프스타일의 첫 챕터.
        </p>
      </header>

      <div class="cheongdam-grid">
        <figure class="cd-cover" v-reveal="{ delay: 100 }">
          <div class="cd-img-wrap">
            <img
              src="/images/about/original.png"
              alt="The original ATTIQUE DESIGN showroom in Cheongdam (2012)"
              class="cd-img"
            />
          </div>
          <span class="photo-mark photo-mark-left">
  <span class="mark-year"><em>2012</em></span>
          </span>
        </figure>

        <figure class="cd-cover" v-reveal="{ delay: 220 }">
          <div class="cd-img-wrap">
            <img
              src="/images/about/original_second.png"
              alt="The second ATTIQUE DESIGN showroom in Cheongdam (2017)"
              class="cd-img"
            />
          </div>
          <span class="photo-mark photo-mark-right">
  <span class="mark-year"><em>2017</em></span>
          </span>
        </figure>
      </div>

      <!-- Timeline -->
      <ol class="timeline" v-reveal="{ delay: 200 }">
        <li
          v-for="item in timeline"
          :key="item.year"
          class="timeline-item"
          :class="{ 'is-highlight': item.highlight }"
        >
          <span class="timeline-year">{{ item.year }}</span>
          <span class="timeline-event">{{ item.event }}</span>
        </li>
      </ol>
    </section>

    <!-- ═════ Philosophy closer ═════ -->
    <section class="philo-section philosophy-section">
      <div class="philosophy-inner" v-reveal>
        <span class="block-label centered">PHILOSOPHY</span>
        <h2 class="philosophy-statement">
          Balance of Space &amp; <em>Life.</em>
        </h2>
        <p class="philosophy-lead">
          머무는 사람의 일상과 공간이 자연스럽게 어우러지는 균형.<br />
          아띠끄 디자인의 고민은 여기서 시작합니다.
        </p>
        <span class="philosophy-rule"></span>
        <p class="philosophy-tail">
          정제된 시선으로 엄선한 셀렉션과 세밀한 맞춤 설계로,<br />
          고객의 라이프스타일이 담긴 공간을 제안합니다.
        </p>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isLoaded = ref(false)

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
  }, 100)
})

const timeline = [
  { year: '2012',    event: '아띠끄 디자인 설립' },
  { year: '2010s',   event: '청담 쇼룸 운영 · 드라마·잡지 스타일링 · 주거/상업 프로젝트' },
  { year: '2020',    event: '한남동 아띠끄빌딩 신축 및 쇼룸 이전' },
  { year: '2026.05', event: '한남 쇼룸 리뉴얼 오픈', highlight: true },
]
</script>

<style scoped>
.philosophy-page {
  background-color: #F5F0E8;
  color: #2C2C2C;
  opacity: 0;
  transition: opacity 0.6s ease;
}

.philosophy-page.is-visible {
  opacity: 1;
}

/* ── Hero ───────────────────────────────────────────── */
.philo-hero {
  position: relative;
  width: 100%;
  height: calc(100vh - 140px);
  min-height: 540px;
  overflow: hidden;
  background-color: #3D1C1B;
}

.philo-hero-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  display: block;
}

.hero-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(30, 12, 11, 0.55) 0%,
    rgba(30, 12, 11, 0.18) 38%,
    transparent 65%);
  z-index: 2;
  pointer-events: none;
}

.hero-overlay {
  position: absolute;
  left: 4rem;
  bottom: 4rem;
  z-index: 5;
  max-width: 640px;
  pointer-events: none;
  color: #F5F0E8;
}

.hero-kicker {
  display: inline-block;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: rgba(245, 240, 232, 0.86);
  text-transform: uppercase;
  margin-bottom: 1.4rem;
  text-shadow: 0 1px 8px rgba(30, 12, 11, 0.5);
}

.hero-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 4.4vw, 3.8rem);
  font-weight: 400;
  line-height: 1.08;
  color: #F5F0E8;
  margin: 0 0 1.6rem 0;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 24px rgba(30, 12, 11, 0.45);
}

.hero-title em {
  font-style: italic;
  color: #E8C7A0;
  font-weight: inherit;
}

.hero-meta {
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  margin: 0;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 400;
  letter-spacing: 0.22em;
  color: rgba(245, 240, 232, 0.82);
  text-transform: uppercase;
  text-shadow: 0 1px 10px rgba(30, 12, 11, 0.5);
}

.hero-meta-place {
  font-weight: 600;
  letter-spacing: 0.36em;
}

.hero-meta-sep {
  display: inline-block;
  width: 28px;
  height: 1px;
  background-color: rgba(245, 240, 232, 0.5);
}

.hero-meta-addr {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  letter-spacing: 0.04em;
  text-transform: none;
}

/* ── Editorial section frame ────────────────────────── */
.philo-section {
  max-width: 1280px;
  margin: 0 auto;
  padding: 8rem 4rem;
  box-sizing: border-box;
}

.philo-section + .philo-section {
  padding-top: 0;
}

.block-label {
  display: inline-block;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: #953735;
  text-transform: uppercase;
}

.block-label.centered {
  display: inline-block;
}

/* ── Brand story ────────────────────────────────────── */
.story-grid {
  display: grid;
  grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr);
  gap: 5rem;
  align-items: start;
}

.story-aside {
  position: sticky;
  top: 160px;
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.story-pullquote {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(1.6rem, 2.6vw, 2.4rem);
  font-weight: 400;
  line-height: 1.2;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.story-pullquote em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.story-body {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.story-text {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  line-height: 1.85;
  color: #555250;
  margin: 0;
  font-weight: 400;
  word-break: keep-all;
}

/* ── Section heads ──────────────────────────────────── */
.section-head {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-bottom: 4rem;
  max-width: 720px;
}

.section-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 3.6vw, 3rem);
  font-weight: 400;
  line-height: 1.1;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.01em;
}

.section-title em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.section-lead {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
  word-break: keep-all;
}

/* ── Cheongdam grid ─────────────────────────────────── */
.cheongdam-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 5rem;
}

.cd-cover {
  margin: 0;
  position: relative;
  isolation: isolate;
}

.cd-img-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  background-color: #EFE9DD;
  filter: grayscale(0.1);
  transition: filter 0.6s ease;
}

.cd-img-wrap::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.55) 0%,
    rgba(0, 0, 0, 0.15) 38%,
    transparent 65%);
  pointer-events: none;
  z-index: 2;
}

.cd-img-wrap:hover {
  filter: grayscale(0);
}

.cd-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.cd-img-wrap:hover .cd-img {
  transform: scale(1.04);
}

.photo-mark {
  position: absolute;
  bottom: 1.6rem;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  pointer-events: none;
  color: #FFFFFF;
}

.photo-mark-left {
  left: 1.6rem;
  align-items: flex-start;
}

.photo-mark-right {
  right: 1.6rem;
  align-items: flex-end;
}

.mark-place {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.36em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.mark-year {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2.6rem, 5vw, 4.6rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.01em;
  color: #FFFFFF;
  text-shadow: 0 2px 28px rgba(0, 0, 0, 0.4);
}

.mark-year em {
  font-style: italic;
  font-weight: inherit;
}

/* ── Timeline ───────────────────────────────────────── */
.timeline {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.timeline-item {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 2.5rem;
  align-items: baseline;
  padding: 1.8rem 0;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  transition: padding-left 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.timeline-item:hover {
  padding-left: 0.6rem;
}

.timeline-item:last-child {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.timeline-year {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-style: italic;
  font-size: 22px;
  font-weight: 400;
  color: #312E2D;
  letter-spacing: 0.005em;
}

.timeline-item.is-highlight .timeline-year {
  color: #953735;
}

.timeline-event {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #555250;
  font-weight: 400;
  word-break: keep-all;
}

/* ── Philosophy closer ──────────────────────────────── */
.philosophy-section {
  padding-bottom: 10rem;
}

.philosophy-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.6rem;
}

.philosophy-statement {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2.2rem, 4vw, 3.4rem);
  font-weight: 400;
  line-height: 1.1;
  color: #312E2D;
  margin: 0.2rem 0 0 0;
  letter-spacing: -0.01em;
}

.philosophy-statement em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.philosophy-lead {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  line-height: 1.85;
  color: #555250;
  margin: 0.6rem 0 0 0;
  font-weight: 400;
  word-break: keep-all;
}

.philosophy-rule {
  display: block;
  width: 40px;
  height: 1px;
  background-color: #953735;
  opacity: 0.5;
  margin: 1.4rem 0;
}

.philosophy-tail {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.85;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
  font-style: italic;
  word-break: keep-all;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 1100px) {
  .hero-overlay {
    left: 2.5rem;
    bottom: 3rem;
  }

  .philo-section {
    padding: 6rem 2.5rem;
  }

  .story-grid {
    gap: 3rem;
  }

  .story-aside {
    position: static;
    top: auto;
  }
}

@media (max-width: 768px) {
  /* Match hero container to image aspect on mobile —
     no crop, no letterbox. Building image is 1:1. */
  .philo-hero {
    height: auto;
    aspect-ratio: 1 / 1;
    min-height: 0;
  }

  .hero-overlay {
    left: 1.4rem;
    right: 1.4rem;
    bottom: 1.6rem;
    max-width: none;
  }

  .hero-kicker {
    font-size: 10px;
    letter-spacing: 0.3em;
    margin-bottom: 0.8rem;
  }

  .hero-title {
    font-size: clamp(1.4rem, 6.5vw, 2rem);
    margin-bottom: 1rem;
  }

  .hero-meta {
    flex-wrap: wrap;
    gap: 0.6rem;
    font-size: 9px;
    letter-spacing: 0.18em;
  }

  .hero-meta-sep {
    width: 18px;
  }

  .hero-meta-addr {
    font-size: 11px;
  }

  .philo-section {
    padding: 4rem 1.5rem;
  }

  .story-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .story-pullquote {
    font-size: clamp(1.3rem, 5.4vw, 1.8rem);
  }

  .story-text {
    font-size: 14px;
    line-height: 1.75;
  }

  .section-head {
    margin-bottom: 2.5rem;
  }

  .section-title {
    font-size: clamp(1.6rem, 6vw, 2.2rem);
  }

  .section-lead {
    font-size: 13px;
  }

  .cheongdam-grid {
    grid-template-columns: 1fr;
    gap: 1.2rem;
    margin-bottom: 3rem;
  }

  .cd-img-wrap {
    aspect-ratio: 3 / 4;
  }

  .photo-mark {
    bottom: 1rem;
    gap: 0.45rem;
  }

  .photo-mark-left { left: 1rem; }
  .photo-mark-right { right: 1rem; }

  .mark-place {
    font-size: 9px;
    letter-spacing: 0.32em;
  }

  .mark-year {
    font-size: clamp(1.9rem, 8.5vw, 2.8rem);
  }

  .timeline-item {
    grid-template-columns: 88px 1fr;
    gap: 1.2rem;
    padding: 1.2rem 0;
  }

  .timeline-year {
    font-size: 17px;
  }

  .timeline-event {
    font-size: 13px;
    line-height: 1.6;
  }

  .philosophy-section {
    padding-bottom: 6rem;
  }

  .philosophy-statement {
    font-size: clamp(1.6rem, 7vw, 2.2rem);
  }

  .philosophy-lead {
    font-size: 14px;
  }

  .philosophy-tail {
    font-size: 13px;
  }
}
</style>
