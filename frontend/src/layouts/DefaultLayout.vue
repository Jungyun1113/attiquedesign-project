<template>
  <div class="min-h-screen flex flex-col">
    <!-- 서비스 페이지 헤더 (간소화 — 로고 + 아이콘만) -->
    <header
      :class="[
        'fixed top-0 left-0 right-0 z-50 transition-all duration-500 bg-background border-b border-border/60',
        scrolled ? 'shadow-sm shadow-black/5' : ''
      ]"
    >
      <div class="container-page flex items-center justify-between h-14 md:h-16">
        <!-- 로고 — 클릭 시 랜딩 홈으로 이동 -->
        <router-link to="/" class="flex items-center">
          <img src="/logo.png" alt="ATTIQUE DESIGN" class="h-7 md:h-9 object-contain" />
        </router-link>

        <!-- 아이콘 영역 (장바구니 + 마이페이지/로그인) -->
        <div class="flex items-center gap-5">
          <!-- 뒤로가기: 서비스 페이지에서 유용 -->
          <button
            class="hidden md:flex items-center gap-1.5 text-[9px] uppercase tracking-[0.2em] text-secondary hover:text-primary transition-colors"
            @click="$router.back()"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>

          <!-- 장바구니 -->
          <router-link to="/cart" class="relative text-primary/70 hover:text-primary transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span
              v-if="cartCount > 0"
              class="absolute -top-1.5 -right-1.5 bg-brand text-white text-[9px] w-4 h-4 rounded-full flex items-center justify-center font-medium"
            >
              {{ cartCount }}
            </span>
          </router-link>

          <!-- 마이페이지 / 로그인 -->
          <router-link
            :to="isLoggedIn ? '/mypage' : '/login'"
            class="text-primary/70 hover:text-primary transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 pt-14 md:pt-16">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer-global">
      <div class="container-page">
        <div class="footer-top">
          <div class="footer-brand">
            <h4 class="footer-logo">ATTIQUE DESIGN</h4>
            <p class="footer-tagline">When Preference Becomes Lifestyle.</p>
          </div>
          
          <div class="footer-nav">
            <div class="footer-nav-col">
              <h5>Contact</h5>
              <p>Showroom. 서울시 용산구 한남대로 21길 27<br>T. 02-3443-8170<br>E. info@attiquedesign.com</p>
            </div>
            <div class="footer-nav-col">
              <h5>Social</h5>
              <div class="social-links">
                <a href="https://instagram.com/attiquedesign" target="_blank">Instagram</a>
                <a href="https://blog.naver.com/attiquedesign" target="_blank">Blog</a>
                <a href="https://pf.kakao.com/_attiquedesign" target="_blank">KakaoTalk</a>
              </div>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <div class="business-info-grid">
            <p>(주) 아띠끄디자인 | 대표이사 홍민영 | 사업자등록번호 123-45-67890 | 통신판매업신고번호 제2026-서울용산-0000호</p>
            <p>주소: 서울시 용산구 한남대로 21길 27 | 개인정보관리책임자: 홍민영</p>
          </div>
          <p class="copyright">© 2026 ATTIQUE DESIGN. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.footer-global {
  background-color: #6D2122; /* 로고 버건디 색상 적용 */
  color: #F1EFE7; /* 아이보리/크림 색상 텍스트 */
  padding: 6rem 0 4rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5rem;
  border-bottom: 1px solid rgba(241, 239, 231, 0.1);
  padding-bottom: 3rem;
}

.footer-logo {
  font-size: 20px;
  letter-spacing: 0.25em;
  margin-bottom: 0.8rem;
  color: #F1EFE7;
}

.footer-tagline {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 14px;
  opacity: 0.7;
  letter-spacing: 0.05em;
}

.footer-nav {
  display: flex;
  gap: 6rem;
}

.footer-nav-col h5 {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.footer-nav-col p {
  font-size: 12px;
  line-height: 1.8;
  font-weight: 300;
  opacity: 0.8;
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.social-links a {
  font-size: 12px;
  text-decoration: none;
  color: inherit;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.social-links a:hover {
  opacity: 1;
}

.footer-bottom {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.business-info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.business-info-grid p {
  font-size: 10px;
  opacity: 0.5;
  margin: 0;
  letter-spacing: -0.01em;
}

.copyright {
  font-size: 9px;
  letter-spacing: 0.15em;
  opacity: 0.3;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .footer-top {
    flex-direction: column;
    gap: 3rem;
  }
  .footer-nav {
    flex-direction: column;
    gap: 2.5rem;
  }
  .footer-global {
    padding: 4rem 0 3rem;
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const authStore = useAuthStore()
const { totalCount: cartCount } = storeToRefs(cartStore)
const { isLoggedIn } = storeToRefs(authStore)

const scrolled = ref(false)

function handleScroll() {
  scrolled.value = window.scrollY > 10
}

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>
