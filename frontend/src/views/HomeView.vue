<template>
  <ScrollSnapContainer>

    <!-- ═══════════════════════════════════════════════════ -->
    <!-- Section 0: LANDING (Video & Logo Animation)        -->
    <!-- ═══════════════════════════════════════════════════ -->
    <FullScreenSection id="intro">
      <!-- 반응형 웰컴 이미지 (PC/모바일 잘림 방지 세팅) -->
      <img
        src="/Place_this_ornate_vintage_French_rococo_floral_pai-1775114198409.png"
        class="landing-image"
        alt="Attique Design Home"
      />
      <!-- 오버레이 제거 (배경색 왜곡 방지) -->

      <!-- 스크롤 힌트 -->
      <div class="scroll-hint" :style="{ opacity: Math.max(0, 1 - scrollProgress * 2.5) }">
        <span class="scroll-hint-text">Scroll</span>
        <div class="scroll-hint-line"></div>
      </div>
    </FullScreenSection>

    <!-- ═══════════════════════════════════════════════════ -->
    <!-- Section 1: PHILOSOPHY (Overlapping Editorial)      -->
    <!-- ═══════════════════════════════════════════════════ -->
    <FullScreenSection id="philosophy" bgClass="philosophy-section">
      <div ref="philoRef" class="philo-container" :class="{ 'is-visible': philoVisible }">

        <!-- 거대한 오버래핑 타이틀: 섹션 상단에 걸쳐짐 -->
        <h2 class="philo-title">
          When Preference Becomes <em class="philo-accent">Lifestyle</em>.
        </h2>

        <!-- 오버래핑 본문 (타이틀과 레이어 겹침) -->
        <div class="philo-body-block">
          <div class="philo-eyebrow">
            <span class="philo-eyebrow-line"></span>
            <p class="philo-eyebrow-text">Our Philosophy</p>
            <span class="philo-eyebrow-line"></span>
          </div>
          <div class="philo-body">
            <p class="philo-text">사람의 일상과 공간이 자연스럽게 어우러지는 밸런스를 고민합니다.</p>
            <p class="philo-text">주거와 상업 공간, 스타일링까지 아우르며 엄선한 셀렉션과 맞춤형 설계로 취향이 담긴 공간을 완성합니다.</p>
          </div>
        </div>

        <!-- 서비스 영역 — 화면 하단에 가로로 길게 흐르는 텍스트 애니메이션 (Marquee) -->
        <div class="philo-services-marquee">
          <div class="philo-marquee-track">
            <span
              v-for="(service, idx) in [...services, ...services, ...services]"
              :key="idx"
              class="philo-service-item"
            >
              {{ service }}
            </span>
          </div>
        </div>

      </div>
    </FullScreenSection>

    <!-- ═══════════════════════════════════════════════════ -->
    <!-- Section 2: PORTFOLIO (Curated Selection Grid)      -->
    <!-- ═══════════════════════════════════════════════════ -->
    <FullScreenSection id="portfolio" bgClass="portfolio-section">
      <div class="portfolio-grid">

        <!-- 대형 1: Residential (좌측, 전체 높이 — 70%+ 비중) -->
        <div 
          class="portfolio-item portfolio-item--large" 
          :class="{ 'is-active': activePortfolioId === portfolioItems[0].id }"
          @click="togglePortfolio(portfolioItems[0])"
        >
          <img :src="portfolioItems[0].img" :alt="portfolioItems[0].label" />
          <div class="portfolio-hover-overlay">
            <span class="portfolio-hover-cat">{{ portfolioItems[0].label }}</span>
          </div>
        </div>

        <!-- 우측 열 -->
        <div class="portfolio-right-col">
          <!-- 대형 2: Commercial -->
          <div 
            class="portfolio-item portfolio-item--medium" 
            :class="{ 'is-active': activePortfolioId === portfolioItems[1].id }"
            @click="togglePortfolio(portfolioItems[1])"
          >
            <img :src="portfolioItems[1].img" :alt="portfolioItems[1].label" />
            <div class="portfolio-hover-overlay">
              <span class="portfolio-hover-cat">{{ portfolioItems[1].label }}</span>
            </div>
          </div>

          <!-- 소형: Drama + Magazine -->
          <div class="portfolio-small-row">
            <div 
              class="portfolio-item portfolio-item--small" 
              :class="{ 'is-active': activePortfolioId === portfolioItems[2].id }"
              @click="togglePortfolio(portfolioItems[2])"
            >
              <img :src="portfolioItems[2].img" :alt="portfolioItems[2].label" />
              <div class="portfolio-hover-overlay">
                <span class="portfolio-hover-cat">{{ portfolioItems[2].label }}</span>
              </div>
            </div>
            <div 
              class="portfolio-item portfolio-item--small" 
              :class="{ 'is-active': activePortfolioId === portfolioItems[3].id }"
              @click="togglePortfolio(portfolioItems[3])"
            >
              <img :src="portfolioItems[3].img" :alt="portfolioItems[3].label" />
              <div class="portfolio-hover-overlay">
                <span class="portfolio-hover-cat">{{ portfolioItems[3].label }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Shared Element Transition: 클릭 시 사진이 풀스크린 줌인 -->
      <Teleport to="body">
        <div
          v-if="expandedItem"
          class="portfolio-expand-overlay"
          :class="{ 'is-entering': expandEntering }"
        >
          <img :src="expandedItem.img" :alt="expandedItem.label" class="expand-img" />
          <!-- 확장 시에도 텍스트가 유지되도록 추가 -->
          <div class="expand-text-wrap" v-if="expandEntering">
            <span class="portfolio-hover-cat">{{ expandedItem.label }}</span>
          </div>
        </div>
      </Teleport>
    </FullScreenSection>

    <!-- ═══════════════════════════════════════════════════ -->
    <!-- Section 3: SELECTION (Exhibition Archive)          -->
    <!-- 컨셉: 제품 나열이 아닌 '공간 전시'               -->
    <!-- ═══════════════════════════════════════════════════ -->
    <FullScreenSection id="selection" bgClass="selection-section">
      <div class="sel-exhibition">

        <!-- 좌측: 스타일링된 공간 전체 샷 (최대 3장 갤러리) -->
        <div class="sel-main-visual">
          <div class="sel-main-gallery">
            <template v-for="(img, imgIdx) in selectionSpaces[activeSpaceIndex].images" :key="imgIdx">
              <img
                :src="img"
                :alt="selectionSpaces[activeSpaceIndex].title + ' ' + imgIdx"
                class="sel-main-img"
                :class="{ 'is-active': activeGalleryIndex === imgIdx }"
              />
            </template>
          </div>
          <div class="sel-main-overlay">
            <h3 class="sel-main-title">{{ selectionSpaces[activeSpaceIndex].title }}</h3>
            <p class="sel-main-subtitle">{{ selectionSpaces[activeSpaceIndex].subtitle }}</p>
          </div>
          <!-- 전환 네비게이션 컨테이너 (오른쪽 하단 통합) -->
          <div class="sel-nav-group">
            <!-- 공간 자체 전환 도트 -->
            <div class="sel-space-nav">
              <button
                v-for="(space, idx) in selectionSpaces"
                :key="space.id"
                class="sel-space-dot"
                :class="{ active: activeSpaceIndex === idx }"
                @click="switchSpace(idx)"
                :aria-label="`${space.title} 보기`"
              ></button>
            </div>
          </div>
        </div>

        <!-- 우측: 해당 공간에 쓰인 오브제들 (위아래 스크롤 가능) -->
        <div class="sel-objects scrollable-objects">
          <div
            v-for="obj in selectionSpaces[activeSpaceIndex].objects"
            :key="obj.id"
            class="sel-object-card"
          >
            <div class="sel-object-img-wrap">
              <img :src="obj.img" :alt="obj.name" />
            </div>
            <p class="sel-object-name">{{ obj.name }}</p>
            <!-- 통합 View Detail 버튼 -->
            <button class="sel-object-cta" @click="enquireObject(obj)">
              View Detail
            </button>
          </div>
        </div>

      </div>
    </FullScreenSection>

    <!-- ═══════════════════════════════════════════════════ -->
    <!-- Section 4: CONTACT & BOOKING (Minimalist Finish)   -->
    <!-- 사진 없이 광활한 여백 중앙에 타이포그래피만        -->
    <!-- ═══════════════════════════════════════════════════ -->
    <FullScreenSection id="contact" bgClass="contact-section">
      <div class="contact-wrapper">
        <div class="contact-layout-split">
          <!-- 좌측: 쇼룸 빌딩 사진 -->
          <div class="contact-image-wrap">
            <img src="/images/showroom-building.jpg" alt="Attique Design Showroom Building" class="contact-building-img" />
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
              <!-- 카카오톡 문의 -->
              <a
                href="https://pf.kakao.com/_attiquedesign"
                target="_blank"
                rel="noopener noreferrer"
                class="contact-kakao-icon"
                aria-label="카카오톡 문의하기"
              >
                <svg class="kakao-svg" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 3C6.48 3 2 6.58 2 10.94c0 2.8 1.86 5.27 4.66 6.67-.15.53-.96 3.41-1 3.57 0 0-.02.15.07.21.1.06.21.01.21.01.28-.04 3.24-2.13 3.75-2.5.74.11 1.52.16 2.31.16 5.52 0 10-3.58 10-7.94S17.52 3 12 3z"/>
                </svg>
              </a>
            </div>
          </div>

          <div class="contact-actions">
            <!-- 방문상담 예약하기 버튼 (네이버 예약 연결) -->
            <a
              href="https://booking.naver.com/booking/13/bizes/1234567"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-booking"
            >
              방문상담 예약하기
            </a>
          </div>

        </div>
        </div>

        <!-- Footer 통합: 국내법에 맞는 사업자 정보 및 저작권 표기를 최하단에 작게 -->
        <div class="contact-footer">
          <p class="business-info">
            상호: 아띠끄디자인 | 대표: 홍민영 | 사업자등록번호: 123-45-67890 | 통신판매업신고번호: 제2026-서울용산-0000호<br/>
            주소: 서울시 용산구 한남대로 21길 27 | 개인정보관리책임자: 홍민영<br/>
            대표전화: 02-3443-8170 | 이메일: info@attiquedesign.com
          </p>
          <p class="contact-copyright">© 2026 ATTIQUE DESIGN. All rights reserved.</p>
        </div>
      </div>
    </FullScreenSection>

  </ScrollSnapContainer>

  <!-- ═══════════════════════════════════════════════════ -->
  <!-- FIXED LOGO: Section 바깥, 스크롤에 따라 축소·이동·고정 -->
  <!-- (miltontextiles.com 참고: 정중앙 거대 → 상단 좌측 고정) -->
  <!-- ═══════════════════════════════════════════════════ -->
  <div
    class="fixed-logo"
    :class="{
      'is-shrunk': scrollProgress > 0.95
    }"
    :style="logoTransformStyle"
  >
    <h1 class="fixed-logo-text">ATTIQUE<br/>DESIGN</h1>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import ScrollSnapContainer from '@/components/navigation/ScrollSnapContainer.vue'
