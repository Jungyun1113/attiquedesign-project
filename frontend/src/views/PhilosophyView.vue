<template>
  <div class="philosophy-page">
    <div class="philo-container" :class="{ 'is-visible': isLoaded }">
      
      <!-- Section 1: Brand Story -->
      <section class="philo-section story-section">
        <h2 class="philo-title">
          Where Curation Meets <em class="philo-accent">Living</em>.
        </h2>
        <div class="section-content">
          <div class="eyebrow">BRAND STORY</div>
          <p class="description">
            미국과 유럽의 하이엔드 가구와 소품을 국내에 직접 소개하고자 아띠끄 디자인을 설립했습니다.<br>
            청담 쇼룸을 시작으로 인테리어와 리빙을 아우르는 브랜드로 자리잡았고,<br>
            단일 브랜드가 아닌 대표의 안목으로 엄선한 다양한 해외 가구와 소품을 조합해 고객만의 공간을 완성해왔습니다.<br>
            2020년 한남동 아띠끄빌딩을 세우고 쇼룸을 이전해, 인테리어 시공과 가구·소품 판매를 이어오고 있습니다.
          </p>
        </div>
      </section>

      <!-- Section 2: History -->
      <section class="philo-section history-section">
        <div class="eyebrow">HISTORY</div>
        <div class="history-list">
          <div class="history-item">
            <span class="year">2012</span>
            <span class="event">아띠끄 디자인 설립</span>
          </div>
          <div class="history-item">
            <span class="year">2010s</span>
            <span class="event">청담 쇼룸 운영 · 드라마·잡지 스타일링 · 주거/상업 프로젝트</span>
          </div>
          <div class="history-item">
            <span class="year">2020</span>
            <span class="event">한남동 아띠끄빌딩 건립 및 쇼룸 이전</span>
          </div>
          <div class="history-item">
            <span class="year highlight">2026.05</span>
            <span class="event">한남 쇼룸 리뉴얼 오픈</span>
          </div>
        </div>
      </section>

      <!-- Section 3: Philosophy -->
      <section class="philo-section philosophy-section">
        <div class="eyebrow">PHILOSOPHY</div>
        <h3 class="philo-sub-title">Balance of Space & Life</h3>
        <p class="description">
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
  color: #312E2D;
}

.philo-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem 10rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease;
}

.philo-container.is-visible {
  opacity: 1;
  transform: translateY(0);
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
.philo-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(40px, 8vw, 72px);
  font-weight: 400;
  line-height: 1.1;
  margin-bottom: 4rem;
  word-break: keep-all;
}

.philo-accent {
  font-style: italic;
  color: #953735;
}

.story-section .section-content {
  max-width: 700px;
  margin-left: auto;
}

.description {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  line-height: 1.8;
  color: #555250;
  word-break: keep-all;
}

/* Section 2: History */
.history-section {
  max-width: 900px;
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
  color: #312E2D;
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

@media (max-width: 768px) {
  .philo-container {
    padding: 3rem 1.5rem 6rem;
  }
  
  .philo-section {
    margin-bottom: 5rem;
  }

  .philo-title {
    font-size: 40px;
    margin-bottom: 3rem;
  }

  .story-section .section-content {
    margin-left: 0;
  }

  .history-item {
    flex-direction: column;
    gap: 0.5rem;
    padding-bottom: 1rem;
  }

  .year {
    font-size: 16px;
    min-width: auto;
  }

  .event {
    font-size: 14px;
  }

  .philo-sub-title {
    font-size: 24px;
  }
}
</style>
