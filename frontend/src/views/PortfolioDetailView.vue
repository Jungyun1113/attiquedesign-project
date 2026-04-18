<template>
  <div class="detail-page">
    <div class="detail-container" :class="{ 'is-visible': isVisible }">

      <router-link to="/portfolio" class="back-link">
        <span class="back-arrow">←</span>
        <span class="back-label">Portfolio</span>
      </router-link>

      <div v-if="loading" class="not-found">
        <p>불러오는 중...</p>
      </div>

      <div v-else-if="!portfolio" class="not-found">
        <p>프로젝트를 찾을 수 없습니다.</p>
        <router-link to="/portfolio" class="back-link">← 포트폴리오로 돌아가기</router-link>
      </div>

      <template v-else>
        <header class="project-header">
          <h1 class="project-title">{{ portfolio.title }}</h1>
          <p v-if="portfolio.description" class="project-desc">{{ portfolio.description }}</p>
        </header>

        <section class="gallery-section">
          <div v-if="portfolio.cover_image_url && portfolio.images.length === 0" class="gallery-hero-wrap">
            <img :src="portfolio.cover_image_url" :alt="portfolio.title" class="gallery-hero-image" loading="lazy" />
          </div>

          <div v-if="portfolio.images.length > 0" class="gallery-hero-wrap">
            <img :src="portfolio.images[0].image_url" :alt="portfolio.title + ' — 1'" class="gallery-hero-image" loading="lazy" />
          </div>

          <div v-if="portfolio.images.length > 1" class="gallery-grid">
            <div
              v-for="(img, idx) in portfolio.images.slice(1)"
              :key="img.id"
              class="gallery-grid-item"
            >
              <img :src="img.image_url" :alt="portfolio.title + ' — ' + (idx + 2)" class="gallery-grid-image" loading="lazy" />
            </div>
          </div>
        </section>

        <footer class="detail-cta">
          <div class="cta-divider"></div>
          <p class="cta-eyebrow">이 공간이 마음에 드신다면.</p>
          <router-link to="/contact" class="cta-button">방문 상담 예약</router-link>
        </footer>
      </template>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { portfolioService, type Portfolio } from '@/services/portfolio.service'

const route = useRoute()
const isVisible = ref(false)
const loading = ref(true)
const portfolio = ref<Portfolio | null>(null)

onMounted(async () => {
  try {
    portfolio.value = await portfolioService.getPortfolioById(route.params.id as string)
  } catch {
    portfolio.value = null
  } finally {
    loading.value = false
  }
  window.scrollTo(0, 0)
  setTimeout(() => { isVisible.value = true }, 80)
})
</script>

<style scoped>
.detail-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
}

.detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem 4rem 8rem;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.detail-container.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Raleway', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(49, 46, 45, 0.5);
  text-decoration: none;
  margin-bottom: 1.5rem;
  transition: color 0.25s ease;
}

.back-link:hover {
  color: #953735;
}

.back-arrow {
  font-size: 14px;
  line-height: 1;
}

.project-header {
  margin-bottom: 1.5rem;
}

.project-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(24px, 3.5vw, 44px);
  font-weight: 400;
  line-height: 1.2;
  color: #312E2D;
  margin: 0 0 0.6rem;
  letter-spacing: 0.01em;
}

.project-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  max-width: 560px;
  word-break: keep-all;
}

.gallery-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 4rem;
}

.gallery-hero-wrap {
  width: 100%;
  aspect-ratio: 16/9;
  background-color: #ECEAE5;
  overflow: hidden;
}

.gallery-hero-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
  transition: transform 0.8s ease;
}

.gallery-hero-wrap:hover .gallery-hero-image {
  transform: scale(1.03);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.gallery-grid-item {
  aspect-ratio: 4/3;
  background-color: #ECEAE5;
  overflow: hidden;
}

.gallery-grid-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: center;
  transition: transform 0.8s ease;
}

.gallery-grid-item:hover .gallery-grid-image {
  transform: scale(1.03);
}

.detail-cta {
  text-align: center;
  padding-top: 3rem;
}

.cta-divider {
  width: 100%;
  height: 1px;
  background: rgba(49, 46, 45, 0.1);
  margin-bottom: 3rem;
}

.cta-eyebrow {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 0.08em;
  color: rgba(49, 46, 45, 0.55);
  margin: 0 0 2rem;
  word-break: keep-all;
}

.cta-button {
  display: inline-block;
  font-family: 'Raleway', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  text-decoration: none;
  color: #F9F8F6;
  background-color: #953735;
  padding: 16px 40px;
  transition: background-color 0.3s ease, letter-spacing 0.3s ease;
}

.cta-button:hover {
  background-color: #953735;
  letter-spacing: 0.34em;
}

.not-found {
  text-align: center;
  padding: 6rem 0;
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  color: #6D6059;
}

@media (max-width: 768px) {
  .detail-container {
    padding: 1rem 1.5rem 6rem;
  }

  .back-link {
    margin-bottom: 2.5rem;
  }

  .project-title {
    font-size: clamp(24px, 7vw, 36px);
  }

  .project-desc {
    font-size: 15px;
  }

  .cta-button {
    padding: 14px 32px;
    width: 100%;
    text-align: center;
  }
}
</style>