import FullScreenSection from '@/components/navigation/FullScreenSection.vue'

const router = useRouter()

// ═══════════════════════════════════════════
// Scroll-driven Logo Animation
// ═══════════════════════════════════════════
const scrollProgress = ref(0)
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth <= 768
}
/* videoRef removal as video is replaced by image */

function handleScroll() {
  const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
  if (!scrollRoot) return
  const sectionHeight = window.innerHeight
  const scrollTop = scrollRoot.scrollTop
  // 0 → 1: Section 0 내에서의 스크롤 진행도
  scrollProgress.value = Math.min(1, Math.max(0, scrollTop / (sectionHeight * 0.55)))
}

onMounted(() => {
  nextTick(() => {
    checkMobile()
    window.addEventListener('resize', checkMobile)
    const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
    if (scrollRoot) {
      scrollRoot.addEventListener('scroll', handleScroll, { passive: true })
    }
    // Philosophy Intersection Observer
    setupPhiloObserver()
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
  if (scrollRoot) {
    scrollRoot.removeEventListener('scroll', handleScroll)
  }
})

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t
}

// 로고 transform: 가구 중앙(거대) → 좌측 상단(축소·고정)
const logoTransformStyle = computed(() => {
  const t = scrollProgress.value
  const eased = 1 - Math.pow(1 - t, 3)

  const scale = lerp(isMobile.value ? 0.6 : 0.75, 0.22, eased)
  // 시작 위치(Y축): PC는 가구 위로 좀 더 올림(-18), 모바일은 기존 유지
  const startTy = isMobile.value ? -22 : -18
  
  // 시작 위치 (기기별로 가구 중앙 정렬 미세 조정)
  const xStart = isMobile.value ? 62 : 54 // PC는 왼쪽으로(-4), 모바일은 오른쪽으로(+4) 각 58vw에서 조정
  const yStart = 50 + startTy // vh
  
  // 타겟 위치 (여백)
  const xEnd = isMobile.value ? 1.2 : 2 // rem
  const yEnd = isMobile.value ? 1.2 : 2 // rem

  // 현재 위치 계산: vw/vh 기반 좌표에서 -> rem 기반 좌표로 부드럽게 전이
  // 중앙 정렬(translate -50%)에서 -> 좌상단 정렬(translate 0)으로 부드럽게 전이
  const curX = lerp(xStart, 0, eased)
  const curY = lerp(yStart, 0, eased)
  const shiftPct = lerp(-50, 0, eased)
  
  const opacity = t > 0.9 ? lerp(1, 0.9, (t - 0.9) / 0.1) : 1

  return {
    transform: `translate(calc(${curX}vw + ${eased} * ${xEnd}rem), calc(${curY}vh + ${eased} * ${yEnd}rem)) translate(${shiftPct}%, ${shiftPct}%) scale(${scale})`,
    opacity: String(opacity),
  }
})

// ═══════════════════════════════════════════
// Philosophy — 서비스 영역 Visibility
// ═══════════════════════════════════════════
const services = [
  'Interior', 'Styling', 'Furniture', 'Lighting', 'Fabric', 'Rug', 'Accessories'
]

const philoRef = ref<HTMLElement | null>(null)
const philoVisible = ref(false)

function setupPhiloObserver() {
  const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
  if (!philoRef.value) return

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          philoVisible.value = true
        }
      })
    },
    {
      root: scrollRoot,
      threshold: 0.3,
    }
  )
  observer.observe(philoRef.value)
}

