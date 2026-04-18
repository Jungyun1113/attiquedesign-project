---
trigger: model_decision
description: when edit or create any backend code
---

# Backend Dev Instructions

## Stack
AWS Chalice + SQLModel (SQLAlchemy) + PostgreSQL + python-jose + boto3  
Entry: `app.py` → Blueprint 등록 / 모든 소스: `chalicelib/`

---

## Directory Structure
```
chalicelib/
├── api/          # 도메인별 Blueprint 라우터
├── core/         # config, db, auth, exceptions, context
├── helpers/db.py # 고수준 DB 헬퍼 (핵심)
├── models/       # SQLModel 테이블 정의
├── schemas/      # Pydantic 요청/응답 스키마
└── services/     # 외부 연동 (payment, storage)
```

---

## Existing Utilities — 재구현 금지

### DB 헬퍼 (`helpers/db.py`)
- `fetch(session, Model, **filters)` — 단건 조회; `raise_not_found=True` 시 NotFoundError
- `bulk_fetch(session, Model, filters, order_by, page, size)` → `(items, total_count)`
- `insert(session, Model, data)` — 생성 후 인스턴스 반환
- `update(session, instance, data)` — 부분 업데이트, `updated_at` 자동 갱신
- `delete(session, instance, soft=True)` — 기본 soft delete (`is_deleted=True`)

직접 `select()` 작성은 복잡한 join/집계 등 헬퍼로 처리 불가한 특수 쿼리에만 허용.

### 인증 (`core/auth.py`)
- `@require_auth` — JWT 검증, ContextVar에 user 주입; 실패 시 401
- `@require_admin` — `@require_auth` + role=ADMIN 검증; 실패 시 403
- `try_extract_user(request)` → `Optional[str]` — 선택적 인증(비회원/회원 공용 라우트)
- `create_access_token(user_id, role)`, `create_refresh_token(user_id)`, `decode_token(token)`
- `hash_password(plain)`, `verify_password(plain, hashed)`

### 컨텍스트 (`core/context.py`)
- `get_user_id()`, `get_user_role()` — ContextVar에서 현재 요청 유저 정보 조회
- `set_user(user_id, role)`, `clear_user()`

### 응답/에러 (`core/exceptions.py`)
- `success_response(data, meta=None, status_code=200)` → `{success: true, data, meta}`
- `error_response(code, message, status_code)` → `{success: false, error: {code, message}}`
- `handle_app_error(exc: AppError)` — AppError → 포맷된 Response 변환

**예외 계층:** `AppError` → `NotFoundError(404)` / `UnauthorizedError(401)` / `ForbiddenError(403)` / `ValidationError(422)` / `ConflictError(409)`

### 스토리지 (`services/storage_service.py`)
- `generate_presigned_put_url(filename, content_type, target)` → `{upload_url, object_key}`
- `get_public_url(object_key)` → S3 퍼블릭 URL

### 결제 (`services/payment_service.py`)
- `verify_webhook_signature(raw_body, signature_header)` — HMAC-SHA256
- `get_payment(payment_id)`, `verify_payment_amount(payment_id, expected_amount)`

---

## Models (`models/`)

**BaseModel** (`models/base.py`): `id(UUID)`, `created_at`, `updated_at`, `is_deleted`

| 모델 | 핵심 필드 |
|---|---|
| User | email(unique), password_hash, role(ADMIN\|USER), auth_provider |
| Product | sku(unique), category, price(Decimal), stock_quantity, status(ACTIVE\|HIDDEN\|SOLDOUT) |
| ProductImage | product_id FK, image_url, display_order, is_primary |
| Order | user_id(nullable), total_amount, status(PENDING\|PAID\|SHIPPED\|DELIVERED\|CANCELLED), pg_transaction_id |
| OrderItem | order_id FK, product_id FK, quantity, unit_price |
| Portfolio | category, title, cover_image_url |
| Selection | title, subtitle |
| Reservation | reservation_type(INTERIOR\|FURNITURE\|TOTAL), status(RECEIVED\|...\|CONTRACTED), guest_info(JSONB), dynamic_data(JSONB) |

---

## Common Patterns

### 라우트 핸들러
```python
@blueprint.route("/path", methods=["POST"], cors=True)
@require_auth  # or @require_admin; 공개 라우트는 생략
def handler():
    try:
        body = app.current_request.json_body
        # validate → raise ValidationError(...)
        with get_session() as session:
            result = insert(session, Model, body)
        return success_response(_serialize(result), status_code=201)
    except AppError as e:
        return handle_app_error(e)
```

### DB 세션
```python
with get_session() as session:  # 자동 commit/rollback
    item = fetch(session, Model, id=item_id)
    update(session, item, {"field": value})
```

### 필터링 + 페이지네이션
```python
filters = {k: v for k, v in {"category": category, "status": status}.items() if v}
items, total = bulk_fetch(session, Model, filters=filters,
                          order_by=Model.created_at.desc(), page=page, size=size)
return success_response(data, meta={"total": total, "page": page, "size": size})
```

### 직렬화
관계형 데이터는 lazy load 없음. 별도 `_serialize_*(instance)` 함수 정의 후:
- `UUID` → `str()`
- `Decimal` → `str()`
- `datetime` → `.isoformat()`
- 연관 모델은 별도 쿼리로 명시적 로드

### 선택적 인증 (비회원/회원 공용)
```python
user_id = try_extract_user(app.current_request)  # None if unauthenticated
```

### 이미지 업로드 흐름
1. `POST /uploads/presign` (@require_admin) → presigned PUT URL + object_key 반환
2. 클라이언트가 S3에 직접 PUT
3. 클라이언트가 object_key를 포함해 도메인 API 호출 → DB 저장

---

## Config (`core/config.py`)
`Settings` 싱글턴으로 모든 환경변수 접근. 직접 `os.environ` 사용 금지.  
주요 키: `DATABASE_URL`, `JWT_SECRET`, `S3_BUCKET`, `AWS_REGION`, `PORTONE_WEBHOOK_SECRET`

---

## Docs Reference
- DB 스키마: `docs/1_database_model.md`
- API 계약: `docs/2_api_spec.md`
- 아키텍처: `docs/4_backend_architecture.md`
