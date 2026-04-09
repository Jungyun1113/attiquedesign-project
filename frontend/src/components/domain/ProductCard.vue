<template>
  <router-link :to="`/products/${product.id}`" class="group block">
    <!-- 이미지 -->
    <div
      class="relative aspect-[3/4] overflow-hidden bg-surface mb-4"
      @mouseenter="hovered = true"
      @mouseleave="hovered = false"
    >
      <img
        :src="displayImage"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
      />
      <!-- 뱃지: 얇은 실선으로 섬세하게 -->
      <div class="absolute top-3 left-3 flex flex-col gap-1.5">
        <span
          v-if="product.status === 'SOLDOUT'"
          class="px-2 py-0.5 border border-white/70 text-white text-[8px] uppercase tracking-[0.2em] backdrop-blur-sm"
        >
          Sold Out
        </span>
        <span
          v-else-if="product.stock_quantity <= 1"
          class="px-2 py-0.5 border border-brand/80 text-brand bg-white/80 text-[8px] uppercase tracking-[0.2em] backdrop-blur-sm"
        >
          단 {{ product.stock_quantity }}개
        </span>
      </div>
    </div>
    <!-- 정보 -->
    <div>
      <p v-if="product.category_name" class="text-[10px] uppercase tracking-widest text-secondary mb-1">
        {{ product.category_name }}
      </p>
      <h3 class="font-sans text-sm font-medium text-primary mb-1 group-hover:text-brand transition-colors duration-500">
        {{ product.name }}
      </h3>
      <p class="text-sm text-secondary">
        <template v-if="product.price !== null">
          {{ product.price.toLocaleString() }}원
        </template>
        <template v-else>
          <span class="text-accent">가격 문의</span>
        </template>
      </p>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Product } from '@/types/api.d'

const props = defineProps<{
  product: Product
}>()

const hovered = ref(false)

const displayImage = computed(() =>
  hovered.value && props.product.hover_image_url
    ? props.product.hover_image_url
    : props.product.thumbnail_url,
)
</script>
