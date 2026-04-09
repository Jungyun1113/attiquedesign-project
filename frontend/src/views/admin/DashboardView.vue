<template>
  <div class="container-page section-gap">
    <h1 class="font-serif text-2xl mb-6">관리자 대시보드</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">총 상품</p>
        <p class="text-3xl font-medium">{{ stats.products }}</p>
      </div>
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">금일 주문</p>
        <p class="text-3xl font-medium">{{ stats.orders }}</p>
      </div>
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">신규 예약</p>
        <p class="text-3xl font-medium">{{ stats.reservations }}</p>
      </div>
    </div>
    <p class="text-sm text-secondary mt-8">관리자 기능은 추후 업데이트됩니다.</p>
  </div>
</template>

<script setup lang="ts">
const stats = { products: 8, orders: 3, reservations: 1 }
</script>
