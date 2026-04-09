# API Specification (AWS Chalice)

## 1. 공통 응답 구조 (Standard Response Format)
프론트엔드에서 일관된 처리를 위해 모든 API는 아래 포맷을 준수한다.

### 성공 응답
- `success`: boolean (true)
- `data`: object | array (실제 페이로드)
- `meta`: object (페이징 정보 등 - `page`, `size`, `total_pages`, `total_count` 등)

### 실패(에러) 응답
- `success`: boolean (false)
- `error`: object
  - `code`: string (예: 'VALIDATION_FAILED', 'UNAUTHORIZED', 'PRODUCT_NOT_FOUND')
  - `message`: string (사용자 노출용 에러 메시지)

## 2. 권한 및 인증
- JWT 기반 인증 (Bearer Token)
- 비회원 허용 엔드포인트는 Token 검증을 Pass 하되 Request payload의 guest 정보를 참조함.

## 3. 도메인별 API 명세

### 3.1. Auth (/api/v1/auth)
- `POST /login`: 로그인 (이메일/비밀번호 OR 소셜 토큰) -> 응답: AccessToken, RefreshToken
- `POST /register`: 회원가입

### 3.2. Products (/api/v1/products)
- `GET /`: 상품 목록 조회
  - Query Params: `page`, `limit`, `type`, `category_id`, `sort` (price_asc, price_desc, latest)
  - Response: `{ meta: { ...pagination }, data: [ ...product_list ] }`
- `GET /{id}`: 상품 상세 조회
- `POST /` (Admin Only): 상품 등록
- `PATCH /{id}` (Admin Only): 상품 상태/정보 수정

### 3.3. Orders (/api/v1/orders)
- `POST /`: 주문 생성 (PG 결제 전 가주문 ID 발급 로직 연동)
  - Payload: `{ items: [], guest_info?: {} }`
- `GET /me`: 내 주문 목록 조회 (회원 커서/페이지 기반)
- `GET /{order_id}`: 비회원/회원 공통 주문 상세 조회 (비회원은 조회 권한용 비밀번호/인증 토큰 동반 필요)

### 3.4. Reservations (/api/v1/reservations)
- `POST /`: 상담/방문 예약 접수 (Dynamic Form)
  - Payload: `{ type: string, expected_date: string, guest_info?: {}, dynamic_data: { address: '', budget: '', space_type: '' } }`
- `GET /`: 예약 관리 목록 조회 (Admin Only, CRM 칸반용 데이터)
- `PATCH /{id}/status`: 예약 상태(상담진행, 계약완료 등) 변경 (Admin Only)

### 3.5. Webhooks (/api/v1/webhooks)
- `POST /payments`: 가상계좌 입금, 결제 성공/실패 통보 수신용 (포트원/토스 웹훅)

### 3.6. Portfolios (/api/v1/portfolios)
- `GET /`: 포트폴리오 목록 조회
- `GET /{id}`: 특정 포트폴리오 상세 조회

### 3.7. Selections (/api/v1/selections)
- `GET /`: 공간 전시 리스트 및 스타일링 샷(최대 3장), 소속 상품 목록 조회
- `GET /{selection_id}/products/{product_id}`: 단일 오브제 타겟 상세 조회
