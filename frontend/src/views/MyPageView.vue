<template>
  <div class="container-page section-gap max-w-3xl">
    <h1 class="font-serif text-3xl md:text-4xl mb-10">마이페이지</h1>

    <!-- 사용자 정보 -->
    <div class="bg-surface p-6 mb-10">
      <p class="text-sm font-medium">{{ user?.name }}</p>
      <p class="text-xs text-secondary mt-1">{{ user?.email }}</p>
      <button class="text-xs text-accent mt-3 hover:underline" @click="logout">로그아웃</button>
    </div>

    <!-- 주문 내역 -->
    <section class="mb-10">
      <h2 class="font-serif text-xl mb-4">주문 내역</h2>
      <div v-if="loadingOrders" class="text-sm text-secondary">불러오는 중...</div>
      <div v-else-if="orders.length" class="divide-y divide-surface">
        <div v-for="order in orders" :key="order.id" class="py-4">
          <div class="flex justify-between items-start mb-2">
            <p class="text-sm font-medium">주문 #{{ order.id.slice(-6) }}</p>
            <span :class="statusClass(order.status)" class="text-[10px] uppercase tracking-wider px-2 py-0.5">{{ statusLabel(order.status) }}</span>
          </div>
          <div v-for="item in order.items" :key="item.id" class="text-xs text-secondary">
            {{ item.product_name }} × {{ item.quantity }}
          </div>
          <p class="text-sm mt-1">{{ order.total_amount.toLocaleString() }}원</p>
        </div>
      </div>
      <p v-else class="text-sm text-secondary">주문 내역이 없습니다.</p>
    </section>

    <!-- 예약 현황 -->
    <section class="mb-10">
      <h2 class="font-serif text-xl mb-4">상담 예약 현황</h2>
      <p class="text-sm text-secondary">예약 내역이 없습니다.</p>
    </section>

    <!-- 위시리스트 -->
    <section class="mb-10">
      <h2 class="font-serif text-xl mb-4">위시리스트</h2>
      <p class="text-sm text-secondary">위시리스트에 담긴 상품이 없습니다.</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { orderService } from '@/services/order.service'
import type { Order } from '@/types/api.d'

const authStore = useAuthStore()
const router = useRouter()
const { user } = storeToRefs(authStore)

const orders = ref<Order[]>([])
const loadingOrders = ref(true)

onMounted(async () => {
  try {
    const res = await orderService.getMyOrders()
    orders.value = res.data
  } catch {
    orders.value = []
  } finally {
    loadingOrders.value = false
  }
})

function logout() {
  authStore.logout()
  router.push('/')
}

function statusClass(s: string) {
  const map: Record<string, string> = {
    DELIVERED: 'bg-success/10 text-success',
    PAID: 'bg-accent/10 text-accent',
    CANCELLED: 'bg-error/10 text-error',
  }
  return map[s] || 'bg-surface text-secondary'
}
function statusLabel(s: string) {
  const map: Record<string, string> = { PENDING: '결제 대기', PAID: '결제 완료', SHIPPED: '배송 중', DELIVERED: '수령 완료', CANCELLED: '취소' }
  return map[s] || s
}
</script>
