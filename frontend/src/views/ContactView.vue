<template>
  <div class="contact-page">
    <div class="contact-asymmetric">

      <!-- ── Left: Photo-dominant column ───────────────── -->
      <div class="photo-side" v-reveal>
        <div class="photo-frame">
          <img
            src="/images/showroom-building.png"
            alt="Attique Design Showroom Building"
            class="photo-img"
          />
        </div>
      </div>

      <!-- ── Right: Editorial content column ───────────── -->
      <div class="content-side">
        <div class="content-inner">

          <!-- Title block -->
          <header class="content-header" v-reveal>
            <span class="kicker">CONTACT</span>
            <h1 class="title">
              Private<br />
              <em>Consultation.</em>
            </h1>
            <p class="lead">
              한남동 쇼룸에서 직접 만나뵙고,<br />
              공간과 가구를 1:1로 큐레이션해 드립니다.
            </p>
          </header>

          <hr class="rule" />

          <!-- Process / How we work -->
          <section class="process-block" v-reveal="{ delay: 100 }">
            <span class="block-label">OUR PROCESS</span>
            <h2 class="process-headline">
              Built, Furnished and <em>Styled.</em>
            </h2>
            <p class="process-intro">
              상담부터 완공까지, 당신의 공간에 온전히 집중합니다.
            </p>

            <ol class="process-list">
              <li
                v-for="(step, i) in processSteps"
                :key="i"
                class="process-step"
              >
                <span class="process-num">0{{ i + 1 }}</span>
                <div class="process-text">
                  <h3 class="process-name">{{ step.title }}</h3>
                  <p class="process-desc">{{ step.desc }}</p>
                </div>
              </li>
            </ol>
          </section>

          <hr class="rule" />

          <!-- Address block -->
          <section class="address-block" v-reveal="{ delay: 150 }">
            <span class="block-label">SHOWROOM</span>
            <p class="address">
              서울시 용산구 한남대로 21길 27<br />
              아띠끄 빌딩
            </p>
            <a
              href="https://map.naver.com/p/search/%EC%84%9C%EC%9A%B8%EC%8B%9C%20%EC%9A%A9%EC%82%B0%EA%B5%AC%20%ED%95%9C%EB%82%A8%EB%8C%80%EB%A1%9C%2021%EA%B8%B8%2027"
              target="_blank"
              rel="noopener noreferrer"
              class="directions-link"
            >
              <span>길찾기</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </a>
          </section>

          <hr class="rule" />

          <!-- Contact methods -->
          <section class="methods" v-reveal="{ delay: 200 }">
            <span class="block-label">GET IN TOUCH</span>

            <ul class="method-list">
              <li class="method-item">
                <a href="tel:02-3443-8170" class="method-link">
                  <span class="method-num">01</span>
                  <div class="method-body">
                    <h3 class="method-name">Call</h3>
                    <p class="method-detail">02-3443-8170</p>
                    <p class="method-meta">Mon — Sat · 10:00 – 19:00</p>
                  </div>
                  <svg class="method-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </a>
              </li>

              <li class="method-item">
                <a
                  href="https://pf.kakao.com/_attiquedesign"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="method-link"
                >
                  <span class="method-num">02</span>
                  <div class="method-body">
                    <h3 class="method-name">KakaoTalk</h3>
                    <p class="method-detail">실시간 상담</p>
                    <p class="method-meta">@아띠끄디자인</p>
                  </div>
                  <svg class="method-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </a>
              </li>

              <li class="method-item">
                <a
                  href="https://m.booking.naver.com/booking/6/bizes/1563733/items/7301622?area=plt&lang=ko&theme=place"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="method-link is-primary"
                >
                  <span class="method-num">03</span>
                  <div class="method-body">
                    <h3 class="method-name">Book a Visit</h3>
                    <p class="method-detail">1:1 프라이빗 방문 상담</p>
                    <p class="method-meta">예약 후 방문</p>
                  </div>
                  <svg class="method-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </a>
              </li>
            </ul>
          </section>

          <hr class="rule" />

          <!-- Social -->
          <section class="social-row" v-reveal="{ delay: 300 }">
            <span class="block-label">FOLLOW</span>
            <div class="social-links">
              <a
                href="https://www.instagram.com/attiquedesign?igsh=d2dmM3Awamo1aWkz"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
              >Instagram</a>
              <a
                href="https://blog.naver.com/attique_"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
              >Blog</a>
            </div>
          </section>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const processSteps = [
  {
    title: '프라이빗 상담',
    desc: '한남 쇼룸에서 1:1 맞춤 상담으로 고객의 라이프스타일과 공간을 깊이 이해합니다.',
  },
  {
    title: '컨셉 설계 & 견적',
    desc: '공간 콘셉트 보드와 3D 시뮬레이션을 통해 완성될 공간을 미리 경험합니다.',
  },
  {
    title: '시공 & 스타일링',
    desc: '전문 시공팀의 꼼꼼한 시공과 아띠끄 셀렉션의 가구·소품 배치까지 원스톱으로 완성합니다.',
  },
]
</script>

<style scoped>
.contact-page {
  background-color: #F5F0E8;
  width: 100%;
}

/* ── Asymmetric grid: photo dominant left, content right ── */
.contact-asymmetric {
  display: grid;
  grid-template-columns: 58fr 42fr;
  min-height: calc(100vh - 140px);
  width: 100%;
}

/* ── Left: Photo side ───────────────────────────────── */
.photo-side {
  background-color: #EFE9DD;
  position: relative;
  overflow: hidden;
}

.photo-frame {
  position: sticky;
  top: 0;
  width: 100%;
  height: 100vh;
  max-height: calc(100vh - 0px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 3rem;
  box-sizing: border-box;
}

.photo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  filter: drop-shadow(0 16px 48px rgba(0, 0, 0, 0.08));
}