// ═══════════════════════════════════════════
// Portfolio — 4 Categories
// ═══════════════════════════════════════════
interface PortfolioItem { id: string; label: string; img: string; desc: string }

const portfolioItems: PortfolioItem[] = [
  {
    id: 'residential', label: 'Residential',
    img: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1800&q=85',
    desc: '주거 공간의 일상과 미학이 자연스럽게 어우러지는 것.'
  },
  {
    id: 'commercial', label: 'Commercial',
    img: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1800&q=85',
    desc: '브랜드의 아이덴티티를 공간으로 번역하는 예술.'
  },
  {
    id: 'drama', label: 'Drama',
    img: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1400&q=85',
    desc: '드라마와 영화 속에서 만나는 아띠끄의 미학.'
  },
  {
    id: 'magazine', label: 'Magazine',
    img: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=1400&q=85',
    desc: '매거진의 질감으로 편집된 아늑함.'
  },
]

const expandedItem = ref<PortfolioItem | null>(null)
const expandEntering = ref(false)

const activePortfolioId = ref<string | null>(null)

function togglePortfolio(item: PortfolioItem) {
  if (isMobile.value) {
    if (activePortfolioId.value === item.id) {
      expandPortfolio(item)
      activePortfolioId.value = null
    } else {
      activePortfolioId.value = item.id
    }
  } else {
    expandPortfolio(item)
  }
}

