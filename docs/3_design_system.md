# Design System (TailwindCSS Ver3 & Vue3)

## 1. 설계 철학
- **High-end & Minimal:** Casa Alexis 벤치마킹. 불필요한 테두리 및 그림자 배제, Full-bleed 이미지와 과감한 여백 사용.
- **Tokenized Tailwind:** Tailwind `tailwind.config.js` 확장을 통해 서비스 고유 컬러/타이포그래피 토큰화.

## 2. Design Tokens (tailwind.config.js 설정)
### 2.1. Colors
- `primary`: `#1A1A1A` (거의 블랙에 가까운 짙은 차콜 - High-end 무드 핵심)
- `secondary`: `#737373` (보조 텍스트, 비활성 아이콘)
- `accent`: `#8C7A6B` (하이엔드 가구 무드의 웜톤/브론즈 계열 포인트 컬러)
- `background`: `#FFFFFF` (순백색 배경으로 컨텐츠 대비 극대화)
- `surface`: `#F5F5F7` (아주 옅은 쿨톤 그레이 - 입력 폼 배경 등에 사용)

### 2.2. Typography
- `font-sans`: 'Pretendard', 'Inter', sans-serif (UI/본문용, 깔끔한 가독성)
- `font-serif`: 'Playfair Display', 'Nanum Myeongjo', serif (브랜드 스토리, 헤드라인 강조용)
- 스케일: `text-xs`(12px) ~ `text-7xl`(72px) 배치. 모바일 대응을 위해 responsive font size(예: `md:text-5xl`) 적극 반영.

### 2.3. Spacing & Layout
- 여백 중심 설계: 기본 컨테이너 패딩은 모바일 `px-4`, PC `px-12` 적용.
- 섹션 간 간격: `py-24` ~ `py-32`를 적극 사용하여 숨통이 트이는 하이엔드 갤러리 레이아웃 구축.

## 3. Core Components (Vue Component 레벨)
### 3.1. Atoms
- `BaseButton.vue`: `variant="solid|outline|ghost"`, 상태(hover/disabled)에 따른 은은한 transition(`duration-300 ease-out`).
- `BaseInput.vue`: 에러 상태 연동 (`v-model:modelValue`, `error` prop).

### 3.2. Molecules
- `FormItem.vue`: 라벨 + 입력 필드 + 에러 메시지를 감싸는 공통 래퍼 컴포넌트.
- `ProductCard.vue`: '품절', '단 1개' 등 condition 뱃지 및 Hover 시 이미지 교체 기능 포함.

### 3.3. Organisms
- `DynamicReservationForm.vue`: v-if를 활용한 조건부 렌더링 폼.
- `StickyHeader.vue`: `translate-y`와 `background-opacity` transition을 혼합한 스크롤 반응형 헤더.
- `ToastContainer.vue` & `useToast`: API의 공통 에러 메시지(Standard Response 참고)를 수신받아 우측 하단에 알림을 띄우는 시스템.
