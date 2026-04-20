<template>
  <div class="interior-page">
    <div class="global-page-container interior-container">
      <div class="interior-header">
        <h1 class="global-eng-subtitle interior-title">Built, Furnished and <em>Styled.</em></h1>
        <div class="interior-subtitle-group">
          <p class="global-kor-desc interior-subtitle">상담부터 완공까지, 당신의 공간에 온전히 집중합니다.</p>
          <p class="global-kor-desc interior-desc">공간의 구조부터 가구, 소품까지 아띠끄의 시선으로 완성합니다.</p>
        </div>
      </div>

      <div class="process-grid">
        <div v-for="(step, i) in steps" :key="i" class="process-item">
          <span class="process-number">0{{ i + 1 }}</span>
          <h3 class="process-title">{{ step.title }}</h3>
          <p class="global-kor-desc process-desc-text">{{ step.desc }}</p>
        </div>
      </div>

      <div class="interior-cta">
        <a
          href="https://m.booking.naver.com/booking/6/bizes/1563733/items/7301622?area=plt&lang=ko&theme=place"
          target="_blank"
          rel="noopener noreferrer"
          class="global-btn-main"
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

.interior-header {
  display: flex;
  flex-direction: column;
}

/* 소제목 마진 조정: 인테리어 메뉴만 살짝 좁게 */
.interior-title {
  margin-bottom: 2rem !important;
}

.interior-subtitle-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 3rem;
}

.interior-desc {
  opacity: 0.7;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 4rem;
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
}

.process-desc-text {
  font-size: 14px;
}

.interior-cta {
  display: flex;
}

@media (max-width: 768px) {
  .process-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .interior-title {
    margin-bottom: 1.5rem !important;
  }

  .interior-subtitle-group {
    margin-bottom: 2.5rem;
  }

  .interior-subtitle {
    font-size: 14px;
  }

  .interior-desc {
    font-size: 12px;
  }

  .process-title {
    font-size: 16px;
  }

  .process-desc-text {
    font-size: 13px;
    line-height: 1.6;
  }
}
</style>
