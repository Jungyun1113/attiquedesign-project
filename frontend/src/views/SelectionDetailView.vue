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

        <div v-if="selection.products.length" class="products-grid">
          <div
            v-for="product in selection.products"
            :key="product.id"
            class="product-item"
            @click="goToProduct(product.product_id)"
          >
            <div class="product-img-wrap">
              <img :src="product.thumbnail_url ?? ''" :alt="product.name ?? ''" loading="lazy" />
            </div>
            <div class="product-info">
              <p class="product-name">{{ product.name }}</p>
              <p v-if="product.price" class="product-price">{{ product.price.toLocaleString() }}원</p>
              <p v-else class="product-price-inquiry">가격 문의</p>
            </div>
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

function goToProduct(productId: string) {
  router.push(`/products/${productId}`)
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

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem 1.5rem;
  margin-bottom: 3rem;
}

.product-item {
  cursor: pointer;
}

.product-img-wrap {
  width: 100%;
  aspect-ratio: 4/5;
  background-color: #E8E2D7;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.product-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.product-item:hover .product-img-wrap img {
  transform: scale(1.04);
}

.product-info {
  text-align: center;
}

.product-name {
  font-family: 'Raleway', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #2C2C2A;
  margin: 0 0 0.3rem;
}

.product-price {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  color: #444;
}

.product-price-inquiry {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  color: #953735;
  letter-spacing: 0.05em;
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

@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .selection-detail-page {
    padding: 6rem 1.5rem 2rem;
  }
}

@media (max-width: 640px) {
  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>
