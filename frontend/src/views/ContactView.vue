<template>
  <div class="contact-page">

    <!-- ── Full-bleed editorial hero (Chanel-style) ───────── -->
    <section class="contact-hero">
      <img
        src="/images/hero/rugs.png"
        alt="Custom fabrics and rugs by ATTIQUE DESIGN"
        class="contact-hero-img"
        fetchpriority="high"
      />

      <div class="hero-vignette"></div>

      <div class="hero-overlay">
        <span class="hero-kicker" v-reveal="{ delay: 100 }">CONTACT</span>
        <h1 class="hero-title" v-reveal="{ delay: 200 }">
          <em>Private Consultation.</em>
        </h1>
        <p class="hero-desc" v-reveal="{ delay: 400 }">
          가구와 인테리어부터 맞춤 패브릭과 러그까지,<br class="mobile-br" />
          공간의 모든 디테일을 한남 쇼룸에서 1:1로 큐레이션합니다.
        </p>
      </div>
    </section>

    <!-- ── Editorial body ─────────────────────────────────── -->
    <div class="contact-body">

      <!-- ═════ Process — image-paired editorial split ═════ -->
      <section class="process-section" v-reveal>
        <header class="section-head">
          <span class="block-label">상담 프로세스 · OUR PROCESS</span>
          <h2 class="section-title">
            Built, Furnished and <em>Styled.</em>
          </h2>
          <p class="section-lead">
            상담부터 완공까지, 당신의 공간에 온전히 집중합니다.
          </p>
        </header>

        <div class="process-split">
          <figure class="process-figure" v-reveal="{ delay: 120 }">
            <img
              src="/images/contact/consultation-table.png"
              alt="Top-down view of the ATTIQUE consultation table"
              class="process-img"
              loading="lazy"
            />
            <div class="process-img-vignette"></div>
            <figcaption class="process-figcaption">
              <span class="figcaption-place">한남 쇼룸</span>
              <span class="figcaption-sep"></span>
              <span class="figcaption-text">프라이빗 상담 테이블</span>
            </figcaption>
            <div class="process-actions">
              <button
                type="button"
                class="process-cta process-cta-trigger"
                :class="{ 'is-open': contactDropdownOpen }"
                :aria-expanded="contactDropdownOpen"
                aria-haspopup="true"
                @click.stop="contactDropdownOpen = !contactDropdownOpen"
              >
                <span class="process-cta-label">예약</span>
                <svg class="process-cta-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>

              <transition name="dropdown">
                <div
                  v-show="contactDropdownOpen"
                  class="process-dropdown"
                  @click.stop
                >
                  <a
                    href="https://m.booking.naver.com/booking/6/bizes/1563733/items/7301622?area=plt&lang=ko&theme=place"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="process-dropdown-item"
                  >
                    <span class="dropdown-label">방문 예약</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <line x1="7" y1="17" x2="17" y2="7"></line>
                      <polyline points="7 7 17 7 17 17"></polyline>
                    </svg>
                  </a>
                  <a href="tel:02-3443-8170" class="process-dropdown-item">
                    <span class="dropdown-label">전화 상담</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <line x1="7" y1="17" x2="17" y2="7"></line>
                      <polyline points="7 7 17 7 17 17"></polyline>
                    </svg>
                  </a>
                  <a
                    href="https://pf.kakao.com/_attiquedesign"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="process-dropdown-item"
                  >
                    <span class="dropdown-label">카카오톡</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <line x1="7" y1="17" x2="17" y2="7"></line>
                      <polyline points="7 7 17 7 17 17"></polyline>
                    </svg>
                  </a>
                </div>
              </transition>
            </div>
          </figure>

          <ol class="process-list" v-reveal="{ delay: 200 }">
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
        </div>
      </section>

      <!-- ═════ Endcap — Showroom block × Social block ═════ -->
      <section class="endcap" v-reveal>
        <div class="endcap-grid">
          <!-- Left: Showroom (address + hours + map link) -->
          <div class="endcap-col">
            <span class="endcap-label">한남 쇼룸 · SHOWROOM</span>
            <p class="endcap-address">
              서울시 용산구 한남대로 21길 27<br />아띠끄빌딩
            </p>
            <p class="endcap-hours">
              평일 · 토요일 10:00 – 19:00<br />
              예약 후 1:1 프라이빗 상담
            </p>
            <ul class="endcap-links">
              <li>
                <a
                  class="endcap-link"
                  href="https://map.naver.com/p/search/%EC%84%9C%EC%9A%B8%EC%8B%9C%20%EC%9A%A9%EC%82%B0%EA%B5%AC%20%ED%95%9C%EB%82%A8%EB%8C%80%EB%A1%9C%2021%EA%B8%B8%2027"
                  target="_blank"
                  rel="noopener noreferrer"
                >지도 보기</a>
              </li>
            </ul>
          </div>

          <!-- Right: Brand social -->
          <div class="endcap-col endcap-col-right">
            <span class="endcap-label">소식 받기 · FOLLOW</span>
            <p class="endcap-social-meta">
              아띠끄 디자인의 새 프로젝트와<br />
              셀렉션 소식을 확인하세요.
            </p>
            <ul class="endcap-links">
              <li>
                <a
                  class="endcap-link endcap-link-icon"
                  href="https://www.instagram.com/attiquedesign?igsh=d2dmM3Awamo1aWkz"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Instagram"
                >
                  <svg class="endcap-link-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <rect x="3" y="3" width="18" height="18" rx="5" ry="5"></rect>
                    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                  </svg>
                  <span>Instagram</span>
                </a>
              </li>
              <li>
                <a
                  class="endcap-link endcap-link-icon"
                  href="https://blog.naver.com/attique_"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Blog"
                >
                  <svg class="endcap-link-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="9" y1="13" x2="16" y2="13"></line>
                    <line x1="9" y1="17" x2="16" y2="17"></line>
                  </svg>
                  <span>Blog</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

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
    desc: '전문 시공팀의 꼼꼼한 시공과 아띠끄 셀렉션의 가구·소품·맞춤 패브릭/러그까지 원스톱으로 완성합니다.',
  },
]

