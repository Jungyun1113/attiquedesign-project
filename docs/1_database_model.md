# Database Model (AWS RDS PostgreSQL & SQLModel)

## 1. 설계 원칙
- **확장성:** 비회원/회원 확장, 동적 폼 데이터를 수용할 수 있는 JSONB 활용.
- **표준화:** 모든 테이블에 공통 Base 필드 (id, created_at, updated_at, is_deleted) 적용하여 Soft Delete 구현.
- **모듈화:** 도메인별(인증, 상품, 주문, 예약) 테이블 분리.

## 2. 공통 Base Model
- `id`: UUID (Primary Key)
- `created_at`: TIMESTAMP (Default: now)
- `updated_at`: TIMESTAMP (Auto update)
- `is_deleted`: BOOLEAN (Default: false)

## 3. 핵심 테이블 명세
### 3.1. Users (사용자)
- `email`: VARCHAR (Unique)
- `password_hash`: VARCHAR (Nullable for Social Login)
- `name`: VARCHAR
- `phone`: VARCHAR
- `role`: ENUM ('ADMIN', 'USER')
- `auth_provider`: ENUM ('LOCAL', 'KAKAO', 'NAVER', 'APPLE')

### 3.2. Products (상품)
- `sku`: VARCHAR (Unique)
- `name`: VARCHAR
- `type`: ENUM ('FURNITURE', 'ACCESSORY')
- `price`: DECIMAL (Nullable for high-end furniture requiring inquiry)
- `stock_quantity`: INT
- `status`: ENUM ('ACTIVE', 'HIDDEN', 'SOLDOUT')
- `category_id`: UUID (Foreign Key)
- `thumbnail_url`: VARCHAR

### 3.3. Product_Images (상품 이미지)
- `product_id`: UUID (Foreign Key)
- `image_url`: VARCHAR
- `display_order`: INT
- `is_primary`: BOOLEAN

### 3.4. Orders (주문 - 소품 위주)
- `user_id`: UUID (Nullable for Guest)
- `guest_email`: VARCHAR (Nullable)
- `guest_phone`: VARCHAR (Nullable)
- `guest_name`: VARCHAR (Nullable)
- `total_amount`: DECIMAL
- `status`: ENUM ('PENDING', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED')
- `pg_transaction_id`: VARCHAR

### 3.5. Order_Items (주문 상세)
- `order_id`: UUID (Foreign Key)
- `product_id`: UUID (Foreign Key)
- `quantity`: INT
- `unit_price`: DECIMAL

### 3.6. Reservations (1:1 프라이빗 방문/상담 예약)
- `user_id`: UUID (Nullable for Guest)
- `guest_info`: JSONB (name, phone, email - for guest handling without strict column dependencies)
- `reservation_type`: ENUM ('INTERIOR', 'FURNITURE', 'TOTAL')
- `status`: ENUM ('RECEIVED', 'IN_PROGRESS', 'QUOTED', 'CONTRACTED', 'NOSHOW')
- `expected_date`: TIMESTAMP
- `dynamic_data`: JSONB (공간 형태, 평형대, 예산, 희망 브랜드 등 프론트의 동적 폼 데이터를 유연하게 수용)

### 3.7. Waitlists (재고 입고 알림)
- `product_id`: UUID (Foreign Key)
- `user_id`: UUID (Nullable)
- `contact_method`: VARCHAR (Email or Phone)
- `status`: ENUM ('PENDING', 'NOTIFIED')
