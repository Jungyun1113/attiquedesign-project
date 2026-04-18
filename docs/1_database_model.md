# Database Model (AWS RDS PostgreSQL & SQLModel)

## 1. 설계 원칙
- **표준화:** 모든 테이블에 공통 Base 필드 (id, created_at, updated_at, is_deleted) 적용, Soft Delete 구현.
- **모듈화:** 도메인별(인증, 상품, 주문, 예약) 테이블 분리.
- **Cascade 원칙:** 자식 레코드는 부모 삭제 시 CASCADE DELETE. 비즈니스 데이터 보존이 필요한 FK(주문↔상품 등)는 RESTRICT 또는 SET NULL 적용.

## 2. 공통 Base Model
- `id`: UUID (Primary Key)
- `created_at`: TIMESTAMP (Default: now)
- `updated_at`: TIMESTAMP (Auto update)
- `is_deleted`: BOOLEAN (Default: false)

## 3. 핵심 테이블 명세

### 3.1. Users (사용자)
- `email`: VARCHAR (Unique)
- `password_hash`: VARCHAR (Nullable — 소셜 로그인)
- `name`: VARCHAR
- `phone`: VARCHAR
- `role`: ENUM ('ADMIN', 'USER')
- `auth_provider`: ENUM ('LOCAL', 'KAKAO', 'NAVER', 'APPLE')

### 3.2. Products (상품)
- `sku`: VARCHAR (Unique)
- `name`: VARCHAR
- `category`: VARCHAR (예: 'FURNITURE', 'ACCESSORY', 'LIGHTING' 등 — 별도 테이블 불필요)
- `price`: DECIMAL (Nullable — 고가 가구는 문의 전용)
- `stock_quantity`: INT
- `status`: ENUM ('ACTIVE', 'HIDDEN', 'SOLDOUT')
- `thumbnail_url`: VARCHAR (S3 객체 키)

### 3.3. Product_Images (상품 이미지)
- `product_id`: UUID (FK → Products, CASCADE DELETE)
- `image_url`: VARCHAR (S3 객체 키)
- `display_order`: INT
- `is_primary`: BOOLEAN

### 3.4. Orders (주문)
- `user_id`: UUID (FK → Users, SET NULL — 탈퇴 시 주문 보존)
- `guest_email`: VARCHAR (Nullable)
- `guest_phone`: VARCHAR (Nullable)
- `guest_name`: VARCHAR (Nullable)
- `total_amount`: DECIMAL
- `status`: ENUM ('PENDING', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED')
- `pg_transaction_id`: VARCHAR

### 3.5. Order_Items (주문 상세)
- `order_id`: UUID (FK → Orders, CASCADE DELETE)
- `product_id`: UUID (FK → Products, RESTRICT — 주문된 상품 삭제 방지)
- `quantity`: INT
- `unit_price`: DECIMAL (주문 시점 가격 스냅샷)

### 3.6. Reservations (1:1 프라이빗 방문/상담 예약)
- `user_id`: UUID (FK → Users, SET NULL)
- `guest_info`: JSONB (비회원용 name, phone, email)
- `reservation_type`: ENUM ('INTERIOR', 'FURNITURE', 'TOTAL')
- `status`: ENUM ('RECEIVED', 'IN_PROGRESS', 'QUOTED', 'CONTRACTED', 'NOSHOW')
- `expected_date`: TIMESTAMP
- `dynamic_data`: JSONB (공간 형태, 평형대, 예산, 희망 브랜드 등 동적 폼 데이터)

### 3.7. Waitlists (재고 입고 알림)
- `product_id`: UUID (FK → Products, CASCADE DELETE)
- `user_id`: UUID (FK → Users, SET NULL)
- `contact_method`: VARCHAR (이메일 또는 전화번호)
- `status`: ENUM ('PENDING', 'NOTIFIED')

### 3.8. Portfolios (포트폴리오)
- `category`: VARCHAR (예: 'Residential', 'Commercial', 'Drama', 'Magazine')
- `title`: VARCHAR
- `description`: TEXT
- `cover_image_url`: VARCHAR (S3 객체 키)

### 3.9. Portfolio_Images (포트폴리오 이미지)
- `portfolio_id`: UUID (FK → Portfolios, CASCADE DELETE)
- `image_url`: VARCHAR (S3 객체 키)
- `display_order`: INT

### 3.10. Selections (공간 전시 아카이브)
- `title`: VARCHAR
- `subtitle`: VARCHAR
- `description`: TEXT

### 3.11. Selection_Images (공간 스타일링 샷, 최대 3장)
- `selection_id`: UUID (FK → Selections, CASCADE DELETE)
- `image_url`: VARCHAR (S3 객체 키)
- `display_order`: INT

### 3.12. Selection_Products (공간 내 전시 오브제)
- `selection_id`: UUID (FK → Selections, CASCADE DELETE)
- `product_id`: UUID (FK → Products, RESTRICT)
- `display_order`: INT