/* ── Right: Content side ────────────────────────────── */
.content-side {
  display: flex;
  align-items: flex-start;
  padding: 5rem 4rem 6rem;
}

.content-inner {
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
}

/* ── Header block ───────────────────────────────────── */
.content-header {
  margin-bottom: 3rem;
}

.kicker,
.block-label {
  display: inline-block;
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.32em;
  color: #953735;
  text-transform: uppercase;
}

.kicker {
  margin-bottom: 1.5rem;
}

.block-label {
  margin-bottom: 1.4rem;
  color: #6D6059;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(40px, 5vw, 72px);
  font-weight: 400;
  line-height: 1.05;
  color: #312E2D;
  margin: 0 0 1.6rem 0;
  letter-spacing: -0.01em;
}

.title em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.lead {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.8;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
}

/* ── Horizontal rule between sections ──────────────── */
.rule {
  border: none;
  border-top: 1px solid #E8E2D7;
  margin: 0;
  width: 100%;
}

/* ── Process block ──────────────────────────────────── */
.process-block {
  padding: 2.5rem 0;
  display: flex;
  flex-direction: column;
}

.process-headline {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 400;
  line-height: 1.2;
  color: #312E2D;
  margin: 0 0 0.8rem 0;
  letter-spacing: -0.01em;
}

.process-headline em {
  font-style: italic;
  color: #953735;
  font-weight: inherit;
}

.process-intro {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0 0 2rem 0;
  font-weight: 300;
}

.process-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}

.process-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.2rem;
  align-items: start;
  padding-top: 1.2rem;
  border-top: 1px solid #E8E2D7;
}

.process-step:first-child {
  border-top: none;
  padding-top: 0;
}

.process-num {
  font-family: 'Playfair Display', serif;
  font-size: 14px;
  font-style: italic;
  color: #953735;
  font-weight: 400;
  min-width: 28px;
  padding-top: 0.15rem;
}

.process-text {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  min-width: 0;
}

.process-name {
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.005em;
}

.process-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
}

/* ── Address block ──────────────────────────────────── */
.address-block {
  padding: 2.5rem 0;
  display: flex;
  flex-direction: column;
}

.address {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  line-height: 1.45;
  color: #312E2D;
  margin: 0 0 1.4rem 0;
  font-weight: 400;
}

.directions-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #312E2D;
  text-decoration: none;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #312E2D;
  align-self: flex-start;
  transition: gap 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.directions-link:hover {
  gap: 0.9rem;
  color: #953735;
  border-bottom-color: #953735;
}

/* ── Methods ────────────────────────────────────────── */
.methods {
  padding: 2.5rem 0;
}

.method-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.method-item + .method-item {
  border-top: 1px dashed #E8E2D7;
}

.method-link {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1.4rem;
  padding: 1.4rem 0.4rem;
  text-decoration: none;
  color: #312E2D;
  transition: padding 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
              background-color 0.4s ease;
}

.method-link:hover {
  padding-left: 1.2rem;
  padding-right: 1.2rem;
  background-color: rgba(149, 55, 53, 0.04);
}

.method-num {
  font-family: 'Playfair Display', serif;
  font-size: 14px;
  font-style: italic;
  color: #953735;
  font-weight: 400;
  min-width: 28px;
}

.method-body {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.method-name {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 400;
  color: #312E2D;
  margin: 0;
  line-height: 1.2;
  transition: color 0.3s ease;
}

.method-link:hover .method-name {
  color: #953735;
}

.method-detail {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  color: #312E2D;
  margin: 0;
  font-weight: 400;
}

.method-meta {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  letter-spacing: 0.18em;
  color: #6D6059;
  margin: 0;
  text-transform: uppercase;
  font-weight: 400;
}

.method-arrow {
  color: #6D6059;
  transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
              color 0.3s ease;
  flex-shrink: 0;
}

.method-link:hover .method-arrow {
  transform: translate(4px, -4px);
  color: #953735;
}

.method-link.is-primary .method-num {
  color: #953735;
}

/* ── Social ─────────────────────────────────────────── */
.social-row {
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.social-links {
  display: flex;
  align-items: center;
  gap: 1.6rem;
}

.social-link {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-style: italic;
  color: #312E2D;
  text-decoration: none;
  position: relative;
  transition: color 0.3s ease;
}

.social-link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 0;
  height: 1px;
  background-color: #953735;
  transition: width 0.4s ease;
}

.social-link:hover {
  color: #953735;
}

.social-link:hover::after {
  width: 100%;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 1100px) {
  .content-side {
    padding: 4rem 2.5rem 5rem;
  }

  .photo-frame {
    padding: 3rem 2rem;
  }
}

@media (max-width: 900px) {
  .contact-asymmetric {
    grid-template-columns: 1fr;
    min-height: 0;
  }

  .photo-side {
    width: 100%;
  }

  .photo-frame {
    position: relative;
    height: 50vh;
    min-height: 320px;
    padding: 2rem 1.5rem;
  }

  .content-side {
    padding: 3rem 1.5rem 5rem;
    justify-content: center;
  }

  .content-inner {
    max-width: 100%;
  }

  .title {
    font-size: clamp(36px, 9vw, 56px);
  }

  .address {
    font-size: 18px;
  }

  .method-name {
    font-size: 20px;
  }

  .process-headline {
    font-size: 22px;
  }

  .process-name {
    font-size: 15px;
  }
}

@media (max-width: 600px) {
  .photo-frame {
    height: 42vh;
    min-height: 280px;
  }

  .content-side {
    padding: 2.5rem 1.25rem 4rem;
  }

  .lead {
    font-size: 14px;
  }
}
</style>
