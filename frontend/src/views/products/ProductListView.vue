<template>
  <div class="container-page section-gap">
    <!-- 필터/정렬 -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-4">
      <div>
        <p class="text-xs uppercase tracking-[0.2em] text-accent mb-2">Shop</p>
        <h1 class="font-serif text-3xl md:text-4xl">{{ pageTitle }}</h1>
      </div>
      <div class="flex items-center gap-4">
        <select
          v-model="selectedCategory"
          class="bg-surface border-0 text-xs uppercase tracking-wider px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-accent"
        >
          <option value="">전체 카테고리</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <select
          v-model="selectedSort"
          class="bg-surface border-0 text-xs uppercase tracking-wider px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-accent"
        >
          <option value="latest">최신순</option>
          <option value="price_asc">가격 낮은순</option>
          <option value="price_desc">가격 높은순</option>
        </select>
      </div>
    </div>

    <!-- 상품 그리드 -->
    <div v-if="products.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </div>
    <div v-else class="text-center py-20 text-secondary text-sm">
      조건에 맞는 상품이 없습니다.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '@/components/domain/ProductCard.vue'
import { productService } from '@/services/product.service'
import type { Product } from '@/types/api.d'

const route = useRoute()
const products = ref<Product[]>([])
const categories = ref(productService.getCategories())
const selectedCategory = ref('')
const selectedSort = ref('latest')

const pageTitle = ref('All Products')

async function loadProducts() {
  const typeFilter = (route.query.type as string) || undefined
  if (typeFilter === 'FURNITURE') pageTitle.value = 'Furniture'
  else if (typeFilter === 'ACCESSORY') pageTitle.value = 'Accessories'
  else pageTitle.value = 'All Products'

  const res = await productService.getProducts({
    category: selectedCategory.value || undefined,
    sort: selectedSort.value,
  })
  products.value = res.data
}

onMounted(() => {
  loadProducts()
})

watch([selectedCategory, selectedSort, () => route.query.type], () => loadProducts())
</script>
