# Frontend Architecture (Vue3 + Vite + TypeScript)

## 1. 구조 설계 원칙
- **상태 최적화:** Pinia를 이용한 권한(Auth) 및 장바구니/옵션(Cart) 전역 상태 관리.
- **HTTP 클라이언트 모듈화:** Axios Interceptor를 통해 모든 API 응답의 규격 대응, 에러 발생 시 UI(Toast Notification) 계층으로 일원화된 전달.
- **코드 스플리팅:** Vue Router 단위 비동기 로드(`() => import(...)`) 및 컴포넌트 Lazy Loading 적극 활용.

## 2. 디렉토리 구조
```text
/frontend
├── index.html              # Open Graph 및 SEO 메타 태그 대응 공간
├── vite.config.ts          # Vite 설정 (sitemap, alias 등)
├── tailwind.config.js      # Design Token화 설정
├── src/
│   ├── main.ts             # App 엔트리, Pinia 및 Router 인젝션
│   ├── router/             # Vue Router (가드 적용: Admin, Auth)
│   │   └── index.ts
│   ├── store/              # Pinia Stores (auth, cart)
│   ├── services/           # API 클라이언트 계층
│   │   ├── api.ts          # Axios 인스턴스, Request/Response Interceptor
│   │   ├── product.service.ts
│   │   └── auth.service.ts
│   ├── composables/        # 공통 Composition API 훅스
│   │   ├── useAuth.ts      # 로그인, 토큰 관리 로직 캡슐화
│   │   ├── useToast.ts     # 시스템 알림 로직
│   │   └── usePagination.ts
│   ├── views/              # Page 레벨 컴포넌트
│   │   ├── HomeView.vue
│   │   ├── products/
│   │   └── admin/          # 백오피스(권한 제어용) 라우트 뷰
│   ├── layouts/            # 전체 프레임 (GNB, Footer 등)
│   │   ├── DefaultLayout.vue
│   │   └── AdminLayout.vue
│   ├── components/         # 원자/분자 단위 UI (Design System 대응)
│   │   ├── common/         # BaseButton, BaseInput 등
│   │   └── domain/         # ProductCard, DynamicReservationForm 등
│   ├── types/              # TS Interface (API Response/Request 스키마 대응)
│   │   └── api.d.ts
│   └── assets/             # CSS (index.css), 이미지 소스
```

## 3. 역방향 검토에 따른 보완 요소 (API/Backend 연계 고려)
- **표준 에러 처리 결합:** `services/api.ts`의 Response Interceptor에서 API Spec의 `{ success, error, meta }` 구조를 판별함.
  - `success: false` 감지 시, 전역 `useToast().showError(response.data.error.message)`를 호출해 일관된 UI 피드백을 주력으로 설계.
  - 이를 통해 각 개별 Component 개발 시 무분별한 `try-catch` 및 중복된 에러 표시 처리를 배제하여 유지보수성 극대화.
- **비회원 상태 유지:** 회원가입/비회원 로직의 엣지 케이스를 커버하기 위해 Pinia 내 `auth` store 뿐 아니라 비회원 임시 세션키나 guest 정보(Email 등)를 `localStorage`를 통해 Persistence하게 처리하는 구조 명시.
- **동적 폼 컴포넌트:** `DynamicReservationForm.vue`는 내부적으로 formData 객체를 유연성 있게 관리하되, 전송 시에는 백엔드 API 명세에 맞춰 `dynamic_data` 필드로 묶어(Packing) 전달하는 Facade 로직 반영.
