<template>
  <div v-if="product" class="container-page section-gap">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16">
      <!-- 이미지 -->
      <div class="aspect-[3/4] bg-surface overflow-hidden">
        <img :src="product.thumbnail_url" :alt="product.name" class="w-full h-full object-cover" />
      </div>

      <!-- 정보 -->
      <div class="flex flex-col justify-center">
        <p class="text-[10px] uppercase tracking-[0.2em] text-accent mb-3">{{ product.category_name }}</p>
        <h1 class="font-serif text-3xl md:text-4xl mb-4">{{ product.name }}</h1>
        <p class="text-sm leading-relaxed text-secondary mb-6">{{ product.description }}</p>

        <!-- 가격 / 문의 -->
        <div class="mb-8">
          <template v-if="product.price !== null">
            <p class="text-2xl font-medium mb-1">{{ product.price.toLocaleString() }}원</p>
          </template>
          <template v-else>
            <p class="text-lg text-accent">가격 문의 상품</p>
          </template>
        </div>

        <!-- 뱃지 -->
        <div class="flex gap-2 mb-8">
          <span v-if="product.stock_quantity <= 1 && product.status !== 'SOLDOUT'" class="px-3 py-1 bg-accent/10 text-accent text-xs">
            단 {{ product.stock_quantity }}개 남았습니다
          </span>
          <span class="px-3 py-1 bg-surface text-secondary text-xs">📍 한남 쇼룸 전시 중</span>
        </div>

        <!-- 액션 버튼 -->
        <div class="flex flex-col sm:flex-row gap-3">
          <template v-if="product.status === 'SOLDOUT'">
            <button class="btn-outline flex-1" @click="showWaitlistToast">재고 입고 알림 신청</button>
          </template>
          <template v-else-if="product.price !== null">
            <button class="btn-primary flex-1" @click="addToCart">장바구니</button>
            <button class="btn-outline flex-1">바로 구매</button>
          </template>
          <template v-else>
            <router-link :to="`/reservation?sku=${product.sku}`" class="btn-primary flex-1 text-center">가격 문의하기</router-link>
          </template>
        </div>

        <!-- 디자이너 스토리 -->
        <div v-if="product.designer_story" class="mt-12 pt-8 border-t border-surface">
          <p class="text-xs uppercase tracking-widest text-accent mb-3">Designer's Story</p>
          <p class="text-sm leading-relaxed text-secondary">{{ product.designer_story }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { productService } from '@/services/product.service'
import { useCartStore } from '@/store/cart'
import { useToast } from '@/composables/useToast'
import type { Product } from '@/types/api.d'

const route = useRoute()
const product = ref<Product | null>(null)
const cartStore = useCartStore()
const { showSuccess } = useToast()

onMounted(async () => {
  product.value = await productService.getProductById(route.params.id as string)
})

function addToCart() {
  if (product.value) {
    cartStore.addItem(product.value)
    showSuccess('장바구니에 추가되었습니다.')
  }
}

function showWaitlistToast() {
  showSuccess('재입고 알림 신청이 접수되었습니다.')
}
</script>