function expandPortfolio(item: PortfolioItem) {
  expandedItem.value = item
  expandEntering.value = false
  requestAnimationFrame(() => {
    expandEntering.value = true
    setTimeout(() => {
      router.push(`/portfolio/${item.id}`)
      setTimeout(() => { expandedItem.value = null; expandEntering.value = false }, 500)
    }, 850)
  })
}

// ═══════════════════════════════════════════
// Selection — Exhibition Archive
// ═══════════════════════════════════════════
const activeSpaceIndex = ref(0)
const activeGalleryIndex = ref(0)

function switchSpace(idx: number) {
  activeSpaceIndex.value = idx
  activeGalleryIndex.value = 0
}

interface SpaceObject { id: string; name: string; img: string; ctaLabel?: string }
interface SelectionSpace { id: string; title: string; subtitle: string; images: string[]; objects: SpaceObject[] }

const selectionSpaces: SelectionSpace[] = [
  {
    id: 'warm-sanctuary',
    title: 'Warm Sanctuary',
    subtitle: 'A curated space where dark walnut meets burgundy textiles',
    images: [
      'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=1800&q=85',
      'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1800&q=85',
      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1800&q=85'
    ],
    objects: [
      { id: 'obj-1', name: 'Walnut Console', img: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=85' },
      { id: 'obj-2', name: 'Linen Armchair', img: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=600&q=85' },
      { id: 'obj-3', name: 'Ceramic Vase', img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=600&q=85' },
      { id: 'obj-4', name: 'Wool Rug', img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=600&q=85' },
      { id: 'obj-5', name: 'Brass Lamp', img: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=85' },
    ]
  },
  {
    id: 'nordic-calm',
    title: 'Nordic Calm',
    subtitle: 'Scandinavian minimalism with warm undertones',
    images: [
      'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1800&q=85',
      'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1800&q=85',
      'https://images.unsplash.com/photo-1513519247388-4e2863d0c647?w=1800&q=85'
    ],
    objects: [
      { id: 'obj-6', name: 'Oak Dining Table', img: 'https://images.unsplash.com/photo-1549497538-303791108f95?w=600&q=85' },
      { id: 'obj-7', name: 'Pendant Light', img: 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=600&q=85' },
      { id: 'obj-8', name: 'Wool Throw', img: 'https://images.unsplash.com/photo-1616627547584-bf28cee262db?w=600&q=85' },
      { id: 'obj-9', name: 'Minimal Vase', img: 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=600&q=85' },
    ]
  },
  {
    id: 'modern-noir',
    title: 'Modern Noir',
    subtitle: 'Sophisticated monochrome with metallic accents',
    images: [
      'https://images.unsplash.com/photo-1594026112284-02bb6f3352fe?w=1800&q=85',
      'https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1800&q=85',
      'https://images.unsplash.com/photo-1540518614846-7eded433c457?w=1800&q=85'
    ],
    objects: [
      { id: 'obj-10', name: 'Black Marble Table', img: 'https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=600&q=85' },
      { id: 'obj-11', name: 'Silver Sculpture', img: 'https://images.unsplash.com/photo-1554188248-986adbb73be4?w=600&q=85' },
      { id: 'obj-12', name: 'Leather Sofa', img: 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600&q=85' },
    ]
  },
]

function enquireObject(obj: SpaceObject) {
  router.push(`/selection/${obj.id}`)
}

// ═══════════════════════════════════════════
// Contact
// ═══════════════════════════════════════════
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════
   FIXED LOGO (position: fixed — 모든 섹션 위에 떠있음)
   miltontextiles.com 참고: 정중앙 거대 → 스크롤 시 축소·좌측상단 이동·고정
   ═══════════════════════════════════════════════════════════ */
.fixed-logo {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 50;
  pointer-events: none;
  will-change: transform, opacity;
  text-align: center;
  transform-origin: top left; /* 축소 및 이동 시 기준점을 고정하여 구석 안착 보정 */
}



.fixed-logo.is-shrunk {
  /* 완전히 축소된 후 상단 좌측에 고정된 상태 */
  pointer-events: auto;
}

.fixed-logo-text {
  display: inline-block;
  background-color: #6D2122;
  padding: 2rem 3rem; /* 여백 소폭 최적화 */
  font-family: 'Futura', 'Jost', 'Montserrat', sans-serif;
  font-size: clamp(2.4rem, 6vw, 5.5rem);
  font-weight: 500;
  letter-spacing: 0.18em;
  color: #F1EFE7;
  text-align: center;
  line-height: 1.1;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25);
  margin: 0;
  white-space: nowrap;
  transform-origin: top left; /* 원점을 좌측 상단으로 하여 정렬 일관성 확보 */
}

/* ═══════════════════════════════════════════════════════════
   Section 0: LANDING (Video & Logo Animation)
   ═══════════════════════════════════════════════════════════ */
.landing-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain; 
  z-index: 0;
}

#intro {
  background-color: #F9F8F6; /* 섹션 자체 배경색 통일 */
}

.landing-video-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0.05) 40%,
    rgba(0, 0, 0, 0.35) 100%
  );
  z-index: 1;
}

/* Scroll Hint */
.scroll-hint {
  position: absolute;
  bottom: 2.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 3;
  transition: opacity 0.3s ease;
}

.scroll-hint-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 8px;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.5);
}

