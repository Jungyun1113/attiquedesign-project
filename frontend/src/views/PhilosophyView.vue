<template>
  <div class="philosophy-page">
    <div class="global-page-container philo-container" :class="{ 'is-visible': isLoaded }">
      
      <!-- Section 1: Brand Story -->
      <section class="philo-section story-section">
        <h2 class="global-eng-subtitle philo-title">
          Where Curation Meets <em class="philo-accent">Living</em>.
        </h2>
        <div class="section-content">
          <div class="eyebrow">BRAND STORY</div>
          <p class="global-kor-desc description">
            미국과 유럽의 하이엔드 가구와 소품을 국내에 직접 소개하고자 아띠끄 디자인을 설립했습니다.<br>
            청담 쇼룸을 시작으로 인테리어와 리빙을 아우르는 브랜드로 자리잡았고,<br>
            단일 브랜드가 아닌 대표의 안목으로 엄선한 다양한 해외 가구와 소품을 조합해 고객만의 공간을 완성해왔습니다.<br>
            2020년 한남동 아띠끄빌딩을 신축하고 쇼룸을 이전해, 인테리어 시공과 가구·소품 판매를 이어오고 있습니다.
          </p>
        </div>
      </section>

      <!-- Section 2: History -->
      <section class="philo-section history-section">
        <!-- Asymmetric stagger: two showroom eras -->
        <header class="stagger-header">
          <span class="stagger-tag">청담 · CHEONGDAM</span>
          <span class="stagger-rule"></span>
        </header>

        <div class="history-stagger">
          <figure class="history-cover history-cover-lead">
            <div class="history-img-wrap">
              <img
                src="/images/about/original.png"
                alt="The original ATTIQUE DESIGN showroom"
                class="history-img"
              />
            </div>
            <span class="history-mark">2012</span>
          </figure>

          <figure class="history-cover history-cover-follow">
            <div class="history-img-wrap">
              <img
                src="/images/about/original_second.png"
                alt="The second ATTIQUE DESIGN showroom"
                class="history-img"
              />
            </div>
            <span class="history-mark">2017</span>
          </figure>
        </div>

        <!-- Timeline -->
        <div class="history-content">
          <div class="eyebrow eyebrow-centered">HISTORY</div>
          <div class="history-list">
            <div class="history-item">
              <span class="year">2012</span>
              <span class="global-kor-desc event">아띠끄 디자인 설립</span>
            </div>
            <div class="history-item">
              <span class="year">2010s</span>
              <span class="global-kor-desc event">청담 쇼룸 운영 · 드라마·잡지 스타일링 · 주거/상업 프로젝트</span>
            </div>
            <div class="history-item">
              <span class="year">2020</span>
              <span class="global-kor-desc event">한남동 아띠끄빌딩 신축 및 쇼룸 이전</span>
            </div>
            <div class="history-item">
              <span class="year highlight">2026.05</span>
              <span class="global-kor-desc event">한남 쇼룸 리뉴얼 오픈</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 3: Philosophy -->
      <section class="philo-section philosophy-section">
        <div class="eyebrow">PHILOSOPHY</div>
        <h3 class="philo-sub-title">Balance of Space & Life</h3>
        <p class="global-kor-desc description">
          머무는 사람의 일상과 공간이 자연스럽게 어우러지는 균형.<br>
          아띠끄 디자인의 고민은 여기서 시작합니다.<br><br>
          정제된 시선으로 엄선한 셀렉션과 세밀한 맞춤 설계로,<br>
          고객의 라이프스타일이 담긴 공간을 제안합니다.
        </p>
      </section>

    </div>
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
</script>

<style scoped>
.philosophy-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
  color: #2C2C2C;
}

.philo-section {
  margin-bottom: 8rem;
}

.philo-section:last-child {
  margin-bottom: 0;
}

/* Common Eyebrow */
.eyebrow {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.3em;
  color: #953735;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.eyebrow::after {
  content: '';
  display: block;
  width: 40px;
  height: 1px;
  background-color: #953735;
  opacity: 0.3;
}

