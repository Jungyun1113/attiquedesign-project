# Backend Architecture (AWS Chalice + SQLModel)

## 1. 설계 원칙
- **Serverless 최적화:** Cold Start 최소화를 위해 전역 로드 최소화.
- **고수준 DB 헬퍼:** Django ORM 스타일의 공통 헬퍼(`helpers/db.py`)를 통해 join, filter, pagination을 단일 인터페이스로 처리. 특수 쿼리가 아닌 경우 서비스 계층은 이 헬퍼만 사용.
- **선언적 권한 제어:** `@require_auth`, `@require_admin` 데코레이터로 라우트에 권한을 선언적으로 부여. 반복 구현 금지.
- **공통 에러 처리:** 모든 예외를 `{ success, error }` 구조로 통일하는 미들웨어 데코레이터 중앙화.

## 2. 디렉토리 구조
```text
/backend
├── app.py                      # Chalice 엔트리포인트 (Blueprint 등록)
├── chalicelib/
│   ├── api/                    # 블루프린트 라우터 (도메인별)
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── reservations.py
│   │   ├── portfolios.py
│   │   ├── selections.py
│   │   ├── uploads.py          # S3 Presigned URL 발급
│   │   └── webhooks.py
│   ├── core/                   # 시스템 코어
│   │   ├── config.py           # python-dotenv 기반 Settings 싱글턴
│   │   ├── db.py               # SQLModel 엔진 및 Session 관리
│   │   ├── auth.py             # JWT 검증 + @require_auth / @require_admin 데코레이터
│   │   └── exceptions.py       # Custom Exception 및 공통 에러 응답 포맷터
│   ├── helpers/
│   │   └── db.py               # 고수준 DB 헬퍼: fetch / bulk_fetch / insert / update / delete
│   │                           # — join, filter, pagination, soft-delete를 내재한 단일 인터페이스
│   ├── models/                 # SQLModel DB 모델 (1_database_model.md 기반)
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── reservation.py
│   │   ├── portfolio.py
│   │   └── selection.py
│   ├── schemas/                # Pydantic Request/Response 스키마
│   │   ├── requests/
│   │   └── responses/
│   └── services/               # 외부 시스템 연동 비즈니스 로직
│       ├── payment_service.py  # PG 결제 검증
│       └── storage_service.py  # S3 Presigned URL 생성
├── .env                        # 로컬 환경변수 (git 제외)
├── .env.example                # 환경변수 키 목록 (git 포함)
└── requirements.txt
```

## 3. 핵심 구현 지침

### 환경변수 관리 (`core/config.py`)
- `python-dotenv`로 `.env`를 로드하는 `Settings` 싱글턴 클래스.
- `DATABASE_URL`, `JWT_SECRET`, `S3_BUCKET`, `AWS_REGION` 등 모든 설정값을 이 객체로 접근.
- AWS SSM/Secrets Manager는 사용하지 않음.

### DB 헬퍼 (`helpers/db.py`)
서비스 계층이 직접 SQLModel `select()`를 작성하지 않도록, 아래 인터페이스를 구현:
- `fetch(Model, **filters)` — 단건 조회 (없으면 None 또는 예외)
- `bulk_fetch(Model, filters, joins, order_by, page, size)` — 다건 + 페이징
- `insert(Model, data)` — 생성 후 반환
- `update(instance, data)` — 부분 업데이트 후 반환
- `delete(instance, soft=True)` — Soft Delete 기본, hard delete 옵션

### 권한 데코레이터 (`core/auth.py`)
- `@require_auth`: JWT 유효성 검증, `request.context`에 user 주입.
- `@require_admin`: `@require_auth` + role=ADMIN 검증. 미충족 시 표준 에러 응답 반환.
- 데코레이터 미적용 라우트는 비회원 공개 접근 허용.

### S3 이미지 업로드 흐름
1. 클라이언트 → `POST /uploads/presign` (Admin 전용) → 서버가 Presigned PUT URL 반환.
2. 클라이언트 → S3에 직접 PUT 업로드.
3. 클라이언트 → 해당 모델 API(PATCH /products/{id} 등)에 `object_key`를 포함해 저장 요청.
- 구현: `services/storage_service.py`에서 `boto3.client('s3').generate_presigned_url` 사용.

### 트랜잭션 관리
- 다중 write 작업(주문 생성 + 재고 차감 등)은 `session.begin()` 컨텍스트 내에서 처리.
- 헬퍼 함수가 세션을 인자로 받아 트랜잭션 경계를 서비스 계층에서 제어.