const contactDropdownOpen = ref(false)

function handleOutsideClick(e: MouseEvent) {
  if (!contactDropdownOpen.value) return
  const target = e.target as HTMLElement | null
  if (!target?.closest('.process-actions')) {
    contactDropdownOpen.value = false
  }
}

function handleEscape(e: KeyboardEvent) {
  if (e.key === 'Escape') contactDropdownOpen.value = false
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.contact-page {
  background-color: #F5F0E8;
  width: 100%;
}

/* ── Hero ───────────────────────────────────────────── */
.contact-hero {
  position: relative;
  width: 100%;
  height: calc(100vh - 140px);
  min-height: 520px;
  overflow: hidden;
  background-color: #1a1a1a;
}

.contact-hero-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.hero-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.2) 38%,
    transparent 65%);
  z-index: 2;
  pointer-events: none;
}

.hero-overlay {
  position: absolute;
  left: 4rem;
  bottom: 4rem;
  z-index: 5;
  max-width: 620px;
  pointer-events: none;
}

.hero-kicker {
  display: inline-block;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.34em;
  color: rgba(255, 255, 255, 0.85);
  text-transform: uppercase;
  margin-bottom: 1.4rem;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
}

.hero-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 4.2vw, 3.6rem);
  font-weight: 400;
  line-height: 1.1;
  color: #FFFFFF;
  margin: 0 0 1.4rem 0;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 24px rgba(0, 0, 0, 0.3);
}

.hero-title em {
  font-style: italic;
  color: #E8C7A0;
  font-weight: inherit;
}

.hero-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.92);
  margin: 0;
  font-weight: 300;
  word-break: keep-all;
  text-shadow: 0 1px 12px rgba(0, 0, 0, 0.35);
}

.mobile-br {
  display: none;
}

/* ── Body ───────────────────────────────────────────── */
.contact-body {
  max-width: 1280px;
  margin: 0 auto;
  padding: 7rem 4rem 6rem;
  display: flex;
  flex-direction: column;
  gap: 7rem;
}

/* Reusable section head */
.section-head {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 3.5rem;
  max-width: 720px;
}

.block-label {
  display: inline-block;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.32em;
  color: #7E1A2C;
  text-transform: uppercase;
}

.section-title {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: clamp(2rem, 3.4vw, 2.8rem);
  font-weight: 400;
  line-height: 1.15;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.01em;
  word-break: keep-all;
}

.section-title em {
  font-style: italic;
  color: #7E1A2C;
  font-weight: inherit;
}

.section-lead {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #6D6059;
  margin: 0;
  font-weight: 300;
  word-break: keep-all;
}

/* ── Process — image-paired editorial split ─────────── */
.process-split {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 3.5rem;
  align-items: stretch;
}

.process-figure {
  position: relative;
  margin: 0;
  overflow: hidden;
  isolation: isolate;
  background-color: #1a1a1a;
  min-height: 480px;
}

.process-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.process-figure:hover .process-img {
  transform: scale(1.03);
}

