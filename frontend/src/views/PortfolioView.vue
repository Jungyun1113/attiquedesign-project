<template>
  <div class="container-page section-gap">
    <div class="text-center mb-12">
      <p class="text-xs uppercase tracking-[0.2em] text-accent mb-2">Portfolio</p>
      <h1 class="font-serif text-3xl md:text-4xl">공간의 완성</h1>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="item in portfolio" :key="item.id" class="group relative aspect-[4/3] overflow-hidden cursor-pointer">
        <img :src="item.image" :alt="item.title" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
        <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors duration-500" />
        <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
          <div class="flex gap-2 mb-2">
            <span v-for="tag in item.tags" :key="tag" class="text-[9px] uppercase tracking-wider bg-white/20 px-2 py-0.5">{{ tag }}</span>
          </div>
          <h3 class="font-serif text-lg">{{ item.title }}</h3>
          <p class="text-xs opacity-70">{{ item.subtitle }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MOCK_PORTFOLIO } from '@/mocks/data'
const portfolio = MOCK_PORTFOLIO
</script>