.scroll-hint-line {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.25);
  animation: lineGrow 2s ease infinite alternate;
}

@keyframes lineGrow {
  from { transform: scaleY(0.4); opacity: 0.3; }
  to   { transform: scaleY(1);   opacity: 0.7; }
}

/* ═══════════════════════════════════════════════════════════
   Section 1: PHILOSOPHY (Overlapping Editorial Design)
   타이틀이 섹션 상단에 거대하게 걸쳐지며
   아래 본문과 레이어가 살짝 겹치는(Overlap) 에디토리얼
   ═══════════════════════════════════════════════════════════ */
.philosophy-section {
  background-color: #F9F8F6;
}

.philo-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  padding: 5rem 4rem 4rem;
  position: relative;
}

/* 개별 요소 fade-up 트랜지션 */
.philo-container .philo-title,
.philo-container .philo-body-block,
.philo-container .philo-services .philo-service-item {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.philo-container.is-visible .philo-title {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.1s;
}

.philo-container.is-visible .philo-body-block {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0.35s;
}

.philo-container.is-visible .philo-services .philo-service-item {
  opacity: 1;
  transform: translateY(0);
  /* 개별 딜레이는 인라인 스타일로 적용 */
}

/* 거대 오버래핑 타이틀 */
.philo-title {
  font-family: 'Playfair Display', 'Cormorant Garamond', serif;
  font-size: clamp(34px, 6vw, 68px);
  font-weight: 400;
  line-height: 1.25;
  color: #312E2D;
  letter-spacing: 0.01em;
  margin: 0 0 -2.5rem 0; /* 오버래핑: 아래 본문과 겹침 */
  word-break: keep-all;
  position: relative;
  z-index: 2;
}

.philo-accent {
  font-style: italic;
  font-family: 'Playfair Display', serif;
  color: #6D2122;
  font-weight: 500;
  letter-spacing: 0.04em;
}

/* 본문 블록 — 타이틀과 오버랩 */
.philo-body-block {
  position: relative;
  z-index: 1;
  padding-top: 4.5rem;
  max-width: 650px;
  margin-left: auto;
  margin-right: 5rem;
}

/* 눈썹 라벨 */
.philo-eyebrow {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}
.philo-eyebrow-line {
  display: block;
  width: 36px;
  height: 1px;
  background: #000;
}
.philo-eyebrow-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  font-weight: 400;
  letter-spacing: 0.48em;
  text-transform: uppercase;
  color: #000;
  margin: 0;
}

