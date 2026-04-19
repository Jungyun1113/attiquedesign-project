<template>
  <div class="portfolio-page">

    <div class="portfolio-header">
      <h2 class="portfolio-title">Curated <em class="portfolio-title-accent">Spaces</em>.</h2>
      <p class="portfolio-subtitle">아띠끄 디자인의 시선으로 완성한 공간들.</p>
    </div>

    <div v-if="loading" class="portfolio-content">
      <p style="font-family: 'Pretendard', sans-serif; font-size: 13px; color: #6D6059;">불러오는 중...</p>
    </div>

    <template v-else-if="categories.length">
      <div class="portfolio-nav">
        <ul class="tab-list">
          <li
            v-for="cat in categories"
            :key="cat.id"
            class="tab-item"
            :class="{ 'is-active': activeCategoryId === cat.id }"
            @click="activeCategoryId = cat.id"
          >
            <span class="tab-text">{{ cat.name }}</span>
          </li>
        </ul>
      </div>

      <div class="portfolio-content">
        <p class="category-desc">{{ activeCategory?.description }}</p>

        <div class="projects-list">
          <section
            v-for="portfolio in activeCategory?.portfolios"
            :key="portfolio.id"
            class="project-card"
          >
            <div class="project-title-row">
              <h2 class="project-title">{{ portfolio.title }}</h2>
            </div>

            <div class="project-gallery">
              <div
                v-for="(img, idx) in portfolio.images.slice(0, 2)"
                :key="idx"
                class="gallery-item"
              >
                <img :src="img.image_url" :alt="portfolio.title + ' ' + (idx + 1)" />
              </div>
              <div v-if="portfolio.images.length === 0 && portfolio.cover_image_url" class="gallery-item">
                <img :src="portfolio.cover_image_url" :alt="portfolio.title" />
              </div>
            </div>

            <div class="project-footer">
              <router-link :to="`/portfolio/${portfolio.id}`" class="view-detail-link">
                View Project Details
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
              </router-link>
            </div>
          </section>
        </div>
      </div>
    </template>

    <div v-else class="portfolio-content">
      <p style="font-family: 'Pretendard', sans-serif; font-size: 13px; color: #6D6059;">등록된 포트폴리오가 없습니다.</p>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { portfolioService, type PortfolioCategory } from '@/services/portfolio.service'

const categories = ref<PortfolioCategory[]>([])
const loading = ref(true)
const activeCategoryId = ref('')

onMounted(async () => {
  try {
    categories.value = await portfolioService.getGroupedByCategory()
    if (categories.value.length) activeCategoryId.value = categories.value[0].id
  } catch {
    categories.value = []
  } finally {
    loading.value = false
  }
})

const activeCategory = computed(() =>
  categories.value.find(c => c.id === activeCategoryId.value) ?? categories.value[0]
)
</script>

<style scoped>
.portfolio-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
}

.portfolio-header {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2.5rem 4rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.portfolio-title {
  font-family: 'Playfair Display', 'Cormorant Garamond', serif;
  font-size: clamp(34px, 6vw, 68px);
  font-weight: 400;
  line-height: 1.25;
  color: #312E2D;
  letter-spacing: 0.01em;
  margin: 0;
  word-break: keep-all;
}

.portfolio-title-accent {
  font-style: italic;
  font-family: 'Playfair Display', serif;
  color: #953735;
  font-weight: 500;
  letter-spacing: 0.04em;
}

.portfolio-subtitle {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  word-break: keep-all;
}

.portfolio-nav {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2.5rem 4rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.tab-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  gap: 0;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem 0.75rem 0;
  margin-right: 2rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.3s ease;
}

.tab-text {
  font-family: 'Raleway', sans-serif;
  font-size: 12px;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: rgba(49, 46, 45, 0.4);
  transition: color 0.3s ease;
}

.tab-item:hover .tab-text {
  color: #312E2D;
}

.tab-item.is-active .tab-text {
  color: #953735;
  font-weight: 600;
}

.tab-item.is-active {
  border-bottom-color: #953735;
}

.portfolio-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 4rem 8rem;
}

.category-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.7;
  color: #6D6059;
  word-break: keep-all;
  white-space: pre-line;
  margin: 0 0 3rem 0;
  max-width: 600px;
}

.projects-list {
  display: flex;
  flex-direction: column;
  gap: 8rem;
}

.project-card {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.project-title-row {
  display: flex;
  align-items: baseline;
}

.project-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 400;
  color: #312E2D;
  margin: 0;
}

.project-gallery {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.gallery-item {
  aspect-ratio: 4/3;
  background-color: #eee;
  overflow: hidden;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.8s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.project-footer {
  display: flex;
}

.view-detail-link {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  font-family: 'Raleway', sans-serif;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.25em;
  color: #312E2D;
  text-decoration: none;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.view-detail-link:hover {
  color: #953735;
  border-bottom-color: #953735;
}

@media (max-width: 768px) {
  .portfolio-header {
    padding: 1.5rem 1.5rem 0;
  }

  .portfolio-nav {
    padding: 2rem 1.5rem 0;
    overflow-x: auto;
  }

  .tab-list {
    flex-wrap: nowrap;
    min-width: max-content;
  }

  .tab-item {
    margin-right: 1.2rem;
    padding-right: 0;
    white-space: nowrap;
  }

  .portfolio-content {
    padding: 1.5rem 1.5rem 6rem;
  }

  .projects-list {
    gap: 4rem;
  }

  .project-title {
    font-size: 18px;
  }
}
</style>