/* Section 1: Story */
.philo-accent {
  font-style: italic;
  color: #953735;
}

.story-section .section-content {
  max-width: 700px;
  margin-left: auto;
}

/* Section 2: History — editorial cover shot + timeline */
.history-section {
  max-width: none;
}

/* Header above the stagger pair */
.stagger-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.stagger-tag {
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: #953735;
  text-transform: uppercase;
}

.stagger-rule {
  flex: 1;
  height: 1px;
  background-color: rgba(149, 55, 53, 0.2);
}

.stagger-meta {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 14px;
  color: #6D6059;
}

/* Asymmetric stagger: editorial layout with two photos at different sizes/positions */
.history-stagger {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  gap: 0;
  margin: 0 0 5rem 0;
  position: relative;
}

.history-cover {
  margin: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  isolation: isolate;
}

/* Lead photo: larger, anchored to left, top */
.history-cover-lead {
  padding-right: 4rem;
}

/* Follow photo: smaller, pushed down, anchored to right */
.history-cover-follow {
  margin-top: 28%;
  padding-left: 1rem;
}

/* Subtle year tag — tucked into the corner of the photo */
.history-mark {
  position: absolute;
  top: 1.2rem;
  left: 1.2rem;
  font-family: 'Montserrat', sans-serif;
  font-style: normal;
  font-size: 11px;
  font-weight: 500;
  color: #F5F0E8;
  line-height: 1;
  z-index: 3;
  letter-spacing: 0.32em;
  pointer-events: none;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.history-cover-follow .history-mark {
  left: auto;
  right: 1.2rem;
  top: 1.2rem;
}

.history-img-wrap {
  position: relative;
}

.history-img-wrap {
  width: 100%;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background-color: #EFE9DD;
  filter: grayscale(0.15);
  transition: filter 0.6s ease;
}

.history-img-wrap:hover {
  filter: grayscale(0);
}

.history-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 1.2s cubic-bezier(0.22, 1, 0.36, 1);
}

.history-img-wrap:hover .history-img {
  transform: scale(1.02);
}


/* Timeline: centered, narrow column */
.history-content {
  max-width: 640px;
  margin: 0 auto;
  padding-top: 1rem;
}

.eyebrow-centered {
  justify-content: center;
  text-align: center;
  margin-bottom: 2.5rem;
}

.eyebrow-centered::after {
  display: none;
}

.eyebrow-centered::before {
  content: '';
  display: block;
  width: 40px;
  height: 1px;
  background-color: #953735;
  opacity: 0.3;
  margin-right: 1rem;
}

.eyebrow-centered::after {
  content: '';
  display: block;
  width: 40px;
  height: 1px;
  background-color: #953735;
  opacity: 0.3;
  margin-left: 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.history-item {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.year {
  font-family: 'Montserrat', sans-serif;
  font-size: 18px;
  font-weight: 600;
  min-width: 100px;
  color: #2C2C2C;
}

.year.highlight {
  color: #953735;
}

.event {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  color: #555250;
  line-height: 1.5;
}

/* Section 3: Philosophy */
.philosophy-section {
  max-width: 700px;
}

.philo-sub-title {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

@media (max-width: 900px) {
  .history-stagger {
    grid-template-columns: 1fr;
    gap: 2.5rem;
    margin-bottom: 3rem;
  }

  .history-cover-lead {
    padding-right: 0;
  }

  .history-cover-follow {
    margin-top: 0;
    padding-left: 18%;
  }

  .history-mark {
    font-size: 10px;
    top: 0.8rem;
    left: 0.8rem;
  }

  .history-cover-follow .history-mark {
    right: 0.8rem;
    top: 0.8rem;
  }

  .stagger-header {
    margin-bottom: 1.8rem;
    gap: 0.8rem;
  }

  .history-content {
    max-width: 100%;
    padding-top: 0;
  }
}

@media (max-width: 600px) {
  .history-cover-follow {
    padding-left: 0;
  }
}

@media (max-width: 768px) {
  .philo-section {
    margin-bottom: 5rem;
  }
}
</style>