/* 본문 */
.philo-text {
  font-family: 'Pretendard', sans-serif;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.7; /* 1.6 - 1.8 권장 */
  color: #000;
  word-break: keep-all;
  overflow-wrap: break-word;
  margin: 0;
}

.philo-text:first-child {
  margin-bottom: 1.4rem; /* 문장 간 시각적 분리 */
}

/* 서비스 영역 — 무한 흐르는 텍스트 애니메이션 (Marquee) */
.philo-services-marquee {
  position: absolute;
  bottom: 2.5rem;
  left: 0;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
}

.philo-marquee-track {
  display: inline-flex;
  gap: 4rem;
  padding-left: 4rem;
  animation: marquee 25s linear infinite;
  will-change: transform;
}

@keyframes marquee {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-33.33333%); }
}

.philo-service-item {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 12px;
  font-weight: 300;
  color: rgba(0, 0, 0, 0.18);
  letter-spacing: 0.14em;
  white-space: nowrap;
  text-transform: capitalize;
}

/* 모바일 */
@media (max-width: 768px) {
  .philo-container {
    padding: 3.5rem 1.5rem 3rem;
  }
  .philo-title {
    font-size: 26px;
    margin-bottom: -1.2rem;
  }
  .philo-body-block {
    padding-top: 3rem;
    margin-right: auto;
    margin-left: auto;
    width: 90%;
    max-width: none;
  }
  .philo-text {
    font-size: 15px;
    line-height: 1.65;
  }
  .philo-services {
    bottom: 1.5rem;
    left: 1.5rem;
    right: 1.5rem;
    gap: 1.2rem;
    flex-wrap: wrap;
  }
  .philo-service-item {
    font-size: 10px;
  }
}

/* ═══════════════════════════════════════════════════════════
   Section 2: PORTFOLIO (비대칭 그리드, Shared Element Transition)
   rayphilly.place AMENITIES 섹션 참고
   사진 위 텍스트: 폰트 크기 줄이고 자간 넓혀 가독성 up
   ═══════════════════════════════════════════════════════════ */
.portfolio-section { background: #111; }

.portfolio-grid {
  display: grid;
  grid-template-columns: 55% 45%;
  height: 100%;
  gap: 3px;
}

.portfolio-right-col {
  display: grid;
  grid-template-rows: 62% 38%;
  gap: 3px;
}

.portfolio-small-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3px;
}

.portfolio-item {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.portfolio-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.9s cubic-bezier(0.76, 0, 0.24, 1);
  filter: brightness(0.8);
}

.portfolio-item:hover img {
  transform: scale(1.06);
  filter: brightness(0.55);
}

/* 호버 오버레이 — 폰트 크기 줄이고 자간 넓혀 가독성 */
.portfolio-hover-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

.portfolio-item:hover .portfolio-hover-overlay {
  opacity: 1;
}

.portfolio-hover-cat {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 400;
  font-style: italic;
  color: #FFF;
  letter-spacing: 0.05em;
  text-transform: capitalize;
  background: rgba(43, 29, 27, 0.7); /* 따뜻한 차콜브라운 오버레이 */
  padding: 12px 28px;
  border-radius: 2px;
  text-shadow: none;
}

/* Shared Element Transition 오버레이 */
.portfolio-expand-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: #000;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.portfolio-expand-overlay.is-entering {
  opacity: 1;
  pointer-events: auto;
}

.expand-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.08);
  transition: transform 1.2s cubic-bezier(0.76, 0, 0.24, 1);
  filter: brightness(0.6);
}

.portfolio-expand-overlay.is-entering .expand-img {
  transform: scale(1);
}

