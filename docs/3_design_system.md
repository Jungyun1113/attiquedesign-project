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
- `--color-burgundy`: `#8B0000` (딥 버건디 — 브랜드 핵심 포인트)
- `--color-burgundy-dark`: `#6B0000` (호버 시 더 깊은 버건디)
- `--color-background`: `#FDFBF8` (전체 배경 — 따뜻한 아이보리)
- `--color-surface`: `#F9F8F6` (섹션 배경 — 톤다운 베이지)
- `--color-border`: `#E8E2D7` (은은한 구분선)
- `--color-overlay`: `#8B0000` (풀스크린 오버레이 메뉴 배경)
- `--color-cream`: `#F5E6D3` (오버레이 메뉴 호버 텍스트)

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

### 3.1. 삭제/폐지된 컴포넌트
- ~~`VerticalSideNav.vue`~~: 기존 우측 세로 네비 → **삭제**. 햄버거 메뉴 오버레이로 대체.

### 3.2. 신규 컴포넌트

#### `HamburgerMenu.vue` (Navigation)
우측 상단 고정 햄버거 메뉴 버튼 + 풀스크린 오버레이 네비게이션.
- **버튼 디자인:** 극도로 얇은 선 2줄 (높이 1px, 너비 28px, 간격 6px).
- **배경 적응:** 어두운 섹션에서는 흰색, 밝은 섹션에서는 검정.
- **클릭 시:** X자 모프 + `#8B0000` 배경 풀스크린 오버레이.
- **메뉴 링크:** 거대한 타이포그래피 (Playfair Display, 48~72px).
- **호버 효과:** 텍스트 컬러 크림 전환 + `translateX(8px)` 미세 이동.

#### `ScrollDrivenLogo.vue` (Section 0 전용)
랜딩 섹션의 스크롤 드리븐 로고 애니메이션.
- **초기 상태:** 화면 정중앙, `font-size: 7rem`, `letter-spacing: 0.22em`.
- **스크롤 시:** 점진적으로 크기 축소(`scale`) + 상단 좌측으로 위치 이동 + Sticky 고정.
- **구현:** Scroll 이벤트 → `scrollProgress` (0~1) 계산 → `transform` 인터폴레이션.

#### `ScrollSnapContainer.vue` (Layout — 기존 유지, 강화)
전체 원페이지를 감싸는 최상위 스크롤 스냅 컨테이너.
- **추가:** `scroll-behavior: smooth` 기본 적용.
- **추가:** ease-in-out 가속도 커브 적용.

#### `FullScreenSection.vue` (Layout — 기존 유지)
변경 없음. `height: 100vh`, `scroll-snap-align: start`.

### 3.3. 기존 유지 컴포넌트 (Atoms)
- `BaseButton.vue`, `BaseInput.vue` 유지.

### 3.4. 기존 유지 컴포넌트 (Molecules)
- `FormItem.vue`, `ProductCard.vue` 유지.

### 3.5. 기존 유지 컴포넌트 (Organisms)
- `DynamicReservationForm.vue`, `ToastContainer.vue` 유지.

---

## 4. 컴포넌트 계층 구조 (Component Hierarchy)

```text
App.vue
├── [랜딩 페이지 "/" 라우트]
│   ├── LandingLayout.vue
│   │   ├── HamburgerMenu.vue              ← 햄버거 메뉴 + 풀스크린 오버레이
│   │   └── ScrollSnapContainer.vue        ← 스크롤 스냅 최상위 래퍼
│   │       ├── FullScreenSection#intro    ← Section 0: Landing
│   │       │   ├── <video> (배경 비디오)
│   │       │   └── ScrollDrivenLogo.vue   ← 스크롤 드리븐 로고
│   │       ├── FullScreenSection#philosophy ← Section 1: Philosophy
│   │       │   └── (Overlapping Editorial Layout)
│   │       ├── FullScreenSection#portfolio  ← Section 2: Portfolio
│   │       │   └── (비대칭 그리드 + Shared Element Transition)
│   │       ├── FullScreenSection#selection  ← Section 3: Selection
│   │       │   └── (좌: 공간 갤러리 최대 3장 / 우: 오브제 스크롤 전시)
│   │       └── FullScreenSection#contact    ← Section 4: Contact
│   │           ├── (미니멀 타이포그래피)
│   │           ├── (네이버 예약 링크)
│   │           ├── (카카오톡 채널 링크)
│   │           └── (Footer 통합)
│
├── [별도 라우트 — 기존 레이아웃 유지]
│   ├── DefaultLayout.vue (간소화된 헤더 + Footer)
│   │   ├── /products         → PLP
│   │   ├── /products/:id     → PDP
│   │   ├── /portfolio/:id    → 포트폴리오 상세
│   │   ├── /selection/:id    → 셀렉션 상세
│   │   ├── /cart              → 장바구니
│   │   ├── /login             → 로그인
│   │   ├── /mypage            → 마이페이지
│   │   └── /reservation       → 전체 예약 폼
│   └── AdminLayout.vue
│       └── /admin/*           → 관리자 백오피스
│
└── ToastContainer.vue                    ← 전역 알림
```

---

## 5. 섹션별 임시 미디어(Placeholder) 정책

> 현재 단계에서는 전체 레이아웃과 애니메이션 뼈대를 잡는 것이 목적.

- **Section 0 배경 영상:** 아띠끄 무드에 어울리는 Placeholder 비디오 (Pexels 등).
- **Section 2·3 사진:** 하이엔드 무드(어두운 원목, 버건디 포인트, 미니멀 공간)에 어울리는 고화질 더미 이미지.
- **구조 확정 후 실제 에셋으로 교체 예정.**
