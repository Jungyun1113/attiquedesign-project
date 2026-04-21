<template>
  <div class="selection-detail-page">
    <div class="selection-detail-container" :class="{ 'is-visible': isAnimated }">

      <div v-if="loading" class="detail-loading">
        <p>불러오는 중...</p>
      </div>

      <template v-else-if="selection">
        <header class="detail-header">
          <p class="detail-eyebrow">ATTIQUE SELECTION</p>
          <h1 class="detail-title">{{ selection.title }}</h1>
          <p v-if="selection.subtitle" class="detail-subtitle">{{ selection.subtitle }}</p>
          <p v-if="selection.description" class="detail-desc">{{ selection.description }}</p>
        </header>

        <div v-if="selection.images && selection.images.length" class="selection-images-grid">
          <div
            v-for="(img, idx) in selection.images"
            :key="img.id"
            class="selection-image-item"
            @click="openLightbox(idx)"
          >
            <img :src="img.image_url" alt="selection image" loading="lazy" />
          </div>
        </div>

        <div class="mt-12 fade-in-delay">
          <button class="back-btn" @click="goBack" style="font-family: 'Montserrat', sans-serif;">
            ← Back to Selection
          </button>
        </div>
      </template>

      <div v-else class="detail-loading">
        <p>셀렉션을 찾을 수 없습니다.</p>
        <button class="back-btn" @click="goBack" style="font-family: 'Montserrat', sans-serif; margin-top: 1rem;">
          ← Back to Selection
        </button>
      </div>

    </div>

    <!-- Lightbox Overlay -->
    <div v-if="lightboxOpen" class="lightbox-overlay" @click.self="closeLightbox">
      <button class="lightbox-close" @click="closeLightbox">✕</button>
      <button class="lightbox-prev" @click.stop="prevImage" v-if="(selection?.images?.length ?? 0) > 1">‹</button>
      <button class="lightbox-next" @click.stop="nextImage" v-if="(selection?.images?.length ?? 0) > 1">›</button>
      <img v-if="selection?.images?.length" :src="selection.images[lightboxIndex]?.image_url" class="lightbox-img" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { selectionService, type Selection } from '@/services/selection.service'

const route = useRoute()
const router = useRouter()
const isAnimated = ref(false)
const loading = ref(true)
const selection = ref<Selection | null>(null)

// Lightbox 상태
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

onMounted(async () => {
  try {
    selection.value = await selectionService.getSelectionById(route.params.id as string)
  } catch {
    selection.value = null
  } finally {
    loading.value = false
  }
  setTimeout(() => { isAnimated.value = true }, 100)
})

function openLightbox(index: number) {
  lightboxIndex.value = index
  lightboxOpen.value = true
  document.body.style.overflow = 'hidden' // 스크롤 방지
}

function closeLightbox() {
  lightboxOpen.value = false
  document.body.style.overflow = ''
}

function prevImage() {
  if (!selection.value) return
  lightboxIndex.value = (lightboxIndex.value - 1 + selection.value.images.length) % selection.value.images.length
}

function nextImage() {
  if (!selection.value) return
  lightboxIndex.value = (lightboxIndex.value + 1) % selection.value.images.length
}

function goBack() {
  router.push('/#selection')
}
</script>

<style scoped>
.selection-detail-page {
  width: 100%;
  min-height: 100vh;
  background: #F5F0E8;
  color: #111;
  padding: 8rem 6rem 4rem;
}

.selection-detail-container {
  max-width: 1400px;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.selection-detail-container.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.detail-loading {
  text-align: center;
  padding: 6rem 0;
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  color: #6D6059;
}

.detail-header {
  margin-bottom: 4rem;
}

.detail-eyebrow {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 1rem;
}

.detail-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 400;
  color: #111;
  line-height: 1.1;
  margin-bottom: 1rem;
  font-style: italic;
}

.detail-subtitle {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: #555;
  margin-bottom: 0.5rem;
}

.detail-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 300;
  line-height: 1.8;
  color: #444;
  max-width: 600px;
  word-break: keep-all;
}

.selection-images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.selection-image-item {
  width: 100%;
  aspect-ratio: 4/5;
  overflow: hidden;
  background-color: #F5F0E8;
  cursor: pointer;
}

.selection-image-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.6s ease;
}

.selection-image-item:hover img {
  transform: scale(1.03);
}

.fade-in-delay {
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) 0.7s;
}

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

/* Lightbox Styles */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(17, 17, 17, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.lightbox-img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  box-shadow: 0 4px 30px rgba(0,0,0,0.3);
  animation: fadeIn 0.3s ease;
}

.lightbox-close {
  position: absolute;
  top: 2rem;
  right: 2.5rem;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
  z-index: 10000;
}

.lightbox-close:hover {
  opacity: 1;
}

.lightbox-prev, .lightbox-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #fff;
  font-size: 4rem;
  cursor: pointer;
  opacity: 0.4;
  transition: opacity 0.2s;
  padding: 1rem;
  z-index: 10000;
}

.lightbox-prev { left: 2rem; }
.lightbox-next { right: 2rem; }

.lightbox-prev:hover, .lightbox-next:hover {
  opacity: 1;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}

@media (max-width: 1024px) {
  .selection-images-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .selection-detail-page {
    padding: 6rem 1.5rem 2rem;
  }
}

@media (max-width: 640px) {
  .selection-images-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .lightbox-prev, .lightbox-next {
    font-size: 3rem;
  }
  .lightbox-prev { left: 0.5rem; }
  .lightbox-next { right: 0.5rem; }
  .lightbox-close { top: 1rem; right: 1rem; }
}
</style>