.expand-text-wrap {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  opacity: 0;
  animation: fadeIn 0.4s ease forwards;
  animation-delay: 0.2s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 모바일 */
@media (max-width: 768px) {
  .portfolio-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
  }
  .portfolio-right-col,
  .portfolio-small-row {
    display: contents;
  }
  
  /* 모바일에서도 PC와 동일하게 호버(터치) 시에만 보이도록 수정 */
  /* 첫 번째 터치로 .is-active 클래스가 붙으면 호버 효과 유지 */
  .portfolio-hover-overlay {
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  
  .portfolio-item:hover .portfolio-hover-overlay,
  .portfolio-item.is-active .portfolio-hover-overlay {
    opacity: 1;
    background: rgba(0, 0, 0, 0.4); 
  }
  
  .portfolio-hover-cat {
    font-size: 16px;
    letter-spacing: 0.12em;
    background: rgba(43, 29, 27, 0.85); /* PC와 동일한 네모 배경 유지 */
    padding: 8px 18px;
    border-radius: 2px;
  }

  .portfolio-item img {
    filter: brightness(0.8);
    transition: transform 0.8s ease;
  }

  .portfolio-item:hover img,
  .portfolio-item.is-active img {
    transform: scale(1.05);
    filter: brightness(0.6);
  }
}

/* ═══════════════════════════════════════════════════════════
   Section 3: SELECTION (Exhibition Archive — 공간 전시)
   좌측: 스타일링 공간 전체 샷 크게
   우측: 오브제들을 박물관 작품처럼 띄엄띄엄 여백 있게
   가격 대신 Enquire / View Detail 버튼만
   ═══════════════════════════════════════════════════════════ */
.selection-section {
  background-color: #F9F8F6;
}

.sel-exhibition {
  display: grid;
  grid-template-columns: 58% 42%;
  height: 100%;
}

/* 좌측: 공간 풀샷 */
.sel-main-visual {
  position: relative;
  overflow: hidden;
}

.sel-main-gallery {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.sel-main-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.sel-main-img.is-active {
  opacity: 1;
}



.sel-nav-group {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
  z-index: 10;
}

.sel-gallery-nav-bottom {
  display: flex;
  gap: 8px;
}

.sel-gallery-dot-small {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.4);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.sel-gallery-dot-small.active {
  background: white;
  border-color: white;
}

.sel-main-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3rem 3rem 4rem; /* 여백 조정 */
  background: linear-gradient(to top, rgba(0,0,0,0.55), transparent);
}

.sel-main-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(26px, 3.5vw, 44px);
  font-weight: 400;
  font-style: italic;
  color: #fff;
  margin: 0 0 0.3rem 0;
  letter-spacing: 0.03em;
}

.sel-main-subtitle {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  font-weight: 300;
  letter-spacing: 0.18em;
  color: rgba(255,255,255,0.55);
  margin: 0;
  text-transform: uppercase;
}

.sel-space-nav {
  display: flex;
  gap: 10px;
}

.sel-space-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.5);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.sel-space-dot.active {
  background: #6D2122;
  border-color: #6D2122;
  box-shadow: 0 0 0 3px rgba(139,0,0,0.3);
}

/* 우측: 오브제 갤러리 — 박물관 작품처럼 여백 넉넉히 */
.sel-objects {
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 상단부터 시작하여 잘림 방지 */
  gap: 4.5rem;          /* 띄엄띄엄 가독성 확장 */
  padding: 6rem 3rem;
  overflow-y: auto;
  /* Allow space for shadows/hover effects so products aren't cut off at the top */
  padding-top: 8rem;
  padding-bottom: 8rem;
}

.sel-objects::-webkit-scrollbar { display: none; }
.sel-objects { scrollbar-width: none; }

.sel-object-card {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.sel-object-img-wrap {
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: #F0EEEB;
}

.sel-object-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s ease;
  filter: brightness(0.95);
}

.sel-object-card:hover .sel-object-img-wrap img {
  transform: scale(1.04);
}

.sel-object-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 15px;
  font-weight: 400;
  font-style: italic;
  color: #444;
  letter-spacing: 0.05em;
  margin: 0;
}

.sel-object-cta {
  font-family: 'Montserrat', sans-serif;
  font-size: 8px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #6D2122;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  position: relative;
  display: inline-block;
  width: fit-content;
  transition: color 0.3s ease;
}

.sel-object-cta::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background: #6D2122;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.sel-object-cta:hover::after {
  transform: scaleX(1);
}

/* 모바일 */
@media (max-width: 768px) {
  .sel-exhibition {
    grid-template-columns: 1fr;
    grid-template-rows: 52% 48%;
  }
  .sel-objects {
    padding: 2rem 0; /* 상하 여백만 부여 */
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
    gap: 1.5rem;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    align-items: flex-start;
    /* 좌우 끝 여백 확보를 위한 가상 요소 */
    display: flex;
  }
  .sel-objects::before,
  .sel-objects::after {
    content: '';
    flex-shrink: 0;
    width: 1.5rem; /* 좌우 끝 보존 여백 */
  }
  .sel-objects::-webkit-scrollbar { display: none; }
  
  .sel-object-card {
    width: 70vw;
    flex-shrink: 0;
    scroll-snap-align: center; /* 중앙 스냅으로 시인성 확보 */
    gap: 0.6rem;
  }
  
  .sel-object-img-wrap {
    aspect-ratio: 4 / 3;
    width: 100%;
  }

  .sel-object-name {
    font-size: 14px;
    word-break: keep-all;
  }

  .sel-main-overlay {
    padding: 1.5rem;
  }
}

