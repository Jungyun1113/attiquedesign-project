# Design System v3.0 (Vanilla CSS & Vue3 — High-end Editorial Magazine)

> **v3.0 핵심 변경:** 에디토리얼 매거진 스타일로 전면 전환.
> - 기존 VerticalSideNav **폐지** → HamburgerMenu + FullscreenOverlayNav 신규 추가.
> - 스크롤 드리븐 로고 애니메이션 (ScrollDrivenLogo) 신규 추가.
> - 오버래핑 타이포그래피 및 Exhibition Archive 레이아웃 시스템 도입.

---

## 1. 설계 철학
- **Editorial Magazine Aesthetic:** 인쇄 매거진을 넘기는 듯한 동적 레이아웃. 텍스트 오버래핑, 비대칭 그리드, 과감한 여백.
- **Scroll-driven Interaction:** 스크롤에 반응하는 로고 축소·고정, 섹션 전환 ease-in-out 가속도.
- **Deep Burgundy Identity:** `#8B0000`을 브랜드 포인트로, 풀스크린 오버레이 메뉴, CTA 호버 등 전반에 적용.
- **Minimal Commerce Feel:** 가격 노출 최소화, Enquire/View Detail로 쇼룸 방문 유도.

---

## 2. Design Tokens

### 2.1. Colors
- `--color-primary`: `#2B1D1B` (메인 텍스트 — 따뜻한 차콜브라운)
- `--color-secondary`: `#6D6059` (서브 텍스트, 비활성)
- `--color-burgundy`: `#953735` (브랜드 핵심 포인트 버건디 — 구현 적용값)
- `--color-burgundy-dark`: `#953735` (호버 상태 — 현재 동일값 적용, 추후 분리 예정)
- `--color-background`: `#F5F0E8` (전체 배경 — 크림. 사이트 전역 통일)
- `--color-surface`: `#F5F0E8` (섹션 배경 — 배경과 통일)
- `--color-border`: `#E8E2D7` (은은한 구분선)
- `--color-overlay`: `#953735` (오버레이/강조 배경)
- `--color-cream`: `#F5E6D3` (보조 크림 텍스트)

> **[원안 대비 변경]** 기존 딥 버건디 `#8B0000` 대신 `#953735`(밝은 버건디/갈색 계열)를 전체 구현에 적용. `index.css` 및 모든 컴포넌트 스타일 일치.

### 2.2. Typography
| 용도 | 폰트 | 비고 |
|------|-------|------|
| 브랜드 로고 | `'Raleway'`, sans-serif | 초경량(200), 넓은 자간 |
| 영문 헤드라인 | `'Playfair Display'`, serif | Italic 강조, 에디토리얼 감성 |
| 영문 캐치프레이즈 | `'Cormorant Garamond'`, serif | 얇은 세리프, 필기체 |
| 네비게이션 라벨 | `'Montserrat'`, sans-serif | 극소형, 넓은 자간 |
| 한글 본문 | `'Pretendard'`, sans-serif | 가독성 최적화 |
| 한글 한정 세리프 | `'Nanum Myeongjo'`, serif | 에디토리얼 보조 |

- 스케일: `12px(xs)` ~ `96px(mega)`. 모바일 대응 `clamp()` 함수 적극 반영.

### 2.3. Spacing & Layout
- 여백 중심 설계. 풀스크린 섹션 (`100vh`).
- 스크롤바 전역 숨김.
- 에디토리얼 오버래핑: 타이틀이 본문 영역과 `margin-top: -2rem ~ -4rem` 겹침.

### 2.4. Animation & Easing
- **섹션 전환:** `ease-in-out` 가속도.
- **로고 축소:** `transition: transform 0.1s linear` (스크롤 연동이므로 즉각 반응).
- **메뉴 오버레이:** `transition: opacity 0.5s ease, transform 0.5s ease`.
- **Shared Element Transition:** `cubic-bezier(0.76, 0, 0.24, 1)` 850ms.
- **마이크로 애니메이션:** `ease-out 0.4s~0.7s` (호버, 페이드인).

---

## 3. Core Components (Vue Component 레벨)

