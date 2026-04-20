<template>
  <div class="notice-page">
    <div class="global-page-container">
      <header class="notice-header">
        <h1 class="global-eng-subtitle">Notice.</h1>
        <p class="global-kor-desc">아띠끄 디자인의 새로운 소식과 안내사항을 확인하세요.</p>
      </header>

      <!-- 탭 -->
      <div class="notice-nav">
        <ul class="tab-list">
          <li
            v-for="tab in tabs"
            :key="tab.key"
            class="tab-item"
            :class="{ 'is-active': activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            <span class="tab-text">{{ tab.label }}</span>
          </li>
        </ul>
      </div>

      <!-- 콘텐츠 영역 -->
      <div class="notice-content">
        <!-- 공지사항 리스트 -->
        <div v-if="activeTab === 'notice'" class="notice-list">
          <div v-for="item in notices" :key="item.id" class="notice-item">
            <div class="item-main">
              <span class="item-tag">NOTICE</span>
              <h3 class="item-title">{{ item.title }}</h3>
            </div>
            <span class="item-date">{{ item.date }}</span>
          </div>
        </div>

        <!-- FAQ -->
        <div v-if="activeTab === 'faq'" class="faq-list">
          <div v-for="item in faqs" :key="item.id" class="faq-item">
            <button class="faq-question" @click="item.open = !item.open">
              <span>{{ item.question }}</span>
              <svg :class="{ 'is-open': item.open }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-if="item.open" class="faq-answer">
              <p class="global-kor-desc">{{ item.answer }}</p>
            </div>
          </div>
        </div>

        <!-- 1:1 Q&A -->
        <div v-if="activeTab === 'qna'" class="qna-section">
          <p class="global-kor-desc text-center">궁금한 사항이 있으신가요? 내용을 남겨주시면 빠르게 답변드리겠습니다.</p>
          <form @submit.prevent="submitQna" class="qna-form">
            <input v-model="qnaForm.title" type="text" placeholder="제목" class="input-field" />
            <textarea v-model="qnaForm.content" placeholder="문의 내용" rows="5" class="textarea-field" />
            <button type="submit" class="btn-submit">문의 접수하기</button>
          </form>
        </div>
      </div>
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

<style scoped>
.notice-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
}

.notice-nav {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  margin-bottom: 3rem;
}

.tab-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
}

.tab-item {
  padding: 1rem 2.5rem 1rem 0;
  margin-right: 1.5rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.3s ease;
}

.tab-text {
  font-family: 'Raleway', sans-serif;
  font-size: 13px;
  letter-spacing: 0.1em;
  color: rgba(0,0,0,0.4);
}

.tab-item.is-active {
  border-bottom-color: #953735;
}

.tab-item.is-active .tab-text {
  color: #953735;
  font-weight: 600;
}

.notice-list {
  display: flex;
  flex-direction: column;
}

.notice-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.item-main {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.item-tag {
  font-size: 10px;
  font-weight: 600;
  color: #953735;
  letter-spacing: 0.1em;
}

.item-title {
  font-size: 15px;
  font-weight: 400;
  color: #312E2D;
}

.item-date {
  font-size: 13px;
  color: #888;
}

.faq-item {
  border: 1px solid rgba(0,0,0,0.08);
  margin-bottom: 1rem;
}

.faq-question {
  width: 100%;
  text-align: left;
  padding: 1.5rem;
  background: none;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-size: 15px;
  color: #312E2D;
}

.faq-question svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.faq-question svg.is-open {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  border-top: 1px solid rgba(0,0,0,0.04);
  padding-top: 1.5rem;
}

.qna-section {
  max-width: 600px;
  margin: 0 auto;
}

.qna-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 3rem;
}

.input-field, .textarea-field {
  width: 100%;
  padding: 1rem;
  background-color: #fff;
  border: 1px solid rgba(0,0,0,0.1);
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
}

.btn-submit {
  padding: 1.2rem;
  background-color: #312E2D;
  color: #fff;
  border: none;
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #953735;
}

.text-center { text-align: center; }

@media (max-width: 768px) {
  .item-main { gap: 1rem; }
  .item-title { font-size: 13px; }
  .item-date { font-size: 11px; }
}
</style>
