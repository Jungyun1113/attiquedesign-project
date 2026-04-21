<template>
  <div class="container-page section-gap">
    <h1 class="font-serif text-2xl mb-6">관리자 대시보드</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
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

    <!-- 비밀번호 변경 -->
    <div class="bg-white p-6 shadow-sm max-w-md">
      <h2 class="text-sm font-semibold uppercase tracking-wider text-secondary mb-4">비밀번호 변경</h2>
      <div class="flex flex-col gap-3">
        <input
          v-model="currentPw"
          type="password"
          placeholder="현재 비밀번호"
          class="border border-border px-3 py-2 text-sm outline-none focus:border-primary"
        />
        <input
          v-model="newPw"
          type="password"
          placeholder="새 비밀번호 (8자 이상)"
          class="border border-border px-3 py-2 text-sm outline-none focus:border-primary"
        />
        <input
          v-model="confirmPw"
          type="password"
          placeholder="새 비밀번호 확인"
          class="border border-border px-3 py-2 text-sm outline-none focus:border-primary"
        />
        <p v-if="pwError" class="text-xs text-red-500">{{ pwError }}</p>
        <p v-if="pwSuccess" class="text-xs text-green-600">{{ pwSuccess }}</p>
        <button
          class="bg-primary text-white text-xs uppercase tracking-wider py-2 px-4 hover:bg-brand transition-colors disabled:opacity-50"
          :disabled="pwLoading"
          @click="changePassword"
        >
          {{ pwLoading ? '변경 중...' : '변경하기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const loading = ref(true)
const stats = ref({ products: 0, orders: 0, reservations: 0 })

const currentPw = ref('')
const newPw = ref('')
const confirmPw = ref('')
const pwLoading = ref(false)
const pwError = ref('')
const pwSuccess = ref('')

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

async function changePassword() {
  pwError.value = ''
  pwSuccess.value = ''

  if (!currentPw.value || !newPw.value || !confirmPw.value) {
    pwError.value = '모든 항목을 입력해주세요.'; return
  }
  if (newPw.value.length < 8) {
    pwError.value = '새 비밀번호는 8자 이상이어야 합니다.'; return
  }
  if (newPw.value !== confirmPw.value) {
    pwError.value = '새 비밀번호가 일치하지 않습니다.'; return
  }

  pwLoading.value = true
  try {
    await api.patch('/auth/password', {
      current_password: currentPw.value,
      new_password: newPw.value,
    })
    pwSuccess.value = '비밀번호가 변경되었습니다.'
    currentPw.value = ''
    newPw.value = ''
    confirmPw.value = ''
  } catch (e: any) {
    pwError.value = e?.response?.data?.message ?? '변경 실패. 현재 비밀번호를 확인해주세요.'
  } finally {
    pwLoading.value = false
  }
}
</script>