### 3.1. 삭제/폐지된 컴포넌트 (v4.0 기준)
- ~~`VerticalSideNav.vue`~~: 기존 우측 세로 네비 → **삭제**.
- ~~`HamburgerMenu.vue`~~: 풀스크린 오버레이 네비 → **삭제**. GlobalHeader로 대체.
- ~~`ScrollDrivenLogo.vue`~~: 스크롤 드리븐 로고 애니메이션 → **삭제**.
- ~~`ScrollSnapContainer.vue`~~: 원페이지 스크롤 스냅 컨테이너 → **삭제**.
- ~~`FullScreenSection.vue`~~: 100vh 섹션 래퍼 → **삭제**.
- ~~`LandingLayout.vue`~~: 랜딩 전용 레이아웃 → **삭제**. DefaultLayout으로 통합.

### 3.2. 핵심 컴포넌트

#### `GlobalHeader.vue` (Navigation — v4.0 신규)
상단 고정(`position: sticky`) 글로벌 헤더.
- **로고:** 헤더 정중앙 배치. `/logo.svg` 사용. 스크롤 시 `scale(0.65)` 축소 + transition.
- **GNB:** 로고 아래 수평 나열. Philosophy / Interior / Selection / Portfolio / Contact.
- **폰트:** Raleway, 11px, letter-spacing 0.3em, uppercase.
- **Active 조건:** Selection은 `?view=grid` 쿼리일 때만 활성화. 나머지는 경로 prefix 매칭.
- **스크롤 반응:** `scrollY > 20`이면 `.is-scrolled` 클래스 → padding 축소 + 미세 shadow.

#### `DefaultLayout.vue` (Layout)
모든 서비스 페이지 공통 레이아웃. GlobalHeader + `<router-view>` + Footer 포함.
- **Footer:** 버건디(`#953735`) 배경. 브랜드 로고, Contact 정보, Social 링크, 사업자 정보, 저작권 표기.

### 3.3. 기존 유지 컴포넌트 (Atoms)
- `BaseButton.vue`, `BaseInput.vue` 유지.

### 3.4. 기존 유지 컴포넌트 (Molecules)
- `FormItem.vue`, `ProductCard.vue` 유지.

### 3.5. 기존 유지 컴포넌트 (Organisms)
- `DynamicReservationForm.vue`, `ToastContainer.vue` 유지.

---

## 4. 컴포넌트 계층 구조 (Component Hierarchy — v4.0 구현 기준)

```text
App.vue
└── DefaultLayout.vue                     ← 모든 서비스 페이지 공통 레이아웃
    ├── GlobalHeader.vue                  ← 중앙 로고 + GNB (sticky)
    ├── <router-view>
    │   ├── /           → redirect /selection?view=hero
    │   ├── /selection  → SelectionView.vue
    │   │   ├── Hero View   (?view=hero)  ← 히어로 슬라이더 + 브랜드텍스트 + 오브제 슬라이더
    │   │   └── Grid View   (?view=grid)  ← 3열 그리드 아카이브
    │   ├── /philosophy → PhilosophyView.vue (오버래핑 에디토리얼)
    │   ├── /interior   → InteriorView.vue  (프로세스 3단 + 예약 CTA)
    │   ├── /portfolio  → PortfolioView.vue (탭 카테고리 + 세로 프로젝트 목록)
    │   ├── /contact    → ContactView.vue   (스플릿 레이아웃 + 카카오/네이버)
    │   ├── /portfolio/:id → PortfolioDetailView.vue
    │   ├── /selection/:id → SelectionDetailView.vue
    │   ├── /products      → ProductListView.vue
    │   ├── /products/:id  → ProductDetailView.vue
    │   ├── /login / /register / /mypage / /cart / /reservation
    │   └── /notice / /showroom / /brand
    └── Footer (DefaultLayout 내 포함)    ← 사업자 정보 + 저작권

AdminLayout.vue
└── /admin/* → DashboardView.vue
```

---

## 5. 섹션별 임시 미디어(Placeholder) 정책

> 현재 단계에서는 전체 레이아웃과 애니메이션 뼈대를 잡는 것이 목적.

- **Section 0 배경 영상:** 아띠끄 무드에 어울리는 Placeholder 비디오 (Pexels 등).
- **Section 2·3 사진:** 하이엔드 무드(어두운 원목, 버건디 포인트, 미니멀 공간)에 어울리는 고화질 더미 이미지.
- **구조 확정 후 실제 에셋으로 교체 예정.**
