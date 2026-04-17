<template>
  <div class="contact-page">
    <div class="contact-wrapper">
      <div class="contact-layout-split">
        <!-- 좌측: 쇼룸 빌딩 사진 -->
        <div class="contact-image-wrap">
          <img src="/images/showroom-building.png" alt="Attique Design Showroom Building" class="contact-building-img" />
        </div>

        <!-- 우측: 컨택 정보 -->
        <div class="contact-inner">
          <!-- 메인 타이틀: "Private Consultation." 딥 버건디 -->
          <h2 class="contact-title">Private Consultation.</h2>

          <!-- 주소 및 연락처 정보 (2줄 배치) -->
          <div class="contact-info">
            <p class="contact-address">Showroom. 서울시 용산구 한남대로 21길 27 아띠끄 디자인</p>
            <div class="contact-phone-row">
              <span class="contact-phone">T. 02-3443-8170</span>
              <div class="contact-social-group">
                <!-- 카카오톡 문의 -->
                <a
                  href="https://pf.kakao.com/_attiquedesign"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="contact-social-icon kakao"
                  aria-label="카카오톡 문의하기"
                >
                  <svg class="social-svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 3C6.48 3 2 6.58 2 10.94c0 2.8 1.86 5.27 4.66 6.67-.15.53-.96 3.41-1 3.57 0 0-.02.15.07.21.1.06.21.01.21.01.28-.04 3.24-2.13 3.75-2.5.74.11 1.52.16 2.31.16 5.52 0 10-3.58 10-7.94S17.52 3 12 3z"/>
                  </svg>
                </a>
                <!-- 인스타그램 -->
                <a
                  href="https://www.instagram.com/attiquedesign?igsh=d2dmM3Awamo1aWkz"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="contact-social-icon instagram"
                  aria-label="인스타그램"
                >
                  <svg class="social-svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 1.17.054 1.805.249 2.227.412.56.216.96.474 1.38.894.42.42.678.82.894 1.38.163.422.358 1.057.412 2.227.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.054 1.17-.249 1.805-.412 2.227-.216.56-.474.96-.894 1.38-.42.42-.82.678-1.38.894-.422.163-1.057.358-2.227.412-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.054-1.805-.249-2.227-.412-.56-.216-.96-.474-1.38-.894-.42-.42-.678-.82-.894-1.38-.163-.422-.358-1.057-.412-2.227-.058-1.266-.07-1.646-.07-4.85s.012-3.584.07-4.85c.054-1.17.249-1.805.412-2.227.216-.56.474-.96.894-1.38.42-.42.82-.678 1.38-.894.422-.163 1.057-.358 2.227-.412 1.266-.058 1.646-.07 4.85-.07zm0-2.163c-3.259 0-3.667.014-4.947.072-1.277.057-2.15.26-2.914.558-.79.308-1.458.72-2.122 1.383-.663.664-1.075 1.332-1.383 2.122-.3 1.114-.501 1.637-.558 2.914-.058 1.28-.072 1.688-.072 4.947s.014 3.667.072 4.947c.057 1.277.26 2.15.558 2.914.308.79.72 1.458 1.383 2.122.664.663 1.332 1.075 2.122 1.383 1.114.3 1.637.501 2.914.558 1.28.058 1.688.072 4.947.072s3.667-.014 4.947-.072c1.277-.057 2.15-.26 2.914-.558.79-.308 1.458-.72 2.122-1.383.663-.664 1.075-1.332 1.383-2.122.3-1.114.501-1.637.558-2.914.058-1.28.072-1.688.072-4.947s-.014-3.667-.072-4.947c-.057-1.277-.26-2.15-.558-2.914-.308-.79-.72-1.458-1.383-2.122-.664-.663-1.332-1.075-2.122-1.383-1.114-.3-1.637-.501-2.914-.558-1.28-.058-1.688-.072-4.947-.072zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.162 6.162 6.162 6.162-2.759 6.162-6.162-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.791-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.209-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                </a>
                <!-- 블로그 -->
                <a
                  href="https://blog.naver.com/attique_"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="contact-social-icon blog"
                  aria-label="블로그"
                >
                  <svg class="social-svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.1 2.9 22 4 22H20C21.1 22 22 21.1 22 20V4C22 2.9 21.1 2 20 2ZM13.5 17.5C11.6 17.5 10 15.9 10 14C10 12.1 11.6 10.5 13.5 10.5C15.4 10.5 17 12.1 17 14C17 15.9 15.4 17.5 13.5 17.5ZM16.2 8.2C15.8 8.2 15.5 7.9 15.5 7.5C15.5 7.1 15.8 6.8 16.2 6.8C16.6 6.8 16.9 7.1 16.9 7.5C16.9 7.9 16.6 8.2 16.2 8.2Z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>

          <div class="contact-actions">
            <!-- 방문상담 예약하기 버튼 (네이버 예약 연결) -->
            <a
              href="https://m.booking.naver.com/booking/6/bizes/1563733/items/7301622?area=plt&lang=ko&theme=place"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-booking"
            >
              방문상담 예약하기
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Logic if needed
</script>

<style scoped>
.contact-page {
  background-color: #F5F0E8;
  min-height: calc(100vh - 160px);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.contact-wrapper {
  width: 100%;
  max-width: 1200px;
}

.contact-layout-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
}

.contact-image-wrap {
  aspect-ratio: 3/4;
  overflow: hidden;
  background-color: #eee;
}

.contact-building-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.contact-inner {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.contact-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: clamp(32px, 5vw, 56px);
  color: #953735;
  margin: 0;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-address {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #000;
  margin: 0;
}

.contact-phone-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.contact-phone {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #000;
}

.contact-social-group {
  display: flex;
  gap: 1rem;
}

.contact-social-icon {
  width: 24px;
  height: 24px;
  color: #312E2D;
  transition: color 0.3s ease;
}

.contact-social-icon:hover {
  color: #953735;
}

.social-svg {
  width: 100%;
  height: 100%;
}

.contact-actions {
  margin-top: 1rem;
}

.btn-booking {
  display: inline-block;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.25em;
  padding: 1.2rem 2.8rem;
  background-color: #312E2D;
  color: #fff;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-booking:hover,
.btn-booking:active {
  background-color: #953735;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

@media (max-width: 900px) {
  .contact-layout-split {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  .contact-image-wrap {
    aspect-ratio: 16/9;
  }
}
</style>