.process-img-vignette {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top,
    rgba(0, 0, 0, 0.65) 0%,
    rgba(0, 0, 0, 0.2) 38%,
    transparent 60%);
  z-index: 2;
  pointer-events: none;
}

.process-figcaption {
  position: absolute;
  left: 1.6rem;
  top: 1.6rem;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.88);
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.4);
  pointer-events: none;
}

.figcaption-place {
  font-weight: 600;
  letter-spacing: 0.34em;
}

.figcaption-sep {
  display: inline-block;
  width: 22px;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.55);
}

.figcaption-text {
  font-family: 'Pretendard', sans-serif;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: none;
}

/* Overlaid trigger + dropdown on the consultation image (bottom-right) */
.process-actions {
  position: absolute;
  right: 1.4rem;
  bottom: 1.4rem;
  z-index: 4;
}

.process-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.7rem 1rem;
  text-decoration: none;
  background-color: rgba(255, 255, 255, 0.94);
  color: #312E2D;
  border: none;
  cursor: pointer;
  font-family: inherit;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  transition: background-color 0.4s ease, color 0.4s ease;
}

.process-cta:hover {
  background-color: #7E1A2C;
  color: #FFFFFF;
}

.process-cta.is-open {
  background-color: #312E2D;
  color: #F5F0E8;
}

.process-cta-label {
  font-family: 'Pretendard', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.22em;
  line-height: 1;
  text-transform: uppercase;
}

.process-cta-chevron {
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.process-cta.is-open .process-cta-chevron {
  transform: rotate(-180deg);
}

/* Dropdown panel — pops up above the trigger */
.process-dropdown {
  position: absolute;
  bottom: calc(100% + 0.4rem);
  right: 0;
  min-width: 180px;
  background-color: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
  z-index: 5;
}

.process-dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1.1rem;
  text-decoration: none;
  color: #312E2D;
  border-bottom: 1px solid rgba(49, 46, 45, 0.08);
  transition: padding 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
              background-color 0.3s ease,
              color 0.3s ease;
}

.process-dropdown-item:last-child {
  border-bottom: none;
}

.process-dropdown-item:hover {
  padding-left: 1.4rem;
  background-color: rgba(126, 26, 44, 0.08);
  color: #7E1A2C;
}

.dropdown-label {
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.04em;
}

/* Dropdown enter/leave transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.25s ease, transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

/* Numbered process list (right side) */
.process-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-self: center;
}

.process-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.4rem;
  align-items: start;
  padding: 1.6rem 0;
  border-top: 1px solid #E8E2D7;
}

.process-step:first-child {
  border-top: none;
  padding-top: 0;
}

.process-step:last-child {
  padding-bottom: 0;
}

.process-num {
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: 18px;
  font-style: italic;
  color: #7E1A2C;
  font-weight: 400;
  min-width: 32px;
  padding-top: 0.05rem;
}

.process-text {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 0;
}

.process-name {
  font-family: 'Pretendard', sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #312E2D;
  margin: 0;
  letter-spacing: -0.005em;
}

.process-desc {
  font-family: 'Pretendard', sans-serif;
  font-size: 14px;
  line-height: 1.75;
  color: #555250;
  margin: 0;
  font-weight: 400;
  word-break: keep-all;
}

/* ── Endcap — 2-col: Showroom × Social ──────────────── */
.endcap {
  padding-top: 3rem;
  border-top: 1px solid #E8E2D7;
}

.endcap-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 3rem;
  align-items: start;
}

