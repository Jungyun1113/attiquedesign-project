<template>
  <div class="philosophy-page">
    <div ref="philoRef" class="philo-container" :class="{ 'is-visible': philoVisible }">
      <!-- 거대한 오버래핑 타이틀: 섹션 상단에 걸쳐짐 -->
      <h2 class="philo-title">
        Where Curation Meets <em class="philo-accent">Living</em>.
      </h2>

      <!-- 오버래핑 본문 (타이틀과 레이어 겹침) -->
      <div class="philo-body-block">
        <div class="philo-body">
          <p class="philo-text">머무는 사람의 일상과 공간이 자연스럽게 어우러지는 균형.<br>아띠끄 디자인의 고민은 여기서 시작합니다.</p>
          <p class="philo-text">해외 하이엔드 가구를 엄선해 소개하고, 스타일링과 인테리어 시공까지 함께하는 토탈 리빙 브랜드입니다.<br>까다롭게 선별한 셀렉션과 아띠끄만의 모던 클래식 감도로, 일상이 달라지는 공간을 제안합니다.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const philoVisible = ref(false)

onMounted(() => {
  // 바로 보이게 하거나, Intersection Observer 사용 가능
  setTimeout(() => {
    philoVisible.value = true
  }, 100)
})
</script>

<style scoped>
.philosophy-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px); /* 헤더 높이 고려 */
  display: flex;
  align-items: flex-start;
}

.philo-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 100%;
  padding: 2.5rem 4rem 4rem;
  position: relative;
}

/* 개별 요소 fade-up 트랜지션 */
.philo-container .philo-title,
.philo-container .philo-body-block {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.philo-container.is-visible .philo-title {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.1s;
}

.philo-container.is-visible .philo-body-block {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.35s;
}

/* 거대 오버래핑 타이틀 */
.philo-title {
  font-family: 'Playfair Display', 'Cormorant Garamond', serif;
  font-size: clamp(34px, 6vw, 68px);
  font-weight: 400;
  line-height: 1.25;
  color: #312E2D;
  letter-spacing: 0.01em;
  margin: 0 0 -2.5rem 0; /* 오버래핑: 아래 본문과 겹침 */
  word-break: keep-all;
  position: relative;
  z-index: 2;
}

.philo-accent {
  font-style: italic;
  font-family: 'Playfair Display', serif;
  color: #953735;
  font-weight: 500;
  letter-spacing: 0.04em;
}

/* 본문 블록 — 타이틀과 오버랩 */
.philo-body-block {
  position: relative;
  z-index: 1;
  padding-top: 4.5rem;
  max-width: 650px;
  margin-left: 0;
  margin-right: auto;
}

/* 눈썹 라벨 */
.philo-eyebrow {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}
.philo-eyebrow-line {
  display: block;
  width: 36px;
  height: 1px;
  background: #000;
}
.philo-eyebrow-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  font-weight: 400;
  letter-spacing: 0.48em;
  text-transform: uppercase;
  color: #000;
  margin: 0;
}

/* 본문 */
.philo-text {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.7;
  color: #6D6059;
  word-break: keep-all;
  overflow-wrap: break-word;
  margin: 0;
}

.philo-text:first-child {
  margin-bottom: 1.4rem;
}


@media (max-width: 768px) {
  .philo-container {
    padding: 1.5rem 1.5rem 6rem;
  }
  .philo-body-block {
    margin-right: 0;
    padding-top: 3.5rem;
  }
}
</style>
