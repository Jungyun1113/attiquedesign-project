<template>
  <div class="container-page section-gap max-w-3xl">
    <h1 class="font-serif text-3xl md:text-4xl mb-10">장바구니</h1>

    <div v-if="items.length">
      <div class="divide-y divide-surface">
        <div v-for="item in items" :key="item.product.id" class="flex gap-4 md:gap-6 py-6">
          <div class="w-24 h-32 bg-surface flex-shrink-0 overflow-hidden">
            <img :src="item.product.thumbnail_url" :alt="item.product.name" class="w-full h-full object-cover" />
          </div>
          <div class="flex-1">
            <p class="text-[10px] uppercase tracking-widest text-accent mb-1">{{ item.product.category_name }}</p>
            <h3 class="text-sm font-medium mb-1">{{ item.product.name }}</h3>
            <p class="text-sm text-secondary mb-3">{{ (item.product.price ?? 0).toLocaleString() }}원</p>
            <div class="flex items-center gap-3">
              <button class="w-7 h-7 border border-surface text-xs hover:border-accent transition-colors" @click="cartStore.updateQuantity(item.product.id, item.quantity - 1)">−</button>
              <span class="text-sm w-6 text-center">{{ item.quantity }}</span>
              <button class="w-7 h-7 border border-surface text-xs hover:border-accent transition-colors" @click="cartStore.updateQuantity(item.product.id, item.quantity + 1)">+</button>
              <button class="ml-auto text-xs text-secondary hover:text-error transition-colors" @click="cartStore.removeItem(item.product.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Total -->
      <div class="mt-8 pt-6 border-t border-primary">
        <div class="flex justify-between items-center mb-6">
          <p class="text-sm uppercase tracking-wider">합계</p>
          <p class="text-xl font-medium">{{ totalPrice.toLocaleString() }}원</p>
        </div>
        <button class="btn-primary w-full">결제하기</button>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <p class="text-sm text-secondary mb-6">장바구니가 비어있습니다.</p>
      <router-link to="/products" class="btn-outline">상품 둘러보기</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '@/store/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const { items, totalPrice } = storeToRefs(cartStore)
</script>
