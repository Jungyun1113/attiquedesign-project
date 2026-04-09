<template>
  <div class="portfolio-detail-page">
    <div class="portfolio-detail-content" :class="{ 'is-visible': isAnimated }">
      <!-- Top Text Section -->
      <div class="detail-header">
        <h1 class="detail-title">{{ itemData?.label }}</h1>
        <p class="detail-desc">{{ itemData?.desc }}</p>
      </div>

      <!-- Arrow Indicators for gallery hints -->
      <div class="gallery-indicators fade-in-delay">
        <span class="indicator-line">SCROLL TO EXPLORE</span>
        <div class="indicator-arrows">
          <span class="arrow-left">←</span>
          <span class="arrow-right">→</span>
        </div>
      </div>

      <!-- Horizontal Scroll Gallery -->
      <div class="detail-gallery-wrap fade-in-delay">
        <div class="gallery-scrollable">
          <img :src="itemData?.img" :alt="itemData?.label" class="gallery-img" />
          <!-- Dummy gallery images for exhibition feel -->
          <img src="https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=1200&q=80" alt="Detail 1" class="gallery-img" />
          <img src="https://images.unsplash.com/photo-1593696140826-c58b021acf8b?w=1200&q=80" alt="Detail 2" class="gallery-img" />
          <img src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=1200&q=80" alt="Detail 3" class="gallery-img" />
          <img src="https://images.unsplash.com/photo-1600607687644-c7171b42498f?w=1200&q=80" alt="Detail 4" class="gallery-img" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isAnimated = ref(false)

const portfolioDB: Record<string, { label: string; img: string; desc: string }> = {
  'residential': {
    label: 'Residential',
    img: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1800&q=85',
    desc: '주거 공간의 일상과 미학이 자연스럽게 어우르는 곳. 거주자의 고유한 취향이 묻어나는 프라이빗한 공간을 제안합니다.'
  },
  'commercial': {
    label: 'Commercial',
    img: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1800&q=85',
    desc: '브랜드의 아이덴티티를 공간으로 번역하는 예술. 방문객에게 잊을 수 없는 시각적 경험을 선사하는 하이엔드 상업 공간 디자인.'
  },
  'drama': {
    label: 'Drama',
    img: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1400&q=85',
    desc: '드라마와 영화 속에서 만나는 아띠끄의 미학. 극의 몰입도를 높이고 캐릭터의 깊이를 더해주는 정교한 세트 스타일링.'
  },
  'magazine': {
    label: 'Magazine',
    img: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=1400&q=85',
    desc: '매거진의 질감으로 편집된 화려함. 시대의 트렌드와 예술적 영감을 결합하여 강렬한 인상을 남기는 에디토리얼 공간.'
  }
}

const itemData = ref(portfolioDB[route.params.id as string])

onMounted(() => {
  window.scrollTo(0,0)
  setTimeout(() => {
    isAnimated.value = true
  }, 100)
})

function goBack() {
  router.push('/#portfolio')
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.portfolio-detail-page {
  width: 100vw;
  min-height: 100vh;
  background: #FDFBF8; /* Ivory */
  color: #2B1D1B;
  display: flex;
  flex-direction: column;
}

.portfolio-detail-content {
  flex: 1;
  padding: 6rem 4rem 4rem; /* top padding reduced from 10rem to 6rem */
  display: flex;
  flex-direction: column;
}

/* Header Text */
.detail-header {
  text-align: center;
  max-width: 850px;
  margin: 0 auto 5rem;
}

.detail-title {
  font-family: 'Pretendard', sans-serif;
  font-size: 26px;
  font-weight: 500;
  color: #111;
  margin-bottom: 2.2rem;
  letter-spacing: 0.02em;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s ease 0.1s;
}

.detail-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  font-weight: 300;
  line-height: 1.9;
  color: #555;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s ease 0.3s;
  word-break: keep-all;
}

/* Gallery Indicators */
.gallery-indicators {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  margin-bottom: 0.8rem;
  border-bottom: 1px solid #E8E2D7;
  padding-bottom: 1rem;
}

.indicator-line {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  letter-spacing: 0.25em;
  color: #888;
}

.indicator-arrows {
  display: flex;
  gap: 1.5rem;
  font-size: 18px;
  color: #111;
}

/* Horizontal Gallery */
.detail-gallery-wrap {
  width: 100%;
  margin-bottom: 6rem;
}

.gallery-scrollable {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 2rem;
  scrollbar-width: thin;
  scrollbar-color: #E8E2D7 transparent;
}

.gallery-scrollable::-webkit-scrollbar {
  height: 2px;
}
.gallery-scrollable::-webkit-scrollbar-track {
  background: transparent;
}
.gallery-scrollable::-webkit-scrollbar-thumb {
  background: #E8E2D7;
}

.gallery-img {
  height: 70vh;
  width: auto;
  object-fit: contain;
  flex-shrink: 0;
  background: #F9F8F6;
}

/* Animations Trigger */
.is-visible .detail-title,
.is-visible .detail-desc {
  opacity: 1;
  transform: translateY(0);
}

.fade-in-delay {
  opacity: 0;
  animation: fadeIn 1.2s ease 0.6s forwards;
}

@keyframes fadeIn {
  to { opacity: 1; }
}

@media (max-width: 1024px) {
  .portfolio-detail-content {
    padding: 6rem 2rem 2rem; /* Reduced top padding */
  }
  .gallery-img {
    height: 50vh;
  }
}
</style>