/* ═══════════════════════════════════════════════════════════
   Section 4: CONTACT (Minimalist Finish)
   ═══════════════════════════════════════════════════════════ */
.contact-section {
  background-color: #F9F8F6; /* 타 섹션과 통일 */
}

.contact-wrapper {
  display: block;
  height: 100%;
  position: relative;
  padding: 0;
}

/* 에디토리얼 스플릿 레이아웃: 화면 높이를 꽉 채우는 비대칭 그리드 */
.contact-layout-split {
  display: grid;
  grid-template-columns: 45% 55%;
  height: 100%;
  width: 100%;
  margin: 0;
}

/* 좌측 이미지 */
.contact-image-wrap {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.contact-building-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.contact-image-wrap:hover .contact-building-img {
  transform: scale(1.03);
}

/* 우측 정보 텍스트 */
.contact-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  padding: 0 4rem;
}

/* "Private Consultation." — 딥 버건디 */
.contact-title {
  font-family: 'Playfair Display', 'Cormorant Garamond', serif;
  font-size: clamp(34px, 5vw, 56px);
  font-weight: 400;
  font-style: italic;
  color: #6D2122;
  line-height: 1.1;
  letter-spacing: 0.01em;
  margin: 0 0 2rem 0;
}

/* 정보 영역 */
.contact-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 3.5rem;
}

.contact-address, 
.contact-phone {
  font-family: 'Pretendard', sans-serif;
  font-size: 15px; /* 가독성 확보를 위해 크기 상향 */
  font-weight: 400;
  color: #000;
  margin: 0;
  letter-spacing: 0.03em;
  white-space: nowrap; /* 주소 한 줄 유지 */
}

.contact-phone-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 카카오톡 아이콘 */
.contact-kakao-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #FEE500;
  color: #3A2929;
  text-decoration: none;
  transition: transform 0.3s ease, filter 0.3s ease;
}

.contact-kakao-icon:hover {
  transform: translateY(-2px);
  filter: brightness(0.95);
}

.contact-kakao-icon .kakao-svg {
  width: 18px;
  height: 18px;
}

/* 액션 버튼 */
.contact-actions {
  display: flex;
  justify-content: center;
}

.btn-booking {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1.2rem 3rem;
  background-color: #6D2122;
  color: #fff;
  font-family: 'Pretendard', sans-serif;
  font-size: 15px;
  font-weight: 400;
  letter-spacing: 0.05em;
  text-decoration: none;
  transition: background-color 0.4s ease, transform 0.4s ease;
}

.btn-booking:hover {
  background-color: #6a0000;
  transform: translateY(-2px);
}

/* 하단 사업자 정보 및 카피라이트 */
.contact-footer {
  position: absolute;
  bottom: 2rem;
  left: 45%;
  width: 55%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.business-info {
  font-family: 'Pretendard', sans-serif;
  font-size: 11px;
  line-height: 1.6;
  color: #888;
  text-align: center;
  margin: 0;
  letter-spacing: -0.01em;
}

.contact-copyright {
  font-family: 'Montserrat', sans-serif;
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #AAA;
  margin: 0;
}

/* 모바일 */
@media (max-width: 768px) {
  .landing-image {
    width: 90%;
    height: 70%;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%);
    object-fit: contain; /* 잘림 없이 전체 모습 유지 */
    /* 가구가 돋보이도록 중앙에 에디토리얼 박스처럼 배치 */
  }
  .fixed-logo {
    --target-y: calc(1.2rem + 18px); /* 햄버거 메뉴 모바일 세로 중앙 */
  }
  .fixed-logo-text {
    font-size: 2.5rem;
    padding: 1.5rem 2rem;
  }
  .contact-layout-split {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .contact-image-wrap {
    width: 100%;
    height: 45vh;
  }
  .contact-inner {
    height: auto;
    padding: 2.5rem 1rem; /* 좌우 패딩 축소하여 텍스트 공간 확보 */
  }
  .contact-footer {
    left: 0;
    width: 100%;
    bottom: 1rem;
  }
  .contact-title { 
    font-size: 28px; 
    margin-bottom: 1.2rem;
  }
  .btn-booking {
    padding: 1rem 2.5rem;
    font-size: 14px;
  }
  .business-info {
    font-size: 10px;
    line-height: 1.5;
    word-break: keep-all;
  }
  .contact-info {
    gap: 0.8rem;
  }
  .contact-address, 
  .contact-phone {
    font-size: clamp(10.5px, 3.1vw, 13px); /* 모바일에서도 가독성 있는 최소 크기 유지 */
  }
  .contact-kakao-icon {
    width: 26px;
    height: 26px;
  }
  .contact-kakao-icon .kakao-svg {
    width: 14px;
    height: 14px;
  }
}
</style>
