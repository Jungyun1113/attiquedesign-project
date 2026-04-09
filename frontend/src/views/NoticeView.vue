<template>
  <div class="container-page section-gap max-w-3xl">
    <p class="text-xs uppercase tracking-[0.2em] text-accent mb-2">Notice</p>
    <h1 class="font-serif text-3xl md:text-4xl mb-8">공지사항</h1>

    <!-- 탭 -->
    <div class="flex border-b border-surface mb-8">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="[
          'px-5 py-3 text-xs uppercase tracking-wider transition-colors border-b-2 -mb-px',
          activeTab === tab.key
            ? 'border-primary text-primary'
            : 'border-transparent text-secondary hover:text-primary',
        ]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 공지사항 -->
    <div v-if="activeTab === 'notice'" class="divide-y divide-surface">
      <div v-for="item in notices" :key="item.id" class="py-5 flex justify-between items-start cursor-pointer hover:bg-surface/50 transition-colors px-2 -mx-2">
        <div>
          <span class="text-[10px] uppercase tracking-wider text-accent mr-2">공지</span>
          <h3 class="font-sans text-sm font-medium mt-1">{{ item.title }}</h3>
        </div>
        <span class="text-xs text-secondary whitespace-nowrap ml-4">{{ item.date }}</span>
      </div>
    </div>

    <!-- FAQ -->
    <div v-if="activeTab === 'faq'" class="space-y-4">
      <div v-for="item in faqs" :key="item.id" class="border border-surface">
        <button
          class="w-full flex justify-between items-center px-5 py-4 text-left text-sm font-medium hover:bg-surface/50 transition-colors"
          @click="item.open = !item.open"
        >
          <span>{{ item.question }}</span>
          <svg :class="['w-4 h-4 transition-transform text-secondary', item.open ? 'rotate-180' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-if="item.open" class="px-5 pb-4 text-sm text-secondary leading-relaxed">
          {{ item.answer }}
        </div>
      </div>
    </div>

    <!-- 1:1 Q&A -->
    <div v-if="activeTab === 'qna'" class="text-center py-16">
      <p class="text-sm text-secondary mb-6">궁금한 사항이 있으신가요?</p>
      <form @submit.prevent="submitQna" class="max-w-md mx-auto space-y-4">
        <input v-model="qnaForm.title" type="text" placeholder="제목을 입력해주세요" class="w-full px-4 py-3 bg-surface text-sm focus:outline-none focus:ring-1 focus:ring-accent" />
        <textarea v-model="qnaForm.content" placeholder="문의 내용을 입력해주세요" rows="5" class="w-full px-4 py-3 bg-surface text-sm focus:outline-none focus:ring-1 focus:ring-accent resize-none" />
        <button type="submit" class="btn-primary w-full">문의 접수하기</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useToast } from '@/composables/useToast'

const { showSuccess } = useToast()

const tabs = [
  { key: 'notice', label: '공지사항' },
  { key: 'faq', label: 'FAQ' },
  { key: 'qna', label: '1:1 Q&A' },
]
const activeTab = ref('notice')

const notices = [
  { id: 1, title: '한남 쇼룸 리뉴얼 오픈 안내', date: '2026.03.15' },
  { id: 2, title: '봄 시즌 New Arrivals 안내', date: '2026.03.01' },
  { id: 3, title: '설 연휴 배송/쇼룸 운영 안내', date: '2026.01.20' },
]

const faqs = reactive([
  { id: 1, question: '배송은 얼마나 걸리나요?', answer: '소품류는 결제 후 3~5영업일 내 발송됩니다. 가구류는 주문 제작 특성상 4~8주 소요될 수 있습니다.', open: false },
  { id: 2, question: '쇼룸 방문은 예약 필수인가요?', answer: '월~토 정규 운영시간에는 예약 없이 워크인 방문도 가능합니다. 일요일은 사전 예약제로 운영됩니다.', open: false },
  { id: 3, question: '주문 취소 및 반품은 어떻게 하나요?', answer: '배송 전 주문 취소는 무료이며, 수령 후 7일 이내 반품 가능합니다. 고객 변심 반품 시 왕복 배송비가 발생합니다.', open: false },
  { id: 4, question: '인테리어 시공 범위는 어디까지인가요?', answer: '설계, 철거, 바닥/벽/천장/전기/설비 시공, 가구/소품 배치까지 원스톱 서비스를 제공합니다.', open: false },
])

const qnaForm = reactive({ title: '', content: '' })

function submitQna() {
  if (!qnaForm.title || !qnaForm.content) return
  showSuccess('문의가 접수되었습니다. 빠르게 답변드리겠습니다.')
  qnaForm.title = ''
  qnaForm.content = ''
}
</script>
