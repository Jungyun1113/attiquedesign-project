<template>
  <div class="selection-detail-page">
    <div class="selection-detail-container" :class="{ 'is-visible': isAnimated }">
      <div class="detail-image-wrap fade-in-delay">
        <img :src="itemData?.img" :alt="itemData?.label" class="detail-main-img" />
      </div>
      <div class="detail-text-wrap">
        <p class="detail-eyebrow">Product Detail</p>
        <h1 class="detail-title">{{ itemData?.label }}</h1>
        <p class="detail-desc">{{ itemData?.desc }}</p>

        <div class="mt-12 fade-in-delay">
          <button class="back-btn" @click="goBack" style="font-family: 'Montserrat', sans-serif;">
            ← Back to Selection
          </button>
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

interface SelectionDetail {
  label: string
  img: string
  desc: string
}

const selectionDB: Record<string, SelectionDetail> = {
  'obj-1': {
    label: 'Walnut Console',
    img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1800&q=85',
    desc: '고급스러운 월넛 우드의 결을 살린 미니멀 콘솔. 어떤 공간에도 깊이감을 더합니다.'
  },
  'obj-2': {
    label: 'Linen Armchair',
    img: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=1800&q=85',
    desc: '부드러운 리넨 소재와 인체공학적 설계가 돋보이는 암체어. 편안한 휴식을 선사합니다.'
  },
  'obj-3': {
    label: 'Ceramic Vase',
    img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=1800&q=85',
    desc: '장인의 손길이 닿은 세라믹 베이스. 단아한 곡선미가 시선을 머물게 합니다.'
  },
  'obj-4': {
    label: 'Wool Rug',
    img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=1800&q=85',
    desc: '천연 울로 짜여진 견고한 러그. 발끝에 닿는 감촉이 일상에 포근함을 더합니다.'
  },
  'obj-5': {
    label: 'Brass Lamp',
    img: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=1800&q=85',
    desc: '빈티지한 브라스 마감의 스탠딩 램프. 공간을 따뜻하게 물들입니다.'
  },
  'obj-6': {
    label: 'Oak Dining Table',
    img: 'https://images.unsplash.com/photo-1549497538-303791108f95?w=1800&q=85',
    desc: '견고한 오크 우드의 다이닝 테이블. 다이닝 공간에 북유럽 감성을 더합니다.'
  },
  'obj-7': {
    label: 'Pendant Light',
    img: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=1800&q=85',
    desc: '모던한 실루엣의 펜던트 조명. 미니멀한 공간에 완벽한 빛을 내립니다.'
  },
  'obj-8': {
    label: 'Wool Throw',
    img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=1800&q=85',
    desc: '섬세하게 짜여진 울 담요. 쌀쌀한 날씨에 안락함을 선사합니다.'
  },
  'obj-9': {
    label: 'Minimal Vase',
    img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=1800&q=85',
    desc: '구조적인 미니멀 화병. 꽃이 없어도 그 자체로 작품이 됩니다.'
  }
}

const itemData = ref(selectionDB[route.params.id as string])

onMounted(() => {
  setTimeout(() => { isAnimated.value = true }, 100)
})

function goBack() {
  router.push('/#selection')
}
</script>

<style scoped>
.selection-detail-page {
  width: 100vw;
  min-height: 100vh;
  background: #FDFBF8;
  color: #111;
  display: flex;
  justify-content: center;
  padding: 8rem 6rem 4rem; /* top padding adjusted, and centering preserved but moves up with alignment */
  align-items: flex-start; /* Aligned to top to be visible immediately */
}

.selection-detail-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6rem;
  max-width: 1400px;
  width: 100%;
  align-items: center;
}

.detail-image-wrap {
  width: 100%;
  aspect-ratio: 4 / 5;
  background: #E8E2D7;
  overflow: hidden;
}

.detail-main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s ease;
}
.detail-image-wrap:hover .detail-main-img {
  transform: scale(1.05);
}

.detail-text-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.detail-eyebrow {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.1s;
}

.detail-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3rem, 4vw, 4rem);
  font-weight: 400;
  color: #111;
  line-height: 1.1;
  margin-bottom: 2.5rem;
  font-style: italic;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s;
}

.detail-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  font-weight: 300;
  line-height: 1.8;
  color: #444;
  word-break: keep-all;
  max-width: 500px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.5s;
}

.fade-in-delay {
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.7s;
}

.is-visible .detail-eyebrow,
.is-visible .detail-title,
.is-visible .detail-desc,
.is-visible .fade-in-delay {
  opacity: 1;
  transform: translateY(0);
}

.back-btn {
  background: transparent;
  border: 1px solid #d1cbc0;
  color: #111;
  padding: 0.75rem 2rem;
  font-size: 10px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.4s ease;
}

.back-btn:hover {
  background: #f1f0ea;
  border-color: #111;
}

@media (max-width: 1024px) {
  .selection-detail-container {
    grid-template-columns: 1fr;
    gap: 4rem;
  }
  .selection-detail-page {
    padding: 6rem 1.5rem 2rem;
  }
}

</style>
