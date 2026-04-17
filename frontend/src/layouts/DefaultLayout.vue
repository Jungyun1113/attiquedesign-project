<template>
  <div class="min-h-screen flex flex-col">
    <!-- Global Header (Logo Center + GNB) -->
    <GlobalHeader />

    <!-- Main content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer-global">
      <div class="container-page">
        <div class="footer-top">
          <div class="footer-brand">
            <p class="footer-logo-text">
              <span class="logo-line-attique">ATTIQUE</span>
              <span class="logo-line-design">DESIGN</span>
              <span class="logo-line-korean">아띠끄 디자인</span>
            </p>
          </div>
          
          <div class="footer-nav">
            <div class="footer-nav-col">
              <h5>Contact</h5>
              <p>Showroom. 서울시 용산구 한남대로 21길 27<br>T. 02-3443-8170<br>E. attique_@naver.com</p>
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
            <p>(주) 아띠끄디자인 | 대표이사 홍민영 | 사업자등록번호 116-01-39525</p>
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
  background-color: #953735;
  color: #F1EFE7;
  padding: 3rem 0 2.5rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(241, 239, 231, 0.1);
  padding-bottom: 1.5rem;
}

.footer-logo-text {
  font-family: 'Raleway', sans-serif;
  font-weight: 300;
  font-size: 1.4rem;
  line-height: 1.25;
  color: #F1EFE7;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.logo-line-attique {
  display: block;
  letter-spacing: 0.19em;
}

.logo-line-design {
  display: block;
  letter-spacing: 0.27em;
}

.logo-line-korean {
  display: block;
  font-family: 'Pretendard', sans-serif;
  font-size: 0.975rem;
  font-weight: 300;
  letter-spacing: 0.08em;
  opacity: 1;
  color: #F1EFE7;
  margin-top: 0.5rem;
}

.footer-nav {
  display: flex;
  gap: 6rem;
}

.footer-nav-col h5 {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 0.8rem;
  opacity: 0.75;
}

.footer-nav-col p {
  font-size: 12px;
  line-height: 1.8;
  font-weight: 300;
  opacity: 1;
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
  opacity: 1;
  transition: opacity 0.3s ease;
}

.social-links a:hover {
  opacity: 1;
}

.footer-bottom {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
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
  margin-top: 0.4rem;
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
    padding: 2.5rem 0 2rem;
  }
  .footer-logo-text {
    font-size: 1.12rem;
    align-items: flex-start;
    text-align: left;
  }
  .logo-line-korean {
    font-size: 0.78rem;
  }
}
</style>

<script setup lang="ts">
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import { storeToRefs } from 'pinia'
import GlobalHeader from '@/components/navigation/GlobalHeader.vue'

const cartStore = useCartStore()
const authStore = useAuthStore()
const { totalCount: cartCount } = storeToRefs(cartStore)
const { isLoggedIn } = storeToRefs(authStore)

</script>
