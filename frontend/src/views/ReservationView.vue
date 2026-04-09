<template>
  <div class="container-page section-gap max-w-2xl">
    <div class="text-center mb-12">
      <p class="text-xs uppercase tracking-[0.2em] text-accent mb-2">Reservation</p>
      <h1 class="font-serif text-3xl md:text-4xl">1:1 프라이빗 방문 상담 예약</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-1">
      <!-- Step 1: 상담 분야 선택 -->
      <FormItem label="상담 분야" :required="true">
        <div class="flex flex-col sm:flex-row gap-3">
          <label v-for="opt in typeOptions" :key="opt.value" class="flex items-center gap-2 cursor-pointer">
            <input type="radio" :value="opt.value" v-model="form.type" class="accent-accent" />
            <span class="text-sm">{{ opt.label }}</span>
          </label>
        </div>
      </FormItem>

      <!-- Step 2: 공통 필수 -->
      <FormItem label="방문 희망 일시" :required="true">
        <BaseInput v-model="form.expected_date" type="datetime-local" />
      </FormItem>
      <FormItem label="고객 이름" :required="true">
        <BaseInput v-model="form.name" placeholder="이름을 입력해주세요" />
      </FormItem>
      <FormItem label="연락처" :required="true">
        <BaseInput v-model="form.phone" placeholder="010-0000-0000" />
      </FormItem>
      <FormItem label="이메일">
        <BaseInput v-model="form.email" type="email" placeholder="email@example.com" />
      </FormItem>

      <!-- 공통 선택 -->
      <FormItem label="공간 형태 및 평형대">
        <BaseInput v-model="form.space_type" placeholder="예: APT 42평" />
      </FormItem>

      <!-- 조건부: 인테리어/토탈 -->
      <template v-if="form.type === 'INTERIOR' || form.type === 'TOTAL'">
        <FormItem label="현장 주소">
          <BaseInput v-model="form.address" placeholder="시공 현장 주소" />
        </FormItem>
        <FormItem label="공사 희망일">
          <BaseInput v-model="form.construction_date" type="date" />
        </FormItem>
        <FormItem label="전체 예산">
          <BaseInput v-model="form.budget" placeholder="예: 1억 ~ 1.5억" />
        </FormItem>
        <FormItem label="도면/현장 사진 업로드">
          <input type="file" multiple accept="image/*,.pdf" class="w-full text-sm text-secondary file:mr-4 file:py-2 file:px-4 file:border file:border-surface file:text-xs file:bg-surface file:text-primary hover:file:bg-accent/10 file:transition-colors file:cursor-pointer" />
          <p class="mt-1 text-[10px] text-secondary">이미지 또는 PDF 파일 (데모 단계에서는 업로드 기능이 제한됩니다)</p>
        </FormItem>
      </template>

      <!-- 조건부: 가구 -->
      <template v-if="form.type === 'FURNITURE' || form.type === 'TOTAL'">
        <FormItem label="필요 가구 품목">
          <BaseInput v-model="form.furniture_items" placeholder="예: 소파, 다이닝 테이블" />
        </FormItem>
        <FormItem label="선호 브랜드/스타일">
          <BaseInput v-model="form.preferred_style" placeholder="예: 미니멀, 모던 클래식" />
        </FormItem>
      </template>

      <!-- SKU 숨김 필드 (상품 상세에서 진입 시 자동 기입) -->
      <div v-if="form.linked_sku" class="px-4 py-3 bg-accent/5 text-xs text-accent">
        연관 상품: {{ form.linked_sku }}
      </div>

      <!-- 모바일 Sticky Bottom / PC 일반 -->
      <div class="pt-6 md:static fixed bottom-0 left-0 right-0 md:p-0 p-4 bg-white md:bg-transparent border-t md:border-0 border-surface z-40">
        <button type="submit" class="btn-primary w-full" :disabled="submitting">
          {{ submitting ? '접수 중...' : '예약 신청하기' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import FormItem from '@/components/common/FormItem.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import { reservationService } from '@/services/reservation.service'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const { showSuccess, showError } = useToast()
const submitting = ref(false)

const typeOptions = [
  { label: '인테리어 설계 및 시공', value: 'INTERIOR' },
  { label: '가구 및 홈스타일링', value: 'FURNITURE' },
  { label: '토탈 솔루션', value: 'TOTAL' },
]

const form = reactive({
  type: 'INTERIOR' as 'INTERIOR' | 'FURNITURE' | 'TOTAL',
  expected_date: '',
  name: '',
  phone: '',
  email: '',
  space_type: '',
  address: '',
  construction_date: '',
  budget: '',
  furniture_items: '',
  preferred_style: '',
  linked_sku: '',
})

// 상품 상세에서 ?sku=XXX로 진입 시 자동 기입
onMounted(() => {
  const sku = route.query.sku as string
  if (sku) {
    form.linked_sku = sku
    form.type = 'FURNITURE'
  }
})

async function handleSubmit() {
  if (!form.expected_date || !form.name || !form.phone) {
    showError('필수 항목을 모두 입력해주세요.')
    return
  }
  submitting.value = true
  try {
    // dynamic_data 패킹 (Backend API 규격 대응)
    const dynamicData: Record<string, unknown> = {
      space_type: form.space_type,
    }
    if (form.type === 'INTERIOR' || form.type === 'TOTAL') {
      dynamicData.address = form.address
      dynamicData.construction_date = form.construction_date
      dynamicData.budget = form.budget
    }
    if (form.type === 'FURNITURE' || form.type === 'TOTAL') {
      dynamicData.furniture_items = form.furniture_items
      dynamicData.preferred_style = form.preferred_style
    }
    await reservationService.createReservation({
      type: form.type,
      expected_date: form.expected_date,
      guest_info: { name: form.name, phone: form.phone, email: form.email },
      dynamic_data: dynamicData,
    })
    showSuccess('예약이 접수되었습니다. 곧 연락드리겠습니다.')
  } catch {
    showError('예약 접수에 실패했습니다.')
  } finally {
    submitting.value = false
  }
}
</script>
