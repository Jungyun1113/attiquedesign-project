<template>
  <div class="container-page section-gap">
    <h1 class="font-serif text-2xl mb-6">관리자 대시보드</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">총 상품</p>
        <p class="text-3xl font-medium">{{ loading ? '—' : stats.products }}</p>
      </div>
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">전체 주문</p>
        <p class="text-3xl font-medium">{{ loading ? '—' : stats.orders }}</p>
      </div>
      <div class="bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-wider text-secondary mb-1">전체 예약</p>
        <p class="text-3xl font-medium">{{ loading ? '—' : stats.reservations }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const loading = ref(true)
const stats = ref({ products: 0, orders: 0, reservations: 0 })

onMounted(async () => {
  try {
    const [pRes, oRes, rRes] = await Promise.all([
      api.get('/products', { params: { limit: 1 } }),
      api.get('/orders', { params: { limit: 1 } }),
      api.get('/reservations', { params: { limit: 1 } }),
    ])
    stats.value = {
      products: pRes.data.meta?.total_count ?? 0,
      orders: oRes.data.meta?.total_count ?? 0,
      reservations: rRes.data.meta?.total_count ?? 0,
    }
  } catch {
    // stats remain 0
  } finally {
    loading.value = false
  }
})
</script>
