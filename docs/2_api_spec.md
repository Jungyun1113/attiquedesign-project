# API Specification (AWS Chalice)

## 1. 공통 응답 구조
모든 API는 아래 포맷을 준수한다.

### 성공 응답
- `success`: true
- `data`: 실제 페이로드 (object | array)
- `meta`: 페이징 정보 등 (`page`, `size`, `total_pages`, `total_count`)

### 실패 응답
- `success`: false
- `error.code`: string (예: `VALIDATION_FAILED`, `UNAUTHORIZED`, `NOT_FOUND`)
- `error.message`: string (사용자 노출용)

## 2. 권한 및 인증
- JWT Bearer Token 기반. 데코레이터(`@require_auth`, `@require_admin`)로 라우트에 선언적 적용.
- 비회원 허용 엔드포인트는 토큰 없이도 접근 가능하며, payload의 `guest_info`를 참조.

## 3. 도메인별 API 명세

### 3.1. Auth (`/auth`)
- `POST /auth/login`: 로그인 → AccessToken, RefreshToken 반환
- `POST /auth/register`: 회원가입

### 3.2. Products (`/products`)
- `GET /products`: 상품 목록 (Query: `page`, `limit`, `category`, `sort`)
- `GET /products/{id}`: 상품 상세
- `POST /products` (Admin): 상품 등록
- `PATCH /products/{id}` (Admin): 상품 수정

### 3.3. Orders (`/orders`)
- `POST /orders`: 주문 생성 (PG 결제 전 가주문 ID 발급 포함)
- `GET /orders/me`: 내 주문 목록 (회원 전용)
- `GET /orders/{id}`: 주문 상세 (비회원은 guest 인증 토큰 필요)

### 3.4. Reservations (`/reservations`)
- `POST /reservations`: 상담/방문 예약 접수 (Dynamic Form)
- `GET /reservations` (Admin): 예약 목록 (CRM 칸반용)
- `PATCH /reservations/{id}/status` (Admin): 예약 상태 변경

### 3.5. Webhooks (`/webhooks`)
- `POST /webhooks/payments`: 포트원/토스 결제 웹훅 수신

### 3.6. Portfolios (`/portfolios`)
- `GET /portfolios`: 목록 조회
- `GET /portfolios/{id}`: 상세 조회

### 3.7. Selections (`/selections`)
- `GET /selections`: 공간 전시 리스트 (스타일링 샷 + 소속 상품 포함)
- `GET /selections/{id}/products/{product_id}`: 단일 오브제 상세

### 3.8. Storage (`/uploads`) — S3 Presigned URL
관리자가 이미지를 S3에 직접 업로드하기 위해 Presigned URL 방식을 사용한다.
서버는 서명된 URL만 발급하며, 실제 파일 전송은 클라이언트↔S3 간 직접 수행된다.

- `POST /uploads/presign` (Admin): Presigned PUT URL 발급
  - Payload: `{ filename: string, content_type: string, target: string }` (`target`: `products`, `portfolios`, `selections` 등)
  - Response: `{ upload_url: string, object_key: string }`
  - 업로드 완료 후 클라이언트가 `object_key`를 해당 모델의 URL 필드에 저장 요청