.endcap-col {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.endcap-col-right {
  /* visual divider on the left edge */
  padding-left: 3rem;
  border-left: 1px solid rgba(49, 46, 45, 0.08);
}

.endcap-label {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: #7E1A2C;
}

.endcap-address {
  margin: 0;
  font-family: 'Playfair Display', 'Noto Serif KR', serif;
  font-size: 18px;
  line-height: 1.5;
  color: #312E2D;
  font-weight: 400;
  letter-spacing: -0.005em;
}

.endcap-hours {
  margin: 0;
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.7;
  color: #6D6059;
  font-weight: 400;
}

.endcap-social-meta {
  margin: 0;
  font-family: 'Pretendard', sans-serif;
  font-size: 13px;
  line-height: 1.7;
  color: #6D6059;
  font-weight: 400;
}

.endcap-links {
  list-style: none;
  padding: 0;
  margin: 0.4rem 0 0;
  display: flex;
  align-items: center;
  gap: 1.4rem;
}

/* Icon-paired links (Instagram, Blog) */
.endcap-link-icon {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.endcap-link-svg {
  flex-shrink: 0;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.endcap-link-icon:hover .endcap-link-svg {
  opacity: 1;
}

.endcap-link {
  font-family: 'Montserrat', 'Pretendard', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #312E2D;
  text-decoration: none;
  position: relative;
  padding-bottom: 0.25rem;
  transition: color 0.3s ease;
}

.endcap-link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 1px;
  background-color: rgba(49, 46, 45, 0.2);
  transition: background-color 0.3s ease;
}

.endcap-link:hover {
  color: #7E1A2C;
}

.endcap-link:hover::after {
  background-color: #7E1A2C;
}

/* ── Responsive ─────────────────────────────────────── */
@media (max-width: 1100px) {
  .hero-overlay {
    left: 2.5rem;
    bottom: 3rem;
  }

  .contact-body {
    padding: 5rem 2.5rem 5rem;
    gap: 5rem;
  }

  .process-split {
    gap: 2.5rem;
  }

  .process-figure {
    min-height: 420px;
  }
}

@media (max-width: 768px) {
  .mobile-br {
    display: block;
  }

  /* Match hero container to image aspect (3:2) on mobile —
     no crop, no letterbox. */
  .contact-hero {
    height: auto;
    aspect-ratio: 3 / 2;
    min-height: 0;
  }

  .hero-overlay {
    left: 1.5rem;
    right: 1.5rem;
    bottom: 1.6rem;
    max-width: none;
  }

  .hero-kicker {
    font-size: 10px;
    letter-spacing: 0.3em;
    margin-bottom: 0.8rem;
  }

  .hero-title {
    font-size: clamp(1.4rem, 6.5vw, 2rem);
    margin-bottom: 0.8rem;
  }

  .hero-desc {
    font-size: 12px;
    line-height: 1.55;
  }

  .contact-body {
    padding: 3.5rem 1.5rem 4rem;
    gap: 4rem;
  }

  .section-head {
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: clamp(1.5rem, 6vw, 2rem);
  }

  .section-lead {
    font-size: 13px;
  }

  /* Process: stack image then list */
  .process-split {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .process-figure {
    aspect-ratio: 4 / 3;
    min-height: 0;
  }

  .process-figcaption {
    left: 1rem;
    top: 1rem;
    gap: 0.5rem;
    font-size: 9px;
    letter-spacing: 0.22em;
  }

  .figcaption-sep {
    width: 14px;
  }

  .figcaption-text {
    font-size: 10px;
  }

  .process-cta {
    right: 0.9rem;
    bottom: 0.9rem;
    padding: 0.6rem 0.85rem;
    gap: 0.5rem;
  }

  .process-cta-label {
    font-size: 11px;
    letter-spacing: 0.2em;
  }

  .process-cta-arrow {
    width: 12px;
    height: 12px;
  }

  .process-step {
    padding: 1.2rem 0;
    gap: 1rem;
  }

  .process-num {
    font-size: 15px;
  }

  .process-name {
    font-size: 15px;
  }

  .process-desc {
    font-size: 13px;
    line-height: 1.7;
  }

  /* Process actions: smaller on mobile */
  .process-actions {
    right: 0.8rem;
    bottom: 0.8rem;
  }

  .process-cta {
    padding: 0.55rem 0.85rem;
    gap: 0.55rem;
  }

  .process-cta-label {
    font-size: 11px;
    letter-spacing: 0.2em;
  }

  .process-cta-chevron {
    width: 10px;
    height: 10px;
  }

  .process-dropdown {
    min-width: 160px;
  }

  .process-dropdown-item {
    padding: 0.7rem 0.95rem;
  }

  .dropdown-label {
    font-size: 12px;
  }

  /* Endcap: stack 2 cols vertically */
  .endcap {
    padding-top: 2.4rem;
  }

  .endcap-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .endcap-col-right {
    padding-left: 0;
    padding-top: 2rem;
    border-left: none;
    border-top: 1px solid rgba(49, 46, 45, 0.08);
  }

  .endcap-label {
    font-size: 9px;
    letter-spacing: 0.28em;
  }

  .endcap-address {
    font-size: 16px;
    line-height: 1.5;
  }

  .endcap-hours,
  .endcap-social-meta {
    font-size: 12px;
    line-height: 1.65;
  }

  .endcap-links {
    gap: 1.2rem;
  }

  .endcap-link {
    font-size: 10px;
    letter-spacing: 0.2em;
  }
}

@media (max-width: 600px) {
  .hero-overlay {
    bottom: 1.2rem;
  }

  /* Hide the figcaption on very small screens — CTA is enough */
  .process-figcaption {
    display: none;
  }
}
</style>
