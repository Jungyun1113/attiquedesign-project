<template>
  <div class="interior-page">
    <div class="interior-container">
      <div class="interior-header">
        <h1 class="interior-title">Built, Furnished and <em>Styled.</em></h1>
        <p class="interior-subtitle">상담부터 완공까지, 당신의 공간에 온전히 집중합니다.</p>
        <p class="interior-desc">공간의 구조부터 가구, 소품까지 아띠끄의 시선으로 완성합니다.</p>
      </div>

      <div class="process-grid">
        <div v-for="(step, i) in steps" :key="i" class="process-item">
          <span class="process-number">0{{ i + 1 }}</span>
          <h3 class="process-title">{{ step.title }}</h3>
          <p class="process-desc">{{ step.desc }}</p>
        </div>
      </div>

      <div class="interior-cta">
        <a
          href="https://m.booking.naver.com/booking/6/bizes/1563733/items/7301622?area=plt&lang=ko&theme=place"
          target="_blank"
          rel="noopener noreferrer"
          class="btn-booking"
        >방문상담 예약하기</a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const steps = [
  { title: '프라이빗 상담', desc: '한남 쇼룸에서 1:1 맞춤 상담으로 고객의 라이프스타일과 공간을 깊이 이해합니다.' },
  { title: '컨셉 설계 & 견적', desc: '공간 콘셉트 보드와 3D 시뮬레이션을 통해 완성될 공간을 미리 경험합니다.' },
  { title: '시공 & 스타일링', desc: '전문 시공팀의 꼼꼼한 시공과 아띠끄 셀렉션의 가구·소품 배치까지 원스톱으로 완성합니다.' },
]
</script>

<style scoped>
.interior-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
  display: flex;
  align-items: flex-start;
}

.interior-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem 4rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.interior-header {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.interior-eyebrow {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.4em;
  color: rgba(49, 46, 45, 0.45);
}

.interior-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(28px, 4vw, 52px);
  font-weight: 400;
  line-height: 1.2;
  color: #312E2D;
  margin: 0;
}

.interior-title em {
  font-style: italic;
  color: #953735;
}

.interior-subtitle {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  word-break: keep-all;
  max-width: 560px;
}

.interior-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.7;
  color: rgba(49, 46, 45, 0.5);
  margin: 0;
  word-break: keep-all;
  max-width: 560px;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.process-item {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.process-number {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #953735;
}

.process-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 400;
  color: #312E2D;
  margin: 0;
}

.process-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.75;
  color: #6D6059;
  margin: 0;
  word-break: keep-all;
}

.interior-cta {
  display: flex;
}

.btn-booking {
  display: inline-block;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.25em;
  padding: 1.1rem 2.6rem;
  background-color: #312E2D;
  color: #fff;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-booking:hover,
.btn-booking:active {
  background-color: #953735;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 모바일: 가로 3단 유지, 폰트/패딩 축소 */
@media (max-width: 768px) {
  .interior-page {
    height: auto;
    min-height: calc(100vh - 120px);
    overflow: visible;
  }

  .interior-container {
    padding: 2rem 1.2rem;
    gap: 2rem;
  }

  .process-grid {
    gap: 1rem;
  }

  .process-item {
    padding-top: 1rem;
    gap: 0.6rem;
  }

  .process-title {
    font-size: 14px;
  }

  .process-desc {
    font-size: 11px;
    line-height: 1.65;
  }

  .interior-subtitle {
    font-size: 12px;
  }

  .btn-booking {
    font-size: 10px;
    padding: 0.9rem 2rem;
    letter-spacing: 0.2em;
  }
}
</style>
